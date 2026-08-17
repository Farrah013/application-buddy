"""Generate the v0.4 review-only résumé fixture."""

import json
from pathlib import Path

from src.application_buddy.docx_renderer import render_resume_docx
from src.application_buddy.resume_draft import create_resume_draft


ROOT = Path(__file__).resolve().parents[1]
job = json.loads((ROOT / "examples/sample-job.json").read_text())
evidence = json.loads((ROOT / "data/candidate-evidence.json").read_text())
source = json.loads((ROOT / "data/resume-source.json").read_text())
draft = create_resume_draft(job, evidence, source)
output_dir = ROOT / "output/v0.4-review"
output_dir.mkdir(parents=True, exist_ok=True)
(output_dir / "resume-review-draft.json").write_text(json.dumps(draft, indent=2), encoding="utf-8")
render_resume_docx(draft, str(output_dir / "resume-review-draft.docx"))
