# -*- encoding: utf-8 -*-

from bnf import Group, NamedToken, Literal

from tl.bnf.type import Type
from tl.bnf.variable import Variable
from tl.bnf.endstatement import EndStatement
from tl.bnf.expression import Expression
from tl import ast

# Declaration ::= Type Variable
class Declaration(Group):
    __group__ = [
        NamedToken('type', Type),
        NamedToken('name', Variable),
        Group(
            Group(['(', Expression, ')']) |
            Group(['=', Expression]),
            min=0, max=1
        ),
        EndStatement
    ]

    def match(self, context):
        context.beginExpression()
        res = Group.match(self, context)
        context.endExpression()
        return res

    def onMatch(self, context):
        expr = None
        try:
            expr = context.getCurrentExpression()
        except:
            pass
        type = self.getByName('type').getToken().id
        name = self.getByName('name').getToken().id
        print "declaration", type, name
        printExpression(cleanExpression(expr))
        context.getCurrentScope().addDeclaration(ast.Variable(type, name, expr))


