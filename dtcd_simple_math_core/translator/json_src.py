graph = {"graph": {"edges": [], "groups": [], "nodes": [
    {"primitiveID": "TargetRichLabelNode1_1", "primitiveName": "TargetRichLabelNode1",
     "properties": {"testField": {"expression": "", "type": "expression", "status": "complete", "value": ""},
                    "R": {"type": "expression", "expression": "", "status": "complete",
                          "input": {"component": "textarea"}, "value": "2"}, "P": {"type": "expression",
                                                                                   "expression": "\"ControlledRichLabelNode01_207.V*ControlledRichLabelNode01_207.I*StepRichLabelNode11_1.Enabled\"",
                                                                                   "status": "complete", "input": {
                 "component": "textarea"}, "value": 2.0},
                    "_operations_order": {"type": "expression", "expression": "3", "status": "complete", "value": 3,
                                          "input": {"component": "textarea"}}},
     "extensionName": "ExtensionRiskPrimitives", "nodeTitle": "<p>Lamp</p>", "initPorts": [
        {"primitiveName": "inPort1", "type": "IN", "properties": {"status": {
            "expression": "let portOwner = graph.ports.find(port => port.tag.primitiveID === primitiveID).owner;\nlet inEdges = graph.inEdgesAt(portOwner).filter(edge => edge.targetPort.tag.primitiveID === primitiveID).toArray()\nif (inEdges.length < 1) ''\nelse {\neval(inEdges[0].sourcePort.tag.primitiveID).status\n}",
            "type": "expression", "status": "complete", "value": ""}},
         "primitiveID": "TargetRichLabelNode1_1_inPort1", "location": {"x": 667, "y": 204.96}}],
     "layout": {"x": 520, "y": 54, "height": 148, "width": 294}},
    {"primitiveID": "ControlledRichLabelNode01_207", "primitiveName": "ControlledRichLabelNode01",
     "properties": {"testField": {"expression": "", "type": "expression", "status": "complete", "value": ""},
                    "V": {"type": "expression", "expression": "", "status": "complete",
                          "input": {"component": "textarea"}, "value": "2"}, "I": {"type": "expression",
                                                                                   "expression": "\"StepRichLabelNode11_1.Enabled*V/TargetRichLabelNode1_1.R\"",
                                                                                   "status": "complete", "input": {
                 "component": "textarea"}, "value": 1.0},
                    "_operations_order": {"type": "expression", "expression": "1", "status": "complete", "value": 1,
                                          "input": {"component": "textarea"}}},
     "extensionName": "ExtensionRiskPrimitives", "nodeTitle": "<p>Battery</p>", "initPorts": [
        {"primitiveName": "outPort1", "type": "OUT",
         "properties": {"status": {"expression": "", "type": "expression", "status": "complete", "value": ""}},
         "primitiveID": "ControlledRichLabelNode01_207_outPort1", "location": {"x": 667, "y": 548.04}}],
     "layout": {"x": 520, "y": 551, "height": 148, "width": 294}},
    {"primitiveID": "StepRichLabelNode11_1", "primitiveName": "StepRichLabelNode11",
     "properties": {"testField": {"expression": "", "type": "expression", "status": "complete", "value": ""},
                    "Enabled": {"type": "expression", "expression": "", "status": "complete",
                                "input": {"component": "textarea"}, "value": "1"},
                    "_operations_order": {"type": "expression", "expression": "2", "status": "complete", "value": 2,
                                          "input": {"component": "textarea"}}},
     "extensionName": "ExtensionRiskPrimitives", "nodeTitle": "<p>Switch</p>", "initPorts": [
        {"primitiveName": "outPort1", "type": "OUT",
         "properties": {"status": {"expression": "", "type": "expression", "status": "complete", "value": ""}},
         "primitiveID": "StepRichLabelNode11_1_outPort1", "location": {"x": 667, "y": 299.54}},
        {"primitiveName": "inPort1", "type": "IN", "properties": {"status": {
            "expression": "let portOwner = graph.ports.find(port => port.tag.primitiveID === primitiveID).owner;\nlet inEdges = graph.inEdgesAt(portOwner).filter(edge => edge.targetPort.tag.primitiveID === primitiveID).toArray()\nif (inEdges.length < 1) ''\nelse {\neval(inEdges[0].sourcePort.tag.primitiveID).status\n}",
            "type": "expression", "status": "complete", "value": ""}},
         "primitiveID": "StepRichLabelNode11_1_inPort1", "location": {"x": 667, "y": 453.46000000000004}}],
     "layout": {"x": 520, "y": 302.5, "height": 148, "width": 294}}]}}