import unittest

from translator.commands.reader import Reader


class TestTranslatorRead(unittest.TestCase):

    def test_read_by_graph_name(self):
        graph_name = "example_of_swt"
        first = "readFile format=CSV path=SWT/example_of_swt"
        second = Reader.read(graph_name)
        self.assertEqual(first, second)

    def test_read_last_raw_by_graph_name(self):
        graph_name = "example_of_swt"
        first = "readFile format=CSV path=SWT/example_of_swt | tail 1"
        second = Reader.read_last_row(graph_name)
        self.assertEqual(first, second)


if __name__ == '__main__':
    unittest.main()
