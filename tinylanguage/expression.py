# -*- encoding: utf-8 -*-

from bnf import Group, Identifier, TokenFunctor, Literal

class UnaryPrefixOperator(Group):
    __group__ = [
        Literal('++') |
        Literal('--') |
        Literal('!') |
        Literal('+') |
        Literal('-')
    ]

class UnaryPostfixOperator(Group):
    __group__ = [
        Literal('++') |
        Literal('--')
    ]

class BinaryInfixOperator(Group):
    __group__ = [
        Literal('+') |
        Literal('-') |
        Literal('*') |
        Literal('/') |
        Literal('^') |
        Literal('&&') |
        Literal('&') |
        Literal('||') |
        Literal('|')
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
    _parenthesis = 0

    def __init__(self):
        Group.__init__(self, [
            Group(['(', TokenFunctor(self.onLeftParenthesis)], min=0, max=-1),
            Group([UnaryPrefixOperator], min=0, max=-1),
            Value,
            Group([UnaryPostfixOperator], min=0, max=1),
            Group([BinaryInfixOperator, Expression], min=0, max=-1),
            Group([
                TokenFunctor(self.canHaveRightParenthesis),
                ')',
                TokenFunctor(self.onRightParenthesis)
            ], min=0, max=-1)
        ])

    def onLeftParenthesis(self, context):
        self._parenthesis += 1
        return True

    def canHaveRightParenthesis(self, context):
        return self._parenthesis > 0

    def onRightParenthesis(self, context):
        self._parenthesis -= 1
        return True

    def onMatch(self, context):
        if self._parenthesis != 0:
            raise Exception("Wrong number of parenthesis")
        print "match !!!"
