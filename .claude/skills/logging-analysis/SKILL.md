# MuleSoft Logging Analysis Skill

## Purpose

Perform a comprehensive logging review of the MuleSoft application.

Review the application as a:

- Senior MuleSoft Architect
- Senior Technical Lead
- Production Operations Architect

The objective is to determine whether application logging is sufficient to:

- Trace application flow
- Diagnose failures
- Correlate requests across systems
- Troubleshoot production issues
- Monitor important business processing
- Identify integration failures
- Support operational support teams

The review must focus on useful, actionable logging.

Do NOT recommend logging every processor or every variable.

Do NOT report a problem without providing a practical solution.

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

- Review agents
- Skills
- Prompt files
- Framework scripts
- Generated reports

---

# 3. Logging Discovery

Identify all logging implementations.

Search for:

- Logger processors
- Logger scopes
- Mule logger configuration
- Log levels
- Structured logging
- Correlation IDs
- Request IDs
- Transaction IDs
- Business identifiers
- Error logging
- Exception logging
- Logging inside error handlers

Review all Mule XML configuration files.

Also review logging implemented through:

- DataWeave
- Java
- Custom code
- Other supported components

---

# 4. Logging Inventory

Build an internal inventory:

| File | Flow | Logger | Level | Purpose | Useful Context | Sensitive Data Risk | Assessment |
|---|---|---|---|---|---|---|---|

Identify:

- INFO
- DEBUG
- TRACE
- WARN
- ERROR

Do not treat the use of a particular level as automatically correct or incorrect.

---

# 5. Application Flow Traceability

Determine whether logs allow an operator to understand the major application journey.

For important flows, look for enough information to identify:

1. Request received
2. Important processing started
3. Important external integration invoked
4. Important processing completed
5. Error occurred
6. Processing failed or completed

Do not require a logger for every step.

Focus on meaningful application boundaries.

---

# 6. Flow Entry Logging

For important application entry points, determine whether sufficient information exists to establish:

- Which flow was invoked
- Request/correlation identifier
- Relevant business identifier
- Operation being performed

Do not log complete payloads by default.

---

# 7. Flow Completion Logging

For important processing flows, determine whether successful completion can be identified.

Useful information may include:

- Flow name
- Operation
- Correlation ID
- Business identifier
- Processing result
- Duration where appropriate

Do not recommend redundant completion logs for trivial flows.

---

# 8. External Integration Logging

For important external calls, determine whether logging provides enough information to troubleshoot integration problems.

Useful information may include:

- Target system
- Operation
- Endpoint identifier without exposing secrets
- Correlation ID
- Request/response status
- Duration
- Result

Do not log authentication headers or credentials.

---

# 9. Integration Failure Logging

Determine whether important connector failures are logged with sufficient context.

Examples:

- HTTP failure
- Database failure
- SFTP failure
- Messaging failure
- Salesforce failure

The log should help identify:

- What operation failed
- Which system was involved
- Which request/transaction was affected
- What error occurred

---

# 10. Error Handler Logging

Review:

- On Error Continue
- On Error Propagate
- Try scopes
- Global error handlers
- Flow-level error handlers

Determine whether meaningful errors are logged.

An error should generally contain enough information to diagnose the problem without exposing sensitive information.

---

# 11. Error Context

Evaluate whether ERROR logs provide useful context such as:

- Error type
- Error description
- Flow
- Correlation ID
- Business identifier
- Operation
- External system
- Relevant non-sensitive context

Avoid recommending only:

"An error occurred."

---

# 12. Stack Trace

Determine whether technical exceptions retain sufficient diagnostic information.

Do not require stack traces to be manually logged everywhere.

Avoid duplicate stack traces.

If Mule/runtime logging already provides sufficient exception information, do not report duplicate logging.

---

# 13. Error Duplication

Identify situations where the same error may be logged multiple times.

Examples:

- Child flow logs ERROR
- Parent flow logs same ERROR
- Global error handler logs same ERROR

Avoid reporting legitimate layered logging.

Only report duplication when it creates excessive or confusing logs.

---

# 14. WARN Usage

Review WARN logs.

Determine whether WARN represents an actionable abnormal condition.

Examples:

- Retry occurring
- Fallback triggered
- Optional data missing
- Degraded dependency

Do not use WARN for normal processing.

---

# 15. INFO Usage

INFO should generally represent important operational events.

Examples:

- Application processing started
- Important integration completed
- Business transaction completed
- Significant state transition

Avoid excessive INFO logging for high-frequency technical details.

---

# 16. DEBUG Usage

DEBUG may contain detailed diagnostic information.

Review whether:

- Debug information is unnecessarily logged at INFO
- Sensitive information is exposed
- Large payloads are logged
- High-frequency debug statements could create operational noise

Do not recommend removing useful DEBUG logging solely because it exists.

---

# 17. TRACE Usage

Review TRACE logging where present.

TRACE should generally be reserved for very detailed diagnostics.

Identify inappropriate high-volume TRACE logging if it is enabled in production configuration.

---

# 18. Sensitive Data Logging

Check whether logs contain:

- Passwords
- API keys
- Tokens
- Authorization headers
- Client secrets
- Private keys
- Sensitive personal data
- Financial information
- Security credentials

Never reproduce actual sensitive values in the review.

Use:

[REDACTED]

---

# 19. Payload Logging

Identify complete payload logging.

Examples:

logger message:

#[payload]

or equivalent.

Determine whether the payload may contain sensitive or large data.

Do not report payload logging automatically.

Consider:

- Payload sensitivity
- Payload size
- Frequency
- Operational value

---

# 20. Large Payload Logging

Identify logging of potentially large:

- JSON
- XML
- Binary
- File content
- Arrays
- Objects

Evaluate the risk of:

- High log volume
- Performance degradation
- Storage consumption
- Sensitive data exposure

Provide a safer alternative.

---

# 21. Variable Logging

Identify log statements that print:

- Entire variables
- Collections
- Request objects
- Response objects

Determine whether logging is actually useful.

Avoid recommending removal if the variable is safe and operationally important.

---

# 22. Header Logging

Check whether HTTP headers are logged.

Pay particular attention to:

- Authorization
- Cookie
- Set-Cookie
- API keys
- Client secrets

These should not be logged.

---

# 23. Query Parameter Logging

Determine whether URLs/query parameters may contain sensitive values.

Examples:

- Token
- Password
- Account number
- Personal information

Recommend masking or excluding sensitive parameters.

---

# 24. Correlation ID

Determine whether application processing can be traced using a correlation identifier.

Look for:

- Mule correlation ID
- Request ID
- Trace ID
- Transaction ID
- Custom correlation ID

Do not require a custom correlation mechanism if Mule/runtime capabilities already provide sufficient correlation.

---

# 25. Correlation Propagation

For distributed integrations, determine whether correlation information is propagated where appropriate.

Examples:

API A

to:

Mule Application

to:

External API

to:

Another Mule Application

Look for:

- Headers
- Message attributes
- Correlation IDs

Do not require propagation to systems that cannot support it.

---

# 26. Business Identifiers

For business-critical flows, determine whether logs can identify the affected business transaction.

Examples:

- Customer ID
- Order ID
- Transaction ID
- Case ID
- File ID

Only recommend identifiers that are safe to log.

---

# 27. Business Identifier Security

Business identifiers should not expose sensitive personal information unnecessarily.

Where an identifier itself is sensitive, recommend:

- Masking
- Hashing where appropriate
- Tokenized identifier
- Internal reference ID

Do not recommend hashing merely for aesthetic reasons.

---

# 28. Logging Consistency

Compare logging patterns across flows.

Look for:

- Different correlation strategies
- Different message formats
- Inconsistent levels
- Inconsistent terminology
- Inconsistent error logging

Report meaningful inconsistencies.

---

# 29. Logger Message Quality

Review logger messages for clarity.

Poor:

"Error happened"

Better:

"Customer lookup failed for operation=customerLookup"

Do not require a specific message format unless the application has an established standard.

---

# 30. Structured Logging

Determine whether structured logging would materially improve operations.

Potential fields:

- timestamp
- application
- environment
- flow
- operation
- correlationId
- transactionId
- businessId
- status
- duration
- errorType

Do not require JSON logging if the existing logging infrastructure does not support it.

Recommend structured logging where it would significantly improve searchability and observability.

---

# 31. Log Message Consistency

Look for inconsistent terminology.

Example:

"Customer ID"

"customerId"

"cust-id"

Recommend consistent terminology when logs are consumed by operational teams or log-search tools.

---

# 32. Processing Duration

For important integrations or long-running operations, determine whether duration can be measured.

Potential approach:

- Start timestamp
- End timestamp
- Duration

Do not add timing logs to every processor.

Prioritize:

- External API calls
- Database operations
- Batch processing
- Large transformations
- Long-running flows

---

# 33. Performance Impact of Logging

Identify logging that may negatively affect performance.

Examples:

- Large payload serialization
- High-frequency logging
- Logging inside loops
- Logging large collections
- Excessive DEBUG/TRACE operations

Provide practical alternatives.

---

# 34. Logging Inside Loops

Identify log statements inside:

- For Each
- Parallel For Each
- Batch processing
- Large collection processing

Determine whether log volume can become excessive.

Do not report every logger inside a loop as a defect.

---

# 35. Batch Logging

For batch processing, determine whether logs can identify:

- Batch execution
- Batch status
- Record processing status
- Errors
- Completion

Avoid logging every record unless operationally necessary.

---

# 36. Scheduler Logging

For scheduled flows, determine whether logs identify:

- Job start
- Job completion
- Job failure
- Number of records where useful
- Duration where useful

Avoid unnecessary scheduler noise.

---

# 37. File Processing Logging

For file-processing flows, useful context may include:

- File name
- File identifier
- Processing status
- Record count
- Failure reason
- Completion

Do not log file contents unless explicitly justified.

---

# 38. Messaging Logging

For messaging flows, determine whether logs provide enough context to identify:

- Message processing
- Message identifier
- Correlation ID
- Processing result
- Failure

Do not log sensitive message contents.

---

# 39. API Logging

For API flows, evaluate whether logs allow operators to determine:

- Operation
- Request correlation
- Response status
- Processing result
- Failure reason
- Duration where appropriate

Do not log complete request/response bodies by default.

---

# 40. Database Logging

For database interactions, avoid logging:

- Passwords
- Connection strings containing secrets
- Sensitive query parameters
- Full sensitive result sets

Useful information may include:

- Operation
- Table/business operation
- Duration
- Success/failure
- Correlation ID

Do not log full SQL statements if they expose sensitive values.

---

# 41. Retry Logging

Where retry logic exists, determine whether logs identify:

- Retry occurred
- Attempt number
- Maximum attempts
- Target operation
- Final result

Do not log every internal retry at ERROR.

---

# 42. Reconnection Logging

Where reconnect/reconnection behavior exists, determine whether operators can identify:

- Connection failure
- Reconnection attempt
- Successful reconnection
- Final failure

Avoid duplicate logs from connector/runtime logging.

---

# 43. Authentication Logging

Review authentication-related logging.

Do not log:

- Passwords
- Tokens
- Authorization headers
- Client secrets

Useful information may include:

- Authentication failure
- Authentication mechanism
- Request/correlation identifier
- Security event type

Detailed API security belongs to api-security-analysis.

---

# 44. Log Level Configuration

Determine whether log levels can be managed appropriately by environment.

Review:

- DEV
- QA
- UAT
- PROD

Avoid recommending DEBUG/TRACE in production without a controlled operational reason.

---

# 45. Production Logging

Assess whether production logging is likely to provide enough information for support without creating excessive noise.

Balance:

Diagnostic value

against:

- Performance
- Storage
- Security
- Noise

---

# 46. Logging Configuration

Review relevant logging configuration files.

Look for:

- Log levels
- Appenders
- Patterns
- Rolling policies where visible
- Environment-specific logging
- Sensitive information
- Duplicate configuration

Do not claim log retention is incorrect unless retention configuration is actually visible.

---

# 47. Log Rotation

If logging/rolling configuration is present, review:

- Maximum file size
- Rotation
- Retention
- Compression where applicable

If not visible in the repository, mark:

Verification Required

Do not invent infrastructure configuration.

---

# 48. Log Retention

Do not make unsupported claims about retention.

If retention is not controlled in the repository, state:

"Log retention could not be validated from repository source."

---

# 49. Logging Framework Configuration

Review logging configuration for:

- Excessive root logging
- Duplicate appenders
- Inconsistent levels
- Development settings carried into production
- Sensitive output

Do not recommend changes without understanding the current configuration.

---

# 50. Duplicate Loggers

Identify duplicate or redundant log statements.

Examples:

- Same event logged repeatedly
- Same payload logged at multiple levels
- Same error logged by multiple layers

Report only meaningful duplication.

---

# 51. Missing Operational Logs

Report missing logs only when the absence makes production troubleshooting materially difficult.

Examples:

- Important flow has no identifiable start/end
- External integration failure has no useful context
- Critical business transaction cannot be traced

Do not report:

"Every flow needs a logger."

---

# 52. Logging in Error Paths

Important error paths should generally provide enough diagnostic context.

Review:

- Choice error branches
- Error handlers
- Validation failures
- Connector failures
- Retry exhaustion

---

# 53. Logging and Exception Handling

Ensure exceptions are not silently swallowed without useful logging or an appropriate response.

Particularly inspect:

- On Error Continue
- Try scopes
- Suppressed errors
- Custom error handling

Do not require logging when an intentional error is fully handled and observability is provided elsewhere.

---

# 54. Logging and Custom Code

If Java/Python/custom code performs important processing, determine whether failures can be traced back to the relevant Mule flow.

Detailed custom-code analysis belongs to mule-code-quality and connector-analysis where applicable.

---

# 55. Logging and Duplicate Processing

If duplicate flow execution or duplicate connector calls are identified elsewhere, determine whether logs provide enough information to diagnose the behavior.

Do not duplicate the root-cause finding.

---

# 56. Logging Recommendations

Recommendations should be concrete.

Weak:

"Improve logging."

Strong:

"Add a single INFO log at the start of customer-order processing containing correlationId, orderId, and operation name. Add an ERROR log in the terminal error handler containing correlationId, flow name, errorType, and sanitized error description. Do not log the request payload."

---

# 57. Finding Format

Every finding MUST contain:

## Finding ID

Example:

MULE-LOG-001

## Title

Concise issue.

## Severity

High / Medium / Low / Warning

## Category

Logging

## Location

File and flow.

## Evidence

Observed implementation.

## Impact

Operational or technical impact.

## Recommendation

What should be improved.

## Solution

Concrete implementation guidance.

## Priority

Immediate / Short Term / Medium Term / Long Term

---

# 58. Severity Guidelines

## High

Logging deficiency creates significant inability to:

- Diagnose production failures
- Trace critical transactions
- Detect important security/operational events

or logging exposes highly sensitive information.

## Medium

Meaningful observability gap or excessive logging risk.

## Low

Minor logging improvement.

## Warning

Logging behavior cannot be fully validated statically.

Do not inflate severity.

---

# 59. Sensitive Information Findings

When sensitive data is found:

- Never reproduce the value.
- Identify the type of sensitive information.
- Identify the file/flow.
- Explain the risk.
- Recommend masking/removal.
- Coordinate detailed security remediation with security-analysis.

Example:

"Authorization header is logged in flow X."

Do not include the actual token.

---

# 60. Positive Logging Observations

Identify good practices such as:

- Effective correlation IDs
- Useful error context
- Appropriate log levels
- Sensitive data protection
- Clear operational messages
- Structured logging
- Good integration tracing
- Appropriate retry logging
- Useful business identifiers
- Controlled production verbosity

---

# 61. Cross-Skill Boundaries

Detailed findings owned by these skills should not be duplicated unnecessarily:

- mulesoft-architecture
- mule-code-quality
- connector-analysis
- api-security-analysis
- security-analysis
- performance-analysis
- munit-analysis
- configuration-analysis
- duplication-analysis

This skill owns application logging and operational observability.

If a logger exposes credentials:

- logging-analysis identifies the exposure.
- security-analysis owns the security severity/remediation.

If excessive payload logging creates performance problems:

- logging-analysis identifies the logging issue.
- performance-analysis owns the detailed performance impact.

If duplicate logger statements exist:

- logging-analysis identifies the logging duplication.
- duplication-analysis may consolidate duplicate-code observations.

The final report reviewer must consolidate duplicate root causes.

---

# 62. No Unsupported Claims

Never claim:

- Logs are retained for a specific period unless configuration/evidence confirms it.
- Logs are searchable unless infrastructure supports it.
- Logs are centralized unless configuration/evidence confirms it.
- A production log level is incorrect without environment evidence.
- A logger is useless solely because it appears simple.

Use:

Verification Required

where infrastructure behavior cannot be established from source.

---

# 63. Logging Score

Provide a logging quality score based on:

- Traceability
- Error visibility
- Correlation
- Sensitive data protection
- Log-level appropriateness
- Operational usefulness
- Consistency
- Performance impact
- Production suitability

Do not calculate the score solely from the number of log statements.

---

# 64. Final Output

Return structured logging analysis containing:

## Logging Summary

## Logger Inventory

## Flow Traceability Assessment

## Error Logging Assessment

## Integration Logging Assessment

## Correlation ID Assessment

## Business Identifier Assessment

## Sensitive Data Logging Assessment

## Payload Logging Assessment

## Log Level Assessment

## Structured Logging Assessment

## Performance Impact Assessment

## Logging Configuration Assessment

## Positive Logging Observations

## Logging Findings

## Recommended Logging Improvements

## Verification Required

## Logging Score

Do not generate the final Word document from this skill.

The word-report-generation skill is responsible for creating the final .docx.

---

# 65. Quality Standard

Before completing the review, ask:

"Would a production support team and Senior MuleSoft Architect have enough information from these logs to diagnose important application failures without being overwhelmed by noise or exposed to sensitive information?"

If not:

- Remove trivial findings.
- Re-check whether the missing log is genuinely operationally important.
- Avoid recommending logging everywhere.
- Avoid recommending complete payload logging.
- Protect sensitive information.
- Provide concrete logger recommendations.
- Distinguish source-level findings from infrastructure-level verification.
- Prioritize critical flows and integrations.

The objective is production-quality logging analysis, not a generic logging checklist.