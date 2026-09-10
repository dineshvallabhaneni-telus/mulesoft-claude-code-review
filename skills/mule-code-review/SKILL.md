````markdown
---
name: mule-code-review
description: Performs senior-level, production-focused Mule 4 code reviews covering application architecture, Mule XML, DataWeave, error handling, security, APIs, connectors, databases, messaging, performance, logging, MUnit, Maven, configuration, reliability, and production readiness.
---

# MuleSoft Code Review Skill

## Purpose

Perform a senior-level, production-focused review of a MuleSoft 4
application using repository evidence.

The review is:

- evidence-based
- read-only
- production-focused
- technically defensible
- cross-file aware
- aware of Mule runtime semantics
- aware of integration failure modes
- conservative when evidence is incomplete

The objective is not to maximize the number of findings.

The objective is to identify meaningful, defensible production risks
and provide actionable remediation guidance.

---

# 1. Execution Model

The framework runs with the **MuleSoft application root as the current
working directory**.

The application root is therefore:

```text
Path.cwd()
````

The framework may use:

```text
workspace/execution/
```

for temporary execution evidence and structured review artifacts.

The final report is generated under:

```text
reports/CODE_REVIEW_REPORT_<YYYYMMDD-HHMMSS>.docx
```

The application source remains read-only.

Do not assume the framework has a separate parent directory available
during review.

---

# 2. Mandatory Review Workflow

Complete the following sequence:

1. Read `CLAUDE.md`.
2. Read `agents/mule-code-review-agent.md`.
3. Read this `SKILL.md`.
4. Read `references/review-report-schema.md`.
5. Read applicable specialized reference files.
6. Execute:

   * `scripts/discover_application.py`
   * `scripts/collect_review_evidence.py`
7. Inspect the complete repository.
8. Understand the application architecture.
9. Inspect application metadata and Maven configuration.
10. Inspect Mule XML and global configurations.
11. Inspect DataWeave.
12. Inspect APIs and specifications where present.
13. Inspect security configuration.
14. Inspect error handling.
15. Inspect connectors and external integrations.
16. Inspect database behavior where applicable.
17. Inspect messaging behavior where applicable.
18. Inspect logging and observability.
19. Inspect performance characteristics.
20. Inspect MUnit tests.
21. Validate potential findings against surrounding implementation.
22. Remove unsupported and duplicate findings.
23. Construct the structured review JSON.
24. Execute `scripts/validate_review.py`.
25. Generate the Word report using `scripts/generate_report.py`.
26. Validate the generated report.
27. Confirm exactly one final Word report exists.

Do not skip repository-wide understanding in favor of file-by-file
inspection.

---

# 3. Review Scope

A full application review includes, where applicable:

* repository structure
* application metadata
* Mule runtime
* Java version
* Maven configuration
* Mule Maven Plugin
* connector dependencies
* Mule XML
* flows
* subflows
* private flows
* flow references
* global configuration
* DataWeave
* API specifications
* API implementation
* properties
* secure properties
* deployment configuration
* HTTP listeners
* HTTP requests
* database access
* messaging
* Salesforce
* schedulers
* batch
* Object Store
* external services
* error handling
* retries
* reconnection
* transactions
* idempotency
* logging
* observability
* MUnit
* configuration separation
* production readiness

Only report areas supported by repository evidence.

---

# 4. Review Modes

## 4.1 Full Application Review

Inspect the entire repository and understand the complete application
before assessing individual implementation details.

Do not perform a Git-diff-only review.

## 4.2 Change Review

When explicitly requested as a Git, PR, or change review:

* inspect the relevant diff
* identify changed files
* inspect surrounding implementation
* inspect affected global configuration
* inspect affected APIs
* inspect dependencies
* inspect tests
* inspect related flows
* identify regressions

Changed lines must never be judged in isolation.

---

# 5. Repository Reconnaissance

Identify actual repository evidence for:

| Area              | Evidence                                          |
| ----------------- | ------------------------------------------------- |
| Application name  | Actual repository/application metadata            |
| Runtime           | `pom.xml` and applicable configuration            |
| Java              | `pom.xml` and build configuration                 |
| Mule Maven Plugin | `pom.xml`                                         |
| Connectors        | Maven dependencies and Mule XML                   |
| Mule XML          | Application source                                |
| DataWeave         | `.dwl` and inline transformations                 |
| APIs              | RAML/OAS and implementation                       |
| Properties        | `.properties` and configuration                   |
| Secure properties | Secure-properties configuration                   |
| MUnit             | Test source and dependencies                      |
| Deployment        | Repository deployment configuration               |
| HTTP              | Listener/request configuration                    |
| Database          | DB connector and SQL                              |
| Messaging         | Messaging connectors and acknowledgement behavior |
| Scheduler         | Scheduler configuration                           |
| Batch             | Batch configuration                               |
| Object Store      | Object Store configuration                        |
| Logging           | Logger configuration                              |
| Error handling    | Error handlers and error mappings                 |

Do not infer that a technology exists merely because it is common in
Mule applications.

---

# 6. Evidence-First Review Method

For every potential issue:

1. Identify the source.
2. Inspect the surrounding implementation.
3. Inspect referenced configuration.
4. Inspect related flows.
5. Inspect DataWeave.
6. Inspect API contracts.
7. Inspect tests.
8. Inspect dependencies.
9. Determine whether another component mitigates the issue.
10. Determine actual Mule behavior.
11. Determine production impact.
12. Assign severity.
13. Assign confidence.
14. Assign a precise location.
15. Provide actionable remediation.

If the issue cannot be substantiated:

**DO NOT REPORT IT.**

A detection rule or regex signal is not proof of a defect.

---

# 7. Evidence Standards

Every material finding must identify actual repository evidence.

Evidence may include:

* file path
* structural location
* processor
* flow
* subflow
* global configuration
* DataWeave expression
* API specification
* Maven dependency
* property reference
* test
* SQL statement
* connector configuration
* deployment configuration

Do not fabricate:

* source code
* code excerpts
* line numbers
* runtime behavior
* configuration
* requirements
* deployment behavior
* business requirements

If an exact line cannot be established, use the most specific
structural location available.

Use:

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

---

# 8. Finding Requirements

Every finding must contain:

* `id`
* `severity`
* `category`
* `title`
* `location`
* `confidence`
* `problem`
* `evidence`
* `impact`
* `recommendation`

Where available, also include:

* `file`
* `evidenceExcerpt`

Every finding must answer:

### Evidence

What repository evidence proves the issue?

### Behavior

What will Mule actually do?

### Impact

What production impact can occur?

### Existing Controls

Is the issue already mitigated elsewhere?

### Severity

Does the evidence justify the assigned severity?

### Location

Can the issue be tied to a precise repository location?

### Recommendation

Can a concrete remediation be provided?

If any answer is insufficient, investigate further before creating the
finding.

---

# 9. Finding Quality

Findings must be:

* specific
* evidence-backed
* technically defensible
* production-relevant
* actionable
* non-duplicative

Do not create findings merely because:

* another implementation is possible
* a newer dependency version exists
* a preferred coding style is not used
* a configuration setting is absent without demonstrated impact
* a theoretical optimization exists
* a common Mule pattern is not present
* runtime behavior is merely conceivable

Do not report personal style preferences as defects.

---

# 10. Finding Deduplication

Group occurrences when they share the same:

* root cause
* production impact
* remediation

Separate findings when their:

* root cause
* impact
* remediation
* severity

materially differ.

Do not create multiple findings for the same underlying defect merely
because it occurs in multiple files.

---

# 11. Severity

Allowed severity values:

```text
CRITICAL
HIGH
MEDIUM
LOW
NIT
```

## CRITICAL

Use only when repository evidence supports severe production impact,
such as:

* exposed secrets with meaningful security impact
* severe authorization bypass
* severe TLS weakness
* likely data loss
* likely data corruption
* catastrophic failure

## HIGH

Examples:

* major security issue
* message loss
* duplicate processing with meaningful business impact
* API breakage
* severe error-handling defect
* unsafe retry causing material impact
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

Use only for optional, low-impact improvements.

Severity must reflect actual evidence and production impact.

---

# 12. Confidence

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

Avoid LOW-confidence findings unless they represent a meaningful risk.

Do not use LOW confidence as a mechanism for reporting speculative
issues that should not be reported at all.

---

# 13. Mule Runtime Awareness

The review must consider actual Mule 4 behavior involving:

* payload
* attributes
* variables
* error types
* error propagation
* `on-error-propagate`
* `on-error-continue`
* Try scopes
* flow references
* transactions
* streaming
* retries
* reconnection
* asynchronous processing
* connector behavior
* acknowledgement
* redelivery
* Object Store
* batch processing
* scheduler execution
* connector connection pools

Do not claim Mule runtime behavior without a defensible technical basis.

---

# 14. Architecture Review

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
* duplicated business logic
* testability

Architecture findings:

```text
ARCH-001  Excessive flow complexity
ARCH-002  Duplicated business logic
ARCH-003  Tight coupling creating meaningful production risk
ARCH-004  Incorrect abstraction creating behavioral risk
ARCH-005  Synchronous dependency creating meaningful reliability risk
```

A long flow is not automatically a complexity finding.

The finding must demonstrate meaningful maintainability, reliability,
testability, or operational impact.

---

# 15. Mule XML Review

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
* contradictory configuration

Finding IDs:

```text
XML-001  Incorrect processor ordering
XML-002  Unsafe or inconsistent global configuration
XML-003  Hardcoded environment-specific configuration
XML-004  Unused or contradictory configuration
XML-005  Flow configuration creating runtime risk
```

Evidence must establish actual behavior.

---

# 16. DataWeave Review

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

Finding IDs:

```text
DW-001  Incorrect transformation behavior
DW-002  Unsafe null or missing-field handling
DW-003  Incorrect type conversion
DW-004  Potential memory problem
DW-005  Inefficient transformation with production impact
DW-006  Date/time or timezone defect
```

Performance findings require a credible mechanism.

Do not report performance problems merely because a transformation looks
complex.

---

# 17. Error Handling Review

Review:

* error types
* error hierarchy
* error propagation
* `on-error-propagate`
* `on-error-continue`
* Try scopes
* global handlers
* error mapping
* retries
* reconnection
* root-cause preservation
* HTTP responses
* transaction interaction

Finding IDs:

```text
ERR-001  Error swallowed
ERR-002  Incorrect error propagation
ERR-003  Overly broad error handling
ERR-004  Unsafe retry
ERR-005  Root cause lost
ERR-006  Sensitive error information exposed
```

Severity must be based on actual production impact.

---

# 18. Security Review

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

Finding IDs:

```text
SEC-001  Secret exposed in source
SEC-002  Secret exposed in logs
SEC-003  Sensitive data exposed
SEC-004  Authentication weakness
SEC-005  Authorization weakness
SEC-006  TLS/security configuration weakness
SEC-007  Injection risk
```

Never print:

* passwords
* API keys
* client secrets
* access tokens
* private keys
* authorization headers
* secure property values

When evidence requires demonstrating presence, mask the sensitive value.

---

# 19. API Review

Where API contracts exist, review:

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

Finding IDs:

```text
API-001  Implementation does not align with contract
API-002  Incorrect status code behavior
API-003  Missing validation
API-004  Authentication/authorization concern
API-005  Breaking API behavior
API-006  Incorrect error contract
```

Only report compatibility issues when the affected contract is visible
in repository evidence.

---

# 20. Logging and Observability Review

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

Finding IDs:

```text
LOG-001  Sensitive information logged
LOG-002  Full payload logged without sufficient justification
LOG-003  Meaningful operational context missing
LOG-004  Excessive logging creates production risk
```

Do not report missing logging merely because an operational practice
would be preferable.

There must be a meaningful operational consequence supported by
evidence.

---

# 21. Connector Review

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

Finding IDs:

```text
CON-001  Unsafe connector configuration
CON-002  Missing timeout
CON-003  Unsafe retry/reconnection
CON-004  Connection/resource risk
CON-005  Rate-limit or external-call risk
```

Only report missing settings when repository evidence supports
production impact.

---

# 22. Database Review

Where database access exists, review:

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

Finding IDs:

```text
DB-001  SQL injection
DB-002  Inefficient query
DB-003  N+1 database access
DB-004  Unbounded result retrieval
DB-005  Unsafe transaction behavior
DB-006  Connection/resource risk
```

Do not infer database performance problems without a credible mechanism.

---

# 23. Messaging Review

Where messaging is present, review:

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

Finding IDs:

```text
MSG-001  Message acknowledgement risk
MSG-002  Duplicate processing risk
MSG-003  Missing idempotency where required by visible behavior
MSG-004  Unsafe retry
MSG-005  Message loss risk
```

Never assume exactly-once processing without repository evidence.

---

# 24. Performance Review

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

Classify performance evidence as:

```text
CONFIRMED
MECHANISM-BASED RISK
SPECULATIVE
```

`SPECULATIVE` performance issues must not be reported as confirmed
defects.

Do not create performance findings without a credible production
mechanism.

Finding IDs:

```text
PERF-001  Large payload memory risk
PERF-002  N+1 external calls
PERF-003  N+1 database calls
PERF-004  Unbounded processing
PERF-005  Excessive logging
PERF-006  Inefficient processing
```

---

# 25. MUnit Review

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

Finding IDs:

```text
MUNIT-001  Important path lacks meaningful coverage
MUNIT-002  Test lacks meaningful assertion
MUNIT-003  Error path not tested
MUNIT-004  Downstream failure not tested
MUNIT-005  Test does not validate business outcome
```

A flow executing successfully without meaningful assertions does not
constitute meaningful coverage.

Test findings should focus on important production behavior, not
arbitrary coverage percentages unless such requirements are visible.

---

# 26. Maven and Dependency Review

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

Finding IDs:

```text
MAVEN-001  Runtime/plugin compatibility concern
MAVEN-002  Dependency conflict
MAVEN-003  Duplicate dependency
MAVEN-004  Unsafe dependency configuration
```

Do not recommend upgrades merely because newer versions exist.

An upgrade recommendation requires an identified compatibility,
security, reliability, or support concern.

---

# 27. Configuration Review

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

Finding IDs:

```text
CFG-001  Environment-specific value hardcoded
CFG-002  Credential configuration concern
CFG-003  Configuration duplication creates risk
CFG-004  Environment separation concern
```

Do not assume deployment configuration exists.

---

# 28. Production Readiness

Assess:

* downstream failures
* timeouts
* retries
* duplicate processing
* redelivery
* transactions
* idempotency
* resource exhaustion
* large payloads
* rate limits
* operational recovery
* observability
* configuration separation
* testing

Readiness status must be one of:

```text
READY
PARTIAL
NOT READY
NOT APPLICABLE
NOT ASSESSED
```

The readiness assessment must be supported by the review evidence and
must reconcile with material findings.

---

# 29. Positive Observations

Identify meaningful strengths when supported by actual repository
evidence.

Examples include:

* strong error taxonomy
* effective secure properties
* good API contract alignment
* appropriate retry behavior
* good idempotency controls
* effective streaming
* clean flow separation
* useful operational logging
* strong MUnit assertions
* clear configuration separation

Do not provide generic praise.

Every positive observation should identify supporting evidence.

---

# 30. Missing Information and Limitations

Do not turn missing information into a finding.

Use:

```text
Not Identified
```

when information is unavailable.

Use:

```text
Not Assessed
```

when an area could not reasonably be reviewed.

Use:

```text
Not Applicable
```

when the area does not apply.

Record material review limitations in the report.

Examples:

* deployment configuration not present
* external runtime settings unavailable
* external API contract unavailable
* production traffic volumes unavailable
* runtime metrics unavailable
* external infrastructure unavailable

---

# 31. Final Verdict Reconciliation

The final verdict must be reconciled against findings.

Minimum rules:

| Findings        | Minimum Risk | Minimum Recommendation     |
| --------------- | ------------ | -------------------------- |
| Any CRITICAL    | CRITICAL     | HIGH RISK                  |
| Any HIGH        | HIGH         | CHANGES REQUIRED           |
| Any MEDIUM      | MEDIUM       | CHANGES REQUIRED           |
| LOW or NIT only | LOW          | APPROVE WITH MINOR CHANGES |
| No findings     | LOW          | APPROVE                    |

Allowed recommendations:

```text
HIGH RISK
CHANGES REQUIRED
APPROVE WITH MINOR CHANGES
APPROVE
```

A more severe recommendation is allowed.

A less severe recommendation is not allowed.

The original stated verdict must be preserved when reconciliation
changes it.

The report must explain the reconciliation.

---

# 32. Structured Review Contract

The review agent must produce:

```text
workspace/execution/review.json
```

The JSON must contain, at minimum:

```json
{
  "application": {},
  "reviewType": "FULL_APPLICATION",
  "reviewDate": "YYYY-MM-DD",
  "reviewer": "Claude MuleSoft Code Review Agent",
  "findings": [],
  "overallRisk": "LOW",
  "overallRecommendation": "APPROVE"
}
```

Finding objects must satisfy the required finding fields defined by
`references/review-report-schema.md`.

Do not create arbitrary report structures.

---

# 33. Validation

Before report generation:

1. Validate JSON syntax.
2. Validate finding structure.
3. Validate finding IDs are unique.
4. Validate severity values.
5. Validate confidence values.
6. Validate finding counts.
7. Validate verdict reconciliation.
8. Validate category counts.
9. Validate finding inventory reconciliation.
10. Confirm limitations are documented.
11. Confirm review coverage is documented.

Use:

```text
scripts/validate_review.py
```

The validator is authoritative for structural validation and minimum
verdict reconciliation.

---

# 34. Report Generation

The final report must be generated exclusively through:

```text
scripts/generate_report.py
```

Do not manually construct the Word document.

The generator owns:

* formatting
* headings
* tables
* colors
* finding cards
* severity indicators
* risk summaries
* readiness matrices
* headers
* footers
* final filename

The final artifact must be:

```text
reports/CODE_REVIEW_REPORT_<YYYYMMDD-HHMMSS>.docx
```

Do not create:

```text
CODE_REVIEW_REPORT.md
review-summary.md
findings.json
findings.md
```

or arbitrary report files.

---

# 35. Source Protection

The review is strictly read-only.

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
* delete files
* rename files

Generated execution artifacts must remain outside application source
areas and must not be treated as application evidence.

---

# 36. Security of Review Artifacts

Never expose sensitive values in:

* findings
* evidence
* evidence excerpts
* logs
* generated JSON
* Word report
* final chat response

Sensitive information includes:

* passwords
* API keys
* client secrets
* access tokens
* private keys
* authorization headers
* secure property values
* confidential credentials

Describe the presence and location of sensitive information without
printing the value.

---

# 37. Review Completion Criteria

The review is complete only when all applicable areas have been
considered:

* repository structure reviewed
* application metadata reviewed
* runtime reviewed
* Java reviewed
* Maven reviewed
* dependencies reviewed
* flows reviewed
* global configuration reviewed
* Mule XML reviewed
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
* production readiness assessed
* findings validated
* duplicate findings removed
* limitations documented
* coverage documented
* final verdict reconciled
* Word report generated
* Word report validated
* exactly one final Word report confirmed

---

# 38. Final Chat Response

When running in GitHub Actions, the final response must contain only:

```text
Overall Status: <PASS | FAIL | BLOCKED>
Recommendation: <APPROVE | APPROVE WITH MINOR CHANGES | CHANGES REQUIRED | HIGH RISK>
Report: reports/<generated-file-name>.docx
```

No additional commentary should be returned in the GitHub Actions final
response.

```

This version should be the authoritative skill file going forward. It also keeps the distinction clear between **discovery/evidence signals** and **actual review findings**, which is important for preventing regex-based false positives.
```