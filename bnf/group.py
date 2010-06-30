# -*- encoding: utf-8 -*-

from bnf.token import Token
from bnf.literal import Literal
from bnf.namedtoken import NamedToken
import inspect

indent = 0

class Group(Token):
    """
        Represent a group: contain a list of token
    """
    _min = 1
    _max = 1
    __recursive_group__ = False
    # class scope
    __group__ = None
    # object scope
    _group = None
    _named_tokens = None

    def __init__(self, group=None, min=1, max=1):
        if group is None:
            if self.__class__.__group__ is None:
                raise Exception("Group must be defined somewhere !")
            group = self.__class__.__group__
        elif not isinstance(group, list):
            group = [group]

        if isinstance(group, Group):
            min = group._min
            max = group._max
            group = group._group
        self._named_tokens = {}
        self._group = list(self.prepareItem(item) for item in group)
        self._min = min
        self._max = max

    def clone(self):
        new = self.__class__(group=self._group, min=self._min, max=self._max)
        return new

    def prepareItem(self, item):
        if isinstance(item, NamedToken):
            return NamedToken(item.getName(), self.prepareItem(item.getToken()))
        if isinstance(item, basestring):
            res = Literal(token=item)
        elif inspect.isclass(item):
            if issubclass(item, Group):
                if item == Group or item.__recursive_group__ == False:
                    res = item()
                else:
                    res = item
            else:
                res = item()
        elif hasattr(item, 'clone'):
            res = item.clone()
        elif isinstance(item, list):
            res = Group(item)
        else:
            res = item
        return res

    def getByName(self, name):
        res = self._named_tokens.get(name)
        if res is not None:
            return res
        groups = []
        for token in self._group:
            if isinstance(token, NamedToken) and token.getName() == name:
                res = token
                break
            elif isinstance(token, Group):
                groups.append(token)

        if res is None:
            for group in groups:
                res = group.getByName(name)
                if res is not None:
                    break
        return res

    def match(self, context):
        debug = False
        global indent
        indent += 1
        i = 0
        context.pushToken(self)
        while True:
            backup = context.clone()
            for index, token in enumerate(self._group):
                if inspect.isclass(token):
                    if issubclass(token, Group):
                        token = token()
                        self._group[index] = token
                    else:
                        raise Exception("Wrong object found in the group")
                if debug:
                    print '-' * indent, i, "search:", str(token)
                if not token.match(context):
                    if i >= self._min:
                        if debug:
                            print '-' * indent, i, "not found:", str(token)
                            print '-' * indent, i, "but validating", str(self)
                        self.onMatch(context)
                        context.restore(backup)
                        indent -= 1
                        return True

                    indent -= 1
                    context.restore(backup)
                    if debug:
                        print '-' * indent, i, "not found:", str(token)
                    return False
                else:
                    self.onSubMatch(context, token)
                    context.popToken(start=token)
            i += 1
            if i >= self._max and self._max != -1:
                break
        if debug:
            print '-' * indent, i, "found:", str(self)
        indent -= 1
        self.onMatch(context)
        return True

    def onMatch(self, context):
        pass

    def onSubMatch(self, context, token):
        pass

    def __str__(self):
        strings = []
        for token in self._group:
            strings.append(str(token))
        strbase = '[' + ' '.join(strings) + ']'

        if self._min == 1 and self._max == 1:
            return strbase
        elif self._min == 0 and self._max == 1:
            return strbase +'?'

        if self._max == -1:
            if self._min == 0:
                return strbase + '*'
            elif self._min == 1:
                return strbase + '+'
            return strbase + '(' + str(self._min) + '..*)'
        return strbase + '(' + str(self._min) + '..' + str(self._max) + ')'


