# File: standards/munit/munit-standards.md

# MuleSoft MUnit Standards

## 1. Purpose

This document defines standards for reviewing MUnit tests in MuleSoft applications.

The review must determine whether tests are:

- Correct
- Meaningful
- Maintainable
- Deterministic
- Isolated
- Sufficiently comprehensive
- Focused on observable behavior
- Appropriate for the application's risk

The review should prioritize test quality over test-count metrics.

A large number of tests does not automatically indicate good coverage.

---

## 2. General Principles

MUnit tests should verify application behavior rather than implementation details.

Tests should clearly establish:

1. Test input
2. Expected behavior
3. Expected result
4. Relevant verification
5. Relevant error behavior

Avoid tests that pass without proving anything meaningful.

---

## 3. Test Naming

Test names should describe the behavior being tested.

Prefer:

    shouldReturnBadRequestWhenCustomerIdIsMissing

over:

    test1

or:

    testCustomer

A good test name should make the expected behavior understandable without opening the test implementation.

---

## 4. Test Structure

Tests should have a clear structure.

A typical structure is:

    Setup
    -> Execute
    -> Verify

Keep preparation, execution, and verification logically distinguishable.

---

## 5. Test Independence

Tests should be independent from one another.

A test should not depend on:

- Another test running first
- Shared mutable state
- Previous test output
- External execution order

Tests should be safely executable individually.

---

## 6. Determinism

Tests should produce predictable results.

Avoid depending on:

- Current time
- Random values
- External systems
- Network availability
- Local machine configuration
- Uncontrolled environment variables
- Non-deterministic ordering

When such dependencies are necessary, control them explicitly.

---

## 7. External Dependencies

External systems should generally be mocked in unit-level MUnit tests.

Examples:

- HTTP APIs
- Databases
- Salesforce
- SFTP
- Messaging systems
- External services

Unit tests should not require live production-like systems.

---

## 8. Mocking

Mocks should represent the behavior required by the test.

Do not mock every operation automatically.

A mock should be used when it:

- Is external to the unit
- Is expensive
- Is unavailable in the test environment
- Has non-deterministic behavior
- Must return controlled scenarios

---

## 9. Mock Accuracy

Mocked responses should resemble realistic responses from the dependency.

Avoid mocks that return unrealistic data simply to make the test pass.

---

## 10. Mock Scope

Mocks should be scoped narrowly enough that they do not accidentally affect unrelated operations.

A broad mock can cause a test to pass even when the actual implementation would fail.

---

## 11. Mocking Success and Failure

Tests should cover important dependency behaviors.

Examples:

- Successful response
- Timeout
- Connectivity failure
- Authentication failure
- Invalid response
- Empty response
- Unexpected response

Only include scenarios relevant to the application's actual behavior.

---

## 12. Verify Important Interactions

Where an interaction is part of the behavior, verify it.

Examples:

- Expected connector was invoked
- Expected downstream call occurred
- Correct parameters were supplied
- Operation occurred the expected number of times

Do not verify implementation details that are irrelevant to the contract.

---

## 13. Avoid Over-Verification

Do not assert every internal operation merely because it can be verified.

Overly strict tests can become brittle when implementation changes without changing behavior.

Focus on meaningful interactions.

---

## 14. Assertions

Tests must contain meaningful assertions.

An MUnit test that executes successfully but does not verify an outcome provides limited value.

Verify:

- Payload
- Attributes
- Variables
- Error type
- Error response
- Status code
- Important connector interaction

as appropriate.

---

## 15. Assertion Quality

Assertions should verify the intended behavior.

Avoid assertions that merely prove something exists when the actual value matters.

Weak:

    payload != null

when the contract requires a specific output.

Prefer assertions that verify the relevant structure and values.

---

## 16. Payload Assertions

Payload assertions should verify meaningful content.

Review:

- Structure
- Required fields
- Field values
- Types
- Array contents
- Ordering where relevant

Do not compare entire payloads when only a small portion is behaviorally important unless full equality is intentional.

---

## 17. Attribute Assertions

When attributes affect behavior, verify them.

Examples:

- HTTP status
- Headers
- Query parameters
- URI parameters

Do not ignore attributes when they are part of the operation's contract.

---

## 18. Variable Assertions

Variables should be asserted when they represent meaningful business or processing state.

Avoid asserting every temporary variable.

---

## 19. Error Assertions

Error scenarios should verify the correct error behavior.

Review:

- Error type
- Error description
- HTTP status
- Error response
- Propagation behavior

A test that only checks that "an error occurred" may be insufficient when a specific error is expected.

---

## 20. Expected Errors

Tests should explicitly expect errors when the scenario is intentionally negative.

Do not treat expected failures as unexpected test failures.

---

## 21. Error Mapping Tests

If the application maps internal errors to external responses, test the mapping.

Examples:

    HTTP:TIMEOUT
    -> 504

    VALIDATION
    -> 400

    DB:CONNECTIVITY
    -> 503

The exact mapping should follow the application's contract.

---

## 22. Error Handler Tests

Where error handling is important, test:

- Specific error types
- Generic/unexpected errors
- Continue behavior
- Propagate behavior
- Error response structure

---

## 23. Success Path

Every important flow should have tests for its primary successful behavior.

Verify the actual business result, not merely successful execution.

---

## 24. Failure Path

Important failure scenarios should be tested.

Examples:

- Invalid input
- Missing required field
- Downstream timeout
- Downstream error
- Database failure
- Authentication failure
- Authorization failure

Prioritize scenarios based on business and operational risk.

---

## 25. Boundary Conditions

Tests should cover meaningful boundary values.

Examples:

- Empty collection
- One record
- Maximum supported size
- Minimum value
- Maximum value
- Zero
- Null
- Missing field

Do not create boundary tests that have no meaningful business impact.

---

## 26. Null Input

Where null input is possible, test the expected behavior.

Verify whether the application should:

- Reject the request
- Return a validation error
- Produce an empty result
- Apply a default

Do not assume null should always be accepted.

---

## 27. Empty Input

Test empty input where it can occur in real operation.

Examples:

- Empty array
- Empty object
- Empty string
- Empty file
- Empty response

---

## 28. Missing Fields

Test requests missing required fields.

Verify:

- Validation behavior
- Error code
- Error message
- HTTP status
- Downstream invocation behavior

The application should not call downstream services unnecessarily when validation should fail first.

---

## 29. Invalid Data Types

Where input type validation matters, test invalid types.

Examples:

- String instead of number
- Invalid date
- Invalid boolean
- Invalid object structure

---

## 30. DataWeave Testing

Important DataWeave transformations should have tests covering:

- Normal input
- Null values
- Missing fields
- Empty collections
- Invalid values
- Boundary conditions

Complex transformations should receive proportionate test coverage.

---

## 31. API Testing

For API flows, tests should verify relevant:

- HTTP status
- Response payload
- Headers
- Validation behavior
- Authentication/authorization behavior where testable
- Downstream interaction

---

## 32. Connector Testing

Connector integrations should verify important connector behavior.

Examples:

- Correct operation
- Correct parameters
- Successful response handling
- Error handling
- Timeout behavior where relevant

Do not require live external services for unit tests unless the test is explicitly an integration test.

---

## 33. Database Testing

Database-dependent flows should isolate database behavior where appropriate.

Tests should cover:

- Successful operation
- No-result scenario
- Expected constraint failure
- Connectivity failure
- Timeout where relevant

Do not make unit tests dependent on a developer's local database.

---

## 34. Messaging Testing

Messaging flows should consider:

- Successful message processing
- Invalid message
- Processing failure
- Redelivery
- Dead-letter behavior where applicable

Tests should avoid uncontrolled external brokers for unit-level tests.

---

## 35. Scheduler Testing

Scheduled flows should be testable without waiting for an actual scheduler interval.

Invoke the relevant flow or processing logic directly where practical.

---

## 36. Batch Testing

Batch jobs should test meaningful behavior such as:

- Successful records
- Failed records
- Partial failures
- Empty input
- Aggregation
- Retry behavior where applicable

Do not test only that the batch starts.

---

## 37. Async Testing

Asynchronous processing requires care because execution may continue after the initiating flow returns.

Tests should reliably verify the expected asynchronous behavior without depending on arbitrary sleeps.

---

## 38. Avoid Arbitrary Sleeps

Avoid tests that depend on fixed delays such as:

    sleep(5000)

to wait for asynchronous behavior.

Such tests can become:

- Slow
- Flaky
- Environment-dependent

Prefer deterministic synchronization mechanisms where available.

---

## 39. Test Isolation

Tests should clean up resources they create.

Consider:

- Temporary files
- Database records
- Shared state
- Test variables
- External resources

Avoid leaving state that affects subsequent tests.

---

## 40. Test Data

Test data should be:

- Deterministic
- Understandable
- Representative
- Safe

Do not use real production data unless explicitly authorized and appropriately protected.

---

## 41. Sensitive Test Data

Do not commit:

- Production credentials
- API keys
- Access tokens
- Personal data
- Financial data
- Private certificates

Use safe synthetic test data.

---

## 42. Test Fixtures

Reusable test fixtures can improve consistency.

Use them when multiple tests require the same meaningful setup.

Avoid creating excessively abstract fixtures that make tests difficult to understand.

---

## 43. Test Data Builders

For complex payloads, builders or reusable fixtures may improve maintainability.

The resulting test should remain understandable.

A reviewer should be able to identify the important differences between test scenarios.

---

## 44. Duplicate Test Setup

Repeated setup should be considered for reuse when it becomes substantial.

Do not abstract tiny setup blocks merely to eliminate a few repeated lines.

---

## 45. Test Coverage

Coverage should be evaluated based on behavior and risk, not only percentage.

Important areas include:

- Core business logic
- Error handling
- Security-sensitive behavior
- Data transformations
- Integration boundaries
- Important edge cases

---

## 46. Coverage Gaps

Potential coverage gaps include:

- Important flow has only a happy-path test
- Error handlers are untested
- Validation is untested
- Downstream failures are untested
- Critical DataWeave mappings are untested
- Security behavior is untested
- Boundary conditions are ignored

---

## 47. Coverage Percentage

A high coverage percentage does not prove test quality.

Coverage tools may report code as covered even when assertions do not verify meaningful behavior.

Use coverage as a signal, not as the sole quality criterion.

---

## 48. Branch Coverage

Where practical, tests should exercise important decision branches.

Examples:

- Valid vs invalid input
- Success vs failure
- Authorized vs unauthorized
- Found vs not found
- Retry vs no retry

---

## 49. Negative Testing

Negative tests are particularly important for integration applications.

Consider:

- Invalid input
- Invalid authentication
- Invalid authorization
- Downstream failure
- Timeout
- Malformed response
- Missing configuration

---

## 50. Security Testing

Security-sensitive behavior should have appropriate tests.

Examples:

- Authentication failure
- Authorization failure
- Input validation
- Sensitive field filtering
- Secure error responses

Do not expose real credentials in security tests.

---

## 51. Idempotency Testing

Where retry or duplicate delivery is possible, test idempotent behavior where practical.

For example:

    same request
    -> repeated processing
    -> no unintended duplicate business operation

---

## 52. Retry Testing

Retry behavior should be tested where retry is part of the application's design.

Verify:

- Retry occurs when expected
- Retry count is bounded
- Backoff behavior is appropriate where testable
- Non-retryable errors are not retried

---

## 53. Mock Invocation Count

Invocation counts should be verified when the number of calls is part of expected behavior.

Examples:

- Exactly one database update
- Maximum three retries
- No downstream call when validation fails

Do not over-constrain calls that are implementation details.

---

## 54. Mock Argument Verification

Verify important arguments passed to mocks.

Examples:

- Customer ID
- Order ID
- Endpoint parameters
- Query parameters
- Important request fields

Do not assert irrelevant internal formatting.

---

## 55. Test Coupling

Tests should not depend unnecessarily on:

- Specific internal variable names
- Exact implementation structure
- Specific subflow layout
- Number of internal transformations

Tests should primarily verify externally meaningful behavior.

---

## 56. Brittle Tests

Potentially brittle tests include those that:

- Compare entire payloads unnecessarily
- Verify every internal call
- Depend on ordering that is not part of the contract
- Depend on timestamps
- Depend on random values
- Depend on environment-specific configuration

---

## 57. Test Maintainability

A test should remain understandable when implementation changes.

Prefer tests that describe behavior rather than implementation mechanics.

---

## 58. Test Readability

Tests should clearly communicate:

- What is being tested
- What input is provided
- What result is expected
- Why the scenario matters

Avoid overly complicated test setup.

---

## 59. Test Documentation

Comments should explain non-obvious test intent.

Good comments explain:

- Why a scenario exists
- Why a mock is required
- Why a particular boundary is important
- Why a workaround is necessary

Avoid comments that simply restate the test name.

---

## 60. Test Organization

Tests should be organized logically.

Examples:

- Success scenarios
- Validation scenarios
- Error scenarios
- Boundary scenarios
- Security scenarios

The exact organization may follow project conventions.

---

## 61. Test Naming Consistency

Use a consistent naming convention across the test suite.

Examples:

    shouldReturnCustomerWhenCustomerExists

    shouldReturnNotFoundWhenCustomerDoesNotExist

    shouldReturnBadRequestWhenCustomerIdIsMissing

Consistency improves discoverability.

---

## 62. Test Execution

Tests should be executable through the project's standard build process.

Review whether:

- MUnit tests are included in CI.
- Failures cause the expected build failure.
- Test reports are generated.
- Required test configuration is available.

---

## 63. CI Test Execution

MUnit tests should normally execute as part of CI for relevant code changes.

Do not configure CI to silently ignore test failures unless there is a documented reason.

---

## 64. Flaky Tests

Potential flaky-test indicators include:

- Arbitrary sleeps
- External service dependencies
- Current-time assertions
- Random data
- Shared state
- Uncontrolled concurrency
- Environment-specific assumptions

Flaky tests should be treated as a quality problem.

---

## 65. Time-Dependent Tests

Tests involving time should control or explicitly define time-dependent behavior where possible.

Avoid assertions that fail merely because execution occurs at a different time.

---

## 66. Random Data

Random test data should use deterministic seeds or controlled values when reproducibility matters.

A failing test should be reproducible.

---

## 67. Environment Dependencies

Tests should not depend unnecessarily on:

- Developer machine paths
- Local credentials
- Local services
- Specific operating systems
- Uncontrolled environment variables

---

## 68. Test Configuration

Test-specific configuration should be clearly separated from production configuration.

Do not allow MUnit tests to accidentally use production credentials or endpoints.

---

## 69. Test Credentials

Use mock credentials or safe test credentials.

Never commit real production credentials to MUnit configuration.

---

## 70. MUnit Test Resources

Test resources should be:

- Clearly named
- Minimal
- Relevant
- Safe

Remove obsolete fixtures and unused test resources.

---

## 71. XML Test Readability

MUnit XML should remain readable.

Avoid excessively large test definitions containing unrelated setup and verification.

Break complex scenarios into focused tests.

---

## 72. One Behavior Per Test

A test should preferably verify one logical behavior.

A single test may contain multiple assertions when they collectively verify the same behavior.

Avoid tests that verify many unrelated behaviors simultaneously.

---

## 73. Assertion Grouping

Multiple assertions are appropriate when they describe one result.

For example, verifying:

- HTTP status
- Error code
- Correlation ID

may be appropriate when all three form one error response contract.

---

## 74. Overly Broad Tests

Avoid tests that execute an entire application workflow merely to verify a small isolated behavior when a focused unit test is possible.

Use integration-level tests where end-to-end behavior is specifically required.

---

## 75. Unit vs Integration Tests

Clearly distinguish between:

- Unit tests
- Integration tests
- End-to-end tests

A test requiring live external infrastructure should not be mistaken for a fully isolated unit test.

---

## 76. External Service Contracts

Where appropriate, tests should verify assumptions about external responses.

However, contract testing should not require every unit test to call the live external service.

---

## 77. Regression Tests

When a significant defect is fixed, consider adding a regression test that reproduces the failure.

The test should fail before the fix and pass after the fix where practical.

---

## 78. Defect-Oriented Tests

Important production defects should result in tests when feasible.

Examples:

- Incorrect status mapping
- Duplicate processing
- Missing validation
- Incorrect transformation
- Error handler swallowing failures

---

## 79. Test Quality Smells

Potential test-quality problems include:

- No assertions
- Assertions unrelated to the scenario
- Excessive mocking
- Live external dependencies
- Arbitrary sleeps
- Shared mutable state
- Duplicate test logic
- Real credentials
- Production endpoints
- Tests that always pass regardless of implementation

---

## 80. False-Positive Tests

A test is suspicious if it can pass even when the behavior under test is broken.

Examples:

- Only checking that a flow completed
- Only checking that payload is non-null
- Mocking the entire flow under test
- Never verifying the output
- Catching and ignoring test errors

---

## 81. False-Negative Tests

A test is overly strict when harmless implementation changes cause failures.

Examples:

- Verifying irrelevant internal calls
- Comparing unstable timestamps
- Depending on unordered collection order
- Checking implementation-specific variable names

---

## 82. Test Security

MUnit test artifacts should not introduce security risks.

Review:

- Credentials
- Tokens
- Certificates
- Sensitive fixtures
- Production endpoints
- Personal data

---

## 83. Test Logging

Tests should avoid unnecessary sensitive logging.

Debug output from tests can accidentally expose credentials or payloads in CI logs.

---

## 84. CI Log Security

Ensure failed tests do not print:

- Passwords
- Tokens
- Secrets
- Private keys
- Sensitive payloads

A secret hidden from source code can still be exposed through a failed test log.

---

## 85. Test Cleanup

Tests that create resources should clean them up.

Examples:

- Temporary files
- Database records
- Mock state
- Message queues
- Test artifacts

---

## 86. Test Ordering

Tests should not rely on execution order.

If test order appears necessary, investigate shared-state or isolation problems.

---

## 87. Parallel Execution

If tests can execute in parallel, ensure they do not conflict through:

- Shared files
- Shared database records
- Shared ports
- Shared mutable state

---

## 88. MUnit Version Compatibility

MUnit configuration and test syntax should be compatible with the project's Mule runtime and MUnit version.

Do not recommend test syntax without considering project version compatibility.

---

## 89. Test Dependency Management

MUnit dependencies should be properly configured.

Avoid unnecessary test dependencies that increase build complexity.

---

## 90. Test Execution Time

Tests should execute within a reasonable time for CI.

Potential concerns include:

- Excessive integration tests
- Large fixtures
- Repeated expensive setup
- Arbitrary sleeps
- Unnecessary external calls

---

## 91. Slow Tests

Slow tests should be investigated when they materially affect development or CI feedback.

Do not optimize trivial test execution time at the expense of meaningful coverage.

---

## 92. Test Suite Balance

A healthy suite should contain a reasonable balance of:

- Success tests
- Failure tests
- Boundary tests
- Security tests where applicable
- Integration-boundary tests

The exact ratio depends on application complexity and risk.

---

## 93. MUnit Review Checklist

Before completing the MUnit review, confirm:

- Important flows have meaningful tests.
- Test names describe behavior.
- Tests are deterministic.
- Tests are independent.
- External dependencies are mocked where appropriate.
- Mocks return realistic responses.
- Important interactions are verified.
- Assertions verify meaningful outcomes.
- Error scenarios are tested.
- Success scenarios are tested.
- Validation scenarios are tested.
- Null and empty inputs are considered.
- Boundary conditions are considered.
- Security-sensitive behavior is tested where appropriate.
- Retry behavior is tested where relevant.
- Idempotency is tested where relevant.
- Tests do not use real production credentials.
- Tests do not depend on production endpoints.
- Arbitrary sleeps are avoided.
- Shared state is minimized.
- Test cleanup is performed.
- Tests do not depend on execution order.
- Tests are included in CI.
- Test failures are not silently ignored.
- CI logs do not expose secrets.
- Tests are not unnecessarily coupled to implementation details.
- Tests are maintainable.
- Important production defects have regression coverage where appropriate.
- MUnit syntax is compatible with the project version.

---

## 94. MUnit Quality Gate

The reviewer must be able to answer the following questions:

1. Do the tests verify actual application behavior?
2. Would the tests fail if the important behavior were broken?
3. Are both success and meaningful failure paths covered?
4. Are important boundary conditions covered?
5. Are external dependencies controlled?
6. Are tests deterministic and independent?
7. Could the tests expose secrets in source code or CI logs?
8. Are assertions focused on meaningful outcomes?
9. Are tests overly coupled to implementation details?
10. Are retry and error-handling behaviors tested where required?
11. Are security-sensitive behaviors tested where appropriate?
12. Are tests executed reliably in CI?
13. Are flaky-test risks minimized?
14. Are regression tests added for important defects?
15. Is the test suite providing meaningful confidence rather than merely high coverage?

### Final Question

> If an important piece of application behavior were accidentally broken, would the MUnit test suite reliably detect it without depending on external systems, hidden state, or fragile implementation details?