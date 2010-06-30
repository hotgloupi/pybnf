#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from bnf import Literal, Group, Identifier

# Separator ::= ";"
class Separator(Literal):
    __token__ = ';'
    __whitespaces__ = [' ', '\t']

    def onMatch(self, context): pass

# EOL ::= ['\r' | '\n']+
class EOL(Identifier):
    __default_regex__ = r'[\r\n]+'
    __whitespaces__ = []

    def onMatch(self, context): pass

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

csv = CSV()
print "CSV:", csv

from bnf import Context

c = Context('test.csv')
c.rows = [[]]

csv.parse(c)
print "Found rows:"
for i, row in enumerate(c.rows):
    print str(i) + ": " + ''.join(("%-10s" % col) for col in row)
