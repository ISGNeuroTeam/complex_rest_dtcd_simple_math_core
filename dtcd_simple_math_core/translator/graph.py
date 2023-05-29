import json
import logging
import re

from ..settings import GRAPH_GLOBALS, plugin_name
from swt import SourceWideTable

from node import Node
from typing import Dict


class Graph:
    log = logging.getLogger(plugin_name)

    def __init__(self, name: str, graph: Dict):
        self.nodes: Dict[str, Node] = {}
        self.name = name
        self.dictionary = graph
        self.parse_nodes()

    def initialize(self) -> None:
        self.dictionary = json.loads(self.dictionary) if isinstance(self.dictionary, str) else self.dictionary
        self.parse_nodes()

    def parse_nodes(self) -> None:
        for node in self.dictionary['graph']['nodes']:
            self.nodes[node['primitiveID']] = Node(node)

    @staticmethod
    def filtered_columns(swr: []) -> []:
        return filter(lambda c: not c.startswith("_"), swr)

    def get_property_of_the_node_by_id(self, object_id: str) -> Dict:
        nodes = self.dictionary['graph']['nodes']
        for node in nodes:
            if node['primitiveID'] == object_id:
                return node['properties']

    def update_property_at_graph(self, object_id: str, _property: str, value: str) -> None:
        _properties = self.get_property_of_the_node_by_id(object_id=object_id)
        _properties[_property]['value'] = value

    def update(self, swr: []) -> Dict:
        for column in self.filtered_columns(swr=swr):
            object_id, object_property = re.match(GRAPH_GLOBALS['re_object_id_and_property'], column).groups()

            try:
                self.nodes[object_id].update_property(object_property, swr[column])
                self.update_property_at_graph(object_id=object_id, _property=object_property, value=swr[column])

            except KeyError:
                self.log.warning(f'No {object_id} node found, only {self.nodes.keys()} got')

        return self.dictionary

    def calc(self) -> Dict:
        swt = SourceWideTable(self.name)
        list_of_sw_rows = swt.calc(self.get_nodes_eval_expressions())
        return self.update(list_of_sw_rows[-1])

    def swt(self) -> Dict:
        swt = SourceWideTable(self.name)
        return swt.calc(self.get_nodes_eval_expressions())

    def get_nodes_eval_expressions(self) -> str:
        sorted_nodes = self.get_sorted_nodes()
        eval_expressions = []
        for name, node in sorted_nodes.items():
            eval_expressions += node.get_eval_expressions(name)
        return eval_expressions

    def get_sorted_nodes(self) -> dict:
        try:
            return dict(sorted(self.nodes.items(), key=lambda x: int(x[1].properties['_operations_order'].expression)))
        except KeyError:
            raise Exception('Not all nodes have _operations_order property')

    def __str__(self):
        return f'{self.name=}\n' + '\n'.join(f'\t{node}' for node in self.nodes)

    @classmethod
    def read_from_file(cls, filename: str) -> 'Graph':
        path = GRAPH_GLOBALS['path_to_graph'].format(filename)
        cls.log.debug(f'reading a graph {filename=} at {path=}')
        cls.log.debug(f'{path=}')
        with open(path) as fr:
            return Graph(filename, fr.read())


def main():
    with open('../graphs/budget.json', 'r') as f:
        graph = Graph('budget', f.read())

    print(graph.get_nodes_eval_expressions())

    print('bye')


if __name__ == "__main__":
    main()
