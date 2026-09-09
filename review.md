# MuleSoft Full Application Code Review

## Review Type

FULL APPLICATION REVIEW

This review evaluates the current state of the complete MuleSoft
application repository.

This is a READ-ONLY review.

This is NOT:

- a Git diff review
- a pull request review
- a branch comparison
- a changed-files-only review
- a refactoring exercise
- a remediation exercise
- an implementation task

Review the complete application and its relevant supporting configuration,
tests, API specifications, dependencies, and deployment configuration.

---

# 1. Review Objective

Determine the application's current:

- architecture quality
- Mule XML correctness
- functional correctness
- security posture
- error-handling quality
- API quality
- DataWeave quality
- connector/integration quality
- database integration quality
- messaging reliability
- performance
- scalability
- test quality
- Maven/dependency health
- configuration quality
- maintainability
- observability
- operational readiness
- production readiness

The review must identify meaningful technical and business risks supported
by repository evidence.

---

# 2. Review Mode

The review MUST be performed in READ-ONLY mode.

Do not:

- modify source code
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
- checkout another branch
- reset repository state
- perform remediation

The only file that may be created is the Word review report:

`CODE_REVIEW_REPORT.docx`

Do not create `CODE_REVIEW_REPORT.md` or any other intermediate report file.

Generate the Word document by piping the review Markdown into
`scripts/md_to_docx.py` as described in `prompts/mule-full-review.md`
(PHASE 20).

Do not modify any existing application file.

---

# 3. Review Scope

Review the CURRENT STATE of the repository.

Include, where present:

- Mule application XML
- DataWeave
- RAML
- OAS/OpenAPI
- JSON schemas
- XML schemas
- properties
- secure properties
- Maven configuration
- Mule metadata
- connector configuration
- global configurations
- deployment configuration
- MUnit tests
- batch processing
- scheduling
- Object Store
- database integrations
- messaging integrations
- HTTP integrations
- Salesforce integrations
- SFTP/File integrations
- SAP integrations
- other external integrations

Review relationships between files rather than reviewing each file in
isolation.

---

# 4. Repository Reconnaissance

Before detailed review, determine the actual repository structure.

Identify:

- application name
- Mule runtime version
- Java version
- Mule Maven Plugin version
- connector versions
- Maven dependencies
- application packaging
- Mule XML files
- DataWeave files
- API specifications
- property files
- secure property configuration
- MUnit tests
- deployment configuration
- external systems
- HTTP listeners
- HTTP requests
- database integrations
- messaging integrations
- Salesforce integrations
- batch jobs
- scheduled jobs
- Object Store usage
- error-handling architecture
- logging approach
- observability approach

Do not assume any of these exist.

Use repository evidence.

---

# 5. Files to Inspect

Prioritize:

- `pom.xml`
- `mule-artifact.json`
- `src/main/mule/**`
- `src/main/resources/**`
- `src/test/**`
- RAML files
- OAS/OpenAPI files
- DataWeave files
- property files
- secure property configuration
- deployment configuration
- Maven configuration
- MUnit configuration

Exclude generated/build/IDE artifacts from normal review:

- `target/`
- `.git/`
- compiled artifacts
- IDE metadata
- temporary files
- generated artifacts

Inspect excluded artifacts only when necessary to understand application
behavior.

---

# 6. Review Execution Order

Perform the review in the following order.

## Phase 1 — Repository Discovery

Determine:

1. repository structure
2. application metadata
3. Mule runtime
4. Java version
5. Maven configuration
6. connector versions
7. API specifications
8. application flows
9. configuration
10. tests
11. deployment model

---

## Phase 2 — Application Architecture

Understand:

- entry points
- APIs
- schedulers
- message consumers
- batch jobs
- orchestration flows
- reusable flows
- subflows
- private flows
- external-system boundaries
- synchronous dependencies
- asynchronous processing
- transaction boundaries

Create a mental model of the application before reporting findings.

---

## Phase 3 — Dependency and Configuration Review

Inspect:

- `pom.xml`
- `mule-artifact.json`
- global configurations
- properties
- secure properties
- deployment configuration

Determine actual versions and compatibility.

Do not recommend upgrades simply because newer versions exist.

---

## Phase 4 — Flow and Mule XML Review

Review:

- processor ordering
- flow structure
- routing
- scopes
- variables
- payload mutation
- attributes
- flow references
- subflows
- transactions
- retry
- reconnection
- concurrency
- scheduler configuration
- batch configuration
- listener/request configuration

Use:

`references/mule-xml.md`

---

## Phase 5 — Error Handling Review

Review:

- error types
- propagation
- continuation
- error handlers
- Try scopes
- retry
- transaction behavior
- error mapping
- root-cause preservation
- downstream failures
- API error responses

Use:

`references/error-handling.md`

---

## Phase 6 — Security Review

Review:

- secrets
- credentials
- tokens
- API keys
- client secrets
- private keys
- authorization
- authentication
- TLS
- HTTP
- sensitive configuration
- injection
- excessive permissions
- sensitive logging

Use:

`references/security.md`

---

## Phase 7 — API Review

Review:

- API contract
- HTTP methods
- status codes
- request validation
- response schemas
- content types
- authentication
- authorization
- headers
- timeout
- retry
- idempotency
- compatibility
- error contract

Compare implementation against RAML/OAS when available.

Use:

`references/api.md`

---

## Phase 8 — DataWeave Review

Review:

- transformation correctness
- schema alignment
- null handling
- type conversion
- dates
- timezone
- numeric precision
- collection operations
- nested iteration
- streaming
- memory usage
- payload copying
- maintainability

Use:

`references/dataweave.md`

---

## Phase 9 — Connector Review

Review applicable connectors:

- HTTP
- Database
- Salesforce
- Anypoint MQ
- JMS
- SFTP
- File
- Object Store
- SAP
- Email
- other external-system connectors

Review:

- configuration
- authentication
- timeout
- retry
- reconnection
- pooling
- rate limits
- external-call volume
- transactions
- idempotency
- compatibility

Use:

`references/connectors.md`

---

## Phase 10 — Database Review

Review:

- SQL injection
- query correctness
- query efficiency
- N+1 queries
- result-set size
- pagination
- connection pooling
- timeout
- transactions
- rollback
- error handling

Use:

`references/database.md`

---

## Phase 11 — Messaging Review

Review:

- acknowledgement
- redelivery
- duplicate processing
- idempotency
- retry
- dead-letter handling
- poison messages
- ordering
- transactions
- message loss

Do not assume exactly-once processing without evidence.

Use:

`references/messaging.md`

---

## Phase 12 — Performance Review

Review:

- large payload memory usage
- streaming
- DataWeave efficiency
- N+1 external calls
- N+1 database calls
- excessive logging
- unbounded collections
- excessive retries
- unnecessary sequential processing
- blocking operations
- concurrency
- payload copies

Do not claim a performance defect without a reasonable technical
mechanism.

Use:

`references/performance.md`

---

## Phase 13 — Logging and Observability Review

Review:

- credentials in logs
- tokens
- authorization headers
- PII
- sensitive payloads
- excessive logging
- log levels
- diagnostic context
- correlation information
- duplicate logging
- error context
- retry visibility
- production observability

Use:

`references/logger.md`

---

## Phase 14 — MUnit Review

Review:

- happy-path coverage
- error-path coverage
- important branches
- edge cases
- assertions
- verification
- mocks
- connector failures
- downstream failures
- business outcome validation
- regression coverage

Do not consider a test adequate merely because it executes a flow.

Use:

`references/munit.md`

---

## Phase 15 — Maven Review

Review:

- Mule runtime compatibility
- Java compatibility
- Mule Maven Plugin
- connector versions
- dependency versions
- duplicate dependencies
- dependency conflicts
- plugin configuration
- dependency scopes
- packaging
- repositories
- profiles
- security concerns

Use:

`references/maven.md`

---

# 7. Review Reference Rules

Use the applicable reference files during review.

Available references may include:

- `references/mule-architecture.md`
- `references/mule-xml.md`
- `references/dataweave.md`
- `references/error-handling.md`
- `references/security.md`
- `references/api.md`
- `references/logger.md`
- `references/connectors.md`
- `references/database.md`
- `references/messaging.md`
- `references/performance.md`
- `references/munit.md`
- `references/maven.md`

Do not assume every reference applies to every repository.

Use only applicable rules.

---

# 8. Evidence Requirement

Every finding MUST be supported by repository evidence.

Evidence may include:

- exact Mule XML
- DataWeave logic
- property configuration
- API specification
- dependency configuration
- MUnit test behavior
- connector configuration
- flow relationships
- error handlers
- transaction boundaries
- logging expressions
- deployment configuration

Do not invent:

- business requirements
- downstream behavior
- infrastructure behavior
- production traffic levels
- external system capabilities
- security controls that are not visible
- performance characteristics without evidence

When external behavior cannot be verified, clearly state the limitation.

---

# 9. Finding Quality Gate

Before reporting a finding, verify:

1. Is the issue supported by repository evidence?
2. Is the affected code/configuration clearly identified?
3. Is it a real technical problem?
4. What is the realistic impact?
5. Is the issue already handled elsewhere?
6. Is the issue duplicated by another finding?
7. Is the severity justified?
8. Is the issue within review scope?
9. Can the location be identified?
10. Is remediation actionable?
11. Is confidence appropriate?

If the issue cannot be substantiated:

DO NOT REPORT IT.

---

# 10. Avoid Duplicate Findings

A single root cause must not produce multiple duplicate findings.

For example, an `on-error-continue` problem may be relevant to:

- Mule XML
- error handling
- API behavior

Do not automatically create three findings.

Select the finding that best represents the actual production risk.

Cross-reference related areas when useful.

---

# 11. Severity

Use the following severity model.

## CRITICAL

Use for:

- exposed credentials
- exposed secrets
- private keys
- severe authorization bypass
- critical TLS weakness
- likely data corruption
- likely message/data loss
- catastrophic production failure
- critical authentication exposure

---

## HIGH

Use for:

- significant security issue
- message loss
- duplicate business processing
- broken API contract
- serious error-handling problem
- serious reliability problem
- severe performance problem
- incorrect transaction behavior
- unsafe retry/idempotency
- significant runtime incompatibility

---

## MEDIUM

Use for:

- meaningful functional defect
- realistic edge-case failure
- important test gap
- moderate performance issue
- configuration problem
- maintainability problem with production impact

---

## LOW

Use for:

- minor issue
- limited operational risk
- lower-priority improvement

---

## NIT

Optional improvement only.

Do not clutter the report with NIT findings.

---

# 12. Confidence

Every finding should include confidence.

Use:

- HIGH
- MEDIUM
- LOW

## HIGH

The repository provides direct and clear evidence of the issue.

## MEDIUM

The issue is strongly supported but depends on limited assumptions or
context that cannot be fully verified.

## LOW

The issue is plausible but repository evidence is incomplete.

Avoid reporting LOW-confidence issues unless they represent meaningful
risk and the limitation is clearly explained.

---

# 13. Finding Format

Every finding MUST use this structure:

## [SEVERITY] Finding Title

**Finding ID:** SEC-001

**Category:** SECURITY

**File:** `src/main/mule/example.xml:123`

**Location:** Flow / Processor / Configuration

**Confidence:** HIGH

**Problem:**

Describe the issue clearly and concisely.

**Evidence:**

Describe the exact repository evidence supporting the finding.

**Impact:**

Explain the realistic technical and/or business impact.

**Recommendation:**

Provide a concrete remediation approach.

---

# 14. Finding IDs

Use category-specific IDs.

Examples:

- ARCH-001
- XML-001
- ERR-001
- DW-001
- API-001
- SEC-001
- LOG-001
- CON-001
- DB-001
- MSG-001
- PERF-001
- MUNIT-001
- MAVEN-001

If the reference rule already defines an ID, use that ID.

Do not invent a second ID for the same rule.

If multiple occurrences of the same rule exist, either:

- group them into one finding when they share the same root cause, or
- create separate findings only when impact/remediation is materially
  different.

---

# 15. File and Location Requirements

Every finding must identify the most specific practical location.

Preferred:

`src/main/mule/order.xml:145`

or:

`src/main/resources/dw/order-transform.dwl:42`

or:

`pom.xml:118`

or:

`src/test/munit/order-test.xml:75`

If an exact line cannot be determined, use a meaningful structural
location.

Example:

`src/main/mule/order.xml — global HTTP Request configuration`

Do not invent line numbers.

---

# 16. Architecture Assessment

Provide an overall assessment covering:

- application structure
- flow responsibilities
- coupling
- reuse
- orchestration
- separation of concerns
- transaction boundaries
- synchronous/asynchronous architecture
- external-system dependencies
- scalability
- testability

Distinguish between:

- actual defects
- architectural risks
- improvement opportunities

Do not convert architectural preferences into defects without evidence.

---

# 17. Application Inventory

Provide an inventory containing, where applicable:

| Area | Inventory |
|---|---|
| Application | Application name |
| Mule Runtime | Actual version |
| Java | Actual version |
| Mule Maven Plugin | Actual version |
| Connectors | Relevant connectors and versions |
| APIs | API specifications/endpoints |
| Flows | Major flows |
| Subflows | Major reusable components |
| DataWeave | Important transformations |
| Databases | Databases and operations |
| Messaging | Queues/topics/brokers |
| Salesforce | Salesforce integrations |
| Batch | Batch jobs |
| Schedulers | Scheduled flows |
| Object Store | Object Store usage |
| External Systems | Major dependencies |
| Tests | MUnit coverage/areas |
| Deployment | Deployment model/configuration |

Use `Not identified` when repository evidence does not provide the
information.

Do not guess.

---

# 18. Integration Inventory

Identify major integration boundaries.

For each important integration, document:

- source
- target
- protocol/connector
- operation
- synchronous/asynchronous behavior
- authentication mechanism when identifiable
- timeout/retry behavior
- transaction behavior
- idempotency considerations
- error-handling approach

Example:

| Source | Target | Mechanism | Mode | Retry | Transaction | Risk |
|---|---|---|---|---|---|---|
| API | Database | DB Connector | Sync | N/A | Local | Medium |
| MQ Consumer | Salesforce | Salesforce Connector | Async | Yes | None | High |

Only include information supported by repository evidence.

---

# 19. Security Assessment

Provide a dedicated security assessment covering:

- secret management
- authentication
- authorization
- TLS
- transport security
- injection risks
- sensitive logging
- PII handling
- permissions
- dependency security
- configuration security

Clearly distinguish:

- confirmed vulnerabilities
- security weaknesses
- areas not verifiable from the repository

Do not claim the application is secure merely because no finding was
identified.

---

# 20. Error Handling Assessment

Assess:

- error taxonomy
- propagation
- continuation
- error mapping
- retries
- root-cause preservation
- downstream failures
- API error responses
- transaction interaction
- message failure handling

Identify whether error handling is:

- strong
- adequate
- inconsistent
- weak
- high risk

Support conclusions with repository evidence.

---

# 21. API Assessment

Assess:

- API contract consistency
- implementation alignment
- validation
- HTTP methods
- status codes
- schemas
- authentication
- authorization
- error contracts
- timeout
- retry
- idempotency
- compatibility

If no API specification is present, state that contract verification was
limited.

---

# 22. DataWeave Assessment

Assess:

- transformation correctness
- schema alignment
- null handling
- type handling
- date/time handling
- numeric precision
- collection processing
- complexity
- streaming
- memory behavior
- maintainability

---

# 23. Connector Assessment

Assess applicable connectors for:

- configuration
- authentication
- timeout
- retry
- reconnection
- pooling
- transaction behavior
- idempotency
- external call volume
- compatibility

---

# 24. Database Assessment

Assess:

- SQL safety
- query efficiency
- N+1 behavior
- result-set handling
- pagination
- pooling
- timeout
- transactions
- rollback
- error handling

---

# 25. Messaging Assessment

Assess:

- acknowledgement
- redelivery
- duplicate processing
- idempotency
- retries
- dead-letter behavior
- poison messages
- ordering
- transactions
- message loss

---

# 26. Performance Assessment

Assess:

- payload size
- memory usage
- streaming
- DataWeave complexity
- external calls
- database calls
- concurrency
- blocking operations
- logging
- retries
- collections

Do not claim measured performance unless actual performance testing was
performed.

Use terms such as:

- "potential performance risk"
- "mechanism indicates"
- "could result in"

when runtime measurements are unavailable.

---

# 27. Logging and Observability Assessment

Assess:

- sensitive logging
- payload logging
- log volume
- log levels
- correlation identifiers
- diagnostic context
- error visibility
- retry visibility
- asynchronous processing visibility
- operational supportability

---

# 28. MUnit Assessment

Assess:

- happy-path coverage
- error-path coverage
- branch coverage
- assertions
- mocks
- connector failures
- downstream failures
- edge cases
- business outcome verification
- regression coverage

Do not use test-file count as evidence of adequate testing.

---

# 29. Maven and Dependency Assessment

Assess:

- Mule runtime
- Java
- Mule Maven Plugin
- connector compatibility
- dependency conflicts
- dependency versions
- plugin configuration
- dependency scopes
- packaging
- repositories
- profiles
- security concerns

Do not recommend upgrades solely because versions are old.

---

# 30. Configuration Assessment

Assess:

- property management
- secure properties
- environment separation
- hardcoded values
- endpoint configuration
- credentials
- configuration duplication
- deployment configuration
- configuration consistency

---

# 31. Production Readiness Assessment

Assess:

## Security

Is sensitive information appropriately protected?

## Reliability

Can expected downstream failures be handled safely?

## Error Recovery

Can failures be retried, propagated, recovered, or dead-lettered
appropriately?

## Idempotency

Can retries or redelivery create duplicate business effects?

## Observability

Can operators diagnose failures effectively?

## Performance

Are there obvious architectural or implementation risks?

## Scalability

Can throughput increase without disproportionate resource consumption?

## Configuration

Can environments be configured safely without source modification?

## Testing

Are critical business and failure scenarios covered?

## Operational Support

Can the application be supported effectively in production?

---

# 32. Positive Observations

Include meaningful strengths.

Examples:

- strong error taxonomy
- effective secure-property usage
- good API contract alignment
- strong MUnit assertions
- appropriate retry/idempotency strategy
- good transaction boundaries
- effective streaming
- clean flow separation
- reusable connector configurations
- good operational logging

Do not include generic praise.

---

# 33. Findings by Severity

Summarize findings using:

| Severity | Count |
|---|---:|
| CRITICAL | 0 |
| HIGH | 0 |
| MEDIUM | 0 |
| LOW | 0 |
| NIT | 0 |

Ensure the counts match the detailed findings.

---

# 34. Findings by Category

Provide:

| Category | Findings |
|---|---:|
| ARCHITECTURE | 0 |
| MULE-XML | 0 |
| ERROR-HANDLING | 0 |
| DATAWEAVE | 0 |
| API | 0 |
| SECURITY | 0 |
| LOGGING | 0 |
| CONNECTOR | 0 |
| DATABASE | 0 |
| MESSAGING | 0 |
| PERFORMANCE | 0 |
| MUNIT | 0 |
| MAVEN | 0 |
| CONFIGURATION | 0 |
| RELIABILITY | 0 |
| PRODUCTION-READINESS | 0 |

Only include categories relevant to the review, but do not omit categories
where a meaningful assessment was performed.

---

# 35. Risk Summary

Provide a concise summary of the application's major risks.

Example:

| Risk Area | Risk | Severity | Explanation |
|---|---|---|---|
| Security | Secret exposure | CRITICAL | Credential committed in configuration |
| Reliability | Unsafe retry | HIGH | Non-idempotent operation retried |
| API | Contract mismatch | HIGH | Response differs from OAS |
| Performance | Large payload materialization | MEDIUM | Large payload held in memory |

Do not duplicate complete findings.

---

# 36. Top 10 Remediation Priorities

Rank the ten most important remediation priorities.

Use:

| Priority | Finding | Severity | Recommended Action |
|---|---|---|---|
| 1 | SEC-001 | CRITICAL | Remove exposed secret |
| 2 | MSG-002 | HIGH | Introduce idempotency |
| 3 | ERR-004 | HIGH | Correct error propagation |

Priorities should consider:

1. severity
2. production impact
3. likelihood
4. data/security impact
5. remediation value
6. dependency between issues

Do not simply sort by severity.

---

# 37. Review Limitations

Clearly document limitations.

Examples:

- API specification not present
- downstream systems not available
- deployment configuration not present
- runtime behavior could not be executed
- production traffic characteristics unavailable
- external security controls not visible
- dependency vulnerability verification unavailable
- line-level evidence unavailable

Do not treat unverified areas as verified.

---

# 38. Overall Risk

Choose one:

- CRITICAL
- HIGH
- MEDIUM
- LOW

Base the overall risk on the most significant confirmed findings and the
application's overall production exposure.

Do not automatically classify the application based only on the number of
findings.

---

# 39. Overall Recommendation

Choose one:

## APPROVE

No material production risks identified.

## APPROVE WITH MINOR CHANGES

Only low-risk issues identified and no material production blocker.

## CHANGES REQUIRED

Material issues exist that should be remediated before production release.

## HIGH RISK

Critical/high-risk issues exist that materially threaten security,
reliability, data integrity, or production availability.

---

# 40. Final Report Structure

The report is written as Markdown and delivered as
`CODE_REVIEW_REPORT.docx`.

Use `#` for the report title, `##` for sections, `###` for individual
findings, pipe tables for summary tables, `**bold**` for field labels, and
fenced code blocks for evidence. Write severity keywords in upper case.
Do not use raw HTML.

The final review output MUST contain:

# MuleSoft Full Application Code Review

## Executive Summary

Provide a concise executive-level summary.

## Review Scope

Describe what was reviewed.

## Review Methodology

Describe how the repository was analyzed.

## Application Inventory

Provide application and technology inventory.

## Architecture Summary

Describe the overall architecture.

## Integration Inventory

Describe major integration boundaries.

## Critical Findings

List all CRITICAL findings.

## High Findings

List all HIGH findings.

## Medium Findings

List all MEDIUM findings.

## Low Findings

List all LOW findings.

## Security Assessment

Provide security assessment.

## Mule Architecture Assessment

Provide architecture assessment.

## Mule XML Assessment

Provide Mule XML assessment.

## Error Handling Assessment

Provide error-handling assessment.

## DataWeave Assessment

Provide DataWeave assessment.

## API Assessment

Provide API assessment.

## Connector Assessment

Provide connector assessment.

## Database Assessment

Provide database assessment.

## Messaging Assessment

Provide messaging assessment.

## Performance Assessment

Provide performance assessment.

## Logging and Observability Assessment

Provide logging assessment.

## MUnit Assessment

Provide MUnit assessment.

## Maven/Dependency Assessment

Provide Maven assessment.

## Configuration Assessment

Provide configuration assessment.

## Maintainability Assessment

Provide maintainability assessment.

## Production Readiness Assessment

Provide production-readiness assessment.

## Positive Observations

List meaningful strengths.

## Findings Summary

Provide counts by severity and category.

## Risk Summary

Summarize major risks.

## Top 10 Remediation Priorities

Provide ranked remediation priorities.

## Review Limitations

Document areas that could not be verified.

## Overall Risk

CRITICAL / HIGH / MEDIUM / LOW

## Recommendation

APPROVE

APPROVE WITH MINOR CHANGES

CHANGES REQUIRED

HIGH RISK

---

# 41. Final Review Rules

Before completing the review:

1. Confirm the entire repository was considered.
2. Confirm generated artifacts were appropriately excluded.
3. Confirm application metadata was inspected.
4. Confirm Mule runtime and Java versions were identified.
5. Confirm Maven configuration was inspected.
6. Confirm global configurations were inspected.
7. Confirm all major flows were considered.
8. Confirm related subflows/private flows were considered.
9. Confirm DataWeave was reviewed.
10. Confirm error handling was reviewed.
11. Confirm API contracts were reviewed where available.
12. Confirm security was reviewed.
13. Confirm logging was reviewed.
14. Confirm connector usage was reviewed.
15. Confirm database integrations were reviewed where applicable.
16. Confirm messaging integrations were reviewed where applicable.
17. Confirm performance risks were reviewed.
18. Confirm MUnit tests were reviewed.
19. Confirm dependency/configuration risks were reviewed.
20. Confirm findings are evidence-based.
21. Confirm duplicate findings were removed.
22. Confirm severity is justified.
23. Confirm every finding has a location.
24. Confirm every finding has evidence.
25. Confirm every finding has impact.
26. Confirm every finding has remediation.
27. Confirm finding counts match detailed findings.
28. Confirm the final recommendation is consistent with the findings.
29. Confirm no application files were modified.

---

# 42. Completion Criteria

The review is complete only when:

- the application has been inventoried
- the major architecture has been understood
- applicable reference rules have been evaluated
- findings have been validated
- duplicate findings have been removed
- findings have been categorized
- severity has been assigned
- confidence has been assigned
- positive observations have been documented
- production readiness has been assessed
- remediation priorities have been ranked
- limitations have been documented
- overall risk has been determined
- final recommendation has been provided
- `CODE_REVIEW_REPORT.docx` has been generated and verified

Do not respond with only:

- "review completed"
- "no issues found"
- "analysis complete"
- "report generated"

The actual review findings and assessment MUST be presented in the
response unless the user explicitly requests file-only output.

If no findings are identified, explicitly state:

"No material findings were identified based on the repository evidence
reviewed."

Then provide the assessment, coverage summary, limitations, and overall
recommendation.