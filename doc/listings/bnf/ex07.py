
# Hello ::= "Hello" | "hello"
Hello = Identifier(r'[hH]ello')

# World ::= ["world" | "World"] [<whitespace]* "!"
class World(Identifier):
    __default_regex__ = r'[wW]orld[\w]*!'
