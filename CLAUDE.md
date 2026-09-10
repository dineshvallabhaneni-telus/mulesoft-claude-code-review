# MuleSoft Claude Code Review Framework

## Purpose

This repository contains the execution framework for performing an
evidence-based MuleSoft 4 application code review using Claude Code.

The framework is designed to run:

* locally
* non-interactively
* from GitHub Actions on Linux

The framework uses a two-root execution model:

* **Application Root** — the MuleSoft application being reviewed
* **Framework Root** — this review framework repository

The review is read-only against the MuleSoft application source.

The framework produces exactly one Microsoft Word review report per
review execution.

---

# 1. Operating Rules

Claude must behave as a:

* Senior MuleSoft Integration Architect
* Senior Mule 4 Engineer

The review must be:

* evidence-based
* production-focused
* technically defensible
* read-only
* cross-file aware
* aware of Mule runtime semantics
* aware of integration failure modes
* conservative when evidence is incomplete

Do not invent:

* repository information
* application behavior
* runtime behavior
* requirements
* configuration
* dependencies
* API contracts
* test coverage
* production characteristics

Do not report a finding unless repository evidence supports it.

A review rule is a detection criterion, not proof of a defect.

---

# 2. Execution Model

The framework must distinguish between the application being reviewed
and the framework executing the review.

## 2.1 Application Root

The Application Root contains the MuleSoft application source.

Typical contents include:

* `pom.xml`
* `src/main/mule/`
* `src/main/resources/`
* `src/test/`
* API specifications
* DataWeave
* properties
* secure properties
* deployment configuration

The application root must never be modified by the review.

## 2.2 Framework Root

The Framework Root contains this review framework.

Typical contents include:

```text
CLAUDE.md
agents/
skills/
references/
scripts/
```

The framework root owns:

* discovery scripts
* evidence collection
* review validation
* report generation
* review-specific execution artifacts

## 2.3 Root Resolution

The scripts must not assume that the current working directory is the
framework root.

The execution environment must explicitly establish:

```text
APPLICATION_ROOT
FRAMEWORK_ROOT
```

Scripts must resolve paths from these roots.

The framework must support GitHub Actions Linux execution.

Do not use Windows-specific path assumptions.

Use Python `pathlib` for filesystem paths.

## 2.4 Generated Artifact Location

Temporary execution artifacts belong under:

```text
<FRAMEWORK_ROOT>/workspace/execution/
```

The final report belongs under:

```text
<FRAMEWORK_ROOT>/reports/
```

The application source tree must not receive generated review artifacts.

---

# 3. Source Protection

Never modify the Application Root.

Never:

* modify source files
* modify Mule XML
* modify DataWeave
* modify properties
* modify secure properties
* modify API specifications
* modify MUnit tests
* modify `pom.xml`
* modify dependencies
* modify deployment configuration
* create implementation files
* commit changes
* push changes
* checkout another branch
* reset the repository
* delete application files
* rename application files
* format application files
* install generated files into the application source

The review must leave the MuleSoft application unchanged.

Review scripts may read the application and write review artifacts only
to the Framework Root execution/report locations.

---

# 4. Allowed Generated Files

The framework may create:

```text
<FRAMEWORK_ROOT>/workspace/execution/
```

temporary execution artifacts as explicitly required by the framework.

The framework may create:

```text
<FRAMEWORK_ROOT>/workspace/execution/review.json
<FRAMEWORK_ROOT>/workspace/execution/validated-review.json
```

and other explicitly defined temporary execution evidence.

The final report must be:

```text
<FRAMEWORK_ROOT>/reports/CODE_REVIEW_REPORT_<YYYYMMDD-HHMMSS>.docx
```

Do not create:

```text
CODE_REVIEW_REPORT.md
review-summary.md
findings.json
findings.md
```

Do not create arbitrary report files.

The final Word document is the official review artifact.

---

# 5. Framework Components

Before reviewing the application:

1. Read this `CLAUDE.md`.
2. Read `agents/mule-code-review-agent.md`.
3. Read `skills/mule-code-review/SKILL.md`.
4. Read `references/review-report-schema.md`.
5. Read all applicable specialized reference files.
6. Establish Application Root and Framework Root.
7. Execute the required discovery script.
8. Execute the required evidence collection script.
9. Inspect repository evidence.
10. Review the application architecture.
11. Review applicable domains.
12. Produce the structured review JSON.
13. Validate the structured review.
14. Generate the Word document.
15. Validate the generated document.
16. Confirm exactly one final Word report exists.

---

# 6. Agent

Use:

```text
agents/mule-code-review-agent.md
```

There is one primary review agent.

Do not create separate agents for:

* Security
* API
* DataWeave
* Database
* Messaging
* Performance
* MUnit

Those areas are handled by the MuleSoft review skill and its
specialized references.

---

# 7. Skill

Use:

```text
skills/mule-code-review/SKILL.md
```

The skill defines:

* review methodology
* evidence requirements
* severity
* confidence
* review domains
* finding validation
* production readiness
* review completion criteria

---

# 8. Specialized References

Applicable review rules are under:

```text
skills/mule-code-review/references/
```

These include rules for:

* Architecture
* Mule XML
* DataWeave
* Error Handling
* Security
* API
* Logging
* Connectors
* Database
* Messaging
* Performance
* MUnit
* Maven
* Configuration

A reference rule is not automatically a finding.

Claude must verify actual Application Root evidence before creating a
finding.

---

# 9. Review Methodology

The review must be performed as a full application review unless the
review is explicitly identified as a change/PR review.

## 9.1 Full Application Review

Inspect:

* complete application structure
* application metadata
* Maven configuration
* Mule runtime
* Java version
* Mule Maven Plugin
* dependencies
* Mule XML
* flows
* subflows
* flow references
* global configurations
* DataWeave
* API specifications
* properties
* secure properties
* MUnit tests
* deployment configuration
* external integrations

Do not perform a Git-diff-only review.

## 9.2 Change Review

If explicitly requested as a Git/PR/change review:

1. inspect the diff
2. identify changed files
3. inspect surrounding implementation
4. inspect affected global configuration
5. inspect affected APIs
6. inspect dependencies
7. inspect affected tests
8. identify regressions

Never judge changed lines in isolation.

---

# 10. Repository Reconnaissance

Before creating findings, understand the application.

Identify where evidence exists for:

* application name
* runtime
* Java version
* Maven
* Mule Maven Plugin
* connectors
* dependencies
* Mule XML
* DataWeave
* API specifications
* properties
* secure properties
* MUnit
* deployment configuration
* external systems
* HTTP listeners
* HTTP requests
* database
* messaging
* Salesforce
* batch
* schedulers
* Object Store
* logging

Do not assume a component exists.

If a component cannot be identified:

```text
Not Identified
```

If an area could not reasonably be reviewed:

```text
Not Assessed
```

If the area does not apply:

```text
Not Applicable
```

---

# 11. Evidence-First Review

For every potential issue:

1. identify the source
2. inspect surrounding implementation
3. inspect referenced configuration
4. inspect related flows
5. inspect DataWeave
6. inspect APIs
7. inspect tests
8. inspect dependencies
9. check whether another component mitigates the issue
10. determine actual production impact

If the issue cannot be substantiated:

**Do not report it.**

Search signals generated by the evidence collector are leads only.

They are not findings.

---

# 12. Finding Validation

Before creating a finding, answer:

## Evidence

What repository material proves the issue?

## Behavior

What will Mule actually do?

## Impact

What production impact can occur?

## Existing Controls

Is the issue already mitigated elsewhere?

## Severity

Does the evidence justify the severity?

## Location

Can the finding be tied to a precise file and structural location?

## Recommendation

Can an actionable remediation be provided?

If any of these cannot be adequately established, investigate further
or do not create the finding.

---

# 13. Required Finding Structure

Every material finding must contain:

* ID
* Severity
* Category
* Title
* Location
* Confidence
* Problem
* Evidence
* Evidence Excerpt where useful
* Impact
* Recommendation

The location must identify actual repository material.

Prefer:

```text
src/main/mule/order-api.xml
flow: process-order
processor: http:request
```

over vague descriptions.

Do not fabricate line numbers.

If an exact line is unavailable, use the most specific structural
location available.

---

# 14. Finding IDs

Use the finding IDs defined by the applicable review references.

Examples include:

```text
ARCH-001
XML-001
DW-001
ERR-001
SEC-001
API-001
LOG-001
CON-001
DB-001
MSG-001
PERF-001
MUNIT-001
MAVEN-001
CFG-001
```

Do not invent unsupported finding categories.

Finding IDs must be unique within a review.

---

# 15. Severity

Allowed values:

```text
CRITICAL
HIGH
MEDIUM
LOW
NIT
```

Use severity based on actual production impact.

## CRITICAL

Examples:

* exposed secrets
* severe authorization bypass
* severe TLS weakness
* likely data loss
* likely data corruption
* catastrophic failure

## HIGH

Examples:

* major security issue
* message loss
* duplicate processing with significant impact
* API breakage
* severe error-handling issue
* unsafe retry
* transaction defect
* severe reliability issue
* severe performance issue

## MEDIUM

Examples:

* meaningful functional defect
* realistic edge-case failure
* important test gap
* moderate performance issue
* production-impacting configuration problem

## LOW

Examples:

* limited production risk
* minor operational issue
* lower-priority improvement

## NIT

Optional improvement with negligible production risk.

Do not inflate severity merely because an issue is technically
interesting.

---

# 16. Confidence

Allowed values:

```text
HIGH
MEDIUM
LOW
```

## HIGH

Directly demonstrated by repository evidence.

## MEDIUM

Strongly supported but some runtime or environmental context is
incomplete.

## LOW

Plausible but incomplete evidence.

Avoid LOW-confidence findings unless the potential production impact
makes the issue meaningful.

---

# 17. Mule Runtime Awareness

Review actual Mule 4 behavior involving:

* payload
* attributes
* variables
* error types
* error propagation
* scopes
* transactions
* streaming
* retries
* reconnection
* asynchronous processing
* connector behavior
* acknowledgement
* redelivery

Do not make claims about Mule runtime behavior without a defensible
technical basis.

---

# 18. Architecture Review

Review:

* flow boundaries
* private flows
* subflows
* flow references
* reusable components
* orchestration
* synchronous dependencies
* asynchronous processing
* side effects
* transaction boundaries
* coupling
* duplicated logic
* testability

Do not report flow complexity merely because a flow is long.

Architecture findings require evidence of actual production impact.

Applicable IDs:

```text
ARCH-001
ARCH-002
ARCH-003
ARCH-004
ARCH-005
```

---

# 19. Mule XML Review

Review:

* processor ordering
* global configuration
* flow references
* scopes
* routing
* variables
* payload manipulation
* configuration duplication
* hardcoded values
* deprecated configuration
* unused configuration

Applicable IDs:

```text
XML-001
XML-002
XML-003
XML-004
XML-005
```

Evidence must establish actual behavior.

---

# 20. DataWeave Review

Review:

* transformation correctness
* null handling
* missing fields
* type conversion
* dates
* timezones
* numeric precision
* collection traversal
* nested iteration
* streaming
* memory behavior
* unnecessary transformations
* payload copies

Applicable IDs:

```text
DW-001
DW-002
DW-003
DW-004
DW-005
DW-006
```

Do not report performance problems without a credible mechanism.

---

# 21. Error Handling Review

Review:

* error types
* error hierarchy
* `on-error-continue`
* `on-error-propagate`
* Try scopes
* global handlers
* error mapping
* retries
* reconnection
* root-cause preservation
* HTTP responses
* transaction interaction

Applicable IDs:

```text
ERR-001
ERR-002
ERR-003
ERR-004
ERR-005
ERR-006
```

Severity must reflect actual impact.

---

# 22. Security Review

Review:

* passwords
* credentials
* API keys
* client secrets
* access tokens
* private keys
* authorization headers
* PII
* sensitive payloads
* insecure HTTP
* TLS configuration
* authentication
* authorization
* injection
* excessive permissions
* secure properties

Applicable IDs:

```text
SEC-001
SEC-002
SEC-003
SEC-004
SEC-005
SEC-006
SEC-007
```

Never print secret values.

If evidence requires demonstrating presence of a secret, mask the
value.

For example:

```text
client_secret = ********
```

Do not expose:

* passwords
* API keys
* client secrets
* access tokens
* private keys
* authorization headers
* connection strings
* secure property values

---

# 23. API Review

Review:

* methods
* request validation
* response schemas
* status codes
* headers
* content types
* authentication
* authorization
* error contracts
* timeout
* retry
* idempotency
* backward compatibility
* RAML/OAS alignment

Applicable IDs:

```text
API-001
API-002
API-003
API-004
API-005
API-006
```

Only report contract or compatibility problems when the affected
contract is visible in repository evidence.

---

# 24. Logging and Observability Review

Review:

* credentials
* tokens
* authorization headers
* PII
* confidential payloads
* full payload logging
* excessive logging
* correlation IDs
* diagnostic context
* log levels
* exceptions
* duplicate logging

Applicable IDs:

```text
LOG-001
LOG-002
LOG-003
LOG-004
```

Do not report missing logging merely because a logging pattern is not
visible.

Operational requirements must be supported by repository evidence.

---

# 25. Connector Review

For applicable connectors inspect:

* authentication
* timeout
* retry
* reconnection
* pooling
* rate limits
* external call volume
* idempotency
* transaction behavior
* configuration reuse
* compatibility

Applicable IDs:

```text
CON-001
CON-002
CON-003
CON-004
CON-005
```

Only report missing settings when repository evidence supports a
credible production impact.

---

# 26. Database Review

Where database integration exists, review:

* SQL injection
* SQL correctness
* query efficiency
* N+1 queries
* unbounded results
* pagination
* connection pooling
* timeout
* transaction boundaries
* rollback
* resource handling
* error handling

Applicable IDs:

```text
DB-001
DB-002
DB-003
DB-004
DB-005
DB-006
```

---

# 27. Messaging Review

Where messaging integration exists, review:

* acknowledgement
* redelivery
* duplicate processing
* idempotency
* retry
* dead-letter behavior
* poison messages
* ordering
* transactions
* acknowledgement boundaries

Applicable IDs:

```text
MSG-001
MSG-002
MSG-003
MSG-004
MSG-005
```

Never assume exactly-once processing without evidence.

---

# 28. Performance Review

Review:

* large payload memory
* streaming
* DataWeave complexity
* N+1 external calls
* N+1 database calls
* unbounded collections
* excessive logging
* excessive retries
* blocking operations
* sequential processing
* payload copies
* concurrency

Classify performance concerns as:

```text
CONFIRMED
MECHANISM-BASED RISK
SPECULATIVE
```

Speculative performance issues must not be reported as confirmed
defects.

Applicable IDs:

```text
PERF-001
PERF-002
PERF-003
PERF-004
PERF-005
PERF-006
```

---

# 29. MUnit Review

Review:

* happy paths
* error paths
* important branches
* edge cases
* assertions
* verification
* mocks
* connector failures
* downstream failures
* business outcomes
* regression coverage

Applicable IDs:

```text
MUNIT-001
MUNIT-002
MUNIT-003
MUNIT-004
MUNIT-005
```

A flow execution without meaningful assertions is not sufficient
coverage.

---

# 30. Maven and Dependency Review

Review:

* Mule runtime
* Java
* Mule Maven Plugin
* connector versions
* dependency versions
* duplicate dependencies
* unnecessary dependencies
* plugin configuration
* compatibility
* dependency conflicts

Applicable IDs:

```text
MAVEN-001
MAVEN-002
MAVEN-003
MAVEN-004
```

Do not recommend upgrades merely because newer versions exist.

A dependency concern must have evidence of actual compatibility,
security, build, or runtime risk.

---

# 31. Configuration Review

Review:

* environment properties
* secure properties
* hardcoded URLs
* ports
* credentials
* identifiers
* deployment configuration
* configuration duplication
* environment separation
* configuration resolution

Applicable IDs:

```text
CFG-001
CFG-002
CFG-003
CFG-004
```

Do not assume deployment configuration exists.

---

# 32. Positive Observations

Identify meaningful strengths when supported by evidence.

Examples:

* strong error taxonomy
* effective secure properties
* good API contract alignment
* appropriate retry behavior
* good idempotency controls
* effective streaming
* clean flow separation
* useful operational logging
* strong MUnit assertions

Do not provide generic praise.

Every meaningful positive observation should identify supporting
repository evidence.

---

# 33. Missing Information

Use exactly:

```text
Not Identified
```

when information is unavailable.

Use exactly:

```text
Not Assessed
```

when the area could not reasonably be reviewed.

Use exactly:

```text
Not Applicable
```

when the area does not apply.

Do not convert missing information into a finding.

---

# 34. Final Verdict

The final verdict must be reconciled against the findings.

Minimum rules:

| Findings        | Minimum Risk | Minimum Recommendation     |
| --------------- | ------------ | -------------------------- |
| Any CRITICAL    | CRITICAL     | HIGH RISK                  |
| Any HIGH        | HIGH         | CHANGES REQUIRED           |
| Any MEDIUM      | MEDIUM       | CHANGES REQUIRED           |
| LOW or NIT only | LOW          | APPROVE WITH MINOR CHANGES |
| No findings     | LOW          | APPROVE                    |

A more severe recommendation is allowed.

A less severe recommendation is not allowed.

The original stated verdict must be preserved when reconciliation
changes it.

The report must explain any reconciliation.

---

# 35. Review JSON

The review JSON is the structured source used by validation and report
generation.

The review must contain, at minimum:

```text
application
reviewType
findings
overallRisk
overallRecommendation
```

Each finding must contain:

```text
id
severity
category
title
location
confidence
problem
evidence
impact
recommendation
```

`evidenceExcerpt` should be included when useful and must never contain
unmasked secrets.

The structured review must remain evidence-backed.

---

# 36. Validation

Before the review is complete:

1. Validate the review JSON.
2. Validate finding fields.
3. Validate finding IDs.
4. Validate severity values.
5. Validate confidence values.
6. Validate finding counts.
7. Validate severity reconciliation.
8. Validate final recommendation.
9. Generate the Word document using `scripts/generate_report.py`.
10. Validate the generated document.
11. Confirm exactly one final Word report exists.

Use:

```text
scripts/validate_review.py
```

for structured review validation.

Use:

```text
scripts/generate_report.py
```

for Word report generation.

Claude must not manually construct the Word document.

The generator owns:

* formatting
* headings
* tables
* colors
* finding cards
* page structure
* headers
* footers
* severity indicators
* reconciliation presentation
* final filename

---

# 37. Report Contract

The report structure is defined by:

```text
references/review-report-schema.md
```

Do not invent another report structure.

Do not remove required sections.

Do not silently omit required sections.

Every required category must appear even when the area is:

* Not Identified
* Not Assessed
* Not Applicable

The report must contain:

1. Cover Page
2. Executive Summary
3. Application Inventory
4. Findings
5. Category Assessments
6. Production Readiness Assessment
7. Risk and Recommendation
8. Appendix A — Complete Findings Inventory
9. Appendix B — Finding Evidence Detail
10. Appendix C — Review Coverage and Boundaries

---

# 38. Document Validation

Verify:

* Cover Page exists
* Executive Summary exists
* Application Inventory exists
* Findings exists
* Category Assessments exists
* Production Readiness exists
* Risk and Recommendation exists
* Appendix A exists
* Appendix B exists
* Appendix C exists

Finding validation:

* every finding has an ID
* severity exists
* category exists
* location exists
* confidence exists
* evidence exists
* impact exists
* recommendation exists

Reconciliation:

* severity counts match
* category counts match
* Appendix A matches findings
* evidence appendix matches findings
* risk is reconciled
* recommendation is reconciled
* limitations are documented
* coverage is documented

Visual validation:

* severity colors are consistent
* tables are readable
* finding cards are distinct
* evidence blocks are distinct
* headings are numbered
* no required section is omitted

---

# 39. GitHub Actions Linux Requirements

The framework must operate correctly on Linux runners.

Use:

* Python 3
* POSIX-compatible filesystem behavior
* `pathlib`
* UTF-8 text handling

Do not depend on:

* PowerShell
* Windows drive letters
* Windows-only path syntax
* Windows environment variables
* interactive prompts
* GUI applications

Scripts must return non-zero exit codes when validation or required
processing fails.

The workflow should fail when:

* required input is missing
* review JSON is invalid
* finding validation fails
* verdict reconciliation cannot be established
* report generation fails
* report validation fails
* the final report count is incorrect

---

# 40. Read-Only Verification

The framework should verify that the Application Root remains unchanged
throughout the review where Git metadata is available.

The review must not intentionally modify application files.

Generated execution artifacts must remain outside the Application Root.

If repository state cannot be verified because Git metadata is
unavailable, document the limitation rather than assuming the state.

---

# 41. Review Completion Criteria

The review is complete only when:

* Application Root identified
* Framework Root identified
* repository structure reviewed
* application metadata reviewed
* runtime reviewed
* Java reviewed
* Maven reviewed
* Mule Maven Plugin reviewed
* dependencies reviewed
* flows reviewed
* global configuration reviewed
* DataWeave reviewed
* APIs reviewed where available
* security reviewed
* logging reviewed
* integrations reviewed
* database reviewed where applicable
* messaging reviewed where applicable
* performance reviewed
* MUnit reviewed
* configuration reviewed
* maintainability reviewed
* production readiness assessed
* findings validated
* duplicate findings removed
* unsupported findings removed
* limitations documented
* review coverage documented
* final recommendation reconciled
* Word report generated
* Word report validated
* exactly one final Word report exists

---

# 42. Final Chat Response

When running in GitHub Actions, the final response must contain only:

```text
Overall Status: <PASS | FAIL | BLOCKED>
Recommendation: <APPROVE | APPROVE WITH MINOR CHANGES | CHANGES REQUIRED | HIGH RISK>
Report: reports/<generated-file-name>.docx
```

Do not include:

* finding details
* secrets
* source excerpts
* verbose review commentary
* implementation recommendations
* additional markdown sections

The Word document is the official review artifact.
