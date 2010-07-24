# -*- encoding: utf-8 -*-

from bnf import Group
from tl.bnf.variable_declaration import VariableDeclaration
from tl.bnf.affectation import Affectation

# Statement ::= VariableDeclaration | Affectation
class Statement(Group):
    __group__ = [VariableDeclaration | Affectation]

    def onMatch(self, context):
        print "match  statement"


