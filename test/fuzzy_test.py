# -*- coding: utf-8 -*-
from fuzzywuzzy import fuzz

if __name__ == '__main__':
    a = 'asdf'
    b = 'sdfa'
    print(fuzz.partial_ratio(a, b))
