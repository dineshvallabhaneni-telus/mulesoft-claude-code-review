# MUnit Review Rules

## Purpose

Review MuleSoft MUnit tests for meaningful confidence in application
behavior, including:

* happy paths
* error paths
* important branches
* edge cases
* assertions
* verifications
* mocks
* connector failures
* downstream failures
* business outcomes
* regression coverage
* configuration-dependent behavior

The objective is not maximum test count or line coverage.

The objective is meaningful behavioral and production-risk coverage.

---

# MUnit Review Principles

Before reporting a testing finding:

1. Identify important application flows.
2. Identify their meaningful success paths.
3. Identify important failure paths.
4. Identify significant branches.
5. Identify external dependencies.
6. Identify database/messaging interactions.
7. Identify important business outcomes.
8. Inspect corresponding MUnit tests.
9. Inspect mocks and spies.
10. Inspect assertions.
11. Inspect verification behavior.
12. Determine whether failures would be detected.
13. Consider regression risk.
14. Avoid treating execution alone as meaningful coverage.

A test that executes a flow without validating its behavior is not
sufficient evidence of meaningful coverage.

---

# MUNIT-001 — Important Path Lacks Meaningful Coverage

## Description

An important application path lacks MUnit coverage sufficient to detect
meaningful regression or production defects.

Important paths may include:

* primary business flows
* important conditional branches
* database updates
* message consumers/producers
* external API integrations
* authentication/authorization behavior
* transformation logic
* retry behavior
* error handling
* transaction-sensitive processing

## Finding Gate

Establish:

1. the path is important based on visible application behavior,
2. no meaningful test covers it, or existing tests do not exercise the
   relevant behavior, and
3. the gap creates credible regression risk.

Do not report missing tests for every flow or processor.

Prioritize paths with meaningful production consequences.

## Evidence Requirements

Identify:

* affected flow/component
* important behavior
* available tests
* specific coverage gap
* production/regression impact

---

# MUNIT-002 — Test Lacks Meaningful Assertion

## Description

A test executes application code but does not meaningfully verify the
expected result.

Weak examples include tests that only establish:

* flow completed
* no exception occurred
* processor executed
* a generic payload exists

Meaningful assertions should validate relevant behavior.

Potential assertions include:

* payload content
* payload structure
* attributes
* variables
* response status
* error type
* error message where appropriate
* database outcome
* message publication
* external interaction
* business state

## Finding Gate

Establish that:

* the test executes the relevant behavior,
* the test has no meaningful assertion of the expected outcome, and
* a regression could pass unnoticed.

Do not report a test simply because it has few assertions.

One strong assertion can be sufficient when it validates the important
business outcome.

## Evidence Requirements

Identify:

* test method/name
* execution under test
* existing assertion(s)
* expected behavior that is not validated
* resulting confidence gap

---

# MUNIT-003 — Error Path Not Tested

## Description

An important error path is implemented but is not meaningfully tested.

Potential areas include:

* connector failure
* validation failure
* transformation failure
* database failure
* timeout
* authentication failure
* downstream HTTP error
* message-processing failure
* retry exhaustion
* transaction rollback
* global error handling

## Finding Gate

Establish:

1. the error path exists in application code,
2. the error can materially affect production behavior,
3. no meaningful test exercises it.

Do not require a separate test for every possible Mule error type.

Prioritize error paths with meaningful business or operational impact.

## Evidence Requirements

Identify:

* error-handling implementation
* triggering condition
* available tests
* missing validation
* production consequence

---

# MUNIT-004 — Downstream Failure Not Tested

## Description

A flow depends on a database, messaging system, HTTP service, SaaS
connector, or other external system, but the relevant downstream failure
behavior is not meaningfully tested.

Potential scenarios include:

* HTTP 4xx/5xx
* timeout
* connection failure
* authentication failure
* database failure
* message publication failure
* broker unavailability
* malformed downstream response
* downstream rate limiting

## Finding Gate

Establish:

* the downstream dependency is visible,
* its failure can materially affect the flow,
* failure handling exists or is expected,
* and no meaningful test verifies the behavior.

Do not report every external dependency as requiring a dedicated failure
test.

Prioritize dependencies whose failure can cause:

* data loss
* duplicate processing
* incorrect responses
* partial processing
* transaction problems
* message loss
* incorrect business state

## Evidence Requirements

Identify:

* downstream operation
* failure mechanism
* application error/recovery behavior
* available tests
* missing scenario
* production impact

---

# MUNIT-005 — Test Does Not Validate Business Outcome

## Description

A test verifies technical execution but does not establish that the
application produced the required business result.

Examples include:

* flow completed but no output is validated
* API returned but response content is not checked
* database operation executed but persisted state is not verified
* message was sent but message content or publication behavior is not
  verified
* transformation ran but transformed structure/content is not asserted

## Finding Gate

Establish that:

1. a meaningful business outcome is visible in the repository,
2. the test exercises the relevant behavior, and
3. the test does not validate that outcome.

Do not invent business requirements.

The expected outcome must be established from repository evidence such as:

* implementation logic
* API contract
* transformation
* database operation
* message contract
* existing tests
* documented configuration

## Evidence Requirements

Identify:

* business behavior
* test
* technical assertion currently present
* missing business assertion
* regression risk

---

# Happy Path Coverage

Inspect whether important successful scenarios are covered.

Consider:

* valid request
* expected payload
* expected response
* successful external call
* successful database operation
* successful message publication
* normal business routing

Happy-path tests should validate meaningful outcomes rather than merely
successful execution.

---

# Error Path Coverage

Prioritize failures that can materially change behavior.

Examples:

```text id="z5kq2m"
External failure
      |
      v
Error Handler
      |
      v
Expected error response
```

Tests should verify the behavior that matters, such as:

* error type
* response status
* response payload
* rollback
* retry behavior
* message redelivery
* downstream interaction
* business state

Do not require assertions on implementation details that are irrelevant
to externally observable behavior.

---

# Branch Coverage

Inspect important branches such as:

* Choice routing
* validation conditions
* error branches
* conditional enrichment
* feature/configuration branches
* success/failure routing

Do not equate branch count with quality.

A small number of high-value tests can provide better confidence than
large numbers of superficial tests.

---

# Mocks

Inspect whether mocks:

* represent the actual dependency behavior,
* return realistic payloads,
* simulate relevant failures,
* preserve important attributes,
* exercise the intended processor,
* are scoped appropriately.

A test that mocks away the behavior it claims to validate may create
false confidence.

Do not report the use of mocks itself as a defect.

---

# Connector Failure Testing

For important connectors, consider tests for:

* timeout
* connection failure
* authentication failure
* authorization failure
* server failure
* malformed response
* rate limiting
* unavailable dependency

Only require scenarios that are relevant to the connector and visible
application behavior.

---

# Database Testing

Where database behavior is important, inspect whether tests meaningfully
cover:

* successful query/update
* expected result handling
* no-result behavior
* database failure
* transaction rollback
* important constraint failures
* incorrect/invalid data where relevant

Do not require live database integration tests if the repository uses an
intentional unit-testing strategy, provided important behavior is still
meaningfully verified.

---

# Messaging Testing

Where messaging is applicable, consider:

* successful consumption
* successful publication
* processing failure
* acknowledgement behavior
* redelivery
* duplicate handling
* idempotency
* poison-message behavior
* dead-letter routing where implemented

Do not claim that a test proves broker-level semantics unless the test
actually exercises those semantics.

---

# API Testing

Where APIs are present, inspect tests for:

* valid requests
* invalid requests
* authentication/authorization behavior where testable
* response status
* response payload
* headers where relevant
* error contract
* important validation rules
* backward-compatible behavior where relevant

Tests should validate observable API behavior.

---

# DataWeave Testing

For important transformations, inspect:

* normal input
* missing fields
* null values
* empty collections
* type variations
* date/time behavior
* boundary values
* representative nested structures

Prioritize cases where incorrect transformation can cause data loss or
corruption.

---

# Regression Coverage

Identify high-risk behavior that is vulnerable to regression.

Examples:

* previously complex routing
* important transformations
* error mappings
* API contracts
* database writes
* message processing
* security controls
* idempotency behavior

Do not infer historical defects unless repository evidence establishes
them.

---

# Assertions and Verifications

Distinguish:

**Assertion**

Validates a resulting state or expected value.

**Verification**

Validates that an interaction occurred.

Both can be useful, but verification alone does not prove that the
business outcome is correct.

For example:

```text id="3s6kq1"
verify HTTP request occurred
```

does not necessarily prove:

```text id="w8m2px"
correct response was produced
correct data was transformed
correct business state was created
```

Evaluate the test against the behavior it is intended to protect.

---

# Coverage Quality

Do not rely solely on:

* line coverage
* processor execution
* flow invocation count
* number of test cases
* number of assertions

Meaningful coverage requires behavioral validation.

---

# False-Positive Controls

Do not create an MUnit finding when:

* the important behavior is meaningfully tested elsewhere,
* a shared test/helper provides the required coverage,
* a higher-level integration test validates the relevant outcome,
* the test has one or more strong assertions that adequately validate
  the behavior,
* a mock intentionally isolates the unit under test and still verifies
  the relevant outcome,
* the behavior is not important enough to create meaningful regression
  risk,
* the expected business behavior is not established,
* evidence is insufficient.

When evidence is insufficient:

**Do not report the finding.**

Record the limitation where relevant.

---

# Severity Guidance

Severity must reflect the production impact of the untested behavior.

## CRITICAL

Rarely appropriate.

Use only when the testing gap leaves a highly critical behavior
effectively unprotected and repository evidence establishes severe
regression consequences.

## HIGH

Use for:

* critical security behavior without meaningful coverage
* important transaction/rollback behavior without meaningful coverage
* message-processing behavior where regression could cause message loss
* critical business processing with severe corruption/loss consequences

## MEDIUM

Use for:

* important error paths not tested
* significant downstream failure scenarios not tested
* meaningful business outcomes not asserted
* important branches without regression coverage

## LOW

Use for:

* limited but useful coverage gaps
* lower-impact edge cases
* localized assertion weaknesses

## NIT

Use only for optional testing improvements without material production
impact.

---

# Confidence Guidance

## HIGH

The missing or ineffective test coverage is directly demonstrated.

## MEDIUM

The coverage gap is strongly supported, but the importance of the
scenario has some contextual uncertainty.

## LOW

Use only when the gap is meaningful but important repository context is
missing.

Avoid LOW-confidence findings when the expected behavior cannot be
established.

---

# Positive Testing Indicators

Where supported by evidence, recognize strengths such as:

* meaningful business-outcome assertions
* strong error-path coverage
* realistic connector failure mocks
* rollback verification
* message redelivery/idempotency testing
* API contract validation
* edge-case DataWeave tests
* meaningful branch coverage
* regression tests for critical behavior
* appropriate use of mocks and verifications
* tests that validate externally observable behavior

Positive observations must be evidence-backed.

---

# Required Finding Fields

Any MUnit finding must include:

* Finding ID
* Severity
* Category
* Title
* File
* Location
* Confidence
* Problem
* Evidence
* Evidence Excerpt
* Impact
* Recommendation

Evidence excerpts must remain faithful to repository content.

Never include:

* passwords
* API keys
* access tokens
* private keys
* authorization headers
* secure property values
* sensitive production data

Sensitive information must be sanitized before inclusion in the review
artifact.