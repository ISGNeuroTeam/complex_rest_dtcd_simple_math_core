import unittest

from dtcd_simple_math_core.translator.queries.read import ReadQuery


class TestTranslatorRead(unittest.TestCase):

    def test_read_by_graph_name(self):
        graph_name = "example_of_swt"
        first = "readFile format=CSV path=SWT/example_of_swt"
        second = ReadQuery.get(graph_name)
        self.assertEqual(first, second)

    def test_read_last_raw_by_graph_name(self):
        graph_name = "example_of_swt"
        first = "readFile format=CSV path=SWT/example_of_swt | tail 1"
        second = ReadQuery.get(graph_name, last_row=True)
        self.assertEqual(first, second)


if __name__ == '__main__':
    unittest.main()
