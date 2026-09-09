# mulesoft-claude-code-review

Claude Code review kit for Mule 4 applications.

The review methodology lives in `CLAUDE.md`, `review.md`,
`finding-taxonomy.md` and `.claude/skills/mule-code-review/`.

## Running a full application review

Call the master prompt:

```text
prompts/mule-full-review.md
```

The review is read-only. Its single deliverable is a Word document in the
repository root:

```text
CODE_REVIEW_REPORT.docx
```

No Markdown report file is produced. The report text is piped straight into
the converter, so the `.docx` is the only file written.

## The converter

`scripts/md_to_docx.py` turns the review Markdown into a styled Word
document: cover page with app/branch/commit metadata, a Word table of
contents, styled headings, pipe tables with repeating header rows, shaded
code blocks, and severity keywords (CRITICAL / HIGH / MEDIUM / LOW / NIT)
colour-coded throughout.

It is invoked by PHASE 20 of the prompt:

```bash
python3 scripts/md_to_docx.py \
  --input - \
  --output CODE_REVIEW_REPORT.docx \
  --app "order-experience-api" \
  --branch "$(git rev-parse --abbrev-ref HEAD)" \
  --commit "$(git rev-parse --short HEAD)" <<'MULE_REVIEW_EOF'
# MuleSoft Full Application Code Review Report
...
MULE_REVIEW_EOF
```

Requirements: Python 3.9+ and `python-docx`. The script installs
`python-docx` on first use if it is missing.

Run `python3 scripts/md_to_docx.py --help` for all options
(`--title`, `--repo`, `--review-type`, `--eyebrow`, `--footnote`,
`--date`, `--no-toc`).

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
fails the job if `CODE_REVIEW_REPORT.docx` was not produced, writes the
review summary to the job summary, and uploads the Word document as a build
artifact.

Notes:

- `REVIEW_KIT_DIR` tells the prompt where the kit files and the converter
  live. Use `.` when the kit and the application are the same repository.
- The kit checkout path is added to `.git/info/exclude` so the read-only
  verification in PHASE 20 sees a clean working tree. That file is local to
  the runner and never committed.
- Triggers are `workflow_dispatch` and `pull_request` on `main`/`develop`.
  Adjust to taste; a full review is a long job, so per-push triggers are
  usually not worthwhile.
