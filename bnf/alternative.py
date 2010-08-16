# -*- encoding: utf-8 -*-

from bnf.group import Group
import inspect

class Alternative(Group):

    def __init__(self, alternatives):
        Group.__init__(self, group=list(alternatives))

    def __str__(self):
        strings = []
        for alternative in self._group:
            strings.append(str(alternative))
        return "[" + " | ".join(strings) + "]"

    def match(self, context):
        context.pushToken(self)
        for index, alternative in enumerate(self._group):
            if inspect.isclass(alternative):
                if issubclass(alternative, Group):
                    alternative = alternative()
                    self._group[index] = alternative
                else:
                    raise Exception("Wrong object found in alternatives")
            if alternative.match(context):
                return True
            else:
                context.popToken(start=alternative)
        return False

    def __or__(self, other):
        self._group.append(self.prepareItem(other))
        return self

