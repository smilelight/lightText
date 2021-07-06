# -*- coding: utf-8 -*-
from typing import List
import jieba


def token_split(text: str) -> List[str]:
    return list(jieba.cut(text))
