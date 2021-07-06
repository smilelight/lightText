# -*- coding: utf-8 -*-
from lighttext.doc_search.searcher import Searcher


if __name__ == '__main__':
    searcher = Searcher()
    searcher.add_events('曹操和刘备去赶集')
    searcher.add_events('人生苦短，我用Python')
    print(list(searcher.search('曹操')))
