# -*- coding: utf-8 -*-
# @Time    : 2020/7/2 15:16
# @Author  : lightsmile
# @Software: PyCharm

from lighttext import KeywordProcessor


if __name__ == '__main__':
    kp = KeywordProcessor()
    kp.add_keyword("曹操")
    kp.add_keyword("曹丕")
    kp.add_keyword("司马懿")
    kp.add_keyword("司马")
    stn = "曹操、曹丕和司马懿一起去吃大盘鸡。"

    print(kp.extract_keywords(stn))
