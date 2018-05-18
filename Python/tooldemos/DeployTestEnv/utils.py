#coding: utf-8


class DictObj(dict):
    '''class doc'''
    def __init__(self, names=(), values=(), **kw):
        super(DictObj, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            setattr(self, key, None)
            return self[key]
            # raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value