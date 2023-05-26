# -*- coding: utf-8 -*-

from log.logger import logger

from return_tools import return_success


def handle_check_health_local(kwargs):
    logger.debug('handle check health local start, {}'.format(kwargs))
    return return_success(kwargs, kwargs, dump=False)
