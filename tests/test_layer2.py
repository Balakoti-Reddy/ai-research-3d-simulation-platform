import unittest
from src.layer1_understanding.extractor import PrimaryUnderstandingEngine
from src.layer2_decision.decision_engine import ResearchDecisionEngine

class TestLayer2DecisionEngine(unittest.TestCase):
    def setUp(self):
        self.understanding = PrimaryUnderstandingEngine()
        self.decision_engine = ResearchDecisionEngine()

    def test_a_unclear_objective(self):
        spec = self.understanding.parse_input("I want to make it better.")
        decision = self.decision_engine.evaluate_state_and_decide(spec)
        self.assertEqual(decision.selected_action, "CLARIFY")

    def test_b_literature_exploration(self):
        spec = self.understanding.parse_input("I want to investigate existing methods for predicting flood-prone areas.")
        decision = self.decision_engine.evaluate_state_and_decide(spec)
        self.assertEqual(decision.selected_action, "RESEARCH")

    def test_c_missing_data(self):
        spec = self.understanding.parse_input("Run a flood prediction simulation.")
        decision = self.decision_engine.evaluate_state_and_decide(spec, {"model_ready": False})
        self.assertEqual(decision.selected_action, "REPORT_BLOCKER")

    def test_i_user_approval(self):
        spec = self.understanding.parse_input("Train a heavy computation neural network model.")
        decision = self.decision_engine.evaluate_state_and_decide(spec, {"user_approved": False})
        self.assertEqual(decision.selected_action, "WAIT_FOR_USER")
        self.assertTrue(decision.requires_user_approval)

if __name__ == '__main__':
    unittest.main()
