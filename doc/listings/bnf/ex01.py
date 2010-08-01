#!/usr/bin/env python

from bnf import Context
from bnf import Literal

if __name__ == '__main__':
    context = Context('filename')

    # language ::= "Hello, World!"
    language = Literal('Hello, World!')
    language.parse(context)
