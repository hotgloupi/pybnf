# -*- encoding: utf-8 -*-


class Expression(list):
    """
        Contains expression
    """

    @staticmethod
    def _clean(expr)
        if isinstance(expr, list):
            if len(expr) == 1:
                return cleanExpression(expr[0])
            else:
                return list(cleanExpression(i) for i in expr)
        return expr

    def clean(self):
        return Expression._clean(self)

    @staticmethod
    def _toString(expr):
        if isinstance(expr, list):
            print '(',
            for i in expr:
                printExpression(i)
            print ')',
        else:
            return str(expr)

    def __str__
