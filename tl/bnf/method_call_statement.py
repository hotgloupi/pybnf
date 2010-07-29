# -*- encoding: utf-8 -*-

from bnf import Group

from tl.bnf.endstatement import EndStatement
from tl.bnf.attribute_access_sub_expr import AttributeAccessSubExpr
from tl.bnf.variable_value import VariableValue

class MethodCallStatement(Group):

    __group__ = [
        AttributeAccessSubExpr(VariableValue),
        EndStatement
    ]

    def match(self, context):
        context.beginExpression()
        res = Group.match(self, context)
        context.endExpression()
        return res

    def onMatch(self, context):
        print "EXPR", context.getCurrentExpression()


