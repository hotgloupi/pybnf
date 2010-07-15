# -*- encoding: utf-8 -*-

from bnf import Identifier

# Type ::= r'[a-zA-Z_][a-zA-Z0-9_]*'
class Type(Identifier):
    __regex__ = r'[a-zA-Z_][a-zA-Z0-9_]*'

    def onMatch(self, context):
        print "type", self.id


