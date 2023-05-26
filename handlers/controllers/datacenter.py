# -*- coding: utf-8 -*-

import six

from utils.misc import format_params
from api.return_tools import return_error
from log.logger import logger
# from local
import connexion as connexion
from constants import (
    ACTION_VMWARE_MANAGER_DATACENTER_DESCRIBE_DATACENTER,
    ACTION_VMWARE_MANAGER_DATACENTER_DETAIL_DATACENTER
)
from handlers.controllers.common import (
    process_query_list_param,
    validate_user_request,
    build_params
)
from handlers.impl.datacenter_impl import (
    handle_describe_datacenter_local,
    handle_detail_datacenter_local
)


def describe_datacenter(**kwargs):
    """Describe Datacenter获取数据中心列表信息"""
    if "Channel" in connexion.request.headers:
        kwargs["channel"] = connexion.request.headers["Channel"]
    process_query_list_param(kwargs, connexion.request.args)
    logger.debug("describe_datacenter with req params: [%s]"
                 % format_params(kwargs))

    if 'body' in kwargs:
        del kwargs['body']
        body = connexion.request.get_json()
        if body:
            for k, v in six.iteritems(body):
                kwargs[k] = v
    
    action = ACTION_VMWARE_MANAGER_DATACENTER_DESCRIBE_DATACENTER
    kwargs.update({'action': action})
    valid_user, error = validate_user_request(kwargs,
                                              connexion.request)
    if not valid_user:
        return return_error(kwargs, error, dump=False)

    # build_params
    kwargs = build_params(valid_user, kwargs, connexion.request)

    return handle_describe_datacenter_local(kwargs)


def detail_datacenter(**kwargs):
    """Detail Datacenter详述数据中心信息"""
    if "Channel" in connexion.request.headers:
        kwargs["channel"] = connexion.request.headers["Channel"]
    process_query_list_param(kwargs, connexion.request.args)
    logger.debug("detail_datacenter with req params: [%s]"
                 % format_params(kwargs))

    if 'body' in kwargs:
        del kwargs['body']
        body = connexion.request.get_json()
        if body:
            for k, v in six.iteritems(body):
                kwargs[k] = v

    action = ACTION_VMWARE_MANAGER_DATACENTER_DETAIL_DATACENTER
    kwargs.update({'action': action})
    valid_user, error = validate_user_request(kwargs,
                                              connexion.request)
    if not valid_user:
        return return_error(kwargs, error, dump=False)

    # build_params
    kwargs = build_params(valid_user, kwargs, connexion.request)

    return handle_detail_datacenter_local(kwargs)
