# -*- coding: utf-8 -*-
from typing import List
from collections import defaultdict

from .bloom import BloomFilter
from ..utils.tokenize import token_split


class Searcher:
    def __init__(self):
        self.bf = BloomFilter(256)
        self.terms = defaultdict(set)
        self.events = []

    def add_events(self, event: str):
        event_id = len(self.events)
        self.events.append(event)

        for term in token_split(event):
            self.bf.add_value(term)

            self.terms[term].add(event_id)

    def search(self, term: str):
        if not self.bf.might_contain(term):
            return

        if term not in self.terms:
            return

        for event_id in sorted(self.terms[term]):
            yield self.events[event_id]

    def search_all(self, terms: List[str]):
        results = set(range(len(self.events)))
        for term in terms:
            if not self.bf.might_contain(term):
                return
            if term not in self.terms:
                return

            results = results.union(self.terms[term])

        for event_id in sorted(results):
            yield self.events[event_id]
