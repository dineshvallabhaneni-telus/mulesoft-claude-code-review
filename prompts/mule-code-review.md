# MuleSoft Code Review — Execution Prompt

You are executing the MuleSoft application code review defined by this repository's review framework.

You are operating in a Linux GitHub Actions environment.

The review is read-only against the MuleSoft application.

---

## 1. Execution Context

The workflow provides these environment variables:

```text
APPLICATION_ROOT
FRAMEWORK_ROOT
REVIEW_TYPE
```

Use them as follows:

* `APPLICATION_ROOT` = MuleSoft application being reviewed.
* `FRAMEWORK_ROOT` = root directory containing this review framework.
* `REVIEW_TYPE` = review mode, normally `FULL_APPLICATION`.

Do not assume the application and framework share the same directory.

Before doing any review work, verify that both paths exist.

---

## 2. Read the Framework Instructions

Before inspecting the application, read:

```text
$FRAMEWORK_ROOT/CLAUDE.md
$FRAMEWORK_ROOT/agents/mule-code-review-agent.md
$FRAMEWORK_ROOT/skills/mule-code-review/SKILL.md
$FRAMEWORK_ROOT/references/review-report-schema.md
```

Then read the applicable specialized references under:

```text
$FRAMEWORK_ROOT/skills/mule-code-review/references/
```

Use the repository's actual reference files as the authoritative detection criteria for their respective domains.

A reference rule is a detection criterion, not automatic proof of a defect.

---

## 3. Read Discovery and Evidence

Read:

```text
$FRAMEWORK_ROOT/workspace/execution/application-discovery.json
$FRAMEWORK_ROOT/workspace/execution/review-evidence.json
```

Use these as reconnaissance and evidence aids.

Do not treat keyword matches as findings.

Inspect the actual application source under:

```text
$APPLICATION_ROOT
```

Discovery and evidence files must never replace direct source inspection.

---

## 4. Review Objective

Perform a complete, evidence-based, production-focused MuleSoft 4 application review.

Understand the application architecture before judging individual files.

Inspect applicable:

* application architecture
* flow boundaries
* private flows
* subflows
* flow references
* orchestration
* Mule XML
* global configuration
* DataWeave
* error handling
* security
* APIs
* API specifications
* logging and observability
* connectors
* database access
* messaging
* performance
* MUnit
* Maven
* dependencies
* configuration
* maintainability
* production readiness

Trace important flows across files.

Inspect related configuration, properties, API specifications, dependencies, DataWeave, tests, and integration behavior where applicable.

---

## 5. Mule Runtime Analysis

Base runtime conclusions on defensible Mule 4 behavior.

Consider, where applicable:

* payload
* attributes
* variables
* scopes
* error types
* error propagation
* `on-error-propagate`
* `on-error-continue`
* Try scopes
* transactions
* retries
* reconnection
* acknowledgement
* redelivery
* idempotency
* streaming
* asynchronous processing
* synchronous dependencies
* connector behavior
* downstream failures
* timeout behavior
* resource usage

Do not claim runtime behavior unless technically defensible from the implementation and Mule semantics.

---

## 6. Evidence-First Decision Process

For every potential issue:

1. Identify the source.
2. Inspect the surrounding implementation.
3. Inspect referenced global configuration.
4. Inspect related flows.
5. Inspect DataWeave.
6. Inspect API contracts where applicable.
7. Inspect properties and configuration.
8. Inspect dependencies.
9. Inspect MUnit tests.
10. Check whether another component mitigates the issue.
11. Determine what Mule will actually do.
12. Determine the realistic production impact.
13. Determine severity.
14. Determine confidence.
15. Determine the most precise supported location.
16. Determine actionable remediation.
17. Validate the finding.
18. Report it only if repository evidence supports it.

If the issue cannot be substantiated:

```text
DO NOT REPORT IT.
```

Do not create findings merely because:

* another implementation is possible
* a setting could theoretically be added
* a newer dependency version exists
* a flow is long
* logging could be improved
* a requirement is unknown
* runtime metrics are unavailable
* a design preference differs from your preference

---

## 7. Cross-File Analysis

Do not inspect changed or individual files in isolation.

Follow references between:

* flows
* subflows
* flow references
* global configurations
* properties
* secure properties
* DataWeave
* APIs
* connectors
* database operations
* messaging
* error handlers
* MUnit tests
* Maven dependencies
* deployment configuration

A potential issue in one file may be mitigated or caused by another file.

Validate the complete behavior before creating a finding.

---

## 8. Security

Review for:

* secrets
* credentials
* API keys
* client secrets
* access tokens
* private keys
* authorization headers
* sensitive payloads
* PII
* insecure HTTP
* TLS weaknesses
* authentication weaknesses
* authorization weaknesses
* injection risks
* excessive permissions
* secure-property usage

Never expose secret values.

If a secret is detected, describe its presence and location without printing its value.

Mask sensitive evidence where necessary.

Do not place credentials, tokens, private keys, secure property values, or authorization header values into `review.json`.

---

## 9. Performance

Only report performance problems with a credible mechanism.

Classify performance observations appropriately as:

```text
CONFIRMED
MECHANISM-BASED RISK
SPECULATIVE
```

Do not report speculative issues as confirmed defects.

Consider:

* large payloads
* payload materialization
* streaming
* DataWeave complexity
* nested iteration
* N+1 external calls
* N+1 database calls
* unbounded collections
* unbounded database results
* excessive logging
* excessive retries
* blocking operations
* sequential processing
* payload copies
* concurrency

---

## 10. Messaging

Where messaging exists, inspect:

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

Never assume exactly-once processing without evidence.

---

## 11. API Review

Where RAML or OpenAPI specifications are available, compare implementation behavior with the visible contract.

Inspect:

* methods
* request validation
* response schemas
* status codes
* headers
* content types
* authentication
* authorization
* error contracts
* timeout behavior
* retry behavior
* idempotency
* backward compatibility

Only report compatibility problems when the affected contract is visible in repository evidence.

---

## 12. Database Review

Where database access exists, inspect:

* SQL injection
* SQL correctness
* query efficiency
* N+1 access
* unbounded result retrieval
* pagination
* connection pooling
* timeout
* transactions
* rollback
* resource handling
* error handling

Do not report a missing setting without establishing production impact from repository evidence.

---

## 13. MUnit Review

Inspect meaningful coverage of:

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
* regression scenarios

A flow execution without meaningful assertions is not sufficient coverage.

Do not create a test-gap finding solely because additional tests are conceivable.

---

## 14. Dependency Review

Inspect:

* Mule runtime
* Java version
* Mule Maven Plugin
* connector versions
* dependency versions
* duplicate dependencies
* unnecessary dependencies
* plugin configuration
* compatibility
* dependency conflicts

Do not recommend upgrades merely because newer versions exist.

A dependency finding requires an identifiable technical or compatibility concern.

---

## 15. Finding Rules

Every material finding must contain:

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

An `evidenceExcerpt` may be included when useful and safe.

Allowed severity values:

```text
CRITICAL
HIGH
MEDIUM
LOW
NIT
```

Allowed confidence values:

```text
HIGH
MEDIUM
LOW
```

Finding IDs should use the appropriate domain prefix defined by the applicable reference.

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

Do not duplicate findings.

Group occurrences when they have the same:

* root cause
* impact
* remediation

Separate findings when root cause, impact, remediation, or severity materially differs.

---

## 16. Severity

Use the framework severity definitions.

As a minimum:

### CRITICAL

Use for issues such as:

* exposed secrets
* severe authorization bypass
* severe TLS weakness
* likely data loss
* likely data corruption
* catastrophic failure

### HIGH

Use for issues such as:

* major security issues
* message loss
* duplicate processing
* API breakage
* severe error handling problems
* unsafe retry
* transaction defects
* severe reliability issues
* severe performance issues

### MEDIUM

Use for issues such as:

* meaningful functional defects
* realistic edge-case failures
* important test gaps
* moderate performance issues
* production-impacting configuration problems

### LOW

Use for:

* limited production risk
* minor operational issues
* lower-priority improvements

### NIT

Use only for optional, low-impact improvements.

Severity must reflect actual evidence and production impact.

---

## 17. Confidence

Use:

### HIGH

The issue is directly demonstrated by repository evidence.

### MEDIUM

The issue is strongly supported but some context is incomplete.

### LOW

The issue is plausible but evidence is incomplete.

Avoid LOW-confidence findings unless the potential production impact makes the issue meaningful.

---

## 18. Missing Information

Use exactly:

```text
Not Identified
```

when information is unavailable.

Use:

```text
Not Assessed
```

when the area could not reasonably be reviewed.

Use:

```text
Not Applicable
```

when the area does not apply.

Do not convert missing information into a finding.

---

## 19. Positive Observations

Record meaningful strengths supported by repository evidence.

Examples may include:

* effective secure properties
* strong error taxonomy
* appropriate retry behavior
* good idempotency controls
* effective streaming
* clean flow separation
* useful operational logging
* strong API contract alignment
* meaningful MUnit assertions

Do not provide generic praise.

---

## 20. Production Readiness

Assess production readiness using evidence.

Consider:

* security
* reliability
* error recovery
* idempotency
* observability
* performance
* scalability
* configuration
* testing
* operational support
* downstream failure behavior
* timeout behavior
* retries
* resource exhaustion
* recovery behavior

Use only the readiness statuses defined by the report schema.

---

## 21. Final Verdict

Determine the initial overall risk and recommendation from the findings.

Then reconcile them using these mandatory minimums:

| Findings Present | Minimum Risk | Minimum Recommendation     |
| ---------------- | ------------ | -------------------------- |
| Any CRITICAL     | CRITICAL     | HIGH RISK                  |
| Any HIGH         | HIGH         | CHANGES REQUIRED           |
| Any MEDIUM       | MEDIUM       | CHANGES REQUIRED           |
| LOW or NIT only  | LOW          | APPROVE WITH MINOR CHANGES |
| No findings      | LOW          | APPROVE                    |

A more severe recommendation is allowed.

A less severe recommendation is not allowed.

The structured review must preserve the original verdict if reconciliation changes it.

---

## 22. Required Review JSON

Create exactly this structured review artifact:

```text
$FRAMEWORK_ROOT/workspace/execution/review.json
```

The file must contain valid JSON.

Use the report schema:

```text
$FRAMEWORK_ROOT/references/review-report-schema.md
```

as the authoritative report structure.

The JSON must provide the information required to generate all report sections, including:

* application information
* review type
* review date
* reviewer
* overall risk
* overall recommendation
* executive summary
* review scope
* review methodology
* findings
* category assessments
* production readiness
* positive observations
* risk summary
* remediation priorities
* review limitations
* review coverage
* review controls
* verdict reconciliation where applicable

Every required category must be represented.

If a category does not apply, explicitly use:

```text
Not Applicable
```

If information is unavailable, use:

```text
Not Identified
```

If the area could not reasonably be reviewed, use:

```text
Not Assessed
```

---

## 23. Finding Evidence

Evidence must identify actual repository material.

Use:

* file paths relative to `APPLICATION_ROOT` where possible
* structural locations
* processor names
* flow names
* configuration names
* DataWeave locations
* API paths
* test names
* dependency declarations

Use exact line numbers only when confidently established.

Do not fabricate line numbers.

Do not fabricate source excerpts.

Do not include sensitive values.

---

## 24. Source Protection

The MuleSoft application under:

```text
$APPLICATION_ROOT
```

is strictly read-only.

Do not:

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
* delete repository files
* rename repository files

Do not perform remediation.

Only create the required review artifact:

```text
$FRAMEWORK_ROOT/workspace/execution/review.json
```

Do not create:

```text
CODE_REVIEW_REPORT.md
review-summary.md
findings.json
findings.md
```

Do not manually generate the Word document.

---

## 25. Final Self-Validation Before Writing review.json

Before completing the review, verify:

* repository structure was reviewed
* application metadata was reviewed
* runtime was reviewed
* Maven was reviewed
* important flows were reviewed
* global configuration was reviewed
* DataWeave was reviewed
* APIs were reviewed where available
* security was reviewed
* logging was reviewed
* integrations were reviewed
* database was reviewed where applicable
* messaging was reviewed where applicable
* performance was reviewed
* MUnit was reviewed
* dependencies were reviewed
* configuration was reviewed
* findings were validated
* duplicate findings were removed
* production readiness was assessed
* limitations were documented
* final recommendation was reconciled

Do not claim an area was reviewed if it was not reasonably assessed.

---

## 26. Final Action

Write the completed structured review to:

```text
$FRAMEWORK_ROOT/workspace/execution/review.json
```

Ensure the file is valid JSON and contains the complete review.

Do not generate the `.docx` report.

Do not run remediation.

Do not modify the application.

After successfully writing the file, respond only with:

```text
Review JSON created: $FRAMEWORK_ROOT/workspace/execution/review.json
```