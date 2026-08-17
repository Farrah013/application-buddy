import unittest

from src.application_buddy.approval_queue import create_approval_item
from src.application_buddy.contact_records import validate_contact
from src.application_buddy.job_intake import create_job_record
from src.application_buddy.recency import assess_recency
from src.application_buddy.requirement_extractor import extract_requirements


class V03WorkflowTests(unittest.TestCase):
    def test_intake_requires_real_url_and_fields(self):
        with self.assertRaises(ValueError):
            create_job_record({"company": "A", "title": "B", "source_url": "made-up", "description": "Text"})

    def test_requirement_extraction_requires_review(self):
        items = extract_requirements("Responsibilities:\n- Lead customer onboarding projects.")
        self.assertEqual(items[0]["category"], "core_responsibilities")
        self.assertEqual(items[0]["extraction_status"], "REVIEW_REQUIRED")

    def test_missing_published_timestamp_stays_unverified(self):
        result = assess_recency({"retrieved_at": "2026-08-17T18:00:00Z", "displayed_posting_text": "Today"})
        self.assertEqual(result["recency_status"], "UNVERIFIED")
        self.assertIsNone(result["within_window"])

    def test_inferred_email_never_allows_automatic_outreach(self):
        result = validate_contact({
            "email_status": "INFERRED_PATTERN", "person_name": "Example Person",
            "company": "Example Co", "email": "example@example.com",
            "pattern": "first@company.com", "confidence": 0.8,
            "supporting_sources": ["https://example.com/a", "https://example.com/b"],
        })
        self.assertFalse(result["outreach_automation_allowed"])
        self.assertTrue(result["verification_required"])

    def test_approval_queue_starts_pending(self):
        result = create_approval_item({
            "approval_type": "RESUME_APPROVAL", "related_record_id": "job-1",
            "reason": "Review tailored résumé",
        })
        self.assertEqual(result["status"], "PENDING")


if __name__ == "__main__":
    unittest.main()
