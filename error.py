# -*- coding: utf-8 -*-

from enum import Enum
from api.constants import (
    EN,
    ZH_CN,
    DEFAULT_LANG,
    SUPPORTED_LANGS
)


class Error(object):
    """ error class """

    def __init__(self, code, message, *args, **kwargs):
        """
        @param code - the error code, it is an integer.
        @param message - the error message to describe the error information in detail.
                         it is a dict with multi-language defined
        """
        self._code = code
        self._message = message
        self._args = args
        self._kwargs = kwargs

    def format_args(self):
        if isinstance(self._args, (int, long, float, bool)):
            return self._args

        # case 2, non unicode characters
        try:
            return str(self._args).decode('utf-8')
        except Exception:
            pass

        # case 3, it comes from the API parameter passed by the user
        return "%s" % self._args

    @property
    def code(self):
        """ return a valid error code that defined in error codes"""
        return self._code

    def get_message(self, lang=DEFAULT_LANG):
        lang = DEFAULT_LANG if lang not in SUPPORTED_LANGS else lang
        raw_message = self._message.get(lang)

        assert not all([self._args, self._kwargs])

        msg = raw_message
        if self._args:
            try:
                msg = raw_message % format(self.format_args())
            except:
                pass

        if self._kwargs:
            try:
                msg = raw_message.format(**self._kwargs)
            except:
                pass

        return msg


class ErrorCode(Enum):
    # 成功
    SUCCESS = 0

    # 通用错误
    ERROR_COMMON = 1

    # VMware vSphere平台相关错误
    ERROR_VMWARE_VSPHERE_PLATFORM_COMMON = 2000
    ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT = 2001
    ERROR_VMWARE_VSPHERE_PLATFORM_EXISTS = 2002
    ERROR_VMWARE_VSPHERE_PLATFORM_NOT_EXISTS = 2003

    # VMware vSphere数据中心相关错误
    ERROR_VMWARE_VSPHERE_DATACENTER_COMMON = 3000
    ERROR_VMWARE_VSPHERE_DATACENTER_LIST_DATACENTER_ERROR = 3001
    ERROR_VMWARE_VSPHERE_DATACENTER_DETAIL_DATACENTER_ERROR = 3002

    # VMware vSphere目录相关错误
    ERROR_VMWARE_VSPHERE_FOLDER_COMMON = 4000
    ERROR_VMWARE_VSPHERE_FOLDER_DETAIL_FOLDER_ERROR = 4001

    # VMware vSphere虚拟机相关错误
    ERROR_VMWARE_VSPHERE_VM_COMMON = 6000
    ERROR_VMWARE_VSPHERE_VM_ORDER_PAGINATE_VMS_ERROR = 6001
    ERROR_VMWARE_VSPHERE_VM_OPERATE_VM_ERROR = 6002
    ERROR_VMWARE_VSPHERE_VM_UPDATE_VM_ERROR = 6003
    ERROR_VMWARE_VSPHERE_VM_LIST_VM_ERROR = 6004
    ERROR_VMWARE_VSPHERE_VM_GET_VM_ERROR = 6005
    ERROR_VMWARE_VSPHERE_VM_VM_NOT_EXISTS = 6006
    ERROR_VMWARE_VSPHERE_VM_VMWARE_TOOLS_NOT_OK = 6007
    ERROR_VMWARE_VSPHERE_VM_MOINTOR_TIME_RANGE_ERROR = 6008
    ERROR_VMWARE_VSPHERE_VM_GET_VM_TICKET_ERROR = 6009
    ERROR_VMWARE_VSPHERE_VM_INVALID_VM_POWERSTATUS= 6010


class ErrorMsg(Enum):
    # 成功
    SUCCESS = {
        EN: u"",
        ZH_CN: u""
    }

    # 通用错误
    ERROR_COMMON = {
        EN: u"common error",
        ZH_CN: u"通用错误"
    }

    # VMware vSphere平台相关错误
    ERROR_VMWARE_VSPHERE_PLATFORM_COMMON = {
        EN: u"platform common error",
        ZH_CN: u"平台通用错误"
    }
    ERROR_VMWARE_VSPHERE_PLATFORM_CAN_NOT_CONNECT = {
        EN: u"platform can not connect",
        ZH_CN: u"平台无法联通，请检查后重试"
    }
    ERROR_VMWARE_VSPHERE_PLATFORM_EXISTS = {
        EN: u"platform has already been managed",
        ZH_CN: u"平台之前已经被添加，无需重复添加"
    }
    ERROR_VMWARE_VSPHERE_PLATFORM_NOT_EXISTS = {
        EN: u"platform do not exists",
        ZH_CN: u"平台不存在，请检查后重试"
    }

    # VMware vSphere数据中心相关错误
    ERROR_VMWARE_VSPHERE_DATACENTER_COMMON = {
        EN: u"datacenter common error",
        ZH_CN: u"数据中心通用错误，请检查后重试"
    }
    ERROR_VMWARE_VSPHERE_DATACENTER_LIST_DATACENTER_ERROR = {
        EN: u"list datacenter error",
        ZH_CN: u"获取数据中心列表失败，请检查后重试"
    }
    ERROR_VMWARE_VSPHERE_DATACENTER_DETAIL_DATACENTER_ERROR = {
        EN: u"detail datacenter error",
        ZH_CN: u"详述数据中心信息失败，请检查后重试"
    }


    # VMware vSphere目录相关错误
    ERROR_VMWARE_VSPHERE_FOLDER_COMMON = {
        EN: u"folder common error",
        ZH_CN: u"目录通用错误，请检查后重试"
    }
    ERROR_VMWARE_VSPHERE_FOLDER_DETAIL_FOLDER_ERROR = {
        EN: u"detail folder error",
        ZH_CN: u"详述目录失败，请检查后重试"
    }

    # VMware vSphere虚拟机相关错误
    ERROR_VMWARE_VSPHERE_VM_COMMON = {
        EN: u"vm common error",
        ZH_CN: u"虚拟机通用错误，请检查后重试"
    }
    ERROR_VMWARE_VSPHERE_VM_ORDER_PAGINATE_VMS_ERROR = {
        EN: u"order and paginate vms error",
        ZH_CN: u"虚拟机排序分页错误，请检查后重试"
    }
    ERROR_VMWARE_VSPHERE_VM_OPERATE_VM_ERROR = {
        EN: u"operate vm error",
        ZH_CN: u"虚拟机操作错误，请检查后重试"
    }
    ERROR_VMWARE_VSPHERE_VM_UPDATE_VM_ERROR = {
        EN: u"update vm config error",
        ZH_CN: u"虚拟机更新配置错误，请检查后重试"
    }
    ERROR_VMWARE_VSPHERE_VM_VM_NOT_EXISTS = {
        EN: u"vm do not exists",
        ZH_CN: u"虚拟机不存在，请检查后重试"
    }
    ERROR_VMWARE_VSPHERE_VM_VMWARE_TOOLS_NOT_OK = {
        EN: u"vmware tools not ok",
        ZH_CN: u"虚拟机的VMware Tools工具非OK状态，请检查后重试"
    }
    ERROR_VMWARE_VSPHERE_VM_LIST_VM_ERROR = {
        EN: u"list vm error",
        ZH_CN: u"获取虚拟机列表失败，请检查后重试"
    }
    ERROR_VMWARE_VSPHERE_VM_GET_VM_ERROR = {
        EN: u"get vm error",
        ZH_CN: u"获取虚拟机信息失败，请检查后重试"
    }
    ERROR_VMWARE_VSPHERE_VM_MOINTOR_TIME_RANGE_ERROR = {
        EN: u"mointor time range error",
        ZH_CN: u"监控时间片段错误，请检查后重试"
    }
    ERROR_VMWARE_VSPHERE_VM_GET_VM_TICKET_ERROR = {
        EN: u"get vm ticket error",
        ZH_CN: u"获取虚拟机票据失败，请检查后重试"
    }
    ERROR_VMWARE_VSPHERE_VM_INVALID_VM_POWERSTATUS = {
        EN: u"invalid vm powerstatus",
        ZH_CN: u"虚拟机运行状态非法，请检查后重试"
    }
