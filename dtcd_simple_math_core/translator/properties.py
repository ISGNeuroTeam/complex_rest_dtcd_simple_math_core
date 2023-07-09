# -*- coding: utf-8 -*-
"""This module describes logic of working with Property objects.
"""

from typing import Dict, List


class Property:
    """This class describes how Property works.
    Wrapper for simple data storage

    Args:
         :: value: value of the property
         :: status: status of the property
         :: type_: type of the property
         :: expression: expression of the property
         :: has_import: flag that shows if property uses import of data via inPort
                        technically it says if an expression has 'inPort' string in it
         :: imports: list of strings, that represent exact `inPort1`, `inPort2` etc.
         :: import_expression: expression to use when it is imported, in order not to change expression graph value,
                               but to calc imported value
    """
    value: str
    status: str
    type_: str
    expression: str
    has_import: bool
    imports: List[str]
    import_expression: str

    def __init__(self, value: str = '', status: str = 'complete', type_: str = 'expression',
                 expression='', **kwargs):
        self.value = value
        self.status = status
        self.type_ = type_
        self.expression = expression
        self.has_import = type(self.expression) == str and 'inPort' in self.expression
        self.imports = [value for value in self.expression.split() if 'inPort' in value] if self.has_import else 0
        self.import_expression = self.expression if self.has_import else ''
        self.__dict__.update(kwargs)

    @property
    def get_expression(self) -> str:
        """Get string representation of the expression"""
        return str(self.expression) if not isinstance(self.expression, str) else self.expression

    def update(self, value: str, status: str = ...) -> None:
        """Function to save value and status inside Property object"""
        self.value = value
        self.status = status if status else self.status

    def replace_import_expression(self, target: str, source: str):
        new_exp = self.import_expression.replace(target, source)
        self.import_expression = new_exp

    def has_expression(self) -> bool:
        """Checks if property has an expression"""
        return len(str(self.expression)) > 0

    def get_dictionary(self) -> Dict:
        """Get dictionary representation of the Property"""
        return self.__dict__

    # def get_all_object_property_names_out_of_expression(self):
    #     result = re.findall(EVAL_GLOBALS['re_object_property_name'], self.expression)
    #     return result

    def __str__(self):
        """Get string representation of the Property"""
        return ' | '.join(f'{key}={value}' for key, value in self.__dict__.items())
