# -*- encoding: utf-8 -*-

from bnf import Identifier

class Number(Identifier):
    __default_regex__ = r'[0-9]+'

    def onMatch(self, context):
        context.getCurrentExpression().append(self.id)

