# -*- encoding: utf-8 -*-

from bnf import Literal

# EndStatement ::= ";"
class EndStatement(Literal):
    __token__ = ';'

