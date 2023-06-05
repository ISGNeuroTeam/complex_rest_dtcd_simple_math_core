from unittest import TestCase
from dtcd_simple_math_core.translator.swt import SourceWideTable


class TestSwt(TestCase):

    def setUp(self):
        self.name = 'n_serditov_graph_001'
        self.swt = SourceWideTable(self.name)

    def test_read(self):
        sample = [{'DataLakeNode_22.Sum1': 28, 'TargetRichLabelNode2_5.Sum1': 28, 'UncontrolledRichLabelNode01_1.Sum1': 28, 'UncontrolledRichLabelNode01_2.Sum1': 28, '_sn': 1, '_t': 1685695989, '_time': 1685695989}, {'DataLakeNode_22.Sum1': 28, 'TargetRichLabelNode2_5.Sum1': 28, 'UncontrolledRichLabelNode01_1.Sum1': 28, 'UncontrolledRichLabelNode01_2.Sum1': 28, '_sn': 1, '_t': 1685695989, '_time': 1685695989}, {'DataLakeNode_22.Sum1': 28, 'TargetRichLabelNode2_5.Sum1': 28, 'UncontrolledRichLabelNode01_1.Sum1': 28, 'UncontrolledRichLabelNode01_2.Sum1': 28, '_sn': 1, '_t': 1685695989, '_time': 1685695989}, {'DataLakeNode_22.Sum1': 28, 'TargetRichLabelNode2_5.Sum1': 28, 'UncontrolledRichLabelNode01_1.Sum1': 28, 'UncontrolledRichLabelNode01_2.Sum1': 28, '_sn': 1, '_t': 1685695989, '_time': 1685695989}, {'DataLakeNode_22.Sum1': 28, 'TargetRichLabelNode2_5.Sum1': 28, 'UncontrolledRichLabelNode01_1.Sum1': 28, 'UncontrolledRichLabelNode01_2.Sum1': 28, '_sn': 1, '_t': 1685695989, '_time': 1685695989}, {'UncontrolledRichLabelNode01_2.Sum1': 28, '_sn': 1, '_t': 1685695989, '_time': 1685695989}, {'DataLakeNode_22.Sum1': 28, 'TargetRichLabelNode2_5.Sum1': 28, 'UncontrolledRichLabelNode01_1.Sum1': 28, 'UncontrolledRichLabelNode01_2.Sum1': 28, '_sn': 1, '_t': 1685695989, '_time': 1685695989}, {'DataLakeNode_22.Sum1': 28, 'TargetRichLabelNode2_5.Sum1': 28, 'UncontrolledRichLabelNode01_1.Sum1': 28, 'UncontrolledRichLabelNode01_2.Sum1': 28, '_sn': 1, '_t': 1685695989, '_time': 1685695989}, {'DataLakeNode_22.Sum1': 28, 'TargetRichLabelNode2_5.Sum1': 28, 'UncontrolledRichLabelNode01_1.Sum1': 28, 'UncontrolledRichLabelNode01_2.Sum1': 28, '_sn': 1, '_t': 1685695989, '_time': 1685695989}, {'DataLakeNode_22.Sum1': 28, 'TargetRichLabelNode2_5.Sum1': 28, 'UncontrolledRichLabelNode01_1.Sum1': 28, 'UncontrolledRichLabelNode01_2.Sum1': 28, '_sn': 1, '_t': 1685695989, '_time': 1685695989}, {'DataLakeNode_22.Sum1': 28, 'TargetRichLabelNode2_5.Sum1': 28, 'UncontrolledRichLabelNode01_1.Sum1': 28, 'UncontrolledRichLabelNode01_2.Sum1': 28, '_sn': 1, '_t': 1685695989, '_time': 1685695989}, {'DataLakeNode_22.Sum1': 28, 'TargetRichLabelNode2_5.Sum1': 28, 'UncontrolledRichLabelNode01_1.Sum1': 28, 'UncontrolledRichLabelNode01_2.Sum1': 28, '_sn': 1, '_t': 1685695989, '_time': 1685695989}, {'DataLakeNode_22.Sum1': 28, 'TargetRichLabelNode2_5.Sum1': 28, 'UncontrolledRichLabelNode01_1.Sum1': 28, 'UncontrolledRichLabelNode01_2.Sum1': 28, '_sn': 1, '_t': 1685695989, '_time': 1685695989}]
        result = self.swt.read()
        self.assertEqual(sample, result)

    def test_read_last_row(self):
        sample = [{'UncontrolledRichLabelNode01_2.Sum1': 28, '_sn': 1, '_t': 1685695989, '_time': 1685695989}]
        result = self.swt.read(last_row=True)
        self.assertEqual(sample, result)

    def test_calc(self):
        eval_names = [{'UncontrolledRichLabelNode01_1.Sum1': '28'}, {'UncontrolledRichLabelNode01_2.Sum1': '28'}, {'TargetRichLabelNode2_5.Sum1': '28'}, {'DataLakeNode_22.Sum1': '28'}]
        sample = [{'DataLakeNode_22.Sum1': 28, 'TargetRichLabelNode2_5.Sum1': 28, 'UncontrolledRichLabelNode01_1.Sum1': 28, 'UncontrolledRichLabelNode01_2.Sum1': 28, '_sn': 1, '_t': 1685695989, '_time': 1685695989}]
        result = self.swt.calc(graph_eval_names=eval_names)
        self.assertEqual(sample, result)
