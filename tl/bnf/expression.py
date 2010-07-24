# -*- encoding: utf-8 -*-

from bnf import Group, Identifier, TokenFunctor, Literal, NamedToken, Alternative
from tl.bnf.variable import Variable

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


class BinaryInfixOperator(Literal):

    def onMatch(self, context):
        context.getCurrentExpression().append(self._token)

class SubExpr(Group):

    def __init__(self, operators=None, subexpr=None, group=None, min=1, max=1):
        if operators is not None and subexpr is not None:
            ops = list(BinaryInfixOperator(op) for op in operators)
            Group.__init__(self, [
                NamedToken('op1', subexpr),
                Group([Alternative(ops), NamedToken('op2', subexpr)], min=0, max=-1)
            ], min=min, max=max)
        elif group is not None:
            Group.__init__(self, group, min, max)


    def match(self, context):
        context.beginExpression()
        res = Group.match(self, context)
        expr = context.getCurrentExpression()
        context.endExpression()
        if res == True:
            context.getCurrentExpression().append(expr)
        return res

class Expression(Group):
    __group__ = None
    __recursive_group__ = True
    __operators__ = [
        ['*', '/'],
        ['+', '-'],
    ]
    __affect_operators__ = [
        "=", "+=", "-=", "*=", "/="
    ]
    is_affectation = False

    def __init__(self, is_affectation=False):
        from tl.bnf.value import Value
        expr = []
        expr.append(
            SubExpr(group=(Group(['(', Expression, ')']) | Value))
        )
        for i, op in enumerate(self.__class__.__operators__):
            expr.append(SubExpr(
                operators=self.__class__.__operators__[i],
                subexpr=expr[i]
            ))
        #print '#'*80
        #print expr[-1]
        #print '#'*80
        self.is_affectation = is_affectation
        if is_affectation:
            ops = list(BinaryInfixOperator(op) for op in self.__affect_operators__)
            Group.__init__(self, [
                NamedToken('name', Variable), TokenFunctor(self.pushName),
                Alternative(ops),
                expr[-1]
            ])
        else:
            Group.__init__(self, expr[-1])

    def pushName(self, context):
        name = self.getByName('name').getToken().id
        if not context.getCurrentScope().hasDeclaration(name):
            raise Exception("Unknown variable name " + name)
        context.getCurrentExpression().append(context.getCurrentScope().getDeclaration(name))
        return True

    def clone(self):
        return Expression(self.is_affectation)

    def __str__(self):
        return 'Expression'
