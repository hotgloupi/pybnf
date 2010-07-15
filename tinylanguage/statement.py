# -*- encoding: utf-8 -*-

from bnf import Group
from tinylanguage.declaration import Declaration

# Statement ::= Declaration EndStatement
class Statement(Group):
    __group__ = [Declaration]

    def onMatch(self, context):
        print "match  statement"


