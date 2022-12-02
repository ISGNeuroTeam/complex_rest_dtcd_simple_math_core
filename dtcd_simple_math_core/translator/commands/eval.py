import json
import logging
import re

from translator.graph import Graph


class Eval:
    RE_IN_PORTS = r"inPort\d+"
    IN_PORT_TYPE = "IN"
    OUT_PORT_TYPE = "OUT"
    PROPERTY_TYPE = "expression"
    PLUGIN_NAME = "dtcd_simple_math_core"
    OBJECT_ID_COLUMN = "primitiveID"
    OBJECT_PORTS_KEY = "initPorts"
    RE_OBJECT_PROPERTY_NAME = r"[\.\w]+"
    RE_NUMBERS = r"^\d+\.?\d*$"

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

    def filter_port_by_id(cls, port, port_id):
        flag = port["primitiveID"] == port_id
        return flag

    @classmethod
    def get_port_id_by_name(cls, port_name, node_ports_in):
        filtered_ports = filter(lambda p: cls.filter_port_by_name(p, port_name), node_ports_in)
        port = next(filtered_ports)
        port_id = port["primitiveID"]
        return port_id

    @classmethod
    def get_port_by_id(cls, port_id, node_ports_in):
        filtered_ports = filter(lambda p: cls.filter_port_by_id(p, port_id), node_ports_in)
        port = next(filtered_ports)
        return port

    @classmethod
    def filter_edge_by_target_port(cls, port_id, edge):
        flag = edge["targetPort"] == port_id
        return flag

    @classmethod
    def get_edge_by_port_id(cls, port_id, edges):
        filtered_edges = filter(lambda e: cls.filter_edge_by_target_port(port_id, e), edges)
        edge = next(filtered_edges)
        return edge

    @classmethod
    def resolve_ports_in(cls, re_group, node_ports_in, edges, nodes):
        port_name = re_group.group(0)
        port_id = cls.get_port_id_by_name(port_name, node_ports_in)
        edge = cls.get_edge_by_port_id(port_id, edges)
        source_node_id = edge["sourceNode"]
        source_port_id = edge["sourcePort"]
        source_node = Graph.search_node_by_id(source_node_id, nodes)
        source_node_ports = source_node[cls.OBJECT_PORTS_KEY]
        source_node_out_ports = filter(cls.filter_out_ports, source_node_ports)
        source_node_out_port = cls.get_port_by_id(source_port_id, source_node_out_ports)
        source_node_out_port_expression = source_node_out_port["properties"][cls.PROPERTY_TYPE]

        # TODO Continue


    @staticmethod
    def sort_eval_expressions(expr):
        return expr[""]

    @classmethod
    def make_expression(cls, cp_tuple, node_properties, node_ports_in, edges, nodes):
        column, _property, node_id = cp_tuple
        if _property['expression']:
            _exp = _property["expression"]
            _exp = re.sub(cls.RE_IN_PORTS, lambda p: cls.resolve_ports_in(p, node_ports_in, edges, nodes), _exp)
            _exp = re.sub(cls.RE_OBJECT_PROPERTY_NAME, lambda p: cls.make_object_property_full_name(p, node_properties,
                                                                                                    node_id), _exp)
            expression = f'eval \'{node_id}.{column}\' = {_exp}'
        else:
            expression = ''
        return expression

    @classmethod
    def from_graph(cls, graph):
        nodes = graph["graph"]["nodes"]
        cls.log.debug(f"Nodes: {nodes}")
        edges = graph["graph"]["edges"]
        cls.log.debug(f"Edges: {edges}")
        try:
            sorted_nodes = sorted(nodes, key=lambda n: int(n["properties"]["_operations_order"]["expression"]))
            cls.log.debug(f"Sorted nodes: {sorted_nodes}")
        except KeyError:
            raise Exception("Not all nodes have _operations_order property")
        eval_expressions = []
        for node in sorted_nodes:
            object_id = node[cls.OBJECT_ID_COLUMN]

            node_ports_in = filter(cls.filter_in_ports, node[cls.OBJECT_PORTS_KEY])

            node_properties = node["properties"]
            node_eval_properties = filter(cls.filter_eval_properties, node_properties.items())
            node_eval_properties = map(lambda x: x + (object_id,), node_eval_properties)
            node_eval_expressions = list(filter(None, map(lambda p: cls.make_expression(p, node["properties"].keys(),
                                                                                        node_ports_in, edges, nodes),
                                                          node_eval_properties)))
            eval_expressions += node_eval_expressions

        otl = ' | '.join(eval_expressions)

        return otl
