# -*- coding: utf-8 -*-

import six

from utils.misc import format_params
from api.return_tools import return_error
from log.logger import logger
# from local
import connexion as connexion
from constants import (
    ACTION_VMWARE_MANAGER_VM_DESCRIBE_VM,
    ACTION_VMWARE_MANAGER_VM_DETAIL_VM,
    ACTION_VMWARE_MANAGER_VM_MONITOR_VM,
    ACTION_VMWARE_MANAGER_VM_OPERATE_VM,
    ACTION_VMWARE_MANAGER_VM_UPDATE_VM,
    ACTION_VMWARE_MANAGER_VM_DETAIL_VM_TICKET
)
from handlers.controllers.common import (
    process_query_list_param,
    validate_user_request,
    build_params
)
from handlers.impl.vm_impl import (
    handle_describe_vm_local,
    handle_detail_vm_local,
    handle_monitor_vm_local,
    handle_operate_vm_local,
    handle_update_vm_local,
    handle_detail_vm_ticket_local
)


def describe_vm(**kwargs):
    """Describe Vm获取虚拟机列表"""
    if "Channel" in connexion.request.headers:
        kwargs["channel"] = connexion.request.headers["Channel"]
    process_query_list_param(kwargs, connexion.request.args)
    logger.debug("describe_vm with req params: [%s]"
                 % format_params(kwargs))

    if 'body' in kwargs:
        del kwargs['body']
        body = connexion.request.get_json()
        if body:
            for k, v in six.iteritems(body):
                kwargs[k] = v

    action = ACTION_VMWARE_MANAGER_VM_DESCRIBE_VM
    kwargs.update({'action': action})
    valid_user, error = validate_user_request(kwargs,
                                              connexion.request)
    if not valid_user:
        return return_error(kwargs, error, dump=False)

    # build_params
    kwargs = build_params(valid_user, kwargs, connexion.request)

    return handle_describe_vm_local(kwargs)


def detail_vm(**kwargs):
    """Detail Vm详述虚拟机信息"""
    if "Channel" in connexion.request.headers:
        kwargs["channel"] = connexion.request.headers["Channel"]
    process_query_list_param(kwargs, connexion.request.args)
    logger.debug("detail_vm with req params: [%s]"
                 % format_params(kwargs))

    if 'body' in kwargs:
        del kwargs['body']
        body = connexion.request.get_json()
        if body:
            for k, v in six.iteritems(body):
                kwargs[k] = v

    action = ACTION_VMWARE_MANAGER_VM_DETAIL_VM
    kwargs.update({'action': action})
    valid_user, error = validate_user_request(kwargs,
                                              connexion.request)
    if not valid_user:
        return return_error(kwargs, error, dump=False)

    # build_params
    kwargs = build_params(valid_user, kwargs, connexion.request)

    return handle_detail_vm_local(kwargs)


def monitor_vm(**kwargs):
    """Monitor Vm监控虚拟机"""
    if "Channel" in connexion.request.headers:
        kwargs["channel"] = connexion.request.headers["Channel"]
    process_query_list_param(kwargs, connexion.request.args)
    logger.debug("monitor_vm with req params: [%s]"
                 % format_params(kwargs))

    if 'body' in kwargs:
        del kwargs['body']
        body = connexion.request.get_json()
        if body:
            for k, v in six.iteritems(body):
                kwargs[k] = v

    action = ACTION_VMWARE_MANAGER_VM_MONITOR_VM
    kwargs.update({'action': action})
    valid_user, error = validate_user_request(kwargs,
                                              connexion.request)
    if not valid_user:
        return return_error(kwargs, error, dump=False)

    # build_params
    kwargs = build_params(valid_user, kwargs, connexion.request)

    return handle_monitor_vm_local(kwargs)


def operate_vm(**kwargs):
    """Operate Vm操作虚拟机"""
    if "Channel" in connexion.request.headers:
        kwargs["channel"] = connexion.request.headers["Channel"]
    process_query_list_param(kwargs, connexion.request.args)
    logger.debug("operate_vm with req params: [%s]"
                 % format_params(kwargs))

    if 'body' in kwargs:
        del kwargs['body']
        body = connexion.request.get_json()
        if body:
            for k, v in six.iteritems(body):
                kwargs[k] = v

    action = ACTION_VMWARE_MANAGER_VM_OPERATE_VM
    kwargs.update({'action': action})
    valid_user, error = validate_user_request(kwargs,
                                              connexion.request)
    if not valid_user:
        return return_error(kwargs, error, dump=False)

    # build_params
    kwargs = build_params(valid_user, kwargs, connexion.request)

    return handle_operate_vm_local(kwargs)


def update_vm(**kwargs):
    """Update Vm更新虚拟机信息"""
    if "Channel" in connexion.request.headers:
        kwargs["channel"] = connexion.request.headers["Channel"]
    process_query_list_param(kwargs, connexion.request.args)
    logger.debug("update_vm with req params: [%s]"
                 % format_params(kwargs))

    if 'body' in kwargs:
        del kwargs['body']
        body = connexion.request.get_json()
        if body:
            for k, v in six.iteritems(body):
                kwargs[k] = v

    action = ACTION_VMWARE_MANAGER_VM_UPDATE_VM
    kwargs.update({'action': action})
    valid_user, error = validate_user_request(kwargs,
                                              connexion.request)
    if not valid_user:
        return return_error(kwargs, error, dump=False)

    # build_params
    kwargs = build_params(valid_user, kwargs, connexion.request)

    return handle_update_vm_local(kwargs)


def detail_vm_ticket(**kwargs):
    """Detail Vm Ticket详述虚拟机票据信息"""
    if "Channel" in connexion.request.headers:
        kwargs["channel"] = connexion.request.headers["Channel"]
    process_query_list_param(kwargs, connexion.request.args)
    logger.debug("detail_vm_ticket with req params: [%s]"
                 % format_params(kwargs))

    if 'body' in kwargs:
        del kwargs['body']
        body = connexion.request.get_json()
        if body:
            for k, v in six.iteritems(body):
                kwargs[k] = v

    action = ACTION_VMWARE_MANAGER_VM_DETAIL_VM_TICKET
    kwargs.update({'action': action})
    valid_user, error = validate_user_request(kwargs,
                                              connexion.request)
    if not valid_user:
        return return_error(kwargs, error, dump=False)

    # build_params
    kwargs = build_params(valid_user, kwargs, connexion.request)

    return handle_detail_vm_ticket_local(kwargs)