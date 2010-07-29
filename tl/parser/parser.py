# -*- encoding: utf-8 -*-

from tl.parser.context import Context
from tl.bnf import Language
from tl.ast.type import Type

class Parser(object):

    _context = None

    def parse(self, filename):
        context = Context(filename)
        main_scope = context.beginScope(filename[:-3])
        main_scope.declarations.extend([
            Type('c_int', 'int'),
            Type('c_uint', 'unsigned int'),
            Type('c_float', 'float'),
            Type('c_double', 'double'),
            Type('c_char', 'char'),
            Type('c_char', 'unsigned char'),
            Type('c_string', 'char*'),
            Type('c_short', 'short'),
            Type('c_ushort', 'unsigned short'),
            Type('c_void', 'void'),
            Type('auto'),
        ])
        res = Language().parse(context)
        context.endScope()
        print "Main Scope :"
        print main_scope
        return main_scope


