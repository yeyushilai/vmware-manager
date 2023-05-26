# -*- coding: utf-8 -*-

from utils.misc import (
    format_params,
)
from utils.time_stamp import (
    parse_ts,
    get_expired_ts,
    get_ts,
    cmp_ts,
)
from log.logger import logger
from api.constants import SUPPORTED_LANGS, CHANNEL_API
from api.error import Error
import api.error_code as ErrorCodes
import api.error_msg as ErrorMsg
# from local
import context as context
from constants import (
    REQ_EXPIRED_INTERVAL,
    CONTROLLER_PITRIX,
    NORMAL_PRIVILEGE,
    ROLE_NORMAL_USER,
    API_TYPE_VMWARE_MANAGER,
)
from resource_control.iaas.api_access import (
    check_user_access,
    check_api_access_control
)


def _get_sender(user):
    sender = {'user_id': user['user_id'],
              'privilege': user['privilege'],
              'role': user['role'],
              'console_id': user['console_id'],
              'root_user_id': user['root_user_id'],
              'lang': user['lang']}
    return sender


def process_query_list_param(params, query):
    query = dict(query)
    for key in params:
        if key not in query:
            continue
        # logger.error("in process_query_list_param query [%s]"
        #              % (query))
        value = query[key]
        if type(value) is list and len(value) > 1:
            logger.error("update [%s|%s] in params to [%s]"
                         % (key, params[key], value))
            params[key] = value


def _check_expires(params, request):
    """
    check expires of request
    :param request:
    :return:
    """
    # either "expires" or "time_stamp" should be contained in params
    if "expires" not in params and "timestamp" not in params:
        logger.error("both [expires] and [timestamp] not found in params [%s]"
                     % params)
        err = Error(ErrorCodes.INVALID_REQUEST_FORMAT,
                    ErrorMsg.ERR_MSG_MISSING_PARAMETER,
                    "expires or timestamp")
        return False, err

    # check time stamp format
    for param in ["expires", "timestamp"]:
        if param not in params:
            continue
        if 0 == parse_ts(params[param]):
            logger.error("[%s]'s format is incorrect in request [%s]"
                         % (param, params))
            err = Error(ErrorCodes.INVALID_REQUEST_FORMAT,
                        ErrorMsg.ERR_MSG_ILLEGAL_TIMESTAMP, param)
            return False, err

    current_time = get_ts()
    expires = params.get("expires", None)
    if not expires:
        expires = get_expired_ts(params['timestamp'], REQ_EXPIRED_INTERVAL)
    # request is expires if current_time greater than expires
    if 1 == cmp_ts(current_time, expires):
        logger.error("request [%s] is expired, current_time [%s], expires [%s]"
                     % (params, current_time, expires))
        err = Error(ErrorCodes.REQUEST_HAS_EXPIRED)
        return False, err
    return True, None


def validate_user_request(params, request):
    """
    check user request  parameters
    :param params: params from connexion
    :param request: flask request
    :param action: the expected action for this request
    :return: True if user request can handle furthermore, otherwise False
    """

    # check if user request expired
    is_valid, err = _check_expires(params, request)
    if not is_valid:
        return None, err

    is_pitrix_request = False
    key_controller = params['token_info']['access_key'].get('controller')
    if key_controller is CONTROLLER_PITRIX:
        is_pitrix_request = True

    # check if user can access
    user_info = params['user']
    action = params['action']
    api_type = API_TYPE_VMWARE_MANAGER
    user, err = check_user_access(user_info, api_type, action, is_pitrix_request)
    if err:
        return None, err

    # check api access
    # fixme: remove default CHANNEL_API.
    channel = params.get("channel", CHANNEL_API)
    sender = _get_sender(user_info)
    ret, err = check_api_access_control(action, sender, channel)
    if not ret:
        return None, err

    return user_info, None


def build_params(user, params, request):
    """
    build parameters
    :param user:
    :param params:
    :param request:
    :return:
    """

    ctx = context.instance()
    new_params = {}
    # remove token_info from the param list(send to fg)
    if 'token_info' in params:
        del params['token_info']
    # remove user from the param list(send to fg)
    if 'user' in params:
        del params['user']

    for k in params:
        new_params[k] = params[k]

    # wheather the request is sent through a secure path
    is_secure = False
    server_port = request.headers.environ.get('SERVER_PORT')
    if int(server_port) in ctx.secure_ports:
        is_secure = True

    logger.debug("server_port: %s, ctx.secure_ports: %s, is_secure: %s"
                 % (server_port, ctx.secure_ports, is_secure))

    # request sender infomation
    # init sender
    sender = _get_sender(user)
    if params.get('api_lang') in SUPPORTED_LANGS:
        lang = params['api_lang']
    else:
        lang = ErrorMsg.EN
    sender.update({'lang': lang})
    sender.update({'channel': params.get("channel", CHANNEL_API)})

    # mgmt request should be sent from secure path
    if not is_secure:
        sender["privilege"] = NORMAL_PRIVILEGE
        sender["role"] = ROLE_NORMAL_USER

    # add auth and expires
    new_params["sender"] = sender
    new_params["expires"] = get_expired_ts(get_ts(), REQ_EXPIRED_INTERVAL)
    logger.info("build request [%s] finished." % format_params(new_params))
    return new_params
