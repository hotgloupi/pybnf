# -*- encoding: utf-8 -*-

from tl.bnf.variable import Variable

# VariableValue ::= Variable
class VariableValue(Variable):

    def onMatch(self, context):
        if not context.getCurrentScope().hasDeclaration(self.id):
            raise Exception("Unknown variable " + self.id)
        context.getCurrentExpression().append(self.id)
