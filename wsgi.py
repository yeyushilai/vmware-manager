# -*- coding: utf-8 -*-

from vmware_manager_server import get_app
from log.logger import logger

application = get_app()
logger.info("vmware manager server is running now.")


def main():
    get_app().run(port=8888, debug=True)


if __name__ == '__main__':
    main()
