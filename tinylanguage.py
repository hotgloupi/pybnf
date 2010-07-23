#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from tl.parser import Parser

if __name__ == '__main__':
    parser = Parser('test.tl')

    ast = parser.parse()
    for d in parser._context._scopes['test']._declarations:
        print " -", d


