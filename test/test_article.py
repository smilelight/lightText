import unittest

from lighttext import Article


class TestArticle(unittest.TestCase):

    def test_str(self):
        title = '月亮和六便士'
        content = """
            《月亮和六便士》是英国小说家威廉· 萨默赛特·毛姆的创作的长篇小说，成书于1919年。
作品以法国印象派画家保罗·高更的生平为素材，描述了一个原本平凡的伦敦证券经纪人思特里克兰德，突然着了艺术的魔，抛妻弃子，绝弃了旁人看来优裕美满的生活，奔赴南太平洋的塔希提岛，用圆笔谱写出自己光辉灿烂的生命，把生命的价值全部注入绚烂的画布的故事。
贫穷的纠缠，病魔的折磨他毫不在意，只是后悔从来没有光顾过他的意识。作品表现了天才、个性与物质文明以及现代婚姻、家庭生活之间的矛盾，有着广阔的生命视角，用散发着消毒水味道的手术刀对皮囊包裹下的人性进行了犀利地解剖，混合着看客讪笑的幽默和残忍的目光。
"""
        article = Article(title=title, content=content)
        print(article)
