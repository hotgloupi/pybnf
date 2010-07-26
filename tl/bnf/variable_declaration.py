# -*- encoding: utf-8 -*-

from bnf import Group, NamedToken

from tl.bnf.type import Type
from tl.bnf.variable import Variable
from tl.bnf.endstatement import EndStatement
from tl.bnf.expression import Expression
from tl import ast

# VariableDeclaration ::= Type Variable [ [ "(" Expression ")" ] | [ "=" Expression ] ]? EndStatement
class VariableDeclaration(Group):
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
            expr = context.getCurrentExpression().clean()
        except:
            pass
        type = self.getByName('type').getToken().id
        name = self.getByName('name').getToken().id
        if context.getCurrentScope().hasDeclaration(name, recursive=False):
            raise Exception("Cannot redefine " + name)
        context.getCurrentScope().declarations.append(ast.Variable(type, name, expr))

    def __str__(self):
        return 'VariableDeclaration'

