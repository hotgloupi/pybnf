# -*- encoding: utf-8 -*-

from bnf import Group, NamedToken, TokenFunctor

from tl.bnf.type import Type
from tl.bnf.variable import Variable
from tl.bnf.endstatement import EndStatement
from tl.bnf.expression import Expression
from tl import ast

# VariableDeclaration ::= Type Variable [ [ "(" Expression ")" ] | [ "=" Expression ] ]? EndStatement
class VariableDeclaration(Group):

    def __init__(self):
        Group.__init__(self, [
            Group([
                NamedToken('type', Type),
                NamedToken('name', Variable),
                TokenFunctor(self.pushBoth)
            ])
            | Group([
                NamedToken('auto_name', Variable),
                TokenFunctor(self.pushName)
            ]),
            Group(
                Group([
                    TokenFunctor(self.hasBoth),
                    Group(['(', Expression, ')'])
                ]) | Group(['=', Expression]),
                min=0, max=1
            ),
            EndStatement
        ])

    def clone(self):
        return VariableDeclaration()

    def pushBoth(self, context):
        self._type = self.getByName('type').getToken().id
        self._name = self.getByName('name').getToken().id
        self._has_both = True
        return True

    def pushName(self, context):
        self._type = 'auto'
        self._name = self.getByName('auto_name').getToken().id
        self._has_both = False
        return True

    def hasBoth(self, context):
        return self._has_both

    def match(self, context):
        context.beginExpression()
        res = Group.match(self, context)
        context.endExpression()
        return res

    def onMatch(self, context):
        expr = None
        try:
            expr = context.getCurrentExpression().clean()
            if expr is not None and len(expr) == 0:
                expr = None
        except:
            pass
        scope = context.getCurrentScope()
        if scope.hasDeclaration(self._name, recursive=False):
            raise Exception("Cannot redefine " + self._name)
        if not scope.hasDeclaration(self._type):
            raise Exception("Type "+ self._type + " is unknown")

        type = ast.Reference(scope.getDeclaration(self._type))
        var = ast.Variable(type, self._name, None)
        scope.declarations.append(var)
        scope.statements.append(
            ast.Expression(['#create_', ast.Reference(var)])
        )
        scope.statements.append(ast.Expression([ast.Reference(var),'=', expr]))

    def __str__(self):
        return 'VariableDeclaration'

