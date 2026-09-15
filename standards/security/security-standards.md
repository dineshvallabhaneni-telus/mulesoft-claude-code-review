# MuleSoft Security Standards

## 1. Purpose

This document defines standards for reviewing security in MuleSoft applications.

The review must identify security weaknesses involving:

- Authentication
- Authorization
- Secrets
- Sensitive data
- Input validation
- Injection
- Transport security
- API exposure
- Error handling
- Logging
- Configuration
- Dependency and runtime security
- External integrations

Security findings should be evaluated based on realistic attack paths and business impact.

---

## 2. General Security Principles

MuleSoft applications should follow these principles:

- Deny by default
- Least privilege
- Defense in depth
- Secure by default
- Validate untrusted input
- Protect secrets
- Minimize sensitive data exposure
- Use encrypted transport
- Avoid unnecessary privileges
- Fail securely
- Do not expose internal implementation details

---

## 3. Authentication

Applications exposing protected resources must use appropriate authentication.

Review whether:

- Authentication is required where appropriate.
- Authentication is enforced consistently.
- Authentication failures are handled securely.
- Authentication credentials are protected.
- Tokens are validated correctly.
- Authentication is not bypassable through alternate paths.

---

## 4. Authentication Bypass

Look for conditions that could allow unauthenticated access to protected functionality.

Examples:

- Public endpoint accidentally exposing internal functionality
- Missing policy enforcement
- Alternate endpoint bypassing authentication
- Authentication applied only to some routes
- Trusting client-supplied identity information

Authentication bypass is generally a high-severity finding when it exposes protected functionality or data.

---

## 5. Authorization

Authentication establishes identity; authorization determines what that identity may access.

Review whether authorization is enforced for:

- Resources
- Operations
- Administrative functions
- Sensitive data
- Tenant-specific data

---

## 6. Least Privilege

Application identities should have only the permissions required to perform their responsibilities.

Review:

- Database users
- Cloud identities
- API clients
- Messaging permissions
- File-system permissions
- Runtime permissions

Avoid broad administrative permissions when narrower permissions are sufficient.

---

## 7. Broken Object-Level Authorization

Applications should verify that an authenticated caller is authorized to access the specific resource requested.

For example:

    GET /customers/{customerId}

must not assume that authentication alone permits access to every customer.

Authorization should consider the caller's permissions and resource ownership where applicable.

---

## 8. Tenant Isolation

Multi-tenant applications must prevent one tenant from accessing another tenant's data.

Review whether tenant identity is:

- Authenticated
- Validated
- Used in authorization
- Applied to data queries
- Applied consistently across downstream calls

Do not rely solely on a tenant ID supplied by the client.

---

## 9. Client-Supplied Identity

Do not blindly trust client-supplied values such as:

- userId
- username
- role
- tenantId
- accountId
- customerId

Where these values affect authorization, derive or validate them from trusted authentication context.

---

## 10. Secrets

Never hard-code:

- Passwords
- API keys
- Client secrets
- Access tokens
- Private keys
- Database credentials
- Encryption keys

in source code or committed configuration.

---

## 11. Secure Property Management

Sensitive configuration should use the project's approved secure property mechanism.

Review whether:

- Secrets are externalized.
- Secrets are encrypted where appropriate.
- Secret values are not committed to source control.
- Runtime secret injection is used where appropriate.

---

## 12. Secret Exposure in Configuration

Review all:

- YAML
- XML
- Properties
- JSON
- RAML/OAS examples
- MUnit fixtures
- Scripts
- CI configuration

for credentials or secret values.

---

## 13. Secrets in Logs

Never log:

- Passwords
- Access tokens
- Client secrets
- API keys
- Private keys
- Session credentials

Sensitive values must be masked or excluded.

---

## 14. Secrets in Error Messages

Error responses and stack traces must not expose credentials or secret configuration values.

---

## 15. Secrets in URLs

Avoid placing secrets in:

- Query parameters
- Path parameters
- URLs

URLs may be logged by proxies, gateways, browsers, and monitoring systems.

Prefer secure headers or approved authentication mechanisms.

---

## 16. Access Tokens

Access tokens should:

- Be transmitted securely.
- Not be logged.
- Not be persisted unnecessarily.
- Have appropriate expiration.
- Be validated appropriately.

---

## 17. API Keys

API keys should be treated as secrets.

Do not expose them through:

- Source code
- Logs
- Error messages
- Query strings
- Public API responses

---

## 18. Transport Security

External communication containing sensitive or protected information should use TLS.

Review:

- HTTPS
- Secure database connections
- Secure messaging connections
- Secure file transfers

---

## 19. TLS Validation

Do not disable certificate validation merely to make connectivity work.

Configurations that effectively trust all certificates should be treated as security findings unless there is a tightly controlled and documented exception.

---

## 20. Weak TLS

Avoid obsolete or insecure TLS protocols and cipher configurations.

Use versions and cryptographic settings supported by the organization's security baseline.

---

## 21. Certificate Validation

Certificates should be properly validated.

Avoid:

- Trust-all configurations
- Disabled hostname verification
- Untrusted certificate stores
- Expired certificates

unless a controlled test environment explicitly requires an exception.

---

## 22. Mutual TLS

Where mutual TLS is required, review:

- Client certificate validation
- Private-key protection
- Truststore configuration
- Keystore configuration
- Certificate rotation

---

## 23. Certificate Secrets

Private keys and keystore passwords must be protected.

Do not commit private keys or production certificates containing sensitive private material.

---

## 24. Input Validation

All untrusted input should be validated before being used in sensitive operations.

Sources include:

- HTTP requests
- Query parameters
- Path parameters
- Headers
- Message payloads
- Files
- Database data
- External APIs

---

## 25. Allowlist Validation

Where practical, validate against an allowlist of expected values rather than attempting to identify every possible malicious value.

Examples:

- Supported status values
- Known sort fields
- Allowed file types
- Supported operation names

---

## 26. Input Length

Input size should be bounded where appropriate.

Unbounded:

- Strings
- Arrays
- Objects
- Files
- Requests

can create resource-exhaustion risks.

---

## 27. Type Validation

Validate expected data types.

Examples:

- Numeric IDs
- Dates
- Enumerations
- Boolean values
- Structured objects

Do not rely solely on downstream systems to reject malformed input.

---

## 28. Required Fields

Required fields should be validated before downstream processing.

Missing required values should result in controlled validation errors.

---

## 29. Injection

Review whether untrusted input is inserted into:

- SQL
- Dynamic expressions
- URLs
- File paths
- Commands
- Queries
- Headers
- Scripts

without appropriate validation or parameterization.

---

## 30. SQL Injection

Database queries must not construct executable SQL by directly concatenating untrusted input.

Prefer parameterized queries or the connector's safe parameter mechanisms.

Potentially dangerous pattern:

    "SELECT * FROM customer WHERE id = " ++ vars.customerId

Safer designs use parameter binding.

---

## 31. Dynamic SQL

Dynamic SQL requires additional review.

If dynamic SQL is unavoidable:

- Strictly validate dynamic identifiers.
- Parameterize values.
- Avoid accepting arbitrary SQL fragments from clients.

---

## 32. NoSQL Injection

Where NoSQL or structured query systems are used, validate and constrain client-controlled query components.

Do not allow clients to submit arbitrary query expressions unless explicitly designed and secured.

---

## 33. Expression Injection

Do not evaluate untrusted input as executable DataWeave, Mule expressions, scripts, or configuration.

Data should remain data.

---

## 34. Command Injection

Mule applications should not execute operating-system commands using untrusted input.

If command execution is required:

- Validate arguments.
- Use allowlists.
- Avoid shell interpretation.
- Apply least privilege.

---

## 35. Path Traversal

File paths derived from user input must be validated.

Potentially dangerous values include:

    ../

    ..\

and encoded equivalents.

Prefer allowlisted file identifiers rather than accepting arbitrary paths.

---

## 36. File Uploads

File uploads should be validated for:

- Size
- Type
- Extension
- Content where appropriate
- Filename
- Storage location

Uploaded files should not automatically be treated as trusted.

---

## 37. Untrusted Filenames

Do not directly use user-controlled filenames as filesystem paths.

Normalize and validate filenames before use.

---

## 38. XML Security

When processing XML from untrusted sources, use secure XML parser configurations appropriate to the runtime and connector.

Review protections against:

- External entity processing
- Entity expansion
- Excessive XML nesting
- Large XML payloads

---

## 39. XXE

External XML entities should be disabled where not required.

Applications should not allow untrusted XML to cause access to local files or internal network resources.

---

## 40. SSRF

Server-side requests using user-controlled URLs should be carefully restricted.

Do not allow clients to freely select arbitrary destinations for server-side HTTP requests.

---

## 41. SSRF Controls

Where dynamic outbound URLs are required:

- Allowlist permitted hosts.
- Restrict protocols.
- Validate destinations.
- Prevent access to sensitive internal services.
- Avoid trusting redirects blindly.

---

## 42. Header Injection

Client-controlled headers should not be blindly propagated into downstream systems.

Review:

- Authorization
- Host
- Forwarded headers
- Internal identity headers
- Routing headers

---

## 43. Header Trust

Do not trust headers such as:

    X-User-Id

    X-Role

    X-Tenant-Id

for authorization unless they are added by a trusted component and cannot be spoofed by external clients.

---

## 44. Sensitive Data

Applications should minimize collection, processing, storage, and transmission of sensitive information.

Sensitive information may include:

- Personal information
- Financial information
- Authentication data
- Health information
- Government identifiers
- Credentials

---

## 45. Data Minimization

Only process the sensitive data required for the business operation.

Do not retrieve or propagate unnecessary sensitive fields.

---

## 46. Sensitive Data in Responses

Do not return sensitive internal data unless explicitly required by the API contract.

Examples:

- Password hashes
- Internal credentials
- Internal tokens
- Private identifiers
- Database implementation details

---

## 47. Sensitive Data in Logs

Sensitive fields should be masked or omitted.

Examples:

    password = ****

    token = [REDACTED]

Do not rely on developers remembering to avoid logging sensitive data manually.

---

## 48. Sensitive Data in Errors

Error responses should not expose:

- Database connection details
- SQL statements
- Internal hostnames
- Stack traces
- Credentials
- Internal filesystem paths

---

## 49. Error Handling

Security-sensitive failures should produce controlled errors.

Do not expose excessive implementation detail to external clients.

---

## 50. Error Response Design

External error responses should generally contain:

- Appropriate status
- Stable error identifier
- Safe message
- Correlation/reference identifier where appropriate

They should not contain internal stack traces or secret configuration.

---

## 51. Stack Traces

Stack traces should not be returned directly to untrusted clients.

They may reveal:

- Internal classes
- File paths
- Connector configuration
- Host information
- Implementation details

---

## 52. Authentication Error Responses

Authentication and authorization responses should avoid revealing unnecessary information.

For example, do not expose sensitive details that allow attackers to enumerate valid accounts unless the API explicitly requires such behavior.

---

## 53. CORS

CORS configuration should be appropriately restrictive.

Avoid unrestricted origins for sensitive APIs unless there is a documented and justified requirement.

---

## 54. Credentialed CORS

When credentials are supported, review:

- Allowed origins
- Allowed headers
- Allowed methods
- Credential behavior

Do not combine credentialed access with an overly broad origin policy.

---

## 55. HTTP Methods

Only expose HTTP methods required by the API.

Unnecessary methods can increase attack surface.

---

## 56. API Exposure

Review whether internal flows are accidentally exposed as public API endpoints.

Administrative and internal functionality should not be unintentionally reachable from external clients.

---

## 57. Administrative Endpoints

Administrative operations should receive stronger security controls where appropriate.

Examples:

- Configuration changes
- User management
- Data deletion
- Replay operations
- Operational controls

---

## 58. Debug Endpoints

Do not expose debugging or diagnostic endpoints in production unless explicitly secured and required.

---

## 59. Health Endpoints

Health endpoints should expose only information required for health monitoring.

Avoid exposing:

- Credentials
- Internal configuration
- Detailed dependency information
- Sensitive environment details

---

## 60. Rate Limiting

Public or sensitive APIs should consider rate limiting where abuse or resource exhaustion is possible.

Rate limiting is particularly relevant for:

- Authentication endpoints
- Expensive operations
- Search endpoints
- File uploads
- Password-related operations

---

## 61. Denial of Service

Review whether attackers can cause excessive resource consumption through:

- Large payloads
- Large collections
- Expensive queries
- Repeated requests
- Excessive concurrency
- Expensive transformations

---

## 62. Request Limits

Apply reasonable limits for:

- Request body size
- File size
- Collection size
- Pagination limits
- Query length
- Processing time

---

## 63. Pagination Limits

Clients should not be able to request arbitrarily large pages.

For example:

    pageSize=1000000

should not cause the application to retrieve an excessive amount of data.

---

## 64. Authentication Credential Handling

Credentials should not be stored in variables longer than necessary.

Avoid copying credentials into multiple variables or payloads.

---

## 65. Password Handling

Applications should not log or return passwords.

Where password processing is unavoidable, minimize exposure and use approved authentication mechanisms.

---

## 66. Token Propagation

Only propagate tokens to systems that legitimately require them.

Do not forward an inbound authorization token to every downstream system automatically.

---

## 67. Token Audience

Where applicable, validate that a token is intended for the service or API receiving it.

---

## 68. Token Expiration

Authentication tokens should respect expiration requirements.

Do not accept expired tokens.

---

## 69. JWT Validation

Where JWTs are used, review:

- Signature validation
- Issuer validation
- Audience validation
- Expiration validation
- Not-before validation where relevant
- Algorithm restrictions

Do not trust JWT claims merely because they are present.

---

## 70. JWT Algorithm Handling

Do not allow an attacker to arbitrarily select an insecure or unexpected signing algorithm.

Use an approved algorithm set.

---

## 71. Replay Protection

Where replay attacks are relevant, consider:

- Token expiration
- Nonces
- Idempotency keys
- Request timestamps
- Replay detection

The appropriate control depends on the protocol and business operation.

---

## 72. Idempotency Keys

For sensitive operations that may be retried, idempotency controls can prevent duplicate actions.

Examples:

- Payments
- Orders
- Transfers
- Provisioning

---

## 73. Database Security

Database connections should use:

- Least-privileged accounts
- Secure transport where required
- Protected credentials
- Appropriate authentication

---

## 74. Database Credentials

Database credentials must not be hard-coded or committed to source control.

---

## 75. Database Authorization

The Mule application should not normally use a database account with unrestricted administrative privileges.

Use an account limited to required operations.

---

## 76. Database Data Exposure

Queries should retrieve only data required for the operation.

Avoid unnecessarily returning sensitive columns.

---

## 77. External System Credentials

Credentials for external APIs, SFTP servers, SaaS systems, and messaging platforms must be protected using approved secret-management mechanisms.

---

## 78. SFTP Security

For SFTP integrations, review:

- Host verification
- Authentication method
- Private-key protection
- Password protection
- Secure transfer
- Least-privileged account

Do not disable host verification simply to resolve connection problems.

---

## 79. Messaging Security

Messaging integrations should use appropriate:

- Authentication
- Authorization
- TLS
- Credential protection

Review whether messages can be accessed by unauthorized consumers.

---

## 80. File Security

Files containing sensitive information should be:

- Stored securely
- Access-controlled
- Encrypted where required
- Removed when no longer needed

---

## 81. Temporary Files

Temporary files containing sensitive data should be protected and deleted after use.

---

## 82. Source Control

Do not commit:

- Secrets
- Private keys
- Production configuration containing credentials
- Sensitive customer data
- Production exports

---

## 83. Repository Security

Review source-controlled files including:

- Mule XML
- Properties
- YAML
- JSON
- Scripts
- Test fixtures
- CI configuration

for sensitive information.

---

## 84. Dependency Security

Review dependencies for:

- Known vulnerabilities
- Unsupported versions
- Unnecessary libraries
- Suspicious or untrusted dependencies

Security findings should consider the actual applicability of a vulnerability to the application.

---

## 85. Dependency Minimization

Remove dependencies that are not required.

Every unnecessary dependency increases the application's attack surface and maintenance burden.

---

## 86. Runtime Security

Mule runtime versions should follow the organization's supported and security-approved versions.

Unsupported runtimes may contain unresolved security vulnerabilities.

---

## 87. Secure Defaults

Security-sensitive configuration should default to the safer behavior.

Examples:

- TLS enabled
- Authentication enabled
- Access denied by default
- Sensitive logging disabled
- Strong validation enabled

---

## 88. Security Configuration Drift

Review whether environments can unintentionally disable security controls.

Examples:

- Production authentication disabled
- TLS verification disabled
- Broad CORS allowed
- Debug logging enabled
- Security policies omitted

---

## 89. Environment Separation

Production credentials and configuration should not be reused in development or test environments unless explicitly required and appropriately protected.

---

## 90. Logging and Security

Logging should support security monitoring without exposing sensitive information.

Review:

- Authentication failures
- Authorization failures
- Suspicious requests
- Security-relevant errors

while ensuring sensitive values are masked.

---

## 91. Audit Logging

Security-sensitive operations should generate appropriate audit information where required.

Examples:

- Administrative actions
- Permission changes
- Sensitive data access
- Configuration changes
- Financial operations

---

## 92. Audit Log Integrity

Audit logs should not be easily modified or deleted by ordinary application users.

The exact implementation depends on the organization's logging architecture.

---

## 93. Correlation IDs

Correlation IDs should help trace requests without becoming security-sensitive identifiers.

Do not place secrets or credentials into correlation IDs.

---

## 94. Security and Error Handling

Security failures should fail closed where appropriate.

For example, if authorization cannot be established, the application should not continue as though authorization succeeded.

---

## 95. Fail Securely

When a security control fails unexpectedly, the application should default to the safer behavior where practical.

Examples:

- Authorization service unavailable -> deny access
- Token validation fails -> reject request
- Required security configuration missing -> fail startup or reject operation

---

## 96. Security Exceptions

Security exceptions should be explicit and documented.

Do not suppress security failures merely to keep a flow running.

---

## 97. Sensitive Data in Payloads

Avoid unnecessarily carrying sensitive data through multiple flows and processors.

Reduce exposure by removing or masking sensitive fields when no longer needed.

---

## 98. Data Encryption at Rest

Sensitive information stored persistently should use appropriate encryption controls where required.

Review:

- Databases
- Object Stores
- Files
- Queues
- Persistent caches

---

## 99. Encryption Key Management

Encryption keys should be:

- Protected
- Rotated according to policy
- Access-controlled
- Separated from encrypted data where appropriate

Do not hard-code encryption keys.

---

## 100. Security Review Checklist

Before completing the security review, confirm:

- Authentication is enforced where required.
- Authentication cannot be bypassed through alternate paths.
- Authorization is enforced for protected resources.
- Object-level authorization is implemented where required.
- Tenant isolation is enforced.
- Client-supplied identity is not blindly trusted.
- Least privilege is applied.
- Secrets are not hard-coded.
- Secure properties or approved secret management is used.
- Secrets are not logged.
- Secrets are not exposed in URLs.
- TLS is used for sensitive communications.
- TLS certificate validation is enabled.
- Weak TLS configurations are avoided.
- Private keys are protected.
- Input is validated.
- Input sizes are bounded where appropriate.
- SQL injection risks are controlled.
- Dynamic query construction is controlled.
- Expression injection is prevented.
- Command injection is prevented.
- Path traversal is prevented.
- File uploads are validated.
- XML processing is secured.
- XXE risks are controlled.
- SSRF risks are controlled.
- Header injection risks are controlled.
- Sensitive data is minimized.
- Sensitive data is not unnecessarily returned.
- Error responses do not expose internals.
- Stack traces are not returned to clients.
- CORS is appropriately restricted.
- Unnecessary HTTP methods are not exposed.
- Administrative endpoints are protected.
- Debug endpoints are not exposed unnecessarily.
- Health endpoints do not expose sensitive details.
- Rate limiting is considered for abuse-prone endpoints.
- Resource-exhaustion risks are controlled.
- Pagination limits are enforced.
- Tokens are securely handled.
- JWT validation is complete where applicable.
- Database credentials are protected.
- Database privileges are limited.
- External-system credentials are protected.
- SFTP host verification is not disabled.
- Messaging security is configured appropriately.
- Temporary sensitive files are protected and cleaned up.
- Secrets are absent from source control.
- Dependencies and runtime versions follow security requirements.
- Production security configuration cannot be accidentally disabled.
- Security events are logged appropriately.
- Sensitive values are masked in logs.
- Audit logging is implemented where required.
- Security failures fail securely.

---

## 101. Security Severity Guidance

### Critical

Use critical severity for issues that can enable severe compromise with little or no additional control.

Examples:

- Remote code execution
- Direct exposure of highly sensitive credentials
- Authentication bypass providing broad administrative access
- Unrestricted arbitrary command execution

### High

Use high severity for issues such as:

- Authorization bypass
- SQL injection
- Significant SSRF
- Hard-coded production credentials
- Private-key exposure
- Broad sensitive-data exposure
- Disabled TLS validation in production
- Cross-tenant data access

### Medium

Examples:

- Missing security validation with limited exploitability
- Excessively permissive CORS
- Missing rate limiting on sensitive endpoints
- Sensitive information exposed through controlled errors
- Excessive application privileges

### Low

Examples:

- Minor security-hardening gaps
- Non-sensitive information disclosure
- Missing defense-in-depth control where exploitation requires another weakness

Severity should consider exploitability, impact, exposure, and compensating controls.

---

## 102. Security Quality Gate

The reviewer must be able to answer the following questions:

1. Is authentication enforced where required?
2. Is authorization enforced at the appropriate resource and operation level?
3. Can one user or tenant access another user's data?
4. Are secrets protected throughout configuration, runtime, and logging?
5. Is transport security correctly configured?
6. Is untrusted input validated?
7. Are injection risks controlled?
8. Are dynamic URLs and file paths restricted?
9. Are sensitive errors prevented from reaching external clients?
10. Are APIs protected against excessive resource consumption?
11. Are external credentials and downstream permissions appropriately restricted?
12. Are sensitive data and files minimized and protected?
13. Are production security controls resistant to configuration mistakes?
14. Are security-relevant actions observable without exposing sensitive information?
15. Does the application fail securely when security controls cannot be established?

### Final Question

> Could an untrusted user, compromised credential, malicious input, or misconfigured client bypass a security boundary, obtain unauthorized data, execute unintended operations, or gain access to secrets—and if so, are those risks adequately prevented and contained?