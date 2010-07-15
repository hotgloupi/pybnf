# -*- encoding: utf-8 -*-

class Scope(object):

    _parent = None
    _name = None
    _childs = None
    _declarations = None

    def __init__(self, name, parent):
        self._parent = parent
        self._name = name
        self._childs = {}
        self._declarations = {}

    def addDeclaration(self, type, name):
        self._declarations[name] = type
