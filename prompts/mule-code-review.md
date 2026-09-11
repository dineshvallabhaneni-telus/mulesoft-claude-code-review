# MuleSoft Code Review — Execution Prompt

You are executing a production-focused MuleSoft 4 application code review using the review framework provided in this repository.

You are operating in a Linux GitHub Actions environment.

The review is strictly read-only against the MuleSoft application source.

---

# 1. EXECUTION CONTEXT

The workflow provides these environment variables:

```text
APPLICATION_ROOT
REVIEW_KIT_ROOT
REVIEW_TYPE
```

Definitions:

```text
APPLICATION_ROOT = root directory of the MuleSoft application being reviewed.
APPLICATION_ROOT = ${{ github.workspace }}


REVIEW_KIT_ROOT = root directory of the MuleSoft code review framework.
REVIEW_KIT_ROOT = ${{ github.workspace }}/.mule-code-review-kit

REVIEW_TYPE = review mode, normally FULL_APPLICATION.
```

The application and review framework are separate locations.

For this execution:

```text
APPLICATION_ROOT
    = MuleSoft application

REVIEW_KIT_ROOT
    = review framework
```

Do not confuse the two locations.

Before beginning the review, verify that both directories exist.

---

# 2. MANDATORY OUTPUT

You MUST physically create exactly this file:

```text
$APPLICATION_ROOT/workspace/execution/review.json
```

This is the only structured review artifact Claude is responsible for creating.

Do not create:

```text
review-summary.md
findings.json
findings.md
CODE_REVIEW_REPORT.md
review-report.json
any other review JSON
any other report artifact
```

The final Microsoft Word report will be generated later by the framework.

Do not manually generate the Word document.

Do not create the Word document yourself.

---

# 3. FRAMEWORK FILES

The review framework is located at:

```text
$REVIEW_KIT_ROOT
```

Read the following files before reviewing the application:

```text
$REVIEW_KIT_ROOT/CLAUDE.md

$REVIEW_KIT_ROOT/agents/mule-code-review-agent.md

$REVIEW_KIT_ROOT/skills/mule-code-review/SKILL.md

$REVIEW_KIT_ROOT/references/review-report-schema.md
```

Then inspect the applicable specialized references under:

```text
$REVIEW_KIT_ROOT/skills/mule-code-review/references/
```

Use the actual framework files as the authoritative review instructions.

A reference rule is a detection criterion.

A reference rule is NOT automatic proof of a defect.

---

# 4. APPLICATION LOCATION

The MuleSoft application being reviewed is located at:

```text
$APPLICATION_ROOT
```

All application source inspection must be performed under this directory.

Inspect the actual application source.

Do not review the framework itself as if it were the MuleSoft application.

The framework provides the review methodology.

The application provides the evidence.

---

# 5. DISCOVERY AND EVIDENCE

Before performing detailed review work, inspect:

```text
$APPLICATION_ROOT/workspace/execution/application-discovery.json

$APPLICATION_ROOT/workspace/execution/review-evidence.json
```

These files provide reconnaissance and evidence signals.

They do not replace direct source inspection.

Keyword matches are signals only.

Never create a finding solely because a keyword appears in discovery or evidence output.

Always inspect the actual application source before reporting a finding.

---

# 6. REQUIRED REVIEW SEQUENCE

Perform the review in this order.

## Step 1 — Verify execution roots

Verify:

```text
$APPLICATION_ROOT

$REVIEW_KIT_ROOT
```

exist.

Verify the required framework files exist.

Verify discovery and evidence files exist where expected.

---

## Step 2 — Understand the application

Inspect the repository structure.

Identify, where present:

* application name
* Mule runtime
* Java version
* Maven configuration
* Mule Maven Plugin
* connector dependencies
* Mule XML
* DataWeave
* API specifications
* properties
* secure properties
* MUnit tests
* deployment configuration
* HTTP listeners
* HTTP requests
* database access
* messaging
* Salesforce
* batch
* schedulers
* Object Store
* logging
* external integrations

Do not assume a component exists.

---

## Step 3 — Understand architecture

Understand the application before judging individual files.

Inspect:

* main flows
* private flows
* subflows
* flow references
* orchestration
* reusable components
* synchronous dependencies
* asynchronous processing
* side effects
* transaction boundaries
* coupling
* duplicated logic
* testability

Trace important flows across files.

---

## Step 4 — Inspect global configuration

Inspect:

* global elements
* HTTP listener configuration
* HTTP request configuration
* database configuration
* messaging configuration
* connector configuration
* TLS configuration
* retry configuration
* reconnection configuration
* transaction configuration
* property configuration
* secure property configuration

Determine how global configuration affects runtime behavior.

---

## Step 5 — Inspect DataWeave

Review applicable transformations for:

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

Only report performance issues when there is a credible technical mechanism.

---

## Step 6 — Inspect APIs

Where RAML or OpenAPI specifications exist, compare implementation against the visible contract.

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
* timeout behavior
* retry behavior
* idempotency
* backward compatibility

Only report contract or compatibility problems supported by repository evidence.

---

## Step 7 — Inspect error handling

Review:

* error types
* error hierarchy
* Try scopes
* on-error-continue
* on-error-propagate
* global error handlers
* error mapping
* retries
* reconnection
* root-cause preservation
* HTTP responses
* transaction interaction

Determine actual Mule runtime behavior before reporting an error-handling finding.

---

## Step 8 — Inspect security

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

Never expose secret values.

If a secret is detected, describe the presence and location without printing the value.

Never put actual secret values into `review.json`.

---

## Step 9 — Inspect connectors and integrations

For applicable connectors review:

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

Only report missing configuration when repository evidence establishes meaningful production impact.

---

## Step 10 — Inspect database access

Where database access exists, inspect:

* SQL correctness
* SQL injection
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

Do not report speculative database risks.

---

## Step 11 — Inspect messaging

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

## Step 12 — Inspect logging and observability

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

Do not report missing logging when operational requirements are unknown.

---

## Step 13 — Inspect MUnit

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

A flow execution without meaningful assertions is not sufficient coverage.

Do not create a finding merely because additional tests could theoretically be added.

---

## Step 14 — Inspect Maven and dependencies

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

Do not recommend upgrades merely because newer versions exist.

A dependency finding requires an identifiable technical or compatibility concern.

---

## Step 15 — Inspect configuration

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

Do not assume deployment configuration exists.

---

# 7. EVIDENCE-FIRST DECISION PROCESS

For every potential issue:

1. Identify the source.
2. Inspect the surrounding implementation.
3. Inspect referenced configuration.
4. Inspect related flows.
5. Inspect DataWeave.
6. Inspect APIs where applicable.
7. Inspect properties and secure properties.
8. Inspect dependencies.
9. Inspect MUnit tests.
10. Determine whether another component mitigates the issue.
11. Determine actual Mule runtime behavior.
12. Determine realistic production impact.
13. Determine severity.
14. Determine confidence.
15. Determine precise supported location.
16. Determine actionable remediation.
17. Validate the finding.
18. Report it only if repository evidence supports it.

If the issue cannot be substantiated:

```text
DO NOT REPORT IT.
```

Do not report something merely because:

* another implementation is possible
* another setting could theoretically be added
* a newer dependency version exists
* a flow is long
* logging could be improved
* requirements are unknown
* runtime metrics are unavailable
* the implementation differs from personal preference

---

# 8. CROSS-FILE ANALYSIS

Never inspect important files in isolation.

Trace relationships between:

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

A potential issue in one file may be mitigated by another file.

Validate the complete behavior before creating a finding.

---

# 9. PERFORMANCE CLASSIFICATION

Performance observations must be classified as:

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

# 10. FINDING REQUIREMENTS

Every material finding MUST contain:

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

An optional `evidenceExcerpt` may be included when useful and safe.

Allowed severities:

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

Finding IDs must use the appropriate domain prefix defined by the applicable reference.

Examples:

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

# 11. SEVERITY

Use the severity definitions in the framework.

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
* duplicate processing
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

Use only for optional, low-impact improvements.

Severity must reflect actual evidence and production impact.

---

# 12. CONFIDENCE

## HIGH

The issue is directly demonstrated by repository evidence.

## MEDIUM

The issue is strongly supported but some context is incomplete.

## LOW

The issue is plausible but evidence is incomplete.

Avoid LOW-confidence findings unless the potential production impact makes the issue meaningful.

---

# 13. MISSING INFORMATION

Use exactly:

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

Do not convert missing information into a finding.

---

# 14. POSITIVE OBSERVATIONS

Record meaningful strengths supported by repository evidence.

Examples include:

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

# 15. PRODUCTION READINESS

Assess production readiness based on evidence.

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

Use only readiness statuses defined by the report schema:

```text
READY
PARTIAL
NOT READY
NOT APPLICABLE
NOT ASSESSED
```

---

# 16. REQUIRED REVIEW JSON STRUCTURE

The structured review must provide enough information for the report generator to produce all required report sections.

Use:

```text
$REVIEW_KIT_ROOT/references/review-report-schema.md
```

as the authoritative report schema.

The JSON must contain information for:

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

If a category does not apply, use:

```text
Not Applicable
```

If information is unavailable, use:

```text
Not Identified
```

If an area could not reasonably be reviewed, use:

```text
Not Assessed
```

---

# 17. FINDING EVIDENCE

Evidence must identify actual repository material.

Prefer:

* file paths relative to `APPLICATION_ROOT`
* flow names
* processor names
* configuration names
* DataWeave locations
* API paths
* test names
* dependency declarations
* structural locations

Use exact line numbers only when confidently established.

Do not fabricate line numbers.

Do not fabricate source excerpts.

Do not include sensitive values.

---

# 18. SOURCE PROTECTION

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
* perform remediation

The only file Claude is permitted to create as the review artifact is:

```text
$APPLICATION_ROOT/workspace/execution/review.json
```

Do not create review artifacts inside:

```text
$REVIEW_KIT_ROOT
```

Do not modify the review framework.

---

# 19. FINAL VERDICT

Determine the overall risk and recommendation from the validated findings.

Mandatory minimums:

| Findings Present | Minimum Risk | Minimum Recommendation     |
| ---------------- | ------------ | -------------------------- |
| Any CRITICAL     | CRITICAL     | HIGH RISK                  |
| Any HIGH         | HIGH         | CHANGES REQUIRED           |
| Any MEDIUM       | MEDIUM       | CHANGES REQUIRED           |
| LOW or NIT only  | LOW          | APPROVE WITH MINOR CHANGES |
| No findings      | LOW          | APPROVE                    |

A more severe recommendation is allowed.

A less severe recommendation is not allowed.

If reconciliation changes the verdict, preserve the original verdict using:

```text
originalOverallRisk
originalOverallRecommendation
```

and document the reconciliation.

---

# 20. FINAL SELF-VALIDATION

Before declaring the review complete, verify:

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

# 21. CREATE review.json

Write the completed structured review to exactly:

```text
$APPLICATION_ROOT/workspace/execution/review.json
```

Before finishing:

1. Confirm the file exists.
2. Read the file back.
3. Parse it as JSON.
4. Confirm it is a JSON object.
5. Confirm `findings` is an array.
6. Confirm every finding contains:

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
7. Confirm no secret values are present.
8. Confirm the final verdict is reconciled against the findings.

The file must contain the complete structured review.

Do not merely output the JSON in your response.

You must physically create the file.

Do not say that the review was written unless the file actually exists.

---

# 22. COMPLETION REQUIREMENT

The review is NOT complete until this file physically exists:

```text
$APPLICATION_ROOT/workspace/execution/review.json
```

The final Word report is NOT your responsibility.

Do not generate a `.docx`.

Do not perform remediation.

Do not modify the MuleSoft application.

After successfully creating and validating the file, respond only with:

```text
Review JSON created: $APPLICATION_ROOT/workspace/execution/review.json
```