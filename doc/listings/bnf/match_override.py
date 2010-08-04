
class MyToken(Token):

    def match(self, context):
        backup = context.clone()
        # your actual code to know whatever the token match or not.
        # we assume the variable 'res' contains resulting boolean
        if res == False:
            context.restore(backup)
        elif res == True:
            self.onMatch(self, context)
        else: # if you are paranoid :)
            raise Exception("Wrong type for match result !")
        return res
