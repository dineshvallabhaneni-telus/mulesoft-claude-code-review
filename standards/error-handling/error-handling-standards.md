# File: standards/error-handling/error-handling-standards.md

# MuleSoft Error Handling Standards

## 1. Purpose

This document defines standards for reviewing error handling in MuleSoft applications.

The review must determine whether error handling is:

- Correct
- Predictable
- Secure
- Maintainable
- Observable
- Appropriate for the failure type
- Consistent with the API or integration contract
- Capable of preserving important failures
- Appropriate for retry and recovery scenarios

The review must distinguish between:

- Technical errors
- Connectivity errors
- Validation errors
- Business errors
- Security errors
- Configuration errors
- Unexpected system failures

Do not report an error-handling difference as a defect merely because another implementation approach exists.

---

## 2. General Principles

Error handling should:

- Detect failures
- Preserve important failure information
- Return appropriate responses
- Avoid leaking sensitive implementation details
- Provide useful operational diagnostics
- Avoid hiding unexpected failures
- Support appropriate recovery
- Prevent duplicate processing where relevant

Errors should be handled at the narrowest reasonable scope.

---

## 3. Error Classification

Review whether errors are correctly classified.

Common categories include:

- Input validation failure
- Authentication failure
- Authorization failure
- Connectivity failure
- Timeout
- Downstream server failure
- Rate limiting
- Database failure
- Messaging failure
- Business rule violation
- Configuration failure
- Unexpected application failure

Incorrect classification can lead to inappropriate retry or response behavior.

---

## 4. Specific Error Handling

Prefer specific error types when the application knows which failure it is handling.

Avoid catching every possible error when only a specific error is expected.

Broad error handling should have a clear architectural reason.

---

## 5. Broad Error Handling

Use broad handlers such as `ANY` carefully.

Broad handlers can accidentally:

- Hide programming defects
- Convert unexpected failures into successful responses
- Prevent proper error propagation
- Make troubleshooting difficult

If broad handling is required, ensure unexpected errors remain observable.

---

## 6. On Error Continue

`On Error Continue` should only be used when continuing after an error is intentional.

Review whether the flow:

- Can safely continue
- Produces a valid result
- Maintains data integrity
- Does not hide a failure

Using `On Error Continue` merely to prevent an error response is a potential defect.

---

## 7. On Error Propagate

`On Error Propagate` should be used when the failure must remain visible to the caller or parent scope.

Review whether:

- The error is correctly propagated.
- Required logging occurs.
- The response is correctly constructed.
- Sensitive details are not exposed.

---

## 8. Error Handler Scope

Error handlers should be scoped appropriately.

Avoid placing an error handler around a very large section of processing when different operations require different recovery behavior.

Prefer precise boundaries where practical.

---

## 9. Flow-Level Error Handling

Flow-level error handling may be appropriate for common behavior such as:

- Standard error responses
- Correlation ID handling
- Common logging
- Error mapping

Do not centralize unrelated recovery logic merely for convenience.

---

## 10. Global Error Handling

Global error handling should be used carefully.

It should provide common behavior without masking errors that require local handling.

---

## 11. Error Propagation

Errors must not disappear silently.

Review:

- Empty error handlers
- `On Error Continue`
- Generic catch blocks
- Error suppression
- Fallback responses

A failure should remain visible when it affects business correctness or system availability.

---

## 12. Error Mapping

Internal Mule errors may need to be mapped to application-specific errors.

For example:

    HTTP:TIMEOUT
    -> downstream timeout

    DB:CONNECTIVITY
    -> database unavailable

    VALIDATION
    -> invalid request

Mappings should be consistent and intentional.

---

## 13. API Error Responses

API error responses should provide appropriate:

- HTTP status code
- Error code
- Message
- Correlation ID
- Optional details

Do not expose internal stack traces or implementation details.

---

## 14. HTTP Status Codes

Use status codes according to the API contract.

Typical examples:

- `400` — invalid request
- `401` — unauthenticated
- `403` — unauthorized
- `404` — resource not found
- `409` — conflict
- `429` — rate limited
- `500` — unexpected server error
- `502` — downstream gateway/service issue
- `503` — service unavailable
- `504` — downstream timeout

The exact mapping depends on the API contract and business requirements.

---

## 15. Client Errors

Client-caused failures should not normally be represented as generic server errors.

Examples:

- Invalid input
- Missing required field
- Invalid format
- Unsupported operation

These should be mapped consistently to the appropriate client-facing response.

---

## 16. Authentication Errors

Authentication failures should not be treated as generic internal failures.

Review:

- HTTP status
- Error response
- Logging
- Sensitive data handling

Do not reveal authentication implementation details.

---

## 17. Authorization Errors

Authorization failures should be distinguishable from authentication failures where the API contract requires it.

Do not disclose information that could help an attacker determine internal authorization rules.

---

## 18. Validation Errors

Validation failures should provide enough information for the client to correct the request without exposing sensitive implementation details.

Where appropriate, identify:

- Field
- Validation rule
- Error code

Avoid exposing internal exception messages.

---

## 19. Business Errors

Business-rule failures should be distinguished from technical failures.

Examples:

- Customer is inactive
- Order cannot be cancelled
- Account limit exceeded
- Duplicate transaction

Do not retry business errors as though they were transient infrastructure failures.

---

## 20. Downstream Errors

Errors from external systems should be translated appropriately.

Do not blindly expose downstream:

- Stack traces
- URLs
- Hostnames
- Database errors
- Internal identifiers
- Authentication details

---

## 21. Database Errors

Database failures should be handled according to their type.

Examples:

- Connectivity failure
- Timeout
- Constraint violation
- Deadlock
- Query failure

Do not expose raw database errors to API consumers.

---

## 22. Database Constraint Errors

Constraint violations should be mapped appropriately when they represent expected business conditions.

For example:

- Duplicate record
- Missing parent record
- Invalid relationship

Do not return generic `500` responses when a meaningful business response is appropriate.

---

## 23. Timeout Errors

Timeouts should be handled separately from other errors where recovery behavior differs.

Review:

- Retry behavior
- Response status
- Logging
- Correlation
- Idempotency

Do not retry indefinitely.

---

## 24. Connectivity Errors

Connectivity failures should be treated as potentially transient.

Review:

- Retry
- Reconnection
- Timeout
- Circuit breaking where applicable
- Downstream availability

---

## 25. Rate-Limit Errors

Rate-limit failures should not normally be retried immediately without considering the downstream service's guidance.

Review:

- Retry delay
- Backoff
- Maximum attempts
- `Retry-After` behavior where applicable

---

## 26. Retryable Errors

Only retry errors that are reasonably likely to succeed later.

Potentially retryable:

- Temporary connectivity failure
- Timeout
- Temporary service unavailability
- Transient messaging failure

Usually not retryable:

- Validation failure
- Authentication failure
- Authorization failure
- Invalid request
- Business-rule failure

---

## 27. Retry Limits

Retries must be bounded.

Review:

- Maximum attempts
- Maximum elapsed time
- Backoff
- Jitter where appropriate

Avoid infinite retry loops.

---

## 28. Retry Amplification

Retry mechanisms can increase load on an already failing downstream system.

Review whether:

- Multiple layers retry the same request.
- Parallel requests retry simultaneously.
- Large batches retry together.
- Backoff is absent.

Avoid retry storms.

---

## 29. Idempotency

Retryable operations should be evaluated for idempotency.

Examples:

- Create order
- Submit payment
- Publish message
- Insert record
- Update external resource

A retry must not unintentionally duplicate a business transaction.

---

## 30. Error Handling and Transactions

Review how errors interact with transactions.

A failure should correctly trigger rollback when transactional semantics require it.

Do not assume external systems participate in the same transaction.

---

## 31. Partial Failure

Distributed integrations can partially succeed.

Example:

    Database update
    -> HTTP call
    -> messaging operation

If the later operation fails, the earlier operation may not be automatically reversible.

Review whether the application has an appropriate strategy.

---

## 32. Compensation

Where rollback across systems is impossible, consider whether compensation is required.

Possible strategies include:

- Compensating transaction
- Retry
- Dead-letter queue
- Reconciliation
- Manual recovery

Do not require compensation where the business process does not need it.

---

## 33. Messaging Errors

Messaging flows should define intentional behavior for:

- Processing failure
- Redelivery
- Maximum retries
- Dead-letter handling
- Poison messages

Avoid infinite redelivery.

---

## 34. Poison Messages

A message that repeatedly fails should not remain indefinitely in the normal processing path.

Consider:

- Maximum redelivery
- Dead-letter queue
- Error queue
- Operational alerting

---

## 35. Duplicate Messages

Error handling should consider duplicate delivery.

Where message processing is not inherently idempotent, implement an appropriate deduplication or idempotency strategy.

---

## 36. Error Logging

Errors should generate sufficient diagnostic information.

Useful information may include:

- Correlation ID
- Flow name
- Error type
- Operation
- External system
- Safe contextual identifiers

Do not log secrets or sensitive payloads.

---

## 37. Stack Traces

Stack traces may be useful internally but should not normally be returned to external API consumers.

If stack traces are logged, ensure logs are appropriately protected.

---

## 38. Sensitive Error Information

Do not expose:

- Passwords
- Access tokens
- API keys
- Database credentials
- Internal hostnames
- File system paths
- SQL statements containing sensitive values
- Stack traces
- Internal implementation details

---

## 39. Error Messages

Error messages should be:

- Clear
- Actionable where appropriate
- Consistent
- Safe for the intended audience

Avoid vague messages such as:

    Something went wrong

when a useful safe description can be provided.

---

## 40. Internal vs External Error Messages

Maintain a distinction between:

- Internal diagnostic information
- External consumer-facing information

Internal logs may contain more technical detail than API responses, subject to security and privacy requirements.

---

## 41. Correlation IDs

Error responses should include a correlation identifier when appropriate.

The identifier should allow operations teams to locate the corresponding logs.

---

## 42. Correlation ID Preservation

If an incoming request already has an accepted correlation ID, preserve it according to the application's tracing standard.

Do not overwrite it unnecessarily.

---

## 43. Error Response Consistency

APIs should use a consistent error response structure.

For example:

    {
      "errorCode": "...",
      "message": "...",
      "correlationId": "..."
    }

The exact structure must follow the application's API contract.

---

## 44. Error Code Standards

Error codes should be:

- Stable
- Meaningful
- Documented
- Independent from internal exception class names

Avoid exposing raw Mule error identifiers as the public business error code unless intentionally defined by the API contract.

---

## 45. Error Details

Detailed validation information may be useful for client errors.

However, details should not expose:

- Secrets
- Internal architecture
- Stack traces
- Database details
- Internal hostnames

---

## 46. Error Handler Duplication

Repeated error-handling logic should be considered for reuse.

Examples:

- Standard error response
- Common logging
- Correlation ID extraction
- Error mapping

Do not abstract error handlers when the behavior intentionally differs.

---

## 47. Error Handler Ordering

When multiple error handlers are present, ordering and specificity must be intentional.

A broad handler should not intercept an error that should be handled by a more specific handler.

---

## 48. Error Type Matching

Verify that error types used in handlers actually match the errors generated by the relevant operation.

A handler that can never execute is a defect.

---

## 49. Error Handler Reachability

Review whether:

- Error handlers are reachable.
- Earlier handlers consume errors.
- Error mappings are shadowed.
- Broad handlers intercept specific errors.

---

## 50. Empty Error Handlers

An empty error handler is suspicious.

Determine whether the error is intentionally ignored.

If not, report the failure to preserve or propagate the error.

---

## 51. Logging Without Propagation

Logging an error does not necessarily mean the error has been handled.

Review patterns such as:

    log error
    continue successfully

If the operation actually failed, ensure the failure is propagated or represented correctly.

---

## 52. Success Responses After Failure

Pay particular attention to flows that return a successful response after:

- Downstream failure
- Database failure
- Transformation failure
- Validation failure

This can create false-positive business outcomes.

---

## 53. Fallback Responses

Fallback behavior should be explicit and justified.

Do not return stale, empty, or default data merely to avoid returning an error unless the business requirement permits it.

---

## 54. Error Recovery

Recovery should restore the application to a valid state.

Review whether recovery:

- Leaves partial data
- Leaves messages unacknowledged
- Creates duplicates
- Leaves files locked
- Leaves transactions open

---

## 55. Cleanup After Errors

Where appropriate, error handling should clean up:

- Temporary files
- Resources
- Streams
- Variables
- Temporary records

Do not perform cleanup that could itself hide the original failure.

---

## 56. Error Handling in Parallel Processing

Review error behavior in:

- Parallel For Each
- Scatter-Gather
- Batch
- Async processing

Determine:

- Whether one failure stops all processing.
- Whether partial results are acceptable.
- Whether failed items can be retried.
- Whether duplicate processing is possible.

---

## 57. Batch Error Handling

Batch processing should define behavior for failed records.

Review:

- Failed record handling
- Retry
- Aggregation
- Dead-letter behavior
- Reporting
- Partial completion

---

## 58. Async Error Handling

Asynchronous processing requires explicit error visibility.

An error occurring after the original request has completed must still be:

- Logged
- Tracked
- Alerted
- Stored
- Otherwise observable

where operationally required.

---

## 59. Scheduled Flow Errors

Scheduled jobs should not silently fail.

Review:

- Error logging
- Retry
- Alerting
- Job status
- Partial processing
- Duplicate execution

---

## 60. Error Handling and Monitoring

Important failures should be observable through the application's operational monitoring strategy.

Review whether critical errors can be detected without manually inspecting logs.

---

## 61. Error Handling and Security

Security failures should not be handled in a way that weakens security controls.

Examples:

- Authentication failure followed by anonymous access
- Authorization failure followed by default access
- Certificate failure followed by TLS bypass

---

## 62. Fail Securely

When security validation fails, the application should fail securely.

Do not default to:

- Allow
- Authenticated
- Authorized
- Trusted

when validation cannot be completed.

---

## 63. Error Handling and Information Disclosure

Error responses must not reveal information useful to attackers.

Avoid exposing:

- Database schema
- Internal service names
- File paths
- Stack traces
- Dependency versions
- Authentication mechanisms
- Internal network details

---

## 64. Error Handling and API Contracts

Error handling must comply with the API specification.

Review:

- Status codes
- Error schemas
- Headers
- Content type
- Error codes

---

## 65. Error Handling and Client Expectations

Clients should receive predictable error responses.

Do not return different structures for similar failure types unless the API contract explicitly defines them.

---

## 66. Error Handling and Observability

A useful error should answer:

- What failed?
- Where did it fail?
- Which operation failed?
- Which external system was involved?
- Which request or transaction was affected?
- Can it be retried?
- Is intervention required?

Do this without logging sensitive data.

---

## 67. Error Handling and Performance

Error handling should not create excessive overhead.

Avoid:

- Repeated serialization
- Large payload logging
- Repeated retries
- Expensive transformations during failure processing

---

## 68. Error Handling and Logging Levels

Use appropriate log levels.

Typical guidance:

- `INFO` — expected operational events
- `WARN` — recoverable or unusual conditions
- `ERROR` — failed operations requiring attention
- `DEBUG` — diagnostic detail

Do not classify expected validation failures as system errors unless operational requirements justify it.

---

## 69. Error Handling Checklist

Before completing the error-handling review, confirm:

- Errors are intentionally classified.
- Specific errors are handled where appropriate.
- Broad error handlers have a clear purpose.
- `On Error Continue` is justified.
- `On Error Propagate` is used where required.
- Errors are not silently swallowed.
- Error mappings are intentional.
- API status codes are appropriate.
- Error responses follow the contract.
- Sensitive details are not exposed.
- Stack traces are not returned to consumers.
- Correlation IDs are preserved or generated appropriately.
- Error messages are useful and safe.
- Retryable and non-retryable errors are distinguished.
- Retry counts are bounded.
- Retry storms are avoided.
- Idempotency is considered.
- Transaction behavior is correct.
- Partial failures are considered.
- Messaging redelivery is bounded.
- Poison messages are handled.
- Duplicate processing is considered.
- Cleanup occurs where necessary.
- Parallel and asynchronous failures are observable.
- Scheduled-job failures are observable.
- Security failures fail securely.
- Success responses are not returned after failed operations.
- Fallback behavior is intentional.
- Error handling is testable.

---

## 70. Error Handling Quality Gate

The reviewer must be able to answer the following questions:

1. Will important failures remain visible?
2. Are errors handled at the correct scope?
3. Are specific errors distinguished from unexpected failures?
4. Can any handler accidentally hide an error?
5. Are client errors distinguished from server errors?
6. Are downstream failures mapped appropriately?
7. Are retryable errors distinguished from non-retryable errors?
8. Can retries create duplicate business operations?
9. Are retry limits bounded?
10. Are partial failures handled?
11. Are message redelivery and poison messages handled?
12. Are error responses consistent with the API contract?
13. Are sensitive implementation details protected?
14. Can operators diagnose failures using safe logs and correlation IDs?
15. Do asynchronous and scheduled failures remain observable?
16. Does the application fail securely when security validation fails?

### Final Question

> When something goes wrong, does the application fail safely, preserve the failure, provide the right response, avoid duplicate or inconsistent processing, and give operators enough safe information to diagnose and recover from the problem?