from log.logger import logger
from utils.thread_local import (
    get_request_zone,
    set_request_zone,
)

import context
from resource_control.iaas.interface import get_all_zones

g_region_zones = None


def get_region_zones():
    """
    return dict, key is region id, value are zone_ids.
    :return:
    """

    global g_region_zones
    if g_region_zones:
        return g_region_zones

    zones = get_all_zones()  # type: dict

    if not zones:
        logger.error("get zones failed")
        return None
    logger.debug("get zones %s" % zones)

    g_region_zones = {}

    for zone_id, zone in zones.items():
        region_id = zone['region_id']
        if region_id not in g_region_zones:
            g_region_zones[region_id] = []
        g_region_zones[region_id].append(zone)

    return g_region_zones


def is_region_id(zone_id):

    region_zones = get_region_zones()
    if zone_id and region_zones and zone_id in region_zones:
        return True

    return False


def get_zones(region_id):
    """
    return list_dict, zone info
    :param region_id:
    :return:
    """
    region_zones = get_region_zones()

    if region_id not in region_zones:
        return None
    return region_zones[region_id]


def dispatch_region_request(req, sender):
    request_zone = None

    ctx = context.instance()
    # convert region id to zone id when needed
    if 'zone' in req:
        request_zone = get_request_zone()
        if request_zone and not is_region_id(req['zone']):
            # already dispatched
            req['request_zone'] = request_zone
            return request_zone

        zone_id = req['zone']
        request_zone = zone_id
        req['request_zone'] = request_zone

        if is_region_id(zone_id):
            if ctx.region_default_zone:
                req['zone'] = ctx.region_default_zone[zone_id]
            logger.debug("dispatch region [%s] request to zone [%s] with "
                         "ctx.region_default_zone [%s]",
                         request_zone, req['zone'], ctx.region_default_zone)

    set_request_zone(request_zone)

    return request_zone
