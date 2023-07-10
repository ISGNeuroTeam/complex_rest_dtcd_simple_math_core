from unittest import TestCase

from dtcd_simple_math_core.translator.properties import Property


class TestProperties(TestCase):

    def setUp(self):
        self.name = 'testField'
        data = {'expression': 'shaba-laba-daba-doo', 'type_': 'expression', 'status': 'not complete', 'value': '',
                'rockstar': 'Lenny Kravitz'}
        self.prop = Property(**data)

    def test_get_expression(self):
        sample = 'shaba-laba-daba-doo'
        result = self.prop.get_expression
        self.assertEqual(sample, result)

    def test_update(self):
        value = 'shwooom'
        status = 'complete'
        self.prop.update(value=value, status=status)
        self.assertEqual(value, self.prop.value)
        self.assertEqual(status, self.prop.status)

    def test_has_expression_true(self):
        sample = True
        result = self.prop.has_expression()
        self.assertEqual(sample, result)

    def test_has_expression_false(self):
        sample = False
        self.prop.expression = ''
        result = self.prop.has_expression()
        self.assertEqual(sample, result)

    def test_get_dictionary(self):
        sample = {'expression': 'shaba-laba-daba-doo', 'has_import': False, 'has_swt_import': False,
                  'import_expression': '', 'imports': 0, 'rockstar': 'Lenny Kravitz', 'status': 'not complete',
                  'swt_import': 'SWTImport', 'type_': 'expression', 'value': ''}
        result = self.prop.get_dictionary()
        self.assertEqual(sample, result)
