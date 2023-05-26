import json
import logging
import re

from dtcd_simple_math_core.settings import GRAPH_GLOBALS, connector, EVAL_GLOBALS, plugin_name
from dtcd_simple_math_core.translator.queries.query import Query

from dtcd_simple_math_core.translator.node import Node
from typing import Dict


class Graphy:
    log = logging.getLogger(plugin_name)

    def __init__(self, name, graph):
        self.nodes: Dict[str, Node] = {}
        self.name = name
        self.graph = json.loads(graph) if isinstance(graph, str) else graph
        self.parse_nodes()

    def get_dictionary(self):
        return self.__dict__

    @property
    def dictionary(self):
        return self.graph

    def parse_nodes(self):
        for node in self.graph['graph']['nodes']:
            self.nodes[node['primitiveID']] = Node(node)

    @staticmethod
    def filtered_columns(swr: []):
        return filter(lambda c: not c.startswith("_"), swr)

    def get_property_of_the_node_by_id(self, object_id):
        nodes = self.graph['graph']['nodes']
        for node in nodes:
            if node['primitiveID'] == object_id:
                return node['properties']

    def update_property_at_graph(self, object_id: str, _property: str, value: str) -> None:
        _properties = self.get_property_of_the_node_by_id(object_id=object_id)
        _properties[_property]['value'] = value

    def update(self, swr: []):
        for column in self.filtered_columns(swr=swr):
            object_id, object_property = re.match(GRAPH_GLOBALS['re_object_id_and_property'], column).groups()

            try:
                self.nodes[object_id].update_property(object_property, swr[column])
                self.update_property_at_graph(object_id=object_id, _property=object_property, value=swr[column])

            except KeyError:
                self.log.warning(f'No {object_id} node found, only {self.nodes.keys()} got')

        return self.graph

    def calc(self):
        otl_query = self.get_query()
        list_of_sw_rows = connector.create_query_job(otl_query)
        return self.update(list_of_sw_rows[-1])

    @classmethod
    def get_read_expression(cls, swt_name: str, last_row: bool = False, _path: str = "SWT",
                            _format: str = "JSON") -> str:
        cls.log.debug(f'input: {swt_name=}{" | last_row=" + str(last_row) if last_row else ""} | {_path=} | {_format=}')
        result = f'readFile format={_format} path={_path}/{swt_name}{" | tail 1" if last_row else ""}'
        cls.log.debug(f'result: {result}')
        return result

    @classmethod
    def get_write_expression(cls, swt_name: str, append: bool = False, _path: str = "SWT",
                             _format: str = "JSON") -> str:
        cls.log.debug(f'input: {swt_name=}{" | " + append if append else ""} | {_path=} | {_format=}')
        result = f'writeFile format={_format} {"mode=append " if append else ""}path={_path}/{swt_name}'
        cls.log.debug(f'result: {result}')
        return result

    def get_nodes_eval_expressions(self):
        sorted_nodes = self.get_sorted_nodes()
        eval_expressions = []
        for name, node in sorted_nodes.items():
            eval_expressions += node.get_eval_expressions(name)

        result = ' | '.join(eval_expressions)
        return result

    def get_query(self) -> str:
        read_query = self.get_read_expression(self.name)
        eval_query = self.get_nodes_eval_expressions()
        write_query = self.get_write_expression(self.name)

        # TODO fix the problem with overwriting or switch to append mode
        subquery = f"otloadjob otl={json.dumps(' | '.join((read_query, eval_query)))}"

        result = " | ".join((subquery, write_query))

        return result

    def get_sorted_nodes(self) -> dict:
        try:
            return dict(sorted(self.nodes.items(), key=lambda x: int(x[1].properties['_operations_order'].expression)))
        except KeyError:
            raise Exception('Not all nodes have _operations_order property')

    def __str__(self):
        return f'{self.name=}\n' + '\n'.join(f'\t{node}' for node in self.nodes)

    @classmethod
    def read_from_file(cls, filename: str):
        path = GRAPH_GLOBALS['path_to_graph'].format(filename)
        cls.log.debug(f'reading a graph {filename=} at {path=}')
        cls.log.debug(f'{path=}')
        with open(path) as fr:
            return Graphy(filename, fr.read())


def main():
    with open('budget.json', 'r') as f:
        graph = Graphy('budget', f.read())

    print(graph.get_nodes_eval_expressions())

    print('bye')


if __name__ == "__main__":
    main()
