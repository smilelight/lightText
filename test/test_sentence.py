import unittest

from lighttext import Sentence


class TestSentence(unittest.TestCase):

    def test_str(self):
        text = '桥上的恋人入对出双，桥边红药叹夜太漫长。'
        sen = Sentence(text)
        self.assertEqual(str(sen), text)

    def test_split(self):
        import jieba

        text = '桥上的恋人入对出双，桥边红药叹夜太漫长。'
        sen = Sentence(text)
        self.assertEqual(sen.split(), list(jieba.cut(text)))

    def test_words(self):
        from lighttext import Word
        text = '桥上的恋人入对出双，桥边红药叹夜太漫长。'
        sen = Sentence(text)
        self.assertTrue(type(sen.words[0]) == Word)
