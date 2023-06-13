# -*- coding: utf-8 -*-
"""
This module describes logic of analyzing and merging graph data
"""

import json
import logging
import re

from ..settings import GRAPH_GLOBALS, plugin_name
from .swt import SourceWideTable

from .node import Node
from typing import Dict, Union


class Graph:
    """
    This class describes how Graph works:
    Args:
        :: log: local instance of plugin logger
        :: nodes: dictionary of all nodes, consist of its names and its Node instances
        :: name: name of current Graph
        :: dictionary: raw json object to keep, update and send back on api request
    """
    log: logging.Logger = logging.getLogger(plugin_name)
    nodes: Dict[str, Node]
    name: str
    dictionary: Union[Dict, str]

    def __init__(self, name: str, graph: Union[Dict, str]):
        self.nodes = {}
        self.name = name
        self.dictionary = graph

    def initialize(self) -> None:
        """Here we parse the graph if it was given as a string.
        And then parse all the nodes of the graph from json to nodes dictionary in order
        to keep them in Nodes objects.
        """
        self.log.debug(f'started initialization of graph')
        self.dictionary = json.loads(self.dictionary) if isinstance(self.dictionary, str) \
            else self.dictionary
        self.parse_nodes()

    def parse_nodes(self) -> None:
        """We parse graph from json into Nodes objects
        """
        self.log.debug(f'started parsing the nodes...')
        for node in self.dictionary['graph']['nodes']:
            self.nodes[node['primitiveID']] = Node(node)
        self.log.debug(f'parsed nodes successfully...')

    def filtered_columns(self, swr: []) -> []:
        """We get a row of the source wide table which is "Source Wide Row" >>> swr 
        and filter out all strings that start with "_" symbol

        Args: 
            swr: list of strings to filter

        Returns:
            list of filtered strings

        Example:
            input: swr = ['test', 'row', '_operations_order', '_size']
            output: ['test', 'row']
        """
        self.log.debug(f'started filtering columns at {swr=}')
        return filter(lambda c: not c.startswith("_"), swr)

    def get_property_of_the_node_by_id(self, object_id: str) -> Dict:
        """This function gets the actual property object out of saved raw json Graph
        by its 'primitiveID'

        It is required for its' further update

        Args:
            object_id: name of the object to find and return
        
        Return:
            dictionary with data of the object with name object_id found
            in raw json dictionary of the Graph

        TODO:
            * it seems that here we haven't checked the situation when object is not found
              this is actually impossible because we check if we have this object in graph 
              before using this function.
        """
        self.log.debug(f'getting the properties object of the {object_id} node')
        nodes = self.dictionary['graph']['nodes']
        for node in nodes:
            if node['primitiveID'] == object_id:
                self.log.debug(f'properties object is found')
                return node['properties']

        self.log.warning(f'{object_id} node is not found, returning empty dictionary...')
        return {}

    def update_property_at_graph(self, node_name: str, prop_name: str, value: str) -> None:
        """Function to update given property with data

        Args:
            node_name: name of the node where to look for property
            prop_name: name of the property to update
            value: actual value to set to property
        """
        self.log.debug(f'updating {prop_name=} of the {node_name} node with {value=}...')
        properties = self.get_property_of_the_node_by_id(object_id=node_name)
        properties[prop_name]['value'] = value
        self.log.debug(f'update successfully done...')

    def update(self, swr: []) -> Dict:
        """Function to update nodes objects and actual raw json dictionary

        Args: 
            swr: the least row of the source wide table
        """
        self.log.debug(f'updating the graph...')
        self.log.debug(f'input: {swr=}')
        for column in self.filtered_columns(swr=swr):
            reg_exp = GRAPH_GLOBALS['re_object_id_and_property']
            object_id, object_property = re.match(reg_exp, column).groups()
            
            self.log.debug(f'from {column=} we have {object_id=} and {object_property=}')

            try:
                self.nodes[object_id].update_property(object_property, swr[column])
                self.log.debug(f'updated property at the self.nodes dictionary')
                self.update_property_at_graph(node_name=object_id, prop_name=object_property,
                                              value=swr[column])
                self.log.debug(f'updated property at the self.graph dictionary')

            except KeyError:
                self.log.warning(f'No {object_id} node found, only {self.nodes.keys()} got')

        return self.dictionary

    def calc(self) -> Dict:
        """Main calculation function of Graph
        """
        self.log.debug(f'calculating graph...')
        swt = SourceWideTable(self.name)
        list_of_sw_rows = swt.calc(self.get_nodes_eval_expressions())
        self.log.debug(f'{list_of_sw_rows[-1]=}')
        return self.update(list_of_sw_rows[-1])

    def swt(self) -> Dict:
        """Function to get the whole source wide table
        """
        self.log.debug(f'getting swt...')
        swt = SourceWideTable(self.name)
        return swt.calc(self.get_nodes_eval_expressions())

    def get_nodes_eval_expressions(self) -> str:
        """Function to get all the eval expressions for all nodes and properties
        """
        self.log.debug(f'getting nodes eval expressions...')
        sorted_nodes = self.get_sorted_nodes()
        eval_expressions = []
        for node in sorted_nodes:
            eval_expressions += node.get_eval_expressions()
        self.log.debug(f'{eval_expressions=}')
        return eval_expressions

    def get_sorted_nodes(self) -> dict:
        """Function to get the dictionary of all nodes sorted by their _operations_order
        and name

        Example:
            "nodes": [
                {
                    "primitiveID": "Data_685",
                    "primitiveName": "Data",
                    "properties": {
                        "type": {...},
                        "name": {...},
                        "description": {...},
                        "_operations_order": {        <<< this property is used
                            "status": "complete",
                            "type": "expression",
                            "expression": 100,        <<< this is expression sorted by
                            "input": {
                                "component": "textarea"
                            }
        """
        self.log.debug(f'sorting the nodes by operations order...')
        try:
            return sorted(self.nodes.values(),
                          key=lambda x: int(x.properties['_operations_order'].expression))
        except KeyError:
            raise Exception('Not all nodes have _operations_order property')

    def __str__(self):
        """Simple string representation of the Graph object
        """
        return f'{self.name=}\n' + '\n'.join(f'\t{node}' for node in self.nodes)

    @classmethod
    def read_from_file(cls, filename: str) -> 'Graph':
        """Function to read Graph from file on disk

        Args: 
            filename: name of the file to read

        Returns:
            Function returns already parsed Graph object of the json read from file.
        """
        path = GRAPH_GLOBALS['path_to_graph'].format(filename)
        cls.log.debug(f'reading a graph {filename=} at {path=}')
        with open(path) as fr:
            return Graph(filename, fr.read())
