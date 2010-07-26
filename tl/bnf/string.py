# -*- encoding: utf-8 -*-

from bnf import Identifier, Group, NamedToken

class InnerString(Identifier):
    __default_regex__ = r'([^\\"]|\\.)*'
    __whitespaces__ = []

# String ::= "\"" InnerString "\""
class String(Group):
    __group__ = [
        '"', NamedToken('string', InnerString), '"'
    ]

    def onMatch(self, context):
        string = self.getByName('string').getToken().id
        context.getCurrentExpression().append('"'+string+'"')
