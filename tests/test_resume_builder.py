import json
import unittest
from pathlib import Path

from src.application_buddy.resume_builder import build_tailoring_plan


ROOT = Path(__file__).resolve().parents[1]


class ResumeBuilderTests(unittest.TestCase):
    def setUp(self):
        self.job = json.loads((ROOT / "examples/sample-job.json").read_text())
        self.evidence = json.loads((ROOT / "data/candidate-evidence.json").read_text())

    def test_unverified_portfolio_evidence_requires_confirmation(self):
        result = build_tailoring_plan(self.job, self.evidence)
        cf002 = next(
            item for item in result["recommended_evidence"]
            if item["evidence_id"] == "portfolio-cf002"
        )
        self.assertEqual(cf002["resume_status"], "USER_CONFIRMATION_REQUIRED")

    def test_builder_never_enables_metric_invention(self):
        result = build_tailoring_plan(self.job, self.evidence)
        self.assertFalse(result["builder_rules"]["invent_metrics"])

    def test_supported_skills_come_from_evidence(self):
        result = build_tailoring_plan(self.job, self.evidence)
        evidence_skills = {
            skill for item in self.evidence["evidence"] for skill in item["skills"]
        }
        self.assertTrue(set(result["supported_skills"]).issubset(evidence_skills))

