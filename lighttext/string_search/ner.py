# -*- coding: utf-8 -*-
import os
import csv
import pickle
from collections import defaultdict

from tqdm import tqdm
from lightutils import logger, get_file_name, check_file

from .keyword import KeywordProcessor


def default_type():
    return None


class NER:
    def __init__(self):
        self._kp = KeywordProcessor()
        self._type_dict = defaultdict(default_type)

    def build_from_txt(self, file_path: str):
        check_file(file_path, 'txt')
        file_name = get_file_name(file_path)
        file_data = open(file_path, encoding='utf8').read().split('\n')
        logger.info("正在从{}中导入词表，共计{}条数据".format(file_path, len(file_data)))
        self._kp.add_keywords_from_list(file_data)
        for word in tqdm(file_data):
            self._type_dict[word] = file_name

    def build_from_csv(self, file_path: str, column: int):
        check_file(file_path, 'csv')
        file_name = get_file_name(file_path)
        file_data = []
        with open(file_path, encoding='utf8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
            assert column < len(headers)
            logger.info("headers:{}".format(','.join(headers)))
            for line in csv_reader:
                file_data.append(line[column])
        logger.info("正在从{}中导入词表，共计{}条数据".format(file_path, len(file_data)))
        self._kp.add_keywords_from_list(file_data)
        for word in tqdm(file_data):
            self._type_dict[word] = file_name

    def build_from_dir(self, file_dir):
        for file_path in os.listdir(file_dir):
            file_full_path = os.path.join(file_dir, file_path)
            file_name = get_file_name(file_full_path)
            if file_path.endswith('csv'):
                file_data = []
                with open(file_full_path, encoding='utf8') as file:
                    csv_reader = csv.reader(file)
                    headers = next(csv_reader)
                    logger.info("headers:{}".format(','.join(headers)))
                    for line in csv_reader:
                        file_data.append(line[1])
            else:  # default txt format
                file_data = open(file_full_path, encoding='utf8').read().split('\n')

            logger.info("正在从{}中导入词表，共计{}条数据".format(file_path, len(file_data)))
            self._kp.add_keywords_from_list(file_data)
            for word in tqdm(file_data):
                self._type_dict[word] = file_name

    def save(self, save_path: str = 'ner.pt'):
        logger.info("将模型保存至{}中".format(save_path))
        with open(save_path, 'wb') as file:
            pickle.dump(self._kp, file)
            pickle.dump(self._type_dict, file)
        logger.info("成功将模型保存至{}中".format(save_path))

    def load(self, save_path: str = 'ner.pt'):
        logger.info("从{}中加载模型中".format(save_path))
        with open(save_path, 'rb') as file:
            self._kp = pickle.load(file)
            self._type_dict = pickle.load(file)
        logger.info("成功从{}中加载模型".format(save_path))

    def extract(self, sentence: str):
        keywords = self._kp.extract_keywords(sentence, span_info=True)
        # return keywords
        return [(x[0], self._type_dict[x[0]], x[1], x[2]) for x in keywords]
