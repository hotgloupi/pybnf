#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from bnf import Literal, Group, Identifier
from bnf import Context

# Separator ::= ";"
class Separator(Literal):
    __token__ = ';'
    __whitespaces__ = [' ', '\t']

# EOL ::= ['\r' | '\n']+
class EOL(Identifier):
    __default_regex__ = r'[\r\n]+'
    __whitespaces__ = []

# Data ::= "[^;\r\n"]*"
class Data(Identifier):
    __default_regex__ = r'[^;\r\n"]*'
    __whitespaces__ = []

    def onMatch(self, context):
        context.rows[-1].append(self.id)

# Row ::= Data [Separator Data]* EOL
class Row(Group):
    __group__ = [Data, Group([Separator, Data], min=0, max=-1), EOL]

    def onMatch(self, context):
        context.rows.append([])

# CSV ::= [Row]+
class CSV(Group):
    __group__ = Group([Row], max=-1)

context = Context('test.csv')
context.rows = [[]]
csv.parse(context)

print "Found rows:"
for i, row in enumerate(c.rows):
    print str(i) + ": " + ''.join(str(col) +'|' for col in row)
