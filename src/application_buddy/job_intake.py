"""Validated job intake records for Application Buddy."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse


REQUIRED_FIELDS = ("company", "title", "source_url", "description")


def _valid_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def create_job_record(raw: dict[str, Any], retrieved_at: str | None = None) -> dict[str, Any]:
    missing = [field for field in REQUIRED_FIELDS if not str(raw.get(field, "")).strip()]
    if missing:
        raise ValueError(f"Missing required job fields: {', '.join(missing)}")
    if not _valid_http_url(raw["source_url"]):
        raise ValueError("source_url must be a valid HTTP or HTTPS URL")

    timestamp = retrieved_at or datetime.now(timezone.utc).isoformat()
    return {
        "job_id": raw.get("job_id") or f"{raw['company']}::{raw['title']}::{raw['source_url']}",
        "company": raw["company"].strip(),
        "title": raw["title"].strip(),
        "source_url": raw["source_url"].strip(),
        "source_name": raw.get("source_name", "unknown"),
        "description": raw["description"].strip(),
        "location": raw.get("location"),
        "salary_text": raw.get("salary_text"),
        "displayed_posting_text": raw.get("displayed_posting_text"),
        "published_at": raw.get("published_at"),
        "retrieved_at": timestamp,
        "record_status": "INTAKE_COMPLETE",
        "facts_status": "SOURCE_CAPTURED",
    }
