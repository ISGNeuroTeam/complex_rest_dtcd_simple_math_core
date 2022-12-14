import json
import unittest

from translator.swt import SourceWideTable


class TestSourceWideTable(unittest.TestCase):

    def setUp(self) -> None:
        self.swt = SourceWideTable("example_of_swt")

    def test_read(self):
        with open("resources/example_of_swt.json") as fr:
            first = json.loads(fr.read())
        second = self.swt.read()
        self.assertEqual(first, second)

    def test_read_last_row(self):
        with open("resources/example_of_swt.json") as fr:
            first = [json.loads(fr.read())[-1]]
        second = self.swt.read_last_row()
        self.assertEqual(first, second)

    def test_read_tick(self):
        tick = -1
        with open("resources/example_of_swt.json") as fr:
            first = [json.loads(fr.read())[-1]]
        second = self.swt.read_tick(-1)
        self.assertEqual(first, second)
        tick = 0
        with open("resources/example_of_swt.json") as fr:
            first = json.loads(fr.read())
        second = self.swt.read_tick(0)
        self.assertEqual(first, second)
        first = [{'ControlledRichLabelNode01_2.V': '7.5', 'StepRichLabelNode11_2.Enabled': '1',
                  'TargetRichLabelNode1_2.R': '2', '_sn': '0', '_t': '10'}]
        tick = 10
        second = self.swt.read_tick(tick)
        self.assertEqual(first, second)


if __name__ == '__main__':
    unittest.main()
