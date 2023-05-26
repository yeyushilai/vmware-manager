# -*- coding: utf-8 -*-

import context


def get_cache(prefix, key):
    ctx = context.instance()

    return ctx.mcm.get(prefix, key)


def set_cache(prefix, key, val, time=3600*24):
    ctx = context.instance()

    return ctx.mcm.set(prefix, key, val, time=time)


def unset_cache(prefix, key):
    ctx = context.instance()

    return ctx.mcm.delete(prefix, key)