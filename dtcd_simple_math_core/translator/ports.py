# -*- coding: utf-8 -*-
"""This module stored information about how to work with ports"""
import logging
from typing import Dict

from ..settings import plugin_name


class Port:
    """this is how port look like

    {
              "primitiveName": "inPort1",  << short name of the port of the current node
              "type": ["IN"],
              "properties": {
                "status": {
                  "title": "",
                  "type": "expression",
                  "expression": "",
                  "input": {"component": "textarea"},
                  "status": "inProgress",
                  "value": ""
                }
              },
              "primitiveID": "Calc2_96_inPort1",  << this is the name, by which we will look the out
                                                     port to get data from
              "location": {"x": 370.55, "y": 204.5}
            },

            so, if node has an expression: 'inPort1 + inPort2`
            we must get its primitiveIds
            - find its targetPort names
            - find targetPortName expression and save it to its source values
            so
            - inPort1 >>> Calc2_96_inPort1 >>> Data1_12_outPort1 >>> '2000`
            - inPort2 >>> Calc2_96_inPort2 >>> Data1_12_outPort2 >>> '100`
            - inPort1 + inPort2 >>> Data1_12_outPort1 + Data1_12_outPort2 >>> all the rest will otl do

        Args:
            :: primitiveName: short name of the port in terms of the Node, like 'outPort1'
            :: primitiveID: full name of the port in terms of the Graph, like 'Data1_12_outPort1'
            :: type: type of the port, like 'IN' or 'OUT'
            :: expression: value of properties.status.expression to import to target port
            :: log: local logger instance
    """
    primitiveName: str
    primitiveID: str
    type: str
    expression: str
    log: logging.Logger = logging.getLogger(plugin_name)

    def __init__(self, data: Dict):
        self.primitiveName = data['primitiveName']
        self.primitiveID = data['primitiveID']
        self.type = data['type'][0] if 'type' in data.keys() and len(data['type']) > 0 else ''
        self.expression = data['properties']['status']['expression']
        self.log.debug('port saved: %s' % self)


    @property
    def is_in_type(self):
        return self.type == 'IN'

    @property
    def is_out_type(self):
        return self.type == 'OUT'

    def __str__(self):
        return f'{self.primitiveID=} | {self.primitiveName=} | {self.type=}'