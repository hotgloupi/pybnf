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
    __operators__ = [
        ['*', '/'],
        ['+', '-'],
    ]

    def __init__(self, group=None, min=1, max=1):
        from tinylanguage.value import Value
        from bnf import Alternative
        expr = []
        expr.append(Group(['(', Expression, ')']) | Value)
        for i, op in enumerate(self.__class__.__operators__):
            expr.append(Group([expr[i], Group([
                Alternative(self.__class__.__operators__[i]), expr[i]
            ], min=0, max=-1)]))
        print '#'*80
        print expr[-1]
        print '#'*80

        Group.__init__(self, expr[-1])

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

