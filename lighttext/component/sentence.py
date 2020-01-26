import jieba

from .word import Word


class Sentence:
    def __init__(self, text):
        assert type(text) == str
        self.text = text

    def split(self):
        return list(jieba.cut(self.text))

    @property
    def words(self):
        return [Word(x) for x in self.split()]

    def __str__(self):
        return self.text
