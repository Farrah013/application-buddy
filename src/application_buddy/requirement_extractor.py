"""Conservative requirement extraction from captured job text."""

from __future__ import annotations

import re
from typing import Any


SECTION_MAP = {
    "responsibilities": "core_responsibilities",
    "what you'll do": "core_responsibilities",
    "what you will do": "core_responsibilities",
    "required qualifications": "required_qualifications",
    "requirements": "required_qualifications",
    "minimum qualifications": "required_qualifications",
    "preferred qualifications": "preferred_qualifications",
    "nice to have": "preferred_qualifications",
}
NON_NEGOTIABLE_TERMS = ("must", "required", "minimum", "need to", "at least")


def extract_requirements(description: str) -> list[dict[str, Any]]:
    """Extract only explicit lines. Unknown section lines require review."""
    current_category = "required_qualifications"
    results: list[dict[str, Any]] = []
    for raw_line in description.splitlines():
        line = re.sub(r"^[\s\-•*\d.)]+", "", raw_line).strip()
        if not line:
            continue
        heading = line.lower().rstrip(":")
        if heading in SECTION_MAP:
            current_category = SECTION_MAP[heading]
            continue
        if len(line.split()) < 3:
            continue
        lower = line.lower()
        results.append({
            "id": f"req-{len(results) + 1:03d}",
            "category": current_category,
            "text": line,
            "non_negotiable": any(term in lower for term in NON_NEGOTIABLE_TERMS),
            "status": "unclear",
            "evidence_ids": [],
            "extraction_status": "REVIEW_REQUIRED",
        })
    return results
