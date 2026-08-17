"""Human review queue for consequential actions."""

from __future__ import annotations

from typing import Any


APPROVAL_TYPES = {
    "REQUIREMENT_REVIEW",
    "EVIDENCE_CONFIRMATION",
    "RESUME_APPROVAL",
    "CONTACT_VERIFICATION",
    "OUTREACH_APPROVAL",
    "APPLICATION_ANSWER",
    "SUBMISSION_APPROVAL",
}


def create_approval_item(item: dict[str, Any]) -> dict[str, Any]:
    approval_type = item.get("approval_type")
    if approval_type not in APPROVAL_TYPES:
        raise ValueError(f"Unknown approval type: {approval_type}")
    if not item.get("related_record_id") or not item.get("reason"):
        raise ValueError("Approval items require related_record_id and reason")
    return {
        **item,
        "status": "PENDING",
        "decision": None,
        "decided_at": None,
        "decision_notes": None,
    }
