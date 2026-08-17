"""Create traceable, review-only résumé content."""

from __future__ import annotations

from typing import Any

from .resume_builder import build_tailoring_plan, tokens


def create_resume_draft(job: dict[str, Any], evidence: dict[str, Any], source: dict[str, Any]) -> dict[str, Any]:
    plan = build_tailoring_plan(job, evidence)
    job_terms = tokens(" ".join(item.get("text", "") for item in job.get("requirements", [])))
    roles = []
    used_evidence_ids: set[str] = set()
    for role in source.get("experience", []):
        ranked_bullets = []
        for bullet in role.get("bullets", []):
            overlap = sorted(job_terms & tokens(bullet["text"]))
            ranked_bullets.append({**bullet, "relevance_terms": overlap, "relevance_score": len(overlap)})
            used_evidence_ids.update(bullet.get("evidence_ids", []))
        ranked_bullets.sort(key=lambda item: (-item["relevance_score"], item["id"]))
        roles.append({**{key: value for key, value in role.items() if key != "bullets"}, "bullets": ranked_bullets})

    approved_evidence = [
        item for item in evidence.get("evidence", [])
        if item.get("type") in {"verified_professional", "portfolio_evidence"}
    ]
    supported_skills = sorted({
        skill
        for item in approved_evidence
        for skill in item.get("skills", [])
        if tokens(skill) & job_terms
    }, key=str.lower)
    summary = (
        "Customer Success and implementation professional with experience in customer onboarding, "
        "training, technical issue resolution, cross-functional coordination, and customer feedback workflows."
    )
    return {
        "document_status": "REVIEW_DRAFT",
        "final_use_allowed": False,
        "company": job.get("company"),
        "target_title": job.get("title"),
        "candidate": source["candidate"],
        "summary": {"text": summary, "evidence_ids": sorted(used_evidence_ids), "approval_status": "REVIEW_REQUIRED"},
        "skills": supported_skills,
        "experience": roles,
        "education": source.get("education", []),
        "portfolio_items": [item for item in plan["recommended_evidence"] if item["evidence_type"] == "user_provided_unverified"],
        "approval_requirements": ["SUMMARY", "BULLET_SELECTION", "SKILLS", "PORTFOLIO_CLAIMS", "FINAL_DOCUMENT"],
    }
