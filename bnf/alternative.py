# -*- encoding: utf-8 -*-

from bnf.group import Group

class Alternative(Group):

    def __init__(self, alternatives):
        super(Alternative, self).__init__(group=list(alternatives))

    def __str__(self):
        strings = []
        for alternative in self._group:
            strings.append(str(alternative))
        return "[" + " | ".join(strings) + "]"

    def match(self, context):
        for alternative in self._group:
            context.pushToken(self)
            if alternative.match(context):
                return True
            else:
                context.popToken(start=alternative)
        return False

    def onMatch(self, context): pass

    def clone(self):
        return self.__class__(self._group)

    def __or__(self, other):
        self._group.append(self.prepareItem(other))
        return self

