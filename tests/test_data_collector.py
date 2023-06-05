from unittest import TestCase
from resources.swt_example import whole_swt
from dtcd_simple_math_core.translator.data_collector import DataCollector


class TestDataCollector(TestCase):

    def setUp(self):
        self.datacollector = DataCollector('example_of_swt')

    def test_read_swt_whole(self):
        sample = whole_swt
        result = self.datacollector.read_swt(last_row=False)
        self.assertEqual(sample, result)

    def test_read_swt_last_row(self):
        sample = [whole_swt[-1]]
        result = self.datacollector.read_swt(last_row=True)
        self.assertEqual(sample, result)

    # TODO this test is not finished till we have a sample of graph eval names
    def test_calc_swt(self):
        eval_names = [{'UncontrolledRichLabelNode01_1.Sum1': '28'}, {'UncontrolledRichLabelNode01_2.Sum1': '28'}, {'TargetRichLabelNode2_5.Sum1': '28'}, {'DataLakeNode_22.Sum1': '28'}]
        sample = [{'ControlledRichLabelNode01_172.testField': 13.1, 'ControlledRichLabelNode01_173.testField': 13.1, 'ControlledRichLabelNode01_2.V': '2', 'ControlledRichLabelNode01_2.external_enabled': 1, 'ControlledRichLabelNode01_2.testField': 13.1, 'ControlledRichLabelNode01_207.I': "'StepRichLabelNode11_1.Enabled'*V/'TargetRichLabelNode1_1.R'", 'ControlledRichLabelNode01_207.P': "'ControlledRichLabelNode01_207.V'*'ControlledRichLabelNode01_207.I'*'StepRichLabelNode11_1.Enabled'", 'ControlledRichLabelNode01_207.testField': 10.1, 'DataLakeNode_22.Sum1': 28, 'StepRichLabelNode11_1.I': "'StepRichLabelNode11_1.Enabled'*V/'TargetRichLabelNode1_1.R'", 'StepRichLabelNode11_1.P': "'ControlledRichLabelNode01_207.V'*'ControlledRichLabelNode01_207.I'*'StepRichLabelNode11_1.Enabled'", 'StepRichLabelNode11_2.Enabled': '1', 'StepRichLabelNode31_1.a': 2, 'StepRichLabelNode31_1.name': 'MD_operirovanie', 'TargetRichLabelNode1_1.I': "'StepRichLabelNode11_1.Enabled'*V/'TargetRichLabelNode1_1.R'", 'TargetRichLabelNode1_1.P': "'ControlledRichLabelNode01_207.V'*'ControlledRichLabelNode01_207.I'*'StepRichLabelNode11_1.Enabled'", 'TargetRichLabelNode1_2.R': '2', 'TargetRichLabelNode1_2.testField': 1.0, 'TargetRichLabelNode2_5.Sum1': 28, 'UncontrolledRichLabelNode01_1.Sum1': 28, 'UncontrolledRichLabelNode01_2.Sum1': 28, 'UncontrolledRichLabelNode11_97.name': 'Risk_snizheniya_MD', 'UncontrolledRichLabelNode11_99.name': 'Risk_snizheniya_parka', 'UncontrolledRichLabelNode21_4.testField': 27.2, '_sn': '0', '_t': '25'}]
        result = self.datacollector.calc_swt(eval_names=eval_names)
        self.assertEqual(sample, result)
