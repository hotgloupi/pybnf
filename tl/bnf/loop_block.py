# -*- encoding: utf-8 -*-

from bnf import Group
from tl.bnf.block import Block

class LoopBlock(Group):
    __recursive_group__ = True

    def __init__(self):
        Group.__init__(self, [
            Block("while", True)
        ])

    def clone(self):
        return LoopBlock()
