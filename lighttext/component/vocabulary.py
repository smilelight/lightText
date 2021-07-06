import itertools
from typing import List, Dict
from collections import Counter
from lightutils import logger


class Vocabulary:
    """
    词汇表结构，做word和id之间的映射
    """
    def __init__(self, padding: str = '<pad>', unknown: str = '<unk>'):
        self._word2idx: Dict = dict()
        self._idx2word: Dict = dict()
        self._word_count: Counter = Counter()
        self.padding = padding
        self.unknown = unknown
        self._init()

    def _init(self):
        self._word2idx = {self.padding: 0, self.unknown: 1}
        self._idx2word = {0: self.padding, 1: self.unknown}

    def build_from_corpora(self, corpora: List[List[str]]) -> None:
        """
        从corpora中构造词典
        Args:
            corpora: 分词后的语料

        Returns:

        """
        self._word_count.update(itertools.chain(*corpora))
        offset = len(self.special_words)
        self._word2idx.update({word: idx + offset for idx, word in enumerate(self._word_count)})
        self._idx2word.update({idx + offset: word for idx, word in enumerate(self._word_count)})

    def __len__(self) -> int:
        assert len(self._word2idx) == len(self._idx2word)
        return len(self._word2idx)

    def add_word(self, word: str):
        self._word_count[word] += 1
        idx = len(self)
        if word not in self._word2idx:
            self._word2idx[word] = idx
        if idx not in self._idx2word:
            self._idx2word[idx] = word

    def update(self, word_lst: List[str]):
        for word in word_lst:
            self.add_word(word)

    def to_word(self, idx: int):
        return self._idx2word[idx]

    def to_idx(self, word: str):
        word = word if word in self else self.unknown
        if word == self.unknown:
            logger.error('{} not in vocab'.format(word))
        return self[word]
    
    def __contains__(self, item):
        return item in self._word2idx

    def has_word(self, word: str):
        return word in self

    def __getitem__(self, item):
        return self._word2idx[item]

    def __str__(self):
        return str(self._word2idx)

    @property
    def word2idx(self):
        return self._word2idx

    @property
    def idx2word(self):
        return self._idx2word

    @property
    def word_count(self):
        return self._word_count

    @property
    def special_words(self):
        return {self.padding: 0, self.unknown: 1}

