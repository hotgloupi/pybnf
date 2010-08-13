# Pair ::= Key "=" Value ";"
class Pair(Group):
    __group__ = [
        {'key': Key},
        "=",
        {'val': Value},
        ";"
    ]
