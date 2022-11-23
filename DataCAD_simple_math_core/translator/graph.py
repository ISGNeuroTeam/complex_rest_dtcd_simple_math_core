import json
import re


class Graph:

    OBJECT_ID_COLUMN = "primitiveID"
    RE_OBJECT_ID_AND_PROPERTY = r"(\w+)\.(\w+)"

    def __init__(self, graph):
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
        return json.dumps(self._graph)
