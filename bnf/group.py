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
    # class scope
    __recursive_group__ = False
    __group__ = None
    # object scope
    _group = None
    _named_tokens = None
    _min = 1
    _max = 1

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

    def getMinMatch(self, context=None):
        if isinstance(self._min, int):
            return self._min
        else:
            return self._min(context)

    def getMaxMatch(self, context=None):
        if isinstance(self._max, int):
            return self._max
        else:
            return self._max(context)


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
        groups = []
        res = None
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
        debug = True
        global indent
        indent += 1
        i = 0
        context.pushToken(self)
        while i < self.getMaxMatch(context) or self.getMaxMatch(context) == -1:
            backup = context.clone()
            for index, token in enumerate(self._group):
                if inspect.isclass(token):
                    if issubclass(token, Group):
                        token = token()
                        self._group[index] = token
                    else:
                        raise Exception("Wrong object found in the group")
                #elif i > 0:
                #    token = token.clone()
                #    self._group[index] = token

                if debug:
                    print '-' * indent, i, "search:", str(token)
                has_matched = token.match(context)
                if not isinstance(has_matched, bool):
                    raise Exception("Match function must return a bool ("+str(token.__class__)+")")
                if has_matched == False:
                    if i >= self.getMinMatch(context):
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
            if hasattr(token, '__recursive_group__') and token.__recursive_group__ == True:
                strings.append(token.__class__.__name__)
            else:
                strings.append(str(token))
        strbase = '[' + ' '.join(strings) + ']'

        min = self.getMinMatch(None)
        max = self.getMaxMatch(None)
        if min == 1 and max == 1:
            return strbase
        elif min == 0 and max == 1:
            return strbase +'?'

        if max == -1:
            if min == 0:
                return strbase + '*'
            elif min == 1:
                return strbase + '+'
            return strbase + '(' + str(min) + '..*)'
        return strbase + '(' + str(min) + '..' + str(max) + ')'



