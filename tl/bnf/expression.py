# -*- encoding: utf-8 -*-

from bnf import Group, Identifier, TokenFunctor, Literal, NamedToken, Alternative
from tl.bnf.variable import Variable
from tl import ast

class BinaryInfixOperator(Literal):

    def onMatch(self, context):
        context.getCurrentExpression().append(self._token)

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

class AttributeAccessSubExpr(Group):

    def __init__(self, subexpr):
        self._subexpr = subexpr
        from tl.bnf.function_call import FunctionParam
        from tl.bnf.variable_value import VariableValue
        Group.__init__(self, [
            subexpr,
            Group([
                BinaryInfixOperator("."),
                NamedToken('attribute', Variable),
                Group([
                    '(',
                    Group([
                        FunctionParam,
                        Group([
                            ',',
                            FunctionParam
                        ], min=0, max=-1)
                    ], min=0, max=1),
                    ')',
                    TokenFunctor(self.pushMethod),
                ])
                | TokenFunctor(self.pushMember)
            ], min=0, max=-1)
        ])

    def clone(self):
        return AttributeAccessSubExpr(self._subexpr)

    def pushMember(self, context):
        member = self.getByName('attribute').getToken().id
        context.endExpression()
        if self._is_first:
            context.getCurrentExpression().extend([self._expr[0], '.', member])
        else:
            context.getCurrentExpression().extend(['.', member])

        self._expr = context.beginExpression()
        self._is_first = False
        return True

    def pushMethod(self, context):
        method = self.getByName('attribute').getToken().id
        context.endExpression()
        if self._is_first:
            context.getCurrentExpression().extend([self._expr[0], '.', ast.FunctionCall(method, self._expr[2:])])
        else:
            context.getCurrentExpression().extend(['.', [ast.FunctionCall(method, self._expr[1:])]])

        self._expr = context.beginExpression()
        self._is_first = False
        return True

    def match(self, context):
        self._is_first = True
        main = context.beginExpression()
        self._expr = context.beginExpression()
        res = Group.match(self, context)
        context.endExpression()
        if res == True and len(self._expr) > 0:
            main.append(self._expr)
        context.endExpression()
        context.getCurrentExpression().append(main)
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
            ops = list(BinaryInfixOperator(op) for op in self.__affect_operators__)
            Group.__init__(self, [
                NamedToken('name', Variable), TokenFunctor(self.pushName),
                Alternative(ops),
                expr
            ])
        else:
            Group.__init__(self, expr)

    def pushName(self, context):
        name = self.getByName('name').getToken().id
        if not context.getCurrentScope().hasDeclaration(name):
            print "Unknown variable name " + name
            return False
        declaration = context.getCurrentScope().getDeclaration(name)
        context.getCurrentExpression().append(ast.VariableReference(declaration))
        return True

    def clone(self):
        return Expression(self.is_affectation)

    def __str__(self):
        return 'Expression'
