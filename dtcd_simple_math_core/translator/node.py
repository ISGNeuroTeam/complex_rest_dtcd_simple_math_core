import logging
import re

from properties import Property
from plugins.dtcd_simple_math_core.settings import EVAL_GLOBALS, plugin_name
from typing import Dict


class Node:
    object_id: str = ''
    properties: Dict[str, Property] = {}
    log = logging.getLogger(plugin_name)

    def __init__(self, node: []):
        for _property, data in node['properties'].items():
            self.fill_default_properties(_property, data=data)
        if '_operations_order' not in self.properties.keys():
            self.fill_default_properties('_operations_order', {})

    def fill_default_properties(self, name: str, data: {}):
        self.properties[name] = Property(**data)

    def update_property(self, _property, value):
        try:
            self.properties[_property].update(value, "complete")
            self.properties['_operations_order'].update(self.properties['_operations_order'].expression, "complete")
        except KeyError:
            self.log.warning(f'no {_property} property found, only {self.properties.keys()} got')

    @classmethod
    def filter_eval_properties(cls, _property):
        result = _property[1].type == EVAL_GLOBALS['property_type'] and not _property[0].startswith("_")
        return result

    def get_eval_properties(self):
        return list(filter(self.filter_eval_properties, self.properties.items()))

    @classmethod
    def make_object_property_full_name(cls, re_group, node_properties, node_id):
        name = re_group.group(0)
        if "." not in name and name in node_properties:
            name = ".".join((node_id, name))

        # here we must make this 'StepRichLabelNode11_1.Enabled'
        # look like this "'StepRichLabelNode11_1.Enabled'"
        if re.fullmatch(EVAL_GLOBALS['re_numbers'], name) is None and '.' in name:
            name = f"'{name}'"
        return name

    @classmethod
    def make_expression(cls, cp_tuple, node_properties):
        column, _property, node_id = cp_tuple
        if _property['expression']:
            _exp = _property["expression"]
            _exp = re.sub(EVAL_GLOBALS['re_object_property_name'],
                          lambda p: cls.make_object_property_full_name(p, node_properties,
                                                                       node_id), _exp)
            expression = f'eval \'{node_id}.{column}\' = {_exp}'
        else:
            expression = ''
        return expression

    def get_eval_expressions(self, name: str):
        result = []
        node_properties = self.get_eval_properties()
        for _prop_name, _prop in node_properties:
            if _prop.has_expression():
                _exp = _prop.get_expression
                _exp = re.sub(EVAL_GLOBALS['re_object_property_name'],
                              lambda p: self.make_object_property_full_name(p, self.properties.values(),
                                                                            name), _exp)
                expression = {f'{name}.{_prop_name}': {_exp}}
                result.append(expression)
        return result

    def __str__(self):
        return f'{self.object_id=}\n' + '\n'.join(f'\t\t{prop}' for prop in self.properties)
