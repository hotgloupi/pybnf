# -*- encoding: utf-8 -*-

from bnf import Group, EOF
from tl.bnf.declaration import Declaration

# Language ::= [Statement]*
class Language(Group):
    __group__ = [Group([Declaration], min=0, max=-1), EOF]

