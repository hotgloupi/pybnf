# -*- encoding: utf-8 -*-

class Reference(object):

    reference = None

    def __init__(self, reference):
        self.reference = reference;

    def __str__(self):
        return "reference<" + str(self.reference) + ">"
