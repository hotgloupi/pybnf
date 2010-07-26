# -*- encoding: utf-8 -*-

from bnf import Group
from tl.bnf.function_declaration import FunctionDeclaration
from tl.bnf.variable_declaration import VariableDeclaration
from tl.bnf.class_declaration import ClassDeclaration

# Declaration ::= FunctionDeclaration | VariableDeclaration | ClassDeclaration
class Declaration(Group):
    __group__ = [FunctionDeclaration | VariableDeclaration | ClassDeclaration]
