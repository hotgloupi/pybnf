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

    def hasDeclaration(self, name, recursive=True):
        for d in self.declarations:
            if name == d.name:
                return True
        if self.parent is not None and recursive == True:
            return self.parent.hasDeclaration(name, recursive=True)
        return False


    def getDeclaration(self, name):
        for d in self.declarations:
            if name == d.name:
                return d
        if self.parent is None:
            return None
        return self.parent.getDeclaration(name)


    def __str__(self):
        global indent
        res = " " * indent + "* Scope " + str(self.name) + " declarations :\n"
        for declaration in self.declarations:
            res += " " * indent + "      -- "+ str(declaration) + "\n"

        if len(self.statements) > 0:
            res += " " * indent + "      -- statements:\n"
            for statement in self.statements:
                res += " " * (indent + 2) + "      $ "+ str(statement) + "\n"
        else:
            res += " " * indent + "      -- no statements.\n"

        indent += 2
        for child in self.childs:
            res += str(child)
        indent -= 2
        return res


