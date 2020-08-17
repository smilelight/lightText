# -*- coding: utf-8 -*-
# @Time    : 2020/7/2 15:05
# @Author  : lightsmile
# @Software: PyCharm

from typing import List, Set, Union
from .ac import AC


def get_longest_sequence(lst, sen):
    """
    使用动态规划算法求取最长序列
    :param lst: 关键词列表
    :param sen: 原始句子
    :return: 最长关键词序列与长度
    """
    target = len(sen)
    matrix = [[0] * (target+1) for i in range(len(lst)+1)]
    for i in range(1, len(lst) + 1):
        for j in range(1, target+1):
            if j >= lst[i-1][2]:
                matrix[i][j] = max(matrix[i-1][j], matrix[i-1][lst[i-1][1]] + len(lst[i-1][0]))
            else:
                matrix[i][j] = matrix[i-1][j]
    a = []
    n = target
    for m in range(len(lst), 0, -1):
        if lst[m-1][2] <= n and matrix[m-1][n] < matrix[m-1][lst[m-1][1]] + len(lst[m-1][0]):
            a.append(lst[m-1])
            n = lst[m-1][1]
    return a[::-1], matrix[-1][-1]


class KeywordProcessor:
    def __init__(self):
        self.ac = AC()
        self.word_types = dict()

    def add_keyword(self, word: str, word_type=None):
        self.ac.add_word(word)
        if word_type:
            self.word_types[word] = word_type

    def remove_keyword(self, word: str):
        self.ac.remove_word(word)
        if word in self.word_types:
            del self.word_types[word]

    @property
    def keyword_nums(self):
        return len(self.ac.end_notes.keys())

    def __contains__(self, item):
        return item in self.ac.end_notes

    def __len__(self):
        return len(self.ac.end_notes.keys())

    @property
    def keyword_sets(self):
        return set(self.ac.end_notes.keys())

    def add_keywords(self, words: Union[List, Set]):
        if isinstance(words, list):
            words = set(words)
        for word in words:
            self.add_keyword(word)

    def extract_keywords(self, sentence: str):
        pointer_set = set()
        ret = []
        for index, char in enumerate(sentence):
            kw_list = self.ac.go(pointer_set, char)
            ret += [[kw, index - len(kw) + 1, index + 1] for kw in kw_list]
        for item in ret:
            if item[0] in self.word_types:
                item.append(self.word_types[item[0]])
        return ret

    def extract_keyword_sequence(self, sentence: str, contact=True):
        keywords = self.extract_keywords(sentence)
        words, max_len = get_longest_sequence(keywords, sentence)
        if contact:
            res = []
            for word in words:
                if not res:
                    res.append(word)
                elif res[-1][2] == word[1]:
                    if res[-1][0] + word[0] in self:
                        res[-1] = [res[-1][0] + word[0], res[-1][1], word[2]]
                        if res[-1][0] in self.word_types:
                            res[-1].append(self.word_types[res[-1][0]])
                    else:
                        res.append(word)
                else:
                    res.append(word)
            return res
        else:
            return words


