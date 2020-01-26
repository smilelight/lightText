import unittest

from lighttext import Paragraph


class TestParagraph(unittest.TestCase):

    def test_str(self):
        text = '桥上的恋人入对出双，桥边红药叹夜太漫长。月也摇晃，人也彷徨，乌蓬里传来了一曲离殇。'
        para = Paragraph(text)
        self.assertEqual(str(para), text)
        for x in para.sentences:
            print(type(x))
            print(x)
        print(para.split())
