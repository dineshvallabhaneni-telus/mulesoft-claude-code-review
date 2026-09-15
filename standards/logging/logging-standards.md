# File: standards/logging/logging-standards.md

# MuleSoft Logging Standards

## 1. Purpose

This document defines standards for reviewing logging in MuleSoft applications.

The review must determine whether logging is:

- Useful
- Consistent
- Secure
- Operationally relevant
- Sufficient for troubleshooting
- Appropriate for the configured environment
- Free from unnecessary sensitive-data exposure
- Appropriate for the expected application volume

Logging should support observability without becoming a security, performance, or maintenance problem.

---

## 2. General Principles

Logging should provide enough information to understand:

- What happened
- Where it happened
- When it happened
- Which operation was involved
- Whether the operation succeeded or failed
- Which request or transaction was affected

Logs should not expose sensitive information.

Prefer meaningful operational events over excessive diagnostic output.

---

## 3. Log Levels

Use log levels consistently.

Typical guidance:

- `ERROR` — operation failed and requires attention
- `WARN` — unusual or potentially problematic condition
- `INFO` — important normal operational event
- `DEBUG` — detailed diagnostic information
- `TRACE` — highly detailed diagnostic information, where supported

Do not use `ERROR` for expected business validation failures unless operational requirements justify it.

---

## 4. ERROR Logging

Use `ERROR` when a failure prevents an expected operation from completing and requires investigation or operational attention.

Examples:

- Database unavailable
- Critical downstream service failure
- Unexpected transformation failure
- Unhandled application error

Avoid logging the same failure repeatedly at `ERROR` across multiple layers.

---

## 5. WARN Logging

Use `WARN` for conditions that are not necessarily failures but may require attention.

Examples:

- Retry occurring
- Deprecated configuration detected
- Recoverable downstream issue
- Unexpected but recoverable condition

Do not use `WARN` for every normal validation failure.

---

## 6. INFO Logging

Use `INFO` for significant operational events.

Examples:

- Application startup
- Application shutdown
- Important business process completion
- Scheduled job start/completion
- Major integration operation

Avoid logging every internal processing step at `INFO`.

---

## 7. DEBUG Logging

Use `DEBUG` for diagnostic information useful during troubleshooting.

Examples:

- Detailed transformation information
- Connector interaction details
- Internal decision paths
- Configuration diagnostics that do not contain secrets

Production should not normally depend on DEBUG logs for routine operations.

---

## 8. TRACE Logging

Use `TRACE` only where extremely detailed diagnostic information is required.

Because TRACE can generate significant log volume, ensure it is disabled or tightly controlled in normal production operation.

---

## 9. Sensitive Data

Never log sensitive data unnecessarily.

Potentially sensitive information includes:

- Passwords
- API keys
- Access tokens
- Refresh tokens
- Client secrets
- Authorization headers
- Private keys
- Session identifiers
- Financial information
- Personally identifiable information
- Authentication credentials

---

## 10. Authorization Headers

Do not log complete authorization headers.

Examples that must not be logged:

    Authorization: Bearer <token>

If diagnostic logging requires authentication information, use an approved masked representation.

---

## 11. Tokens

Do not log:

- JWTs
- OAuth tokens
- API tokens
- Refresh tokens
- Session tokens

A token must not be considered safe simply because it is logged at DEBUG level.

---

## 12. Passwords

Passwords must never be logged.

This applies to:

- Incoming requests
- Outgoing requests
- Connector configuration
- Database credentials
- Error messages
- Debug output

---

## 13. API Keys and Secrets

API keys, client secrets, encryption keys, and similar credentials must never be written to application logs.

If a value must be identified for troubleshooting, use a safe identifier or masked representation.

---

## 14. Personal Data

Avoid logging personal data unless there is a documented operational requirement.

Examples include:

- Full name
- Email address
- Phone number
- Address
- Government identifiers
- Customer identifiers
- Date of birth

Where logging is required, minimize the data and follow applicable organizational privacy requirements.

---

## 15. Financial Data

Avoid logging:

- Full credit card numbers
- Bank account numbers
- Payment credentials
- Security codes
- Sensitive transaction details

Use approved masked representations where operationally necessary.

---

## 16. Payload Logging

Do not log complete request or response payloads by default.

Full payload logging can:

- Expose sensitive information
- Increase log volume
- Increase storage requirements
- Reduce performance
- Make troubleshooting harder

Log only the fields needed for the operational purpose.

---

## 17. Payload Logging at DEBUG

Payload logging at DEBUG is not automatically safe.

Review whether DEBUG logging could accidentally expose sensitive data when enabled in production.

---

## 18. Masking

Sensitive values that genuinely need to appear in logs must be masked.

Examples:

    ****1234

    eyJ****abcd

Masking must be applied before the value is written to the log.

Do not log the complete value and rely on downstream log-processing tools to mask it.

---

## 19. Log Filtering

Sensitive data should ideally be prevented from reaching the logging statement.

Do not rely exclusively on external log filters to protect secrets.

---

## 20. Correlation IDs

Important requests should have a correlation identifier.

The correlation ID should allow related log entries to be associated with the same transaction or request.

---

## 21. Correlation ID Propagation

When an inbound request already contains an accepted correlation ID, preserve it according to the application's tracing standard.

When one does not exist, generate one where required.

---

## 22. Correlation ID in Errors

Error logs should include the relevant correlation ID where available.

API error responses should also expose the correlation ID when required by the API contract.

---

## 23. Consistent Context

Logs for the same operation should provide consistent contextual information.

Useful context may include:

- Correlation ID
- Flow name
- Operation name
- Application name
- Environment
- External system
- Business transaction identifier

Only include identifiers that are safe to log.

---

## 24. Business Identifiers

Business identifiers can be useful for troubleshooting.

Examples:

- Order ID
- Customer ID
- Transaction ID
- Request ID

Before logging them, verify that organizational privacy and security requirements permit their use.

---

## 25. Log Message Quality

Log messages should clearly describe the event.

Prefer:

    Customer order submission failed for transaction <safe-id>

over:

    Error occurred

---

## 26. Avoid Redundant Messages

Do not log the same event repeatedly at multiple layers unless each log provides distinct operational value.

For example, avoid:

    Connector logs error
    Flow logs same error
    Global handler logs same error
    API layer logs same error

This can create noisy logs and duplicate alerts.

---

## 27. Error Context

An error log should provide enough safe context to diagnose the failure.

Useful information may include:

- Operation
- Error type
- External system
- Correlation ID
- Safe business identifier
- Retry attempt
- Relevant status code

Do not include the full payload merely to provide context.

---

## 28. Exception Information

When appropriate, preserve the exception/error type and useful diagnostic information.

Do not replace a meaningful exception with an uninformative message such as:

    Something went wrong

---

## 29. Stack Traces

Stack traces can be valuable for unexpected failures.

However:

- Do not expose them to API consumers.
- Avoid logging them repeatedly.
- Ensure logs containing stack traces are appropriately protected.

---

## 30. Error Message Sanitization

External system error messages should be reviewed before being logged or returned.

They may contain:

- Credentials
- URLs
- SQL
- Internal paths
- Tokens
- Personal information

Do not blindly log downstream exception messages.

---

## 31. Logging HTTP Requests

When logging HTTP requests, avoid logging sensitive:

- Headers
- Authorization information
- Cookies
- Query parameters
- Payload fields

Log only what is required for troubleshooting.

---

## 32. Logging HTTP Responses

The same principle applies to HTTP responses.

Do not automatically log complete downstream responses.

Review whether the response may contain:

- Personal information
- Credentials
- Tokens
- Internal system details

---

## 33. Query Parameters

Be careful when logging URLs containing query parameters.

A URL may contain sensitive information such as:

    token
    api_key
    password
    session
    authorization

Do not log sensitive query parameters.

---

## 34. Database Logging

Avoid logging:

- Database passwords
- Connection strings containing credentials
- Full SQL containing sensitive values
- Complete query results

If SQL diagnostics are necessary, use safe parameter handling.

---

## 35. SQL Parameters

Be careful when logging SQL parameters.

Parameterized SQL does not make logging the parameter values safe.

Sensitive values should still be excluded or masked.

---

## 36. File Logging

Avoid logging complete file contents.

Review whether files may contain:

- Credentials
- Personal data
- Financial information
- Confidential business information

Log safe metadata where possible.

---

## 37. Messaging Logging

For messaging applications, avoid logging complete messages by default.

Useful metadata may include:

- Message ID
- Correlation ID
- Queue/topic name
- Processing result
- Retry count

Ensure message identifiers themselves are safe to log.

---

## 38. Batch Logging

Batch processing should avoid producing one excessive log entry per record unless operationally necessary.

For large batches, consider logging:

- Batch ID
- Total records
- Successful records
- Failed records
- Processing duration
- Summary information

---

## 39. Loop Logging

Avoid logging inside high-volume loops unless there is a clear operational requirement.

Excessive loop logging can significantly increase:

- Log volume
- Processing time
- Storage
- Cost

---

## 40. Performance Impact

Logging has runtime cost.

Review:

- Payload serialization
- String construction
- Large object conversion
- Repeated logging
- High-frequency DEBUG statements

Do not perform expensive transformations solely to generate a log message unless necessary.

---

## 41. Large Payloads

Avoid converting large payloads to strings simply for logging.

This can increase memory usage and processing time.

---

## 42. Logging in Production

Production logging should prioritize:

- Operational visibility
- Security
- Performance
- Troubleshooting

Avoid enabling verbose diagnostic logging indefinitely.

---

## 43. Environment-Specific Log Levels

Log levels may differ between environments.

A typical approach is:

- Development: DEBUG as appropriate
- Test: DEBUG/INFO as needed
- Production: INFO/WARN/ERROR according to operational requirements

The exact configuration should follow the organization's standards.

---

## 44. Production DEBUG

Production DEBUG logging should be intentionally controlled.

Do not assume DEBUG is harmless because it is not visible under the normal configuration.

A temporary DEBUG change should have an operational process and security review where required.

---

## 45. Startup Logging

Application startup logging should provide useful operational information without exposing secrets.

Useful examples:

- Application started
- Environment
- Version
- Important feature state

Do not log:

- Passwords
- Encryption keys
- Client secrets
- Full connection strings

---

## 46. Configuration Logging

Do not log complete configuration objects.

Configuration frequently contains sensitive values.

If configuration diagnostics are required, log safe metadata such as:

- Configuration source
- Environment
- Enabled feature name
- Presence/absence of required properties

Do not log the actual secret.

---

## 47. Connector Logging

Connector-specific debug logging should be reviewed for sensitive-data exposure.

Some connectors or libraries may produce detailed request/response information.

Do not assume connector-generated logs are automatically safe.

---

## 48. Third-Party Library Logging

Review logging generated by:

- Connectors
- HTTP clients
- Database drivers
- Messaging clients
- External libraries

Third-party logs can expose sensitive information even when application logging is implemented correctly.

---

## 49. Log Format

Logs should follow a consistent format.

Where supported, structured logging is preferred for operationally important applications.

Useful fields may include:

    timestamp
    level
    application
    environment
    correlationId
    operation
    message

---

## 50. Structured Logging

Structured logs should use consistent field names.

For example:

    correlationId

should not be inconsistently represented as:

    correlation_id
    correlationID
    requestCorrelation

unless different fields have intentionally different meanings.

---

## 51. Timestamp

Logs should include timestamps with sufficient precision for troubleshooting.

Time-zone handling should be consistent across the application and logging infrastructure.

---

## 52. Log Time Zones

A consistent time standard should be used.

UTC is commonly preferred for distributed systems, but the organization may define another standard.

The important requirement is consistency and unambiguous interpretation.

---

## 53. Log Ordering

Distributed systems can produce logs from multiple components.

Correlation IDs and timestamps should make it possible to reconstruct the relevant operation sequence.

---

## 54. Business Event Logging

Important business events may require explicit logs.

Examples:

- Order submitted
- Payment completed
- Customer created
- File processed
- Batch completed

Business event logging should not duplicate an authoritative event store when one already exists.

---

## 55. Audit Logging

Security- or compliance-sensitive events may require audit logging.

Examples:

- Authentication
- Authorization changes
- Privileged operations
- Sensitive configuration changes
- Important business actions

Audit logging requirements should follow organizational policy.

---

## 56. Audit vs Application Logs

Do not assume normal application logs are sufficient for formal audit requirements.

Audit records may require:

- Stronger retention
- Integrity controls
- Restricted access
- Additional metadata
- Dedicated storage

---

## 57. Authentication Logging

Authentication events should be logged according to security requirements.

Useful information may include:

- Success/failure
- Safe user or client identifier
- Timestamp
- Correlation ID
- Source information where appropriate

Never log authentication credentials.

---

## 58. Authorization Logging

Important authorization failures may require logging.

Do not log sensitive authorization tokens or complete security contexts.

---

## 59. Security Events

Security-relevant events should be distinguishable from normal application events where operationally useful.

Examples:

- Repeated authentication failures
- Unauthorized access attempt
- Invalid token
- Certificate validation failure
- Suspicious request pattern

---

## 60. Logging and Error Handling

Error handling and logging should work together.

When an error is handled:

- Log appropriate diagnostic information.
- Preserve the error when required.
- Avoid duplicate logging.
- Do not expose sensitive details.

Logging an error does not mean the error has been correctly handled.

---

## 61. Logging and Retry

Retry behavior should be observable.

Useful information may include:

- Operation
- Retry attempt
- Maximum retry count
- External system
- Correlation ID

Avoid generating excessive logs for every retry in high-volume systems.

---

## 62. Logging and Dead-Letter Processing

When a message is moved to a dead-letter destination, log enough information to identify:

- Message
- Processing operation
- Failure reason
- Correlation ID
- Destination

Do not log the complete message unless explicitly required and safe.

---

## 63. Logging and Scheduled Jobs

Scheduled jobs should log enough information to determine:

- Job started
- Job completed
- Duration
- Records processed
- Failures
- Correlation or execution ID

Avoid logging every record by default.

---

## 64. Logging and Async Processing

Asynchronous operations should retain sufficient correlation information to trace their execution back to the initiating request or business transaction where applicable.

---

## 65. Logging and Parallel Processing

Parallel processing should not produce ambiguous or misleading logs.

Include sufficient context to distinguish individual operations where necessary.

---

## 66. Logging and DataWeave

Do not use DataWeave merely to serialize large payloads for logging.

Review expressions such as:

    write(payload, "application/json")

when used solely for logging.

Ensure that serialization does not expose sensitive information or create unnecessary overhead.

---

## 67. Logging and Data Masking

Mask sensitive values before they reach the logger.

Do not rely on developers remembering to manually mask a value every time it is logged.

Where practical, establish reusable masking utilities or standardized patterns.

---

## 68. Log Injection

Do not allow untrusted input to manipulate log structure or create misleading log entries.

Review logging of:

- User-controlled strings
- Headers
- Query parameters
- File names
- External system responses

Use structured logging or appropriate sanitization where necessary.

---

## 69. Newline and Control Characters

Untrusted values containing newline or control characters can make logs misleading or difficult to parse.

Where relevant, sanitize or safely encode such values before logging.

---

## 70. Logging Configuration

Review logging configuration for:

- Log level
- Appenders
- Destinations
- Rotation
- Retention
- Formatting
- Sensitive-data controls

---

## 71. Log Rotation

Log files should not grow without bounds where file-based logging is used.

Review:

- Rotation
- Maximum size
- Retention
- Compression
- Disk usage

---

## 72. Log Retention

Retention should follow organizational, operational, security, and compliance requirements.

Do not retain sensitive logs indefinitely without justification.

---

## 73. Log Access

Logs may contain sensitive operational information.

Access should be appropriately restricted.

The application review should identify obvious patterns that could unnecessarily expose secrets or personal data.

---

## 74. Logging Failures

Logging itself should not cause the business operation to fail unless the architecture explicitly requires guaranteed logging.

Avoid designs where a secondary logging failure unintentionally breaks the primary business transaction.

---

## 75. Excessive Logging

Potential excessive-logging indicators include:

- Logging entire payloads repeatedly
- Logging inside large loops
- Logging the same error at multiple layers
- Logging every connector operation
- Logging large binary content
- Logging every retry
- Logging normal variable values unnecessarily

---

## 76. Missing Logging

Potential missing-logging indicators include:

- Important scheduled jobs with no completion/failure visibility
- Critical downstream failures with no diagnostic context
- Security failures with no operational visibility
- Asynchronous processing with no traceability
- Dead-letter processing with no useful context

---

## 77. Logging Consistency

Similar operations should use consistent log messages and fields.

This makes logs easier to:

- Search
- Aggregate
- Monitor
- Alert on
- Troubleshoot

---

## 78. Avoid Sensitive Debugging Workarounds

Do not add temporary logging of secrets or complete payloads simply to troubleshoot an issue.

If detailed diagnostic information is required, use safe masking and controlled logging.

---

## 79. Logging Checklist

Before completing the logging review, confirm:

- Appropriate log levels are used.
- ERROR is reserved for meaningful failures.
- WARN is used for recoverable or unusual conditions.
- INFO is used for important operational events.
- DEBUG does not expose sensitive information.
- TRACE is appropriately controlled.
- Passwords are never logged.
- Tokens are never logged.
- API keys are never logged.
- Client secrets are never logged.
- Private keys are never logged.
- Sensitive personal data is minimized.
- Financial information is protected.
- Complete payload logging is avoided.
- Authorization headers are protected.
- Sensitive query parameters are protected.
- Database credentials are protected.
- SQL logging is safe.
- File contents are not unnecessarily logged.
- Messaging payloads are not unnecessarily logged.
- Correlation IDs are available where appropriate.
- Business identifiers are logged only when safe.
- Error logs contain useful context.
- Stack traces are not exposed externally.
- Duplicate logging is minimized.
- High-volume loops do not generate excessive logs.
- Large payload serialization is avoided where unnecessary.
- Production DEBUG logging is controlled.
- Structured logging is consistent where used.
- Log timestamps are unambiguous.
- Log injection risks are considered.
- Log rotation and retention are appropriate.
- Security events are observable.
- Asynchronous operations remain traceable.
- Scheduled jobs remain observable.
- Retry behavior is observable.
- Dead-letter processing is observable.
- Logging failures do not unnecessarily break business processing.

---

## 80. Logging Quality Gate

The reviewer must be able to answer the following questions:

1. Can operators understand important application events from the logs?
2. Can a failed request be traced using a correlation ID?
3. Are important failures logged with useful context?
4. Are sensitive values protected?
5. Are payloads logged only when justified?
6. Are production log levels appropriate?
7. Could logging materially affect application performance?
8. Could logs expose personal, financial, or security-sensitive information?
9. Are errors logged without excessive duplication?
10. Are asynchronous and scheduled operations observable?
11. Are retries and dead-letter processing traceable?
12. Are security events sufficiently visible?
13. Are logs structured consistently where required?
14. Can logs be retained and managed safely?
15. Could untrusted input manipulate log content?

### Final Question

> Do the application's logs provide enough safe, consistent, and actionable information to operate and troubleshoot the system without exposing sensitive data or creating unnecessary performance and storage overhead?