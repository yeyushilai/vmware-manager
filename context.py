# -*- coding: utf-8 -*-

import os
from log.logger import logger
from utils.yaml_tool import yaml_load
from constants import API_SECURE_PORTS


class VMwareManagerContext(object):
    """ thread context for VMware Manager
    """
    def __init__(self):
        self.conf_file = None
        self.conf = None
        self.pg = None
        self.pgm = None
        self.locator = None
        self.zk = None
        self.client = None
        self.mcclient = None
        self.domain_name = None

    def get_server_conf(self):
        if not self.conf:
            # get config
            if self.conf_file != "":
                if not os.path.isfile(self.conf_file):
                    logger.error("config file [%s] not exist" % self.conf_file)
                    return

                with open(self.conf_file, "r") as fd:
                    self.conf = yaml_load(fd).get('ws_server', None)

    def __getattr__(self, attr):
        # get conf short cut
        try:
            self.get_server_conf()
            if self.conf:
                if attr == "iaas_client_conf":
                    return self.conf['iaas_client_conf']
                if attr == "secure_ports":
                    return self.conf.get('secure_ports', API_SECURE_PORTS)
                if attr == "zone_id":
                    return self.conf.get('zone_id', None)
                if attr == "enable_find_fg_with_zk":
                    return self.conf.get('enable_find_fg_with_zk', False)
                if attr == "check_access_limit":
                    return self.conf.get('check_access_limit', False)
                if attr == "verify_signature_via_iam":
                    return self.conf.get('verify_signature_via_iam', True)
                if attr == "broker_port":
                    return self.conf.get('broker_port')

        except Exception as _:
            pass

        return None


g_ws_ctx = VMwareManagerContext()


def instance():
    """ get webservice context """
    global g_ws_ctx
    return g_ws_ctx
