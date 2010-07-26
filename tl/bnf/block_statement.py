# -*- encoding: utf-8 -*-

from bnf import Group
from tl.bnf.conditional_block import ConditionalBlock
from tl.bnf.loop_block import LoopBlock

# BlockStatement ::= ConditionalBlock | LoopBlock | TryCatchBlock
class BlockStatement(Group):
    __group__ = [
        ConditionalBlock | LoopBlock
    ]
