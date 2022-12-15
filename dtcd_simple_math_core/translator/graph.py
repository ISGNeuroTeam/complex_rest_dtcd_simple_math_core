import json
import re
import logging

from dtcd_simple_math_core.translator.swt import SourceWideTable


class Graph:
    PLUGIN_NAME = "dtcd_simple_math_core"
    log = logging.getLogger(PLUGIN_NAME)
    OBJECT_ID_COLUMN = "primitiveID"
    RE_OBJECT_ID_AND_PROPERTY = r"(\w+)\.(\w+)"
    PATH_TO_GRAPH = "./plugins/dtcd_simple_math_core/graphs/{0}.json"

    DEFAULT_OPERATIONS_ORDER = 100

    def __init__(self, swt_name, graph_string=None, graph_dict=None):
        self.swt_name = swt_name
        if graph_string is not None:
            self.graph_string = graph_string
            self.graph_dict = json.loads(graph_string)
        elif graph_dict is not None:
            self.graph_dict = graph_dict
            self.graph_string = json.dumps(graph_dict)
        else:
            raise Exception("Can`t load graph")

    @classmethod
    def search_node_by_id(cls, nid, nodes):
        node = filter(lambda n: n[cls.OBJECT_ID_COLUMN] == nid, nodes)
        try:
            node = list(node)[0]
        except IndexError:
            node = None
        return node

    def _search_node_by_id(self, nid):
        nodes = self.graph_dict["graph"]["nodes"]
        node = self.search_node_by_id(nid, nodes)
        return node

    def update(self, swt_line):
        self.log.debug(f"swt_line: {swt_line}")
        filtered_columns = filter(lambda c: not c.startswith("_"), swt_line)
        for column in filtered_columns:
            object_id, object_property = re.match(self.RE_OBJECT_ID_AND_PROPERTY, column).groups()
            self.log.debug(f"object_id: {object_id}, object_property: {object_property}")
            node = self._search_node_by_id(object_id)
            if node is not None and object_property in node["properties"]:
                self.log.debug(f"node: {node}")
                _property = node["properties"][object_property]
                _property["value"] = swt_line[column]
                _property["status"] = "complete"
                self.log.debug(f"_property: {_property}")
                if "_operations_order" in node["properties"]:
                    node["properties"]["_operations_order"]["value"] = node["properties"]["_operations_order"][
                        "expression"]
                    node["properties"]["_operations_order"]["status"] = "complete"
                    self.log.debug(f"Updated _operations_order: {node['properties']['_operations_order']}")
                else:
                    node["properties"]["_operations_order"] = {}
                    node["properties"]["_operations_order"]["value"] = self.DEFAULT_OPERATIONS_ORDER
                    node["properties"]["_operations_order"]["status"] = "complete"
                    node["properties"]["_operations_order"]["type"] = "expression"
                    node["properties"]["_operations_order"]["expression"] = self.DEFAULT_OPERATIONS_ORDER
                    node["properties"]["_operations_order"]["input"] = {"component": "textarea"}
                    self.log.debug(f"Created _operations_order: {node['properties']['_operations_order']}")
            else:
                self.log.warning(f"Object property {object_id}.{object_property} from SWT is absent in the graph")
            # TODO move graph key names to external shared object between math core classes

        self.graph_string = json.dumps(self.graph_dict)
        return self.graph_string

    def new_iteration(self):
        swt = SourceWideTable(self.swt_name)
        swt = swt.new_iteration(self.graph_dict)
        swt_last_line = swt[-1]
        self.log.info(f"swt_last_line: {swt_last_line}")
        return self.update(swt_last_line)

    def save(self):
        path = self.PATH_TO_GRAPH.format(self.swt_name)
        with open(path, 'w') as fw:
            fw.write(self.graph_string)

    @classmethod
    def read(cls, swt_name):
        path = cls.PATH_TO_GRAPH.format(swt_name)
        with open(path) as fr:
            return Graph(swt_name, fr.read())
