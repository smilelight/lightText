import os

import jieba


STOP_WORDS_FILE = os.path.dirname(__file__) + '/../../data/stopword.txt'
DICT_FILE = os.path.dirname(__file__) + '/../../data/dict.txt'


def return_zero():
    return 0


def get_stopwords():
    with open(STOP_WORDS_FILE, 'r', encoding='utf-8') as f:
        stopwords = [line.strip() for line in f]
    return set(stopwords)


def gen_ngram(input_list, n):
    result = []
    for i in range(1, n+1):
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
                line_list = line.strip().split(' ')
                # 规定最少词频
                if int(line_list[1]) > 2:
                    word_freq[line_list[0]] = (int(line_list[1]), line_list[2])
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


if __name__ == '__main__':
    print(get_stopwords())
    data = ['它', '是', '小', '狗']
    print(gen_ngram(data, 4))
