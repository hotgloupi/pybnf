#!/usr/bin/env python

from bnf import Literal, Group, Identifier, NamedToken, Context, TokenFunctor

# BaliseTag = r'[a-zA-Z][a-zA-Z0-9_:-]*'
class BaliseTag(Identifier):
    __default_regex__ = r'[a-zA-Z][a-zA-Z0-9_:-]*'
    

# Balise ::= BaliseTag [Data | [Balise]*] BaliseTag
class Balise(Group):
    __recursive_group__ = True

    def __init__(self):
        Group.__init__(self, [
            '<', NamedToken('open', BaliseTag), '>',
            Identifier(r'[^<]+') | Group(Balise, min=0, max=-1)),
            '</', NamedToken('close', BaliseTag), '>',
            TokenFunctor(self.hasSameTag),
        ])

    def hasSameTag(self, context):
        open_tag = self.getByName('open').getToken().id
        close_tag = self.getByName('close').getToken().id
        if open_tag != close_tag:
            raise Exception("Node tag name mismatch: " + open_tag + ' != ' + close_tag)
        return True

