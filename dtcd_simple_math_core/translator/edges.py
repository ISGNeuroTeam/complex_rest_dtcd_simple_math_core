# -*- coding: utf-8 -*-
"""Module to work with Edge instance"""
from typing import Dict


class Edge:
    """Class to store information about edge.

    Args:
        :: source_port: name of the port of the source node, like 'Data_87_outPort1'
                        it is always must include `outPort` string
        :: source_node: name of the source node, like 'Data_87'
        :: target_port: name of the port of the target node, like 'Calc2_96_inPort1'
                        it is always must include `inPort` string
        :: target_node: name of the target node, like 'Calc2_96'
    """
    # pylint: disable=too-few-public-methods
    source_port: str
    source_node: str
    target_port: str
    target_node: str

    def __init__(self, data: Dict):
        self.source_node = data['sourceNode']
        self.source_port = data['sourcePort']
        self.target_node = data['targetNode']
        self.target_port = data['targetPort']

    @property
    def sp(self):
        """short wrapper of the source_port parameter"""
        return self.source_port
