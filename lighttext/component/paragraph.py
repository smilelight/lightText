import re

from .sentence import Sentence

sen_spliter = re.compile('[！~。？；\s.?!;]')


class Paragraph:
    def __init__(self, text):
        assert type(text) == str
        self.text = text

    def split(self):
        return [x for x in sen_spliter.split(self.text) if x]

    @property
    def sentences(self):
        return [Sentence(x) for x in self.split()]

    def __str__(self):
        return self.text
