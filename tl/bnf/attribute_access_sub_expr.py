# -*- encoding: utf-8 -*-

from bnf import Group, NamedToken, TokenFunctor
from tl import ast

class AttributeAccessSubExpr(Group):

    def __init__(self, subexpr):
        self._subexpr = subexpr
        from tl.bnf.function_call import FunctionParam
#        from tl.bnf.variable_value import VariableValue
        from tl.bnf.operators import BinaryInfixOperator
        from tl.bnf.variable import Variable
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
            context.getCurrentExpression().extend([
                self._expr[0], '.', ast.FunctionCall(method, self._expr[2:])
            ])
        else:
            context.getCurrentExpression().extend([
                '.', [ast.FunctionCall(method, self._expr[1:])]
            ])

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
