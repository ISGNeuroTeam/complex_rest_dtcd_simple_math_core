import json
import unittest

from swt import SourceWideTable


class TestSourceWideTable(unittest.TestCase):

    def test_read(self):
        with open("resources/example_of_swt.json") as fr:
            first = json.loads(fr.read())
        swt = SourceWideTable("example_of_swt.csv")
        second = swt.read()
        self.assertEqual(first, second)

    def test_read_last_row(self):
        with open("resources/example_of_swt.json") as fr:
            first = [json.loads(fr.read())[-1]]
        swt = SourceWideTable("example_of_swt.csv")
        second = swt.read_last_row()
        self.assertEqual(first, second)


if __name__ == '__main__':
    unittest.main()
