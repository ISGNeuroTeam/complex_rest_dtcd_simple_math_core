from unittest import TestCase, mock

import json

import os

from dtcd_simple_math_core.translator.graph import Graph, get_row_of_swt
from .resources.wide_swt_dates import dates


class TestGraph(TestCase):

    def setUp(self):
        # budget.json graph is so big, that it calculates too long | thought it is just breaking
        self.name = 'n_serditov_graph_001'
        parent_folder = os.path.dirname(__file__)
        with open(f'{parent_folder}/resources/{self.name}.json') as file:
            self.graph_from_json_file = json.loads(file.read())
        self.graph = Graph(self.name, self.graph_from_json_file)
        self.graph.initialize()

    def test_init_graph(self):
        self.assertEqual(self.name, self.graph.name)
        self.assertEqual(self.graph_from_json_file, self.graph.dictionary)

    def test_graph_initialize(self):
        sample = dict
        result = type(self.graph.dictionary)
        self.assertEqual(sample, result)

    def test_parse_nodes(self):
        sample = len(self.graph.dictionary['graph']['nodes'])
        result = len(self.graph.nodes)
        self.assertEqual(sample, result)

    def test_get_property_of_the_node_by_id(self):
        object_id = 'DataLakeNode_22'
        sample = {'_operations_order': {'expression': 1, 'status': 'complete', 'type': 'expression', 'value': ''},
                  'query': {'expression': '', 'status': 'complete', 'type': 'expression', 'value': ''}}
        result = self.graph.get_property_of_the_node_by_id(object_id=object_id)
        self.assertEqual(sample, result)

    def test_update_property_at_graph(self):
        object_id = 'UncontrolledRichLabelNode01_2'
        _property = 'Sum1'
        sample = '150'
        control_property = self.graph.get_property_of_the_node_by_id(object_id=object_id)
        self.graph.update_property_at_graph(node_name=object_id, prop_name=_property, parameter='value', value=sample)
        result = control_property[_property]['value']
        self.assertEqual(sample, result)

    def test_get_eval_expressions(self):
        sample = [{'UncontrolledRichLabelNode01_2.Sum1': '28'},
                  {'Data_396.type': '"Примитив с данными"'},
                  {'Data_396.value': '0.6 + 0.7'},
                  {'Goal_10.type': '"Цель"'},
                  {'Goal_10.value': "('Data_395.value' + 'Data_396.value') * 200"},
                  {'Data_395.type': '"Примитив с данными"'},
                  {'Data_395.value': '0.5'}]
        result = self.graph.get_nodes_eval_expressions()
        self.assertEqual(sample, result)

    def test_graph_has_this(self):
        true_result = self.graph.graph_has_this('Data_396.type')
        false_result = self.graph.graph_has_this('Data_396.exportedProperty')
        self.assertTrue(true_result)
        self.assertFalse(false_result)

    # @mock.patch('time.time', mock.MagicMock(return_value=1692118295)) # 1562014800
    @mock.patch('time.time', mock.MagicMock(return_value=1562014800))
    def test_get_row_of_swt_previous_month(self):
        # 1562014800 (2023.07.01)>> {'_t': '1561928400'} (2023.06.30)
        list_of_rows = dates
        swt_line_index = 'PREVIOUS_MONTH'
        sample = {'_t': '1561928400'}
        result = get_row_of_swt(list_of_rows=list_of_rows, swt_line_index=swt_line_index)
        self.assertEqual(sample, result)

    def test_get_row_of_swt_latest_index(self):
        list_of_rows = dates
        swt_line_index = 'LATEST'
        sample = {'_t': '1661979600'}
        result = get_row_of_swt(list_of_rows=list_of_rows, swt_line_index=swt_line_index)
        self.assertEqual(sample, result)
