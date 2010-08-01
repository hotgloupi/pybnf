# Language ::= "Hello, World!"
class Language(Literal):
    __token__ = "Hello, World!"

    def onMatch(self, context):
        print "Match !!"
