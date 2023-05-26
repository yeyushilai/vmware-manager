# -*- coding: utf-8 -*-

import re
import random
from datetime import datetime, timedelta

from log.logger import logger
from uutils.common import (
    format_value_by_timeslice,
    order_list_and_paginate
)

from uutils.pg import VMwareManagerPGInterface
from resource_control.vmware_vsphere import VMwareVSphere
from error import (
    Error,
    ErrorCode,
    ErrorMsg
)
from return_tools import (
    return_error,
    return_success
)
from constants import (
    METRIC_CN_MAPPING,
    METRIC_COUNTER_MAPPING,
    METRIC_UNIT_MAPPING,

    PlatformVMwareToolsStatus,
    PlatformVmOperationType,
    PlatformVmStatus
)

import context
ctx = context.instance()


def handle_describe_vm_local(kwargs):
    logger.debug('handle describe vm local start, {}'.format(kwargs))
    platform_id = kwargs.get("platform_id")
    offset = kwargs.get("offset") or 0
    limit = kwargs.get("limit") or 10
    search_word = kwargs.get("search_word")
    sort_key = kwargs.get("sort_key") or "name"
    reverse = bool(kwargs.get("reverse"))

    # if search_word and is_contains_chinese(search_word):
    #     search_word = search_word.encode("utf-8")

    pi = VMwareManagerPGInterface()
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
        raw_vm_list = vs.list_vm()
    except (Exception, SystemExit) as e:
        if not vs.is_connected():
            logger.exception("connect to VMware vSphere platform failed, "
                             "platform host: {host}, platform username: {username}"
                             "".format(host=account["host"],
                                       username=account["username"]))
            return return_error(kwargs,
                                Error(
                                    ErrorCode.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value,
                                    ErrorMsg.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value),
                                dump=False)
        logger.error("list vm failed, platform id: {platform_id}, reason: {e}"
                     "".format(platform_id=platform_id, e=str(e)))
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_VM_LIST_VM_ERROR.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_VM_LIST_VM_ERROR.value),
                            dump=False)

    # 搜索
    vm_list = list()
    for vm_info in raw_vm_list:
        if search_word:
            match_len = re.findall(r'%s.*' % search_word, vm_info["name"])
            if len(match_len) == 0:
                continue
        vm_list.append(vm_info)

    # 排序、分页
    try:
        result_list, count = order_list_and_paginate(vm_list, sort_key, offset,
                                                     limit, reverse)
        result_list = result_list or []
        count = count or 0
    except Exception as e:
        logger.exception(
            "describe vm order and paginate error, reason: %s" % e)
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_VM_ORDER_PAGINATE_VMS_ERROR.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_VM_ORDER_PAGINATE_VMS_ERROR.value),
                            dump=False)

    data = dict(datas=result_list, count=count)
    return return_success(kwargs, data, dump=False)


def handle_detail_vm_local(kwargs):
    logger.debug('handle detail vm local start, {}'.format(kwargs))

    platform_id = kwargs.get("platform_id")
    vm_id = kwargs.get("vm_id")
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
        vm_data = vs.get_vm(vm_uuid=vm_id)
    except (Exception, SystemExit) as e:
        if not vs.is_connected():
            logger.exception(
                "connect to VMware vSphere platform failed, platform "
                "host: {host}, platform username: {username}"
                "".format(host=account["host"],
                          username=account["username"]))
            return return_error(kwargs,
                                Error(
                                    ErrorCode.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value,
                                    ErrorMsg.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value),
                                dump=False
                                )
        logger.exception("get vm info failed, platform id: {platform_id}, "
                         "vm id: {vm_id}, reason: {e}"
                         "".format(platform_id=platform_id, vm_id=vm_id,
                                   e=str(e)))
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_VM_GET_VM_ERROR.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_VM_GET_VM_ERROR.value),
                            dump=False
                            )

    if not vm_data:
        logger.error(
            "vm do not exists, platform id: {platform_id}, vm id: {vm_id}"
            "".format(platform_id=platform_id, vm_id=vm_id))
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_VM_VM_NOT_EXISTS.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_VM_VM_NOT_EXISTS.value),
                            dump=False)

    data = dict(data=vm_data)
    return return_success(kwargs, data, dump=False)


def handle_monitor_vm_local(kwargs):
    logger.info('handle monitor vm local start, {}'.format(kwargs))

    platform_id = kwargs.get("platform_id")
    vm_uuid = kwargs.get("vm_uuid")

    user_id = kwargs.get("user_id")
    metrics = kwargs.get("metrics")
    interval = kwargs.get("interval")

    pi = VMwareManagerPGInterface()
    platform = pi.query_platform(platform_id=platform_id)
    if not platform:
        logger.error(
            "monitor api platform do not exists, platform id: {platform_id}"
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
    logger.info("monitor api get account: [%s]" % account)
    vs = VMwareVSphere(account)

    # 获取虚拟机对象
    try:
        vm_obj = vs.vi.get_vm_by_uuid(vm_uuid=vm_uuid)
    except (Exception, SystemExit) as e:
        if not vs.is_connected():
            logger.exception(
                "connect to VMware vSphere platform failed, platform "
                "host: {host}, platform username: {username}"
                "".format(host=account["host"],
                          username=account["username"]))
            return return_error(kwargs,
                                Error(
                                    ErrorCode.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value,
                                    ErrorMsg.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value),
                                dump=False)
        logger.exception("get vm failed, platform id: {platform_id}, "
                         "vm id: {vm_id}, reason: {e}"
                         "".format(platform_id=platform_id, vm_id=vm_uuid,
                                   e=str(e)))
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_VM_GET_VM_ERROR.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_VM_GET_VM_ERROR.value),
                            dump=False)
    logger.info("monitor api get vm obj success [%s]" % vm_obj.name)

    # 获取couter - metric 映射关系
    counter_id_dict = vs.vi.get_counter_dict()
    counterid_metric_dict = {
        counter_id_dict.get(METRIC_COUNTER_MAPPING.get(metric)): metric for
        metric in metrics}
    logger.info(
        "monitor api get counterid_metric_dict [%s]" % counterid_metric_dict)

    # 获取对应metric监控数据
    nowtime = datetime.now()
    start_time = nowtime - timedelta(minutes=80)
    end_time = nowtime - timedelta(minutes=1)
    result = vs.vi.BuildQuery(
        start_time=start_time,
        end_time=end_time,
        counterIds=list(counterid_metric_dict.keys()),
        instance="",
        entity=vm_obj,
    )
    result_data = {"data": [], "ret_code": 0, "total_count": 0}
    if result:
        value = result[0].value
        value_start_time = result[0].sampleInfo[0].timestamp + timedelta(hours=8)
        logger.info("monitor api get value success")

        for metric_data in value:
            counterid = metric_data.id.counterId
            metric = counterid_metric_dict.get(counterid)
            monitor_data = format_value_by_timeslice(metric_data.value,
                                                     value_start_time,
                                                     metric, interval)
            item = {
                "monitor_data": monitor_data,
                "resource_id": vm_uuid,
                "metric_name": metric,
                "metric_cn_name": METRIC_CN_MAPPING.get(metric, metric),
                "metric_unit": METRIC_UNIT_MAPPING.get(metric, ""),
                "create_time": "",
                "description": METRIC_CN_MAPPING.get(metric, metric),
                "step": 20,
                "tags": "",
                "user_id": user_id
            }
            result_data["data"].append(item)
        result_data["total_count"] = len(result_data["data"])
        # logger.info("monitor api result success, result_data [%s]" % result_data)
    return return_success(kwargs, result_data, dump=False)


def handle_operate_vm_local(kwargs):
    logger.debug('handle operate vm local start, {}'.format(kwargs))

    platform_id = kwargs.get("platform_id")
    vm_id = kwargs.get("vm_id")
    operation = kwargs.get("operation")
    pi = VMwareManagerPGInterface()

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

    # 若动作为重启操作系统和关闭操作系统，虚拟机必须安装且运行了VMware Tools
    if operation in [
        PlatformVmOperationType.REBOOT.value,
        PlatformVmOperationType.SHUTDOWN.value
    ]:
        try:
            vm_info = vs.get_vm(vm_uuid=vm_id)
        except (Exception, SystemExit) as e:
            if not vs.is_connected():
                logger.exception(
                    "connect to VMware vSphere platform failed, platform "
                    "host: {host}, platform username: {username}"
                    "".format(host=account["host"],
                              username=account["username"]))
                return return_error(kwargs,
                                    Error(
                                        ErrorCode.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value,
                                        ErrorMsg.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value),
                                    dump=False)
            logger.exception("get vm info failed, platform id: {platform_id}, "
                             "vm id: {vm_id}, reason: {e}"
                             "".format(platform_id=platform_id, vm_id=vm_id,
                                       e=str(e)))
            return return_error(kwargs,
                                Error(
                                    ErrorCode.ERROR_VMWARE_VSPHERE_VM_GET_VM_ERROR.value,
                                    ErrorMsg.ERROR_VMWARE_VSPHERE_VM_GET_VM_ERROR.value),
                                dump=False)

        assert "vmware_tools_status" in vm_info
        if vm_info["vmware_tools_status"] != PlatformVMwareToolsStatus.TOOLSOK.value:
            logger.error(
                "the status of vmware tools for vm is not ok, vm can not been "
                "operatored, platform id: {platform_id}, vm id: {vm_id}, "
                "operation: {operation}, vmware tools status: {vmware_tools_status}"
                "".format(platform_id=platform_id, vm_id=vm_id,
                          operation=operation,
                          vmware_tools_status=vm_info["vmware_tools_status"]))
            return return_error(kwargs,
                                Error(
                                    ErrorCode.ERROR_VMWARE_VSPHERE_VM_VMWARE_TOOLS_NOT_OK.value,
                                    ErrorMsg.ERROR_VMWARE_VSPHERE_VM_VMWARE_TOOLS_NOT_OK.value),
                                dump=False)

    try:
        vs.operate_vm(vm_id, operation)
    except (Exception, SystemExit) as e:
        logger.exception("operate vm failed, platform id: {platform_id}, "
                         "vm id: {vm_id}, operation: {operation}, "
                         "reason: {reason}"
                         "".format(platform_id=platform_id, vm_id=vm_id,
                                   operation=operation, reason=str(e)))
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_VM_OPERATE_VM_ERROR.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_VM_OPERATE_VM_ERROR.value),
                            dump=False)
    data = dict(platform_id=platform_id, vm_id=vm_id)
    return return_success(kwargs, dict(data=data), dump=False)


def handle_update_vm_local(kwargs):
    logger.debug('handle update vm local start, {}'.format(kwargs))
    platform_id = kwargs.get("platform_id")
    vm_id = kwargs.get("vm_id")
    vm_name = kwargs.get("vm_name")
    vm_note = kwargs.get("vm_note")

    vm_info = dict()
    if vm_name:
        vm_info["vm_name"] = vm_name
    if vm_note:
        vm_info["vm_note"] = vm_note

    pi = VMwareManagerPGInterface()
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
        vs.update_vm(vm_uuid=vm_id, vm_info=vm_info)
    except (Exception, SystemExit) as e:
        if not vs.is_connected():
            logger.exception(
                "connect to VMware vSphere platform failed, platform host: "
                "{host}, platform username: {username}"
                "".format(host=account["host"],
                          username=account["username"]))
            return return_error(kwargs,
                                Error(
                                    ErrorCode.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value,
                                    ErrorMsg.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value),
                                dump=False)
        logger.exception("update vm config failed, platform id: {platform_id}"
                         ", vm id: {vm_id}, vm info: {vm_info}, reason: "
                         "{reason}"
                         "".format(platform_id=platform_id, vm_id=vm_id,
                                   vm_info=vm_info, reason=str(e)))
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_VM_UPDATE_VM_ERROR.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_VM_UPDATE_VM_ERROR.value),
                            dump=False)

    data = dict(platform_id=platform_id, vm_id=vm_id)
    return return_success(kwargs, dict(data=data), dump=False)


def handle_detail_vm_ticket_local(kwargs):
    logger.debug('handle detail vm ticket local start, {}'.format(kwargs))

    platform_id = kwargs.get("platform_id")
    vm_id = kwargs.get("vm_id")
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
        vm_ticket = vs.get_vm_ticket(vm_id)
    except (Exception, SystemExit) as e:
        # 检查连通性
        if not vs.is_connected():
            logger.exception("connect to VMware vSphere platform failed, "
                             "platform host: {host}, platform username: {username}"
                             "".format(host=account["host"],
                                       username=account["username"]))
            return return_error(kwargs,
                                Error(
                                    ErrorCode.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value,
                                    ErrorMsg.ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT.value),
                                dump=False)
        # 检查虚拟机状态
        # 只有在开机状态下才能拿到ticket
        vm_power_status = vs.get_vm_power_status(vm_id)
        if vm_power_status != PlatformVmStatus.POWEREDON.value:
            logger.exception("the power status of vm in Vmware vSphere is not "
                             "poweredOn, platform id: {platform_id}, vm id: "
                             "{vm_id}, vm power status: {vm_power_status}"
                             "".format(platform_id=platform_id,
                                       vm_id=vm_id,
                                       vm_power_status=vm_power_status))
            return return_error(kwargs,
                                Error(
                                    ErrorCode.ERROR_VMWARE_VSPHERE_VM_INVALID_VM_POWERSTATUS.value,
                                    ErrorMsg.ERROR_VMWARE_VSPHERE_VM_INVALID_VM_POWERSTATUS.value),
                                dump=False)

        logger.exception("get vm ticket failed, platform id: {platform_id}, "
                         "vm id: {vm_id}, reason: {e}"
                         "".format(platform_id=platform_id, vm_id=vm_id,
                                   e=str(e)))
        return return_error(kwargs,
                            Error(
                                ErrorCode.ERROR_VMWARE_VSPHERE_VM_GET_VM_TICKET_ERROR.value,
                                ErrorMsg.ERROR_VMWARE_VSPHERE_VM_GET_VM_TICKET_ERROR.value),
                            dump=False)

    # 获取代理主机和端口
    data = {
        "broker_host": random.choice(ctx.domain_name.values()),
        "broker_port": ctx.broker_port,
        "host": vm_ticket["host"],
        "port": vm_ticket["port"],
        "ticket": vm_ticket["ticket"]
    }

    return return_success(kwargs, dict(data=data), dump=False)
