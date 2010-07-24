# -*- encoding: utf-8 -*-

from tl.ast.function_call import FunctionCall

class Expression(list):
    """
        Contains expression
    """

    @staticmethod
    def _clean(expr):
        if isinstance(expr, (Expression, list)):
            if len(expr) == 1:
                return Expression._clean(expr[0])
            else:
                return Expression(list(Expression._clean(i) for i in expr))
        if isinstance(expr, FunctionCall):
            params = list(Expression._clean(p) for p in expr.params)
            return FunctionCall(expr.name, params)
        return expr

    def clean(self):
        return Expression._clean(self)

    @staticmethod
    def _toString(expr):
        if isinstance(expr, list):
            res = '('
            for i in expr:
                res += str(i)
            res += ')'
        else:
            res = str(expr)
        return res

    def __str__(self):
        return Expression._toString(self)
