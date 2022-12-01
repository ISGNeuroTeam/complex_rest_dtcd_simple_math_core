import json
import unittest

from translator.commands.eval import Eval


class TestTranslatorEval(unittest.TestCase):

    def test_from_graph(self):
        with open("resources/example_of_graph.json") as fr:
            first = "eval 'ControlledRichLabelNode01_207.testField' = 5+5.1 | eval 'ControlledRichLabelNode01_207.I'" \
                    " = 'StepRichLabelNode11_1.Enabled'*'ControlledRichLabelNode01_207.V'/'TargetRichLabelNode1_1.R'" \
                    " | eval 'TargetRichLabelNode1_1.testField' = cos('TargetRichLabelNode1_1.R') |" \
                    " eval 'TargetRichLabelNode1_1.P' = 'ControlledRichLabelNode01_207.V'" \
                    "*'ControlledRichLabelNode01_207.I'*'StepRichLabelNode11_1.Enabled'"
            second = Eval.from_graph(json.loads(fr.read()))
            self.assertEqual(first, second)


if __name__ == '__main__':
    unittest.main()
