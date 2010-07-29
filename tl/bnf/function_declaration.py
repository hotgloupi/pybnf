# -*- encoding: utf-8 -*-

from bnf import Group, NamedToken, TokenFunctor

from tl.bnf.type import Type
from tl.bnf.variable import Variable
from tl.bnf.statement import Statement
from tl import ast

class FunctionDeclarationParam(Group):
    def __init__(self):
        Group.__init__(self, [
            Group([
                NamedToken('type', Type),
                NamedToken('name', Variable),
                TokenFunctor(self.pushBoth)
            ])| Group([
                NamedToken('auto_name', Variable),
                TokenFunctor(self.pushName)
            ])
        ])

    def clone(self):
        return FunctionDeclarationParam()

    def pushBoth(self, context):
        self.type = self.getByName('type').getToken().id
        self.name = self.getByName('name').getToken().id
        self.has_both = True
        return True

    def pushName(self, context):
        self.type = 'auto'
        self.name = self.getByName('auto_name').getToken().id
        self.has_both = False
        return True

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
                    NamedToken('param', FunctionDeclarationParam),
                    TokenFunctor(self.pushParam),
                ],
                Group([
                    ",",
                    NamedToken('oparam', FunctionDeclarationParam),
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
        token = self.getByName('param').getToken()
        type = token.type
        name = token.name
        if not context.getCurrentScope().hasDeclaration(type):
            raise Exception("Unknown reference to type " + type)
        ref = ast.Reference(context.getCurrentScope().getDeclaration(type))
        self._params.append([ref, name])
        return True

    def pushOtherParam(self, context):
        token = self.getByName('param').getToken()
        type = token.type
        name = token.name
        if not context.getCurrentScope().hasDeclaration(type):
            raise Exception("Unknown reference to type " + type)
        ref = ast.Reference(context.getCurrentScope().getDeclaration(type))
        self._params.append([ref, name])
        return True

    def startScope(self, context):
        type = self.getByName('type').getToken().id
        name = self.getByName('name').getToken().id
        if context.getCurrentScope().hasDeclaration(name, recursive=False):
            raise Exception("The name "+name+" is already defined in current scope")
            return False
        if not context.getCurrentScope().hasDeclaration(type):
            raise Exception("Unknown return type: "+type)
            return False
        self._scope = context.beginScope(ast.SCOPE_TYPES['function'], name=name)
        ref_type = ast.Reference(context.getCurrentScope().getDeclaration(type))
        self._function = ast.Function(ref_type, name, self._params)
        self._scope.declarations.append(self._function)
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

