# -*- encoding: utf-8 -*-

from bnf import Context as BaseContext

from tinylanguage.scope import Scope

class Context(BaseContext):

    #
    _scopes = None
    _cur_scope = None

    def __init__(self, filename):
        BaseContext.__init__(self, filename)
        _scopes = {}
        self.pushScope(new Package)

