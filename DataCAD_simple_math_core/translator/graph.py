import json
import re

from DataCAD_simple_math_core.translator.swt import SourceWideTable


class Graph:

    OBJECT_ID_COLUMN = "primitiveID"
    RE_OBJECT_ID_AND_PROPERTY = r"(\w+)\.(\w+)"
    PATH_TO_GRAPH = "./plugins/DataCAD_simple_math_core/graphs/{0}.json"

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

    def search_node_by_id(self, nid):
        nodes = self.graph_dict["graph"]["nodes"]
        node = filter(lambda n: n[self.OBJECT_ID_COLUMN] == nid, nodes)
        node = list(node)[0]
        return node

    def update(self, swt_line):
        filtered_columns = filter(lambda c: not c.startswith("_"), swt_line)
        for column in filtered_columns:
            object_id, object_property = re.match(self.RE_OBJECT_ID_AND_PROPERTY, column).groups()
            node = self.search_node_by_id(object_id)
            _property = node["properties"][object_property]
            _property["value"] = swt_line[column]

        self.graph_string = json.dumps(self.graph_dict)
        return self.graph_string

    def new_iteration(self):
        swt = SourceWideTable(self.swt_name)
        swt = swt.new_iteration(self.graph_dict)
        swt_last_line = swt[-1]
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
