#!/usr/bin/env python

from bnf import Literal, Group, Identifier, NamedToken, Context, TokenFunctor

# Balise ::= OpenBalise [Data | [Balise]*] CloseBalise
class Balise(Group):

    __group__ = None
    __recursive_group__ = True

    def __init__(self):
        super(Balise, self).__init__([
            '<', NamedToken('open', Identifier), '>',
            NamedToken('content', Identifier(r'[^<]+')) | Group(Balise, min=0, max=-1),
            '</', NamedToken('close', Identifier), '>',
            TokenFunctor(self, Balise.hasSameTag),
        ])
        self._open_tag = self.getByName('open')
        self._node_content = self.getByName('content')
        self._close_tag = self.getByName('close')

    def onSubMatch(self, context, token):
        if token == self._open_tag:
            context.beginNode(token.getToken().id)
        elif token == self._node_content:
            context.setNodeData(token.getToken().id)
        elif token == self._close_tag:
            context.endNode(token.getToken().id)
        else:
            print token

    def hasSameTag(self, context):
        open_tag = self.getByName('open').getToken().id
        close_tag = self.getByName('close').getToken().id
        if open_tag != close_tag:
            raise Exception("Node tag name mismatch: " + open_tag + ' != ' + close_tag)
        return True

    def clone(self):
        return Balise()

# TinyXml ::= [Balise]+
class TinyXml(Group):
    __group__ = Group([Balise()], max=-1)

class XmlContext(Context):

    def __init__(self, filename):
        super(XmlContext, self).__init__(filename)
        self._root_node = {
            'name': 'root',
            'data': '',
            'childs': []
        }
        self._current_node = self._root_node
        self._nodes = [self._root_node]

    def beginNode(self, name):
        child = {
            'name': name,
            'data': '',
            'childs': []
        }
        self._current_node['childs'].append(child)
        self._current_node = child
        self._nodes.append(child)

    def endNode(self, name):
        if self._current_node['name'] != name:
            print "### Node names mismatch: " + self._current_node['name'] + ' != ' + name
        self._nodes.pop()
        self._current_node = self._nodes[-1]

    def setNodeData(self, content):
        print "set content node", content
        self._current_node['data'] = content

    def getRoot(self): return self._root_node

if __name__ == '__main__':

    ctx = XmlContext('test.sfml')

    lang = TinyXml()
    print "### TinyXml:", lang
    if lang.parse(ctx) == True:
        print "### Xml tree:"
        from pprint import pprint
        pprint(ctx.getRoot())
