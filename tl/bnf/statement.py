# -*- encoding: utf-8 -*-

from bnf import Group
from tl.bnf.affectation import Affectation
from tl.bnf.function_call_statement import FunctionCallStatement
from tl.bnf.block_statement import BlockStatement
from tl.bnf.return_statement import ReturnStatement

# Statement ::= BlockStatement | Declaration | Affectation | FunctionCallStatement | ReturnStatement
class Statement(Group):
    __recursive_group__ = True
    def __init__(self):
        from tl.bnf.declaration import Declaration
        Group.__init__(self, [
            BlockStatement
            | ReturnStatement
            | Declaration
            | Affectation
            | FunctionCallStatement
        ])

    def clone():
        return Statement()

