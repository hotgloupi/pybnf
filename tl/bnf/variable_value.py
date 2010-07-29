# -*- encoding: utf-8 -*-

from tl.bnf.variable import Variable
from tl import ast

# VariableValue ::= Variable
class VariableValue(Variable):

    def match(self, context):
        res = Variable.match(self, context)
        if res == True:
            if not context.getCurrentScope().hasDeclaration(self.id):
                return False
            var = context.getCurrentScope().getDeclaration(self.id)
            context.getCurrentExpression().append(ast.Reference(var))
        return res
