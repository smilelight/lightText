import re
import json

from .sentence import Sentence
from .paragraph import Paragraph

para_spliter = re.compile('\n')


class Article:
    def __init__(self, title, content):
        assert type(title) == str
        assert type(content) == str
        self.raw_title = title.strip()
        self.raw_content = content.strip()
        self.title = Sentence(self.raw_title)
        self.content = [Paragraph(x) for x in para_spliter.split(self.raw_content) if x]

    def __str__(self):
        return json.dumps({
            'title': self.raw_title,
            'content': self.raw_content
        }, ensure_ascii=False, indent=1)
