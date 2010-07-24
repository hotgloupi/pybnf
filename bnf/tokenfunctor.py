# -*- encoding: utf-8 -*-

from bnf.group import Group
from inspect import ismethod, isfunction, isclass

class TokenFunctor(Group):

    # Group class compatibility
    _group = None

    # When method is not bounded
    _this = None

    _method = None
    _args = None
    _kwargs = None

    def __init__(self, *args, **kwargs):
        """
            Constructor can receive a function, a bounded method, and a method
            with a self argument.

        """
        if len(args) > 0 and isfunction(args[0]):
            self._this = None
            self._method = args[0]
            self._args = args[1:]
        elif len(args) > 0 and ismethod(args[0]):
            if args[0].__self__ is None:
                raise Exception("Missing self argument")
            self._this = None
            self._method = args[0]
            self._args = args[1:]
        elif len(args) > 1 and ismethod(args[1]):
            if args[1].__self__ is not None:
                raise Exception("Self argument on a bounded method")
            self._this = args[0]
            self._method = args[1]
            self._args = args[2:]
        else:
            print args, kwargs
            raise Exception("Missing method")
        self._kwargs = kwargs
        self._group = list(self._args) + list(self._kwargs.values())
        if self._this is not None:
            self._group.append(self._this)
        self._named_tokens = {}

    def __call__(self, *args, **kwargs):
        new_args = self._args + args
        new_kwargs = {}
        new_kwargs.update(self._kwargs)
        new_kwargs.update(kwargs)
        if self._this is None:
            return self._method(*new_args, **new_kwargs)
        else:
            return self._method(self._this, *new_args, **new_kwargs)

    def match(self, context):
        context.pushToken(self)
        return self.__call__(context)

    def clone(self):
        new_args = []
        if self._this is not None:
            new_args.append(self._this) # we dont clone this arg
        new_args.append(self._method)
        for arg in self._args:
            new_args.append(self.prepareItem(arg))

        new_kwargs = {}
        for k, v in self._kwargs.iteritems():
            new_kwargs[k] = self.prepareItem(v)
        return TokenFunctor(*new_args, **new_kwargs)

    def __str__(self):
        return '' #'functor"' + self._this.__class__.__name__ + "." + self._method.__name__ + '"'

