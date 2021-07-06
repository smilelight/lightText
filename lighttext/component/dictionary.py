# -*- coding: utf-8 -*-
from typing import List
from collections import defaultdict, Counter


class Dictionary:
    def __init__(self):
        self._dict = dict()

    def set(self, word: str, obj: object):
        self._dict[word] = obj

    def get(self, word: str):
        if word in self._dict:
            return self._dict[word]
        return None

    def __contains__(self, item):
        return item in self._dict

    def __str__(self):
        return str(self._dict)
