#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from tl.bnf import Language, Context

if __name__ == '__main__':
    context = Context('test.tl')

    parser = Language()
    parser.parse(context)



