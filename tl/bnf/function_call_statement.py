# -*- encoding: utf-8 -*-

from bnf import Group
from tl.bnf.function_call import FunctionCall
from tl.bnf.endstatement import EndStatement

class FunctionCallStatement(Group):

    __group__ = [FunctionCall, EndStatement]

    def match(self, context):
        expr = context.beginExpression()
        res = Group.match(self, context)
        context.endExpression()
        if res == True:
            context.getCurrentScope().statements.append(expr[0])
        return res
