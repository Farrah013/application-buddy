"""Recency evidence without unsupported timestamp claims."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def _parse(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def assess_recency(job: dict[str, Any], maximum_age_hours: int = 72) -> dict[str, Any]:
    retrieved = _parse(job.get("retrieved_at"))
    published = _parse(job.get("published_at"))
    if retrieved is None:
        raise ValueError("retrieved_at is required for recency assessment")
    if published is None:
        return {
            "recency_status": "UNVERIFIED",
            "age_hours": None,
            "within_window": None,
            "basis": "Displayed posting text only",
            "displayed_posting_text": job.get("displayed_posting_text"),
        }
    age_hours = round((retrieved - published).total_seconds() / 3600, 1)
    return {
        "recency_status": "VERIFIED_TIMESTAMP",
        "age_hours": age_hours,
        "within_window": 0 <= age_hours <= maximum_age_hours,
        "basis": "Published and retrieval timestamps",
        "displayed_posting_text": job.get("displayed_posting_text"),
    }
