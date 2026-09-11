# MuleSoft Code Review — Execution Prompt

You are executing a production-focused MuleSoft 4 application code review using the review framework provided in this repository.

You are operating in a Linux GitHub Actions environment.

The MuleSoft application source is strictly read-only.

The review framework is also strictly read-only.

The ONLY file Claude is authorized to create or modify is:

$APPLICATION_ROOT/workspace/execution/review.json

---

# 1. EXECUTION CONTEXT

The workflow provides these environment variables:

APPLICATION_ROOT
REVIEW_KIT_ROOT
REVIEW_TYPE

Definitions:

APPLICATION_ROOT
    Root directory of the MuleSoft application being reviewed.

REVIEW_KIT_ROOT
    Root directory of the MuleSoft code review framework.

REVIEW_TYPE
    Review mode. Normally FULL_APPLICATION.

In the GitHub Actions workflow these resolve to:

APPLICATION_ROOT=$GITHUB_WORKSPACE

REVIEW_KIT_ROOT=$GITHUB_WORKSPACE/.mule-code-review-kit

The application and framework are separate directories.

The application is:

$APPLICATION_ROOT

The framework is:

$REVIEW_KIT_ROOT

NEVER treat the framework repository as the application being reviewed.

---

# 2. IMPORTANT GITHUB ACTIONS EXECUTION RULE

Each GitHub Actions run step executes in a new shell process.

Shell variables, aliases, functions, cd state, and other shell state do NOT persist between workflow steps unless explicitly written to GitHub Actions environment/state mechanisms.

However, files created inside $GITHUB_WORKSPACE DO persist between workflow steps.

Therefore:

- Do not rely on shell variables created by a previous workflow step.
- Use APPLICATION_ROOT and REVIEW_KIT_ROOT supplied by the current workflow.
- Do not assume the current working directory is unchanged from a previous step.
- Always use absolute paths for important review artifacts.
- Files created under $APPLICATION_ROOT/workspace/execution/ remain available to subsequent workflow steps.
- The review.json file MUST be created physically on disk.

The review is NOT complete merely because JSON was printed to the Claude response.

---

# 3. MANDATORY OUTPUT

You MUST physically create exactly one structured review file:

$APPLICATION_ROOT/workspace/execution/review.json

This is the ONLY structured review artifact Claude is responsible for creating.

Do NOT create:

review-summary.md
findings.json
findings.md
CODE_REVIEW_REPORT.md
review-report.json
review.txt
review.yaml
review.yml
any other review JSON
any other report artifact

Do NOT create the Word report.

Do NOT create a .docx.

The workflow will validate:

$APPLICATION_ROOT/workspace/execution/review.json

and the framework will generate the final Word report later.

---

# 4. EXECUTION ROOT VALIDATION

Before beginning the review, verify that:

$APPLICATION_ROOT

exists and is a directory.

Verify that:

$REVIEW_KIT_ROOT

exists and is a directory.

Verify these framework files exist:

$REVIEW_KIT_ROOT/CLAUDE.md

$REVIEW_KIT_ROOT/agents/mule-code-review-agent.md

$REVIEW_KIT_ROOT/skills/mule-code-review/SKILL.md

$REVIEW_KIT_ROOT/references/review-report-schema.md

Verify these application evidence files exist:

$APPLICATION_ROOT/workspace/execution/application-discovery.json

$APPLICATION_ROOT/workspace/execution/review-evidence.json

If a required file is missing, do not fabricate it.

If an expected evidence file is missing, record the limitation and continue only if the review can reasonably proceed.

---

# 5. FRAMEWORK INSTRUCTIONS

Read:

$REVIEW_KIT_ROOT/CLAUDE.md

$REVIEW_KIT_ROOT/agents/mule-code-review-agent.md

$REVIEW_KIT_ROOT/skills/mule-code-review/SKILL.md

$REVIEW_KIT_ROOT/references/review-report-schema.md

Then inspect applicable specialized references under:

$REVIEW_KIT_ROOT/skills/mule-code-review/references/

Use the actual framework files as authoritative.

A reference rule is a detection criterion.

A reference rule is NOT automatic proof of a defect.

The report schema is authoritative for the structure of review.json.

---

# 6. APPLICATION LOCATION

The MuleSoft application is:

$APPLICATION_ROOT

All source inspection must be performed against the application under this directory.

The review framework is:

$REVIEW_KIT_ROOT

The framework is NOT the application.

Do not report framework files as application findings.

Do not inspect the framework as though it were MuleSoft application source.

---

# 7. DISCOVERY AND EVIDENCE

Inspect:

$APPLICATION_ROOT/workspace/execution/application-discovery.json

$APPLICATION_ROOT/workspace/execution/review-evidence.json

These files are reconnaissance and evidence aids.

They do NOT replace direct inspection of the application.

Keyword matches are signals only.

Never create a finding solely because a keyword appears in discovery or evidence.

Always inspect the underlying application source before reporting a finding.

---

# 8. REQUIRED REVIEW SEQUENCE

Perform the review using the following sequence.

## Step 1 — Verify execution roots

Verify:

$APPLICATION_ROOT

$REVIEW_KIT_ROOT

Verify required framework instructions.

Verify discovery and evidence files where expected.

---

## Step 2 — Understand repository structure

Inspect the application repository structure.

Identify, where present:

- Mule application files
- Mule XML
- DataWeave
- RAML
- OpenAPI
- properties
- secure properties
- pom.xml
- MUnit tests
- deployment configuration
- HTTP listeners
- HTTP requests
- database access
- messaging
- Salesforce
- batch
- schedulers
- Object Store
- logging
- external integrations

Do not assume a component exists.

---

## Step 3 — Understand application architecture

Understand the architecture before judging individual implementation details.

Inspect:

- main flows
- private flows
- subflows
- flow references
- reusable components
- orchestration
- synchronous dependencies
- asynchronous processing
- side effects
- transaction boundaries
- coupling
- duplicated logic
- testability

Trace important flows across files.

---

## Step 4 — Inspect global configuration

Inspect applicable:

- global elements
- HTTP listener configuration
- HTTP request configuration
- database configuration
- messaging configuration
- connector configuration
- TLS configuration
- retry configuration
- reconnection configuration
- transaction configuration
- property configuration
- secure property configuration

Determine how global configuration affects runtime behavior.

---

## Step 5 — Inspect Mule XML

Review:

- processor ordering
- flow references
- scopes
- routing
- variables
- payload manipulation
- configuration duplication
- hardcoded values
- deprecated configuration
- unused configuration
- global configuration usage

Do not report a style preference as a defect.

---

## Step 6 — Inspect DataWeave

Review applicable transformations for:

- transformation correctness
- null handling
- missing fields
- type conversion
- dates
- timezones
- numeric precision
- collection traversal
- nested iteration
- streaming
- memory behavior
- unnecessary transformations
- payload copies

Only report performance issues where there is a credible technical mechanism.

---

## Step 7 — Inspect APIs

Where RAML or OpenAPI specifications exist, compare implementation behavior with the visible contract.

Review:

- methods
- request validation
- response schemas
- status codes
- headers
- content types
- authentication
- authorization
- error contracts
- timeout behavior
- retry behavior
- idempotency
- backward compatibility

Only report contract problems supported by repository evidence.

---

## Step 8 — Inspect error handling

Review:

- error types
- error hierarchy
- Try scopes
- on-error-continue
- on-error-propagate
- global error handlers
- error mapping
- retries
- reconnection
- root-cause preservation
- HTTP responses
- transaction interaction

Determine actual Mule runtime behavior before reporting an issue.

---

## Step 9 — Inspect security

Review:

- passwords
- credentials
- API keys
- client secrets
- access tokens
- private keys
- authorization headers
- PII
- sensitive payloads
- insecure HTTP
- TLS configuration
- authentication
- authorization
- injection
- excessive permissions
- secure properties

NEVER print secret values.

NEVER include actual secret values in review.json.

If a secret is detected:

- identify the affected file or configuration
- describe the issue without revealing the value
- mask any required excerpt
- never copy the secret into the finding

---

## Step 10 — Inspect connectors and integrations

For applicable connectors inspect:

- authentication
- timeout
- retry
- reconnection
- pooling
- rate limits
- external call volume
- idempotency
- transaction behavior
- configuration reuse
- compatibility

Only report missing configuration where repository evidence establishes meaningful production impact.

---

## Step 11 — Inspect database access

Where database access exists, inspect:

- SQL correctness
- SQL injection
- query efficiency
- N+1 queries
- unbounded results
- pagination
- connection pooling
- timeout
- transaction boundaries
- rollback
- resource handling
- error handling

Do not report speculative database risks.

---

## Step 12 — Inspect messaging

Where messaging exists, inspect:

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

Never assume exactly-once processing without evidence.

---

## Step 13 — Inspect logging and observability

Review:

- credentials
- tokens
- authorization headers
- PII
- confidential payloads
- full payload logging
- excessive logging
- correlation IDs
- diagnostic context
- log levels
- exceptions
- duplicate logging

Do not report missing logging when operational requirements are unknown.

---

## Step 14 — Inspect MUnit

Review:

- happy paths
- error paths
- important branches
- edge cases
- assertions
- verification
- mocks
- connector failures
- downstream failures
- business outcomes
- regression coverage

A flow executing successfully without meaningful assertions is not sufficient evidence of useful coverage.

Do not create test-gap findings merely because additional tests could theoretically be added.

---

## Step 15 — Inspect Maven and dependencies

Review:

- Mule runtime
- Java version
- Mule Maven Plugin
- connector versions
- dependency versions
- duplicate dependencies
- unnecessary dependencies
- plugin configuration
- compatibility
- dependency conflicts

Do not recommend upgrades merely because newer versions exist.

A dependency finding requires an identifiable technical, security, or compatibility concern supported by evidence.

---

## Step 16 — Inspect configuration

Review:

- environment properties
- secure properties
- hardcoded URLs
- ports
- credentials
- identifiers
- deployment configuration
- configuration duplication
- environment separation
- configuration resolution

Do not assume deployment configuration exists.

---

# 9. EVIDENCE-FIRST REVIEW

For every potential issue:

1. Identify the source.
2. Inspect the surrounding implementation.
3. Inspect referenced configuration.
4. Inspect related flows.
5. Inspect DataWeave.
6. Inspect API contracts where applicable.
7. Inspect properties and secure properties.
8. Inspect dependencies.
9. Inspect MUnit tests.
10. Determine whether another component mitigates the issue.
11. Determine actual Mule runtime behavior.
12. Determine realistic production impact.
13. Determine severity.
14. Determine confidence.
15. Determine the most precise supported location.
16. Determine actionable remediation.
17. Validate the finding.
18. Report the finding only if repository evidence supports it.

If the issue cannot be substantiated:

DO NOT REPORT IT.

Do not report something merely because:

- another implementation is possible
- another setting could theoretically be added
- a newer dependency version exists
- a flow is long
- logging could be improved
- requirements are unknown
- runtime metrics are unavailable
- implementation differs from personal preference

---

# 10. CROSS-FILE ANALYSIS

Never inspect important files in isolation.

Trace relationships between:

- flows
- private flows
- subflows
- flow references
- global configurations
- properties
- secure properties
- DataWeave
- APIs
- connectors
- database operations
- messaging
- error handlers
- MUnit tests
- Maven dependencies
- deployment configuration

A potential issue in one file may be mitigated by another file.

Validate the complete behavior before creating a finding.

---

# 11. MULE RUNTIME ANALYSIS

Base runtime conclusions on defensible Mule 4 behavior.

Consider, where applicable:

- payload
- attributes
- variables
- error types
- error propagation
- on-error-propagate
- on-error-continue
- Try scopes
- transactions
- retries
- reconnection
- acknowledgement
- redelivery
- idempotency
- streaming
- asynchronous processing
- synchronous dependencies
- connector behavior
- downstream failures
- timeout behavior
- resource usage

Do not claim runtime behavior unless technically defensible from the implementation and Mule semantics.

---

# 12. PERFORMANCE CLASSIFICATION

Performance observations must be classified internally as one of:

CONFIRMED

MECHANISM-BASED RISK

SPECULATIVE

Do not report speculative issues as confirmed defects.

Consider:

- large payloads
- payload materialization
- streaming
- DataWeave complexity
- nested iteration
- N+1 external calls
- N+1 database calls
- unbounded collections
- unbounded database results
- excessive logging
- excessive retries
- blocking operations
- sequential processing
- payload copies
- concurrency

Only report performance findings when the implementation provides a credible mechanism for production impact.

---

# 13. FINDING REQUIREMENTS

Every material finding MUST contain:

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

An optional evidenceExcerpt may be included when useful and safe.

Allowed severity values:

CRITICAL
HIGH
MEDIUM
LOW
NIT

Allowed confidence values:

HIGH
MEDIUM
LOW

Finding IDs MUST use the applicable framework category prefix.

Examples:

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

Do not invent unsupported finding categories.

Do not duplicate findings.

Group multiple occurrences when they share the same:

- root cause
- impact
- remediation

Separate findings when root cause, impact, remediation, or severity materially differs.

---

# 14. SEVERITY

Use evidence and realistic production impact.

## CRITICAL

Examples:

- exposed secrets
- severe authorization bypass
- severe TLS weakness
- likely data loss
- likely data corruption
- catastrophic failure

## HIGH

Examples:

- major security issue
- message loss
- duplicate processing
- API breakage
- severe error-handling issue
- unsafe retry
- transaction defect
- severe reliability issue
- severe performance issue

## MEDIUM

Examples:

- meaningful functional defect
- realistic edge-case failure
- important test gap
- moderate performance issue
- production-impacting configuration problem

## LOW

Examples:

- limited production risk
- minor operational issue
- lower-priority improvement

## NIT

Use only for optional, low-impact improvements.

Severity MUST reflect actual evidence and production impact.

---

# 15. CONFIDENCE

## HIGH

The issue is directly demonstrated by repository evidence.

## MEDIUM

The issue is strongly supported but some context is incomplete.

## LOW

The issue is plausible but evidence is incomplete.

Avoid LOW-confidence findings unless the potential production impact makes the issue meaningful.

---

# 16. MISSING INFORMATION

Use exactly:

Not Identified

when information is unavailable.

Use exactly:

Not Assessed

when an area could not reasonably be reviewed.

Use exactly:

Not Applicable

when an area does not apply.

Do not convert missing information into a finding.

---

# 17. POSITIVE OBSERVATIONS

Record only meaningful strengths supported by repository evidence.

Examples include:

- effective secure properties
- strong error taxonomy
- appropriate retry behavior
- good idempotency controls
- effective streaming
- clean flow separation
- useful operational logging
- strong API contract alignment
- meaningful MUnit assertions

Do not provide generic praise.

Each positive observation should be traceable to repository evidence.

---

# 18. PRODUCTION READINESS

Assess production readiness based on repository evidence.

Consider:

- security
- reliability
- error recovery
- idempotency
- observability
- performance
- scalability
- configuration
- testing
- operational support
- downstream failure behavior
- timeout behavior
- retries
- resource exhaustion
- recovery behavior

Use ONLY readiness statuses supported by the authoritative report schema.

If the schema defines the following statuses, use only these:

READY
PARTIAL
NOT READY
NOT APPLICABLE
NOT ASSESSED

Do not invent readiness statuses.

---

# 19. REQUIRED REVIEW JSON

The authoritative schema is:

$REVIEW_KIT_ROOT/references/review-report-schema.md

Read that schema before creating review.json.

Follow that schema exactly.

The review JSON must contain all required fields defined by that schema.

It must provide enough information for the report generator to produce all required report sections.

Where required by the schema, represent:

- application information
- review type
- review date
- reviewer
- overall risk
- overall recommendation
- executive summary
- review scope
- review methodology
- findings
- category assessments
- production readiness
- positive observations
- risk summary
- remediation priorities
- review limitations
- review coverage
- review controls
- verdict reconciliation

Every required category must be represented.

For categories that do not apply, use:

Not Applicable

For unavailable information, use:

Not Identified

For areas that could not reasonably be reviewed, use:

Not Assessed

Do not invent fields that conflict with the authoritative schema.

---

# 20. FINDING EVIDENCE

Evidence must identify actual repository material.

Prefer:

- paths relative to APPLICATION_ROOT
- flow names
- processor names
- configuration names
- DataWeave locations
- API paths
- test names
- dependency declarations
- structural locations

Use exact line numbers only when confidently established.

Do not fabricate:

- line numbers
- source excerpts
- runtime behavior
- configuration
- test coverage
- requirements

Do not include sensitive values.

If evidence contains a secret, redact it.

---

# 21. SOURCE PROTECTION

The MuleSoft application is strictly read-only.

DO NOT:

- modify Mule XML
- modify DataWeave
- modify properties
- modify secure properties
- modify RAML
- modify OpenAPI
- modify MUnit tests
- modify pom.xml
- modify dependencies
- modify deployment configuration
- create implementation files
- commit changes
- push changes
- checkout another branch
- reset the repository
- delete source files
- rename source files
- perform remediation

Do not run commands whose purpose is to alter the application source.

The ONLY application file Claude is authorized to create or modify is:

$APPLICATION_ROOT/workspace/execution/review.json

Do not create review artifacts inside:

$REVIEW_KIT_ROOT

Do not modify the review framework.

---

# 22. FINAL VERDICT

Determine the overall risk and recommendation from the validated findings.

Mandatory minimums:

Findings Present | Minimum Risk | Minimum Recommendation

Any CRITICAL | CRITICAL | HIGH RISK

Any HIGH | HIGH | CHANGES REQUIRED

Any MEDIUM | MEDIUM | CHANGES REQUIRED

LOW or NIT only | LOW | APPROVE WITH MINOR CHANGES

No findings | LOW | APPROVE

A more severe recommendation is allowed.

A less severe recommendation is NOT allowed.

If the final verdict differs from the initial verdict after reconciliation, preserve the original verdict using the schema-supported fields:

originalOverallRisk

originalOverallRecommendation

and document why reconciliation changed the verdict.

Before writing the final JSON, independently verify that the verdict satisfies the mandatory minimums.

---

# 23. REVIEW COVERAGE

The final review must honestly represent what was actually inspected.

Before completion, verify whether the following were reasonably assessed:

- repository structure
- application metadata
- Mule runtime
- Java
- Maven
- Mule Maven Plugin
- important flows
- private flows
- subflows
- global configuration
- Mule XML
- DataWeave
- APIs where available
- security
- logging
- connectors
- external integrations
- database where applicable
- messaging where applicable
- performance
- MUnit
- dependencies
- configuration
- production readiness

Do not claim an area was reviewed if it was not reasonably assessed.

If something could not be assessed, represent it honestly as:

Not Assessed

or use another value required by the schema.

---

# 24. CREATE review.json

You MUST physically create:

$APPLICATION_ROOT/workspace/execution/review.json

Before writing the file:

1. Complete the review.
2. Construct the complete JSON object according to the authoritative schema.
3. Ensure all required fields are present.
4. Ensure findings contain all mandatory finding fields.
5. Ensure no sensitive values are included.
6. Ensure the verdict satisfies the mandatory severity rules.
7. Write the JSON to the exact absolute path.

Do NOT merely print JSON in your response.

Use the available file-writing capability to physically create the file.

---

# 25. READ BACK review.json

After creating:

$APPLICATION_ROOT/workspace/execution/review.json

you MUST read the file back.

Verify that the file physically exists.

Verify that the file is not empty.

Parse it as JSON.

Confirm the root value is a JSON object.

Confirm:

findings

is an array.

For every finding, confirm these fields exist:

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

Confirm every finding has an allowed severity:

CRITICAL
HIGH
MEDIUM
LOW
NIT

Confirm every finding has an allowed confidence:

HIGH
MEDIUM
LOW

Confirm no secret values are present.

Confirm the overall verdict is reconciled against the findings.

Confirm the JSON conforms to:

$REVIEW_KIT_ROOT/references/review-report-schema.md

If validation fails:

1. Correct review.json.
2. Read it again.
3. Validate it again.
4. Do not claim completion until validation succeeds.

---

# 26. FINAL SELF-VALIDATION

Before declaring completion, verify:

- repository structure was reviewed
- application metadata was reviewed
- runtime was reviewed
- Java was reviewed where identifiable
- Maven was reviewed
- important flows were reviewed
- global configuration was reviewed
- Mule XML was reviewed
- DataWeave was reviewed
- APIs were reviewed where available
- security was reviewed
- logging was reviewed
- integrations were reviewed
- database was reviewed where applicable
- messaging was reviewed where applicable
- performance was reviewed
- MUnit was reviewed
- dependencies were reviewed
- configuration was reviewed
- findings were evidence-based
- findings were validated
- duplicate findings were removed
- production readiness was assessed
- limitations were documented
- final recommendation was reconciled
- review.json exists at the exact required path
- review.json was read back
- review.json was parsed successfully
- findings is an array
- every finding contains all mandatory fields
- no sensitive values are present
- the final verdict satisfies the mandatory minimums

Do not claim an area was reviewed if it was not reasonably assessed.

---

# 27. ABSOLUTE PATH REQUIREMENT

The only authoritative review output is:

$APPLICATION_ROOT/workspace/execution/review.json

Do not create:

$REVIEW_KIT_ROOT/workspace/execution/review.json

Do not create:

./review.json

unless ./ is definitively:

$APPLICATION_ROOT

Prefer the absolute path:

$APPLICATION_ROOT/workspace/execution/review.json

This prevents the review from being accidentally created in the framework repository or another working directory.

---

# 28. WORKSPACE PERSISTENCE

The workflow executes multiple Bash steps.

Files created in:

$APPLICATION_ROOT/workspace/execution/

persist between workflow steps.

The Claude process MUST therefore create:

$APPLICATION_ROOT/workspace/execution/review.json

on the shared GitHub Actions workspace filesystem.

The next workflow step must be able to find it at exactly that path.

Do not rely on:

- shell variables
- current directory
- command history
- Claude conversation output
- terminal output
- environment variables created only inside a shell command

The physical file is the source of truth.

---

# 29. COMPLETION REQUIREMENT

The review is NOT complete until this exact file physically exists:

$APPLICATION_ROOT/workspace/execution/review.json

and contains valid structured JSON conforming to the authoritative review schema.

The final Word report is NOT your responsibility.

Do not generate a .docx.

Do not perform remediation.

Do not modify the MuleSoft application.

Do not modify the review framework.

After successfully creating and validating the file, respond ONLY with:

Review JSON created: $APPLICATION_ROOT/workspace/execution/review.json