# -*- encoding: utf-8 -*-

from bnf import Group, Identifier, NamedToken, TokenFunctor
from tl.bnf.expression import Expression

class Number(Identifier):
    __default_regex__ = r'[0-9]+'

    def onMatch(self, context):
        context.getCurrentExpression().append(self.id)



class FunctionParam(Expression):
    def match(self, context):
        context.beginExpression()
        res = Group.match(self, context)
        expr = context.getCurrentExpression()
        context.endExpression()
        if res == True:
            context.getCurrentExpression().append(expr)
        return res

class FunctionCallDef(object):
    def __str__(self):
        p = list(str(i) for i in self.params)
        return self.name + '(' + ','.join(p) + ')'

    def __init__(self, name, params):
        self.name = name
        self.params = params


class FunctionCall(Group):

    def __init__(self, group=None, min=1, max=1):
        Group.__init__(self, [
            NamedToken('function_name', Identifier()),
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
        context.getCurrentExpression().append(name)

    def match(self, context):
        context.beginExpression()
        res = Group.match(self, context)
        expr = context.getCurrentExpression()
        context.endExpression()
        if res == True:
            context.getCurrentExpression().append(
                FunctionCallDef(expr[0], expr[1:])
            )
        return res


    def onMatch(self, context):
        pass

class Value(Group):
    __group__ = [
        Number | FunctionCall
    ]

    def __str__(self):
        return 'class"Value"'

