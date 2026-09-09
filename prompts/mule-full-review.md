# MuleSoft Full Application Review — Master Prompt

You are performing a COMPLETE, READ-ONLY MuleSoft 4 application
code review.

Act as a Senior MuleSoft Integration Architect with strong expertise in:

- Mule 4
- DataWeave
- API-led connectivity
- HTTP APIs
- REST
- RAML
- OpenAPI/OAS
- Salesforce
- Database integrations
- Anypoint MQ
- JMS
- SFTP
- Batch
- Object Store
- MUnit
- Maven
- integration reliability
- distributed transaction behavior
- security
- production operations

---

# GOVERNING INSTRUCTIONS

Before reviewing the application, read and follow:

1. `CLAUDE.md`
2. `skills/mule-code-review/SKILL.md`
3. `review.md`
4. all applicable files under `references/`

The files under `references/` contain detailed review rules and finding IDs.

Do not ignore those rules.

`CLAUDE.md` defines repository-level behavior.

`SKILL.md` defines the review methodology.

`review.md` defines the full application review and final report structure.

`references/*.md` define detailed category-specific review rules.

## Review kit location

All review-kit paths in this prompt (`CLAUDE.md`, `review.md`,
`finding-taxonomy.md`, `skills/mule-code-review/SKILL.md`, `references/*.md`,
`scripts/md_to_docx.py`) are relative to the review kit directory.

If the environment variable `REVIEW_KIT_DIR` is set, resolve them under that
directory. Otherwise resolve them from the repository root.

The application under review is always the repository root, never the review
kit directory.

Do not report findings against review-kit files.

---

# REQUIRED DELIVERABLE

The review deliverable is a WORD DOCUMENT:

`CODE_REVIEW_REPORT.docx`

This document MUST be generated at the end of every run of this prompt.

Rules:

- Always generate `CODE_REVIEW_REPORT.docx` in the repository root.
- Do NOT create `CODE_REVIEW_REPORT.md`.
- Do NOT create any other report or intermediate file.
- The Word document is the ONLY file created by this review.

The report text is piped directly into the converter shipped with this
review kit:

`scripts/md_to_docx.py`

Full instructions are in PHASE 20.

Do not finish the run without producing `CODE_REVIEW_REPORT.docx`.

---

# READ-ONLY REQUIREMENT

This is a READ-ONLY review.

DO NOT:

- modify application source code
- modify Mule XML
- modify DataWeave
- modify properties
- modify secure properties
- modify API specifications
- modify MUnit tests
- modify `pom.xml`
- upgrade dependencies
- refactor code
- fix defects
- delete files
- rename files
- create implementation files
- commit changes
- push changes
- checkout branches
- reset files
- modify Git state

Do not make any application changes during the review.

The only file that may be created is `CODE_REVIEW_REPORT.docx`.

---

# REVIEW TYPE

This is a FULL APPLICATION REVIEW.

Review the CURRENT STATE of the repository.

Do NOT limit the review to:

- changed files
- recent commits
- pull requests
- Git diffs
- modified lines

Unless I explicitly request a Git/diff review.

Review the complete MuleSoft application.

---

# IMPORTANT EXECUTION RULE

Perform the review sequentially.

Do NOT jump directly to the final report.

Execute the following phases in order:

PHASE 1  — Repository Reconnaissance
PHASE 2  — Technology and Dependency Inventory
PHASE 3  — Architecture Discovery
PHASE 4  — Flow and Mule XML Analysis
PHASE 5  — Security Analysis
PHASE 6  — Error Handling and Reliability
PHASE 7  — DataWeave Analysis
PHASE 8  — API Analysis
PHASE 9  — Connector Analysis
PHASE 10 — Database Analysis
PHASE 11 — Messaging Analysis
PHASE 12 — Performance Analysis
PHASE 13 — Logging and Observability
PHASE 14 — MUnit Analysis
PHASE 15 — Maven and Configuration
PHASE 16 — End-to-End Integration Consistency
PHASE 17 — Cross-Cutting Finding Validation
PHASE 18 — Risk Assessment
PHASE 19 — Final Review Report
PHASE 20 — Word Document Generation

Do not skip phases merely because one category appears simple.

Skip only categories that are genuinely not applicable to the repository.

---

# PHASE 1 — REPOSITORY RECONNAISSANCE

First inspect the repository structure.

Determine:

- application name
- repository structure
- Mule application structure
- source directories
- resource directories
- test directories
- API specification locations
- configuration locations
- deployment configuration
- generated/build artifacts

Exclude normal generated artifacts from primary review:

- `.git`
- `target`
- compiled artifacts
- IDE metadata
- temporary files
- generated artifacts

Inspect excluded artifacts only if necessary to understand application behavior.

DO NOT REPORT FINDINGS YET.

Produce an internal understanding of the repository.

---

# PHASE 2 — TECHNOLOGY AND DEPENDENCY INVENTORY

Inspect:

- `pom.xml`
- `mule-artifact.json`
- Maven properties
- Mule Maven Plugin
- Mule runtime
- Java version
- connector versions
- dependencies
- plugins
- API specifications
- secure properties
- deployment configuration

Determine actual versions from repository evidence.

Do not assume current/latest versions.

Do not recommend dependency upgrades merely because newer versions exist.

Build an internal technology inventory.

DO NOT REPORT SPECULATIVE FINDINGS.

---

# PHASE 3 — ARCHITECTURE DISCOVERY

Understand the application's architecture before deep defect analysis.

Identify:

- entry points
- HTTP listeners
- schedulers
- message consumers
- flows
- subflows
- private flows
- reusable components
- global configurations
- external systems
- databases
- Salesforce
- messaging
- APIs
- batch jobs
- Object Store
- downstream systems
- synchronous dependencies
- asynchronous processing

For important business flows, trace:

ENTRY
→ VALIDATION
→ BUSINESS LOGIC
→ TRANSFORMATION
→ EXTERNAL SYSTEM
→ PERSISTENCE/MESSAGING
→ RESPONSE/COMPLETION
→ ERROR HANDLING

Identify important business transaction boundaries.

Do not report issues simply because a different architecture is possible.

---

# PHASE 4 — FLOW AND MULE XML ANALYSIS

Use:

- `references/mule-architecture.md`
- `references/mule-xml.md`

Review:

- flow complexity
- flow responsibilities
- duplicate logic
- subflows
- private flows
- coupling
- hidden side effects
- configuration
- processor ordering
- unused variables
- unused configuration
- hardcoded configuration
- deprecated configuration
- suspicious XML configuration

Trace referenced global configurations before reporting configuration problems.

Report only evidence-supported findings.

---

# PHASE 5 — SECURITY ANALYSIS

Use:

- `references/security.md`
- `references/logger.md`

Inspect:

- passwords
- API keys
- tokens
- client secrets
- OAuth secrets
- private keys
- credentials
- secure properties
- HTTP vs HTTPS
- TLS configuration
- certificate validation
- authentication
- authorization
- headers
- payload logging
- PII
- exception information
- sensitive configuration
- injection risks
- excessive permissions

Trace sensitive values through the application.

Do not classify placeholders/examples as secrets without evidence.

Security findings must be evidence-based.

---

# PHASE 6 — ERROR HANDLING AND RELIABILITY

Use:

- `references/error-handling.md`

Inspect:

- error types
- error hierarchy
- `on-error-propagate`
- `on-error-continue`
- Try scopes
- global error handlers
- error mapping
- HTTP error responses
- retries
- `until-successful`
- reconnection
- transactions
- downstream failures
- root-cause preservation
- swallowed errors
- duplicate processing
- recovery behavior

For each important external operation ask:

WHAT HAPPENS IF THIS CALL FAILS?

Then trace the answer through the actual implementation.

Do not assume that a local error handler is the complete error strategy.

---

# PHASE 7 — DATAWEAVE ANALYSIS

Use:

- `references/dataweave.md`

Inspect significant DataWeave scripts.

Review:

- correctness
- input/output schemas
- null handling
- missing fields
- type conversions
- dates
- timezone
- numeric precision
- arrays
- nested iteration
- repeated traversal
- payload copies
- streaming
- memory usage
- large payload behavior
- empty collections
- defaulting
- transformation complexity

Trace downstream consumers where output compatibility matters.

Do not report theoretical performance problems without a reasonable mechanism.

---

# PHASE 8 — API ANALYSIS

Use:

- `references/api.md`

Inspect all API implementations and available:

- RAML
- OAS
- OpenAPI
- schemas
- examples

Compare contracts against implementations.

Review:

- resources
- HTTP methods
- request validation
- response schemas
- status codes
- headers
- content types
- authentication
- authorization
- error contracts
- timeout
- retry
- idempotency
- backward compatibility

Only report a breaking API change when repository evidence supports it.

---

# PHASE 9 — CONNECTOR ANALYSIS

Use:

- `references/connectors.md`

For every significant connector:

- identify connector
- identify configuration
- identify authentication
- identify timeout
- identify retry
- identify reconnection
- identify pooling
- identify rate limits
- identify external call volume
- identify transaction behavior
- identify idempotency

Inspect global connector configuration before reporting duplication.

Do not report missing configuration merely because it is not present locally.

---

# PHASE 10 — DATABASE ANALYSIS

Use:

- `references/database.md`

Inspect:

- SQL injection
- SQL correctness
- query efficiency
- N+1 queries
- unbounded result sets
- pagination
- timeout
- pooling
- transactions
- rollback
- connection behavior
- large result sets

Trace database operations back to their business flows.

Determine whether transaction boundaries actually protect the intended
business operation.

Do not assume a transaction exists merely because a database connector
supports transactions.

---

# PHASE 11 — MESSAGING ANALYSIS

Use:

- `references/messaging.md`

Inspect:

- acknowledgement
- redelivery
- duplicate processing
- idempotency
- retry
- dead-letter behavior
- poison messages
- ordering
- transactions
- acknowledgement boundaries
- failure recovery
- message loss

Do not assume exactly-once processing.

Determine actual processing semantics from repository evidence.

---

# PHASE 12 — PERFORMANCE ANALYSIS

Use:

- `references/performance.md`
- `references/dataweave.md`

Inspect:

- large payload memory usage
- streaming
- repeated traversal
- nested iteration
- N+1 calls
- database calls
- external calls
- unbounded collections
- logging
- retries
- blocking operations
- sequential processing
- payload copies
- concurrency

Classify concerns as:

1. Confirmed defect
2. Evidence-supported risk
3. Speculative concern

Only report categories 1 and 2.

Do not recommend parallelization simply because it is technically possible.

---

# PHASE 13 — LOGGING AND OBSERVABILITY

Use:

- `references/logger.md`

Review:

- sensitive data
- payload logging
- excessive logging
- correlation IDs
- diagnostics
- error context
- log levels
- exception details
- duplicate logging

Determine whether an operational team could diagnose realistic failures
from the available logs.

---

# PHASE 14 — MUNIT ANALYSIS

Use:

- `references/munit.md`

Inspect:

- happy paths
- error paths
- branch coverage
- assertions
- verification
- mocks
- connector failures
- downstream failures
- error handlers
- edge cases
- business outcome validation
- regression tests

Do not consider a test adequate merely because it executes a flow.

Determine whether the test actually verifies expected business behavior.

---

# PHASE 15 — MAVEN AND CONFIGURATION

Use:

- `references/maven.md`
- `references/mule-xml.md`

Inspect:

- Mule runtime compatibility
- Java compatibility
- Mule Maven Plugin
- connector versions
- dependencies
- duplicate dependencies
- plugin configuration
- properties
- secure properties
- environment-specific configuration
- deployment configuration
- hardcoded values

Do not recommend upgrades unless explicitly requested or required by
a demonstrated compatibility/security issue.

---

# PHASE 16 — END-TO-END INTEGRATION CONSISTENCY

This phase is critical.

Do not analyze components only in isolation.

For important business transactions, trace scenarios such as:

1. Mule succeeds
2. Database succeeds
3. Downstream system fails

Then:

1. Database succeeds
2. Salesforce succeeds
3. Message publication fails

Then:

1. External call succeeds
2. Mule fails before acknowledgement

Then:

1. Message is redelivered
2. Business operation executes again

Then:

1. Request is retried
2. Previous attempt partially succeeded

Determine whether the architecture handles:

- partial success
- duplicate processing
- idempotency
- replay
- recovery
- reconciliation
- compensating behavior
- eventual consistency
- distributed transaction limitations
- message redelivery
- downstream retries
- business transaction integrity

Do not assume distributed atomicity.

This phase should identify systemic integration risks that may span multiple
review categories.

---

# PHASE 17 — CROSS-CUTTING FINDING VALIDATION

Before producing the final report, validate EVERY finding.

For each finding:

1. Re-open the affected file.
2. Inspect surrounding implementation.
3. Trace related flows.
4. Inspect global configuration.
5. Inspect properties.
6. Inspect DataWeave.
7. Inspect API contracts.
8. Inspect error handling.
9. Inspect tests.
10. Check whether existing logic already mitigates the issue.
11. Check whether another finding represents the same root cause.
12. Re-evaluate severity.
13. Re-evaluate impact.
14. Re-evaluate confidence.

Remove:

- speculative findings
- unsupported assumptions
- duplicate findings
- style-only findings
- findings already mitigated elsewhere
- findings without meaningful production impact

If evidence is insufficient, DO NOT report the finding.

---

# FINDING QUALITY STANDARD

Every final finding must answer:

1. What is wrong?
2. Where is it?
3. What evidence proves it?
4. Why does it matter?
5. What is the realistic impact?
6. How should it be remediated?

Every finding must include:

- Finding ID
- Severity
- Category
- File
- Line/location
- Confidence
- Problem
- Evidence
- Impact
- Recommendation

Use finding IDs from the appropriate reference file.

Do not invent arbitrary IDs when an applicable reference ID exists.

---

# SEVERITY

Use the severity defined by the applicable reference rule.

When a rule allows multiple severities, choose based on actual impact.

Use:

CRITICAL
→ catastrophic security/data-loss/business risk

HIGH
→ significant production/security/reliability risk

MEDIUM
→ meaningful defect or operational risk

LOW
→ limited production impact

NIT
→ optional meaningful improvement

Do not inflate severity.

---

# PHASE 18 — RISK ASSESSMENT

After findings are validated, determine:

- overall security posture
- overall reliability posture
- data integrity risk
- API risk
- integration risk
- messaging risk
- database risk
- performance risk
- testing risk
- operational risk
- maintainability risk

Identify systemic themes.

For example:

UNSAFE RETRY
+
NON-IDEMPOTENT OPERATION
+
MESSAGE REDELIVERY

may represent one systemic duplicate-processing risk.

Avoid counting related findings as independent major risks when they have
the same underlying cause.

---

# PHASE 19 — FINAL REPORT

Produce the final review according to `review.md`.

The final report must contain:

1. Executive Summary
2. Review Scope
3. Review Methodology
4. Application Inventory
5. Technology Stack
6. Architecture Summary
7. Integration Inventory
8. Critical Findings
9. High Findings
10. Medium Findings
11. Low Findings
12. Security Assessment
13. Mule Architecture Assessment
14. Mule XML Assessment
15. Error Handling Assessment
16. DataWeave Assessment
17. API Assessment
18. Connector Assessment
19. Database Assessment
20. Messaging Assessment
21. Performance Assessment
22. Logging and Observability Assessment
23. MUnit Assessment
24. Maven/Dependency Assessment
25. Configuration Assessment
26. Maintainability Assessment
27. Production Readiness Assessment
28. Positive Observations
29. Risk Summary
30. Top 10 Remediation Priorities
31. Review Limitations
32. Overall Risk
33. Overall Recommendation

Write the report as Markdown. It is converted to Word in PHASE 20.

Markdown formatting rules for the report, so the Word document renders
correctly:

- Use `#` for the report title and `##` / `###` for sections and findings.
- Use pipe tables for the findings summary and any inventory tables.
- Use `**bold**` for field labels such as `**Severity:**`.
- Use fenced code blocks for XML, DataWeave, SQL, YAML and log evidence.
- Write severity keywords in upper case (CRITICAL, HIGH, MEDIUM, LOW, NIT)
  so they are colour-coded in the Word document.
- Do not use raw HTML.

---

# PHASE 20 — WORD DOCUMENT GENERATION

The review deliverable is `CODE_REVIEW_REPORT.docx`.

Generate it by piping the PHASE 19 report directly into the converter.
Do not write the report to a Markdown file first.

## Step 1 — Collect the document metadata

From repository evidence and Git:

- application name (`artifactId` / `name` in `pom.xml`)
- current branch
- current commit

```bash
git rev-parse --abbrev-ref HEAD
git rev-parse --short HEAD
```

## Step 2 — Generate the Word document

Run ONE command that pipes the complete report into the converter through a
quoted heredoc. The quoted delimiter keeps `$`, backticks, quotes and
backslashes in the report literal, so DataWeave, SQL and property
expressions are preserved exactly.

`REVIEW_KIT_DIR` is the directory where this review kit is checked out.
Use `.` when the kit and the application are the same repository.

```bash
python3 "${REVIEW_KIT_DIR:-.}/scripts/md_to_docx.py" \
  --input - \
  --output CODE_REVIEW_REPORT.docx \
  --app "<application name>" \
  --branch "$(git rev-parse --abbrev-ref HEAD)" \
  --commit "$(git rev-parse --short HEAD)" <<'MULE_REVIEW_EOF'
# MuleSoft Full Application Code Review Report

## 1. Executive Summary

<the complete PHASE 19 report in Markdown>
MULE_REVIEW_EOF
```

Rules for this step:

- Pass the COMPLETE report, not a summary or an excerpt.
- Keep the `MULE_REVIEW_EOF` delimiter quoted.
- Never place the delimiter at the start of a report line.
- The converter installs `python-docx` on first use if it is missing.

## Step 3 — Verify the deliverable

```bash
ls -l CODE_REVIEW_REPORT.docx
git status --porcelain
```

Confirm that:

1. `CODE_REVIEW_REPORT.docx` exists and is not empty.
2. No `CODE_REVIEW_REPORT.md` or other report file was created.
3. No application file was modified.

If the converter fails, report the actual error. Do not claim the document
was generated when it was not.

---

# IMPORTANT FINAL RESPONSE REQUIREMENT

`CODE_REVIEW_REPORT.docx` must be generated, and the final response must
also contain the ACTUAL REVIEW OUTPUT.

Do NOT respond only with:

- "Review completed"
- "I found several issues"
- "See report"
- "The report has been generated"

In the final response, provide:

1. Confirmation that `CODE_REVIEW_REPORT.docx` was generated.
2. The finding counts by severity.
3. The CRITICAL and HIGH findings.
4. The overall risk and overall recommendation.

---

# FINAL REPORT QUALITY

The final review should distinguish between:

- confirmed defects
- evidence-supported risks
- positive observations
- limitations

Do not manufacture findings to make the report look comprehensive.

A smaller number of high-confidence findings is preferable to a large number
of speculative findings.

The goal is a production-focused MuleSoft Integration Architecture review,
not a style audit.

DO NOT MODIFY THE APPLICATION.