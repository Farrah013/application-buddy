"""Evidence-first role scoring for Application Buddy."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CATEGORY_WEIGHTS = {
    "core_responsibilities": 0.40,
    "required_qualifications": 0.40,
    "preferred_qualifications": 0.10,
    "domain_alignment": 0.10,
}

STATUS_VALUES = {
    "met": 1.0,
    "partial": 0.5,
    "not_met": 0.0,
    "unclear": None,
}

QUALIFICATION_THRESHOLD = 75.0


def score_job(job: dict[str, Any], evidence_data: dict[str, Any]) -> dict[str, Any]:
    evidence_by_id = {item["id"]: item for item in evidence_data.get("evidence", [])}
    requirements = job.get("requirements", [])
    category_results: dict[str, Any] = {}
    missing_evidence_ids: set[str] = set()
    unmet_non_negotiables: list[str] = []

    for category, weight in CATEGORY_WEIGHTS.items():
        items = [item for item in requirements if item.get("category") == category]
        scored_items = []
        category_points = 0.0
        category_possible = 0

        for item in items:
            status = item.get("status", "unclear")
            if status not in STATUS_VALUES:
                raise ValueError(f"Unknown status: {status}")

            value = STATUS_VALUES[status]
            evidence_ids = item.get("evidence_ids", [])
            for evidence_id in evidence_ids:
                if evidence_id not in evidence_by_id:
                    missing_evidence_ids.add(evidence_id)

            if value is not None:
                category_points += value
                category_possible += 1

            if item.get("non_negotiable") and status != "met":
                unmet_non_negotiables.append(item.get("text", item.get("id", "unknown")))

            scored_items.append(
                {
                    "id": item.get("id"),
                    "text": item.get("text"),
                    "status": status,
                    "evidence_ids": evidence_ids,
                }
            )

        category_ratio = category_points / category_possible if category_possible else None
        category_results[category] = {
            "weight": weight,
            "ratio": category_ratio,
            "requirements": scored_items,
        }

    represented_weight = sum(
        result["weight"]
        for result in category_results.values()
        if result["ratio"] is not None
    )
    weighted_points = sum(
        result["weight"] * result["ratio"]
        for result in category_results.values()
        if result["ratio"] is not None
    )
    percentage = round((weighted_points / represented_weight) * 100, 1) if represented_weight else 0.0
    qualifies = (
        percentage >= QUALIFICATION_THRESHOLD
        and not unmet_non_negotiables
        and not missing_evidence_ids
    )

    return {
        "company": job.get("company"),
        "title": job.get("title"),
        "match_percentage": percentage,
        "threshold": QUALIFICATION_THRESHOLD,
        "qualifies": qualifies,
        "unmet_non_negotiables": unmet_non_negotiables,
        "missing_evidence_ids": sorted(missing_evidence_ids),
        "category_results": category_results,
    }


def load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Score a job against traceable evidence.")
    parser.add_argument("--job", required=True)
    parser.add_argument("--evidence", required=True)
    args = parser.parse_args()
    result = score_job(load_json(args.job), load_json(args.evidence))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

