from unittest import TestCase

from dtcd_simple_math_core.translator.query import Query


class TestQuery(TestCase):

    def setUp(self):
        self.query = Query('example_of_swt')

    def test_get_read_expression_for_whole_swt(self):
        sample = 'readFile format=JSON path=SWT/example_of_swt  '
        result = self.query.get_read_expression()
        self.assertEqual(sample, result)

    def test_get_read_expression_for_last_row_of_swt(self):
        sample = 'readFile format=JSON path=SWT/example_of_swt | tail 1  '
        result = self.query.get_read_expression(last_row=True)
        self.assertEqual(sample, result)

    def test_get_write_expression(self):
        sample = 'writeFile format=JSON path=SWT/example_of_swt'
        result = self.query.get_write_expression()
        self.assertEqual(sample, result)

    def test_get_write_expression_with_append(self):
        sample = 'writeFile format=JSON mode=append path=SWT/example_of_swt'
        result = self.query.get_write_expression(append=True)
        self.assertEqual(sample, result)

    def test_get_write_expression_with_custom_path_and_format(self):
        sample = 'writeFile format=XSLX mode=append path=ISGNeuro/example_of_swt'
        result = self.query.get_write_expression(append=True, file_path='ISGNeuro', file_format='XSLX')
        self.assertEqual(sample, result)

    def test_get_eval_expressions_with_empty_eval_names(self):
        sample = ''
        result = self.query.get_eval_expressions([])
        self.assertEqual(sample, result)

    def test_get_eval_expressions(self):
        eval_names = [{'UncontrolledRichLabelNode01_1.Sum1': '28'}, {'UncontrolledRichLabelNode01_2.Sum1': '28'},
                      {'TargetRichLabelNode2_5.Sum1': '28'}, {'DataLakeNode_22.Sum1': '28'}]
        sample = "| eval 'UncontrolledRichLabelNode01_1.Sum1' = 28 | eval 'UncontrolledRichLabelNode01_2.Sum1' = 28 | " \
                 "eval 'TargetRichLabelNode2_5.Sum1' = 28 | eval 'DataLakeNode_22.Sum1' = 28 "
        result = self.query.get_eval_expressions(eval_names=eval_names)
        self.assertEqual(sample, result)

    def test_get_fields_expression(self):
        eval_names = [{'Goal_3.type': '"Цель"'}, {'Goal_3.value': '12'},
                      {'Data_96.type': '"Примитив с данными"'}, {'Data_96.value': '12'}]
        sample = 'fields _t, _sn, _time, Goal_3.type, Goal_3.value, Data_96.type, Data_96.value'
        result = self.query.get_fields_expression(eval_names=eval_names)
        self.assertEqual(sample, result)
