# MuleSoft MUnit Analysis Skill

## Purpose

Perform a comprehensive MUnit test coverage and quality review of the MuleSoft application.

Review the application as a:

- Senior MuleSoft Architect
- Senior QA Architect
- Senior Technical Lead

The objective is to determine whether the MuleSoft application has sufficient, meaningful, maintainable, and production-relevant MUnit coverage.

The review must not measure quality by test-count alone.

A large number of weak tests is not considered good coverage.

The analysis must identify:

- Missing MUnit coverage.
- Important flows without tests.
- Missing negative-path tests.
- Missing error-handler tests.
- Missing connector failure tests.
- Missing boundary-condition tests.
- Weak assertions.
- Tests that only execute a flow without validating behavior.
- Duplicate tests.
- Fragile tests.
- Poor test data practices.
- Environment-dependent tests.
- Missing mocks.
- Missing verification of important interactions.
- Missing regression coverage.

Every meaningful finding MUST include a practical solution.

---

# 1. Repository Scope

The MuleSoft application is:

${GITHUB_WORKSPACE}

The code-review framework is:

${GITHUB_WORKSPACE}/code-review

The reports directory is:

${GITHUB_WORKSPACE}/reports

Review the complete MuleSoft application.

---

# 2. Mandatory Exclusions

Do NOT review these directories as MuleSoft application source:

${GITHUB_WORKSPACE}/code-review/**
${GITHUB_WORKSPACE}/reports/**

Do not report findings against:

- Review agents.
- Review skills.
- Prompt files.
- Framework scripts.
- Generated reports.

---

# 3. MUnit Discovery

Identify all MUnit tests.

Look for:

- `src/test/munit/**`
- MUnit XML files.
- MUnit test suites.
- Test flows.
- Test configurations.
- MUnit mocks.
- MUnit spies.
- MUnit verification scopes.
- MUnit assertions.

Do not assume every XML file under `src/test` is an MUnit test.

Confirm based on content.

---

# 4. Application Flow Inventory

Before assessing coverage, identify the application flows.

Review:

- Main flows.
- Subflows.
- Private flows.
- Error handlers.
- Scheduler-triggered flows.
- HTTP listener flows.
- Messaging flows.
- Batch flows.
- Event-driven flows.
- File-processing flows.
- Reusable processing flows.

The purpose is to establish what functionality should reasonably be tested.

---

# 5. Test Coverage Mapping

Map application functionality to MUnit tests.

Create an internal matrix:

| Application Flow | Flow Type | Business Importance | MUnit Exists | Happy Path | Negative Path | Error Handler | Connector Failure | Assertions |
|---|---|---|---|---|---|---|---|---|

Use:

Covered

Partially Covered

Not Covered

Not Applicable

where appropriate.

Do not claim exact runtime coverage percentages unless actual test coverage metrics are available.

---

# 6. Coverage Philosophy

Do not equate:

Number of tests

with:

Quality of testing.

Evaluate:

- Functional coverage.
- Branch coverage.
- Error coverage.
- Boundary coverage.
- Integration behavior.
- Business-rule coverage.
- Regression coverage.

---

# 7. Critical Flow Identification

Prioritize tests for:

- Customer-facing APIs.
- Financial operations.
- Authentication-related functionality.
- Order processing.
- Transaction processing.
- Important integrations.
- Data transformation.
- Error handling.
- Scheduled jobs.
- Batch processing.

Do not assume business criticality without evidence.

Use the implementation and naming/context to determine likely importance.

---

# 8. Happy Path Tests

Determine whether important flows have tests covering successful execution.

Examples:

- Valid request.
- Valid payload.
- Successful connector response.
- Successful database operation.
- Successful transformation.

A happy-path test should validate meaningful behavior.

---

# 9. Weak Happy Path Tests

Identify tests that merely execute a flow without meaningful validation.

Examples:

- Flow executes successfully.
- No exception occurs.
- Test ends with no assertions.

A test that only proves "the flow did not crash" may be insufficient for important business functionality.

Recommend assertions against:

- Payload.
- Attributes.
- Variables.
- Status.
- Output.
- Connector invocation.
- Business result.

---

# 10. Assertions

Evaluate whether tests contain meaningful assertions.

Look for:

- Assert That.
- Verify Call.
- Assert Equals.
- Assert Expression.
- Expected payload.
- Expected attributes.
- Expected variables.

Do not require a particular MUnit assertion type.

The assertion should validate intended behavior.

---

# 11. Missing Assertions

Report tests that:

- Execute important functionality.
- Do not verify the result.
- Would pass even if the business output were incorrect.

Provide a practical solution.

Example:

Replace execution-only validation with assertions against the expected payload and important attributes.

---

# 12. Negative Path Testing

Determine whether important flows test failure scenarios.

Examples:

- Invalid request.
- Missing required field.
- Invalid data.
- Downstream API failure.
- Database failure.
- Timeout.
- Authentication failure.
- File unavailable.
- Message failure.

Do not require every possible failure combination.

Prioritize realistic and business-impacting failures.

---

# 13. Error Handler Testing

Review application error handlers.

Look for:

- On Error Continue.
- On Error Propagate.
- Try scopes.
- Global error handlers.
- Flow-level error handlers.

Determine whether meaningful error-handling behavior is tested.

---

# 14. On Error Continue

Where On Error Continue is used, tests should verify:

- Expected continuation.
- Error response.
- Variables/attributes after error.
- Logging behavior where appropriate.
- Downstream behavior.

Do not report On Error Continue itself as a defect.

---

# 15. On Error Propagate

Where On Error Propagate is used, tests should verify:

- Error propagation.
- Error type.
- Error response.
- Correct downstream behavior.

---

# 16. Connector Failure Tests

Important external integrations should have failure-path coverage where appropriate.

Examples:

HTTP:

- 400.
- 401.
- 403.
- 404.
- 429.
- 500.
- Timeout.

Database:

- Connection failure.
- Query failure.
- Constraint error.

SFTP:

- Connection failure.
- Missing file.
- Permission failure.

Do not require every status code if several codes are handled identically.

Group equivalent scenarios where appropriate.

---

# 17. Mocking External Systems

Review whether external systems are appropriately mocked in unit tests.

Look for:

- Mock When.
- Then Return.
- Spy.
- Verify Call.

Unit tests should generally avoid depending on live external systems.

Do not report a missing mock if the operation is genuinely local and deterministic.

---

# 18. External System Isolation

Identify tests that appear to require:

- Real database.
- Real HTTP endpoint.
- Real SFTP server.
- Real Salesforce instance.
- Real messaging system.

Such tests may be integration tests rather than unit tests.

Report when external dependencies make MUnit tests:

- Slow.
- Fragile.
- Environment-dependent.
- Difficult to reproduce.

Recommend appropriate mocking or separate integration testing.

---

# 19. Mock Accuracy

Mocks should represent realistic downstream behavior.

Review whether mocks:

- Return expected payloads.
- Return expected attributes.
- Represent errors realistically.
- Include required fields.

Do not require overly complex mocks.

---

# 20. Verify Call

For important integrations, consider whether tests verify the expected interaction.

Examples:

- Correct connector called.
- Correct operation invoked.
- Expected number of calls.
- Expected parameters.

Do not require Verify Call when output assertions already provide sufficient confidence.

---

# 21. Call Count

Identify tests that should verify:

- One call.
- No call.
- Multiple calls.

Especially important when:

- Retry exists.
- Conditional branches exist.
- Duplicate calls are possible.

---

# 22. Retry Testing

Where retry behavior exists, consider testing:

- Initial failure.
- Retry.
- Successful retry.
- Retry exhaustion.
- Final error.

Do not require exhaustive retry testing for trivial retry configurations.

---

# 23. Timeout Testing

Where timeout behavior is business-critical, consider tests for:

- Timeout.
- Error handling.
- Retry.
- Final response.

Do not attempt to create real long-running timeouts unnecessarily.

Prefer mocking the failure behavior.

---

# 24. DataWeave Testing

Important transformations should have meaningful test coverage.

Test:

- Valid input.
- Missing fields.
- Null values.
- Empty arrays.
- Unexpected values.
- Boundary values.
- Data type variations.

Do not create a separate test for every trivial mapping.

---

# 25. Null Handling

Evaluate whether transformations correctly handle:

- Null.
- Missing.
- Empty string.
- Empty array.
- Empty object.

Report missing coverage where null/empty input can cause production failures.

---

# 26. Boundary Testing

Consider:

- Zero.
- One.
- Maximum expected value.
- Empty collections.
- Large collections.
- Minimum/maximum dates.
- Boundary strings.
- Optional fields.

Only recommend boundary cases relevant to the implementation.

---

# 27. Business Rule Testing

Identify important business rules implemented in:

- Choice.
- DataWeave.
- Validation.
- Expressions.
- Routing.
- Filters.

Ensure meaningful branches have tests.

---

# 28. Choice Coverage

For Choice routers, determine whether important branches are tested.

Example:

if condition A
else if condition B
else

Ideally test:

- Condition A.
- Condition B.
- Default path.

Do not require every branch when several branches are equivalent and low-risk.

---

# 29. Until Successful Testing

Where Until Successful is used, test meaningful behavior such as:

- Success on first attempt.
- Failure followed by success.
- Failure after maximum retries.

---

# 30. Batch Testing

Where Batch Job is used, review whether tests cover:

- Valid records.
- Invalid records.
- Record-level errors.
- Batch completion.
- Aggregation behavior.

Do not force API-style unit tests onto batch architecture.

---

# 31. Scheduler Testing

For scheduled flows, focus on the processing logic rather than waiting for the actual scheduler.

Where possible:

- Invoke the processing flow directly.
- Mock external systems.
- Validate successful processing.
- Validate failure behavior.

---

# 32. File Processing Testing

For file flows, consider:

- File exists.
- File missing.
- Empty file.
- Invalid file.
- Duplicate file.
- Large file behavior where appropriate.
- Processing success.
- Processing failure.

Do not require actual filesystem integration for every unit test.

---

# 33. Messaging Testing

For messaging flows, consider:

- Valid message.
- Invalid message.
- Consumer failure.
- Processing failure.
- Redelivery behavior where applicable.

Use mocks where practical.

---

# 34. API Testing

For API flows, review whether tests cover:

- Valid request.
- Invalid request.
- Required field missing.
- Invalid data.
- Successful response.
- Error response.
- Authorization/security behavior where testable.

API security itself belongs to api-security-analysis.

---

# 35. HTTP Listener Testing

Where appropriate, tests should validate:

- Request handling.
- Response payload.
- Status.
- Headers.
- Error behavior.

Do not require direct listener testing when the core implementation is better tested through the underlying flow.

---

# 36. Error Response Testing

Where API/application errors are standardized, tests should verify:

- Status.
- Error type.
- Error code.
- Message.
- Required metadata.

Avoid asserting overly implementation-specific details that make tests fragile.

---

# 37. Test Data

Review whether test data is:

- Readable.
- Maintainable.
- Representative.
- Reusable where appropriate.
- Free from real credentials.
- Free from production-sensitive data.

Never expose secrets or production PII in findings.

---

# 38. Test Data Duplication

Identify excessive duplication in test payloads and setup.

Where appropriate recommend:

- Shared test fixtures.
- Reusable test data.
- Helper flows.

Do not over-abstract simple tests.

---

# 39. Environment Independence

Tests should not depend unnecessarily on:

- Developer machine paths.
- Production endpoints.
- Environment-specific credentials.
- Local files.
- External services.

Report environment dependency when it reduces test reliability.

---

# 40. Test Isolation

Tests should be independently executable where practical.

Look for:

- Shared mutable state.
- Ordering dependency.
- Shared external state.
- Test data dependency.

Recommend isolation where necessary.

---

# 41. Flaky Test Indicators

Look for patterns such as:

- Real external systems.
- Time-dependent assertions.
- Hard-coded delays.
- Uncontrolled asynchronous behavior.
- Shared state.
- Random data without deterministic control.

Do not claim a test is flaky solely from one suspicious pattern.

Use:

Potential Flakiness

when appropriate.

---

# 42. Hard-Coded Waits

Identify:

- Sleep.
- Fixed delays.
- Long waits.

Evaluate whether they can make tests slow or unreliable.

Prefer deterministic synchronization where possible.

---

# 43. Test Naming

Evaluate whether test names clearly communicate:

- Scenario.
- Expected behavior.
- Failure condition where relevant.

Avoid reporting every naming difference.

Example of a useful name:

shouldReturnCustomerNotFoundWhenCustomerDoesNotExist

---

# 44. Test Organization

Evaluate:

- Test suite organization.
- Logical grouping.
- Reusable setup.
- Clear test naming.
- Separation of concerns.

Do not over-engineer test structure.

---

# 45. Duplicate Tests

Identify tests that validate substantially identical behavior.

Do not report tests as duplicates merely because they use similar setup.

Consider:

- Same input.
- Same mocked behavior.
- Same assertions.
- Same expected result.

---

# 46. Regression Coverage

Identify important previously implemented functionality that appears to have no regression tests.

Examples:

- Complex transformations.
- Important business rules.
- Known error paths.
- Important integrations.

Do not assume historical production incidents unless documented.

---

# 47. Test Maintainability

Review:

- Excessive duplication.
- Brittle assertions.
- Excessive implementation-specific assertions.
- Complex setup.
- Hard-coded environment values.

Recommendations should improve maintainability without reducing coverage.

---

# 48. Test Quality Categories

Classify findings as:

- Coverage
- Assertion Quality
- Error Handling
- Mocking
- Test Isolation
- Test Data
- Maintainability
- Reliability
- Performance
- Regression

---

# 49. MUnit Coverage Matrix

Produce an internal matrix:

| Flow | MUnit | Happy Path | Negative Path | Error Handler | Assertions | External Mock | Assessment |
|---|---|---|---|---|---|---|---|

Use:

Good

Partial

Missing

Not Applicable

---

# 50. MUnit Findings

Every finding MUST contain:

## Finding ID

Example:

MULE-MUNIT-001

## Title

Concise test issue.

## Severity

High / Medium / Low / Warning

## Category

MUnit

## Location

Flow/test file.

## Evidence

Observed implementation.

## Impact

Why the missing or weak test matters.

## Recommendation

What should be tested or improved.

## Solution

Provide the actual test scenario that should be added or improved.

## Priority

Immediate / Short Term / Medium Term / Long Term

---

# 51. Severity Guidelines

## High

Important production-critical flow has no meaningful test coverage or has severe testing gaps.

## Medium

Meaningful coverage gap or weak validation.

## Low

Minor test quality issue.

## Warning

Coverage cannot be fully established without runtime/test execution data.

Do not classify every missing test as High.

---

# 52. MUnit Test Recommendations

When coverage is missing, provide concrete scenarios.

Example:

Flow:

processOrder

Recommended tests:

1. shouldProcessValidOrder
2. shouldRejectInvalidOrder
3. shouldHandleDatabaseFailure
4. shouldHandleDownstreamTimeout
5. shouldReturnExpectedResponse

Do not merely say:

"Add more tests."

---

# 53. Test Case Recommendations

Recommended test cases should include:

- Test name.
- Scenario.
- Input condition.
- Mock behavior.
- Expected result.
- Important assertions.

Example:

Test:

shouldReturnCustomerNotFoundWhenCustomerDoesNotExist

Given:

Customer API returns 404.

Expected:

Application returns the defined not-found response.

Assertions:

- Response status.
- Error code.
- Response payload.

---

# 54. No Runtime Coverage Claims

If tests are not executed during the review, do not claim:

"80% coverage"

or any exact runtime coverage percentage.

You may provide:

Static coverage assessment

based on source inspection.

Clearly label it as static analysis.

---

# 55. Test Execution

If the review process has access to Maven/MUnit execution, consider:

- `mvn test`
- MUnit execution
- Coverage reports

Use actual results when available.

If tests cannot be executed:

State:

"Runtime MUnit execution was not available during this review."

Do not fabricate results.

---

# 56. Positive MUnit Observations

Identify good practices such as:

- Strong flow coverage.
- Meaningful assertions.
- Good mocking.
- Negative-path coverage.
- Error-handler tests.
- Clear test naming.
- Reusable fixtures.
- Good isolation.
- Regression coverage.

---

# 57. Cross-Skill Boundaries

Detailed findings owned by these skills should not be duplicated unnecessarily:

- mulesoft-architecture
- mule-code-quality
- connector-analysis
- api-security-analysis
- security-analysis
- performance-analysis
- configuration-analysis
- logging-analysis
- duplication-analysis

This skill owns MUnit and automated test quality.

If a production flow has a performance problem, performance-analysis owns the performance finding.

If the flow lacks tests for that behavior, MUnit owns the coverage finding.

The final report reviewer should consolidate related findings.

---

# 58. No Unsupported Claims

Never claim:

- Exact code coverage percentage.
- Test pass percentage.
- Tests are flaky.
- Tests are failing.

unless actual test execution or coverage evidence supports the statement.

Use:

Static Analysis

or:

Verification Required

where appropriate.

---

# 59. MUnit Score

Provide an MUnit quality score based on:

- Important flow coverage.
- Happy-path coverage.
- Negative-path coverage.
- Error-handler coverage.
- Assertions.
- Mocking.
- Isolation.
- Maintainability.
- Regression coverage.

Do not calculate the score solely from test count.

---

# 60. Final Output

Return structured MUnit analysis containing:

## MUnit Summary

## Application Flow Inventory

## MUnit Test Inventory

## Static Coverage Assessment

## Happy Path Assessment

## Negative Path Assessment

## Error Handler Assessment

## Mocking Assessment

## Assertion Quality Assessment

## Test Isolation Assessment

## Test Data Assessment

## Test Maintainability Assessment

## Positive MUnit Observations

## MUnit Findings

## Recommended Test Cases

## Verification Required

## MUnit Score

Do not generate the final Word document from this skill.

The word-report-generation skill is responsible for creating the final `.docx`.

---

# 61. Quality Standard

Before completing the review, ask:

"Would a Senior QA Architect trust this MUnit assessment as a realistic production test-quality review?"

If not:

- Remove trivial findings.
- Do not equate test count with quality.
- Re-check flow coverage.
- Provide concrete missing test scenarios.
- Distinguish static analysis from executed coverage.
- Prioritize business-critical functionality.
- Ensure every meaningful finding has a practical solution.

The objective is production-quality MUnit assessment, not a generic testing checklist.