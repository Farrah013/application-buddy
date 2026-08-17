"""Evidence requirements for public and inferred contact data."""

from __future__ import annotations

from typing import Any


EMAIL_STATES = {"VERIFIED_PUBLISHED", "VERIFIED_BY_SERVICE", "INFERRED_PATTERN", "UNVERIFIED", "NOT_FOUND"}


def validate_contact(contact: dict[str, Any]) -> dict[str, Any]:
    state = contact.get("email_status")
    if state not in EMAIL_STATES:
        raise ValueError(f"Unknown email status: {state}")
    sources = contact.get("supporting_sources", [])
    if state in {"VERIFIED_PUBLISHED", "VERIFIED_BY_SERVICE"} and not sources:
        raise ValueError("Verified contact records require a supporting source")
    if state == "INFERRED_PATTERN":
        required = ("person_name", "company", "email", "pattern", "confidence")
        missing = [field for field in required if not contact.get(field)]
        if missing:
            raise ValueError(f"Inferred email missing evidence fields: {', '.join(missing)}")
        if len(sources) < 2:
            raise ValueError("Inferred email requires at least two supporting sources")
        contact["outreach_automation_allowed"] = False
        contact["verification_required"] = True
    else:
        contact["outreach_automation_allowed"] = state in {"VERIFIED_PUBLISHED", "VERIFIED_BY_SERVICE"}
        contact["verification_required"] = state not in {"VERIFIED_PUBLISHED", "VERIFIED_BY_SERVICE", "NOT_FOUND"}
    return contact
