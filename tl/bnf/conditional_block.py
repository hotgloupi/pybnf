# -*- encoding: utf-8 -*-

from bnf import Group
from tl.bnf.block import Block

# ConditionalBlock ::= "if" "(" Expression ")" "{" [Statement]* "}"
#                      [ "else" "if" "(" Expression ")" "{" [Statement]* "}" ]*
#                      [ "else" "{" [Statement]* "}" ]?
class ConditionalBlock(Group):
    __recursive_group__ = True

    def __init__(self):
        Group.__init__(self, [
            Block("if", True),
            Block(["else", "if"], True, min=0, max=-1),
            Block("else", False, min=0, max=1)
        ])

    def clone(self):
        return ConditionalBlock()


