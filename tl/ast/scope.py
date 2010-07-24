# -*- encoding: utf-8 -*-

indent = 0

class Scope(object):

    parent = None
    name = None
    childs = None
    declarations = None
    statements = None

    def __init__(self, name, parent):
        self.parent = parent
        self.name = name
        self.childs = []
        self.declarations = []
        self.statements = []

    def hasDeclaration(self, name):
        for d in self.declarations:
            if name == d.name:
                return True
        if self.parent is None:
            return False
        return self.parent.hasDeclaration(name)

    def getDeclaration(self, name):
        for d in self.declarations:
            if name == d.name:
                return d
        if self.parent is None:
            return None
        return self.parent.getDeclaration(name)


    def __str__(self):
        global indent
        res = " " * indent + "* Scope " + self.name + " declarations :\n"
        for declaration in self.declarations:
            res += " " * indent + "      -- "+ str(declaration) + "\n"
            res += " " * indent + "      -- "+ str(self.statements) + "\n"
        indent += 2
        for child in self.childs:
            res += str(child)
        indent -= 2
        return res


