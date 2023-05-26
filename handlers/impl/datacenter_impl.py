# -*- coding: utf-8 -*-

from log.logger import logger

from resource_control.vmware_vsphere import VMwareVSphere
from uutils.pg import VMwareManagerPGInterface
from error import (
    Error,
    ErrorMsg,
    ErrorCode
)
from return_tools import (
    return_error,
    return_success,
)


def handle_describe_datacenter_local(kwargs):
    """列举VMware vSphere数据中心列表"""
    logger.debug('handle describe datacenter local start, {}'.format(kwargs))

    platform_id = kwargs.get("platform_id")
    pi = VMwareManagerPGInterface()

    # 平台存在性检查
    platform = pi.query_platform(platform_id=platform_id)
    if not platform:
        logger.error("platform do not exists, platform id: {platform_id}"
                     "".format(platform_id=platform_id))
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_PLATFORM_NOT_EXISTS.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_PLATFORM_NOT_EXISTS.value),
                            dump=False)
    account = dict(
        host=platform["platform_host"],
        port=platform["platform_port"],
        username=platform["platform_user"],
        encrypt_password=platform["platform_password"]
    )

    vs = VMwareVSphere(account)
    try:
        datacenter_list = vs.list_datacenter()
    except (Exception, SystemExit) as e:
        if not vs.is_connected():
            return return_error(kwargs,
                                Error(
                                    ErrorCode.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value,
                                    ErrorMsg.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value),
                                dump=False
                                )
        logger.exception("list datacenter failed, platform id: {platform_id}, "
                         "reason: {e}"
                         "".format(platform_id=platform_id, e=str(e)))
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_DATACENTER_LIST_DATACENTER_ERROR.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_DATACENTER_LIST_DATACENTER_ERROR.value),
                            dump=False)

    return return_success(kwargs, dict(data=datacenter_list), dump=False)


def handle_detail_datacenter_local(kwargs):
    """详述VMware vSphere数据中心信息"""
    logger.debug('handle detail datacenter local start, {}'.format(kwargs))

    platform_id = kwargs.get("platform_id")
    datacenter_id = kwargs.get("datacenter_id")
    pi = VMwareManagerPGInterface()

    # 平台存在性检查
    platform = pi.query_platform(platform_id=platform_id)
    if not platform:
        logger.error("platform do not exists, platform id: {platform_id}"
                     "".format(platform_id=platform_id))
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_PLATFORM_NOT_EXISTS.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_PLATFORM_NOT_EXISTS.value),
                            dump=False)
    account = dict(
        host=platform["platform_host"],
        port=platform["platform_port"],
        username=platform["platform_user"],
        encrypt_password=platform["platform_password"]
    )

    vs = VMwareVSphere(account)
    try:
        datacenter_info = vs.detail_datacenter(datacenter_id)
    except (Exception, SystemExit) as e:
        if not vs.is_connected():
            return return_error(kwargs,
                                Error(
                                    ErrorCode.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value,
                                    ErrorMsg.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value),
                                dump=False
                                )
        logger.exception("detail datacenter failed, platform id: {platform_id}, "
                         "reason: {e}"
                         "".format(platform_id=platform_id, e=str(e)))
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_DATACENTER_DETAIL_DATACENTER_ERROR.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_DATACENTER_DETAIL_DATACENTER_ERROR.value),
                            dump=False)

    return return_success(kwargs, dict(data=datacenter_info), dump=False)