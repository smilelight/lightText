# -*- coding: utf-8 -*-
from lighttext.text_similarity.sim import SimModel

if __name__ == '__main__':
    documents = [
        '乔布斯极力推崇自己家的苹果手机',
        '这苹果又大又圆又甜，还便宜',
        '这年头，谁还用安卓手机，要么是苹果，要么是鸿蒙'
    ]

    text = '苹果手机还是小米手机呢？'

    corpus = [
        '许多超市里都有卖苹果的',
        '比尔盖茨打算收购乔布斯的苹果手机'
    ]

    path = "sim.bin"
    doc_path = "doc.txt"

    model = SimModel(model_type='lsi')

    # 从documents中初始化模型
    # model.build_from_documents(documents)

    model.build_from_txt(doc_path)

    model.save(path)
    model: SimModel = SimModel.load(path)
    model.set_documents(corpus)
    print(model.dic.id2token)
    print(model.search(text))
    print(model.process(text, corpus))
