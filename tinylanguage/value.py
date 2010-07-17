# -*- encoding: utf-8 -*-

from bnf import Group, Identifier

class Number(Identifier):
    __default_regex__ = r'[0-9]+'
    def onMatch(self, context):
        print "found number", self.id


class FunctionCall(Group):

    def __init__(self, group=None, min=1, max=1):
        from tinylanguage.expression import Expression
        Group.__init__(self, [
            Identifier(),
            '(',
            Group([
                Expression,
                Group([
                    ',',
                    Expression
                ], min=0, max=-1)
            ], min=0, max=1),
            ')'
        ], min=min, max=max)


class Value(Group):
    __group__ = [
        Number | FunctionCall
    ]

    def __str__(self):
        return 'class"Value"'

