import json
import unittest
from pathlib import Path

from src.application_buddy.software_matcher import match_software


ROOT = Path(__file__).resolve().parents[1]


class SoftwareMatcherTests(unittest.TestCase):
    def setUp(self):
        self.evidence = json.loads((ROOT / "data/candidate-evidence.json").read_text())

    def test_exact_match_uses_self_reported_status(self):
        result = match_software("Salesforce", "CRM", self.evidence)
        self.assertEqual(result["status"], "EXACT_SELF_REPORTED")
        self.assertEqual(result["score"], 1.0)

    def test_similar_tool_receives_partial_alignment(self):
        result = match_software("Dynamics 365", "CRM", self.evidence)
        self.assertEqual(result["status"], "SIMILAR_FUNCTIONAL_CATEGORY")
        self.assertEqual(result["score"], 0.5)
        self.assertIn("Salesforce", result["matched_software"])

    def test_unknown_tool_requires_candidate_confirmation(self):
        result = match_software("Unknown Platform", None, self.evidence)
        self.assertEqual(result["status"], "USER_CONFIRMATION_REQUIRED")
        self.assertIsNone(result["score"])

