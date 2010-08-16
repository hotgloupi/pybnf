# -*- encoding: utf-8 -*-

from token import Token
from context import Context
import re

class Identifier(Token):
    id = None
    _regex_str = None
    _regex = None
    _regex_res = None
    __default_regex__ = r'[_a-zA-Z][_a-zA-Z0-9]*'
    __whitespaces__ = [' ', '\n', '\r', '\t']

    def __init__(self, regex=None, whitespaces=None):
        if regex is None:
            self._regex_str = self.__class__.__default_regex__
        else:
            self._regex_str = regex
        if whitespaces is None:
            whitespaces = self.__class__.__whitespaces__

        self._regex = re.compile(self._regex_str)
        self._whitespaces = whitespaces
        self.id = None

    def match(self, context):
        context.pushToken(self)
        context.pushRule('whitespaces', self._whitespaces)
        retval = False
        res = []
        if context.readRegex(self._regex, res):
            self.id = str(res[0])
            self.onMatch(context)
            retval = True
        context.popRule('whitespaces')

        context.pushToken("buf: " +context.getBuf())
        return retval


    def __str__(self):
        if self.id is not None:
            return '"' + self.id + '"'# + '{' + object.__str__(self) + '}'
        elif self._regex_str is not None:
            return '"'+ self._regex_str + '"'# + '{' + object.__str__(self) + '}'
        else:
            return 'i""'# + '{' + object.__str__(self) + '}'

