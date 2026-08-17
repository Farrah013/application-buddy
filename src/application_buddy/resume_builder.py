"""Build an evidence-locked resume tailoring plan."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


TOKEN_PATTERN = re.compile(r"[a-zA-Z][a-zA-Z0-9+.#-]{1,}")
STOP_WORDS = {
    "and", "for", "the", "with", "from", "into", "then", "this", "that",
    "role", "work", "experience", "customer", "customers", "required",
}


def tokens(text: str) -> set[str]:
    return {
        token.lower().strip(".#-+")
        for token in TOKEN_PATTERN.findall(text)
        if token.lower().strip(".#-+")
        and token.lower().strip(".#-+") not in STOP_WORDS
    }


def build_tailoring_plan(
    job: dict[str, Any], evidence_data: dict[str, Any]
) -> dict[str, Any]:
    requirement_text = " ".join(
        item.get("text", "")
        for item in job.get("requirements", [])
        if item.get("status") in {"met", "partial"}
    )
    job_tokens = tokens(requirement_text)
    ranked = []

    for item in evidence_data.get("evidence", []):
        searchable = " ".join(
            [item.get("statement", ""), *item.get("skills", [])]
        )
        overlap = sorted(job_tokens & tokens(searchable))
        ranked.append(
            {
                "evidence_id": item["id"],
                "evidence_type": item.get("type"),
                "statement": item.get("statement"),
                "relevance_terms": overlap,
                "relevance_score": len(overlap),
                "resume_status": (
                    "USER_CONFIRMATION_REQUIRED"
                    if item.get("type") == "user_provided_unverified"
                    else "SOURCE_VERIFIED"
                ),
            }
        )

    ranked.sort(key=lambda item: (-item["relevance_score"], item["evidence_id"]))
    supported_skills = sorted(
        {
            skill
            for item in evidence_data.get("evidence", [])
            for skill in item.get("skills", [])
            if tokens(skill) & job_tokens
        },
        key=str.lower,
    )

    return {
        "company": job.get("company"),
        "title": job.get("title"),
        "recommended_evidence": ranked,
        "supported_skills": supported_skills,
        "builder_rules": {
            "invent_metrics": False,
            "change_employment_facts": False,
            "include_unverified_without_approval": False,
            "produce_change_report": True,
        },
    }


def load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a resume tailoring plan.")
    parser.add_argument("--job", required=True)
    parser.add_argument("--evidence", required=True)
    args = parser.parse_args()
    result = build_tailoring_plan(load_json(args.job), load_json(args.evidence))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
