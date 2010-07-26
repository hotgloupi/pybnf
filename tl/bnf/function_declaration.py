# -*- encoding: utf-8 -*-

from bnf import Group, NamedToken, TokenFunctor

from tl.bnf.type import Type
from tl.bnf.variable import Variable
from tl.bnf.statement import Statement
from tl import ast

# FunctionDeclaration ::= Type Variable "(" [[Type Variable] [ "," Type Variable]*]? ")" "{" [Statement]* "}"
class FunctionDeclaration(Group):
    _params = None


    def __init__(self):
        Group.__init__(self, [
            NamedToken('type', Type),
            NamedToken('name', Variable),
            "(",
            Group([
                [
                    NamedToken('param_type', Type),
                    NamedToken('param_name', Variable),
                    TokenFunctor(self.pushParam),
                ],
                Group([
                    ",",
                    NamedToken('oparam_type', Type),
                    NamedToken('oparam_name', Variable),
                    TokenFunctor(self.pushOtherParam),
                ], min=0, max=-1)
            ], min=0),
            ")",
            "{",
            TokenFunctor(self.startScope),
            Group([Statement], min=0, max=-1),
            "}",
        ])


    def clone(self):
        return FunctionDeclaration()

    def pushParam(self, context):
        type = self.getByName('param_type').getToken().id
        name = self.getByName('param_name').getToken().id
        self._params.append([type, name])
        return True

    def pushOtherParam(self, context):
        type = self.getByName('oparam_type').getToken().id
        name = self.getByName('oparam_name').getToken().id
        self._params.append([type, name])
        return True

    def startScope(self, context):
        type = self.getByName('type').getToken().id
        name = self.getByName('name').getToken().id
        if context.getCurrentScope().hasDeclaration(name, recursive=False):
            raise Exception("Cannot redefine " + name)
        self._scope = context.beginScope(name)
        self._function = ast.Function(type, name, self._params)
        self._scope.declarations.append(self._function)
        print "declare", self._function, self._params
        for p in self._params:
            self._scope.declarations.append(ast.Variable(p[0], p[1], None))
        return True

    def match(self, context):
        self._params = []
        self._scope = None
        res = Group.match(self, context)
        if self._scope is not None:
            context.endScope()
        return res

    def onMatch(self, context):
        self._scope.parent.childs.append(self._scope)
        self._scope.parent.declarations.append(self._function)


    def __str__(self):
        return 'FunctionDeclaration'

