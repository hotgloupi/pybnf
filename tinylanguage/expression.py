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


class Expression(Group):
    __group__ = None
    __recursive_group__ = True
    _parenthesis = 0

    def __init__(self, group=None, min=1, max=1):
        from tinylanguage.value import Value
        Group.__init__(self, [
            Group(['(', Expression, ')'])
            | Group([
                Group([UnaryPrefixOperator], min=0, max=-1),
                Value,
                Group([UnaryPostfixOperator], min=0, max=1),
            ]),
            Group([BinaryInfixOperator, Expression], min=0, max=-1),
        ], min=min, max=max)

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

