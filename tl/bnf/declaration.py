# -*- encoding: utf-8 -*-

from bnf import Group
from tl.bnf.function_declaration import FunctionDeclaration
from tl.bnf.variable_declaration import VariableDeclaration

# Declaration ::= FunctionDeclaration | VariableDeclaration
class Declaration(Group):
    __group__ = [FunctionDeclaration | VariableDeclaration]
