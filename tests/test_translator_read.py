import unittest

from translator.commands.reader import Reader


class TestTranslatorRead(unittest.TestCase):

    def setUp(self):
        self.format = "JSON"

    def test_read_by_graph_name(self):
        graph_name = "example_of_swt"
        first = f"readFile format={self.format} path=SWT/example_of_swt"
        second = Reader.read(graph_name)
        self.assertEqual(first, second)

    def test_read_last_raw_by_graph_name(self):
        graph_name = "example_of_swt"
        first = f"readFile format={self.format} path=SWT/example_of_swt | tail 1"
        second = Reader.read_last_row(graph_name)
        self.assertEqual(first, second)

    def test_read_tick(self):
        graph_name = "example_of_swt"
        tick = 0
        first = f"readFile format={self.format} path=SWT/example_of_swt | search _t=0"
        second = Reader.read_tick(graph_name, tick)
        self.assertEqual(first, second)
        tick = -1
        first = f"readFile format={self.format} path=SWT/example_of_swt | tail 1"
        second = Reader.read_tick(graph_name, tick)
        self.assertEqual(first, second)
        tick = 10
        first = f"readFile format={self.format} path=SWT/example_of_swt | search _t=10"
        second = Reader.read_tick(graph_name, tick)
        self.assertEqual(first, second)


if __name__ == '__main__':
    unittest.main()
