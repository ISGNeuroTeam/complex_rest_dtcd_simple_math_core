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

    @classmethod
    def make_expression(cls, cp_tuple, node_properties):
        eval_re = r"[\.\w]+"
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
    def get_from_graph(cls, nodes):
        # extract nodes from graph and save them to nodes variable
        cls.log.debug(f"input {nodes=}")
        # let's sort that nodes by its expressions,
        # by default they are digits saved as strings: `expression' = {str} '3'
        try:
            sorted_nodes = sorted(nodes, key=lambda n: int(n["properties"]["_operations_order"]["expression"]))
            cls.log.debug(f"Sorted nodes: {sorted_nodes}")
        except KeyError:
            raise Exception("Not all nodes have _operations_order property")
        # start creating evaluation expressions | make an empty list for it
        eval_expressions = []
        cls.log.debug(f'Looping through {sorted_nodes=}')
        # loop through nodes
        for node in sorted_nodes:
            # get object id from column with the name saved at EVAL_GLOBALS['object_id_column']
            # currently it is {str} 'primitiveID'
            primitive_id = node[EVAL_GLOBALS['object_id_column']]
            # get node properties
            node_properties = node["properties"]
            # now let's filter node properties by
            # if its type is equal to value saved at EVAL['property_type'], currently is 'expression'
            # and if its key is not started with '_' symbol
            node_eval_properties = list(filter(cls.filter_eval_properties, node_properties.items()))
            node_eval_properties = list(map(lambda x: x + (primitive_id,), node_eval_properties))
            node_eval_expressions = list(filter(None, map(lambda p: cls.make_expression(p, node["properties"].keys()),
                                                          node_eval_properties)))
            eval_expressions += node_eval_expressions

        otl = ' | '.join(eval_expressions)
        cls.log.debug(f'result: {otl}')

        return otl
