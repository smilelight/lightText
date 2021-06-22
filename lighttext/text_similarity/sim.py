# -*- coding: utf-8 -*-
from typing import List, Callable, Union
from enum import Enum
import pickle

import jieba.posseg as pseg
from gensim import corpora, models, similarities

from ..utils.sen_split import split_sentence

NUM_TOPICS = 300
NUM_FEATURES = 300
MODEL_PATH = 'saves/model'
DIC_PATH = 'saves/dic'


class ModelType(Enum):
    TFIDF = 1
    LDA = 2
    LSI = 3


type_dict = {
    "tfidf": ModelType.TFIDF,
    "lda": ModelType.LDA,
    "lsi": ModelType.LSI
}


def tokenize(text: str) -> List[str]:
    # {标点符号、连词、助词、副词、介词、时语素、‘的’、数词、方位词、代词}
    # {'x', 'c', 'u', 'd', 'p', 't', 'uj', 'm', 'f', 'r'}
    stop_flags = {'x', 'c', 'u', 'd', 'p', 't', 'uj', 'm', 'f', 'r'}
    stop_words = {'nbsp', '\u3000', '\xa0'}
    words = pseg.cut(text)
    return [word for word, flag in words if flag not in stop_flags and word not in stop_words]


class SimModel:
    def __init__(self, model_type: str = 'lda', token_fn: Callable = tokenize, split_fn: Callable = split_sentence):
        if model_type not in type_dict:
            raise Exception('undefined model_type: {}, must be one of {}'.format(model_type, list(type_dict.keys())))
        self._model_type = model_type
        self._token_fn = token_fn
        self._split_fn = split_fn
        self._dic = corpora.Dictionary()
        self._models = {
            'tfidf': None,
            'lsi': None,
            'lda': None
        }
        self._mtx: similarities.MatrixSimilarity = None
        self._documents: List[str] = []

    @property
    def dic(self):
        return self._dic

    @property
    def token_fn(self):
        return self._token_fn

    @property
    def split_fn(self):
        return self._split_fn

    def add_vocab_from_documents(self, documents: List[str]):
        """
        构造dic词典
        Args:
            documents: 原始文本列表

        Returns:

        """
        texts = [self._token_fn(doc) for doc in documents]
        self._dic.add_documents(texts)

    def tokenize_texts(self, texts: List[str]):
        """
        对文本列表进行分词处理
        Args:
            texts: 文本列表

        Returns:

        """
        return [self._token_fn(doc) for doc in texts]

    def build_vocab(self, documents: List[str]):
        """
        从文本中构造dic词表
        Args:
            documents: 构造dic词典

        Returns:

        """
        self.add_vocab_from_documents(documents)

    def get_corpus(self, texts: List[str]):
        """
        得到文本列表对应的倒排索引表
        Args:
            texts: 原始文本列表

        Returns:

        """
        texts = self.tokenize_texts(texts)
        return [self._dic.doc2bow(text) for text in texts]

    def _init_tfidf_model(self, corpus):
        self._models["tfidf"] = models.TfidfModel(corpus, id2word=self._dic)

    def _init_lsi_model(self, corpus):
        self._models["lsi"] = models.LsiModel(corpus, id2word=self._dic, num_topics=len(self._dic.token2id))

    def _init_lda_model(self, corpus):
        self._models['lda'] = models.LdaModel(corpus, id2word=self._dic, num_topics=len(self._dic.token2id))

    def _init_model(self, corpus):
        if self._model_type == 'tfidf':
            self._init_tfidf_model(corpus)
        elif self._model_type == 'lsi':
            self._init_lsi_model(corpus)
        else:
            self._init_lda_model(corpus)

    def build_model(self, corpus):
        """
        创建模型
        Args:
            corpus:

        Returns:

        """
        self._init_model(corpus)

    def _check_model(self):
        model = self._models[self._model_type]
        if not model:
            raise Exception('model must be initialized')

    def build_from_documents(self, documents: List[str]):
        """
        从文本列表中构造词表并构造模型
        Args:
            documents: 文本列表

        Returns:

        """
        self.build_vocab(documents)
        self.build_model(self.get_corpus(documents))

    def build_from_txt(self, path: str):
        """
        从txt文本中构造词表并构造模型
        Args:
            path: 文本路径

        Returns:

        """
        documents = []
        with open(path, encoding='utf8') as f:
            for line in f:
                documents.extend(self._split_fn(line))
        self.build_from_documents(documents)

    def process(self, text: str, documents: List[str]):
        vec = self._dic.doc2bow(self._token_fn(text))
        model = self._models[self._model_type]
        if not model:
            raise Exception('model must be initialized')
        corpus = self.get_corpus(documents)
        mtx = similarities.MatrixSimilarity(model[corpus], num_features=len(self._dic.token2id))
        scores = mtx[model[vec]]
        return sorted(zip(scores, documents), key=lambda x: x[0], reverse=True)

    def set_documents(self, documents: List[str]):
        """
        设置待检索的文档
        Args:
            documents:

        Returns:

        """
        self._documents = documents
        corpus = self.get_corpus(self._documents)
        model = self._models[self._model_type]
        if not model:
            raise Exception('model must be initialized')
        self._mtx = similarities.MatrixSimilarity(model[corpus], num_features=len(self._dic.token2id))

    def search(self, text: str):
        """
        根据text检索最相关的文档片段
        Args:
            text: 待检索的文本

        Returns: 文档结果及分数

        """
        vec = self._dic.doc2bow(self._token_fn(text))
        model = self._models[self._model_type]
        if not model:
            raise Exception('model must be initialized')
        scores = self._mtx[model[vec]]
        return sorted(zip(scores, self._documents), key=lambda x: x[0], reverse=True)

    def save(self, path: str):
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, path: str):
        with open(path, 'rb') as f:
            model = pickle.load(f)
            return model
