
# Key ::= r'[_a-zA-Z][_a-zA-Z0-9]*'
class Key(bnf.Identifier):
    # r'[_a-zA-Z][_a-zA-Z0-9]*' is the default regex for bnf.Identifier
    pass

# Value ::= r'[0-9]+'
class Value(bnf.Identifier):
    __default_regex__ = r'[0-9]+'

# Pair ::= Key "=" Value ";"
class Pair(Group):
    __group__ = [
        NamedToken('key', Key),
        "=",
        NamedToken('val', Value),
        ";"
    ]

    def onMatch(self, context):
        key = self.getByName('key').getToken()
        val = self.getByName('val').getToken()
        print "FOUND:", key.id, '=', val.id

# lang ::= [Pair]*
lang = Group([Pair], max=-1)

