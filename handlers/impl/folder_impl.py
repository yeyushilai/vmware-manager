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


def handle_detail_folder_local(kwargs):
    """获取VMware vSphere目录子项信息"""
    logger.debug('handle datail folder local start, {}'.format(kwargs))

    platform_id = kwargs.get("platform_id")
    datacenter_moid = kwargs.get("datacenter_moid")
    folder_moid = kwargs.get("folder_moid")

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
        data_list = vs.detail_folder(folder_moid, datacenter_moid=datacenter_moid)
    except (Exception, SystemExit) as e:
        if not vs.is_connected():
            return return_error(kwargs,
                                Error(
                                    ErrorCode.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value,
                                    ErrorMsg.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value),
                                dump=False
                                )
        logger.exception("detail folder failed, platform id: "
                         "{platform_id}, datacenter moid: {datacenter_moid}, "
                         "folder moid: {folder_moid}, reason: {e}"
                         "".format(platform_id=platform_id,
                                   datacenter_moid=datacenter_moid,
                                   folder_moid=folder_moid,
                                   e=str(e)))
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_FOLDER_DETAIL_FOLDER_ERROR.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_FOLDER_DETAIL_FOLDER_ERROR.value),
                            dump=False)

    return return_success(kwargs, dict(data=data_list), dump=False)


def handle_detail_root_folder_local(kwargs):
    """详述VMware vSphere根目录信息"""
    logger.debug('handle detail root folder local start, {}'.format(kwargs))

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
        data_list = vs.detail_root_folder()
    except (Exception, SystemExit) as e:
        if not vs.is_connected():
            return return_error(kwargs,
                                Error(
                                    ErrorCode.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value,
                                    ErrorMsg.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value),
                                dump=False
                                )
        logger.exception("detail root folder failed, platform id: {platform_id}"
                         ", reason: {e}"
                         "".format(platform_id=platform_id, e=str(e)))
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_FOLDER_DETAIL_FOLDER_ERROR.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_FOLDER_DETAIL_FOLDER_ERROR.value),
                            dump=False)

    return return_success(kwargs, dict(data=data_list), dump=False)
