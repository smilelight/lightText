# -*- coding: utf-8 -*-
from typing import List
from collections import defaultdict, Counter


class InvertedIndex:
    def __init__(self):
        self._inverted_index = defaultdict(Counter)
        self._documents = dict()

    def build_from_corpus(self, corpora: List[List[str]]):
        for idx, corpus in enumerate(corpora):
            for word in corpus:
                self._inverted_index[word][idx] += 1

