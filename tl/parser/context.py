# -*- encoding: utf-8 -*-

from bnf import Context as BaseContext

from tl.ast import Scope,           \
                   Expression
import random
random.seed(0)

class Context(BaseContext):

    _cur_scope = None
    _expressions = None
    _cur_expression = None

    def __init__(self, filename):
        BaseContext.__init__(self, filename)
        self._scopes = {}
        self._expressions = []


    def beginScope(self, name=None, generate_unique=False):
        if generate_unique == True:
            if name is None:
                name = "Anonymous"
            name += str(random.randint(1, 9999))
            if self._cur_scope is not None:
                while self._cur_scope.hasDeclaration(name):
                    name += str(random.randint(1, 9))
        if name is None:
            raise Exception("Cannot begin scope with no name")
        scope = Scope(name, self._cur_scope)
        self._cur_scope = scope
#        print "$$ Enter in", name
        return scope

    def endScope(self):
#        print "$$ Out of", self._cur_scope.name
        self._cur_scope = self._cur_scope.parent

    def getCurrentScope(self):
        return self._cur_scope

    def beginExpression(self):
        self._cur_expression = Expression()
        self._expressions.append(self._cur_expression)
        return self._cur_expression

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


