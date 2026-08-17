# Public contact research and email confidence

## Purpose

Application Buddy researches public contact information for people relevant to a qualified opening. Email is preferred. LinkedIn is an accepted fallback. The agent never invents a person, title, relationship to the opening, email address, or source.

## Target order

1. Hiring manager named in the posting or a verified company source
2. Recruiter tied to the opening
3. Leader of the hiring department
4. Talent acquisition employee associated with the company
5. Employee in the same or a comparable function

## Contact states

- `VERIFIED_PUBLISHED`: The address appears on an official company page, the person's public professional page, or another reliable public source.
- `VERIFIED_BY_SERVICE`: A permitted verification service reports the address as deliverable. Store the service, result, and retrieval time.
- `INFERRED_PATTERN`: The address was generated from a verified employee name and a company email pattern supported by public examples.
- `UNVERIFIED`: A source mentions the address, but reliability or ownership is unclear.
- `NOT_FOUND`: Research found no supportable email address.

## Inferred-email rule

An inferred address requires all of the following:

1. A verified full name.
2. A verified current company relationship.
3. At least two publicly available company email examples showing the same naming pattern, unless an authoritative company source explicitly publishes the pattern.
4. Source URLs and retrieval dates for the name, role, and pattern.
5. A confidence score and the `INFERRED_PATTERN` label.
6. Verification before automated outreach.

The agent must never describe an inferred address as found, confirmed, verified, or published.

## Required contact record

- Person name
- Current title
- Company
- Relationship to opening
- Job URL or job ID
- LinkedIn URL
- Email
- Email status
- Confidence
- Supporting sources
- Retrieval time
- Verification result
- Outreach approval
- Last contact date
- Follow-up date
- Opt-out status

## Research limits

Use public professional information. Respect source access rules and rate limits. Do not collect sensitive personal data, private contact details, or unrelated personal information. Do not bypass logins, CAPTCHAs, access controls, or site restrictions.
