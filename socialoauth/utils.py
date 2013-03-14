# -*- coding: utf-8 -*-


def import_module(m):
    m = m.split('.')
    c = m.pop(-1)
    module = __import__('.'.join(m), fromlist=[c])
    return getattr(module, c)

