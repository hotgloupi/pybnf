# -*- encoding: utf-8 -*-

class Type(object):

    def __init__(self, name, cname=None):
        self.name = name
        self.cname = cname

    def __str__(self):
        return 'type '+ self.name


