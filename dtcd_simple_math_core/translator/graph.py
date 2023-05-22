import json
import re
import logging

from dtcd_simple_math_core.translator.swt import SourceWideTable
from dtcd_simple_math_core.settings import GRAPH_GLOBALS, plugin_name, GRAPH_KEY_NAMES as GK


class Graph:
    log = logging.getLogger(plugin_name)

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

    def get_node_by_id(self, nid):
        self.log.debug(f'input: {nid=}')
        nodes = self.graph_dict["graph"]["nodes"]
        node = next(filter(lambda n: n[GRAPH_GLOBALS['object_id_column']] == nid, nodes), None)
        self.log.debug(f'result: {node=}')
        return node

    def update(self, swt_line):
        self.log.debug(f"input: {swt_line=}")
        filtered_columns = filter(lambda c: not c.startswith("_"), swt_line)
        for column in filtered_columns:
            object_id, object_property = re.match(GRAPH_GLOBALS['re_object_id_and_property'], column).groups()

            node = self.get_node_by_id(object_id)
            if node is not None and object_property in node["properties"]:
                _property = node["properties"][object_property]
                _property["value"] = swt_line[column]
                _property["status"] = "complete"
                self.log.debug(f"_property: {_property}")
                node["properties"][GK['ops_order']]["value"] = node["properties"][GK['ops_order']]["expression"]
                node["properties"][GK['ops_order']]["status"] = GK['status_complete']
            else:
                self.log.warning(f"Object property {object_id}.{object_property} from SWT is absent in the graph")

        self.graph_string = json.dumps(self.graph_dict)
        self.log.debug(f"result: {self.graph_string=}")
        return self.graph_string

    def new_iteration(self):
        self.log.debug(f'starting a new graph iteration...')
        swt = SourceWideTable(self.swt_name)
        swt = swt.new_iteration(self.graph_dict)
        swt_last_line = swt[-1]
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
