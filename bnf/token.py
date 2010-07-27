#-*- encoding: utf-8 -*-

from bnf.context import Context

import inspect
from abc import abstractmethod, ABCMeta

class MetaToken(ABCMeta):
    def __str__(cls):
        if cls.__token__ is not None:
            return str(cls.__token__)
        else:
            return cls.__name__

    def __or__(cls, other_token):
        from bnf.alternative import Alternative
        return Alternative([cls, other_token])


class Token(object):
    """
        Generic class to contain a Token
    """
    __metaclass__ = MetaToken

    __token__ = None

    @abstractmethod
    def match(self, context):
        """
            Boolean method that checks if the context match.
            It let the context untouched when result is False
        """
        return False

    @abstractmethod
    def onMatch(self, context):
        """
            When matching is True, the method match should call this hook
        """
        pass

    def parse(self, context):
        """
            parse the content of context into the match method.
            When the result is True, it call the translate method.
            If out is None, output is redirecter in stderr
        """
        try:
            if self.match(context):
                self.onMatch(context)
                return True
            else:
                print "### Wrong token found, expected ", context.getTokenStack()[-2]
                print "### But found '" + context.getTokenStack()[-1] + "'"
                print "### Stack trace :"
                for token in context.getTokenStack():
                    print '-', token
                return False
        except Exception as e:
            from traceback import print_exc
            print_exc()
            print "### l.", context.getCurrentLine(), ":", e
            print "### Stack trace :"
            for token in context.getTokenStack():
                print '-', token
        return False

    def __str__(self):
        return str(self.__class__.__token__)

    def __or__(self, other_token):
        from bnf.alternative import Alternative
        if inspect.isclass(other_token):
            return Alternative([self, other_token()])
        elif isinstance(other_token, basestring):
            from bnf.literal import Literal
            return Literal(other_token)
        else:
            return Alternative([self, other_token])

    @abstractmethod
    def clone(self):
        """
            Return a new copy a the token
        """
        return self.__class__()
