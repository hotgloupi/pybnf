# -*- encoding: utf-8 -*-

from bnf import Group, Identifier

class UnaryPrefixOperator(Group):
    __group__ = [
        '++', '--', '!', '+', '-',
    ]

class UnaryPostfixOperator(Group):
    __group__ = [
        '++', '__',
    ]

class BinaryInfixOperator(Group):
    __group__ = [
        '+', '-', '*', '/',
    ]

class Number(Identifier):
    __default_regex__ = r'[0-9]+'
    def onMatch(self, context):
        print "found number", self.id

class Value(Group):
    __group__ = [
        Number
    ]



class Expression(Group):
    __group__ = None
    __recursive_group__ = True

    def __init__(self):
        Group.__init__(self, [
            Group([UnaryPrefixOperator], min=0, max=-1),
            Value,
            Group([UnaryPostfixOperator], min=0, max=1),
            Group([BinaryInfixOperator, Expression], min=0, max=-1)
        ])

