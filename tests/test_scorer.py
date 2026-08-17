import json
import unittest
from pathlib import Path

from src.application_buddy.scorer import score_job


ROOT = Path(__file__).resolve().parents[1]


class ScoreJobTests(unittest.TestCase):
    def setUp(self):
        self.job = json.loads((ROOT / "examples/sample-job.json").read_text())
        self.evidence = json.loads((ROOT / "data/candidate-evidence.json").read_text())

    def test_sample_job_scores_85_percent(self):
        result = score_job(self.job, self.evidence)
        self.assertEqual(result["match_percentage"], 85.0)
        self.assertTrue(result["qualifies"])

    def test_unmet_non_negotiable_blocks_qualification(self):
        self.job["requirements"][0]["non_negotiable"] = True
        self.job["requirements"][0]["status"] = "partial"
        result = score_job(self.job, self.evidence)
        self.assertFalse(result["qualifies"])
        self.assertEqual(len(result["unmet_non_negotiables"]), 1)

    def test_missing_evidence_blocks_qualification(self):
        self.job["requirements"][0]["evidence_ids"] = ["missing-record"]
        result = score_job(self.job, self.evidence)
        self.assertFalse(result["qualifies"])
        self.assertEqual(result["missing_evidence_ids"], ["missing-record"])


if __name__ == "__main__":
    unittest.main()
