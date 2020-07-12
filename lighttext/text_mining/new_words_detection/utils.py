import os
import re

import jieba

# 词性规范详见：https://github.com/NLPchina/ansj_seg/wiki/%E8%AF%8D%E6%80%A7%E6%A0%87%E6%B3%A8%E8%A7%84%E8%8C%83
STOP_WORDS_FILE = os.path.dirname(__file__) + '/../../data/stopwords.txt'
DICT_FILE = os.path.dirname(__file__) + '/../../data/dict.txt'
PRE_FILTER_POS = os.path.dirname(__file__) + '/../../data/pre_filter_pos.txt'
POST_FILTER_POS = os.path.dirname(__file__) + '/../../data/post_filter_pos.txt'
BAN_FILE = os.path.dirname(__file__) + '/../../data/ban.txt'
spliter = re.compile('[\s]+')


def return_zero():
    return 0


def get_stopwords():
    with open(STOP_WORDS_FILE, 'r', encoding='utf-8') as f:
        stopwords = [line.strip() for line in f]
    return set(stopwords)


def gen_ngram(input_list, n):
    result = []
    for i in range(1, n + 1):
        result.extend(zip(*[input_list[j:] for j in range(i)]))
    return result


def load_dictionary(filename=DICT_FILE):
    """
    加载外部词频记录
    :param filename:
    :return:
    """
    word_freq = {}
    with open(filename, encoding='utf-8') as f:
        for line in f:
            try:
                line_list = spliter.split(line.strip())
                # 规定最少词频
                if int(line_list[1]) > 2:
                    word_freq[line_list[0]] = (int(line_list[1]), line_list[2])  # 词频，词性
            except IndexError as e:
                print(line)
                continue
    return word_freq


def load_data(filename):
    """

    :param filename:
    :return: 二维数组,[[句子1分词list], [句子2分词list],...,[句子n分词list]]
    """
    data = []
    with open(filename, encoding='utf-8') as f:
        for line in f:
            word_list = [x for x in jieba.cut(line.strip(), cut_all=False)]
            data.append(word_list)
    return data


def get_pre_list():
    pre_list = []
    with open(PRE_FILTER_POS, encoding='utf-8') as f:
        pre_list.extend([x.strip() for x in f.readlines()])
    return pre_list


def get_post_list():
    post_list = []
    with open(POST_FILTER_POS, encoding='utf-8') as f:
        post_list.extend([x.strip() for x in f.readlines()])
    return post_list


def get_ban_list():
    ban_list = [' ']
    with open(BAN_FILE, encoding='utf-8') as f:
        ban_list.extend([x.strip() for x in f.readlines()])
    return ban_list


if __name__ == '__main__':
    print(get_stopwords())
    data = ['它', '是', '小', '狗']
    print(gen_ngram(data, 4))
    print(spliter.split('与	2510  p'))
