# -*- coding: utf-8 -*-
"""This module describes logic of analyzing and merging graph data
"""

import json
import logging
import re
import time
from typing import Dict, Union, List

from ..settings import GRAPH_GLOBALS, plugin_name, EVAL_GLOBALS
from .swt import SourceWideTable

from .node import Node
from .edges import Edge


class Graph:
    """This class describes how Graph works:

    Args:
        :: log: local instance of plugin logger
        :: nodes: dictionary of all nodes, consist of its names and its Node instances
        :: edges: list of all edges, consists of all port connections of nodes in graph
        :: name: name of current Graph
        :: dictionary: raw json object to keep, update and send back on api request
        :: swt_imported_tables: list of strings that represent names of the swt_tables
                                that are required to be imported
    """
    log: logging.Logger = logging.getLogger(plugin_name)
    nodes: Dict[str, Node]
    edges: List[Edge]
    name: str
    dictionary: Dict
    swt_import_tables: List[str]

    def __init__(self, name: str, graph: Union[Dict, str]):
        self.nodes = {}
        self.edges = []
        self.name = name
        self.dictionary = graph
        self.swt_import_tables = []

    def initialize(self) -> None:
        """Here we parse the graph if it was given as a string.
        And then parse all the nodes of the graph from json to nodes dictionary in order
        to keep them in Nodes objects.
        """
        self.log.debug('started initialization of graph')
        self.dictionary = json.loads(self.dictionary) if isinstance(self.dictionary, str) \
            else self.dictionary
        self.parse_nodes()
        self.parse_edges()
        self.parse_ports_of_nodes()

    def parse_nodes(self) -> None:
        """We parse graph from json into Nodes objects
        """
        self.log.debug('started parsing the nodes...')
        for node in self.dictionary['graph']['nodes']:
            self.nodes[node['primitiveID']] = Node(node.get('primitiveID', ''))
            self.nodes[node['primitiveID']].initialize(node)
            self.log.debug("parsed node %s", node['primitiveID'])
            # self.swt_import_tables.extend(self.nodes[node['primitiveID']].swt_imported_tables)
        self.log.debug('parsed nodes successfully...')

    def parse_edges(self) -> None:
        """We parse graph from json to get name connections of inPorts and outPorts
        It will be a dict of pairs: {targetPort: sourcePort}
        """
        self.log.debug('started parsing the edges...')
        for edge in self.dictionary['graph']['edges']:
            self.edges.append(Edge(edge))
        self.log.debug('parsed edges successfully...')

    def parse_ports_of_nodes(self):
        """Function to parse ports of the nodes

        As node has OUT or IN ports, and they may be getting data from another nodes
        we must do this in graph layer.

        Here we loop through edges to know where we take data and where we should put it."""
        # pylint: disable=line-too-long
        for edge in self.edges:
            # get outPort value
            node = self.nodes[edge.source_node]
            source_port_expression = node.get_port_expression_by_primitive_id(edge.sp)
            if '.' not in source_port_expression:
                source_port_expression = '.'.join([edge.source_node, source_port_expression])
            if re.fullmatch(EVAL_GLOBALS['re_numbers'],
                            source_port_expression) is None and '.' in source_port_expression:
                source_port_expression = f"{source_port_expression}"
            # change inPort value
            self.nodes[edge.target_node].change_import_expression_by_primitive_id(edge.target_port,
                                                                                  source_port_expression)

    def filtered_columns(self, swr: List) -> List:
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
        self.log.debug('started filtering columns at swr=%s', swr)
        result = list(filter(lambda c: not c.startswith("_"), swr))
        self.log.debug('result=%s', result)

        return result

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
        self.log.debug('getting the properties object of the %s node', object_id)
        nodes = self.dictionary['graph']['nodes']
        for node in nodes:
            if node['primitiveID'] == object_id:
                self.log.debug('properties object is found')
                return node['properties']

        self.log.debug('%s node is not found, returning empty dictionary...', object_id)
        return {}

    def update_property_at_graph(self, node_name: str, prop_name: str, parameter: str, value: Union[str, dict]) -> None:
        """Function to update given property with data

        Args:
            node_name: name of the node where to look for property
            prop_name: name of the property to update
            parameter: name of the parameter of the property to update
            value: actual value to set to property
        """
        self.log.debug('updating prop_name=%s of the %s node with value=%s...',
                       prop_name, node_name, value)
        properties = self.get_property_of_the_node_by_id(object_id=node_name)
        if prop_name in properties:
            if parameter in properties[prop_name].keys():
                properties[prop_name][parameter] = value
            else:
                properties[prop_name].update({parameter: value})
        else:
            properties[prop_name] = {parameter: value}
        self.log.debug('update successfully done...')

    def update(self, swr: List) -> Dict:
        """Function to update nodes objects and actual raw json dictionary

        Args:
            swr: the least row of the source wide table
        """
        # updating graph with data from otl
        self.log.debug('updating the graph...')
        self.log.debug('input: swr=%s', swr)
        for column in self.filtered_columns(swr=swr):
            # here we need to check if columns returned from calculations are present in graph
            if not self.graph_has_this(column):
                continue
            reg_exp = GRAPH_GLOBALS['re_object_id_and_property']
            object_id, object_property = re.match(reg_exp, column).groups()

            self.log.debug('from column=%s we have object_id=%s and object_property=%s',
                           column, object_id, object_property)

            try:
                self.nodes[object_id].update_property(object_property, swr[column])
                self.log.debug('updated property at the self.nodes dictionary')
                self.update_property_at_graph(node_name=object_id, prop_name=object_property,
                                              parameter='value', value=swr[column])
                self.log.debug('updated property at the self.graph dictionary')

            except KeyError:
                self.log.debug('No %s node found, only %s got', object_id, self.nodes.keys())

        # updating graph with data from self.nodes, especially _operations_order property
        for node in self.nodes:
            if '_operations_order' in self.get_properties_of_the_node_from_dictionary_by_id(node_name=node):
                continue
            self.update_property_at_graph(node_name=node, prop_name='_operations_order',
                                          parameter='expression',
                                          value=self.nodes[node].properties[
                                              '_operations_order'].get_expression)
            self.update_property_at_graph(node_name=node, prop_name='_operations_order',
                                          parameter='type',
                                          value=self.nodes[node].properties['_operations_order'].type)
            self.update_property_at_graph(node_name=node, prop_name='_operations_order',
                                          parameter='value',
                                          value=self.nodes[node].properties['_operations_order'].value)
            self.update_property_at_graph(node_name=node, prop_name='_operations_order',
                                          parameter='title',
                                          value=self.nodes[node].properties['_operations_order'].__dict__.get(
                                              "title", ""))
            self.update_property_at_graph(node_name=node, prop_name='_operations_order',
                                          parameter='status',
                                          value=self.nodes[node].properties['_operations_order'].status)

        return self.dictionary

    def get_properties_of_the_node_from_dictionary_by_id(self, node_name: str) -> Dict:
        node_list = self.dictionary['graph']['nodes']
        for node in node_list:
            if node['primitiveID'] == node_name:
                return node['properties']

    def graph_has_this(self, column: str) -> bool:
        """function to check if column is in graph, because some swt imported data is saved
        from external swt tables and are not present at current graph, and must not.

        Args:
            ::column: name of the column to check, for example: "SWTNode_44.exportedProperty"

        Result:
            True if column is at the graph, False otherwise
        """
        if '.' not in column:
            return False

        columns = column.split('.')
        if len(columns) != 2:
            return False
        node_name, prop_name = tuple(columns)
        return node_name in self.nodes and prop_name in self.nodes[node_name].properties

    def calc(self) -> Dict:
        """Main calculation function of Graph
        """
        self.log.debug('calculating graph...')
        swt = SourceWideTable(self.name)
        swt.initialize()
        nodes_eval_expressions = self.get_nodes_eval_expressions()
        self.log.debug('nodes_eval_expressions: %s', nodes_eval_expressions)
        list_of_sw_rows = swt.calc(nodes_eval_expressions, self.swt_import_tables)
        self.log.debug('list_of_sw_rows[-1]=%s', list_of_sw_rows[-1])

        row_of_swt = get_row_of_swt(list_of_sw_rows, GRAPH_GLOBALS['swt_line_index'])
        result = self.update(row_of_swt)
        return result

    def get_nodes_eval_expressions(self) -> List[Dict]:
        """Function to get all the eval expressions for all nodes and properties
        """
        self.log.debug('getting nodes eval expressions...')
        sorted_nodes = self.get_sorted_nodes()
        eval_expressions = []
        for node in sorted_nodes:
            evals, imported_columns = node.get_eval_expressions()
            self.swt_import_tables.extend(imported_columns)
            eval_expressions.extend(evals)
        self.log.debug('eval_expressions=%s', eval_expressions)
        return eval_expressions

    def get_sorted_nodes(self) -> list[Node]:
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
                            "expression": 100,        <<< this is what current property sorted by
                            "input": {
                                "component": "textarea"
                            }
        """
        self.log.debug('sorting the nodes by operations order...')
        try:
            result = sorted(self.nodes.values(),
                            key=lambda x: int(x.properties['_operations_order'].expression))
            self.log.debug('result=%s', result)
            return result

        except KeyError as error:
            raise Exception('Not all nodes have _operations_order property') from error

    def get_imported_data(self):
        ...

    def __str__(self) -> str:
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
        cls.log.debug('reading a graph %s at %s', filename, path)
        with open(path, encoding='utf-8') as file:
            return Graph(filename, file.read())


def get_row_of_swt(list_of_rows: List[Dict], swt_line_index: str) -> Dict:
    if swt_line_index == 'PREVIOUS_MONTH':
        current_time = int(time.time())

        # Create a list comprehension that filters out dictionaries with `_t` value
        # larger than or equal to the current time
        filtered_list = [d for d in list_of_rows if int(d['_t']) < current_time]

        # Find the dictionary with the highest `_t` value in the filtered list
        result = max(filtered_list, key=lambda d: d['_t'])
    else:  # if swt_line_index is 'LAST' or anything else we return latest row
        result = list_of_rows[-1]

    return result
