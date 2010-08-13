
class XmlContext(bnf.Context):

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
