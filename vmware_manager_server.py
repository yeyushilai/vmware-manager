# -*- coding: utf-8 -*-

from flask_cors import CORS

from log.logger_name import set_logger_name
set_logger_name("vmware_manager_server")
from log.logger import logger

from utils.global_conf import (
    get_pg,
    get_zk,
    connect_zk,
    get_mc,
    get_cb_conf
)
from utils.misc import exit_program
from db.pg_model import PGModel
from db.constants import DB_VMWARE_MANAGER
from server.locator import set_global_locator
from mc.mc_model import MCModel
from zk.dlocator import DLocator

import context
import connexion
from connexion.apps.flask_app import FlaskJSONEncoder
from constants import PITRIX_CONF_HOME
from comm.base_client import BaseClient


class WebService(object):
    """ web service is a vmware_manager restful server """

    def __init__(self, conf_file):
        """
        constructor
        :param conf_file:
        """

        self.conf_file = conf_file

        # initialize context
        ctx = context.instance()
        ctx.conf_file = conf_file

        # domain name
        ctx.domain_name = get_cb_conf().conf.get("domain_name")

        # connect to postgresql db
        ctx.pg = get_pg(DB_VMWARE_MANAGER, maxconn=50)
        if ctx.pg is None:
            logger.error("connect to PostgreSQL failed: can't connect")
            exit_program(-1)
        ctx.pgm = PGModel(ctx.pg)

        # connect to zookeeper
        ctx.locator = DLocator()
        ctx.zk = get_zk(WebService._zk_connect_cb,
                        WebService._zk_disconnect_cb)
        if 0 != connect_zk(ctx.zk):
            logger.error("connect to zookeeper failed: can't connect")
            exit_program(-1)
        set_global_locator(ctx.locator)

        # connect to memcached
        ctx.mcclient = get_mc()
        if not ctx.mcclient:
            logger.error("connect to memcached failed: can't connect")
            exit_program(-1)
        ctx.mcm = MCModel(ctx.mcclient)

        # shared base client
        ctx.client = BaseClient(use_sock_pool=True)
        self.connexion_app = connexion.App(__name__,
                                           specification_dir='./spec/')
        self.connexion_app.app.json_encoder = FlaskJSONEncoder
        self.connexion_app.add_api('swagger.yaml',
                                   arguments={'title': 'Swagger Petstore'})
        CORS(self.connexion_app.app)

    @staticmethod
    def _zk_disconnect_cb():
        """ callback when zookeeper is disconnected """
        # stop locator service
        ctx = context.instance()
        ctx.locator.stop()

    @staticmethod
    def _zk_connect_cb():
        """ callback when zookeeper is connected """
        # start locator service
        ctx = context.instance()
        ctx.locator.start(ctx.zk)

        # # register self as server
        # from utils.net import get_hostname
        # ctx.locator.register(SERVER_TYPE_VMWARE_MANAGER_SERVER,
        #                      get_hostname(),
        #                      VMWARE_MANAGER_SERVER_PORT)

    def run(self, port=None, server=None, debug=None, host=None, **options):
        # pragma: no cover
        ctx = context.instance()
        ctx.conf_file = self.conf_file
        self.connexion_app.run(port=port, server=server, debug=debug,
                               host=host, **options)

    def __call__(self, environ, start_response):  # pragma: no cover
        """
        Makes the class callable to be WSGI-compliant.
        As Flask is used to handle requests, this is a passthrough-call to
          the Connexion/Flask callable class.
        This is an abstraction to avoid directly referencing the app attribute
          from outside the class and protect it from unwanted modification.
        """
        ctx = context.instance()
        ctx.conf_file = self.conf_file
        return self.connexion_app(environ, start_response)


def get_app():
    conf_file = "%s/%s.yaml" % (PITRIX_CONF_HOME, "vmware_manager_server")
    app = WebService(conf_file)
    logger.info("vmware manager server is running now.")
    return app


def main():
    get_app().run(port=8888, debug=True)


if __name__ == '__main__':
    main()

__all__ = [get_app]
