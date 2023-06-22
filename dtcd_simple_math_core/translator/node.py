# -*- coding: utf-8 -*-
"""This module describes logic of working with Node objects.
"""
import logging
import re

from .properties import Property
from ..settings import EVAL_GLOBALS, plugin_name
from typing import Dict, Any, Optional, Iterable, Tuple, List


class Node:
    """This class describes how Node works

    Args:
        :: object_id: name of the node
        :: properties: dictionary of the properties Node has
        :: log: local instance of plugin logger
    """
    object_id: str
    properties: Dict[str, Property]
    log: logging.Logger = logging.getLogger(plugin_name)

    def __init__(self, node: {}):
        self.object_id = node.get('primitiveID', '')
        self.properties = {}
        # TODO split [initiating object_id and properties] and [filling default parameters]
        for prop_name, data in node['properties'].items():
            self.fill_default_properties(prop_name, data=data)
        if '_operations_order' not in self.properties.keys():
            self.fill_default_properties('_operations_order', {'expression': 100})

    def fill_default_properties(self, name: str, data: Dict):
        """Here we save the empty Property instance as a value of the name key
        of the properties' dictionary.
        Args:
              :: name: name of the property to save
              :: data: dictionary of the data we need to save according to the named property.
        """
        self.properties[name] = Property(**data)

    def update_property(self, prop_name: str, value: Any) -> None:
        """Here we update the property with prop_name with its value
        and also update _operations_order's expression to "complete",
        if we have such property saved.
        """
        try:
            self.properties[prop_name].update(value, "complete")
            self.properties['_operations_order'].update(self.properties['_operations_order'].expression, "complete")
        except KeyError:
            self.log.warning(f'no {prop_name} property found, only {self.properties.keys()} got')

    @classmethod
    def filter_eval_properties(cls, prop: Tuple[str, Property]) -> bool:
        """ Here we check if current property satisfies the conditions:
        1. not starts with "_"
        2. its type is equal to EVAL_GLOBALS['property_type'] saved in
           dtcd_simple_math_core.conf plugin config

        Args:
            :: prop: tuple of property name and property data dictionary

        Returns:
            True or False depending on whether prop satisfies the conditions described above
        """
        result = prop[1].type_ == EVAL_GLOBALS['property_type'] and not prop[0].startswith("_")
        return result

    def get_eval_properties(self) -> List[Tuple[str, Property]]:
        """Function takes all properties saved and return the ones that satisfy filter conditions
        described in filter_eval_properties functions

        Returns:
            list of tuples with names and dictionaries of properties that do satisfy
            that conditions
        """
        result = list(filter(self.filter_eval_properties, self.properties.items()))
        return result

    @classmethod
    def make_object_property_full_name(cls, re_group: re.Match, node_properties: Iterable, node_id: str) -> str:
        """
        Here we make several manipulations and checks in order to create proper object property names.
        Example:
            if we have a node: 'UncontrolledRichLabelNode01_1'
            and it has properties:
                - testField
                - movieStar
                - theBest
                - _operations_order

            and current property "theBest" [taken from re_group] has "movieStar" in its expression,
            it must make it look like 'UncontrolledRichLabelNode01_1.movieStar'

        Returns:
            full object property name
        """
        name = re_group.group(0)
        if "." not in name and name in node_properties:
            name = ".".join((node_id, name))

        # here we must make this 'StepRichLabelNode11_1.Enabled'
        # look like this "'StepRichLabelNode11_1.Enabled'"
        if re.fullmatch(EVAL_GLOBALS['re_numbers'], name) is None and '.' in name:
            name = f"'{name}'"
        return name

    def get_eval_expressions(self) -> List[Dict]:
        """This function loops through the node and its properties to get the string of
        all possible eval expressions.

        Returns:
            list of all properly created object property names and its expression values

        Example:
            we have a node: 'UncontrolledRichLabelNode01_1'
            with only one property: 'testField'
            which has an expression: '2018'
            result of all eval expressions ofr this node will be:
            {'UncontrolledRichLabelNode01_1.testField': '2018'}
        """
        result = []
        node_properties = self.get_eval_properties()
        for _prop_name, _prop in node_properties:
            if _prop.has_expression():
                _exp = _prop.get_expression
                _exp = re.sub(EVAL_GLOBALS['re_object_property_name'],
                              lambda p: self.make_object_property_full_name(p, self.properties.keys(),
                                                                            self.object_id), _exp)
                expression = {f'{self.object_id}.{_prop_name}': _exp}
                result.append(expression)
        return result

    def __str__(self):
        """String representation of the node"""
        return f'{self.object_id=}\n' + '\n'.join(f'\t\t{prop}' for prop in self.properties)
