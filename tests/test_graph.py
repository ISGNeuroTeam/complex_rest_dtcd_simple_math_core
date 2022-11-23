import json
import unittest

from translator.graph import Graph


class TestGraph(unittest.TestCase):

    def setUp(self) -> None:
        with open("resources/example_of_graph.json") as fr:
            self._graph = Graph(fr.read(), "example_of_swt")
        Graph.PATH_TO_GRAPH = "./resources/graphs/{0}.json"

    def test_search_node_by_id(self):
        node_id = "TargetRichLabelNode1_1"
        first = {'primitiveID': 'TargetRichLabelNode1_1', 'primitiveName': 'TargetRichLabelNode1', 'properties': {'testField': {'expression': '', 'type': 'expression', 'status': 'complete', 'value': ''}, 'R': {'type': 'expression', 'expression': '', 'status': 'complete', 'input': {'component': 'textarea'}, 'value': ''}, 'P': {'type': 'expression', 'expression': '"ControlledRichLabelNode01_207.V*ControlledRichLabelNode01_207.I*StepRichLabelNode11_1.Enabled"', 'status': 'complete', 'input': {'component': 'textarea'}, 'value': 'ControlledRichLabelNode01_207.V*ControlledRichLabelNode01_207.I*StepRichLabelNode11_1.Enabled'}, '_operations_order': {'type': 'expression', 'expression': '3', 'status': 'complete', 'value': 3, 'input': {'component': 'textarea'}}}, 'extensionName': 'ExtensionRiskPrimitives', 'nodeTitle': '<p>Lamp</p>', 'initPorts': [{'primitiveName': 'inPort1', 'type': 'IN', 'properties': {'status': {'expression': "let portOwner = graph.ports.find(port => port.tag.primitiveID === primitiveID).owner;\nlet inEdges = graph.inEdgesAt(portOwner).filter(edge => edge.targetPort.tag.primitiveID === primitiveID).toArray()\nif (inEdges.length < 1) ''\nelse {\neval(inEdges[0].sourcePort.tag.primitiveID).status\n}", 'type': 'expression', 'status': 'complete', 'value': ''}}, 'primitiveID': 'TargetRichLabelNode1_1_inPort1', 'location': {'x': 667, 'y': 204.96}}], 'layout': {'x': 520, 'y': 54, 'height': 148, 'width': 294}}
        second = self._graph.search_node_by_id(node_id)
        self.assertEqual(first, second)

    def test_update(self):
        swt_line = """      {
            "_t": "1",
            "_sn": "0",
            "ControlledRichLabelNode01_207.V": "99",
            "StepRichLabelNode11_1.Enabled": "1",
            "TargetRichLabelNode1_1.R": "2"
        }"""
        first = json.dumps({"graph": {"edges": [], "groups": [], "nodes": [{"primitiveID": "TargetRichLabelNode1_1", "primitiveName": "TargetRichLabelNode1", "properties": {"testField": {"expression": "", "type": "expression", "status": "complete", "value": ""}, "R": {"type": "expression", "expression": "", "status": "complete", "input": {"component": "textarea"}, "value": "2"}, "P": {"type": "expression", "expression": "\"ControlledRichLabelNode01_207.V*ControlledRichLabelNode01_207.I*StepRichLabelNode11_1.Enabled\"", "status": "complete", "input": {"component": "textarea"}, "value": "ControlledRichLabelNode01_207.V*ControlledRichLabelNode01_207.I*StepRichLabelNode11_1.Enabled"}, "_operations_order": {"type": "expression", "expression": "3", "status": "complete", "value": 3, "input": {"component": "textarea"}}}, "extensionName": "ExtensionRiskPrimitives", "nodeTitle": "<p>Lamp</p>", "initPorts": [{"primitiveName": "inPort1", "type": "IN", "properties": {"status": {"expression": "let portOwner = graph.ports.find(port => port.tag.primitiveID === primitiveID).owner;\nlet inEdges = graph.inEdgesAt(portOwner).filter(edge => edge.targetPort.tag.primitiveID === primitiveID).toArray()\nif (inEdges.length < 1) ''\nelse {\neval(inEdges[0].sourcePort.tag.primitiveID).status\n}", "type": "expression", "status": "complete", "value": ""}}, "primitiveID": "TargetRichLabelNode1_1_inPort1", "location": {"x": 667, "y": 204.96}}], "layout": {"x": 520, "y": 54, "height": 148, "width": 294}}, {"primitiveID": "ControlledRichLabelNode01_207", "primitiveName": "ControlledRichLabelNode01", "properties": {"testField": {"expression": "", "type": "expression", "status": "complete", "value": ""}, "V": {"type": "expression", "expression": "", "status": "complete", "input": {"component": "textarea"}, "value": "99"}, "I": {"type": "expression", "expression": "\"StepRichLabelNode11_1.Enabled*V/TargetRichLabelNode1_1.R\"", "status": "complete", "input": {"component": "textarea"}, "value": "StepRichLabelNode11_1.Enabled*V/TargetRichLabelNode1_1.R"}, "_operations_order": {"type": "expression", "expression": "1", "status": "complete", "value": 1, "input": {"component": "textarea"}}}, "extensionName": "ExtensionRiskPrimitives", "nodeTitle": "<p>Battery</p>", "initPorts": [{"primitiveName": "outPort1", "type": "OUT", "properties": {"status": {"expression": "", "type": "expression", "status": "complete", "value": ""}}, "primitiveID": "ControlledRichLabelNode01_207_outPort1", "location": {"x": 667, "y": 548.04}}], "layout": {"x": 520, "y": 551, "height": 148, "width": 294}}, {"primitiveID": "StepRichLabelNode11_1", "primitiveName": "StepRichLabelNode11", "properties": {"testField": {"expression": "", "type": "expression", "status": "complete", "value": ""}, "Enabled": {"type": "expression", "expression": "", "status": "complete", "input": {"component": "textarea"}, "value": "1"}, "_operations_order": {"type": "expression", "expression": "2", "status": "complete", "value": 2, "input": {"component": "textarea"}}}, "extensionName": "ExtensionRiskPrimitives", "nodeTitle": "<p>Switch</p>", "initPorts": [{"primitiveName": "outPort1", "type": "OUT", "properties": {"status": {"expression": "", "type": "expression", "status": "complete", "value": ""}}, "primitiveID": "StepRichLabelNode11_1_outPort1", "location": {"x": 667, "y": 299.54}}, {"primitiveName": "inPort1", "type": "IN", "properties": {"status": {"expression": "let portOwner = graph.ports.find(port => port.tag.primitiveID === primitiveID).owner;\nlet inEdges = graph.inEdgesAt(portOwner).filter(edge => edge.targetPort.tag.primitiveID === primitiveID).toArray()\nif (inEdges.length < 1) ''\nelse {\neval(inEdges[0].sourcePort.tag.primitiveID).status\n}", "type": "expression", "status": "complete", "value": ""}}, "primitiveID": "StepRichLabelNode11_1_inPort1", "location": {"x": 667, "y": 453.46000000000004}}], "layout": {"x": 520, "y": 302.5, "height": 148, "width": 294}}]}})
        second = self._graph.update(swt_line)
        self.assertEqual(first, second)

    def test_save(self):
        self._graph.save()
        with open("resources/example_of_graph.json") as fr:
            first = fr.read()
        with open("resources/graphs/example_of_swt.json") as fr:
            second = fr.read()
        self.assertEqual(first, second)

    def test_read(self):
        with open("resources/graphs/example_of_swt.json") as fr:
            first = fr.read()
        second = Graph.read("example_of_swt").graph
        self.assertEqual(first, second)
