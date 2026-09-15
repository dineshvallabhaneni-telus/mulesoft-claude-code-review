# MuleSoft Connector Analysis Skill

## Purpose

Perform a comprehensive analysis of every MuleSoft connector and external-system integration used by the application.

Review the application as a:

- Senior MuleSoft Architect
- Senior Integration Architect
- Senior Technical Lead

The objective is to determine whether connectors are:

- Correctly configured
- Securely configured
- Reusable
- Consistent
- Resilient
- Performant
- Properly scoped
- Appropriately timeout-configured
- Appropriately retry-configured
- Using global configurations where appropriate
- Free from unnecessary duplicate configurations

Review every connector used by the application.

Every meaningful finding MUST include:

- Evidence
- Impact
- Recommendation
- Practical solution

Do not report a problem without providing a solution.

Do not report connector usage itself as a problem.

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

# 3. Mandatory Files and Locations

At minimum inspect:

- pom.xml
- mule-artifact.json
- src/main/mule/**
- src/main/resources/**
- src/main/java/**
- src/main/python/**
- src/test/**

Review all Mule XML files and configuration resources that can affect connector behavior.

---

# 4. Connector Discovery

Identify every connector/module used.

Examples include:

- HTTP
- HTTP Listener
- Database
- SFTP
- FTP
- File
- Salesforce
- SAP
- JMS
- Kafka
- VM
- Object Store
- Email
- Web Service Consumer
- SOAP
- Validation
- Batch
- AI-related connectors
- AWS connectors
- Azure connectors
- Google connectors
- Workday
- ServiceNow
- Any other MuleSoft-supported connector

Do not assume the application only uses common connectors.

Discover connectors from the actual project.

---

# 5. Connector Inventory

Build an internal inventory containing:

| Connector | File | Flow | Operation | Global Config | Timeout | Retry | Pooling | TLS/Auth | Assessment |
|---|---|---|---|---|---|---|---|---|---|

Every connector instance should be accounted for.

---

# 6. Connector Version

Review connector/module versions from:

- pom.xml
- Maven dependencies
- Mule plugin configuration
- Exchange dependencies

Identify:

- Very old versions
- Inconsistent versions
- Multiple versions of the same module
- Version conflicts

Do not claim a version is vulnerable solely because it is old.

If vulnerability information cannot be established from repository evidence, report:

Verification Required

---

# 7. Global Configuration Requirement

Determine whether each connector that supports reusable global configuration appropriately uses one.

Examples:

- HTTP Request Config
- HTTP Listener Config
- Database Config
- SFTP Config
- Salesforce Config

Do not require a global configuration when:

- The connector does not support it meaningfully.
- The configuration is intentionally local.
- A one-off configuration is clearly justified.

---

# 8. Missing Global Configuration

Report connector configurations that are repeatedly defined inline when a shared global configuration would materially improve:

- Reuse
- Consistency
- Maintainability
- Security
- Timeout management
- Connection management

Provide the exact recommended structure.

---

# 9. Duplicate Global Configurations

Identify duplicate or near-duplicate global configurations.

Compare:

- Host
- Port
- Database
- Username reference
- TLS
- Authentication
- Timeout
- Pool settings
- Reconnection
- Proxy settings

Do not merge configurations that intentionally represent different systems or environments.

---

# 10. Duplicate Connector Instances

Identify repeated connector instances using equivalent configurations.

Examples:

Multiple HTTP Request operations using the same:

- Base URL
- Authentication
- TLS
- Timeout

Determine whether the global configuration can be reused.

---

# 11. Configuration Drift

Identify logically equivalent connectors with inconsistent:

- Timeout
- Response timeout
- Connection timeout
- Retry
- Reconnection
- Pool size
- TLS
- Authentication
- Proxy configuration

Report only when the difference creates meaningful operational risk.

---

# 12. HTTP Connector Review

For HTTP Request operations review:

- Request configuration
- Listener configuration
- Base path
- Host
- Port
- TLS
- Authentication
- Response timeout
- Connection timeout
- Reconnection
- Retry
- Headers
- Query parameters
- Streaming
- Follow redirects
- Compression where applicable

Do not report every default value as missing.

---

# 13. HTTP Timeout

Determine whether HTTP timeout settings are appropriate for the operation.

Review:

- Connection timeout
- Response timeout
- Request timeout where applicable

Avoid recommending arbitrary values.

Consider:

- Downstream system behavior
- Expected response time
- Business SLA
- Payload size
- Retry strategy

If the correct value cannot be determined from source, state:

"Timeout value should be validated against downstream SLA."

---

# 14. HTTP Retry

Review retry behavior.

Determine whether retries are appropriate for:

- Transient network errors
- 5xx responses
- Timeouts
- Connection failures

Do not recommend retrying every error.

Pay special attention to non-idempotent operations such as POST.

---

# 15. HTTP Retry Safety

For retryable operations determine whether repeated execution can cause duplicate business effects.

Consider:

- Idempotency key
- PUT vs POST
- Duplicate transaction prevention
- Downstream idempotency support

Do not claim retries are unsafe without evidence.

---

# 16. HTTP Connection Management

Review connection settings where visible.

Look for:

- Connection timeout
- Idle timeout
- Pooling
- Maximum connections
- Reconnection

Do not recommend aggressive connection pooling without considering downstream capacity.

---

# 17. HTTP Authentication

Review authentication configuration.

Identify:

- Basic authentication
- OAuth
- Client credentials
- API key
- Custom headers
- Other authentication mechanisms

Do not report the authentication mechanism itself as a defect.

Detailed API security belongs to api-security-analysis.

---

# 18. HTTP TLS

Review HTTPS/TLS usage.

Determine whether:

- Sensitive traffic uses TLS
- TLS configuration is centralized
- Certificates are managed appropriately
- Weak or obsolete protocols are explicitly configured

Do not claim a TLS version is insecure without evidence.

---

# 19. Database Connector Review

For database connectors review:

- Global DB configuration
- Connection URL
- Driver
- Authentication
- TLS
- Connection timeout
- Query timeout
- Pool configuration
- Reconnection
- Transaction configuration

Do not expose credentials in findings.

---

# 20. Database Connection Pooling

Where pooling is configurable, assess:

- Maximum pool size
- Minimum pool size
- Idle behavior
- Connection lifetime
- Validation

Do not recommend a fixed pool size without workload evidence.

Instead provide:

"Validate pool size against expected concurrency and database connection capacity."

---

# 21. Database Timeout

Review:

- Connection timeout
- Query timeout
- Transaction timeout where applicable

Determine whether timeout configuration is explicit where operationally important.

---

# 22. Database Retry

Review retry/reconnection behavior.

Avoid blindly retrying writes.

Consider:

- Transaction safety
- Idempotency
- Database locking
- Connection failures

---

# 23. Database Query Usage

Review connector operations for:

- Parameterized queries
- Dynamic SQL
- Large result sets
- Pagination
- Streaming
- Excessive repeated queries

Detailed performance analysis belongs to performance-analysis.

---

# 24. SFTP/FTP Connector Review

Review:

- Global configuration
- Host
- Port
- Authentication
- TLS where applicable
- Connection timeout
- Response timeout
- Reconnection
- Retry
- File handling
- Archive behavior
- Error handling

---

# 25. SFTP Authentication

Prefer secure authentication mechanisms where supported.

Review:

- SSH key configuration
- Password references
- Secure properties
- Host key validation

Never reproduce private keys or passwords.

---

# 26. File Connector Review

Review:

- File paths
- Streaming
- Locking
- Read/write behavior
- File naming
- Archive/error handling
- Polling configuration
- Move/delete behavior

Identify hard-coded environment-specific paths.

---

# 27. Messaging Connector Review

For JMS/Kafka/VM and similar connectors review:

- Global configuration
- Connection settings
- Retry
- Reconnection
- Acknowledgement
- Transaction handling
- Consumer configuration
- Concurrency
- Timeout

Do not recommend generic settings without considering delivery semantics.

---

# 28. Kafka Review

Where Kafka is used, review where visible:

- Bootstrap servers
- Security protocol
- Authentication
- TLS
- Consumer groups
- Acknowledgement
- Retry
- Offset handling
- Consumer concurrency
- Producer configuration

Do not claim Kafka reliability without infrastructure evidence.

---

# 29. Salesforce Review

Where Salesforce is used, review:

- Global configuration
- Authentication
- Connection management
- Timeout
- Reconnection
- Bulk API usage where appropriate
- Pagination
- Query design
- Error handling

Do not recommend Bulk API merely because it exists.

Consider workload characteristics.

---

# 30. SOAP/Web Service Review

Where SOAP/Web Service Consumer is used, review:

- WSDL
- Endpoint
- Authentication
- TLS
- Timeout
- Reconnection
- Retry
- Error handling
- Request/response transformation

---

# 31. Object Store Review

Review:

- Global configuration
- Persistence
- TTL
- Entry limits
- Serialization
- Error handling
- Key naming

Determine whether Object Store is appropriate for the use case.

Do not report usage as a defect by itself.

---

# 32. Connector Authentication

For every connector identify the authentication mechanism.

Determine whether credentials are:

- Externalized
- Securely referenced
- Hard-coded
- Stored in plain text

Detailed password/security findings belong to security-analysis.

---

# 33. Secure Property Integration

Determine whether connector secrets are obtained through secure configuration.

Look for:

- Secure properties
- `${secure::...}`
- Environment variables
- Secret references
- External secret-management integrations

Never reproduce secret values.

---

# 34. Hard-Coded Credentials

Report:

- Passwords
- API keys
- Client secrets
- Tokens
- Private keys

when embedded in connector configuration.

Coordinate detailed remediation with security-analysis.

---

# 35. TLS Configuration Reuse

Identify repeated TLS configurations.

Determine whether a shared TLS context would improve:

- Security
- Maintainability
- Certificate management

Do not merge intentionally different trust/key stores.

---

# 36. Reconnection Strategy

Review connector reconnection settings.

Determine whether reconnection is appropriate for:

- Network failures
- Temporary service unavailability
- Connection loss

Do not add retries/reconnection to every connector automatically.

---

# 37. Reconnection vs Retry

Distinguish:

Reconnection:

Restoring the underlying connection.

Retry:

Repeating an operation.

Do not treat them as interchangeable.

---

# 38. Retry Strategy

For retry-enabled connectors review:

- Maximum attempts
- Delay
- Backoff
- Error types
- Idempotency
- Maximum retry duration

Avoid infinite retry patterns unless explicitly justified.

---

# 39. Retry Storm Risk

Identify configurations that could generate excessive downstream traffic.

Examples:

- High concurrency
- Multiple retries
- Short retry intervals
- Multiple application instances

Provide a practical mitigation.

---

# 40. Timeout and Retry Interaction

Review whether:

timeout × retry count

could create unacceptable end-to-end latency.

Consider:

- API SLA
- Thread usage
- Connection pool consumption
- User-facing timeout
- Downstream capacity

Coordinate detailed performance findings with performance-analysis.

---

# 41. Connection Pool Exhaustion

Look for potential pool exhaustion caused by:

- Large concurrency
- Long timeouts
- Long transactions
- Slow downstream systems
- Excessive pool sizes
- Connections not being released correctly

Do not claim exhaustion without evidence.

Use:

Potential Risk

when appropriate.

---

# 42. Connector Concurrency

Review connector concurrency settings.

Determine whether concurrency is aligned with:

- Downstream capacity
- Pool size
- API limits
- Database capacity
- Message broker capacity

Do not maximize concurrency automatically.

---

# 43. Rate Limits

Where connector/service configuration exposes rate limits, determine whether the application appears to account for them.

Examples:

- Salesforce limits
- API throttling
- Messaging limits

If limits are external and not visible, state:

"External service rate limits should be validated."

---

# 44. Connector Error Handling

Review connector operations for appropriate handling of:

- Connection failures
- Authentication failures
- Timeouts
- Invalid responses
- Rate limiting
- Server errors
- Client errors

Do not handle every connector error identically.

---

# 45. Response Validation

For external integrations determine whether important responses are validated before downstream processing.

Examples:

- HTTP status
- Required response fields
- Expected business status

---

# 46. Request Validation

Determine whether connector requests are validated before invocation.

Examples:

- Required identifier
- Required payload
- Valid endpoint parameter
- Valid query parameter

Do not duplicate API-layer validation unnecessarily.

---

# 47. Connector Streaming

Determine whether streaming is appropriate for:

- Large files
- Large HTTP payloads
- Database results

Do not recommend streaming universally.

---

# 48. Large Payload Handling

Review connector operations involving large payloads.

Consider:

- Streaming
- Memory consumption
- Repeated transformations
- Logging
- Network timeouts

Coordinate detailed performance findings with performance-analysis.

---

# 49. Connector Transactions

Where supported, review transaction configuration.

Determine whether:

- Transaction scope is appropriate
- Transaction is unnecessarily broad
- External side effects are mixed with transactional operations

Use:

Verification Required

when business transaction semantics are unclear.

---

# 50. Connector Naming

Global configurations should have descriptive names.

Prefer:

customerDatabaseConfig

over:

dbConfig1

Avoid duplicate numbering when names can describe purpose.

---

# 51. Connector Configuration Naming

Review names for:

- HTTP request configs
- Listener configs
- DB configs
- SFTP configs
- Messaging configs
- TLS contexts

Names should communicate system/purpose.

---

# 52. Connector Endpoint Externalization

Review whether environment-dependent values are externalized:

- Host
- Port
- Base path
- Queue/topic
- Database URL
- File path

Do not externalize values that are true static constants without benefit.

---

# 53. Environment Consistency

Compare connector configuration across:

- DEV
- QA
- UAT
- PROD

Check that configuration structure remains consistent while environment-specific values change appropriately.

Do not report expected environment-specific differences.

---

# 54. Connector Configuration Drift

Report when logically equivalent connector configurations differ unexpectedly across environments.

Examples:

DEV:

timeout = 30s

PROD:

timeout = 5s

if no business reason is evident.

Use:

Verification Required

when environment intent is unclear.

---

# 55. Connector Usage Patterns

Identify connectors being used inefficiently.

Examples:

- Repeated lookup
- Repeated authentication
- Repeated connection setup
- Unnecessary external call
- Calling connector inside a large loop
- Downloading entire payload when streaming is possible

Coordinate with performance-analysis.

---

# 56. Connector Calls Inside Loops

Identify external connector calls inside:

- For Each
- Parallel For Each
- Batch
- Repeatable operations

Determine whether:

- The call is necessary
- Calls can be batched
- Results can be cached
- The connector supports bulk operations

Do not report merely because a connector is inside a loop.

---

# 57. Connector Calls Inside Parallel Processing

Review whether parallel connector calls can overwhelm:

- Database
- API
- Message broker
- Connection pool
- Rate limits

Provide a practical concurrency strategy.

---

# 58. Connector and Caching

Identify repeated read-only external calls where caching could materially improve performance.

Do not recommend caching when:

- Data changes frequently
- Staleness is unacceptable
- Cache invalidation is unsafe

---

# 59. Custom Code Around Connectors

Identify Java/Python/custom code that performs work already supported by:

- MuleSoft connector
- DataWeave
- Mule processor
- Standard module

For each candidate determine:

- Current custom behavior
- Built-in alternative
- Migration complexity
- Functional limitations

Do not recommend replacement when the custom implementation provides required functionality unavailable in MuleSoft.

---

# 60. Connector Security Boundary

Identify connector configurations that could affect security:

- TLS
- Authentication
- Authorization
- Credentials
- Trust stores
- Key stores

Detailed security findings belong to security-analysis.

---

# 61. Connector/API Security Boundary

For API-facing connectors determine whether authentication/security configuration is appropriate.

Detailed API security findings belong to api-security-analysis.

Do not duplicate the entire finding.

---

# 62. Connector Logging

Determine whether connector failures can be diagnosed through application logging.

Review:

- Operation
- Target system
- Correlation ID
- Error information
- Duration where appropriate

Detailed logging findings belong to logging-analysis.

---

# 63. Connector Timeout Recommendations

Do not provide arbitrary universal values such as:

"Set every timeout to 30 seconds."

Instead explain the basis:

- Downstream SLA
- Typical latency
- Maximum expected processing time
- Retry count
- User-facing SLA

---

# 64. Connector Pooling Recommendations

Do not provide arbitrary universal pool sizes.

Use:

"Validate maximum pool size against expected concurrency, application worker count, downstream connection limits, and database/API capacity."

Where source evidence shows obvious misconfiguration, provide a specific recommendation.

---

# 65. Connector Retry Recommendations

Every retry recommendation must consider:

- Error type
- Idempotency
- Retry count
- Backoff
- Downstream limits
- Total execution time

Do not recommend retries for permanent business errors.

---

# 66. Connector Finding Format

Every finding MUST contain:

## Finding ID

Example:

MULE-CONN-001

## Title

Concise connector issue.

## Severity

High / Medium / Low / Warning

## Category

Connector

## Connector

Connector/module name.

## Location

File, flow, processor, and configuration.

## Evidence

Observed implementation.

## Impact

Technical, operational, security, reliability, or performance impact.

## Recommendation

What should change.

## Solution

Concrete MuleSoft implementation guidance.

## Priority

Immediate / Short Term / Medium Term / Long Term

---

# 67. Severity Guidelines

## High

Connector configuration creates significant risk of:

- Production outage
- Data loss
- Security exposure
- Severe integration failure
- Major reliability problem

## Medium

Meaningful reliability, maintainability, performance, or operational issue.

## Low

Minor improvement.

## Warning

Potential issue requiring environment/business verification.

Do not inflate severity.

---

# 68. Positive Connector Observations

Identify good practices such as:

- Global configurations
- Reusable connector configs
- Secure authentication
- Appropriate TLS
- Sensible timeouts
- Appropriate retry policies
- Proper reconnection
- Correct pooling
- Externalized endpoints
- Good error handling
- Bulk operations where appropriate
- Streaming where appropriate

---

# 69. Cross-Skill Boundaries

Detailed findings owned by these skills should not be duplicated unnecessarily:

- mulesoft-architecture
- mule-code-quality
- api-security-analysis
- security-analysis
- performance-analysis
- munit-analysis
- configuration-analysis
- logging-analysis
- duplication-analysis
- word-report-generation

This skill owns connector-specific correctness and integration configuration.

If a connector exposes a password:

- connector-analysis identifies the connector issue.
- security-analysis owns the detailed credential-security finding.

If connector configuration causes performance concerns:

- connector-analysis identifies the connector configuration.
- performance-analysis owns the detailed performance assessment.

If duplicate connector configurations exist:

- connector-analysis identifies the configuration issue.
- duplication-analysis may consolidate the duplication finding.

The final report reviewer must consolidate duplicate root causes.

---

# 70. No Unsupported Claims

Never claim:

- A timeout is incorrect without context.
- A pool size is incorrect without workload evidence.
- A retry is safe without considering idempotency.
- A connector is insecure merely because it uses a particular authentication method.
- A connector version is vulnerable without vulnerability evidence.
- A configuration is unnecessary without understanding its purpose.

Use:

Verification Required

where appropriate.

---

# 71. Connector Score

Provide a connector-quality score based on:

- Configuration quality
- Global configuration reuse
- Security
- Timeout strategy
- Retry/reconnection
- Pooling
- Error handling
- Environment consistency
- Performance considerations
- Maintainability

Do not calculate the score solely from finding count.

---

# 72. Final Output

Return structured connector analysis containing:

## Connector Summary

## Connector Inventory

## Global Configuration Assessment

## Duplicate Configuration Assessment

## HTTP Connector Assessment

## Database Connector Assessment

## File/SFTP/FTP Assessment

## Messaging Assessment

## SaaS Connector Assessment

## TLS Assessment

## Authentication Assessment

## Timeout Assessment

## Retry Assessment

## Reconnection Assessment

## Pooling Assessment

## Concurrency Assessment

## Streaming Assessment

## Transaction Assessment

## Custom Connector-Related Code Assessment

## Environment Consistency Assessment

## Connector Findings

## Recommended Connector Improvements

## Positive Connector Practices

## Verification Required

## Connector Score

Do not generate the final Word document from this skill.

The word-report-generation skill is responsible for creating the final .docx.

---

# 73. Quality Standard

Before completing the review, ask:

"Would a Senior MuleSoft Architect trust these connector configurations in a production integration environment?"

If not:

- Identify the exact connector and configuration.
- Explain the actual risk.
- Avoid generic connector recommendations.
- Consider timeout, retry, pooling, concurrency, and downstream capacity together.
- Consider security and idempotency.
- Provide a practical MuleSoft solution.
- Distinguish source-level evidence from infrastructure-level verification.

The objective is production-quality connector analysis, not a generic connector checklist.