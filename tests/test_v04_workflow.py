import json
import tempfile
import unittest
from pathlib import Path

from src.application_buddy.application_answers import draft_answer
from src.application_buddy.change_report import build_change_report
from src.application_buddy.docx_renderer import render_resume_docx
from src.application_buddy.resume_draft import create_resume_draft


ROOT = Path(__file__).resolve().parents[1]


class V04WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.job = json.loads((ROOT / "examples/sample-job.json").read_text())
        self.evidence = json.loads((ROOT / "data/candidate-evidence.json").read_text())
        self.source = json.loads((ROOT / "data/resume-source.json").read_text())

    def test_resume_stays_review_only(self):
        draft = create_resume_draft(self.job, self.evidence, self.source)
        self.assertEqual(draft["document_status"], "REVIEW_DRAFT")
        self.assertFalse(draft["final_use_allowed"])

    def test_unverified_portfolio_skills_stay_out_of_resume(self):
        draft = create_resume_draft(self.job, self.evidence, self.source)
        self.assertNotIn("tool calling", draft["skills"])
        self.assertNotIn("AI opportunity discovery", draft["skills"])

    def test_sensitive_question_requires_user(self):
        result = draft_answer("What are your salary expectations?", [], self.evidence)
        self.assertEqual(result["status"], "USER_INPUT_REQUIRED")
        self.assertIsNone(result["draft"])

    def test_missing_evidence_blocks_answer(self):
        result = draft_answer("Describe your experience", ["missing"], self.evidence)
        self.assertEqual(result["status"], "BLOCKED_MISSING_EVIDENCE")

    def test_change_report_requires_review(self):
        report = build_change_report({"summary": "A", "skills": []}, {"summary": "B", "skills": ["x"]})
        self.assertEqual(report["change_count"], 2)
        self.assertFalse(report["final_use_allowed"])

    def test_docx_renderer_outputs_file(self):
        draft = create_resume_draft(self.job, self.evidence, self.source)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "draft.docx"
            render_resume_docx(draft, str(path))
            self.assertTrue(path.exists())


if __name__ == "__main__":
    unittest.main()
