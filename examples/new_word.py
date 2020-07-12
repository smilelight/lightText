from lighttext import NewWordDetector

if __name__ == '__main__':
    detector = NewWordDetector()
    detector.load_file('new_word/test_new_word3.txt')
    print(detector.get_top_k(5))
