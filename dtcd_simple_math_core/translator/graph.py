import json
import re
import logging

from dtcd_simple_math_core.translator.swt import SourceWideTable
from dtcd_simple_math_core.settings import GRAPH_GLOBALS, plugin_name, GRAPH_KEY_NAMES as GK
from dtcd_simple_math_core.translator.node import Node


class Graph:
    log = logging.getLogger(plugin_name)
    nodes: [Node]

    def __init__(self, swt_name, graph_string=None, graph_dict=None):
        self.log.debug(f'input: {swt_name=} | {graph_string=} | {graph_dict=}')
        self.swt_name = swt_name
        if graph_string:
            self.graph_string = graph_string
            self.graph_dict = json.loads(graph_string)
            self.log.debug(f'we have graph_string, so {graph_dict=}')
        elif graph_dict:
            self.graph_dict = graph_dict
            self.graph_string = json.dumps(graph_dict)
            self.log.debug(f'we have graph_string, so {graph_string=}')
        else:
            raise Exception("Can`t load graph, no graph_string or graph_dict provided.")

    def parse_nodes(self, graph: []):
        for node in graph['graph']['nodes']:
            self.nodes.append(Node(node))

    def get_node_by_id(self, nid):
        self.log.debug(f'input: {nid=}')
        nodes = self.graph_dict["graph"]["nodes"]
        node = next(filter(lambda n: n[GRAPH_GLOBALS['object_id_column']] == nid, nodes), None)
        self.log.debug(f'result: {node=}')
        return node

    @staticmethod
    def filtered_columns(swr: []):
        return filter(lambda c: not c.startswith("_"), swr)

    @staticmethod
    def get_property(self, node: [], object_property: str):
        return node["properties"][object_property]

    def update_property(self, node: [], object_property: str, object_id: str, result: []):
        _property = self.get_property(node=node, object_property=object_property)
        _property["value"] = result[f'{object_id}.{object_property}']
        _property["status"] = GK['status_complete']
        self.log.debug(f"_property: {_property}")

    def update_node(self, object_id: str, object_property: str, result: []):
        node = self.get_node_by_id(object_id)
        if node is None or object_property not in node['properties']:
            self.log.warning(f"Object property {object_id}.{object_property} from SWT is absent in the graph")
            return

        # update property
        self.update_property(node=node, object_property=object_property, object_id=object_id, result=result)
        # update _operations_order property
        # if we have 17 properties updated per one node, then this code will be repeated 17 times
        node["properties"][GK['ops_order']]["value"] = node["properties"][GK['ops_order']]["expression"]
        node["properties"][GK['ops_order']]["status"] = GK['status_complete']

    def update(self, swt_line):
        self.log.debug(f"input: {swt_line=}")

        for column in self.filtered_columns(swr=swt_line):
            object_id, object_property = re.match(GRAPH_GLOBALS['re_object_id_and_property'], column).groups()

            self.update_node(object_id=object_id, object_property=object_property, result=swt_line)

        self.graph_string = json.dumps(self.graph_dict)
        self.log.debug(f"result: {self.graph_string=}")
        return self.graph_string

    @staticmethod
    def get_last_line_of(_swt: list) -> []:
        return _swt[-1]

    def new_iteration(self):
        self.log.debug(f'starting a new graph iteration...')
        swt = SourceWideTable(self.swt_name)
        swt = swt.new_iteration(self.graph_dict)
        swt_last_line = self.get_last_line_of(swt)
        self.log.debug(f'result: {swt_last_line=}')
        return self.update(swt_last_line)

    def save(self):
        self.log.debug(f'saving a graph...')
        path = GRAPH_GLOBALS['path_to_graph'].format(self.swt_name)
        self.log.debug(f'{path=}')
        with open(path, 'w') as fw:
            fw.write(self.graph_string)

    @classmethod
    def read(cls, swt_name):
        cls.log.debug(f'reading a graph {swt_name=}')
        path = GRAPH_GLOBALS['path_to_graph'].format(swt_name)
        cls.log.debug(f'{path=}')
        with open(path) as fr:
            return Graph(swt_name, fr.read())
