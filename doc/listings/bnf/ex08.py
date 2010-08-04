
# Key ::= r'[_a-zA-Z][_a-zA-Z0-9]*'
class Key(bnf.Identifier):
    # r'[_a-zA-Z][_a-zA-Z0-9]*' is the default regex for bnf.Identifier
    pass

# Value ::= r'[0-9]+'
class Value(bnf.Identifier):
    __default_regex__ = r'[0-9]+'

# Pair ::= Key "=" Value ";"
class Pair(Group):

    def __init__(self):
        Group.__init__(self, [
            NamedToken('key', Key), TokenFunctor(self.validateKey),
            "=",
            NamedToken('val', Value),
            ";"
        ])


    def onMatch(self, context):
        key = self.getByName('key').getToken()
        val = self.getByName('val').getToken()
        print "FOUND:", key.id, '=', val.id
        context.hash[key.id] = val.id

    def validateKey(self, context):
        key = self.getByName('key').getToken().id
        if key is in context.hash:
            print "Redefine key", key
            return False
        return True


# lang ::= [Pair]*
lang = Group([Pair], max=-1)

if __name__ == '__main__':
    context = bnf.Context('pairs.txt')
    context.hash = {}

    lang.parse(context)
