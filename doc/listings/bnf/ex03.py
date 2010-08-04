import bnf

# Language ::= "[hH]ello, [wW]orld!"
class Language(bnf.Identifier):
    __default_regex__ = r"[hH]ello, [wW]orld!"

    def onMatch(self, context):
        print "Match", self.id
