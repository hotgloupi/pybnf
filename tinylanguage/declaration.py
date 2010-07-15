# -*- encoding: utf-8 -*-

from bnf import Group, NamedToken, Literal

from tinylanguage.type import Type
from tinylanguage.variable import Variable
from tinylanguage.endstatement import EndStatement
from tinylanguage.expression import Expression


# Declaration ::= Type Variable
class Declaration(Group):
    __group__ = [
        NamedToken('type', Type),
        NamedToken('name', Variable),
        Group(
            Group(['(', Expression, ')']) |
            Group(['=', Expression]),
            min=0, max=1
        ),
        EndStatement
    ]

    def onMatch(self, context):
        type = self.getByName('type').getToken().id
        name = self.getByName('name').getToken().id
        context.getCurrentScope().addDeclaration(type, name)
        print "declaration", type, name


