# -*- coding: utf-8 -*-
"""This module describes logic of working with Node objects.
"""
import logging
import re
from typing import Dict, Any, Iterable, Tuple, List

from .properties import Property
from .ports import Port
from ..settings import EVAL_GLOBALS, plugin_name


class Node:
    """This class describes how Node works

    Args:
        :: object_id: name of the node
        :: properties: dictionary of the properties Node has
        :: ports: list of the ports Node has
        :: log: local instance of plugin logger
    """
    object_id: str
    properties: Dict[str, Property]
    ports: Dict[str, Port]
    log: logging.Logger = logging.getLogger(plugin_name)
    has_swt_import: bool

    def __init__(self, name: str):
        self.object_id = name
        self.properties = {}
        self.ports = {}

    def initialize(self, node: Dict):
        """here we parse the node data"""
        # init properties
        for prop_name, data in node['properties'].items():
            self.fill_default_properties(prop_name, data=data)
        if '_operations_order' not in self.properties:
            self.fill_default_properties('_operations_order', {'expression': 100})

        # init ports
        for data in node['initPorts']:
            self.fill_default_ports(data=data)

    @property
    def swt_imported_tables(self):
        result = []
        for prop_data in self.properties.values():
            if prop_data.type == "SWT" or prop_data.type == "SWTexp":
                result.append(prop_data.swt_import.swt_name)
        return result

    def fill_default_properties(self, name: str, data: Dict) -> None:
        """Here we save the empty (or not) Property instance as a value of the name key
        of the properties' dictionary.
        Args:
              :: name: name of the property to save
              :: data: dictionary of the data we need to save according to the named property.
        """
        self.log.debug('saving %s property with %s', name, data)
        self.properties[name] = Property(**data)
        self.properties[name].initialize()

    def fill_default_ports(self, data: Dict) -> None:
        """Here we save Port instance as a value of the name key of the 'IN' ports dictionary

        Args:
            :: data: dictionary of the data to save according to the name of the port
            """
        self.log.debug('saving port with %s', data)
        self.ports[data['primitiveID']] = Port(data)

    def get_port_expression_by_primitive_id(self, primitive_id: str) -> str:
        """Function to get expression of the port.

        Args:
            :: primitive_id: primitiveID name of the port

        Returns:
            :: expression of the port instance
        """
        for port in self.ports.values():
            if primitive_id == port.primitive_id:
                return port.expression
        return ''

    def change_import_expression_by_primitive_id(self, primitive_id: str,
                                                 source_expression: str) -> None:
        """Function to change import_expression of the property. It is required because
        we must save it for future query generating without changing the actual expression
        of the property

            Args:
                :: primitive_id: primitiveID value of the port
                :: source_expression: actual expression of the imported data
                                      to be calculated at the property
        """
        for port in self.ports.values():
            if primitive_id == port.primitive_id:
                for prop_data in self.properties.values():
                    if prop_data.has_import and port.primitive_name in prop_data.imports:
                        prop_data.replace_import_expression(port.primitive_name, source_expression)

    def update_property(self, prop_name: str, value: Any) -> None:
        """Here we update the property with prop_name with its value
        and also update _operations_order's expression to "complete",
        if we have such property saved.
        """
        self.log.debug('updating %s property with value=%s', prop_name, value)
        try:
            self.properties[prop_name].update(value, "complete")
            # pylint: disable=line-too-long
            self.properties['_operations_order'].update(self.properties['_operations_order'].expression, "complete")
        except KeyError:
            self.log.warning('no %s property found, only %s got', prop_name, self.properties.keys())

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
        cls.log.debug('checking if property %s is valid for evaluation', prop[0])
        cls.log.debug('its type is %s and required is %s', prop[1].type,
                      EVAL_GLOBALS["property_type"])

        result = prop[1].type in [EVAL_GLOBALS['property_type'], 'SWT', 'SWTexp'] and not prop[0].startswith("_")
        cls.log.debug('result=%s', result)

        return result

    def get_eval_properties(self) -> List[Tuple[str, Property]]:
        """Function takes all properties saved and return the ones that satisfy filter conditions
        described in filter_eval_properties functions

        Returns:
            list of tuples with names and dictionaries of properties that do satisfy
            that conditions
        """
        self.log.debug('Getting eval properties...')
        result = list(filter(self.filter_eval_properties, self.properties.items()))
        self.log.debug('result=%s', result)

        return result

    @classmethod
    def make_obj_prop_full_name(cls, re_group: re.Match, node_properties: Iterable,
                                node_id: str) -> str:
        """
        Here we make several manipulations and checks in order to create proper object
        property names.

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
        cls.log.debug('making a %s node property full name for %s and '
                      'node_properties=%s', node_id, name, node_properties)
        if "." not in name and name in node_properties:
            name = ".".join((node_id, name))

        # here we must make this 'StepRichLabelNode11_1.Enabled'
        # look like this "'StepRichLabelNode11_1.Enabled'"
        if re.fullmatch(EVAL_GLOBALS['re_numbers'], name) is None and '.' in name \
                and not name.startswith("'") and not name.endswith("'"):
            name = f"'{name}'"
        cls.log.debug('result=%s', name)

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
        self.log.debug('Getting all eval expressions for %s node', self.object_id)

        result = []
        node_properties = self.get_eval_properties()

        for _prop_name, _prop in node_properties:
            if _prop.has_expression():
                if _prop.is_float_or_int:
                    _exp = _prop.expression
                else:
                    if _prop.has_import:
                        _exp = _prop.import_expression
                    elif _prop.has_swt_import:
                        _exp = f"{self.object_id}.{_prop.swt_import.column}"
                    else:
                        _exp = _prop.get_expression

                    if not _exp.startswith('"') and not _exp.endswith('"'):
                        _exp = re.sub(EVAL_GLOBALS['re_object_property_name'],
                                      lambda p: self.make_obj_prop_full_name(p,
                                                                             self.properties.keys(),
                                                                             self.object_id), _exp)

                expression = {f'{self.object_id}.{_prop_name}': _exp}
                result.append(expression)
        self.log.debug('result=%s', result)

        return result

    def __str__(self):
        """String representation of the node"""
        return f'{self.object_id=}\n' + '\n'.join(f'\t\t{prop}' for prop in self.properties)
