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
# Project Location:
Mulesoft Repository = ${{ github.workspace }}
Unable to get access the location ${{ github.workspace }} exit and throw error
---
# GOVERNING INSTRUCTIONS

Before reviewing the application, read and follow: All Claude related .md files are located at ${{ github.workspace }}/.mule-code-review folder

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

If a report file is explicitly requested, the only file that may be created
is the requested review report.

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

# PHASE 19 — FINAL REPORT CREATION

This is the final and mandatory phase.

DO NOT RESPOND TO THE USER YET.

You MUST first create the complete final review report.

The report MUST be created at:

$GITHUB_WORKSPACE/CODE_REVIEW_REPORT.md

The file must contain the COMPLETE review output based on all findings,
evidence, analysis, and conclusions from Phases 1–18.

The report MUST NOT be:

- a summary of the review
- a placeholder
- an outline
- a statement that the report will be created
- a partial report
- a report containing only findings

It must contain the complete final report defined in the
"FINAL REPORT" section above.

---

## MANDATORY EXECUTION ORDER

Perform these steps in EXACTLY this order:

### STEP 1 — Compile the final report

Use all validated information from Phases 1–18.

Do not invent information.

Do not omit validated findings.

Do not include speculative findings.

Construct the complete final report.

### STEP 2 — Create the file

Use the Write tool to create:

$GITHUB_WORKSPACE/CODE_REVIEW_REPORT.md

Write the COMPLETE report into this file.

Do NOT merely output the report in your response.

The report MUST physically exist as:

$GITHUB_WORKSPACE/CODE_REVIEW_REPORT.md

### STEP 3 — Verify the file

After writing the file, use the Read tool to read:

$GITHUB_WORKSPACE/CODE_REVIEW_REPORT.md

Verify that the file contains the complete report.

Confirm that the report contains all required sections:

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

### STEP 4 — Validate completeness

Do not respond yet.

Verify:

- $GITHUB_WORKSPACE/CODE_REVIEW_REPORT.md exists
- the file is not empty
- the file contains the actual review
- the file contains the validated findings
- the file contains the evidence
- the file contains recommendations
- all required report sections are present

If anything is missing:

1. Fix the report.
2. Write the corrected report.
3. Read the corrected report again.
4. Validate it again.

Repeat until the report is complete.

### STEP 5 — ONLY NOW RESPOND

You may respond to the user ONLY after:

- $GITHUB_WORKSPACE/CODE_REVIEW_REPORT.md has been created
- the complete report has been written
- the report has been read back
- the report has been verified as complete

Your final response must NOT contain the full report.

Your final response must be concise and confirm:

- the review is complete
- the report was successfully created
- the exact file path
- finding counts by severity
- overall risk
- overall recommendation

Example:

Review completed successfully.

Report created and verified:

$GITHUB_WORKSPACE/CODE_REVIEW_REPORT.md

Findings:
- Critical: X
- High: X
- Medium: X
- Low: X

Overall Risk: HIGH

Overall Recommendation: ...

IMPORTANT:

NEVER respond with messages such as:

- "Writing the final report."
- "I am writing the report."
- "All phases complete."
- "The report will be created."
- "See the report."
- "Review completed."

unless $GITHUB_WORKSPACE/CODE_REVIEW_REPORT.md has already been created, populated
with the COMPLETE report, read back, and verified.

The final response is the LAST action.

FILE CREATION AND VERIFICATION MUST HAPPEN BEFORE THE FINAL RESPONSE.


# FINAL RESPONSE

After successfully creating and verifying the file, the final response MUST:

1. State that the review is complete.
2. State that the report was created.
3. Provide the exact absolute path to the report.
4. Provide a concise summary of the major findings.
5. Include the actual review output summary.

Example:

Review completed.

Report created:

/absolute/path/to/CODE_REVIEW_REPORT.md

The report contains the complete validated MuleSoft application review.

Summary:
- Critical: X
- High: X
- Medium: X
- Low: X
- Overall Risk: <rating>

Top risks:
- ...
- ...
- ...

Do NOT respond only with "Review completed" or "See report".

---

# IMPORTANT FINAL RESPONSE REQUIREMENT

The final response must contain the ACTUAL REVIEW OUTPUT.

Do NOT respond only with:

- "Review completed"
- "I found several issues"
- "See report"
- "The report has been generated"

`CODE_REVIEW_REPORT.md` Should be created and share the full path where the file was created.
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