# -*- coding: utf-8 -*-

import six

from utils.misc import format_params
from api.return_tools import return_error
from log.logger import logger
# from local
import connexion as connexion
from constants import (
    ACTION_VMWARE_MANAGER_FOLDER_DETAIL_FOLDER,
    ACTION_VMWARE_MANAGER_FOLDER_DETAIL_ROOT_FOLDER
)
from handlers.controllers.common import (
    process_query_list_param,
    validate_user_request,
    build_params
)
from handlers.impl.folder_impl import (
    handle_detail_folder_local,
    handle_detail_root_folder_local
)


def detail_folder(**kwargs):
    """Detail Folder获取目录的子项信息"""
    if "Channel" in connexion.request.headers:
        kwargs["channel"] = connexion.request.headers["Channel"]
    process_query_list_param(kwargs, connexion.request.args)
    logger.debug("detail_folder with req params: [%s]"
                 % format_params(kwargs))

    if 'body' in kwargs:
        del kwargs['body']
        body = connexion.request.get_json()
        if body:
            for k, v in six.iteritems(body):
                kwargs[k] = v
    
    action = ACTION_VMWARE_MANAGER_FOLDER_DETAIL_FOLDER
    kwargs.update({'action': action})
    valid_user, error = validate_user_request(kwargs,
                                              connexion.request)
    if not valid_user:
        return return_error(kwargs, error, dump=False)

    # build_params
    kwargs = build_params(valid_user, kwargs, connexion.request)

    return handle_detail_folder_local(kwargs)


def detail_root_folder(**kwargs):
    """detail root folder详述根目录信息"""
    if "Channel" in connexion.request.headers:
        kwargs["channel"] = connexion.request.headers["Channel"]
    process_query_list_param(kwargs, connexion.request.args)
    logger.debug("detail_root_folder with req params: [%s]"
                 % format_params(kwargs))

    if 'body' in kwargs:
        del kwargs['body']
        body = connexion.request.get_json()
        if body:
            for k, v in six.iteritems(body):
                kwargs[k] = v

    action = ACTION_VMWARE_MANAGER_FOLDER_DETAIL_ROOT_FOLDER
    kwargs.update({'action': action})
    valid_user, error = validate_user_request(kwargs,
                                              connexion.request)
    if not valid_user:
        return return_error(kwargs, error, dump=False)

    # build_params
    kwargs = build_params(valid_user, kwargs, connexion.request)

    return handle_detail_root_folder_local(kwargs)