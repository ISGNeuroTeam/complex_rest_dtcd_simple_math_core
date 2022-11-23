import json
import logging
import re


class Eval:
    PROPERTY_TYPE = "expression"
    PLUGIN_NAME = "DataCAD_simple_math_core"
    OBJECT_ID_COLUMN = "primitiveID"
    RE_OBJECT_PROPERTY_NAME = r"[\.\w]+"
    OBJECT_ID = "__OBJECT_ID__"

    log = logging.getLogger(PLUGIN_NAME)

    @classmethod
    def filter_eval_properties(cls, _property):
        flag = _property[1]["type"] == cls.PROPERTY_TYPE and not _property[0].startswith("_")
        return flag

    @classmethod
    def make_object_property_full_name(cls, re_group):
        name = re_group.group(0)
        if "." not in name:
            name = ".".join((cls.OBJECT_ID, name))
        name = f"'{name}'"
        return name

    @staticmethod
    def sort_eval_expressions(expr):
        return expr[""]

    @classmethod
    def make_expression(cls, cp_tuple):
        column, _property, node_id = cp_tuple
        if _property['expression']:
            _exp = _property["expression"].strip("\"")
            _exp = re.sub(cls.RE_OBJECT_PROPERTY_NAME, cls.make_object_property_full_name, _exp)
            _exp = _exp.replace(cls.OBJECT_ID, node_id)
            expression = f'eval \'{node_id}.{column}\' = {_exp}'
        else:
            expression = ''
        return expression

    @classmethod
    def from_graph(cls, graph):
        graph = json.loads(graph)
        nodes = graph["graph"]["nodes"]
        cls.log.debug(f"Nodes: {nodes}")
        sorted_nodes = sorted(nodes, key=lambda n: int(n["properties"]["_operations_order"]["value"]))
        cls.log.debug(f"Sorted nodes: {sorted_nodes}")
        eval_expressions = []
        for node in sorted_nodes:
            object_id = node[cls.OBJECT_ID_COLUMN]
            node_properties = node["properties"]
            node_eval_properties = filter(cls.filter_eval_properties, node_properties.items())
            node_eval_properties = map(lambda x: x + (object_id,), node_eval_properties)
            node_eval_expressions = list(filter(None, map(cls.make_expression, node_eval_properties)))
            eval_expressions += node_eval_expressions

        otl = ' | '.join(eval_expressions)

        return otl
