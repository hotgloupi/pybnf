# -*- encoding: utf-8 -*-

class Function(object):

    type = None
    name = None
    params = None

    def __init__(self, type, name, params):
        self.type = type
        self.name = name
        self.params = params

    def __str__(self):
        res = self.type + ' ' + self.name + '('
        params = []
        for p in self.params:
            params.append(str(p[0]) + ' ' + str(p[1]))
        res += ", ".join(params) + ")"
        return res

