
from qingcloud.iaas import APIConnection
from log.logger import logger

import context as context
from common.misc import (
    get_cache,
    set_cache
)
from constants import (
    ACTION_DESCRIBE_USERS,
    ACTION_DESCRIBE_SUB_USERS,
    ACTION_DESCRIBE_USER_LOCKS,
    ACTION_DESCRIBE_ACCOUNT_QUOTAS,
    ACTION_DESCRIBE_ACCESS_KEYS,
    ACTION_DESCRIBE_DEFAULT_ZONES,
    ACTION_DESCRIBE_ZONES,
    ACTION_DESCRIBE_LOGIN_SERVERS,
    ACTION_DESCRIBE_LOGIN_ACCOUNT_USERS,
    ACTION_DESCRIBE_LOGIN_ACCOUNTS,

    MC_KEY_PREFIX_ACCOUNT_USER_INFO,
    MC_KEY_PREFIX_ACCOUNT_SUB_USER_INFO,
    MC_KEY_PREFIX_ACCOUNT_ACCESS_KEY,
    MC_KEY_PREFIX_ACCOUNT_QUOTA,
    MC_KEY_PREFIX_ACCOUNT_USER_LOCK,
    MC_KEY_PREFIX_ACCOUNT_USER_ZONE,
    MC_KEY_PREFIX_ZONES,
)


class IaasClient:
    def __init__(self, conf):
        self.iaas_client = APIConnection(conf.get('qy_access_key_id'),
                                         conf.get('qy_secret_access_key'),
                                         conf.get('zone', 'test'),
                                         host=conf.get('host'),
                                         port=conf.get('port'),
                                         protocol=conf.get('protocol'))

    def send_request(self, action, req, url='/iaas/', verb='GET'):
        try:
            return self.iaas_client.send_request(action, req,
                                                 url=url, verb=verb)
        except Exception as e:
            logger.error("send iaas request failed, req=[%s] Exception[%s]"
                         % (req, e))
            # if request timeout, None will be returned
            return None


def get_user(user_id, refresh=False):
    if not user_id:
        logger.error("invalid user_id [%s]" % user_id)
        return None

    if not refresh:
        ret = get_cache(MC_KEY_PREFIX_ACCOUNT_USER_INFO, user_id)
        if ret:
            logger.debug("get user [%s] from cache successfully", user_id)
            return ret

    req = {
        'users': [user_id],
    }
    action = ACTION_DESCRIBE_USERS

    ret = None
    ctx = context.instance()
    iaas_client = IaasClient(ctx.iaas_client_conf)
    resp = iaas_client.send_request(action, req)
    if not isinstance(resp, dict) or resp.get('ret_code') != 0:
        logger.error("get data from iaas failed, action=[%s] resp[%s]"
                     % (action, resp))
        return ret

    data_set = resp.get('user_set', [])
    if not data_set:
        return ret

    _user = data_set[0]

    set_cache(MC_KEY_PREFIX_ACCOUNT_USER_INFO, user_id, _user)

    return _user


def get_sub_users(user_id, refresh=True):
    if not user_id:
        logger.error("invalid user_id [%s]" % user_id)
        return None

    if not refresh:
        ret = get_cache(MC_KEY_PREFIX_ACCOUNT_SUB_USER_INFO, user_id)
        if ret:
            logger.debug("get [%s] sub user from cache successfully", user_id)
            return ret

    req = {
        'owner': user_id,
        'status': 'active',
    }
    action = ACTION_DESCRIBE_SUB_USERS

    ret = None
    ctx = context.instance()
    iaas_client = IaasClient(ctx.iaas_client_conf)
    resp = iaas_client.send_request(action, req)
    if not isinstance(resp, dict) or resp.get('ret_code') != 0:
        logger.error("get data from iaas failed, action=[%s] resp[%s]"
                     % (action, resp))
        return ret

    user_set = resp.get('user_set', [])
    if not user_set:
        return []

    set_cache(MC_KEY_PREFIX_ACCOUNT_SUB_USER_INFO, user_id, user_set)
    return user_set


def get_access_key(access_key_id, refresh=False):
    if not access_key_id:
        logger.error("invalid access_key [%s]", access_key_id)
        return None

    if not refresh:
        ret = get_cache(MC_KEY_PREFIX_ACCOUNT_ACCESS_KEY, access_key_id)
        if ret:
            logger.debug("get access_key [%s] from cache successfully"
                         % access_key_id)
            return ret

    req = {
        'access_keys': [access_key_id],
    }
    action = ACTION_DESCRIBE_ACCESS_KEYS

    ret = None
    ctx = context.instance()
    iaas_client = IaasClient(ctx.iaas_client_conf)
    resp = iaas_client.send_request(action, req)
    if not isinstance(resp, dict) or resp.get('ret_code') != 0:
        logger.error("get data from iaas failed, action=[%s] resp[%s]"
                     % (action, resp))
        return ret

    data_set = resp.get('access_key_set', [])
    if not data_set:
        return ret

    _access_key = data_set[0]

    set_cache(MC_KEY_PREFIX_ACCOUNT_ACCESS_KEY, access_key_id, _access_key)

    return _access_key


def get_account_quota(user_id, refresh=False):
    if not refresh:
        ret = get_cache(MC_KEY_PREFIX_ACCOUNT_QUOTA, user_id)
        if ret:
            logger.debug("get account quota [%s] from cache successfully"
                         % user_id)
            return ret

    req = {
        'users': [user_id],
    }
    action = ACTION_DESCRIBE_ACCOUNT_QUOTAS

    ret = None
    ctx = context.instance()
    iaas_client = IaasClient(ctx.iaas_client_conf)
    resp = iaas_client.send_request(action, req)
    if not isinstance(resp, dict) or resp.get('ret_code') != 0:
        logger.error("get data from iaas failed, action=[%s] resp[%s]"
                     % (action, resp))
        return ret

    data_set = resp.get('account_quota_set', [])
    if not data_set:
        return ret

    _quota = data_set[0]

    set_cache(MC_KEY_PREFIX_ACCOUNT_QUOTA, user_id, _quota)

    return _quota


# User lock
def check_user_lock(user_id, lock_type, api_action=None, refresh=False):
    """
        NOTE:
            As we cannot delete keys with prefix in memcached,
            we simply set user lock cache here without `api_action`.
            So do NOT pass `api_action` in internal request either.
    """

    _key = "%s.%s" % (user_id, lock_type)
    if api_action:
        _key = "%s.%s.%s" % (user_id, lock_type, api_action)
    if not refresh:
        ret = get_cache(MC_KEY_PREFIX_ACCOUNT_USER_LOCK, _key)
        if ret is not None:
            logger.debug("get user_lock [%s] from cache successfully, "
                         "ret: [%s]" % (_key, ret))
            return ret

    req = {
        'users': [user_id],
    }
    action = ACTION_DESCRIBE_USER_LOCKS

    ret = None
    ctx = context.instance()
    iaas_client = IaasClient(ctx.iaas_client_conf)
    resp = iaas_client.send_request(action, req)
    if not isinstance(resp, dict) or resp.get('ret_code') != 0:
        logger.error("get data from iaas failed, action=[%s] resp[%s]"
                     % (action, resp))
        return ret
    else:
        logger.debug("get user lock from iaas suc, req=[%s] resp[%s]"
                     % (req, resp))

    data_set = resp.get('user_lock_set', [])
    if not data_set or not data_set[0] or \
            str(data_set[0]['status']) == 'unlock':
        user_lock_status = "unlocked"
    else:
        user_lock_status = "locked"

    set_cache(MC_KEY_PREFIX_ACCOUNT_USER_LOCK, _key, user_lock_status)

    return user_lock_status


def get_user_default_zone(user_id, region_id, refresh=True):
    # get default zone for zone in a region

    # get from cache
    if not refresh:
        user_zones = get_cache(MC_KEY_PREFIX_ACCOUNT_USER_ZONE, user_id)
        if user_zones:
            zone_info = user_zones.get(region_id, None)
            if zone_info:
                return zone_info['default_zone']
            # for region_id, zone_info in user_zones.items():
            #     zone_region = zone_info['default_in_region']
            #     if zone_region == region_id:
            #         return zone_id

    req = {
        'users': [user_id],
    }
    action = ACTION_DESCRIBE_DEFAULT_ZONES

    ret = None
    ctx = context.instance()
    iaas_client = IaasClient(ctx.iaas_client_conf)
    resp = iaas_client.send_request(action, req)
    if not isinstance(resp, dict) or resp.get('ret_code') != 0:
        logger.error("get data from iaas failed, action=[%s] resp[%s]"
                     % (action, resp))
        return ret

    data_set = resp.get('default_zone_set', [])
    if not data_set:
        return ret

    _user_zones = {}
    default_zone = None
    for zone_info in data_set:
        rid = zone_info['region']['region_id']
        _user_zones[rid] = zone_info
        if region_id == rid:
            default_zone = zone_info['default_zone']

    set_cache(MC_KEY_PREFIX_ACCOUNT_USER_ZONE, user_id, _user_zones)

    return default_zone


def get_all_zones(refresh=False):
    """
    get default zone for zone in a region
    :param refresh:
    :return:
    """

    # get from cache
    if not refresh:
        all_zones = get_cache(MC_KEY_PREFIX_ZONES, 'all')
        if all_zones:
            return all_zones

    req = {
    }
    action = ACTION_DESCRIBE_ZONES

    ret = None
    ctx = context.instance()
    iaas_client = IaasClient(ctx.iaas_client_conf)
    resp = iaas_client.send_request(action, req)
    if not isinstance(resp, dict) or resp.get('ret_code') != 0:
        logger.error("get data from iaas failed, action=[%s] resp[%s]"
                     % (action, resp))
        return ret

    data_set = resp.get('zone_set', [])
    if not data_set:
        logger.error("get all zone %s fail from iaas" % data_set)
        return ret

    all_zones = {}
    logger.debug("get all zone %s suc from iaas" % data_set)
    for zone_info in data_set:
        zone_id = zone_info['zone_id']
        all_zones[zone_id] = zone_info

    set_cache(MC_KEY_PREFIX_ZONES, 'all', all_zones)

    return all_zones


def describe_login_account_users(user_ids):
    """
    get login account users by iaas user
    :param user_ids:["",""] id of iaas user
    """
    if not user_ids:
        logger.error("invalid user_ids [%s]" % user_ids)
        return None

    req = {
        "users": user_ids,
        "status": ["active"],
        # "login_accounts": []
    }
    action = ACTION_DESCRIBE_LOGIN_ACCOUNT_USERS

    ret = None
    ctx = context.instance()
    iaas_client = IaasClient(ctx.iaas_client_conf)
    rsp = iaas_client.send_request(action, req)
    if not isinstance(rsp, dict) or rsp.get('ret_code') != 0:
        logger.error("get data from iaas failed, action=[%s] rsp[%s]"
                     % (action, rsp))
        return ret
    return rsp


def describe_login_accounts(login_accounts):
    """
    get login account users by iaas user
    :param login_accounts:["",""] id of login account
    """
    if not login_accounts:
        logger.error("invalid user_ids [%s]" % login_accounts)
        return None

    req = {
        "login_accounts": login_accounts,
        "status": ["active"],
        # "accounts": [],
        # "login_server": "",
    }
    action = ACTION_DESCRIBE_LOGIN_ACCOUNTS

    ret = None
    ctx = context.instance()
    iaas_client = IaasClient(ctx.iaas_client_conf)
    rsp = iaas_client.send_request(action, req)
    if not isinstance(rsp, dict) or rsp.get('ret_code') != 0:
        logger.error("get data from iaas failed, action=[%s] rsp[%s]"
                     % (action, rsp))
        return ret
    return rsp


def describe_login_servers(login_servers):
    """
    get login servers from iaas
    :param login_servers:["",""] ids of login server
    """
    if not login_servers:
        logger.error("invalid login_servers [%s]" % login_servers)
        return None

    req = {
        "login_servers": login_servers,
        "status": ["active"],
        # "server_type": "",
    }
    action = ACTION_DESCRIBE_LOGIN_SERVERS

    ret = None
    ctx = context.instance()
    iaas_client = IaasClient(ctx.iaas_client_conf)
    rsp = iaas_client.send_request(action, req)
    if not isinstance(rsp, dict) or rsp.get('ret_code') != 0:
        logger.error("get data from iaas failed, action=[%s] rsp[%s]"
                     % (action, rsp))
        return ret
    return rsp
