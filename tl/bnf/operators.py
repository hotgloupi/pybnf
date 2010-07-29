# -*- encoding: utf-8 -*-

from bnf import Literal

class BinaryInfixOperator(Literal):

    def onMatch(self, context):
        context.getCurrentExpression().append(self._token)

