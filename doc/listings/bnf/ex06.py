
# HelloWorld ::= "Hello," "World!"
class HelloWorld(Group):
    __group__ = [
        "Hello,", "World!"
    ]

# lang ::= HelloWorld
lang = HelloWorld()

# lang ::= [HelloWorld]*
lang = HelloWorld(min=0, max=-1)
lang = Group([HelloWorld], min=0, max=-1)

