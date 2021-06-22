# -*- coding: utf-8 -*-

# copied from https://gitee.com/fastnlp/fastNLP/blob/master/fastNLP/core/utils.py line:233
class Option(dict):
    """a dict can treat keys as attributes"""

    def __getattr__(self, item):
        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError(item)

    def __setattr__(self, key, value):
        if key.startswith('__') and key.endswith('__'):
            raise AttributeError(key)
        self.__setitem__(key, value)

    def __delattr__(self, item):
        try:
            self.pop(item)
        except KeyError:
            raise AttributeError(item)

    def __getstate__(self):
        return self

    def __setstate__(self, state):
        self.update(state)
