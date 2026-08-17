# Architecture and decision rules

## Modules

1. Job Discovery collects job URLs and source metadata.
2. Recency Validation records the displayed time, original posting time when available, retrieval time, source, and confidence.
3. Requirement Extraction separates responsibilities, required qualifications, preferred qualifications, and domain alignment.
4. Evidence Matching links every score to a resume or portfolio evidence record.
5. Qualification Gate applies the weighted score and non-negotiable gates.
6. Application Preparation creates tailored materials from approved evidence only.
7. People Research records verified public contacts and their relationship to the role.
8. Tracking stores decisions, materials, approvals, submission evidence, and follow-up dates.

## Scoring model

| Category | Weight |
| --- | ---: |
| Core responsibilities | 40% |
| Required qualifications | 40% |
| Preferred qualifications | 10% |
| Industry and domain alignment | 10% |

Requirement scores:

- Clearly met: 1.0
- Partially met: 0.5
- Not met: 0.0
- Unclear: excluded until reviewed

A role qualifies only when the weighted score reaches 75 percent and no unmet non-negotiable requirement exists.

## Evidence classes

- `verified_professional`: supported by the approved resume or employer evidence
- `portfolio_evidence`: supported by an artifact from an independent project
- `user_provided_unverified`: stated by the candidate but awaiting an artifact or confirmation
- `inference`: interpretation, never treated as a qualification fact

## Submission controls

Application Buddy stops before CAPTCHA, unavailable login, SMS verification, legal consent, signature, voluntary demographic disclosures, disability or veteran questions, background-check authorization, unknown salary or work-authorization responses, or unsupported ATS behavior.

