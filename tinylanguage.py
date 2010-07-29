#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from tl.parser import Parser

if __name__ == '__main__':
    parser = Parser()

    ast = parser.parse('test.tl')


