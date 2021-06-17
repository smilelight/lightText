# -*- coding: utf-8 -*-
from typing import List
import jieba.posseg as pseg

from gensim import corpora, models, similarities

NUM_TOPICS = 350
MODEL_PATH = 'saves/model'
DIC_PATH = 'saves/dic'

def tokenize(text: str) -> List[str]:
    # {标点符号、连词、助词、副词、介词、时语素、‘的’、数词、方位词、代词}
    # {'x', 'c', 'u', 'd', 'p', 't', 'uj', 'm', 'f', 'r'}
    stop_flags = {'x', 'c', 'u', 'd', 'p', 't', 'uj', 'm', 'f', 'r'}
    stop_words = {'nbsp', '\u3000', '\xa0'}
    words = pseg.cut(text)
    return [word for word, flag in words if flag not in stop_flags and word not in stop_words]


def get_dic_corpus(contents: List[str]):
    texts = [tokenize(content) for content in contents]

    dic = corpora.Dictionary(texts)
    corpus = [dic.doc2bow(text) for text in texts]
    return dic, corpus


def get_lsi_model(corpus, dic, num_topics: int = NUM_TOPICS):
    lsi = models.LsiModel(corpus, id2word=dic, num_topics=len(dic.token2id))
    index = similarities.MatrixSimilarity(lsi[corpus])
    return lsi, index


def get_tfidf_model(corpus, dic):
    model = models.TfidfModel(corpus, id2word=dic)
    print(dic.token2id, type(dic.token2id))
    index = similarities.MatrixSimilarity(model[corpus], num_features=len(dic.token2id))
    return model, index


def get_lda_model(corpus, dic, num_topics: int = NUM_TOPICS):
    model = models.LdaModel(corpus, id2word=dic, num_topics=len(dic.token2id))
    index = similarities.MatrixSimilarity(model[corpus], num_features=len(dic.token2id))
    return model, index


def get_test_mtx(texts: List[str], dic, model):
    corpus = [dic.doc2bow(tokenize(text)) for text in texts]
    idx = similarities.MatrixSimilarity(model[corpus], num_features=len(dic.token2id))
    return idx



if __name__ == '__main__':
    text = "测试曹操去东北，然后hello world！"
    print(tokenize(text))

    contents = [
        '乔布斯极力推崇自己家的苹果手机',
        '这苹果又大又圆又甜，还便宜',
        '这年头，谁还用安卓手机，要么是苹果，要么是鸿蒙'
    ]

    others = [
        '许多超市里都有卖苹果的',
        '比尔盖茨打算收购乔布斯的苹果手机'
    ]

    dic, corpus = get_dic_corpus(contents)

    text = '苹果手机还是小米手机呢？'
    text_vec = dic.doc2bow(tokenize(text))

    print(text_vec)

    # 获取tfidf模型
    # model, idx = get_tfidf_model(corpus, dic)

    # 获取lsi模型
    # model, idx = get_lsi_model(corpus, dic)
    # print(model.print_topics())

    # 获取lda模型
    model, idx = get_lda_model(corpus, dic)
    print(model.print_topics())

    model.save(MODEL_PATH)
    dic.save(DIC_PATH)
    model = models.LdaModel.load(MODEL_PATH)
    dic = corpora.Dictionary.load(DIC_PATH)

    test_mtx = get_test_mtx(others, dic, model)

    # sims = idx[model[text_vec]]
    sims = test_mtx[model[text_vec]]

    print(list(enumerate(sims)))