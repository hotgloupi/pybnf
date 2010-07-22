# -*- encoding: utf-8 -*-

from bnf import Context as BaseContext

from tinylanguage.scope import Scope

class Context(BaseContext):

    _scopes = None
    _cur_scope = None
    _expressions = None
    _cur_expression = None

    def __init__(self, filename):
        BaseContext.__init__(self, filename)
        self._scopes = {}
        self.pushScope(filename[:-3], None)
        self._expressions = []


    def pushScope(self, name, parent):
        scope = Scope(name, parent)
        self._scopes[name] = scope
        self._cur_scope = scope

    def getCurrentScope(self):
        return self._cur_scope

    def beginExpression(self):
        self._cur_expression = []
        self._expressions.append(self._cur_expression)

    def endExpression(self):
        self._expressions.pop()
        if len(self._expressions) > 0:
            self._cur_expression = self._expressions[-1]
        else:
            self._cur_expression = None

    def getCurrentExpression(self):
        if self._cur_expression is None:
            raise Exception("No expression in stack !")
        return self._cur_expression


