# -*- encoding: utf-8 -*-

from bnf import Group
from tl.bnf.endstatement import EndStatement
from tl.bnf.expression import Expression

# Affectation ::= Expression EndStatement
class Affectation(Group):
    __group__ = [
        Expression(is_affectation=True), EndStatement
    ]

    def match(self, context):
        expr = context.beginExpression()
        res = Group.match(self, context)
        context.endExpression()
        if res == True:
            context.getCurrentScope().statements.append(expr)
        return res

