#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from tl.parser import Parser
from tl.writer import CWriter

if __name__ == '__main__':
    parser = Parser()

    scope = parser.parse('test.tl')
    writer = CWriter('work')
    writer.translate(scope)




