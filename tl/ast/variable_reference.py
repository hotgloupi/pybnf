# -*- encoding: utf-8 -*-


class VariableReference(object):

    declaration = None

    def __init__(self, declaration):
        self.declaration = declaration

    def __str__(self):
        return self.declaration.name
