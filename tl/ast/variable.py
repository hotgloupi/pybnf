# -*- encoding: utf-8 -*-

class Variable(object):
    """
        Store a variable, i.e. its name and its type
    """

    def __init__(self, type, name, value):
        self.type = type
        self.name = name
        self.value = value

    def __str__(self):
        return str(self.type) + " " + str(self.name) + " = " + str(self.value)
