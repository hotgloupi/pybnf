# -*- encoding: utf-8 -*-

from bnf import Group, TokenFunctor, NamedToken
from tl import ast

# ClassDeclaration ::= "class" Variable [":" Variable ["," Variable]*]? "{" [Declaration]* "}"
class ClassDeclaration(Group):
    __recursive_group__ = True

    _class_name = None
    _bases = None

    def __init__(self):
        from tl.bnf.declaration import Declaration
        from tl.bnf.variable import Variable
        Group.__init__(self, [
            "class", NamedToken('class_name', Variable), TokenFunctor(self.pushClassName),
            Group([
                ":", NamedToken('base0', Variable), TokenFunctor(self.pushBase0),
                Group([
                    ",", NamedToken('basen', Variable), TokenFunctor(self.pushBaseN),
                ], min=0, max=-1)
            ], min=0),
            "{",
            TokenFunctor(self.startScope),
            Group([Declaration], min=0, max=-1),
            "}",
        ])
        self._class_name = None
        self._bases = []
        self._scope = None

    def clone(self):
        return ClassDeclaration()

    def pushClassName(self, context):
        name = self.getByName('class_name').getToken().id
        if context.getCurrentScope().hasDeclaration(name, recursive=False):
            raise Exception("Cannot redefine " + name)
        self._class_name = name
        return True

    def pushBase0(self, context):
        name = self.getByName('base0').getToken().id
        if not context.getCurrentScope().hasDeclaration(name):
            raise Exception("Unknown base class " + name)
        self._bases.append(name)
        return True

    def pushBaseN(self, context):
        name = self.getByName('basen').getToken().id
        if not context.getCurrentScope().hasDeclaration(name):
            raise Exception("Unknown base class " + name)
        self._bases.append(name)
        return True

    def startScope(self, context):
        self._scope = context.beginScope(self._class_name)
        self._class = ast.Class(self._class_name, self._bases)
        self._scope.declarations.append(self._class)
        print "declare", self._class
        return True

    def match(self, context):
        self._class_name = None
        self._bases = []
        self._scope = None

        res = Group.match(self, context)
        if self._scope is not None:
            context.endScope()
        return res

    def onMatch(self, context):
        self._scope.parent.childs.append(self._scope)
        self._scope.parent.declarations.append(self._class)

