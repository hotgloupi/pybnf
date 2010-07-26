# -*- encoding: utf-8 -*-

from bnf import Group, Identifier, NamedToken, TokenFunctor
from tl.bnf.expression import Expression
from tl.bnf.variable import Variable
from tl import ast

class FunctionParam(Expression):
    def match(self, context):
        context.beginExpression()
        res = Group.match(self, context)
        expr = context.getCurrentExpression()
        context.endExpression()
        if res == True:
            context.getCurrentExpression().append(expr.clean())
        return res

class FunctionCall(Group):

    def __init__(self, group=None, min=1, max=1):
        Group.__init__(self, [
            NamedToken('function_name', Variable),
            TokenFunctor(self.pushName),
            '(',
            Group([
                FunctionParam,
                Group([
                    ',',
                    FunctionParam
                ], min=0, max=-1)
            ], min=0, max=1),
            ')'
        ], min=min, max=max)

    def pushName(self, context):
        name = self.getByName('function_name').getToken().id
        if not context.getCurrentScope().hasDeclaration(name):
            raise Exception("Unknown function")
        context.getCurrentExpression().append(name)
        return True

    def match(self, context):
        context.beginExpression()
        res = Group.match(self, context)
        expr = context.getCurrentExpression()
        context.endExpression()
        if res == True:
            context.getCurrentExpression().append(
                ast.FunctionCall(expr[0], expr[1:])
            )
        return res

