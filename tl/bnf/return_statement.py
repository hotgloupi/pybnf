# -*- encoding: utf-8 -*-
from bnf import Group
from tl.bnf.expression import Expression

class ReturnStatement(Group):
    __group__ = [
        "return", Group([Expression], min=0), ";"
    ]

    def match(self, context):
        expr = context.beginExpression()
        res = Group.match(self, context)
        context.endExpression()
        if res == True:
            context.getCurrentScope().statements.append(["return", expr.clean()])
        return res


