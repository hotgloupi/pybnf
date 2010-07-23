# -*- encoding: utf-8 -*-

class FunctionCall(object):
    def __str__(self):
        p = list(str(i) for i in self.params)
        return self.name + '(' + ','.join(p) + ')'

    def __init__(self, name, params):
        self.name = name
        self.params = params
