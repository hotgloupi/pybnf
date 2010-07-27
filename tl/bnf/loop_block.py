# -*- encoding: utf-8 -*-

from bnf import Group
from tl.bnf.block import Block

class LoopBlock(Group):
    __recursive_group__ = True

    def __init__(self):
        Group.__init__(self, [
            Block("while", True)
        ])

    def match(self, context):
        context.feedFromFile()
        print "Trying", context.getBuf(), self
        res = Group.match(self, context)
        print " ==>", res
        return res

    def onMatch(self, context):
        print "yipii"

    def clone(self):
        return LoopBlock()
