# -*- coding: utf-8 -*-

from constants import (
    ACTION_VMWARE_MANAGER_HEALTH_CHECK_HEALTH,
)
from api.constants import (
    CHANNEL_API,
    CHANNEL_SESSION,
    ROLE_GLOBAL_ADMIN,
    ROLE_ZONE_ADMIN,
    ROLE_CONSOLE_ADMIN,
    ROLE_NORMAL_USER,
    ROLE_PARTNER,
    ROLE_AGENT,
)


API_ACL_VMWARE_MANAGER_HEALTH = {
        ACTION_VMWARE_MANAGER_HEALTH_CHECK_HEALTH: {
            CHANNEL_API: [ROLE_GLOBAL_ADMIN, ROLE_NORMAL_USER,
                          ROLE_CONSOLE_ADMIN, ROLE_ZONE_ADMIN,
                          ROLE_PARTNER, ROLE_AGENT],
            CHANNEL_SESSION: [ROLE_GLOBAL_ADMIN, ROLE_NORMAL_USER,
                              ROLE_CONSOLE_ADMIN, ROLE_ZONE_ADMIN,
                              ROLE_PARTNER, ROLE_AGENT],
        }
}
