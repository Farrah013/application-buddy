"""Conservative software matching for Application Buddy."""

from __future__ import annotations

from typing import Any


def normalize(name: str) -> str:
    return "".join(character.lower() for character in name if character.isalnum())


def match_software(
    required_name: str,
    required_category: str | None,
    evidence_data: dict[str, Any],
) -> dict[str, Any]:
    baseline = evidence_data.get("software_baseline", [])
    required_normalized = normalize(required_name)

    exact = next(
        (
            item for item in baseline
            if normalize(item.get("name", "")) == required_normalized
            or normalize(item.get("user_term", "")) == required_normalized
        ),
        None,
    )
    if exact:
        return {
            "required_software": required_name,
            "status": "EXACT_SELF_REPORTED",
            "score": 1.0,
            "matched_software": [exact["name"]],
            "confirmation_required": True,
            "reason": "Exact baseline match. Confirm depth or years when requested.",
        }

    similar = [
        item["name"] for item in baseline
        if required_category and item.get("category") == required_category
    ]
    if similar:
        return {
            "required_software": required_name,
            "status": "SIMILAR_FUNCTIONAL_CATEGORY",
            "score": 0.5,
            "matched_software": similar,
            "confirmation_required": True,
            "reason": "Functional-category match only. Do not present as exact experience.",
        }

    return {
        "required_software": required_name,
        "status": "USER_CONFIRMATION_REQUIRED",
        "score": None,
        "matched_software": [],
        "confirmation_required": True,
        "reason": "Software is outside the baseline. Ask Farrah before scoring.",
    }

