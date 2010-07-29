# -*- encoding: utf-8 -*-

from tl.parser.context import Context
from tl.bnf import Language
from tl import ast

class Parser(object):

    _context = None

    def parse(self, filename):
        context = Context(filename)
        main_scope = context.beginScope(
            ast.SCOPE_TYPES['package'],
            name=filename[:-3]
        )
        main_scope.declarations.extend([
            ast.Type('c_int', 'int'),
            ast.Type('c_uint', 'unsigned int'),
            ast.Type('c_float', 'float'),
            ast.Type('c_double', 'double'),
            ast.Type('c_char', 'char'),
            ast.Type('c_char', 'unsigned char'),
            ast.Type('c_string', 'char*'),
            ast.Type('c_short', 'short'),
            ast.Type('c_ushort', 'unsigned short'),
            ast.Type('c_void', 'void'),
            ast.Type('auto'),
        ])
        res = Language().parse(context)
        context.endScope()
        print "Main Scope :"
        print main_scope
        return main_scope


