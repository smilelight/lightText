import math
import gc
from collections import defaultdict

from .utils import gen_ngram, get_stopwords, load_data, load_dictionary, return_zero, get_post_list, get_pre_list, \
    get_ban_list

DEFAULT_DICT = load_dictionary()
DEFAULT_UNI_SUM = sum([x[0] for x in DEFAULT_DICT.values()])
DEFAULT_STOP_WORDS = get_stopwords()
pre_list = get_pre_list()
post_list = get_post_list()
ban_list = get_ban_list()


class WordNode:
    """
    字结点
    """
    def __init__(self, word):
        self._word = word
        self._count = 0
        self.freq = 0
        self.pmi = 0
        self._left = defaultdict(return_zero)
        self._right = defaultdict(return_zero)
        self._child = {}
        self.left_entropy = 0
        self.right_entropy = 0

    def __getitem__(self, item):
        return self._child[item]

    def __contains__(self, item):
        return item in self._child

    def __setitem__(self, key, value):
        self._child[key] = value

    def values(self):
        return self._child.values()

    def items(self):
        return self._child.items()

    def add_count(self, num=1):
        self._count += num

    def get_count(self):
        return self._count

    def get_freq(self):
        return self.freq

    def update_freq(self, words_sum):
        self.freq = self._count / words_sum

    def add_left_nbr(self, word):
        self._left[word] += 1

    def add_right_nbr(self, word):
        self._right[word] += 1

    def update_pmi(self, pmi):
        self.pmi = pmi

    def compute_entropy(self):
        left_length = sum(self._left.values())
        self.left_entropy = sum(map(lambda x: -x/left_length * math.log(x/left_length, 2), self._left.values()))
        right_length = sum(self._right.values())
        self.right_entropy = sum(map(lambda x: -x / right_length * math.log(x / right_length, 2), self._right.values()))

    def __str__(self):
        return self._word


class NewWordDetector:
    """
    字字典
    """
    def __init__(self, dic_file=None, accumulate=False):
        """
        新词发现检测程序
        :param dic_file: 自定义词典文件，每行格式如：`知无不谈 3 i`，分别表示：词语，频次，词性（这里是最常用词性）
        :param accumulate: 是否开启累积模式，默认为False，即每次调用`load_file`函数都会对模型进行初始化
        """
        self.root = {}  # interesting!
        self._pmi = False
        self._entropy = False
        self._dictionary = None
        self._uni_sum = 0
        self._accumulate = accumulate
        if dic_file:
            self._dictionary = load_dictionary(dic_file)
            self._uni_sum = sum([x[0] for x in self._dictionary.values()])
        else:
            self._dictionary = DEFAULT_DICT
            self._uni_sum = DEFAULT_UNI_SUM

    def add(self, word):
        word_node = self.get_node(word)
        word_node.add_count()
        if len(word) > 1:
            left_sub_node = self.get_node(word[:-1])
            left_sub_node.add_right_nbr(word[-1])
            right_sub_node = self.get_node(word[1:])
            right_sub_node.add_left_nbr(word[0])

    def add_node(self, word):
        node = self.root
        for char in word:
            if char not in node:
                new_node = WordNode(char)
                node[char] = new_node
                node = new_node
            else:
                node = node[char]
        return node

    def search_node(self, word):
        node = self.root
        for char in word:
            if char in node:
                node = node[char]
            else:
                return None
        return node

    def get_node(self, word):
        node = self.search_node(word)
        if node:
            return node
        else:
            return self.add_node(word)

    def build(self, data):
        stop_words = DEFAULT_STOP_WORDS
        if not self._accumulate:
            self.clear()
        for word_list in data:
            ngrams = gen_ngram(word_list, 3)
            for d in ngrams:
                if set(d) & stop_words:
                    continue
                else:
                    self.add(d)

    def clear(self):
        self.root = {}
        self._pmi = False
        self._entropy = False
        gc.collect()

    def load_file(self, file_name):
        data = load_data(file_name)
        self.build(data)

    def update_freq(self):
        uni_sum, bi_sum = self.count_sum()
        for word, child in self.root.items():
            if word in self._dictionary:
                child.add_count(self._dictionary[word][0])
            child.update_freq(uni_sum)
        for child in self.root.values():
            for descendant in child.values():
                descendant.update_freq(bi_sum)

    def count_sum(self):
        uni_sum = 0
        bi_sum = 0
        for word in self.root.values():
            count = word.get_count()
            uni_sum += count
        for child in self.root.values():
            for descendant in child.values():
                bi_sum += descendant.get_count()
        return uni_sum + self._uni_sum, bi_sum

    def count_pmi(self):
        self.update_freq()
        for child in self.root.values():
            for word, descendant in child.items():
                descendant.update_pmi(
                    math.log(descendant.get_freq(), 2) -
                    math.log(child.get_freq(), 2) -
                    math.log(self.root[word].get_freq(), 2)
                )
        self._pmi = True

    def compute_entropy(self):
        for child in self.root.values():
            for descendant in child.values():
                descendant.compute_entropy()
        self._entropy = True

    def get_top_k(self, k=5, debug=False, threshold=0.1):
        if not self._pmi:
            self.count_pmi()
        if not self._entropy:
            self.compute_entropy()
        result = {}
        for ch_word, child in self.root.items():
            for des_word, descendant in child.items():
                pmi = descendant.pmi
                freq = descendant.freq
                left_entropy = descendant.left_entropy
                right_entropy = descendant.right_entropy
                result[ch_word + '_' + des_word] = {
                    'pmi': descendant.pmi,
                    'freq': descendant.freq,
                    'left_entropy': descendant.left_entropy,
                    'right_entropy': descendant.right_entropy,
                    'score': (pmi + min(left_entropy, right_entropy)) * freq
                }
        result = {word: info for word, info in result.items() if self.filter_word(word)}
        result = sorted(result.items(), key=lambda x: x[1]['score'], reverse=True)
        if threshold:
            result = [x for x in result if x[1]['score'] >= threshold]
        if debug:
            return result[:k]
        return [(x[0], x[1]['score']) for x in result][:k]

    def filter_word(self, word):
        words = word.split('_')

        if self._dictionary:
            if words[0] in self._dictionary and self._dictionary[words[0]][1] in \
                    pre_list:
                return False
            if words[-1] in self._dictionary and self._dictionary[words[-1]][1] in post_list:
                return False
            if words[0] not in self._dictionary and len(words[0]) > 2:  # 禁止造词，和jieba分出词典外的词
                return False
            if words[1] not in self._dictionary and len(words[1]) > 2:  # 禁止造词，和jieba分出词典外的词
                return False
            for word in words:
                if word in ban_list:
                    return False
        return True
