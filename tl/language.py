# -*- encoding: utf-8 -*-

from bnf import Group, EOF
from tinylanguage.statement import Statement

# Language ::= [Statement]*
class Language(Group):
    __group__ = [Group([Statement], min=0, max=-1), EOF]

