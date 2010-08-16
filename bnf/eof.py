# -*- encoding: utf-8 -*-

from bnf.token import Token

class EOF(Token):

    __token__ = "EOF"
    __whitespaces__ = [' ', '\n', '\t', '\r']

    def match(self, context):
        context.pushToken(self)
        backup = context.clone()
        if self.__whitespaces__ is not None:
            context.skipChars(self.__whitespaces__)
        if context.readSize(1) == False:
            self.onMatch(context)
            return True
        else:
            context.restore(backup)
            return False

