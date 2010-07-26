# -*- encoding: utf-8 -*-

from bnf import Group
from tl.bnf.variable_declaration import VariableDeclaration
from tl.bnf.affectation import Affectation
from tl.bnf.function_call_statement import FunctionCallStatement
from tl.bnf.block_statement import BlockStatement

# Statement ::= BlockStatement | VariableDeclaration | Affectation | FunctionCallStatement
class Statement(Group):
    __recursive_group__ = True
    __group__ = [
        BlockStatement
        | VariableDeclaration
        | Affectation
        | FunctionCallStatement
    ]

