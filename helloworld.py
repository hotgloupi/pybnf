#!/usr/bin/env python

# -*- encoding: utf-8 -*-

from bnf.group import Group
from bnf.literal import Literal

# syntaxe 0

language0 = Group(["Hello", "World!"])              # language0 ::= "Hello" "World!"
print "language0:", language0

# syntaxe 1

class Hello(Literal):                               # Hello ::= "Hello"
    __token__ = "Hello"

class World(Literal):                               # World ::= "World!"
    __token__ = "World!"


language1 = Group([Hello, World])                   # language1 ::= Hello World
print "language1:", language1
language2 = Group([Hello, World], max=-1)           # language2 ::= [Hello World]+
print "language2:", language2
language3 = Group([Hello, World], min=0, max=-1)    # language3 ::= [Hello World]*
print "language3:", language3
language4 = Group([Hello | World], min=0, max=-1)    # language4 ::= [Hello | World]*
print "language4:", language4
language5 = Group([Hello, Group([','], min=0), World]) # language5 ::= [Hello [',']? World]
print "language5:", language5

# syntaxe 2

class Language6(Group):                             # == language 1
    __group__ = [Hello, World]

print "language6:", Language6()

# utilisation de littéraux

class Language7(Group):                         # Language7 ::= [[[Hello ','] | [Hello Hello]] World]*
    __group__ = Group([
        [Group([Hello, ',']) | Group([Hello], min=2, max=2)], World
    ], min=0, max=-1)

print "language7:", Language7()

language8 = Group([Hello | World | "pif"])
print "language8:", language8

