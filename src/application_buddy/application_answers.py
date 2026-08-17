"""Evidence-bound application answer drafts."""

from __future__ import annotations

from typing import Any


SENSITIVE_TOPICS = ("salary", "compensation", "work authorization", "visa", "disability", "veteran", "race", "gender", "signature", "relocation")


def draft_answer(question: str, evidence_ids: list[str], evidence_data: dict[str, Any]) -> dict[str, Any]:
    lower = question.lower()
    if any(topic in lower for topic in SENSITIVE_TOPICS):
        return {"question": question, "status": "USER_INPUT_REQUIRED", "draft": None, "evidence_ids": [], "reason": "Sensitive or personal answer"}
    evidence_by_id = {item["id"]: item for item in evidence_data.get("evidence", [])}
    missing = [item_id for item_id in evidence_ids if item_id not in evidence_by_id]
    if missing:
        return {"question": question, "status": "BLOCKED_MISSING_EVIDENCE", "draft": None, "evidence_ids": evidence_ids, "missing_evidence_ids": missing}
    statements = [evidence_by_id[item_id]["statement"] for item_id in evidence_ids]
    return {
        "question": question,
        "status": "REVIEW_DRAFT",
        "draft": " ".join(statements),
        "evidence_ids": evidence_ids,
        "approval_required": True,
    }
