import unittest

from translator.graph import Graph


class TestGraph(unittest.TestCase):

    def setUp(self) -> None:
        with open("resources/example_of_graph.json") as fr:
            self._graph = Graph(fr.read())

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
        first = ""
        second = self._graph.update(swt_line)
        self.assertEqual(first, second)
