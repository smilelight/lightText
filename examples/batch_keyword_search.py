# -*- coding: utf-8 -*-
# @Time    : 2020/7/12 18:22
# @Author  : lightsmile
# @Software: PyCharm

import time

from tqdm import tqdm
from lightutils import read_json_line, cutoff_iter
from lighttext import KeywordProcessor

data_path = r"D:\Data\NLP\corpus\baike_info_1_to_10000\result.json"
data_path2 = r"D:\Data\NLP\corpus\baike_info_10000_to_100000\result.json"

if __name__ == '__main__':
    word_list = []
    for line in tqdm(read_json_line(data_path)):
        if 'info' in line:
            word_list.append(line['info']['word'])

    for line in tqdm(read_json_line(data_path2)):
        if 'info' in line:
            word_list.append(line['info']['word'])

    word_set = set(word_list)

    print(len(word_list))
    print(len(word_set))

    for word in cutoff_iter(word_set):
        print(word)

    a = time.time()
    kp = KeywordProcessor()
    b = time.time()
    for word in tqdm(word_set):
        if len(word) > 1:
            kp.add_keyword(word)
    c = time.time()
    print(c - b, b - a)
    print(kp.keyword_nums)
    print("曹操" in kp)
    print(len(kp.keyword_sets))
    print(len(kp))

    sentence = """东汉末年，天下大乱，曹操以汉朝天子刘协的名义征讨四方，对内消灭二袁、吕布、刘表、马超、韩遂等割据势力，对外降服南匈奴、乌桓、鲜卑等，统一了中国北方，并实行一系列政策恢复经济生产和社会秩序，扩大屯田、兴修水利、奖励农桑、重视手工业、安置流亡人口、实行“租调制”，从而使中原社会渐趋稳定、经济出现转机。 """

    print(kp.extract_keyword_sequence(sentence))
    print(kp.extract_keywords(sentence))



