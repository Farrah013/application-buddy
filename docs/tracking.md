# Google Sheets and Notion tracking

## Destination choice

Application Buddy supports Google Sheets and Notion. One destination serves as the system of record for a run. A second destination receives updates only when explicit synchronization rules exist.

## Job tracker

The discovery view stores job ID, company, title, job URL, source, displayed posting time, verified posting time, retrieval time, location, compensation, preliminary score, and review state.

The qualified view adds requirement evidence, final score, non-negotiable results, résumé version, application answers, contact research, outreach state, application status, submission proof, and follow-up dates.

## Contact tracker

Contact records use the fields defined in `contact-research.md`. Published, verified, inferred, unverified, and missing email states remain distinct.

## Audit fields

Every created or changed record stores the timestamp, operating mode, source URLs, agent action, approval state, and last confirmed status. Unknown values stay blank or receive an explicit unknown state.

## Write controls

The agent prepares records locally when no authenticated Google Sheets or Notion connection exists. External writes begin only after the user selects a destination and grants access. The agent must report failed writes as failed and must never treat a prepared local record as synchronized.
