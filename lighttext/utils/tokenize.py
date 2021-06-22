# -*- coding: utf-8 -*-
import jieba

def token_split(text: str):
    return list(jieba.cut(text))
