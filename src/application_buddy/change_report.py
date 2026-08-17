"""Auditable comparison between résumé drafts."""

from __future__ import annotations

from typing import Any


def build_change_report(master: dict[str, Any], tailored: dict[str, Any]) -> dict[str, Any]:
    changes = []
    if master.get("summary") != tailored.get("summary"):
        changes.append({"field": "summary", "change_type": "REVISED", "before": master.get("summary"), "after": tailored.get("summary"), "approval_required": True})
    if master.get("skills") != tailored.get("skills"):
        changes.append({"field": "skills", "change_type": "REORDERED_OR_FILTERED", "before": master.get("skills", []), "after": tailored.get("skills", []), "approval_required": True})
    return {"status": "REVIEW_REQUIRED", "change_count": len(changes), "changes": changes, "final_use_allowed": False}
