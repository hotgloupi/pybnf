# -*- encoding: utf-8 -*-

class Class(object):

    def __init__(self, name, bases):
        self.name = name
        self.bases = bases

    def __str__(self):
        return "class " + str(self.name) + "(" + ", ".join(str(b) for b in self.bases) + ")"


