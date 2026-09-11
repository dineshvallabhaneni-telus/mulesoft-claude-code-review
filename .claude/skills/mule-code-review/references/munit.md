# MUnit Review Rules

## Purpose

These rules define how MUnit tests must be reviewed in Mule 4
applications.

The objective is to determine whether the test suite provides meaningful
confidence in:

- functional correctness
- error handling
- business behavior
- connector behavior
- important branches
- API behavior
- DataWeave transformations
- regression protection
- integration behavior

Do not consider test-file existence or execution alone as evidence of
adequate testing.

A test must meaningfully verify expected behavior.

---

## MUnit Review Principles

Before reporting a test-related finding:

1. Identify the flow or component being tested.
2. Understand the business behavior.
3. Inspect the implementation being tested.
4. Inspect related error handlers.
5. Inspect connector interactions.
6. Inspect DataWeave transformations.
7. Inspect assertions.
8. Inspect mocks.
9. Inspect verification behavior.
10. Identify important branches.
11. Identify realistic failure scenarios.
12. Determine whether the test provides meaningful regression protection.

Do not require tests for trivial implementation details when they do not
provide meaningful business or technical value.

---

## MUNIT-001 — Missing Test for New Behavior

### Rule

Flag newly introduced or materially changed behavior that has no
appropriate automated test coverage.

Consider:

- new flows
- new branches
- new transformations
- new error handling
- new connector behavior
- new API behavior
- changed business rules

### Severity

MEDIUM

Escalate when the untested behavior is business-critical or carries
significant production risk.

---

## MUNIT-002 — Missing Happy-Path Test

### Rule

Flag important flows or business operations without a meaningful
successful execution test.

The test should verify the expected successful outcome.

### Severity

MEDIUM

---

## MUNIT-003 — Missing Error-Path Test

### Rule

Flag important error handling that is not tested.

Consider:

- connector failures
- validation failures
- downstream failures
- DataWeave failures
- database failures
- messaging failures
- error handlers
- retry exhaustion
- HTTP error responses

### Severity

MEDIUM

Escalate when incorrect error behavior could cause data loss, message loss,
incorrect API responses, or security exposure.

---

## MUNIT-004 — Missing Important Branch Coverage

### Rule

Flag important business or technical branches that are not meaningfully
tested.

Examples include:

- conditional routing
- Choice branches
- validation branches
- error branches
- retry exhaustion
- alternate processing paths
- empty-data paths

### Severity

MEDIUM

Do not require every trivial branch to have a separate test.

---

## MUNIT-005 — Weak Assertion

### Rule

Flag assertions that do not adequately verify the expected behavior.

Examples include:

- asserting only that execution completed
- checking only that payload is non-null
- checking only message count
- asserting an unrelated value
- assertions that cannot detect the relevant regression

### Severity

MEDIUM

---

## MUNIT-006 — Test Only Executes Code

### Rule

Flag tests that execute a flow or processor but do not meaningfully
verify its result or behavior.

Examples include:

- no meaningful assertions
- no verification of important connector calls
- no validation of output
- no validation of error behavior

### Severity

MEDIUM

---

## MUNIT-007 — Missing Connector Mock

### Rule

Flag tests that directly invoke external systems when mocking would be
appropriate for isolated testing.

Consider:

- HTTP Request
- Database
- Salesforce
- Anypoint MQ
- JMS
- SFTP
- File
- Object Store
- external APIs

### Severity

LOW / MEDIUM

Do not require mocks when the test is intentionally an integration or
end-to-end test and that behavior is clearly documented or established
by project conventions.

---

## MUNIT-008 — Missing Negative Test

### Rule

Flag important business operations where realistic invalid or failure
inputs are not tested.

Examples include:

- invalid request
- missing required field
- null value
- empty collection
- invalid identifier
- downstream failure
- authentication failure
- authorization failure

### Severity

MEDIUM

---

## MUNIT-009 — Brittle Test

### Rule

Flag tests that depend unnecessarily on implementation details and are
likely to fail when valid internal refactoring occurs.

Examples include:

- excessive processor-level assertions
- unnecessary ordering assumptions
- hardcoded implementation details
- fragile payload comparisons
- assertions against internal variables that are not part of the
  behavior being tested

### Severity

LOW / MEDIUM

Do not classify a test as brittle merely because it uses detailed
assertions.

---

## MUNIT-010 — Test Does Not Validate Business Outcome

### Rule

Flag tests that execute technical processing but do not verify the
business outcome that the flow is responsible for producing.

Examples include:

- verifying flow completion without validating output
- verifying a database call without validating resulting behavior
- verifying an HTTP request without validating the API response
- verifying message consumption without validating business processing

### Severity

HIGH

Use HIGH only when the missing business assertion materially reduces
confidence in critical functionality.

---

## MUNIT-011 — Incorrect Mock Behavior

### Rule

Flag mocks that do not accurately represent the behavior required by the
test scenario.

Examples include:

- mocking success when testing a failure scenario
- returning unrealistic payloads
- returning incorrect error types
- omitting required attributes
- mocking a downstream response that cannot occur

### Severity

MEDIUM

---

## MUNIT-012 — Mock Hides the Defect

### Rule

Flag mocks that bypass the behavior the test is intended to validate.

Examples include:

- mocking the component under test
- mocking away critical business logic
- mocking the error handler being tested
- mocking a transformation whose output should be validated

### Severity

HIGH

Only report when the mock materially prevents the test from detecting
real defects.

---

## MUNIT-013 — Missing Verification of Connector Interaction

### Rule

Flag important connector interactions where the test should verify:

- whether the connector was called
- number of calls
- important parameters
- important payload
- important attributes
- important error behavior

### Severity

MEDIUM

Do not require verification for every connector invocation.

---

## MUNIT-014 — Incorrect Connector Verification

### Rule

Flag verification that checks the wrong:

- operation
- number of calls
- parameters
- payload
- attributes
- execution path

### Severity

MEDIUM

---

## MUNIT-015 — Missing Error-Type Assertion

### Rule

Flag important error scenarios where the test verifies only that an
error occurred but does not verify the expected Mule error type or
business error classification when that distinction is important.

### Severity

MEDIUM

---

## MUNIT-016 — Incorrect Error Assertion

### Rule

Flag tests that expect an incorrect error type, status code, error code,
or error response.

### Severity

HIGH

---

## MUNIT-017 — Missing HTTP Response Assertion

### Rule

For API flows, flag tests that do not meaningfully validate important
HTTP response behavior.

Consider:

- status code
- response body
- headers
- content type
- error contract

### Severity

MEDIUM

---

## MUNIT-018 — Missing API Error Test

### Rule

Flag important API operations where expected error responses are not
tested.

Examples include:

- validation errors
- authentication failures
- authorization failures
- not-found responses
- downstream failures
- internal errors

### Severity

MEDIUM / HIGH

---

## MUNIT-019 — Missing DataWeave Transformation Test

### Rule

Flag important DataWeave transformations without meaningful tests for
their required output behavior.

Consider:

- required fields
- optional fields
- null values
- empty collections
- type conversion
- date/time
- numeric values
- nested structures

### Severity

MEDIUM

---

## MUNIT-020 — Missing Null or Empty-Input Test

### Rule

Flag realistic null, missing-field, empty-object, or empty-collection
scenarios that can materially affect processing and are not tested.

### Severity

LOW / MEDIUM

Escalate when the scenario can cause production failure.

---

## MUNIT-021 — Missing Boundary-Condition Test

### Rule

Flag important boundary conditions that can realistically affect
correctness.

Examples include:

- zero records
- one record
- maximum expected records
- maximum field length
- boundary dates
- numeric boundaries
- empty payload
- missing optional fields

### Severity

LOW / MEDIUM

Do not require artificial boundary tests without evidence that the
boundary matters.

---

## MUNIT-022 — Missing Retry Test

### Rule

Flag important retry behavior that is not tested.

Consider:

- first-attempt failure
- successful retry
- retry exhaustion
- duplicate side effects
- downstream recovery

### Severity

MEDIUM / HIGH

Coordinate with:

- `references/error-handling.md`
- `references/messaging.md`

---

## MUNIT-023 — Missing Idempotency Test

### Rule

Flag retryable or message-driven business operations where duplicate
processing is a realistic risk but idempotency behavior is not tested.

### Severity

HIGH

Only report when the application has a meaningful duplicate-processing
risk.

---

## MUNIT-024 — Missing Transaction Behavior Test

### Rule

Flag important transactional processing where commit or rollback
behavior is not meaningfully tested.

Consider:

- database transactions
- messaging transactions
- multi-step processing
- downstream failure
- rollback scenarios

### Severity

HIGH

Only report when transaction behavior is important to correctness.

---

## MUNIT-025 — Missing Batch Test

### Rule

For Batch processing, flag important scenarios that are not tested.

Consider:

- successful batch execution
- record-level failure
- batch-level failure
- empty input
- large input
- batch step behavior
- aggregation behavior

### Severity

MEDIUM

---

## MUNIT-026 — Missing Messaging Failure Test

### Rule

For messaging flows, flag missing tests for important:

- acknowledgement behavior
- redelivery
- duplicate processing
- retry
- dead-letter behavior
- poison messages
- processing failures

### Severity

MEDIUM / HIGH

Coordinate with `references/messaging.md`.

---

## MUNIT-027 — Missing Database Failure Test

### Rule

For database integrations, flag important database failure scenarios
that are not tested.

Examples include:

- connection failure
- timeout
- SQL error
- transaction rollback
- no-result scenario
- duplicate-key failure

### Severity

MEDIUM

---

## MUNIT-028 — Missing External-System Failure Test

### Rule

Flag critical external dependencies where realistic downstream failure
scenarios are not tested.

Examples include:

- HTTP timeout
- HTTP 5xx
- Salesforce failure
- SFTP failure
- database failure
- MQ failure

### Severity

MEDIUM

---

## MUNIT-029 — Test Depends on External Environment

### Rule

Flag unit tests that depend unnecessarily on:

- live databases
- live APIs
- Salesforce environments
- live queues
- external files
- environment-specific credentials

### Severity

MEDIUM

Do not report intentionally designed integration or end-to-end tests as
defects when their purpose is clearly established.

---

## MUNIT-030 — Hardcoded Environment Dependency

### Rule

Flag tests that require environment-specific:

- URLs
- credentials
- identifiers
- file paths
- database details
- external resources

when those dependencies make the test unreliable or non-portable.

### Severity

LOW / MEDIUM

---

## MUNIT-031 — Test Data Does Not Represent Real Behavior

### Rule

Flag test data that is so unrealistic that the test cannot provide
meaningful confidence in production behavior.

Examples include:

- always-populated optional fields
- unrealistic identifiers
- impossible connector responses
- missing important combinations
- unrealistic payload structure

### Severity

MEDIUM

Do not require production data in tests.

Use representative synthetic data where appropriate.

---

## MUNIT-032 — Test Does Not Verify Error Response

### Rule

Flag error-path tests that verify only that an exception occurred but do
not validate the resulting:

- HTTP status
- error payload
- error code
- message
- propagated error type

when those outputs are part of the contract.

### Severity

MEDIUM

---

## MUNIT-033 — Test Does Not Verify Side Effect

### Rule

Flag tests where the primary behavior is an external side effect but
the test does not verify that the side effect occurred correctly.

Examples include:

- database update
- Salesforce update
- message publication
- file creation
- Object Store update
- HTTP downstream invocation

### Severity

MEDIUM

---

## MUNIT-034 — Test Verifies Wrong Side Effect

### Rule

Flag tests that verify an external interaction that is not the actual
business side effect of the flow.

### Severity

HIGH

---

## MUNIT-035 — Missing Regression Test for Defect

### Rule

When repository evidence identifies a defect correction or important
behavioral change, flag the absence of a regression test when the defect
could reasonably recur.

### Severity

MEDIUM

---

## MUNIT-036 — Duplicate or Redundant Tests

### Rule

Flag large numbers of tests that exercise effectively identical behavior
without providing additional meaningful coverage.

### Severity

LOW

Do not report similar tests when they intentionally cover materially
different business scenarios.

---

## MUNIT-037 — Test Contains Excessive Implementation Detail

### Rule

Flag tests that are tightly coupled to internal implementation details
and provide little additional business or regression value.

### Severity

LOW

---

## MUNIT-038 — Test Naming Does Not Describe Behavior

### Rule

Flag test names that make it difficult to understand:

- scenario
- expected behavior
- failure condition

### Severity

LOW

Do not report naming differences when the intent remains clear.

---

## MUNIT-039 — Missing Test for Security Behavior

### Rule

Flag security-sensitive flows without meaningful tests for important:

- authentication behavior
- authorization behavior
- access denial
- sensitive-data handling

### Severity

HIGH

Coordinate with `references/security.md`.

---

## MUNIT-040 — Sensitive Test Data Exposed

### Rule

Flag real:

- passwords
- access tokens
- API keys
- client secrets
- private keys
- sensitive personal information

committed to MUnit test data.

### Severity

CRITICAL / HIGH

Use the security rules for final severity classification.

---

## MUNIT-041 — Incorrect Test Configuration

### Rule

Flag MUnit configuration that prevents tests from reliably executing or
causes important tests to be skipped.

### Severity

HIGH

---

## MUNIT-042 — Disabled Important Test

### Rule

Flag important tests that are disabled, ignored, skipped, or otherwise
prevented from providing regression protection.

### Severity

MEDIUM / HIGH

Escalate when the disabled test covers critical functionality.

---

## MUNIT-043 — Test Failure Not Asserted

### Rule

Flag tests that execute an expected failure scenario but do not verify
that the failure actually occurred.

### Severity

MEDIUM

---

## MUNIT-044 — Incorrect Test Setup

### Rule

Flag setup logic that creates conditions different from the scenario the
test claims to validate.

### Severity

MEDIUM

---

## MUNIT-045 — Test Cleanup Failure

### Rule

Flag tests that leave behind:

- files
- database records
- Object Store entries
- messages
- external resources

when that state can affect subsequent tests.

### Severity

LOW / MEDIUM

---

## MUNIT-046 — Test Order Dependency

### Rule

Flag tests that depend on another test executing before them.

Tests should be independently executable unless project architecture
explicitly requires otherwise.

### Severity

MEDIUM

---

## MUNIT-047 — Non-Deterministic Test

### Rule

Flag tests whose results can change unpredictably due to:

- current time
- random values
- asynchronous timing
- external state
- race conditions
- uncontrolled concurrency

### Severity

MEDIUM

---

## MUNIT-048 — Excessive Test Wait

### Rule

Flag tests that use unnecessarily long waits or timeouts that materially
increase test execution time.

### Severity

LOW / MEDIUM

Do not report waits that are required to test asynchronous behavior.

---

## MUNIT-049 — Missing Asynchronous Verification

### Rule

Flag asynchronous flows where the test does not reliably verify that the
expected processing eventually occurred.

### Severity

MEDIUM

---

## MUNIT-050 — Incorrect Asynchronous Verification

### Rule

Flag asynchronous tests that can pass before the actual processing has
completed.

### Severity

HIGH

---

## MUNIT-051 — Missing Concurrency Test

### Rule

Flag concurrency-sensitive behavior where race conditions or duplicate
processing are realistic but no meaningful concurrency-related test
exists.

### Severity

MEDIUM / HIGH

Only report when concurrency is relevant to the implementation.

---

## MUNIT-052 — Incomplete Test Coverage of Error Handler

### Rule

Flag error handlers with multiple materially different behaviors where
the tests cover only one path.

Examples include:

- different error types
- different status codes
- retry vs non-retry
- propagated vs continued errors

### Severity

MEDIUM

---

## MUNIT-053 — Test Does Not Validate Configuration Behavior

### Rule

Flag tests where configuration behavior materially affects business
processing but is never validated.

Examples include:

- secure property resolution
- environment-specific behavior
- timeout configuration
- routing configuration

### Severity

LOW / MEDIUM

Only report when configuration behavior is important to correctness.

---

## MUNIT-054 — Missing Test for Contract Compatibility

### Rule

For API integrations, flag important changes or behavior where tests do
not verify compatibility with the relevant request or response contract.

### Severity

MEDIUM / HIGH

Coordinate with `references/api.md`.

---

## MUNIT-055 — Missing Test for Large Payload Behavior

### Rule

Flag important flows where large payload behavior is a known production
concern and tests provide no meaningful coverage for:

- memory behavior
- streaming
- large collections
- large files
- large database results

### Severity

LOW / MEDIUM

Do not report simply because test payloads are small.

---

## MUNIT-056 — Missing Test for Pagination

### Rule

Flag integrations using pagination where tests do not verify important
multi-page behavior.

Consider:

- first page
- additional pages
- final page
- empty page
- page boundary
- pagination termination

### Severity

MEDIUM

---

## MUNIT-057 — Missing Test for Retry Exhaustion

### Rule

Flag retry logic where tests verify successful retry but do not verify
behavior after all retries are exhausted.

### Severity

MEDIUM / HIGH

---

## MUNIT-058 — Test Does Not Verify Idempotent Result

### Rule

For idempotent processing, flag tests that do not verify that repeated
processing produces the expected single business outcome.

### Severity

MEDIUM / HIGH

---

## MUNIT-059 — Incorrect Expected Outcome

### Rule

Flag tests whose expected result does not match the actual API contract,
business rule, error handling, or downstream behavior.

### Severity

HIGH

---

## MUNIT-060 — Test Masks a Production Defect

### Rule

Flag tests that are structured in a way that allows an important
production defect to pass unnoticed.

Examples include:

- overly broad mocks
- weak assertions
- incorrect expected values
- testing the mock instead of the application
- bypassing the component under test

### Severity

HIGH

---

# MUnit False-Positive Controls

Do not report:

- missing tests for trivial code
- missing tests for purely cosmetic changes
- missing tests for implementation details with no meaningful behavior
- lack of mocks in intentionally designed integration tests
- small test data by itself
- similar tests when they cover different business scenarios
- detailed assertions that meaningfully validate behavior
- asynchronous waits that are required for correctness
- integration tests merely because they use external systems intentionally
- every uncovered branch automatically
- test naming differences that do not reduce clarity
- missing performance tests without evidence of a performance concern
- missing security tests for code with no security-sensitive behavior
- duplicate findings caused by the same underlying testing weakness

---

# MUnit Finding Quality Gate

Before reporting a MUnit finding:

1. Identify the flow or component.
2. Identify the behavior being tested.
3. Inspect the implementation.
4. Inspect existing tests.
5. Inspect assertions.
6. Inspect mocks.
7. Inspect verification.
8. Identify missing scenario.
9. Determine whether the scenario is important.
10. Verify that another test does not already cover the behavior.
11. Determine realistic production impact.
12. Confirm severity.
13. Identify the exact test or implementation location.

If existing tests adequately cover the behavior, do not report the finding.

---

# MUnit Finding Format

Use the following structure for every MUnit finding.

**Finding ID:** MUNIT-001

**Severity:** MEDIUM

**Category:** MUNIT

**File:** `src/test/munit/example-test.xml:45`

**Flow Under Test:** `example-flow`

**Location:** `test / execution / assertion / mock`

**Problem:**

Describe the testing weakness.

**Evidence:**

Identify the relevant test, assertion, mock, verification, or missing
scenario.

**Impact:**

Explain what production defect could escape detection.

**Recommendation:**

Provide an actionable testing improvement.

**Confidence:** HIGH / MEDIUM / LOW