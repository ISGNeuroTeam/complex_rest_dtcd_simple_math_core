import json
import logging
import re


class Eval:
    PROPERTY_TYPE = "expression"
    PLUGIN_NAME = "dtcd_simple_math_core"
    OBJECT_ID_COLUMN = "primitiveID"
    RE_OBJECT_PROPERTY_NAME = r"[\.\w]+"
    RE_NUMBERS = r"^\d+\.?\d*$"

    log = logging.getLogger(PLUGIN_NAME)

    @classmethod
    def filter_eval_properties(cls, _property):
        flag = _property[1]["type"] == cls.PROPERTY_TYPE and not _property[0].startswith("_")
        return flag

    @classmethod
    def make_object_property_full_name(cls, re_group, node_properties, node_id):
        name = re_group.group(0)
        if "." not in name and name in node_properties:
            name = ".".join((node_id, name))
        if re.fullmatch(cls.RE_NUMBERS, name) is None and '.' in name:
            name = f"'{name}'"
        return name

    @staticmethod
    def sort_eval_expressions(expr):
        return expr[""]

    @classmethod
    def make_expression(cls, cp_tuple, node_properties):
        column, _property, node_id = cp_tuple
        if _property['expression']:
            _exp = _property["expression"]
            _exp = re.sub(cls.RE_OBJECT_PROPERTY_NAME, lambda p: cls.make_object_property_full_name(p, node_properties,
                                                                                                    node_id), _exp)
            expression = f'eval \'{node_id}.{column}\' = {_exp}'
        else:
            expression = ''
        return expression

    @classmethod
    def from_graph(cls, graph):
        # graph = json.loads(graph)
        nodes = graph["graph"]["nodes"]
        cls.log.debug(f"Nodes: {nodes}")
        try:
            sorted_nodes = sorted(nodes, key=lambda n: int(n["properties"]["_operations_order"]["expression"]))
            cls.log.debug(f"Sorted nodes: {sorted_nodes}")
        except KeyError:
            raise Exception("Not all nodes have _operations_order property")
        eval_expressions = []
        for node in sorted_nodes:
            object_id = node[cls.OBJECT_ID_COLUMN]
            node_properties = node["properties"]
            node_eval_properties = filter(cls.filter_eval_properties, node_properties.items())
            node_eval_properties = map(lambda x: x + (object_id,), node_eval_properties)
            node_eval_expressions = list(filter(None, map(lambda p: cls.make_expression(p, node["properties"].keys()),
                                                          node_eval_properties)))
            eval_expressions += node_eval_expressions

        otl = ' | '.join(eval_expressions)

        return otl
