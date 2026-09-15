# File: standards/connectors/connector-standards.md

# MuleSoft Connector Standards

## 1. Purpose

This document defines standards for reviewing MuleSoft connector usage.

The review must determine whether connectors are:

- Correctly configured
- Securely configured
- Appropriately used
- Efficiently used
- Resilient to failures
- Properly authenticated
- Properly monitored
- Consistent with the application's architecture
- Appropriate for the integration requirement

The review must focus on meaningful risks.

Do not report a connector configuration as a finding merely because an alternative configuration exists.

---

## 2. Connector Selection

The selected connector should be appropriate for the target system and integration requirement.

Review whether:

- The connector supports the required operation.
- The connector is officially supported.
- The connector version is appropriate.
- The implementation unnecessarily uses custom code where a suitable connector exists.
- The connector introduces unnecessary complexity.

Do not recommend replacing a connector without evidence of a functional, security, performance, or maintainability problem.

---

## 3. Connector Configuration Reuse

Where appropriate, shared connector configurations should be defined as global configurations.

Examples include:

- HTTP Request Configuration
- Database Configuration
- Salesforce Configuration
- SAP Configuration
- JMS Configuration
- SFTP Configuration

Avoid duplicating identical configurations across multiple flows.

---

## 4. Configuration Separation

Connector configuration should be separated from environment-specific values.

Examples:

- Host
- Port
- Base URL
- Database name
- Username
- Password
- Client ID
- Client secret
- Queue name
- File path

Environment-specific values should normally be externalized.

---

## 5. Authentication

Connector authentication must use appropriate mechanisms supported by the target system.

Review:

- Username/password authentication
- Client credentials
- OAuth
- API keys
- Certificates
- Tokens
- Mutual TLS

Credentials must not be hard-coded in Mule XML or source code.

---

## 6. Secret Protection

Sensitive connector properties must be protected.

Review whether:

- Passwords are encrypted.
- Client secrets are encrypted.
- API keys are protected.
- Tokens are protected.
- Secure properties are used where appropriate.
- Secrets are not duplicated in plain text.

Any exposed credential should be treated as a security finding.

---

## 7. TLS

Connectors communicating over networks must use appropriate TLS configuration when required.

Review:

- HTTPS
- TLS versions
- Truststore
- Keystore
- Certificate configuration
- Mutual TLS
- Certificate validation

Do not recommend disabling certificate validation as a normal solution to connection problems.

---

## 8. Certificate Validation

Certificate validation should remain enabled unless there is a documented and justified exception.

Flag configurations that:

- Disable certificate validation
- Trust all certificates
- Use insecure TLS settings
- Bypass hostname validation

These should normally be treated as security findings.

---

## 9. HTTP Connector

HTTP Request configurations should define appropriate:

- Connection timeout
- Response timeout
- Authentication
- TLS
- Reconnection strategy
- Response handling

Avoid relying on unsuitable defaults for critical integrations.

---

## 10. HTTP Listener

HTTP Listener configurations should use appropriate:

- Host
- Port
- TLS
- Authentication
- Base path
- Listener configuration

Production APIs should not expose unnecessary unsecured HTTP endpoints.

---

## 11. HTTP Timeouts

HTTP requests should have timeout behavior appropriate to the downstream service.

Review:

- Connection timeout
- Response timeout
- Read timeout where applicable

Avoid extremely large timeouts that can unnecessarily consume resources.

Avoid extremely small timeouts that cause legitimate requests to fail.

---

## 12. HTTP Retry

Retries should be used carefully.

Retry only operations where:

- The failure is transient.
- The operation is safe to retry.
- The downstream system can tolerate retries.
- The retry count is bounded.

Avoid blindly retrying all HTTP failures.

---

## 13. HTTP Status Codes

HTTP responses should be handled according to their semantics.

Review handling for:

- 2xx
- 3xx
- 4xx
- 5xx

Do not treat every non-2xx response as an infrastructure failure.

---

## 14. Database Connector

Database configurations should define appropriate:

- Connection settings
- Pool settings
- Timeout
- Authentication
- TLS where applicable
- Transaction behavior

Database credentials must be securely managed.

---

## 15. Database Connection Pooling

Review connection pool configuration for applications with significant database traffic.

Consider:

- Maximum pool size
- Minimum pool size
- Connection timeout
- Idle timeout
- Database capacity

Do not recommend increasing pool size without evidence of a connection bottleneck.

---

## 16. Database Queries

Queries should be:

- Parameterized
- Efficient
- Readable
- Appropriate for the expected data volume

Do not construct SQL by concatenating untrusted input.

---

## 17. Database Transactions

Transactions should be used when multiple operations require atomic behavior.

Review:

- Transaction boundaries
- Rollback behavior
- Nested operations
- External calls inside transactions

Avoid keeping database transactions open across unnecessarily long external operations.

---

## 18. Database Bulk Operations

Use bulk operations when they provide meaningful performance benefits.

Review patterns where a flow performs a database operation individually for every record.

Consider:

- Number of records
- Query complexity
- Transaction requirements
- Database capabilities
- Failure handling

---

## 19. Salesforce Connector

Salesforce integrations should consider:

- Authentication
- Connection configuration
- API limits
- Bulk operations
- Retry behavior
- Error handling
- Query efficiency

Avoid unnecessarily making individual API calls for large record sets when supported bulk operations are more appropriate.

---

## 20. SaaS API Limits

Connectors communicating with SaaS platforms should account for platform limits.

Examples:

- API request limits
- Batch limits
- Payload limits
- Concurrent request limits
- Rate limits

Do not assume unlimited downstream capacity.

---

## 21. Messaging Connectors

Messaging connectors should define appropriate:

- Connection settings
- Acknowledgment behavior
- Retry behavior
- Redelivery behavior
- Error handling
- Dead-letter handling where applicable

Review whether message processing semantics match business requirements.

---

## 22. Message Redelivery

Applications should have an intentional strategy for message redelivery.

Review:

- Maximum redelivery attempts
- Duplicate processing
- Idempotency
- Dead-letter queues
- Error handling

Avoid unlimited redelivery.

---

## 23. Idempotency

Operations that may be retried or redelivered should be evaluated for idempotency.

Examples:

- Database inserts
- Payment requests
- Order creation
- External API updates
- Message processing

A retry must not unintentionally create duplicate business transactions.

---

## 24. SFTP Connector

SFTP integrations should use secure authentication.

Review:

- SSH keys
- Password handling
- Host key validation
- Directory configuration
- File permissions
- Connection timeout
- Retry behavior

Avoid insecure file transfer protocols when secure alternatives are required.

---

## 25. File Connector

File operations should consider:

- File path
- Permissions
- File locking
- Duplicate processing
- Error handling
- Cleanup
- Large files
- Concurrent access

Avoid hard-coded environment-specific file paths.

---

## 26. Object Store

Object Store usage should consider:

- Key naming
- Expiration
- Persistence requirements
- Size
- Serialization
- Concurrency
- Sensitive information

Do not store sensitive data unnecessarily.

---

## 27. Connector Reconnection

Reconnection strategies should be configured appropriately for transient failures.

Review:

- Reconnection enabled/disabled
- Retry count
- Retry frequency
- Blocking/non-blocking behavior where applicable

Avoid infinite reconnection loops.

---

## 28. Reconnection vs Retry

Do not treat connector reconnection and business-operation retry as interchangeable.

Reconnection addresses connection availability.

Retry addresses failed operations.

Both must be evaluated independently.

---

## 29. Connector Error Handling

Connector errors should be handled according to their nature.

Distinguish between:

- Authentication errors
- Authorization errors
- Validation errors
- Connectivity errors
- Timeout errors
- Rate-limit errors
- Server errors
- Business errors

Do not retry errors that are unlikely to succeed without intervention.

---

## 30. Error Propagation

Connector failures must not be silently ignored.

Review:

- On Error Continue
- On Error Propagate
- Error mapping
- Logging
- Response construction

A connector failure must not accidentally produce a successful business response.

---

## 31. Connector Timeouts

Every external connector should be reviewed for appropriate timeout behavior.

Consider:

- Connection establishment
- Read/write
- Response
- Query
- Transaction

Avoid leaving critical external calls with inappropriate defaults.

---

## 32. Performance

Connector usage should consider downstream performance.

Review:

- Number of calls
- Payload size
- Batch size
- Connection reuse
- Parallelism
- Pagination
- Streaming
- Caching where appropriate

Do not introduce caching unless the data consistency requirements allow it.

---

## 33. Pagination

Connectors retrieving large result sets should use pagination where supported.

Review:

- Page size
- Maximum records
- Continuation tokens
- Memory consumption

Avoid retrieving unnecessarily large result sets into memory.

---

## 34. Large Payload Handling

Connectors processing large payloads should use appropriate streaming or batch mechanisms where supported.

Avoid unnecessary:

- Payload duplication
- Serialization
- Deserialization
- In-memory accumulation

---

## 35. Connector Logging

Connector logging should provide enough information to troubleshoot failures without exposing sensitive information.

Do not log:

- Passwords
- Access tokens
- API keys
- Authorization headers
- Private keys
- Sensitive payload fields

---

## 36. Connector Debug Logging

Debug logging should be carefully controlled in production.

Connector debug output may contain:

- Request information
- Response information
- Headers
- Payloads
- Connection information

Verify that enabling debug logging does not expose sensitive information.

---

## 37. Sensitive Headers

Never unnecessarily log or expose:

- Authorization
- Cookie
- Set-Cookie
- API keys
- Security tokens

Sensitive headers should be masked or excluded.

---

## 38. Connector Configuration Naming

Connector configurations should have descriptive names.

Prefer:

    customerApiHttpRequestConfig

over:

    httpRequestConfig1

Prefer:

    customerDatabaseConfig

over:

    dbConfig

---

## 39. Connector Operation Naming

Operations should clearly communicate their purpose.

Prefer:

    Get Customer
    Create Order
    Update Customer

over ambiguous names where the connector configuration or flow structure does not make the operation obvious.

---

## 40. Connector Duplication

Identify unnecessary duplication of connector configuration.

Examples:

- Multiple identical HTTP configurations
- Multiple identical database configurations
- Repeated TLS configurations
- Repeated authentication configuration

Consider reuse when duplication creates maintenance risk.

---

## 41. Connector Version

Review connector versions for:

- Compatibility
- Support status
- Known security issues
- Application runtime compatibility

Do not report an older connector version solely because a newer version exists.

A finding should have a meaningful compatibility, security, support, or maintenance justification.

---

## 42. Deprecated Connectors

Identify deprecated connectors or operations when there is evidence they create:

- Security risk
- Compatibility risk
- Maintenance risk
- Deployment risk

Do not automatically treat every deprecated feature as a critical finding.

---

## 43. Connector Dependencies

Review connector dependencies for:

- Unnecessary dependencies
- Conflicting versions
- Unsupported versions
- Duplicate dependencies

---

## 44. Environment-Specific Connector Configuration

Environment-specific values should be externalized.

Examples:

    dev.customer.api.url
    test.customer.api.url
    prod.customer.api.url

Do not embed environment-specific values directly into flows when configuration properties can be used.

---

## 45. Dynamic Connector Configuration

Dynamic connector configuration should be treated carefully.

Do not allow untrusted input to control:

- Destination URLs
- Hostnames
- File paths
- Database connections
- Credentials
- Connector expressions

This may introduce SSRF, injection, or unauthorized access risks.

---

## 46. Connector Security Boundary

Treat every external connector as a security boundary.

Review:

- Authentication
- Authorization
- TLS
- Certificate validation
- Secrets
- Input validation
- Output handling
- Error handling

---

## 47. External System Trust

Do not automatically trust data received from external systems.

Validate important:

- Fields
- Types
- Values
- Identifiers
- Statuses
- Content

External responses should not bypass application security controls.

---

## 48. Connector Response Validation

Validate connector responses where business correctness depends on specific fields or statuses.

Do not assume a technically successful connector call means the business operation succeeded.

---

## 49. Connector Failover

Where high availability is required, review whether connector configuration supports appropriate failover.

Consider:

- Multiple endpoints
- Load balancing
- Reconnection
- Retry
- Circuit breaking where applicable
- Downstream availability

Do not introduce failover complexity without a business requirement.

---

## 50. Rate Limiting

Connector usage should respect downstream rate limits.

Review:

- Request frequency
- Parallel calls
- Retry amplification
- Batch size
- Backoff

A retry mechanism must not unintentionally amplify load against an already failing system.

---

## 51. Circuit Breaking

For integrations with unreliable downstream systems, consider whether circuit-breaking behavior is required.

Do not automatically require a circuit breaker for every integration.

Evaluate based on:

- Business criticality
- Failure frequency
- Downstream behavior
- Traffic volume
- Recovery characteristics

---

## 52. Connector Transaction Boundaries

Do not assume all connectors participate in the same transaction model.

Review transactions involving multiple systems.

For example:

    Database -> HTTP API -> Database

may not provide atomic rollback across all systems.

The implementation should account for partial failure where necessary.

---

## 53. External Calls Inside Transactions

Avoid unnecessarily performing slow external calls while holding database or other transactional resources.

Review for:

- Long-running HTTP calls
- Messaging calls
- File operations
- External SaaS calls

inside database transactions.

---

## 54. Connector Resource Consumption

Review whether connector usage can exhaust:

- Threads
- Connections
- Memory
- File handles
- API quotas
- Downstream capacity

---

## 55. Connector Concurrency

Parallel connector calls should be justified.

Review:

- Maximum concurrency
- Downstream limits
- Ordering requirements
- Duplicate operations
- Shared state
- Resource limits

---

## 56. Connector Security Checklist

Before completing the connector review, confirm:

- Connector authentication is configured correctly.
- Credentials are not hard-coded.
- Secrets are protected.
- TLS is used where required.
- Certificate validation is enabled.
- Connector URLs are controlled.
- Environment-specific values are externalized.
- Timeouts are appropriate.
- Retry behavior is bounded.
- Reconnection behavior is appropriate.
- Rate limits are considered.
- Large payloads are handled appropriately.
- Pagination is used where appropriate.
- Bulk operations are considered.
- Connector errors are handled intentionally.
- Sensitive headers are not logged.
- Sensitive payloads are not logged.
- Connector versions are appropriate.
- Deprecated functionality was considered.
- Duplicate connector configurations were considered.
- Transaction boundaries are understood.
- Idempotency is considered for retryable operations.
- Concurrency is appropriate for the downstream system.

---

## 57. Connector Review Quality Gate

The reviewer must be able to answer the following questions:

1. Is every connector appropriate for the system it communicates with?
2. Is every connector securely authenticated?
3. Are credentials and secrets protected?
4. Is TLS configured correctly where required?
5. Are certificate validation controls preserved?
6. Are timeout and retry settings appropriate?
7. Could retries create duplicate business operations?
8. Are downstream rate limits considered?
9. Are connector errors handled correctly?
10. Are large payloads and result sets handled efficiently?
11. Are unnecessary connector calls present?
12. Are duplicate connector configurations present?
13. Are environment-specific values externalized?
14. Are connector versions supportable?
15. Are sensitive connector details excluded from logs?
16. Are transaction boundaries correct?
17. Are concurrency and connection-pool settings appropriate?
18. Is the connector configuration maintainable by another developer?

### Final Question

> Can this application communicate with each external system securely, reliably, efficiently, and predictably, even when the external system is slow, unavailable, returns an error, or changes its response?