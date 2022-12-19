import json
import unittest

from translator.graph import Graph


class TestGraphWithEdges(unittest.TestCase):

    def setUp(self) -> None:
        with open("resources/example_of_graph_with_swt.json") as fr:
            self._graph = Graph("example_of_swt", fr.read())
        Graph.PATH_TO_GRAPH = "./resources/graphs/{0}.json"

    def test_new_iteration(self):
        first = {'graph': {'edges': [{'bends': [], 'sourceNode': 'ControlledRichLabelNode01_173', 'sourcePort': 'ControlledRichLabelNode01_173_outPort1', 'targetNode': 'UncontrolledRichLabelNode21_4', 'targetPort': 'UncontrolledRichLabelNode21_4_inPort2', 'extensionName': 'ExtensionCommonPrimitives', 'primitiveName': 'SimpleEdge'}, {'bends': [], 'sourceNode': 'ControlledRichLabelNode01_172', 'sourcePort': 'ControlledRichLabelNode01_172_outPort1', 'targetNode': 'UncontrolledRichLabelNode21_4', 'targetPort': 'UncontrolledRichLabelNode21_4_inPort1', 'extensionName': 'ExtensionCommonPrimitives', 'primitiveName': 'SimpleEdge'}], 'groups': [], 'nodes': [{'primitiveID': 'ControlledRichLabelNode01_173', 'primitiveName': 'ControlledRichLabelNode01', 'properties': {'testField': {'expression': '5+6.1+2', 'type': 'expression', 'status': 'complete', 'input': {'component': 'textarea'}, 'value': 13.1}, 'V': {'type': 'expression', 'expression': '', 'status': 'complete', 'input': {'component': 'textarea'}, 'value': 12}, 'I': {'type': 'expression', 'expression': 'StepRichLabelNode11_2.Enabled*V/TargetRichLabelNode1_2.R', 'status': 'complete', 'input': {'component': 'textarea'}, 'value': 1}, '_operations_order': {'value': 100, 'status': 'complete', 'type': 'expression', 'expression': 100, 'input': {'component': 'textarea'}}}, 'extensionName': 'ExtensionRiskPrimitives', 'nodeTitle': '<p>Battery</p>', 'initPorts': [{'primitiveName': 'outPort1', 'type': ['OUT'], 'properties': {'status': {'type': 'expression', 'expression': 'testField', 'input': {'component': 'textarea'}}}, 'primitiveID': 'ControlledRichLabelNode01_173_outPort1', 'location': {'x': 1459, 'y': 548.04}}], 'layout': {'x': 1312, 'y': 551, 'height': 148, 'width': 294}}, {'primitiveID': 'ControlledRichLabelNode01_172', 'primitiveName': 'ControlledRichLabelNode01', 'properties': {'testField': {'expression': '5+6.1+2', 'type': 'expression', 'status': 'complete', 'input': {'component': 'textarea'}, 'value': 13.1}, 'V': {'type': 'expression', 'expression': '', 'status': 'complete', 'input': {'component': 'textarea'}, 'value': '2'}, 'I': {'type': 'expression', 'expression': 'StepRichLabelNode11_2.Enabled*V/TargetRichLabelNode1_2.R', 'status': 'complete', 'input': {'component': 'textarea'}, 'value': 1}, '_operations_order': {'value': 100, 'status': 'complete', 'type': 'expression', 'expression': 100, 'input': {'component': 'textarea'}}}, 'extensionName': 'ExtensionRiskPrimitives', 'nodeTitle': '<p>Battery</p>', 'initPorts': [{'primitiveName': 'outPort1', 'type': ['OUT'], 'properties': {'status': {'type': 'expression', 'expression': 'testField', 'input': {'component': 'textarea'}}}, 'primitiveID': 'ControlledRichLabelNode01_172_outPort1', 'location': {'x': 1101.5, 'y': 548.04}}], 'layout': {'x': 954.5, 'y': 551, 'height': 148, 'width': 294}}, {'primitiveID': 'UncontrolledRichLabelNode21_4', 'primitiveName': 'UncontrolledRichLabelNode21', 'properties': {'testField': {'expression': '(inPort1*inPort2)/(inPort2* inPort1)+ inPort1+inPort2', 'type': 'expression', 'status': 'complete', 'input': {'component': 'textarea'}, 'value': 27.2}, '_operations_order': {'type': 'expression', 'expression': '2', 'status': 'complete', 'input': {'component': 'textarea'}, 'value': '2'}}, 'extensionName': 'ExtensionRiskPrimitives', 'nodeTitle': '$this.primitiveID$', 'initPorts': [{'primitiveName': 'inPort2', 'type': ['IN'], 'properties': {'status': {'expression': "let portOwner = graph.ports.find(port => port.tag.primitiveID === primitiveID).owner;\nlet inEdges = graph.inEdgesAt(portOwner).filter(edge => edge.targetPort.tag.primitiveID === primitiveID).toArray()\nif (inEdges.length < 1) ''\nelse {\neval(inEdges[0].sourcePort.tag.primitiveID).status\n}", 'type': 'expression', 'status': 'complete', 'value': ''}}, 'primitiveID': 'UncontrolledRichLabelNode21_4_inPort2', 'location': {'x': 1380.2, 'y': 431.96000000000004}}, {'primitiveName': 'inPort1', 'type': ['IN'], 'properties': {'status': {'expression': "let portOwner = graph.ports.find(port => port.tag.primitiveID === primitiveID).owner;\nlet inEdges = graph.inEdgesAt(portOwner).filter(edge => edge.targetPort.tag.primitiveID === primitiveID).toArray()\nif (inEdges.length < 1) ''\nelse {\neval(inEdges[0].sourcePort.tag.primitiveID).status\n}", 'type': 'expression', 'status': 'complete', 'value': ''}}, 'primitiveID': 'UncontrolledRichLabelNode21_4_inPort1', 'location': {'x': 1203.8, 'y': 431.96000000000004}}, {'primitiveName': 'outPort1', 'type': ['OUT'], 'properties': {'status': {'expression': '', 'type': 'expression', 'status': 'complete', 'value': ''}}, 'primitiveID': 'UncontrolledRichLabelNode21_4_outPort1', 'location': {'x': 1292, 'y': 278.04}}], 'layout': {'x': 1145, 'y': 281, 'height': 148, 'width': 294}}, {'primitiveID': 'StepRichLabelNode11_2', 'primitiveName': 'StepRichLabelNode11', 'properties': {'testField': {'expression': '', 'type': 'expression', 'status': 'complete', 'value': ''}, 'Enabled': {'type': 'expression', 'expression': '', 'status': 'complete', 'input': {'component': 'textarea'}, 'value': '1'}, '_operations_order': {'type': 'expression', 'expression': '2', 'status': 'complete', 'input': {'component': 'textarea'}, 'value': '2'}}, 'extensionName': 'ExtensionRiskPrimitives', 'nodeTitle': '<p>Switch</p>', 'initPorts': [{'primitiveName': 'inPort1', 'type': ['IN'], 'properties': {'status': {'expression': "let portOwner = graph.ports.find(port => port.tag.primitiveID === primitiveID).owner;\nlet inEdges = graph.inEdgesAt(portOwner).filter(edge => edge.targetPort.tag.primitiveID === primitiveID).toArray()\nif (inEdges.length < 1) ''\nelse {\neval(inEdges[0].sourcePort.tag.primitiveID).status\n}", 'type': 'expression', 'status': 'complete', 'value': ''}}, 'primitiveID': 'StepRichLabelNode11_2_inPort1', 'location': {'x': 667, 'y': 453.46000000000004}}, {'primitiveName': 'outPort1', 'type': ['OUT'], 'properties': {'status': {'expression': '', 'type': 'expression', 'status': 'complete', 'value': ''}}, 'primitiveID': 'StepRichLabelNode11_2_outPort1', 'location': {'x': 667, 'y': 299.54}}], 'layout': {'x': 520, 'y': 302.5, 'height': 148, 'width': 294}}, {'primitiveID': 'ControlledRichLabelNode01_2', 'primitiveName': 'ControlledRichLabelNode01', 'properties': {'testField': {'expression': '5+6.1+2', 'type': 'expression', 'status': 'complete', 'input': {'component': 'textarea'}, 'value': 13.1}, '_operations_order': {'type': 'expression', 'expression': '1', 'status': 'complete', 'input': {'component': 'textarea'}, 'value': '1'}, 'external_enabled': {'type': 'SWT', 'expression': {'swt_name': 'simple_math_lamp', 'column': 'StepRichLabelNode11_2.Enabled'}, 'status': 'complete', 'value': 1, 'input': {'component': 'textarea'}, '_expression': '1'}}, 'extensionName': 'ExtensionRiskPrimitives', 'nodeTitle': '<p>Battery</p>', 'initPorts': [{'primitiveName': 'outPort1', 'type': ['OUT'], 'properties': {'status': {'expression': '', 'type': 'expression', 'status': 'complete', 'value': ''}}, 'primitiveID': 'ControlledRichLabelNode01_2_outPort1', 'location': {'x': 667, 'y': 548.04}}], 'layout': {'x': 520, 'y': 551, 'height': 148, 'width': 294}}, {'primitiveID': 'TargetRichLabelNode1_2', 'primitiveName': 'TargetRichLabelNode1', 'properties': {'testField': {'expression': 'cos(R*0)', 'type': 'expression', 'status': 'complete', 'input': {'component': 'textarea'}, 'value': 1.0}, 'R': {'type': 'expression', 'expression': '', 'status': 'complete', 'input': {'component': 'textarea'}, 'value': '2'}, 'P': {'type': 'expression', 'expression': 'ControlledRichLabelNode01_2.V*ControlledRichLabelNode01_2.I*StepRichLabelNode11_2.Enabled', 'status': 'complete', 'input': {'component': 'textarea'}, 'value': 1.3333333333333333}, '_operations_order': {'type': 'expression', 'expression': '3', 'status': 'complete', 'input': {'component': 'textarea'}, 'value': '3'}}, 'extensionName': 'ExtensionRiskPrimitives', 'nodeTitle': '<p>Lamp</p>', 'initPorts': [{'primitiveName': 'inPort1', 'type': ['IN'], 'properties': {'status': {'expression': "let portOwner = graph.ports.find(port => port.tag.primitiveID === primitiveID).owner;\nlet inEdges = graph.inEdgesAt(portOwner).filter(edge => edge.targetPort.tag.primitiveID === primitiveID).toArray()\nif (inEdges.length < 1) ''\nelse {\neval(inEdges[0].sourcePort.tag.primitiveID).status\n}", 'type': 'expression', 'status': 'complete', 'value': ''}}, 'primitiveID': 'TargetRichLabelNode1_2_inPort1', 'location': {'x': 667, 'y': 204.96}}], 'layout': {'x': 520, 'y': 54, 'height': 148, 'width': 294}}]}}
        second = self._graph.new_iteration()
        print(second)
        self.assertDictEqual(first, second)
