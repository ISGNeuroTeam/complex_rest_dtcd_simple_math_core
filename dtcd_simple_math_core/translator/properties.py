import re
from ..settings import EVAL_GLOBALS


class Property:
    value: str
    status: str
    type_: str
    expression: str

    def __init__(self, value: str = '', status: str = 'complete', type_: str = 'expression', expression='', **kwargs):
        self.value = value
        self.status = status
        self.type_ = type_
        self.expression = expression
        self.__dict__.update(kwargs)

    @property
    def get_expression(self):
        return str(self.expression) if not isinstance(self.expression, str) else self.expression

    def update(self, value: str, status: str = ...) -> None:
        self.value = value
        self.status = status if status else self.status

    def has_expression(self):
        return len(str(self.expression)) > 0

    def get_dictionary(self):
        return self.__dict__

    def get_all_object_property_names_out_of_expression(self):
        return re.findall(EVAL_GLOBALS['re_object_property_name'], self.expression)

    def __str__(self):
        return ' | '.join(f'{key}={value}' for key, value in self.__dict__.items())
