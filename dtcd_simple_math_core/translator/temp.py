import json
import logging

from dtcd_simple_math_core.translator.graph import Graph
from dtcd_simple_math_core.settings import plugin_name
from json_src import graph

with open("example_of_graph.json") as fr:
    file = fr.read()

logger = logging.getLogger(plugin_name)
_graph = Graph("example_of_swt", file)
Graph.path_to_graph = "./resources/graphs/{0}.json"
left = json.dumps(graph)
right = _graph.new_iteration()

print(f'left is{"" if left is right else " not"} equal to right')
