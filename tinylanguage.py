#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from bnf import Literal, Group, Identifier, NamedToken, EOF

# Variable ::= r'[a-zA-Z_][a-zA-Z0-9_]*'
class Variable(Identifier):
    __regex__ = r'[a-zA-Z_][a-zA-Z0-9_]*'

    def onMatch(self, context):
        print "var", self.id

# Type ::= r'[a-zA-Z_][a-zA-Z0-9_]*'
class Type(Identifier):
    __regex__ = r'[a-zA-Z_][a-zA-Z0-9_]*'

    def onMatch(self, context):
        print "type", self.id


# Declaration ::= Type Variable
class Declaration(Group):
    __group__ = [
        Type,
        NamedToken('name', Variable)
    ]

# EndStatement ::= ";"
EndStatement = Literal(';')

# Statement ::= Declaration EndStatement
class Statement(Group):
    __group__ = [Declaration, EndStatement]

    def onMatch(self, context):
        print "match  statement"

# TinyLanguage ::= [Statement]*
TinyLanguage = Group([Group([Statement], min=0, max=-1), EOF])

if __name__ == '__main__':
    from bnf import Context
    context = Context('test.tl')

    TinyLanguage.parse(context)



