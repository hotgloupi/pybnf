# -*- encoding: utf-8 -*-

class Context(object):
    """
        Context class contain and manage the main stream to parse
    """

    _file = None
    _buf = None
    _rules = None
    _token_stack = None
    _cur_line = 0

    def __init__(self, filename=None):
        if filename is not None:
            self._file = open(filename, 'r')
        self._buf = ""
        self._rules = {}
        self._token_stack = []
        self.pushRule('whitespaces', [])

    def clone(self):
        new = Context()
        new._file = self._file
        new._buf = self._buf
        new._cur_line = self._cur_line
        new._rules = self._rules # by reference
        new._token_stack = self._token_stack # by reference
        new._save_pos = self._file.tell()
        return new

    def restore(self, backup):
        self._file = backup._file
        self._buf = backup._buf
        self._file.seek(backup._save_pos)
        self._cur_line = backup._cur_line

    def skipChars(self, chars):
        buf_len = len(self._buf)
        i = 0
        while True:
            if i >= buf_len:
                if self.feedFromFile() == False:
                    break
                buf_len = len(self._buf)
            if self._buf[i] in chars:
                i += 1
            else:
                break
        if i > 0:
            self._buf = self._buf[i:]
        return True

    def pushRule(self, name, rule):
        if name not in self._rules:
            self._rules[name] = []
        self._rules[name].append(rule)

    def popRule(self, name):
        if name in self._rules:
            self._rules[name].pop()

    def getRule(self, name):
        if name in self._rules and len(self._rules[name]) > 0:
            return self._rules[name][-1]
        return None

    def readString(self, string):
        if self.skipChars(self.getRule('whitespaces')) == False:
            return False
        if len(self._buf) < len(string):
            if self.feedFromFile() == False or len(self._buf) < len(string):
                return False
        if not self._buf.startswith(string):
            return False
        self.readSize(len(string))
        return True

    def readRegex(self, regex, matchlist=None):
        if self.skipChars(self.getRule('whitespaces')) == False:
            return False
        res = regex.match(self._buf)
        if res is not None:
            self.readSize(len(res.group(0)))
            if matchlist is not None:
                matchlist.append(res.group(0))
            return True
        return False

    def readSize(self, size):
        if len(self._buf) < size:
            if self.feedFromFile() == False or len(self._buf) < size:
                return False
        self._buf = self._buf[size:]

    def __str__(self):
        return "<Context '" + self._buf + "'>"

    def feedFromFile(self):
        buf = self._file.readline()
        self._cur_line += 1
        if len(buf) == 0:
            return False
        else:
            self._buf += buf
            return True

    def pushToken(self, token):
        self._token_stack.append(token)
#        print "push", token, ":\n", '\n'.join('- ' + str(token) for token in self._token_stack)

    def popToken(self, start=None):
        if start is None:
            self._token_stack.pop()
        elif start in self._token_stack:
            self._token_stack = self._token_stack[:self._token_stack.index(start) + 1]
#            print "pop:\n", '\n'.join('- ' + str(token) for token in self._token_stack)
        else:
            print '###', start, "not found in stack:"
            print '\n'.join('- ' + str(token) for token in self._token_stack)

    def getTokenStack(self):
        return self._token_stack

    def getBuf(self):
        return self._buf

    def getCurrentLine(self):
        return self._cur_line
