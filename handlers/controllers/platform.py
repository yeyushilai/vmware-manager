# -*- coding: utf-8 -*-

import six

from utils.misc import format_params
from api.return_tools import return_error
from log.logger import logger
# from local
import connexion as connexion
from constants import (
    ACTION_VMWARE_MANAGER_PLATFORM_ADD_PLATFORM,
    ACTION_VMWARE_MANAGER_PLATFORM_CHECK_PLATFORM_CONNECTIVITY,
    ACTION_VMWARE_MANAGER_PLATFORM_DELETE_PLATFORM,
    ACTION_VMWARE_MANAGER_PLATFORM_DESCRIBE_PLATFORM,
    ACTION_VMWARE_MANAGER_PLATFORM_UPDATE_PLATFORM,
)
from handlers.controllers.common import (
    process_query_list_param,
    validate_user_request,
    build_params
)
from handlers.impl.platform_impl import (
    handle_add_platform_local,
    handle_check_platform_connectivity_local,
    handle_delete_platform_local,
    handle_describe_platform_local,
    handle_update_platform_local,
)


def check_platform_connectivity(**kwargs):
    """Check Platform Connectivity检测平台的连通性"""
    if "Channel" in connexion.request.headers:
        kwargs["channel"] = connexion.request.headers["Channel"]
    process_query_list_param(kwargs, connexion.request.args)
    logger.debug("check_platform_connectivity with req params: [%s]"
                 % format_params(kwargs))

    if 'body' in kwargs:
        del kwargs['body']
        body = connexion.request.get_json()
        if body:
            for k, v in six.iteritems(body):
                kwargs[k] = v

    action = ACTION_VMWARE_MANAGER_PLATFORM_CHECK_PLATFORM_CONNECTIVITY
    kwargs.update({'action': action})
    valid_user, error = validate_user_request(kwargs,
                                              connexion.request)
    if not valid_user:
        return return_error(kwargs, error, dump=False)

    # build_params
    kwargs = build_params(valid_user, kwargs, connexion.request)

    return handle_check_platform_connectivity_local(kwargs)


def add_platform(**kwargs):
    """Add Platform添加平台"""
    if "Channel" in connexion.request.headers:
        kwargs["channel"] = connexion.request.headers["Channel"]
    process_query_list_param(kwargs, connexion.request.args)
    logger.debug("add_platform with req params: [%s]"
                 % format_params(kwargs))

    if 'body' in kwargs:
        del kwargs['body']
        body = connexion.request.get_json()
        if body:
            for k, v in six.iteritems(body):
                kwargs[k] = v

    action = ACTION_VMWARE_MANAGER_PLATFORM_ADD_PLATFORM
    kwargs.update({'action': action})
    valid_user, error = validate_user_request(kwargs,
                                              connexion.request)
    if not valid_user:
        return return_error(kwargs, error, dump=False)

    # build_params
    kwargs = build_params(valid_user, kwargs, connexion.request)

    return handle_add_platform_local(kwargs)


def delete_platform(**kwargs):
    """Delete Platform删除平台"""
    if "Channel" in connexion.request.headers:
        kwargs["channel"] = connexion.request.headers["Channel"]
    process_query_list_param(kwargs, connexion.request.args)
    logger.debug("delete_platform with req params: [%s]"
                 % format_params(kwargs))

    if 'body' in kwargs:
        del kwargs['body']
        body = connexion.request.get_json()
        if body:
            for k, v in six.iteritems(body):
                kwargs[k] = v
    
    action = ACTION_VMWARE_MANAGER_PLATFORM_DELETE_PLATFORM
    kwargs.update({'action': action})
    valid_user, error = validate_user_request(kwargs,
                                              connexion.request)
    if not valid_user:
        return return_error(kwargs, error, dump=False)

    # build_params
    kwargs = build_params(valid_user, kwargs, connexion.request)

    return handle_delete_platform_local(kwargs)


def describe_platform(**kwargs):
    """Describe Platform获取平台列表信息"""
    if "Channel" in connexion.request.headers:
        kwargs["channel"] = connexion.request.headers["Channel"]
    process_query_list_param(kwargs, connexion.request.args)
    logger.debug("describe_platform with req params: [%s]"
                 % format_params(kwargs))

    if 'body' in kwargs:
        del kwargs['body']
        body = connexion.request.get_json()
        if body:
            for k, v in six.iteritems(body):
                kwargs[k] = v
    
    action = ACTION_VMWARE_MANAGER_PLATFORM_DESCRIBE_PLATFORM
    kwargs.update({'action': action})
    valid_user, error = validate_user_request(kwargs,
                                              connexion.request)
    if not valid_user:
        return return_error(kwargs, error, dump=False)

    # build_params
    kwargs = build_params(valid_user, kwargs, connexion.request)

    return handle_describe_platform_local(kwargs)


def update_platform(**kwargs):
    """Update Platform更新平台信息"""
    if "Channel" in connexion.request.headers:
        kwargs["channel"] = connexion.request.headers["Channel"]
    process_query_list_param(kwargs, connexion.request.args)
    logger.debug("update_platform with req params: [%s]"
                 % format_params(kwargs))

    if 'body' in kwargs:
        del kwargs['body']
        body = connexion.request.get_json()
        if body:
            for k, v in six.iteritems(body):
                kwargs[k] = v
    
    action = ACTION_VMWARE_MANAGER_PLATFORM_UPDATE_PLATFORM
    kwargs.update({'action': action})
    valid_user, error = validate_user_request(kwargs,
                                              connexion.request)
    if not valid_user:
        return return_error(kwargs, error, dump=False)

    # build_params
    kwargs = build_params(valid_user, kwargs, connexion.request)

    return handle_update_platform_local(kwargs)
