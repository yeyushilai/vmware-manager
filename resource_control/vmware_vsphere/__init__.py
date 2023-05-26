# -*- coding: utf-8 -*-

from pyVmomi import vim

from log.logger import logger
from utils.net import (
    is_reachable,
    is_port_open
)

from resource_control.vmware_vsphere.interface import VMwareVSphereInterface


class VMwareVSphere(object):
    """ VMware vSphere类 """

    def __init__(self, account):
        self.account = account
        self.vi = VMwareVSphereInterface(account)

    def is_connected(self):
        """检查和VMware vSphere平台的连通性
        联通返回True，不连通返回False
        """

        host = self.account["host"]
        port = int(self.account["port"])

        # 检查IP是否通达
        if not is_reachable(host, retries=5):
            logger.error("check network of VMware vSphere failed, host: {host}"
                         ", reason: ip is not reachable"
                         "".format(host=host))
            return False

        # 检查端口是否通达
        if not is_port_open(host, port):
            logger.error("check network of VMware vSphere failed, host: {host}"
                         ", port: {port}, reason: port is not open"
                         "".format(host=host, port=port))
            return False

        # 检测是否联通
        return self.vi.check_connected()

    def detail_root_folder(self):
        root_folder = self.vi.root_folder
        data = self._loop_child_entity(root_folder)
        return data

    def detail_folder(self, folder_moid, datacenter_moid):
        folder_obj = self.vi.get_folder(folder_moid, datacenter_moid)
        data = self._loop_child_entity(folder_obj, datacenter_moid)
        return data

    @staticmethod
    def _loop_child_entity(folder_obj, datacenter_moid=None):
        data = []
        for mo_obj in folder_obj.childEntity:
            mo_dict = {
                "name": mo_obj.name,
                "moid": mo_obj._moId,
                "datacenter_id": datacenter_moid
                # "path": self.vi.parse_obj_path(mo_obj.parent, "")
            }
            if isinstance(mo_obj, vim.VirtualMachine):
                mo_dict["type"] = "vm"
                mo_dict["uuid"] = mo_obj.summary.config.uuid
            if isinstance(mo_obj, vim.Datacenter):
                mo_dict["type"] = "datacenter"
                mo_dict["vm_folder_moid"] = mo_obj.vmFolder._moId
                mo_dict["vm_folder_name"] = mo_obj.vmFolder.name
            if isinstance(mo_obj, vim.Folder):
                mo_dict["type"] = "folder"
                mo_dict["has_child"] = bool(mo_obj.childEntity)
            data.append(mo_dict)
        return data

    def list_datacenter(self):
        dc_list = list()
        for dc_obj in self.vi.datacenters:
            dc_info = self._layout_datacenter(dc_obj=dc_obj)
            dc_list.append(dc_info)
        return dc_list

    def detail_datacenter(self, dc_moid):
        return self._layout_datacenter(dc_moid=dc_moid)

    def _layout_datacenter(self, dc_moid=None, dc_obj=None):
        assert dc_moid or dc_obj
        if not dc_obj:
            dc_obj = self.vi.get_datacenter_by_moid(dc_moid)

        dc_info = dict()
        dc_info["name"] = dc_obj.name
        dc_info["moid"] = dc_obj._moId
        dc_info["vm_folder_name"] = dc_obj.vmFolder.name
        dc_info["vm_folder_moid"] = dc_obj.vmFolder._moId
        dc_info["host_folder_name"] = dc_obj.hostFolder.name
        dc_info["host_folder_moid"] = dc_obj.hostFolder._moId

        cluster_list = []
        for child in dc_obj.hostFolder.childEntity:
            if isinstance(child, vim.ClusterComputeResource):
                cluster_dict = dict()
                cluster_dict["name"] = child.name
                cluster_dict["moid"] = child._moId

                host_list = []
                for host in child.host:
                    host_dict = dict()
                    host_dict["name"] = host.name
                    host_dict["moid"] = host._moId
                    host_list.append(host_dict)
                cluster_dict["host_list"] = host_list
                cluster_list.append(cluster_dict)

        dc_info["cluster_list"] = cluster_list
        return dc_info

    def list_cluster(self, cluster_name=None):
        result = list()

        if cluster_name:
            cluster = self.vi.get_cluster_by_name(cluster_name)
            clusters = [cluster]
        else:
            clusters = self.vi.clusters

        for cluster in clusters:
            temp_dict = dict()
            temp_dict["name"] = cluster.name
            """
            后续视情况返回字段，目前识别到可以返回的字段:
            1.集群的统计信息
            2.集群的网络信息
            3.集群的节点信息
            4.集群的资源池信息
            """
            result.append(temp_dict)
        return result

    def list_cluster_vm(self, cluster_name):
        """展示平台中某一个集群里的虚拟机"""

        vms_data = list()
        for vm_data in self.vi.get_cluster_vms(cluster_name):
            try:
                vms_data.append(self.vi.layout_dict_vm_data(vm_data))
            except Exception as e:
                uuid = vm_data.get("summary.config.uuid")
                logger.exception("layout data from vm data failed, uuid: "
                                 "{uuid}, reason: {reason}"
                                 "".format(uuid=uuid, reason=e))
                continue

        return vms_data

    def list_vm(self, vm_properties=None):
        """展示平台中的所有的虚拟机"""

        if vm_properties is None:
            vm_properties = [
                "parent",
                "guest.ipAddress",
                "guest.toolsStatus",
                "summary.config.uuid",
                "summary.config.template",
                "summary.config.name",
                "summary.runtime.powerState",
                "summary.config.guestId",
                "summary.config.guestFullName",
                "config.hardware.numCPU",
                "config.hardware.memoryMB",
                "config.annotation"
            ]
            version = self.vi.version
            if "6.7" in version:
                vm_properties.append("config.createDate")
            if "7.0" in version:
                vm_properties.append("config.createDate")
            if "8.0" in version:
                vm_properties.append("config.createDate")

        vms_list = list()
        for vm_data in self.vi.get_vms_properties(vm_properties):
            try:
                vms_list.append(self.vi.layout_dict_vm_data(vm_data))
            except Exception as e:
                uuid = vm_data.get("summary.config.uuid")
                logger.exception("layout data from vm data failed, uuid: "
                                 "{uuid}, reason: {reason}"
                                 "".format(uuid=uuid, reason=e))
                continue
        return vms_list

    def get_vm(self, vm_name=None, vm_uuid=None):
        if vm_name:
            vm_obj = self.vi.get_vm_by_name(vm_name)
        else:
            vm_obj = self.vi.get_vm_by_uuid(vm_uuid)

        if not vm_obj:
            return vm_obj

        return self.vi.layout_obj_vm_data(vm_obj)

    def get_vm_ticket(self, vm_uuid):
        vm_ticket_obj = self.vi.get_vm_ticket_by_uuid(vm_uuid)
        vm_ticket = {
            "host": vm_ticket_obj.host,
            "port": vm_ticket_obj.port,
            "ticket": vm_ticket_obj.ticket,
        }
        return vm_ticket

    def get_vm_power_status(self, vm_uuid):
        vm_obj = self.vi.get_vm_by_uuid(vm_uuid)
        return vm_obj.summary.runtime.powerState

    def update_vm(self, vm_uuid, vm_info):
        return self.vi.update_vm_by_uuid(vm_uuid, vm_info)

    def operate_vm(self, vm_uuid, operation):
        return self.vi.operate_vm_by_uuid(vm_uuid, operation)
