# -*- encoding: utf-8 -*-

from bnf import Group, TokenFunctor
from tl import ast

class Block(Group):
    _keywords = None
    _with_expression = None

    def __init__(self, keywords, with_expression, min=1, max=1):
        self._keywords = keywords
        self._with_expression = with_expression
        group = [self._keywords]
        if self._with_expression == True:
            from tl.bnf.expression import Expression
            group.extend(["(", Expression, ")"])
        from tl.bnf.statement import Statement
        group.extend([
            "{",
            Group([Statement], min=0, max=-1),
            "}",
            TokenFunctor(self.endScope)]
        )
        Group.__init__(self, group, min=min, max=max)
        self._scope = None
        self._expr = None

    def match(self, context):
        if self._with_expression == True:
            self._expr = context.beginExpression()
        if isinstance(self._keywords, list):
            name = "-".join(self._keywords)+'_'
        else:
            name = str(self._keywords)+'_'
        self._scope = context.beginScope(
            ast.SCOPE_TYPES['block'],
            name,
            generate_unique=True
        )
        res = Group.match(self, context)
        if self._with_expression == True:
            context.endExpression()
        if self._scope is not None:
            context.endScope()
        return res

    def endScope(self, context):
        context.endScope()
        context.getCurrentScope().childs.append(self._scope)
        if self._expr is not None:
            self._expr = self._expr.clean()
        statement = ast.Block(self._keywords, self._expr, self._scope)
        context.getCurrentScope().statements.append(statement)
        self._scope = None
        return True

    def clone(self):
        return Block(self._keywords, self._with_expression, self._min, self._max)
