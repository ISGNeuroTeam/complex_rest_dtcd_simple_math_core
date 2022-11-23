import json
import re

from translator.swt import SourceWideTable


class Graph:

    OBJECT_ID_COLUMN = "primitiveID"
    RE_OBJECT_ID_AND_PROPERTY = r"(\w+)\.(\w+)"
    PATH_TO_GRAPH = "./graphs/{0}.json"

    def __init__(self, graph, swt_name):
        self.swt_name = swt_name
        self.graph = graph
        self._graph = json.loads(graph)

    def search_node_by_id(self, nid):
        nodes = self._graph["graph"]["nodes"]
        node = filter(lambda n: n[self.OBJECT_ID_COLUMN] == nid, nodes)
        node = list(node)[0]
        return node

    def update(self, swt_line):
        columns = json.loads(swt_line)
        filtered_columns = filter(lambda c: not c.startswith("_"), columns)
        for column in filtered_columns:
            object_id, object_property = re.match(self.RE_OBJECT_ID_AND_PROPERTY, column).groups()
            node = self.search_node_by_id(object_id)
            _property = node["properties"][object_property]
            _property["value"] = columns[column]

        self.graph = json.dumps(self._graph)
        return self.graph

    def new_iteration(self):
        swt = SourceWideTable(self.swt_name)
        swt = swt.new_iteration(self.graph)
        swt_last_line = swt[-1]
        return self.update(swt_last_line)

    def save(self):
        path = self.PATH_TO_GRAPH.format(self.swt_name)
        with open(path, 'w') as fw:
            fw.write(self.graph)

    @classmethod
    def read(cls, swt_name):
        path = cls.PATH_TO_GRAPH.format(swt_name)
        with open(path) as fr:
            return Graph(fr.read(), swt_name)
