# Hello ::= "Hello"
class Hello(Literal):
    __token__ = "Hello"

# World ::= "World"
class World(Literal):
    __token__ = "World"

# lang ::= Hello World
lang = Group([Hello, World])

# lang ::= [Hello World]?
lang = Group([Hello, World], min=0)

# lang ::= [Hello World]+
lang = Group([Hello, World], max=-1)

# lang ::= [Hello World]*
lang = Group([Hello, World], min=0, max=-1)

# lang ::= [Hello World] [Hello World] [Hello World]
lang = Group([Hello, World], min=3, max=3)

# lang ::= Hello "," World "!"
lang = Group([Hello, ",", World, "!"])
