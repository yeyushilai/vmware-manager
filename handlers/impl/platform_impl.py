# -*- coding: utf-8 -*-

from log.logger import logger
from utils.misc import get_current_time

from resource_control.vmware_vsphere import VMwareVSphere
from uutils.pg import VMwareManagerPGInterface
from uutils.common import generate_platform_id
from error import (
    Error,
    ErrorMsg,
    ErrorCode
)
from return_tools import (
    return_error,
    return_success,
)
from constants import PlatformStatus


def handle_check_platform_connectivity_local(kwargs):
    """检查与VMware vSphere平台的连通性"""
    logger.debug('handle check platform connectivity local start, {}'.format(kwargs))

    host = kwargs.get("host")
    if host.startswith("http://"):
        host = host.strip("http://")
    elif host.startswith("https://"):
        host = host.strip("https://")
    if host.endswith("/"):
        host = host.strip("/")

    account = dict()
    account["host"] = host
    account["port"] = int(kwargs.get("port"))
    account["username"] = kwargs.get("username")
    account["encrypt_password"] = kwargs.get("encrypt_password")

    vs = VMwareVSphere(account)
    if not vs.is_connected():
        logger.exception("connect to VMware vSphere platform failed, platform "
                         "host: {host}".format(host=account["host"]))
        return return_error(kwargs,
                            Error(ErrorCode.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value,
                                  ErrorMsg.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value),
                            dump=False)

    return return_success(kwargs, None, dump=False)


def handle_add_platform_local(kwargs):
    """添加VMware vSphere平台"""
    logger.debug('handle add platform local start, {}'.format(kwargs))

    host = kwargs.get("host")
    if host.startswith("http://"):
        host = host.strip("http://")
    elif host.startswith("https://"):
        host = host.strip("https://")
    if host.endswith("/"):
        host = host.strip("/")

    account = dict()
    account["host"] = host
    account["port"] = int(kwargs.get("port"))
    account["username"] = kwargs.get("username")
    account["encrypt_password"] = kwargs.get("encrypt_password")

    user_id = kwargs.get("user_id")
    platform_name = kwargs.get("name")
    platform_desc = kwargs.get("desc")

    pi = VMwareManagerPGInterface()

    # 重复性检测
    platforms = pi.list_platform(user_id=user_id,
                                 platform_host=account["host"],
                                 platform_user=account["username"])
    if platforms:
        logger.error("platform has aleady exists, platform host: "
                     "{platform_host}, platform user: {platform_user}"
                     "".format(platform_host=account["host"],
                               platform_user=account["username"]))
        return return_error(kwargs,
                            Error(ErrorCode.ERROR_VMWARE_VSPHERE_PLATFORM_EXISTS.value,
                                  ErrorMsg.ERROR_VMWARE_VSPHERE_PLATFORM_EXISTS.value),
                            dump=False)

    # 联通性检测
    vs = VMwareVSphere(account)
    if not vs.is_connected():
        logger.exception("connect to VMware vSphere platform failed, platform "
                         "host: {host}".format(host=account["host"]))
        return return_error(kwargs,
                            Error(ErrorCode.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value,
                                  ErrorMsg.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value),
                            dump=False)

    # 从VMware vSphere平台获取信息
    platform_resource = vs.list_datacenter()
    platform_version = vs.vi.version

    # 添加VMware vSphere平台
    platform_id = generate_platform_id()
    platform_info = {
        "platform_id": platform_id,
        "user_id": user_id,
        "platform_name": platform_name,
        "platform_desc": platform_desc,
        "platform_host": account["host"],
        "platform_port": account["port"],
        "platform_user": account["username"],
        "platform_password": account["encrypt_password"],
        "platform_resource": platform_resource,
        "platform_status": PlatformStatus.CONNECTED.value,
        "platform_version": platform_version,
        "manage_time": get_current_time(),
        "is_deleted": False
    }
    pi.create_platform(platform_info)
    data = dict(platform_id=platform_id)
    return return_success(kwargs, data, dump=False)


def handle_describe_platform_local(kwargs):
    """列举VMware vSphere平台列表"""
    logger.debug('handle describe platform local start, {}'.format(kwargs))

    user_id = kwargs.get("user_id")
    offset = kwargs.get("offset") or 0
    limit = kwargs.get("limit") or 10
    search_word = kwargs.get("search_word")
    sort_key = kwargs.get("sort_key") or "platform_name"
    reverse = bool(kwargs.get("reverse"))

    pi = VMwareManagerPGInterface()
    count = pi.get_platform_count(user_id=user_id, search_word=search_word) or 0
    platforms = pi.list_platform(user_id=user_id, search_word=search_word,
                                 limit=limit, offset=offset,
                                 sort_key=sort_key, reverse=reverse) or []

    data = dict(datas=platforms, count=count)
    return return_success(kwargs, data, dump=False)


def handle_update_platform_local(kwargs):
    """更新VMware vSphere平台"""
    logger.debug('handle update platform local start, {}'.format(kwargs))

    platform_id = kwargs.get("platform_id")
    platform_name = kwargs.get("name")
    platform_desc = kwargs.get("desc")

    host = kwargs.get("host")
    if host.startswith("http://"):
        host = host.strip("http://")
    elif host.startswith("https://"):
        host = host.strip("https://")
    if host.endswith("/"):
        host = host.strip("/")

    account = dict()
    account["host"] = host
    account["port"] = int(kwargs.get("port"))
    account["username"] = kwargs.get("username")
    account["encrypt_password"] = kwargs.get("encrypt_password")
    pi = VMwareManagerPGInterface()

    # 存在性检测
    platform = pi.query_platform(platform_id=platform_id)
    if not platform:
        logger.error("platform do not exists, platform id: {platform_id}"
                     "".format(platform_id=platform_id))
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_PLATFORM_NOT_EXISTS.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_PLATFORM_NOT_EXISTS.value),
                            dump=False)

    # 联通性检测
    vs = VMwareVSphere(account)
    if not vs.is_connected():
        logger.exception("connect to VMware vSphere platform failed, platform "
                         "host: {host}".format(host=account["host"]))
        return return_error(kwargs,
                            Error(ErrorCode.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value,
                                  ErrorMsg.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value),
                            dump=False)

    # 从VMware vSphere平台获取信息
    platform_resource = vs.list_datacenter()
    platform_version = vs.vi.version

    # 更新VMware vSphere信息
    platform_info = {
        "platform_host": account["host"],
        "platform_port": account["port"],
        "platform_user": account["username"],
        "platform_password": account["encrypt_password"],
        "platform_name": platform_name,
        "platform_desc": platform_desc,
        "platform_resource": platform_resource,
        "platform_version": platform_version,
        "platform_status": PlatformStatus.CONNECTED.value
    }
    pi.update_platform(platform_id, platform_info)
    data = dict(platform_info=platform_info)
    return return_success(kwargs, data, dump=False)


def handle_delete_platform_local(kwargs):
    """删除VMware vSphere平台"""
    logger.debug('handle delete platform local start, {}'.format(kwargs))

    platform_id = kwargs.get("platform_id")
    pi = VMwareManagerPGInterface()

    # 存在性检测
    platform = pi.query_platform(platform_id=platform_id)
    if not platform:
        logger.error("platform do not exists, platform id: {platform_id}"
                     "".format(platform_id=platform_id))
        return return_error(kwargs,
                            Error(ErrorCode.ERROR_VMWARE_VSPHERE_PLATFORM_NOT_EXISTS.value,
                                  ErrorMsg.ERROR_VMWARE_VSPHERE_PLATFORM_NOT_EXISTS.value),
                            dump=False)

    pi.delete_platform(platform_id)
    data = dict(platform_id=platform_id)
    return return_success(kwargs, dict(data=data), dump=False)
