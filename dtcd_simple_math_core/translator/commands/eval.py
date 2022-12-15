import json
import logging
import regex as re


class Eval:
    RE_IN_PORTS = r"inPort\d+"
    IN_PORT_TYPE = "IN"
    OUT_PORT_TYPE = "OUT"
    PROPERTY_TYPE = "expression"
    PLUGIN_NAME = "dtcd_simple_math_core"
    OBJECT_ID_COLUMN = "primitiveID"
    OBJECT_PORTS_KEY = "initPorts"
    RE_OBJECT_PROPERTY_NAME = r"""(?<=[^'\w\."]|^)([\w\.]+)(?=[^'\w\."]|$)+?"""
    RE_NUMBERS = r"^\d+\.?\d*$"

    DEFAULT_OPERATIONS_ORDER = 100

    log = logging.getLogger(PLUGIN_NAME)

    @classmethod
    def filter_eval_properties(cls, _property):
        flag = _property[1]["type"] == cls.PROPERTY_TYPE and not _property[0].startswith("_")
        return flag

    @classmethod
    def filter_in_ports(cls, _port):
        flag = _port["type"][0] == cls.IN_PORT_TYPE
        return flag

    @classmethod
    def filter_out_ports(cls, _port):
        flag = _port["type"][0] == cls.OUT_PORT_TYPE
        return flag

    @classmethod
    def make_object_property_full_name(cls, re_group, node_properties, node_id):
        name = re_group.group(0)
        if "." not in name and name in node_properties:
            name = ".".join((node_id, name))
        if re.fullmatch(cls.RE_NUMBERS, name) is None and '.' in name:
            name = f"'{name}'"
        return name

    @classmethod
    def filter_port_by_name(cls, port, name):
        flag = port["primitiveName"] == name
        return flag

    @classmethod
    def filter_port_by_id(cls, port, port_id):
        flag = port["primitiveID"] == port_id
        return flag

    @classmethod
    def get_port_id_by_name(cls, port_name, node_ports_in):
        node_ports_in = list(node_ports_in)
        filtered_ports = list(filter(lambda p: cls.filter_port_by_name(p, port_name), node_ports_in))
        port = filtered_ports[0]
        port_id = port["primitiveID"]
        return port_id

    @classmethod
    def get_port_by_id(cls, port_id, node_ports_in):
        filtered_ports = list(filter(lambda p: cls.filter_port_by_id(p, port_id), node_ports_in))
        port = filtered_ports[0]
        return port

    @classmethod
    def filter_edge_by_target_port(cls, port_id, edge):
        flag = edge["targetPort"] == port_id
        return flag

    @classmethod
    def get_edge_by_port_id(cls, port_id, edges):
        filtered_edges = list(filter(lambda e: cls.filter_edge_by_target_port(port_id, e), edges))
        edge = filtered_edges[0]
        return edge

    @classmethod
    def search_node_by_id(cls, nid, nodes):
        node = list(filter(lambda n: n[cls.OBJECT_ID_COLUMN] == nid, nodes))
        try:
            node = node[0]
        except IndexError:
            node = None
        return node

    @classmethod
    def resolve_ports_in(cls, re_group, node_ports_in, edges, nodes):
        port_name = re_group.group(0)
        port_id = cls.get_port_id_by_name(port_name, node_ports_in)
        edge = cls.get_edge_by_port_id(port_id, edges)
        source_node_id = edge["sourceNode"]
        source_port_id = edge["sourcePort"]
        source_node = cls.search_node_by_id(source_node_id, nodes)

        source_node_ports = source_node[cls.OBJECT_PORTS_KEY]
        source_node_out_ports = list(filter(cls.filter_out_ports, source_node_ports))
        source_node_out_port = cls.get_port_by_id(source_port_id, source_node_out_ports)
        source_node_out_port_expression = source_node_out_port["properties"]["status"]["expression"]

        if source_node_out_port_expression:
            source_node_out_port_expression = \
                re.sub(cls.RE_OBJECT_PROPERTY_NAME,
                       lambda p: cls.make_object_property_full_name(p, source_node["properties"], source_node_id),
                       source_node_out_port_expression)

        return source_node_out_port_expression

        # resolved_source_node = cls.preprocess_one_node(source_node, nodes, edges)
        # resolved_source_node_out_port_expression =\
        #     list(filter(lambda exp: f"{source_node_out_port_expression} =" in exp, resolved_source_node))
        #
        # if resolved_source_node_out_port_expression:
        #     return resolved_source_node_out_port_expression[0]
        # else:
        #     raise Exception(f"Port {port_id} wasn't resolved")

    @staticmethod
    def sort_eval_expressions(expr):
        return expr[""]

    @classmethod
    def make_expression(cls, cp_tuple, node_properties, node_ports_in, edges, nodes):
        cls.log.info(f"cp_tuple: {cp_tuple}")
        column, _property, node_id = cp_tuple
        if _property['expression']:
            _exp = _property["expression"]
            _exp = re.sub(cls.RE_IN_PORTS, lambda p: cls.resolve_ports_in(p, node_ports_in, edges, nodes), _exp)
            _exp = re.sub(cls.RE_OBJECT_PROPERTY_NAME, lambda p: cls.make_object_property_full_name(p, node_properties,
                                                                                                    node_id), _exp)
            expression = f'eval \'{node_id}.{column}\' = {_exp}'
        else:
            expression = ''
        cls.log.info(f"expression: {expression}")
        return expression

    @classmethod
    def preprocess_one_node(cls, node, nodes, edges):
        object_id = node[cls.OBJECT_ID_COLUMN]

        node_ports_in = list(filter(cls.filter_in_ports, node[cls.OBJECT_PORTS_KEY]))

        node_properties = node["properties"]
        node_eval_properties = list(filter(cls.filter_eval_properties, node_properties.items()))
        node_eval_properties = list(map(lambda x: x + (object_id,), node_eval_properties))
        cls.log.info(f"node_eval_properties: {node_eval_properties}")
        node_eval_expressions = list(filter(None, map(lambda p: cls.make_expression(p, node["properties"].keys(),
                                                                                    node_ports_in, edges, nodes),
                                                      node_eval_properties)))
        return node_eval_expressions

    @classmethod
    def sort_operations_order(cls, node):
        try:
            _operations_order = int(node["properties"]["_operations_order"]["expression"])
        except KeyError:
            _operations_order = cls.DEFAULT_OPERATIONS_ORDER
        return _operations_order

    @classmethod
    def preprocess_nodes_and_edges(cls, nodes, edges):
        sorted_nodes = sorted(nodes, key=cls.sort_operations_order)
        cls.log.debug(f"Sorted nodes: {sorted_nodes}")
        eval_expressions = []
        for node in sorted_nodes:
            cls.log.info(f"Node: {node}")
            node_eval_expressions = cls.preprocess_one_node(node, nodes, edges)
            eval_expressions += node_eval_expressions

        otl = ' | '.join(eval_expressions)
        return otl

    @classmethod
    def from_graph(cls, graph):
        nodes = graph["graph"]["nodes"]
        cls.log.debug(f"Nodes: {nodes}")
        edges = graph["graph"]["edges"]
        cls.log.debug(f"Edges: {edges}")
        otl = cls.preprocess_nodes_and_edges(nodes, edges)
        return otl
