# -*- encoding: utf-8 -*-

from bnf import Group, Identifier, TokenFunctor, Literal, NamedToken, Alternative
from tl.bnf.variable import Variable
from tl.bnf.operators import BinaryInfixOperator
from tl.bnf.attribute_access_sub_expr import AttributeAccessSubExpr
from tl import ast

class SubExpr(Group):

    def __init__(self, operators=None, subexpr=None, group=None, min=1, max=1):
        if operators is not None and subexpr is not None:
            ops = list(BinaryInfixOperator(op) for op in operators)
            Group.__init__(self, [
                 subexpr,
                Group([Alternative(ops), subexpr], min=0, max=-1)
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
        ['^'],
        ['*', '/', '%'],
        ['+', '-'],
        ['<', '<=', '==', '>=', '>'],
    ]
    __affect_operators__ = [
        "=", "+=", "-=", "*=", "/="
    ]
    is_affectation = False

    def __init__(self, is_affectation=False):
        from tl.bnf.value import Value
        self.is_affectation = is_affectation
        expr = SubExpr(group=(Group(['(', Expression, ')']) | Value))
        expr = AttributeAccessSubExpr(expr)
        for i, op in enumerate(self.__class__.__operators__):
            expr = SubExpr(
                operators=self.__class__.__operators__[i],
                subexpr=expr
            )

        if is_affectation:
            from tl.bnf.variable_value import VariableValue
            ops = list(BinaryInfixOperator(op) for op in self.__affect_operators__)
            Group.__init__(self, [
#                TokenFunctor(self.prepareLeftOperand),
#                AttributeAccessSubExpr(Variable)
#                | TokenFunctor(self.cleanupLeftOperand),
#                TokenFunctor(self.pushLeftOperand),
                AttributeAccessSubExpr(VariableValue),
                Alternative(ops),
                expr
            ])
        else:
            Group.__init__(self, expr)

    def clone(self):
        return Expression(self.is_affectation)

    def __str__(self):
        return 'Expression'
