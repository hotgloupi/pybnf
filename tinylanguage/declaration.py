# -*- encoding: utf-8 -*-

from bnf import Group, NamedToken

from tinylanguage.type import Type
from tinylanguage.variable import Variable
from tinylanguage.endstatement import EndStatement


# Declaration ::= Type Variable
class Declaration(Group):
    __group__ = [
        NamedToken('type', Type),
        NamedToken('name', Variable),
        EndStatement
    ]


