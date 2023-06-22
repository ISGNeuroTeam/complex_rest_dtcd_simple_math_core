from unittest import TestCase

import json
import re

from dtcd_simple_math_core.translator.node import Node, EVAL_GLOBALS


class TestNode(TestCase):

    def setUp(self):
        data = {'primitiveID': 'UncontrolledRichLabelNode01_1', 'primitiveName': 'UncontrolledRichLabelNode01',
                'properties': {
                    'testField': {'expression': '', 'type_': 'expression', 'status': 'complete', 'value': ''}},
                'extensionName': 'ExtensionRiskPrimitives', 'nodeTitle': '$this.primitiveID$', 'initPorts': [
                {'primitiveName': 'outPort1', 'type_': ['OUT'],
                 'properties': {'status': {'expression': '', 'type_': 'expression', 'status': 'complete', 'value': ''}},
                 'primitiveID': 'UncontrolledRichLabelNode01_1_outPort1', 'location': {'x': 298.75, 'y': 136.29}}],
                'layout': {'x': 151.75, 'y': 139.25, 'height': 148, 'width': 294}}
        self.node = Node(data)

    def test_fill_default_properties(self):
        name = 'testField'
        sample = {'expression': '', 'status': 'complete', 'type_': 'expression', 'value': ''}
        result = self.node.properties[name].get_dictionary()
        self.assertEqual(sample, result)
        new_data = {'_operations_order': '100'}
        sample = {'expression': '', 'status': 'complete', 'type_': 'expression', 'value': '',
                  '_operations_order': '100'}
        self.node.fill_default_properties(name=name, data=new_data)
        result = self.node.properties[name].get_dictionary()
        self.assertEqual(sample, result)

    def test_update_property(self):
        name = 'testField'
        value = 'newValueData'
        sample = {'expression': '', 'status': 'complete', 'type_': 'expression', 'value': 'newValueData'}
        self.node.update_property(name, value)
        result = self.node.properties[name].get_dictionary()
        self.assertEqual(sample, result)

    def test_filter_eval_properties_true(self):
        name = 'testField'
        _property = (name, self.node.properties[name])
        result = self.node.filter_eval_properties(prop=_property)
        self.assertTrue(result)

    def test_filter_eval_properties_false(self):
        name = '_operations_order'
        _property = (name, self.node.properties[name])
        result = self.node.filter_eval_properties(prop=_property)
        self.assertFalse(result)

    def test_get_eval_properties(self):
        print(f'\n********\nwe have this properties: {self.node.properties.values()}')
        sample = 1
        eval_properties = [n[0] for n in self.node.get_eval_properties()]
        print(f'eval_properties: {eval_properties}')
        result = len(eval_properties)
        self.assertEqual(sample, result)

    def test_make_object_property_full_name_with_property_link(self):
        self.node.fill_default_properties(name='testField', data={'expression': '2018'})
        self.node.fill_default_properties(name='movieStar', data={'expression': 'Sly'})
        self.node.fill_default_properties(name='theBest', data={'expression': 'movieStar'})
        sample = '2018'
        prop = self.node.properties['theBest']
        re_group = re.search(EVAL_GLOBALS['re_object_property_name'], prop.get_expression)
        result = self.node.make_object_property_full_name(re_group, self.node.properties.keys(), self.node.object_id)
        self.assertEqual(sample, result)

    def test_make_object_property_full_name_with_no_property_link(self):
        self.node.fill_default_properties(name='testField', data={'expression': '2018'})
        self.node.fill_default_properties(name='movieStar', data={'expression': 'Sly'})
        self.node.fill_default_properties(name='theBest', data={'expression': 'movieStar'})
        sample = "'UncontrolledRichLabelNode01_1.movieStar'"
        prop = self.node.properties['testField']
        re_group = re.search(EVAL_GLOBALS['re_object_property_name'], prop.get_expression)
        result = self.node.make_object_property_full_name(re_group, self.node.properties.keys(),
                                                          self.node.object_id)
        self.assertEqual(sample, result)

    def test_get_eval_expressions(self):
        new_data = {'expression': '2018'}
        name = 'testField'
        self.node.fill_default_properties(name=name, data=new_data)
        sample = [{'UncontrolledRichLabelNode01_1.testField': '2018'}]
        result = self.node.get_eval_expressions()
        self.assertEqual(sample, result)
