# -*- coding: utf-8 -*-

from enum import Enum

# controllers
CONTROLLER_SELF = "self"
CONTROLLER_PITRIX = "pitrix"
SUPPORTED_CONTROLLERS = [CONTROLLER_SELF, CONTROLLER_PITRIX]
API_SECURE_PORTS = 8882

PITRIX_CONF_HOME = "/pitrix/conf"
# ---------------------------------------------
#       The constants for access key status
# ---------------------------------------------
ACCESS_KEY_STATUS_ACTIVE = "active"
ACCESS_KEY_STATUS_INACTIVE = "inactive"
ACCESS_KEY_STATUS_DISABLED = "disabled"
ACCESS_KEY_NAME_FOR_MGMT = "pitrix access key for mgmt"


# ---------------------------------------------
#       The constants for api timeout
# ---------------------------------------------
# time interval when client's request expired in seconds
REQ_EXPIRED_INTERVAL = 60

# time out when sending request to front_gate
TIMEOUT_FRONT_GATE = 30
TIMEOUT_FRONT_GATE_FAST = 1
TIMEOUT_FRONT_GATE_FAST_RATE = 80

# time out when sending request to billing server
TIMEOUT_BILLING_SERVER = 60

# time out when sending request to notifier server
TIMEOUT_NOTIFIER_SERVER = 5

# time out when sending request to account server
TIMEOUT_ACCOUNT_SERVER = 5
TIMEOUT_ACCOUNT_SERVER_LONG = 10
TIMEOUT_IAM_SIGNATURE_SERVER_LONG = 10

# long handle time
LONG_HANDLE_TIME = 20


# ---------------------------------------------
#       The constants for users
# ---------------------------------------------
# management user id
MGMT_USER_ID = "yunify"  # management user with the highest privilege
# system user id
SYSTEM_USER_ID = "system"  # providing public resources like image template and vxnet-0
# system console id
SYSTEM_CONSOLE_ID = "system"  # system console id

# user privilege
NO_PRIVILEGE = 0  # access denied for all pitrix service
NORMAL_PRIVILEGE = 1  # normal user
MGMT_PRIVILEGE = 5  # mgmt user, can migrate instance, but not allowed to modify other users' resources
MGMT_PRIVILEGE_7 = 7  # mgmt user and can describe billing data
MGMT_PRIVILEGE_8 = 8  # mgmt user and can get access secrect key
SUPER_PRIVILEGE = 10  # highest privilege, can do any thing, only "yunify" user has this privilege.

# all normal partner privilege is 10
APP_REVIEW_PRIVILEGE = 2  # for high level partner, can review apps

# roles
ROLE_NORMAL_USER = "user"  # normal user
ROLE_PARTNER = "partner"  # partner
ROLE_AGENT = "agent"  # agent
ROLE_ZONE_ADMIN = "zone_admin"  # zone admin, can manager resources in zone
ROLE_CONSOLE_ADMIN = "console_admin"  # console admin, can manage all resources belong to this console
ROLE_GLOBAL_ADMIN = "global_admin"  # global admin, can manager all resources
ROLE_TICKET_MGR = "ticket_mgr"  # ticket manager, reply user tickets.


# ---------------------------------------------
#       Constants for Memcached key prefix
# ---------------------------------------------
MC_KEY_PREFIX_ROOT = "Pitrix.VmwareManager"

# zone cached in ws server
MC_KEY_PREFIX_ZONE = "%s.Zone" % MC_KEY_PREFIX_ROOT
MC_KEY_PREFIX_ZONES = "%s.Zone" % MC_KEY_PREFIX_ROOT

# account
MC_KEY_PREFIX_ACCOUNT = "%s.ZoneAccount" % MC_KEY_PREFIX_ZONE
MC_KEY_PREFIX_ACCOUNT_USER_SET = "%s.UserSet" % MC_KEY_PREFIX_ROOT

# account cached in ws server.
MC_KEY_PREFIX_ACCOUNT_USER_INFO = "%s.UserInfo" % MC_KEY_PREFIX_ACCOUNT
MC_KEY_PREFIX_ACCOUNT_SUB_USER_INFO = "%s.SubUserInfo" % MC_KEY_PREFIX_ACCOUNT
MC_KEY_PREFIX_ACCOUNT_ACCESS_KEY = "%s.AccessKey" % MC_KEY_PREFIX_ACCOUNT
MC_KEY_PREFIX_ACCOUNT_USER_LOCK = "%s.UserLock" % MC_KEY_PREFIX_ACCOUNT
MC_KEY_PREFIX_ACCOUNT_QUOTA = "%s.Quota" % MC_KEY_PREFIX_ACCOUNT
MC_KEY_PREFIX_CERTIFICATES = "%s.Certificates" % MC_KEY_PREFIX_ROOT
MC_KEY_PREFIX_ACCOUNT_USER_ZONE = "%s.UserZone" % MC_KEY_PREFIX_ACCOUNT
MC_DEFAULT_CACHE_TIME = 3600*24

# ---------------------------------------------
#       languages
# ---------------------------------------------
EN = "en"
ZH_CN = "zh-cn"
DEFAULT_LANG = EN
SUPPORTED_LANGS = [EN, ZH_CN]


# ---------------------------------------------
#       zone status
# ---------------------------------------------
ZONE_STATUS_ACTIVE = "active"
ZONE_STATUS_FAULTY = "faulty"
ZONE_STATUS_DEFUNCT = "defunct"


# ---------------------------------------------
#       user status
# ---------------------------------------------
USER_STATUS_ACTIVE = "active"
USER_STATUS_DISABLED = "disabled"
USER_STATUS_DELETED = "deleted"
USER_STATUS_PENDING = "pending"


# ---------------------------------------------
#       Action
# ---------------------------------------------
# Account
ACTION_DESCRIBE_USERS = "DescribeUsers"
ACTION_DESCRIBE_SUB_USERS = "DescribeSubUsers"
ACTION_DESCRIBE_USER_LOCKS = "DescribeUserLocks"
ACTION_DESCRIBE_ACCOUNT_QUOTAS = "DescribeAccountQuotas"
ACTION_DESCRIBE_ACCESS_KEYS = "DescribeAccessKeys"
ACTION_DESCRIBE_DEFAULT_ZONES = "DescribeDefaultZones"
ACTION_DESCRIBE_ZONES = "DescribeZones"
ACTION_DESCRIBE_LOGIN_SERVERS = "DescribeLoginServers"
ACTION_DESCRIBE_LOGIN_ACCOUNT_USERS = "DescribeLoginAccountUsers"
ACTION_DESCRIBE_LOGIN_ACCOUNTS = "DescribeLoginAccounts"

ACTION_GET_PRIVATE_KEY = "GetPrivateKey"
ACTION_GET_SECRET_ACCESS_KEY = "GetSecretAccessKey"
ACTION_GET_VPN_CERTS = "GetVPNCerts"

# ---------------------------------------------
#       The constants for action related
# ---------------------------------------------
# actions allowed where user is locked other than Describe* and Get*
LOCK_ALLOWED_ACTIONS = []

# Describe* and Get* actions that disallowed when user is locked
LOCK_DISALLOWED_ACTIONS = [
    ACTION_GET_PRIVATE_KEY,
    ACTION_GET_SECRET_ACCESS_KEY,
    ACTION_GET_VPN_CERTS
]


# ---------------------------------------------
#       The constants for api action
# ---------------------------------------------
# 健康管理
ACTION_VMWARE_MANAGER_HEALTH_CHECK_HEALTH = "VmwareManagerHealthCheckHealth"

# 平台管理
ACTION_VMWARE_MANAGER_PLATFORM_ADD_PLATFORM = "VmwareManagerPlatformAddPlatform"
ACTION_VMWARE_MANAGER_PLATFORM_CHECK_PLATFORM_CONNECTIVITY = "VmwareManagerPlatformCheckPlatformConnectivity"
ACTION_VMWARE_MANAGER_PLATFORM_DELETE_PLATFORM = "VmwareManagerPlatformDeletePlatform"
ACTION_VMWARE_MANAGER_PLATFORM_DESCRIBE_PLATFORM = "VmwareManagerPlatformDescribePlatform"
ACTION_VMWARE_MANAGER_PLATFORM_UPDATE_PLATFORM = "VmwareManagerPlatformUpdatePlatform"

# 数据中心管理
ACTION_VMWARE_MANAGER_DATACENTER_DESCRIBE_DATACENTER = "VmwareManagerDatacenterDescribeDatacenter"
ACTION_VMWARE_MANAGER_DATACENTER_DETAIL_DATACENTER = "VmwareManagerDatacenterDetailDatacenter"

# 目录管理
ACTION_VMWARE_MANAGER_FOLDER_DETAIL_FOLDER = "VmwareManagerFolderDetailFolder"
ACTION_VMWARE_MANAGER_FOLDER_DETAIL_ROOT_FOLDER = "VmwareManagerFolderDescribeRootFolder"

# 虚拟机管理
ACTION_VMWARE_MANAGER_VM_DESCRIBE_VM = "VmwareManagerVmDescribeVm"
ACTION_VMWARE_MANAGER_VM_DETAIL_VM = "VmwareManagerVmDetailVm"
ACTION_VMWARE_MANAGER_VM_MONITOR_VM = "VmwareManagerVmMonitorVm"
ACTION_VMWARE_MANAGER_VM_OPERATE_VM = "VmwareManagerVmOperateVm"
ACTION_VMWARE_MANAGER_VM_UPDATE_VM = "VmwareManagerVmUpdateVm"
ACTION_VMWARE_MANAGER_VM_DETAIL_VM_TICKET = "VmwareManagerVmDetailVmTicket"


# ---------------------------------------------
#       The constants for api types
# ---------------------------------------------
API_TYPE_VMWARE_MANAGER = "vmware_manager_api"
SUPPORTED_API_TYPES = [
    API_TYPE_VMWARE_MANAGER,
]
API_DURATION = {
    API_TYPE_VMWARE_MANAGER: 'vmware_manager_api_duration',
}

# limitation on api access count during a period of time
MC_KEY_PREFIX_VMWARE_MANAGER_API_ACCESS_COUNT = "%s.VmwareManagerApiAccessCnt" % MC_KEY_PREFIX_ROOT

MC_KEY_MAP = {
    API_TYPE_VMWARE_MANAGER: MC_KEY_PREFIX_VMWARE_MANAGER_API_ACCESS_COUNT,
}

SERVER_TYPE_FRONT_GATE = "vmware_manager_fg"
FRONT_GATE_PORT = 9666
FRONT_GATE_PROXY_PORT = 9665
FRONT_GATE_HAPROXY_PORT = 8665

SERVER_TYPE_IAM_SIGNATURE = "signature_server"
IAM_SIGNATURE_SERVER_PROXY_PORT = 9389

ZONE_SERVER_CACHE_TIME = 600


# ---------------------------------------------
#       The constants for vmware manager business
# ---------------------------------------------
class PlatformStatus(Enum):
    """VMware vSphere平台的状态"""
    CONNECTED = "connected"
    UNCONNECTED = "unconnected"


class PlatformVmStatus(Enum):
    """VMware vSphere虚拟机的状态"""
    POWEREDON = "poweredOn"
    POWEREDOFF = "poweredOff"
    SUSPENDED = "suspended"


class PlatformVmOperationType(Enum):
    """VMware vSphere虚拟机的操作类型"""
    POWEROFF = "poweroff"       # 打开电源
    POWERON = "poweron"         # 关闭电源
    SUSPEND = "suspend"         # 挂起
    REBOOT = "reboot"           # 重启操作系统
    SHUTDOWN = "shutdown"       # 关闭操作系统


class PlatformVMwareToolsStatus(Enum):
    """VMware Tools的状态"""
    TOOLSNOTINSTALLED = "toolsNotInstalled"
    TOOLSNOTRUNNING = "toolsNotRunning"
    TOOLSOK = "toolsOk"


# VMware vSphere平台虚拟机状态和枚举值的映射
PLATFORM_VM_STATUS_ENUM_MAPPER = {
    PlatformVmStatus.POWEREDON.value: 0,
    PlatformVmStatus.POWEREDOFF.value: 1,
    PlatformVmStatus.SUSPENDED.value: 0
}


# timeout for connetct to  VMware vSphere platform
TIMEOUT_CONNECT_TO_PLATFORM = 200


# qingcloud metric 与 VMware metric 映射关系
METRIC_COUNTER_MAPPING = {
    "cpu": "cpu.usage.average",
    "memory": "mem.usage.average",
    "disk_rd": "disk.read.average",
    "disk_wr": "disk.write.average",
    "disk_ri": "disk.numberReadAveraged.average",
    "disk_wi": "disk.numberWriteAveraged.average",
    "disk_us": "disk.usage.average",
    "if_rx": "net.received.average",
    "if_tx": "net.transmitted.average"
}

METRIC_UNIT_MAPPING = {
    "cpu": "%",
    "memory": "%",
    "disk_rd": "Kbps",
    "disk_wr": "Kbps",
    "disk_ri": "count",
    "disk_wi": "count",
    "disk_us": "%",
    "if_rx": "Kbps",
    "if_tx": "Kbps"
}

METRIC_CN_MAPPING = {
    "cpu": "cpu",
    "memory": "内存",
    "disk_rd": "磁盘读字节",
    "disk_wr": "磁盘写字节",
    "disk_ri": "磁盘读次数",
    "disk_wi": "磁盘写次数",
    "disk_us": "磁盘使用量",
    "if_rx": "入带宽",
    "if_tx": "出带宽"
}