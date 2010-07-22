# -*- encoding: utf-8 -*-

from bnf import Group, NamedToken, Literal

from tinylanguage.type import Type
from tinylanguage.variable import Variable
from tinylanguage.endstatement import EndStatement
from tinylanguage.expression import Expression

def cleanExpression(expr):
    if isinstance(expr, list):
        if len(expr) == 1:
            return cleanExpression(expr[0])
        else:
            return list(cleanExpression(i) for i in expr)
    return expr

def printExpression(expr):
    if isinstance(expr, list):
        print '(',
        for i in expr:
            printExpression(i)
        print ')',
    else:
        print expr,

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
        context.getCurrentScope().addDeclaration(type, name)
        print "declaration", type, name
        printExpression(cleanExpression(expr))


