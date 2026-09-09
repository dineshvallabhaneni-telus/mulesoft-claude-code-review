# mulesoft-claude-code-review

Claude Code review kit for Mule 4 applications.

The review methodology lives in `CLAUDE.md`, `review.md`,
`finding-taxonomy.md` and `.claude/skills/mule-code-review/`.

## Running a full application review

Call the master prompt:

```text
prompts/mule-full-review.md
```

The review is read-only. Its single deliverable is one timestamped Word
document in the `reports` folder:

```text
reports/CODE_REVIEW_REPORT_20260909-084530.docx
```

No Markdown or JSON file is produced. The review is piped straight into the
generator, so the `.docx` is the only file written.

## How the report is built

The review is authored as a **structured JSON object**, not as prose. A
deterministic generator turns that JSON into the Word document, so the
document's structure, numbering, tables and colour coding are fixed by code
rather than re-invented on each run.

```text
Claude (PHASE 19)          scripts/generate_report.py       reports/
  review findings JSON  ->   structural python-docx      ->   CODE_REVIEW_REPORT_<stamp>.docx
```

The schema is defined by
`.claude/skills/mule-code-review/references/review-report-schema.md`, which
gives the exact keys, the allowed enum values and a worked example for every
section.

The generated document contains a cover page, a table of contents, sections
1–6 and appendices A–C:

```text
1. Executive Summary            4. Category Assessments (4.1 - 4.15)
2. Application Inventory        5. Production Readiness Assessment
3. Findings (3.1 - 3.5)         6. Risk and Recommendation

Appendix A - Complete Findings Inventory
Appendix B - Finding Evidence Detail
Appendix C - Review Coverage and Boundaries
```

Two properties are worth calling out:

- **Counts cannot lie.** The severity and category counts in sections 1.3 and
  1.4 are derived from the findings array, not authored, so they can never
  disagree with the detailed findings.
- **Verdicts cannot be understated.** `overallRisk` and
  `overallRecommendation` are floored against the finding evidence. A review
  that reports a CRITICAL finding cannot also recommend APPROVE; the verdict
  is raised, the raise is printed on the console, and section 6.4 records
  what was stated alongside what the evidence supports.

## The generator

`scripts/generate_report.py` is invoked by PHASE 20 of the prompt:

```bash
python3 scripts/generate_report.py \
  --input - \
  --output-dir reports \
  --app "order-experience-api" \
  --branch "$(git rev-parse --abbrev-ref HEAD)" \
  --commit "$(git rev-parse --short HEAD)" <<'MULE_REVIEW_EOF'
{ "application": { "name": "order-experience-api" }, ... }
MULE_REVIEW_EOF
```

It creates `reports/` if needed, names the file
`CODE_REVIEW_REPORT_<YYYYMMDD-HHMMSS>.docx` using the same timestamp that
appears on the cover page, re-opens the saved document to confirm every
required section is present, and prints the path it wrote along with the
reconciled verdict and the finding counts. A missing section is a non-zero
exit, not a warning. One run produces one document.

Requirements: Python 3.9+ and `python-docx`. The script installs
`python-docx` on first use if it is missing.

Run `python3 scripts/generate_report.py --help` for all options
(`--output-dir`, `--name-prefix`, `--output`, `--app`, `--repo`, `--branch`,
`--commit`, `--review-type`, `--footnote`, `--date`, `--no-toc`).

## GitHub Actions

A ready-to-use workflow is provided:

```text
workflows/mule-code-review.yml
```

Copy it into the **Mule application repository** as
`.github/workflows/mule-code-review.yml`, then:

1. Add the `ANTHROPIC_API_KEY` secret to that repository.
2. Set `REVIEW_KIT_REPO` in the workflow `env` block to this repository.
3. If this repository is private, add a `REVIEW_KIT_TOKEN` secret (a PAT
   with read access) and uncomment the `token:` line on the review-kit
   checkout step.

The workflow checks out the application at the workspace root and this kit
at `.review-kit`, installs `python-docx` and Claude Code, runs the prompt,
fails the job unless exactly one non-empty document exists in `reports/`,
writes the review summary to the job summary, and uploads the Word document
as a build artifact.

Notes:

- `REVIEW_KIT_DIR` tells the prompt where the kit files and the generator
  live. Use `.` when the kit and the application are the same repository.
- The kit checkout path is added to `.git/info/exclude` so the read-only
  verification in PHASE 20 sees a clean working tree. That file is local to
  the runner and never committed.
- Triggers are `workflow_dispatch` and `pull_request` on `main`/`develop`.
  Adjust to taste; a full review is a long job, so per-push triggers are
  usually not worthwhile.
