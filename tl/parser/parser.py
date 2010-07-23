# -*- encoding: utf-8 -*-

from tl.parser.context import Context
from tl.bnf import Language

class Parser(object):

    _context = None

    def __init__(self, filename):
        self._context = Context(filename)

    def parse(self):
        return Language().parse(self._context)
