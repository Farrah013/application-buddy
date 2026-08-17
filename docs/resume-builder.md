# Evidence-locked resume builder

## Purpose

The resume builder produces a focused resume version for each qualified role. It changes emphasis, ordering, summary language, skills, and project selection. It never changes the underlying facts.

## Workflow

1. Read the approved master resume and evidence inventory.
2. Read the job description and extracted requirements.
3. Reject any requirement without traceable candidate evidence.
4. Rank evidence by job relevance.
5. Select the strongest professional and portfolio evidence.
6. Prepare an ATS-friendly summary and skill list from supported terms.
7. Draft bullets whose factual claims remain bounded by the source evidence.
8. Flag missing metrics, unclear claims, and proposed wording for Farrah's review.
9. Render a DOCX and PDF only after approval.
10. store the job URL, job-description snapshot, evidence IDs, resume version, approval state, and final files.

## Locked fields

The builder never changes these fields without explicit approval and new evidence:

- Employer names
- Job titles
- Employment dates
- Education
- Certifications
- Metrics
- Tools and proficiency
- Portfolio test results
- Client or project status
- Software proficiency and years of use

## Allowed tailoring

- Reorder approved bullets
- Select job-relevant approved bullets
- Replace a supported term with an accurate ATS synonym
- Emphasize relevant skills
- Select relevant portfolio projects
- Shorten or clarify wording without changing meaning
- Produce a role-specific summary from supported evidence

## Review states

- `SOURCE_VERIFIED`
- `USER_CONFIRMATION_REQUIRED`
- `APPROVED_FOR_RESUME`
- `EXCLUDED`

No generated claim reaches the final resume unless its evidence record is approved for resume use.

Software outside the approved baseline triggers a question for Farrah before the builder marks the requirement as missing.

## Output versions

- Master resume
- AI Customer Success resume
- AI Implementation resume
- Technical Customer Success resume
- Job-specific resume

Each version receives a unique ID and a change report explaining what moved, what changed, why the change improves alignment, and which evidence supports each claim.
