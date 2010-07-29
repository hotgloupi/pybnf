# -*- encoding: utf-8 -*-

import os
from tl import ast

class CWriter(object):

    def __init__(self, working_directory):
        self._directory = working_directory
        self._checkDirectory()
        self._translate_methods = {
            ast.SCOPE_TYPES['package']: self._translatePackage,
            ast.SCOPE_TYPES['class']: self._translateClass,
            ast.SCOPE_TYPES['function']: self._translateFunction,
            ast.SCOPE_TYPES['block']: self._translateBlock,
        }

    def _checkDirectory(self):
        p = self._directory
        if not os.path.exists(p):
            os.mkdir(p)
        elif not os.path.isdir(p):
            raise Exception('"'+p+'" is not a directory')

    def translate(self, scope):
        base_name = os.path.join(self._directory, scope.name)
        source = open(base_name + ".c", "w")
        header = open(base_name + ".h", "w")
        print "Translate", scope.name
        header.write("""

#ifndef __""" + scope.name + """_H__
# define __""" + scope.name + """_H__

""")
        self._translateScope(scope, source, header)
        header.write("""
#endif /* !__""" + scope.name + """_H__ */

""")
        source.close()
        header.close()

    def _translateScope(self, scope, source, header):
        if scope.type not in self._translate_methods:
            raise Exception("Cannot translate scope with type '"+str(scope.type)+"'")
        method = self._translate_methods[scope.type]
        method(scope, source, header)

    def _translatePackage(self, scope, source, header):
        for child in scope.childs:
            self._translateScope(child, source, header)

    def _translateClass(self, scope, source, header):
        pass

    def _translateFunction(self, scope, source, header):
        f = scope.getDeclaration(scope.name)
        source.write(self._getCType(f.type)+ " " + f.name + "(")
        for p in f.params:
            print p
        source.write(")\n")
        source.write("{\n")
        for declaration in scope.declarations:
            if declaration != f:
                self._translateDeclaration(declaration, scope, source, header)
        for statement in scope.statements:
            self._translateStatement(statement, scope, source)
        source.write("}\n")


    def _translateBlock(self, scope, source, header):
        pass

    def _getCType(self, type):
        if isinstance(type, ast.Reference):
            type = type.reference
        if isinstance(type, ast.Type):
            if type.cname is not None:
                return type.cname
            else:
                raise Exception("Cannot get CType of "+str(type))
        raise Exception("Hu?")

    def _translateStatement(self, statement, scope, source):
        print "s: " + str(statement.__class__)
        if isinstance(statement, ast.Expression):
            self._translateExpression(statement, scope, source)
        elif isinstance(statement, list):
            for part in statement:
                source.write(str(part) + " ")
            source.write(";\n")
        else:
            raise Exception("Unknown statement type "+statement.__class__)

    def _translateDeclaration(self, declaration, scope, source, header):
        print "d: "+str(declaration.__class__)
        if isinstance(declaration, ast.Variable):
            source.write(
                self._getCType(declaration.type) + " " + declaration.name
            )
            source.write(";\n")

    def _translateExpression(self, expr, scope, source):
        res = []
        for part in expr:
            if isinstance(part, ast.Reference):
                part = part.reference
            if isinstance(part, ast.Variable):
                res.append(part.name)
            elif isinstance(part, str):
                res.append(part)
            print part.__class__, part
        source.write(" ".join(res) + ";\n")
