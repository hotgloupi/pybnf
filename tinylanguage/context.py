# -*- encoding: utf-8 -*-

from bnf import Context as BaseContext

from tinylanguage.scope import Scope

class Context(BaseContext):

    #
    _scopes = None
    _cur_scope = None

    def __init__(self, filename):
        BaseContext.__init__(self, filename)
        self._scopes = {}
        self.pushScope(filename[:-3], None)


    def pushScope(self, name, parent):
        scope = Scope(name, parent)
        self._scopes[name] = scope
        self._cur_scope = scope

    def getCurrentScope(self):
        return self._cur_scope


