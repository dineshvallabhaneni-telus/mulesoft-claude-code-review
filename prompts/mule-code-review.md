# MuleSoft Code Review — Execution Prompt

You are executing a production-focused MuleSoft 4 application code review in a Linux GitHub Actions environment.

The MuleSoft application source is strictly read-only.

The review framework is strictly read-only.

The ONLY artifact this execution is responsible for creating or modifying is:

$APPLICATION_ROOT/workspace/execution/review.json

The review is NOT complete until that file physically exists on disk, contains valid JSON, and passes the validation requirements defined in this prompt.

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

Expected GitHub Actions values:

APPLICATION_ROOT=$GITHUB_WORKSPACE

REVIEW_KIT_ROOT=$GITHUB_WORKSPACE/.mule-code-review-kit

The application and review framework are separate locations.

The application is:

$APPLICATION_ROOT

The review framework is:

$REVIEW_KIT_ROOT

NEVER treat the review framework as the MuleSoft application.

---

# 2. PRIMARY EXECUTION OBJECTIVE

Perform a complete, evidence-based, production-focused MuleSoft 4 application review.

The review must:

1. Understand the application architecture.
2. Inspect the actual application source.
3. Use the framework instructions and reference rules.
4. Validate potential findings against repository evidence.
5. Assess realistic production impact.
6. Produce the structured review JSON.
7. Physically write the JSON to the required filesystem path.
8. Read the file back from disk.
9. Parse and validate the file.
10. Correct any validation failures.
11. Only then declare completion.

The physical file is the source of truth.

A JSON object printed in the response is NOT a substitute for the file.

---

# 3. AUTHORITATIVE OUTPUT

The ONLY authoritative review output is:

$APPLICATION_ROOT/workspace/execution/review.json

You MUST physically create this file.

Do not create review artifacts in the framework repository.

Do not write the review to:

$REVIEW_KIT_ROOT/workspace/execution/review.json

Do not rely on:

./review.json

unless the current directory has been definitively verified as:

$APPLICATION_ROOT

Always prefer the absolute path:

$APPLICATION_ROOT/workspace/execution/review.json

The framework is responsible for any downstream report generation from review.json.

Claude is responsible for creating and validating review.json only.

---

# 4. FILESYSTEM REQUIREMENT

The review is NOT complete merely because:

- JSON was generated in memory
- JSON was printed to stdout
- JSON appeared in the Claude response
- JSON was displayed in a code block
- a tool returned JSON content

The review is complete only when this file physically exists:

$APPLICATION_ROOT/workspace/execution/review.json

The parent directory may be created if necessary:

$APPLICATION_ROOT/workspace/execution/

Creating the execution directory is permitted solely to enable creation of review.json.

Do not modify application source files.

Do not modify framework files.

---

# 5. GITHUB ACTIONS WORKSPACE PERSISTENCE

GitHub Actions workflow steps may execute in separate shell processes.

Shell variables, aliases, functions, current-directory state, and other shell state may not persist between steps.

Files created under:

$GITHUB_WORKSPACE

persist between workflow steps.

Therefore:

- Use the environment variables supplied to the current execution.
- Do not depend on shell state from a previous workflow step.
- Do not depend on the current working directory.
- Use absolute paths for the review artifact.
- Physically write review.json to the shared GitHub Actions workspace.
- Verify the file after writing it.

The next workflow step must be able to locate:

$APPLICATION_ROOT/workspace/execution/review.json

---

# 6. INITIAL PATH VALIDATION

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

Verify these application evidence files where expected:

$APPLICATION_ROOT/workspace/execution/application-discovery.json

$APPLICATION_ROOT/workspace/execution/review-evidence.json

If a required framework file is missing, do not fabricate it.

If discovery or evidence is missing, do not fabricate it.

If an expected evidence file is missing, record the limitation and continue only if the review can reasonably proceed.

---

# 7. FRAMEWORK INSTRUCTIONS

Before reviewing the application, read:

$REVIEW_KIT_ROOT/CLAUDE.md

$REVIEW_KIT_ROOT/agents/mule-code-review-agent.md

$REVIEW_KIT_ROOT/skills/mule-code-review/SKILL.md

$REVIEW_KIT_ROOT/references/review-report-schema.md

Then inspect the applicable specialized references under:

$REVIEW_KIT_ROOT/skills/mule-code-review/references/

The actual framework files are authoritative.

The review-report schema is authoritative for the structure of review.json.

A framework reference rule is a detection criterion.

A reference rule is NOT automatic proof of a defect.

Do not invent framework rules, finding categories, finding IDs, readiness statuses, or schema requirements.

---

# 8. APPLICATION LOCATION

The MuleSoft application being reviewed is:

$APPLICATION_ROOT

All application source inspection must be performed against this directory.

The review framework is:

$REVIEW_KIT_ROOT

The framework is not application source.

Never report framework files as application findings.

Never inspect the framework as though it were MuleSoft application implementation.

---

# 9. DISCOVERY AND EVIDENCE

Inspect:

$APPLICATION_ROOT/workspace/execution/application-discovery.json

$APPLICATION_ROOT/workspace/execution/review-evidence.json

These files are reconnaissance and evidence aids.

They do NOT replace direct application source inspection.

Keyword matches are signals only.

Never create a finding solely because a keyword appears in discovery or evidence.

For every material finding, inspect the underlying application source and relevant related configuration.

---

# 10. REQUIRED REVIEW SEQUENCE

Perform the review in the following sequence.

## Step 1 — Verify execution roots

Verify:

$APPLICATION_ROOT

$REVIEW_KIT_ROOT

Verify required framework instructions.

Verify discovery and evidence files where available.

---

## Step 2 — Understand repository structure

Inspect the actual application repository.

Identify, where present:

- Mule XML
- flows
- private flows
- subflows
- flow references
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

Understand the application architecture before judging individual implementation details.

Inspect:

- flow boundaries
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

Use the framework architecture rules where applicable.

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

Determine how global configuration affects actual runtime behavior.

---

## Step 5 — Inspect Mule XML

Review applicable:

- processor ordering
- flow references
- scopes
- routing
- variables
- payload manipulation
- global configuration usage
- configuration duplication
- hardcoded values
- deprecated configuration
- unused configuration

Do not report style preferences as defects.

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

Only report performance problems where a credible technical mechanism exists.

---

## Step 7 — Inspect APIs

Where RAML or OpenAPI specifications exist, compare implementation behavior against the visible contract.

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

Only report contract or compatibility problems supported by repository evidence.

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

Base conclusions on defensible Mule 4 runtime behavior.

Do not speculate about runtime behavior.

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

NEVER expose secret values.

NEVER place actual secret values in review.json.

If a secret is detected:

- identify the affected file or configuration
- describe the issue without revealing the value
- mask any necessary excerpt
- do not copy the secret into the review

---

## Step 10 — Inspect connectors and integrations

Where applicable, inspect:

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

A dependency finding requires an identifiable technical, security, or compatibility concern supported by repository evidence.

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

# 11. CROSS-FILE ANALYSIS

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

A potential issue in one file may be mitigated or caused by another file.

Validate complete behavior before reporting a finding.

---

# 12. MULE RUNTIME ANALYSIS

Base runtime conclusions on defensible Mule 4 behavior.

Consider where applicable:

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

# 13. EVIDENCE-FIRST DECISION PROCESS

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
18. Report it only if repository evidence supports it.

If the issue cannot be substantiated:

DO NOT REPORT IT.

Do not report an issue merely because:

- another implementation is possible
- another setting could theoretically be added
- a newer dependency exists
- a flow is long
- logging could be improved
- requirements are unknown
- runtime metrics are unavailable
- implementation differs from personal preference

---

# 14. PERFORMANCE CLASSIFICATION

Classify performance observations internally as:

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

# 15. FINDING REQUIREMENTS

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

Optional:

evidenceExcerpt

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

Group occurrences when they share the same:

- root cause
- impact
- remediation

Separate findings when root cause, impact, remediation, or severity materially differs.

---

# 16. SEVERITY

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

# 17. CONFIDENCE

## HIGH

The issue is directly demonstrated by repository evidence.

## MEDIUM

The issue is strongly supported but some context is incomplete.

## LOW

The issue is plausible but evidence is incomplete.

Avoid LOW-confidence findings unless the potential production impact makes the issue meaningful.

---

# 18. MISSING INFORMATION

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

# 19. POSITIVE OBSERVATIONS

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

Each positive observation must be traceable to repository evidence.

Do not provide generic praise.

---

# 20. PRODUCTION READINESS

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

Use ONLY readiness statuses defined by:

$REVIEW_KIT_ROOT/references/review-report-schema.md

Do not invent readiness statuses.

If the authoritative schema defines values such as:

READY
PARTIAL
NOT READY
NOT APPLICABLE
NOT ASSESSED

use only those values.

---

# 21. REVIEW JSON SCHEMA

The authoritative schema is:

$REVIEW_KIT_ROOT/references/review-report-schema.md

Read the schema before constructing review.json.

Follow the schema exactly.

The review JSON must contain every required field defined by the schema.

It must provide sufficient information for the downstream report generator to produce all required report sections.

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

Use:

Not Applicable

when a category does not apply.

Use:

Not Identified

when information is unavailable.

Use:

Not Assessed

when an area could not reasonably be reviewed.

Do not invent fields that conflict with the authoritative schema.

---

# 22. FINDING EVIDENCE

Evidence must identify actual repository material.

Prefer:

- paths relative to $APPLICATION_ROOT
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

---

# 23. SOURCE PROTECTION

The MuleSoft application is strictly read-only.

Do NOT:

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

Do not run commands whose purpose is to alter application source.

The ONLY file you may create or modify is:

$APPLICATION_ROOT/workspace/execution/review.json

Do not modify the review framework.

---

# 24. FINAL VERDICT

Determine the overall risk and recommendation from the validated findings.

Mandatory minimums:

| Findings Present | Minimum Risk | Minimum Recommendation |
|------------------|--------------|------------------------|
| Any CRITICAL    | CRITICAL     | HIGH RISK              |
| Any HIGH        | HIGH         | CHANGES REQUIRED       |
| Any MEDIUM      | MEDIUM       | CHANGES REQUIRED       |
| LOW or NIT only | LOW          | APPROVE WITH MINOR CHANGES |
| No findings     | LOW          | APPROVE                |

A more severe recommendation is allowed.

A less severe recommendation is NOT allowed.

If reconciliation changes the initial verdict, preserve the original verdict using the schema-supported fields, such as:

originalOverallRisk

originalOverallRecommendation

and document why reconciliation changed the verdict.

Before writing review.json, independently verify that the final verdict satisfies the mandatory minimums.

---

# 25. REVIEW COVERAGE

Before completion, honestly determine whether the following were reasonably assessed:

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

Do not claim an area was assessed if it was not.

If an area could not reasonably be assessed, represent it as:

Not Assessed

or use the corresponding value required by the authoritative schema.

---

# 26. CONSTRUCT THE REVIEW

After completing the application review:

1. Construct the complete review JSON object according to:
   
   $REVIEW_KIT_ROOT/references/review-report-schema.md

2. Ensure every required schema field is present.

3. Ensure `findings` is an array.

4. Ensure every finding contains:

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

5. Ensure every finding uses an allowed severity.

6. Ensure every finding uses an allowed confidence.

7. Ensure no sensitive values are present.

8. Ensure the final verdict satisfies the mandatory minimums.

9. Ensure review coverage and limitations honestly reflect what was assessed.

---

# 27. PHYSICALLY CREATE review.json

THIS IS A MANDATORY EXECUTION STEP.

Create the directory if necessary:

$APPLICATION_ROOT/workspace/execution/

Then physically write the complete JSON object to:

$APPLICATION_ROOT/workspace/execution/review.json

Use the available filesystem or file-writing capability.

If a shell is the available writing mechanism, write to the absolute path above.

Do NOT merely output the JSON in the response.

Do NOT stop after constructing the JSON in memory.

Do NOT assume that displaying JSON creates the file.

The file must physically exist on disk.

Immediately after writing, verify:

test -f "$APPLICATION_ROOT/workspace/execution/review.json"

Then verify that it is non-empty.

If the file does not exist, the task is incomplete.

Continue until the file has been physically created.

---

# 28. READ review.json BACK FROM DISK

After creating the file:

1. Read the exact file back from disk.

2. Parse the file as JSON.

3. Confirm the root value is a JSON object.

4. Confirm:

   findings

   is an array.

5. For every finding, confirm these fields exist:

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

6. Confirm every severity is one of:

   CRITICAL
   HIGH
   MEDIUM
   LOW
   NIT

7. Confirm every confidence is one of:

   HIGH
   MEDIUM
   LOW

8. Confirm no sensitive values are present.

9. Confirm the overall verdict satisfies the mandatory minimums.

10. Confirm the JSON conforms to:

$REVIEW_KIT_ROOT/references/review-report-schema.md

If validation fails:

1. Correct review.json.
2. Write the corrected JSON to the same absolute path.
3. Read the file back again.
4. Parse it again.
5. Validate again.
6. Repeat until validation succeeds.

Do not claim completion while validation is failing.

---

# 29. FINAL FILE EXISTENCE CHECK

Before responding, verify ALL of the following:

$APPLICATION_ROOT exists.

$REVIEW_KIT_ROOT exists.

$APPLICATION_ROOT/workspace/execution/review.json exists.

The file is non-empty.

The file parses as valid JSON.

The root value is an object.

`findings` is an array.

Every finding contains all mandatory fields.

Every severity is valid.

Every confidence is valid.

No sensitive values are present.

The verdict satisfies the mandatory minimums.

The JSON conforms to the authoritative report schema.

Only after ALL checks succeed may you declare completion.

---

# 30. FINAL RESPONSE

After successfully creating and validating the physical file, respond ONLY with:

Review JSON created: $APPLICATION_ROOT/workspace/execution/review.json

Do not include the JSON in the final response.

Do not include a summary.

Do not include findings.

Do not claim completion unless the physical file exists and has passed validation.