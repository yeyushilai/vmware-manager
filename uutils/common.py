# -*- coding: utf-8 -*-

import base64
import datetime
import hashlib
import itertools
import uuid

from Crypto.Cipher import AES


def chunked(it, n):
    """手动分页"""
    marker = object()
    for group in (list(g) for g in itertools.izip_longest(
            *[iter(it)] * n, fillvalue=marker)):
        if group[-1] is marker:
            del group[group.index(marker):]
        yield group


def order_list_and_paginate(target_list, sort_key, offset, limit, reverse=False):
    length = len(target_list)
    if length == 0:
        return target_list, length
    page = offset // limit
    target_list.sort(key=lambda x: x.get(sort_key), reverse=reverse)
    if limit <= 0:
        raise Exception("limit must gte 0")
    elif page > (length // limit):
        raise Exception("offset:[%s] out target_list paginate index[%s]" % (offset, length // limit))
    chunk_res = chunked(target_list, limit)
    chunk = next(itertools.islice(chunk_res, page, None))
    return chunk, length


# 检验是否全是中文字符
def is_all_chinese(strs):
    for _char in strs.decode("utf-8"):
        if not u'\u4e00' <= _char <= u'\u9fff':
            return False
    return True


# 检验是否含有中文字符
def is_contains_chinese(strs):
    for _char in strs.decode("utf-8"):
        if u'\u4e00' <= _char <= u'\u9fff':
            return True
    return False


# 生成uuid
def generate_uuid():
    return str(uuid.uuid4()).replace("-", "")


# 生成VMware vSphere平台ID
def generate_platform_id():
    return "-".join(["plf", generate_uuid()[0:8]])


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


def dict_to_obj(dict_obj):
    if not isinstance(dict_obj, dict):
        return dict_obj
    d = Dict()
    for k, v in dict_obj.items():
        d[k] = dict_to_obj(v)
    return d


def get_format_datetime(m_datetime, s_format="%Y-%m-%dT%H:%M:%SZ"):
    """
    返回datetime的格式字符
    """
    return m_datetime.strftime(s_format)


def md5(s):
    if type(s) == str:
        s = s.encode("utf-8")
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


def aes_decode(text):
    # 额外的处理

    text = str(text)
    enc = base64.urlsafe_b64decode(text)
    key = "MFwwDQYJKoZIhvcA"
    iv = key.decode('utf-8')
    key = key.decode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    dec = cipher.decrypt(enc)
    return str(dec[0:-ord(dec[-1])].decode('utf-8'))


def format_value_by_timeslice(value, start_time, metric, interval):
    # 将数据按照时间片段分组
    monitor_data = []
    slice_start_time = start_time
    for item in value:
        item = float(item)
        item = 0 if item < 0 else item
        slice_end_time = slice_start_time + datetime.timedelta(seconds=20)
        if metric in ("cpu", "memory", "disk_us"):
            item = round(item / 100, 2) 
        monitor_data.append({
            "start_time":
            slice_start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time":
            slice_end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "avg_value":
            item
        })
        slice_start_time = slice_end_time
    
    # 获取实时数据
    if interval == 0:
        monitor_data = [monitor_data[-1]]
    else:
        # 获取最近interval分钟数据
        last_interval_data_count = interval * 3
        if len(monitor_data) >= last_interval_data_count:
            monitor_data = monitor_data[-last_interval_data_count:]
    return monitor_data