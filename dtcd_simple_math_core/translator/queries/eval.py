import logging
import re

from dtcd_simple_math_core.settings import EVAL_GLOBALS


class EvalQuery:
    log = logging.getLogger(EVAL_GLOBALS['plugin_name'])

    @classmethod
    def filter_eval_properties(cls, _property):
        cls.log.debug(f'input: {_property=}')
        flag = _property[1]["type"] == EVAL_GLOBALS['property_type'] and not _property[0].startswith("_")
        cls.log.debug(f'result {flag}')
        return flag

    @classmethod
    def make_object_property_full_name(cls, re_group, node_properties, node_id):
        cls.log.debug(f'input: {re_group=} | {node_properties=} | {node_id=}')
        name = re_group.group(0)
        if "." not in name and name in node_properties:
            name = ".".join((node_id, name))
        if re.fullmatch(EVAL_GLOBALS['re_numbers'], name) is None and '.' in name:
            name = f"'{name}'"
        cls.log.debug(f'result: {name}')
        return name

    @staticmethod
    def sort_eval_expressions(expr):
        return expr[""]

    @classmethod
    def make_expression(cls, cp_tuple, node_properties):
        cls.log.debug(f'input: {cp_tuple=} | {node_properties=}')
        column, _property, node_id = cp_tuple
        if _property['expression']:
            _exp = _property["expression"]
            _exp = re.sub(EVAL_GLOBALS['re_object_property_name'],
                          lambda p: cls.make_object_property_full_name(p, node_properties, node_id), _exp)
            expression = f'eval \'{node_id}.{column}\' = {_exp}'
        else:
            expression = ''
        cls.log.debug(f'result: {expression}')
        return expression

    @classmethod
    def get_from_graph(cls, graph):
        nodes = graph["graph"]["nodes"]
        cls.log.debug(f'input graph: {graph=}')
        cls.log.debug(f"{nodes=}")
        try:
            sorted_nodes = sorted(nodes, key=lambda n: int(n["properties"]["_operations_order"]["expression"]))
            cls.log.debug(f"Sorted nodes: {sorted_nodes}")
        except KeyError:
            raise Exception("Not all nodes have _operations_order property")
        eval_expressions = []
        cls.log.debug(f'Looping through {sorted_nodes=}')
        for node in sorted_nodes:
            object_id = node[EVAL_GLOBALS['object_id_column']]
            node_properties = node["properties"]
            node_eval_properties = filter(cls.filter_eval_properties, node_properties.items())
            node_eval_properties = map(lambda x: x + (object_id,), node_eval_properties)
            node_eval_expressions = list(filter(None, map(lambda p: cls.make_expression(p, node["properties"].keys()),
                                                          node_eval_properties)))
            eval_expressions += node_eval_expressions

        otl = ' | '.join(eval_expressions)
        cls.log.debug(f'result: {otl}')

        return otl
