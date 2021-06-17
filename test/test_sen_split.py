# -*- coding: utf-8 -*-
from lighttext.utils.sen_split import split_sentence

if __name__ == '__main__':
    text = "自然语言处理( Natural Language Processing, NLP)是计算机科学领域与人工智能领域中的一个重要方向。 它研究能实现人与计算机之间用自然语言进行有效通信的各种理论和方法。 自然语言处理是一门融语言学、计算机科学、数学于一体的科学。 ... 因而它是计算机科学的一部分 。"
    lst = split_sentence(text)
    # print(lst)
    [print(x) for x in lst]

