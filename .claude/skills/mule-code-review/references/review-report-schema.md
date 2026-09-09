# Code Review Report Schema

Output: a single Microsoft Word `.docx` in `reports/`.

Rendered by `scripts/generate_report.py` from one input:

| Input | Written by | Supplies |
|---|---|---|
| review findings JSON | Claude, in PHASE 19 | cover page, sections 1 to 6, appendices A to C |

The JSON is piped straight into the generator. No Markdown report file and no
JSON file is left behind.

---

## Top-Level JSON Shape

```json
{
  "application": { ... },
  "review": { ... },
  "executiveSummary": "...",
  "scope": { ... },
  "methodology": [ ... ],
  "inventory": [ ... ],
  "technologyStack": [ ... ],
  "architectureSummary": "...",
  "integrations": [ ... ],
  "findings": [ ... ],
  "assessments": { ... },
  "productionReadiness": { ... },
  "positiveObservations": [ ... ],
  "riskSummary": [ ... ],
  "remediationPriorities": [ ... ],
  "limitations": [ ... ],
  "coverage": [ ... ],
  "overallRisk": "HIGH",
  "overallRecommendation": "CHANGES REQUIRED",
  "recommendationRationale": "..."
}
```

Narrative string fields accept `**bold**` and `` `code` `` inline markup, and a
blank line starts a new paragraph. Everything else is plain text.

Use `"Not identified"` where repository evidence does not provide the
information. Do not guess, and do not omit the key.

---

## Cover Page

Application, repository, branch, commit, Mule runtime, Java version, review
type, generation timestamp, total findings, and the overall risk and overall
recommendation — colour-coded.

Drawn from `application`, `review`, and the reconciled verdict. CLI flags
(`--app`, `--repo`, `--branch`, `--commit`) win over the JSON when supplied.

```json
"application": {
  "name": "order-experience-api",
  "muleRuntime": "4.6.0",
  "javaVersion": "17",
  "muleMavenPlugin": "4.1.1",
  "deploymentModel": "CloudHub 2.0"
},
"review": {
  "repository": "org/order-experience-api",
  "branch": "main",
  "commit": "0b058e7"
}
```

---

## 1. Executive Summary

**1.0** Overall risk and overall recommendation as prominent colour-coded
lines, then the `executiveSummary` narrative.

**1.1 Review Scope** — `scope.statement`, then `scope.included` and
`scope.excluded` bullet lists.

**1.2 Review Methodology** — `methodology`, one line per methodology step.

**1.3 Findings by Severity** — CRITICAL, HIGH, MEDIUM, LOW, NIT and a total,
counted from `findings`. Not author-supplied, so it can never disagree with the
detailed findings.

**1.4 Findings by Category** — counted from each finding's `category`.

---

## 2. Application Inventory

`inventory` — the review.md section 17 areas, in the order supplied.

```json
"inventory": [
  { "area": "Mule Runtime", "inventory": "4.6.0" },
  { "area": "Flows", "inventory": "`order-main`, `order-process`, `order-notify`" }
]
```

**2.1 Technology Stack** — `technologyStack`, each entry naming the repository
file that evidences the version.

```json
"technologyStack": [
  { "component": "HTTP Connector", "version": "1.9.1",
    "source": "pom.xml:118", "notes": "Matches runtime 4.6" }
]
```

**2.2 Architecture Summary** — `architectureSummary`.

**2.3 Integration Inventory** — `integrations`, one row per integration
boundary. `risk` is colour-coded.

```json
"integrations": [
  { "source": "API", "target": "Oracle DB", "mechanism": "DB Connector",
    "mode": "Sync", "retry": "None", "transaction": "Local", "risk": "MEDIUM" }
]
```

---

## 3. Findings

One numbered subsection per severity — 3.1 Critical through 3.5 Nit — each
listing its findings ordered by ID. An empty severity states so explicitly
rather than being skipped.

Each finding renders an Attribute/Value table (ID, severity, category, file,
location, confidence) followed by Problem, Evidence, Impact and Recommendation.
`evidenceSnippet`, when present, is rendered as a monospaced excerpt under
Evidence.

```json
"findings": [
  {
    "id": "SEC-001",
    "severity": "CRITICAL",
    "category": "SECURITY",
    "title": "Database password committed in plain text",
    "file": "src/main/resources/config-dev.yaml:14",
    "location": "db.password property",
    "confidence": "HIGH",
    "problem": "...",
    "evidence": "...",
    "evidenceSnippet": "db:\n  password: Pr0dPass!23",
    "impact": "...",
    "recommendation": "..."
  }
]
```

`severity` must be one of CRITICAL, HIGH, MEDIUM, LOW, NIT. `confidence` must
be HIGH, MEDIUM or LOW. A finding declaring anything else is still rendered,
in a separate 3.6 subsection, but is excluded from the counts — so the
generator surfaces the mistake instead of hiding it.

Use the finding IDs defined by the applicable `references/*.md` rule. Do not
invent an ID when a reference ID exists.

---

## 4. Category Assessments

`assessments` — a keyed object. All fifteen areas render as numbered
subsections whether or not they are supplied; a missing area renders as
`NOT ASSESSED`.

Keys, in render order: `security`, `architecture`, `muleXml`, `errorHandling`,
`dataweave`, `api`, `connectors`, `database`, `messaging`, `performance`,
`logging`, `munit`, `maven`, `configuration`, `maintainability`.

```json
"assessments": {
  "security": {
    "rating": "WEAK",
    "summary": "...",
    "observations": ["..."],
    "gaps": ["..."]
  }
}
```

`rating` is one of STRONG, ADEQUATE, WEAK, INADEQUATE, NOT ASSESSED, and is
colour-coded.

---

## 5. Production Readiness Assessment

`productionReadiness.summary`, then:

**5.1 Readiness Dimensions** — all ten review.md section 31 dimensions render
whether or not they are supplied.

Keys: `security`, `reliability`, `errorRecovery`, `idempotency`,
`observability`, `performance`, `scalability`, `configuration`, `testing`,
`operationalSupport`.

```json
"productionReadiness": {
  "summary": "...",
  "dimensions": {
    "security": { "status": "NOT READY", "notes": "Credential in source control" },
    "testing":  { "status": "PARTIAL",   "notes": "Happy path only" }
  }
}
```

`status` is one of READY, PARTIAL, NOT READY, NOT APPLICABLE, NOT ASSESSED.

**5.2 Positive Observations** — `positiveObservations`, each with the
repository evidence that supports it. Generic praise does not belong here.

```json
"positiveObservations": [
  { "observation": "Consistent global error handler",
    "evidence": "src/main/mule/global-error-handler.xml" }
]
```

---

## 6. Risk and Recommendation

**6.1 Risk Summary** — `riskSummary`, sorted with CRITICAL first. Themes, not
repeats of the full findings.

**6.2 Top 10 Remediation Priorities** — `remediationPriorities`, sorted by
`priority` and truncated at ten. Rank by production impact, not by severity
alone.

**6.3 Review Limitations** — `limitations`. What could not be verified, and
why. An unverified area is a limitation, never a defect.

**6.4 Overall Risk and Recommendation** — the reconciled verdict, then
`recommendationRationale`.

---

## Appendix A — Complete Findings Inventory

Every finding: ID, severity, category, confidence, title and location.

No finding may be omitted, and these counts must reconcile with section 1.3 —
the generator prints the reconciliation line at the foot of the table.

---

## Appendix B — Finding Evidence Detail

The verbatim `evidenceSnippet` for every finding that supplies one, so a reader
can confirm a finding without opening the repository.

---

## Appendix C — Review Coverage and Boundaries

`coverage` — per review phase, the status and any note.

```json
"coverage": [
  { "phase": "PHASE 10 - Database Analysis", "status": "COMPLETED",
    "notes": "3 DB operations across 2 flows" },
  { "phase": "PHASE 11 - Messaging Analysis", "status": "NOT APPLICABLE",
    "notes": "No messaging connector in the application" }
]
```

Followed by a fixed control table confirming read-only conduct: source not
modified, no Git writes, no dependency changes, no remediation, one report file
created, generated artifacts excluded, every finding evidence-backed,
unverifiable areas recorded as limitations, and verdict reconciliation applied.

---

## Verdict Reconciliation

The generator will not let the narrative contradict the evidence. `overallRisk`
and `overallRecommendation` are honoured only when they are at least as severe
as the findings require:

| Findings present | Minimum risk | Minimum recommendation |
|---|---|---|
| any CRITICAL | CRITICAL | HIGH RISK |
| any HIGH | HIGH | CHANGES REQUIRED |
| any MEDIUM | MEDIUM | CHANGES REQUIRED |
| LOW or NIT only | LOW | APPROVE WITH MINOR CHANGES |
| none | LOW | APPROVE |

A stated verdict more severe than the floor is kept as stated. A stated verdict
less severe is raised, the raise is printed on the console, and section 6.4
records what was stated alongside what the evidence supports.

## Validation Before Success

After saving, the document is re-opened and checked for all nine required
top-level headings — sections 1 to 6 and appendices A to C. A missing section
is a non-zero exit, not a warning.
