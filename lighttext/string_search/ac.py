# -*- coding: utf-8 -*-
# @Time    : 2020/7/2 15:04
# @Author  : lightsmile
# @Software: PyCharm

from typing import Union, List, Dict, Set


class ACNode:
    def __init__(self, value: str = None, parent=None):
        self.child: Dict[str, ACNode] = {}
        self.value: str = value
        self.parent: ACNode = parent
        self.end_state = False
        self.end_note = None

    def maintain_chain(self, char_list: Union[str, List],
                       end_note: str = ''):
        if isinstance(char_list, str):
            char_list = list(char_list)

        if not len(char_list):
            self.end_state = True
            self.end_note = end_note
            return self
        if char_list[0] not in self.child:
            self.child[char_list[0]]: ACNode = ACNode(char_list[0], self)
        return self.child[char_list[0]].maintain_chain(char_list[1:], end_note)

    def chain_remove(self):
        if len(self.parent.child) > 1:
            del self.parent.child[self.value]
        else:
            return self.parent.chain_remove()

    def remove_this(self):
        if self.end_state:
            if len(self.child):  # over-lap: keep this node and set it to a non end node
                self.end_state = None
                self.end_note = None
                return
            else:
                self.chain_remove()
        else:
            raise ValueError('can not remove the node which is not a end node.')


class NodePointer:
    def __init__(self, node: ACNode):
        self.node = node


class AC:
    def __init__(self):
        self.end_notes: Dict[str, ACNode] = {}
        self.max_len = 0
        self.root = ACNode()

    def add_word(self, word: str):
        self.end_notes[word] = self.root.maintain_chain(word, word)
        self.max_len = max(self.max_len, len(word))

    def remove_word(self, word: str):
        if word not in self.end_notes:
            raise ValueError('{} not be added'.format(word))
        self.end_notes[word].remove_this()
        del self.end_notes[word]

    def go(self, pointer_set: Set[NodePointer], char: str):
        pointer_set.add(NodePointer(self.root))
        ret = []
        remove = set()
        for pointer in pointer_set:
            if char in pointer.node.child:
                pointer.node = pointer.node.child[char]
                if pointer.node.end_state:
                    ret.append(pointer.node.end_note)
            else:
                remove.add(pointer)
        for pointer in remove:
            pointer_set.remove(pointer)
        return ret
