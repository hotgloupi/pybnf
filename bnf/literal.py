# -*- encoding: utf-8 -*-

from bnf.token import Token
from bnf.context import Context

class Literal(Token):
    """
        Represent a literal token
    """

    __token__ = None
    __skip_ws__ = True
    __translation__ = None
    __whitespaces__ = [' ', '\n', '\t', '\r']

    _token = None
    _skip_ws = None
    _translation = None
    _whitespaces = None


    def __init__(self, token=None, skip_ws=None, translation=None, whitespaces=None):
        if token is None:
            token = self.__class__.__token__
        if translation is None:
            translation = self.__class__.__translation__
        if skip_ws is None:
            skip_ws = self.__class__.__skip_ws__
        if whitespaces is None:
            whitespaces = self.__class__.__whitespaces__

        if token is None:
            raise Exception("Litteral class with no Token")
        self._token = token
        self._skip_ws = skip_ws
        self._translation = translation
        self._whitespaces = whitespaces

    def clone(self):
        new = self.__class__(
            token=self._token,
            skip_ws=self._skip_ws,
            translation=self._translation,
            whitespaces=self._whitespaces
        )
        return new

    def match(self, context):
        context.pushToken(self)
        if self._skip_ws:
            context.pushRule('whitespaces', self._whitespaces)
        res = False
        if context.readString(self._token):
            self.onMatch(context)
            res = True
        if self._skip_ws:
            context.popRule('whitespaces')
        return res

    def onMatch(self, context):
        return
        if self._translation is not None:
            print self._translation
        else:
            print self

    def __str__(self):
        return str(self._token)
