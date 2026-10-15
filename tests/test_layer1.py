import unittest
from src.layer1_understanding.extractor import PrimaryUnderstandingEngine

class TestLayer1UnderstandingEngine(unittest.TestCase):
    def setUp(self):
        self.engine = PrimaryUnderstandingEngine()

    def test_a_simple_objective(self):
        spec = self.engine.parse_input("I want to build a system that predicts flood-prone areas.")
        self.assertIn("predicts flood-prone areas", spec.objective)
        self.assertTrue(len(spec.unknowns) > 0)

    def test_b_qualitative_constraint(self):
        spec = self.engine.parse_input("I want to develop an affordable glasses-free 3D display.")
        self.assertIn("Affordable", spec.constraints[0].constraint)

    def test_c_additional_information(self):
        self.engine.parse_input("I want to build a flood prediction system.")
        spec = self.engine.parse_input("I have rainfall data but no historical flood labels.")
        self.assertTrue(any("rainfall" in r for r in spec.available_resources))

    def test_d_user_correction(self):
        self.engine.parse_input("I want to predict flood depth.")
        spec = self.engine.parse_input("Correction: I only want to identify high-risk areas.")
        self.assertIn("Correction", spec.objective)

    def test_e_multidomain(self):
        spec = self.engine.parse_input("I want to test battery materials for solar energy.")
        self.assertIn("Materials Science & Energy Systems", spec.research_domain)

if __name__ == '__main__':
    unittest.main()
