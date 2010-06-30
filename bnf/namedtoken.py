# -*- encoding: utf-8 -*-

from bnf.token import Token

class NamedToken(Token):
    _name = None
    _token = None

    def __init__(self, name, token):
        self._name = name
        self._token = token

    def clone(self):
        return NamedToken(self._name, self._token.clone())

    def getName(self):
        return self._name

    def getToken(self):
        return self._token

    def match(self, context):
        context.pushToken(self)
        return self._token.match(context)

    def onMatch(self): pass

    def __str__(self):
        return "{'" + self._name + "': " + str(self._token) + "}"

    def __or__(self, other):
        from bnf.alternative import Alternative
        return Alternative([self, other])
