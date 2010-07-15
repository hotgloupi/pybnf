# -*- encoding: utf-8 -*-

from bnf import Identifier

# Variable ::= r'[a-zA-Z_][a-zA-Z0-9_]*'
class Variable(Identifier):
    __regex__ = r'[a-zA-Z_][a-zA-Z0-9_]*'

    def onMatch(self, context):
        print "var", self.id


