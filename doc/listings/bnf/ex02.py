#!/usr/bin/env python

from bnf import Context
from bnf import Literal

# Language ::= "Hello, World!"
class Language(Literal):
    __token__ = "Hello, World!"

if __name__ == '__main__':
    context = Context('filename')

    language = Language()
    language.parse(context)
