# -*- encoding: utf-8 -*-

from tl.bnf.variable import Variable

# VariableValue ::= Variable
class VariableValue(Variable):

    def onMatch(self, context):
        context.getCurrentExpression().append(self.id)
