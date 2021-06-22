# -*- coding: utf-8 -*-
from lighttext.component.vocabulary import Vocabulary
from lighttext.utils.tokenize import token_split

if __name__ == '__main__':
    corpora = [
        '我们都是中国人',
        '谁才是最可爱的人'
    ]

    vocab = Vocabulary()
    print(vocab.special_words)
    vocab.build_from_corpora([token_split(text) for text in corpora])
    print(vocab.word_count)
    print(vocab.idx2word)
    print(vocab.word2idx)

    vocab.add_word('曹操')
    vocab.update(['刘备', '司马懿', '关羽'])
    print(vocab.word_count)
    print(vocab.idx2word)
    print(vocab.word2idx)

    print(vocab.has_word('张飞'))
    print(vocab['刘备'])
    print('赵云' in vocab)
    print(vocab.to_idx('徐庶'))
    print(vocab.to_word(2))


