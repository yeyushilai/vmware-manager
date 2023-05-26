# -*- coding: utf-8 -*-

"""功能：API接口层面的SQL操作"""

import json
from copy import deepcopy

from db.constants import DB_VMWARE_MANAGER
from db.constants import TB_VMWARE_MANAGER_PLATFORM
from log.logger import logger
from utils.global_conf import get_pg
from utils.misc import get_current_time
from db.data_types import SearchWordType

MIN_CONNECT = 0
MAX_CONNECT = 100


class PGInterface(object):
    def __init__(self, db, min_connect, max_connect):
        self.pg_name = db
        self.min_connect = min_connect
        self.max_connect = max_connect
        self.client_delegator = self.gen_client_delegator()

    def gen_client_delegator(self):
        return get_pg(self.pg_name, self.min_connect, self.max_connect)


class VMwareManagerPGInterface(PGInterface):
    pg_name = DB_VMWARE_MANAGER
    pg_table_platform = TB_VMWARE_MANAGER_PLATFORM
    max_query_count = 1000

    def __init__(self, min_connect=MIN_CONNECT, max_connect=MAX_CONNECT):
        super(VMwareManagerPGInterface, self).__init__(self.pg_name,
                                                       min_connect,
                                                       max_connect)

    def create_platform(self, columns):
        columns_copy = deepcopy(columns)
        if isinstance(columns_copy["platform_resource"], list):
            columns_copy["platform_resource"] = json.dumps(
                columns_copy["platform_resource"])
        columns_copy["record_create_time"] = get_current_time()
        columns_copy["record_update_time"] = get_current_time()
        self.client_delegator.base_insert(table=self.pg_table_platform,
                                          columns=columns_copy)

    def list_platform(self, user_id=None, platform_user=None,
                      platform_host=None, platform_name=None,
                      is_deleted=False, search_word=None,
                      limit=None, offset=None,
                      sort_key=None, reverse=None):
        condition = dict()
        condition["is_deleted"] = is_deleted
        if user_id:
            condition["user_id"] = user_id
        if platform_user:
            condition["platform_user"] = platform_user
        if platform_host:
            condition["platform_host"] = platform_host
        if platform_name:
            condition["platform_name"] = platform_name
        if search_word:
            condition["search_word"] = SearchWordType(search_word)
        platforms = self.client_delegator.base_get(
            table=self.pg_table_platform,
            condition=condition,
            limit=limit,
            offset=offset,
            sort_key=sort_key,
            reverse=reverse)
        if not platforms:
            log_msg = "VMware vSphere platform not exists, user id: " \
                      "{user_id}".format(user_id=user_id)
            logger.info(log_msg)
            return None

        for platform in platforms:
            if isinstance(platform["platform_resource"], str):
                platform["platform_resource"] = json.loads(
                    platform["platform_resource"])
        return platforms

    def query_platform(self, platform_id, is_deleted=False):
        condition = dict(platform_id=platform_id.strip(), is_deleted=is_deleted)
        platforms = self.client_delegator.base_get(
            table=self.pg_table_platform,
            condition=condition,
            limit=self.max_query_count)
        if not platforms:
            log_msg = "VMware vSphere platform not exists, platform id: " \
                      "{platform_id}".format(platform_id=platform_id)
            logger.info(log_msg)
            return None
        platform = platforms[0]
        if isinstance(platform["platform_resource"], str):
            platform["platform_resource"] = json.loads(
                platform["platform_resource"])
        if "is_deleted" in platform:
            del platform["is_deleted"]
        return platform

    def update_platform(self, platform_id, platform_info):
        platform_info_copy = deepcopy(platform_info)
        platform_info_copy["record_update_time"] = get_current_time()
        if isinstance(platform_info_copy["platform_resource"], list):
            platform_info_copy["platform_resource"] = json.dumps(
                platform_info_copy["platform_resource"])
        self.client_delegator.base_update(
            table=self.pg_table_platform,
            condition=dict(platform_id=platform_id),
            columns=platform_info_copy)

    def delete_platform(self, platform_id=None, user_id=None):
        condition = dict()
        if platform_id:
            condition["platform_id"] = platform_id
        if user_id:
            condition["user_id"] = user_id
        self.client_delegator.base_delete(
            table=self.pg_table_platform,
            condition=condition)

    def get_platform_count(self, user_id=None, search_word=None, is_deleted=False):
        condition = dict()
        if user_id:
            condition["user_id"] = user_id
        if search_word:
            condition["search_word"] = SearchWordType(search_word)
        condition["is_deleted"] = is_deleted
        count_set = self.client_delegator.base_get_count(
            table=self.pg_table_platform, condition=condition)
        return int(count_set[0].get("count"))
