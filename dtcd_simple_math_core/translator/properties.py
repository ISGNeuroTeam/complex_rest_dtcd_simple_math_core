# -*- coding: utf-8 -*-
"""This module describes logic of working with Property objects.
"""
import re
from typing import Dict, List, Union, Any

from ..settings import PROPERTY_GLOBALS


class SWTImport:
    """Class to store information about swt import

    Args:
        :: swt_name: name of the swt table to import from
        :: column: name of the column to import from
        """

    swt_name: str
    column: str

    def __init__(self, data: Union[Dict, Any]):
        self.swt_name = data['swt_name']
        self.column = data['column']
        self.column_property = self.column.split('.')[-1]

    def __str__(self):
        return f'{self.swt_name=} | {self.column=}'

    @property
    def name(self):
        """short wrapper of the swt_name parameter"""
        return self.swt_name


class Property:
    """This class describes how Property works.
    Wrapper for simple data storage
    Property may import value from port of the Node it belongs to,
    or from another property of another node.

    Args:
         :: value: value of the property
         :: status: status of the property
         :: type: type of the property
         :: expression: expression of the property
         :: has_import: flag that shows if property uses import of data via inPort
                        technically it says if an expression has 'inPort' string in it
         :: has_swt_import: flag that show if property uses import of data via swt export
                        technically the expression will be a dict like
                            {'swt_name': 'src_graph',       <<< name of the swt table to read from
                             'column': 'Node_9.Prop_01',    <<< name of the node a prop to read from
                             'graphID':	'e6077bbf-c385-46d6-b679-3087feae21f7',}
         :: swt_import: parameter to store swt import data
         :: imports: list of strings, that represent exact `inPort1`, `inPort2` etc.
         :: import_expression: expression to use when it is imported, in order not to change
                               expression graph value, but to calc imported value
    """
    # pylint: disable=too-many-instance-attributes
    # TODO is it a big problem that class has more than 7 attributes?
    value: str
    status: str
    type: str
    expression: Union[str, Dict]
    has_import: bool
    has_swt_import: bool
    swt_import: SWTImport
    imports: List[str]
    import_expression: str

    def __init__(self, value: str = '', status: str = 'complete', type: str = 'expression',
                 expression: Union[str, Dict] = '', **kwargs):
        self.value = value
        self.status = status
        self.type = type
        self.expression = expression
        self.__dict__.update(kwargs)

    def initialize(self):
        # checking if expression is sent from select and has opening and closing singular quote symbol
        if isinstance(self.expression, str) and self.expression.endswith("'") and self.expression.startswith("'"):
            self.expression = self.expression[self.expression.find("'")+1:self.expression.rfind("'")]
        self.has_import = isinstance(self.expression, str) and 'inPort' in self.expression
        self.imports = re.findall(PROPERTY_GLOBALS['re_inport'], self.expression) \
            if self.has_import else 0
        self.import_expression = self.expression if self.has_import else ''
        self.has_swt_import = isinstance(self.expression, dict)
        self.swt_import = SWTImport(self.expression) if self.has_swt_import else 'SWTImport'

    @property
    def get_expression(self) -> Union[str, int, float]:
        """Get string representation of the expression"""
        if isinstance(self.expression, int) or self.expression.isdigit():
            return int(self.expression)
        if is_float(str(self.expression)):
            return float(self.expression)
        return self.expression

    def update(self, value: str, status: str = ...) -> None:
        """Function to save value and status inside Property object"""
        self.value = value
        self.status = status if status else self.status

    def replace_import_expression(self, target: str, source: str):
        """Function to replace import expression with a different one from source"""
        new_exp = self.import_expression.replace(target, source)
        self.import_expression = new_exp

    @property
    def is_float_or_int(self):
        if self.has_swt_import:
            return False
        return is_float(self.expression) or isinstance(self.expression, int)

    def has_expression(self) -> bool:
        """Checks if property has an expression"""
        return len(str(self.expression)) > 0

    def get_dictionary(self) -> Dict:
        """Get dictionary representation of the Property"""
        return self.__dict__

    def __str__(self):
        """Get string representation of the Property"""
        return ' | '.join(f'{key}={value}' for key, value in self.__dict__.items())


def is_float(string: Any) -> bool:
    pattern = r"^[-+]?[0-9]*\.?[0-9]+$"
    match = re.match(pattern, str(string))
    return bool(match)
