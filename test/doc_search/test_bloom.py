# -*- coding: utf-8 -*-
from lighttext.doc_search.bloom import BloomFilter


if __name__ == '__main__':
    bf = BloomFilter(10)
    bf.add_value('dog')
    bf.add_value('fish')
    bf.add_value('cat')
    print(bf.contents)
