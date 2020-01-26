from pprint import pprint

from lighttext import NewWordDetector

detector = NewWordDetector()
detector.load_file('new_word/test_new_word3.txt')
pprint(detector.get_top_k(10))
