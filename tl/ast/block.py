# -*- encoding: utf-8 -*-

class Block(object):

    def __init__(self, keywords, expression, scope):
        self.keywords = keywords
        self.expression = expression
        self.scope = scope

    def __str__(self):
        res = self.scope.name
        if self.expression is not None:
            res += ' (' + str(self.expression) + ')'
        return res
