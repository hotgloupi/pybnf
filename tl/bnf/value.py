# -*- encoding: utf-8 -*-

from bnf import Group
from tl.bnf.function_call import FunctionCall
from tl.bnf.number import Number
from tl.bnf.variable_value import VariableValue
from tl.bnf.string import String

# Value ::= Number | FunctionCall | VariableValue | String
class Value(Group):
    __group__ = [
        Number | FunctionCall | VariableValue | String
    ]

    def __str__(self):
        return 'Value'

