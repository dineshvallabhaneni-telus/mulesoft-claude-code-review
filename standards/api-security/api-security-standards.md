# MuleSoft API Security Standards

## 1. Purpose

This document defines the standards used to assess API security in MuleSoft applications.

The review must evaluate API security from the perspective of:

- Senior MuleSoft Architect
- API Security Architect
- Enterprise Security Architect
- Senior Technical Lead

The objective is to determine whether APIs are appropriately protected against:

- Unauthorized access
- Authentication failures
- Authorization bypass
- Credential exposure
- Excessive traffic
- Malicious input
- Data leakage
- Insecure transport
- Improper error disclosure
- Abuse of downstream systems

The review must distinguish between:

1. Controls implemented in application source code.
2. Controls configured through MuleSoft API Manager/API policies.
3. Controls implemented externally by infrastructure or gateways.

Do not report an infrastructure control as missing solely because it is not present in the source repository.

---

# 2. API Security Review Principles

The reviewer must evaluate:

- Authentication
- Authorization
- API policies
- TLS
- Client identity
- OAuth/JWT
- Client ID enforcement
- Rate limiting
- Threat protection
- Input validation
- Output protection
- Sensitive data handling
- Error handling
- CORS
- Webhook security
- Replay protection where applicable
- Idempotency
- Logging
- Secrets
- API versioning
- Security configuration
- Environment separation

---

# 3. API Discovery

Identify all API entry points.

Review:

- HTTP Listener
- HTTPS Listener
- APIkit Router
- APIkit Console
- RAML
- OAS/OpenAPI
- HTTP Request exposure where relevant
- Webhook endpoints
- Public endpoints
- Internal endpoints

Also identify APIs indirectly exposed through:

- Flow references
- Listener configurations
- Shared domains
- Gateway configuration where visible

Do not assume every HTTP listener is externally exposed.

---

# 4. API Contract Discovery

Identify API specifications such as:

- RAML
- OpenAPI
- OAS
- API fragments
- JSON schemas
- XML schemas

Compare the implementation against the declared API contract where possible.

Look for:

- Undocumented endpoints
- Undocumented query parameters
- Undocumented headers
- Security mismatches
- Incorrect authentication assumptions
- Inconsistent response codes

---

# 5. Authentication

Every externally accessible API must have an appropriate authentication mechanism unless the endpoint is intentionally public.

Potential mechanisms include:

- OAuth 2.0
- OpenID Connect
- JWT
- Client ID/Client Secret
- Mutual TLS
- Basic authentication where explicitly justified
- API gateway authentication
- Platform identity mechanisms

Do not mandate OAuth for every internal integration.

Authentication must match the API's trust boundary and use case.

---

# 6. Public APIs

Public APIs should not rely solely on obscurity.

Examples of insufficient protection:

- Hidden URL
- Non-obvious endpoint name
- Custom HTTP header without cryptographic verification
- IP restriction alone where stronger authentication is required

---

# 7. Internal APIs

Internal APIs still require appropriate security.

Do not assume that:

> Internal network = trusted network.

Evaluate:

- Authentication
- Authorization
- TLS
- Network controls
- Service identity
- Least privilege

---

# 8. Authentication vs Authorization

Authentication answers:

> Who is calling?

Authorization answers:

> What is the caller allowed to do?

A valid authenticated identity must not automatically receive unrestricted access.

---

# 9. Authorization

Where authorization is required, verify that access is appropriately restricted by:

- Role
- Scope
- Permission
- Application identity
- Resource ownership
- Business rules

Do not report missing authorization when the API intentionally provides the same access to all authenticated clients.

---

# 10. OAuth 2.0

When OAuth 2.0 is used, review:

- Token validation
- Issuer
- Audience
- Expiration
- Signature
- Scopes
- Client authentication
- TLS
- Token storage

Do not assume a token is valid merely because it exists.

---

# 11. JWT

When JWTs are used, verify where implementation evidence exists:

- Signature validation
- Algorithm validation
- Issuer validation
- Audience validation
- Expiration validation
- Not-before validation where appropriate
- Required claims
- Scope/role claims

Avoid accepting unsigned or improperly validated JWTs.

---

# 12. JWT Algorithm Security

The implementation must not blindly trust an attacker-controlled JWT algorithm value.

Avoid insecure configurations that allow:

- `none`
- Unexpected algorithms
- Weak algorithms
- Algorithm confusion

Use an explicitly configured list of accepted algorithms where supported.

---

# 13. Token Expiration

Authentication tokens should have appropriate expiration.

Do not recommend excessively long-lived access tokens without justification.

---

# 14. Token Handling

Never log:

- Access tokens
- Refresh tokens
- Authorization headers
- Client secrets

Tokens should not be unnecessarily stored in:

- Variables
- Object Store
- Files
- Databases
- Logs

---

# 15. Client ID Enforcement

Where Client ID enforcement is part of the API security model, verify that:

- Client identity is validated.
- Credentials are not hard-coded.
- Client secrets are protected.
- Policies are consistently applied.

If enforcement is managed in API Manager and cannot be verified from source:

`Verification Required`

---

# 16. API Manager Policies

Where API Manager policy configuration is visible, review applicable policies such as:

- Client ID enforcement
- OAuth
- JWT validation
- Rate limiting
- Spike control
- IP allow/deny
- Threat protection
- Header validation
- CORS
- Custom policies

Do not assume that absence from source means the policy is absent from the deployed API.

---

# 17. Policy Verification

If policy configuration is external to the repository, report:

`API Manager policy verification required.`

The final report should distinguish:

- Confirmed policy
- Not visible in repository
- Verification required

Do not convert unknown configuration into a confirmed security vulnerability.

---

# 18. TLS

Externally accessible APIs should use HTTPS/TLS.

Avoid exposing sensitive APIs over plain HTTP.

If both HTTP and HTTPS listeners exist, determine whether HTTP is:

- Intentionally internal
- Used only for redirection
- Used by a trusted infrastructure component
- Actually exposed

Report only meaningful security risks.

---

# 19. TLS Configuration

Where configuration is visible, review:

- TLS enabled
- Keystore
- Truststore
- Certificate configuration
- Protocol versions
- Cipher configuration where configurable
- Certificate validation

Do not recommend disabling certificate validation to solve connectivity problems.

---

# 20. Mutual TLS

For high-trust integrations, consider whether mutual TLS is appropriate.

Potential use cases:

- B2B integrations
- High-value internal services
- Strong service identity requirements

Do not require mTLS for every API.

---

# 21. Certificate Management

Review:

- Certificate references
- Keystore configuration
- Truststore configuration
- Expiration management where visible
- Environment-specific certificates

Do not include certificate private keys in findings.

---

# 22. CORS

Review CORS where APIs are consumed by browser-based applications.

Avoid unrestricted configurations such as:

- `Access-Control-Allow-Origin: *`

when credentials or sensitive browser interactions are involved.

Do not report permissive CORS for APIs that are not browser-facing unless it creates an actual risk.

---

# 23. HTTP Methods

Review whether APIs appropriately restrict HTTP methods.

Avoid exposing unnecessary methods.

Examples:

- `DELETE` when not required
- `PUT` when only reads are required
- `PATCH` without appropriate authorization

---

# 24. Input Validation

API input must be validated appropriately.

Review:

- Required fields
- Data types
- Length limits
- Format validation
- Enum validation
- Range validation
- Nested structures
- Query parameters
- Headers

Schema validation should be used where appropriate.

---

# 25. Request Size

APIs should have appropriate request-size limits.

Large unrestricted requests can create:

- Memory pressure
- Denial-of-service risk
- Excessive processing
- Downstream failures

Do not prescribe an arbitrary limit without considering the API contract.

---

# 26. Response Size

Consider whether large responses could cause:

- Memory pressure
- Excessive latency
- Client instability

Use pagination or streaming where appropriate.

---

# 27. Pagination

Collection endpoints should use pagination where result sets may become large.

Review:

- Page size
- Maximum page size
- Offset/cursor strategy
- Sorting
- Stable pagination

Do not require pagination for genuinely small bounded datasets.

---

# 28. Query Parameters

Validate user-controlled query parameters.

Pay attention to:

- Filters
- Sorting
- Pagination
- Field selection
- Dynamic queries

Do not allow uncontrolled user input to directly become:

- SQL
- Script
- Expression
- File path
- Connector configuration

---

# 29. SQL Injection

Database queries must not directly concatenate untrusted API input into SQL.

Prefer:

- Parameterized queries
- Query parameters
- Safe database connector mechanisms

Do not report DataWeave string interpolation as SQL injection unless the resulting value reaches a database query unsafely.

---

# 30. Expression Injection

Do not allow user input to be interpreted as executable Mule expressions or dynamic code.

Review:

- Dynamic expressions
- Dynamic scripts
- Dynamic configuration
- Expression evaluation

---

# 31. Command Injection

API input must not directly become operating-system commands.

Custom Java/Python/script execution requires special attention.

Where custom code is present, inspect whether external input reaches command execution.

---

# 32. Path Traversal

File-related APIs must validate user-controlled paths.

Avoid allowing API input to directly control:

- File names
- Directory names
- File paths

without validation.

Look for patterns such as:

- `../`
- Absolute path injection
- Dynamic file path construction

---

# 33. SSRF

If the API accepts a URL or host from a caller and the application makes an outbound request based on that value, evaluate SSRF risk.

Review:

- URL allowlists
- Host allowlists
- Protocol restrictions
- Internal IP protection
- Metadata endpoint protection

Do not report SSRF where outbound destinations are fixed by configuration.

---

# 34. XML Security

For XML APIs, review protection against:

- XXE
- Entity expansion
- Oversized XML
- Malicious XML structures

Do not recommend disabling required XML features without understanding application requirements.

---

# 35. JSON Security

Review:

- Excessive nesting
- Large payloads
- Unexpected fields
- Schema validation
- Type confusion

---

# 36. SOAP APIs

For SOAP APIs review:

- WS-Security where applicable
- TLS
- Authentication
- Schema validation
- XML security
- Error disclosure

Do not require WS-Security when transport and application security requirements are already appropriately satisfied.

---

# 37. Webhook Security

Webhook endpoints should verify the source where appropriate.

Potential mechanisms:

- Signature validation
- Shared secret
- Mutual TLS
- OAuth
- IP restrictions as an additional control

Do not trust a caller merely because the endpoint is difficult to discover.

---

# 38. Webhook Replay Protection

For signed webhooks, consider replay protection where duplicate requests could cause harm.

Potential controls:

- Timestamp validation
- Nonce
- Event ID
- Idempotency key

---

# 39. Idempotency

API operations that can safely be retried should consider idempotency.

Especially:

- Payments
- Orders
- Resource creation
- State changes

Do not require idempotency for read-only operations.

---

# 40. Rate Limiting

APIs should have appropriate traffic controls.

Potential controls:

- Rate limiting
- Spike control
- Quotas
- Per-client limits

Consider:

- API SLA
- Consumer behavior
- Backend capacity
- Business criticality

---

# 41. Rate Limiting vs Retry

Do not configure aggressive client retries against rate-limited APIs.

Review interaction between:

- API rate limits
- Connector retries
- Client retries
- Downstream limits

---

# 42. Denial-of-Service Protection

Consider protection against:

- Large requests
- Large responses
- Excessive requests
- Expensive operations
- Repeated authentication attempts
- Resource exhaustion

Do not claim full DDoS protection from Mule application code alone.

---

# 43. Expensive Operations

Identify endpoints that perform expensive operations such as:

- Large database queries
- Multiple external calls
- Large transformations
- File processing
- Batch execution

Consider:

- Authorization
- Rate limits
- Pagination
- Async processing
- Request limits

---

# 44. Sensitive Data

Identify APIs handling:

- Passwords
- Financial information
- Personal information
- Tokens
- Credentials
- Confidential business information

Review whether the API unnecessarily exposes sensitive fields.

---

# 45. Data Minimization

API responses should return only the data required by the consumer.

Avoid exposing:

- Internal IDs
- Database metadata
- Internal status fields
- Credentials
- Debug information
- Internal system details

---

# 46. Sensitive Request Data

Sensitive data should not be unnecessarily:

- Logged
- Cached
- Persisted
- Stored in Object Store
- Returned in error messages

---

# 47. Error Responses

API error responses must not expose:

- Stack traces
- Java exceptions
- Database errors
- Internal hostnames
- File paths
- Credentials
- Connector internals

Return controlled error responses.

---

# 48. HTTP Status Codes

API responses should use meaningful HTTP status codes.

Examples:

- `200` Success
- `201` Created
- `202` Accepted
- `204` No Content
- `400` Bad Request
- `401` Unauthorized
- `403` Forbidden
- `404` Not Found
- `409` Conflict
- `429` Too Many Requests
- `500` Internal Server Error
- `502` Bad Gateway
- `503` Service Unavailable

Do not force one status code for all failures.

---

# 49. Authentication Error Handling

Authentication failures should not unnecessarily reveal:

- Whether a username exists
- Internal authorization logic
- Token validation details
- Internal identity provider information

---

# 50. Authorization Error Handling

Avoid exposing excessive authorization details.

For example, do not disclose internal role names unless required.

---

# 51. API Versioning

Security-sensitive API changes should consider backward compatibility.

Do not leave insecure legacy API versions indefinitely without an intentional support strategy.

---

# 52. Deprecated APIs

Identify deprecated APIs where source evidence indicates they are still active.

Recommendations should include:

- Consumer migration
- Deprecation period
- Retirement plan

Do not assume an API is deprecated merely because its version number is old.

---

# 53. Secrets in API Configuration

Never hard-code:

- Client secrets
- API keys
- Passwords
- Tokens
- Private keys

in:

- Mule XML
- RAML
- OAS
- DataWeave
- Java
- Python
- `.properties`
- `.yaml`
- `.yml`

Sensitive values must be securely managed.

---

# 54. Secure Properties

Where MuleSoft Secure Configuration Properties are used, verify that:

- Sensitive values are protected.
- Encryption configuration is appropriate.
- Decryption keys are not committed.
- Plain-text equivalents are not also committed.

---

# 55. Secret Rotation

If a credential is found in source control, remediation must include:

1. Remove the credential.
2. Rotate/revoke the credential.
3. Replace it with secure configuration.
4. Check whether repository history contains the credential.
5. Assess downstream exposure.

Do not treat encryption alone as sufficient after exposure.

---

# 56. API Keys

API keys should:

- Be stored securely.
- Not be logged.
- Not be committed.
- Have appropriate lifecycle management.
- Be revocable.

---

# 57. Basic Authentication

Basic authentication should only be used when justified.

If used:

- TLS is mandatory.
- Credentials must not be logged.
- Credentials must be securely managed.
- Stronger mechanisms should be considered where appropriate.

---

# 58. Authorization Header

Never log complete:

`Authorization`

headers.

Mask or exclude them from logging.

---

# 59. Cookie Security

Where APIs use cookies, review:

- Secure
- HttpOnly
- SameSite
- Appropriate expiration

Do not require cookie controls for APIs that do not use browser cookies.

---

# 60. CSRF

CSRF protection should be considered for browser-based state-changing APIs using cookie-based authentication.

Do not report CSRF against token-based APIs that are not vulnerable to the same browser credential model without evidence.

---

# 61. API Security Logging

Security-relevant events should be observable.

Consider logging:

- Authentication failures
- Authorization failures
- Rejected requests
- Rate-limit events
- Important security policy failures

Never log the sensitive credential itself.

---

# 62. Correlation IDs

Security events should be correlatable with application activity.

Where applicable, preserve:

- Correlation ID
- Request ID
- Trace ID

Do not trust a caller-provided identifier blindly for security decisions.

---

# 63. Header Security

Review whether APIs accept sensitive control headers from callers without validation.

Examples:

- Internal routing headers
- User identity headers
- Role headers
- Security headers

Do not trust headers such as:

`X-User`

or:

`X-Role`

as authoritative identity unless they are injected by a trusted security boundary and cannot be spoofed.

---

# 64. Host and Forwarded Headers

Do not blindly trust externally supplied:

- `Host`
- `X-Forwarded-Host`
- `X-Forwarded-For`
- `X-Forwarded-Proto`

for security decisions.

---

# 65. HTTP Header Injection

Validate user-controlled header values where they can influence:

- Downstream requests
- Redirects
- Logs
- Security decisions

---

# 66. Redirect Security

Do not allow user-controlled redirect destinations without validation.

Open redirects can facilitate:

- Phishing
- Token leakage
- Trust abuse

---

# 67. API Documentation Security

API specifications should not expose:

- Credentials
- Internal secrets
- Private endpoints
- Sensitive internal implementation details

unless required and appropriately protected.

---

# 68. API Console

Development API consoles should not unintentionally be exposed in production.

Verify:

- Console availability
- Authentication
- Environment restrictions

Where this cannot be established:

`Verification Required`

---

# 69. Mocking and Test Endpoints

Test or mock endpoints must not be exposed in production.

Look for:

- Mock APIs
- Debug endpoints
- Test listeners
- Diagnostic flows

---

# 70. Debug Endpoints

Do not expose endpoints that allow:

- Runtime inspection
- Arbitrary data retrieval
- Configuration retrieval
- Test execution
- Internal diagnostics

without strong authorization.

---

# 71. Internal Flow Exposure

Internal flows should not accidentally become externally callable.

Review listener configuration and flow exposure.

---

# 72. API Security Architecture

The reviewer must document:

- Authentication architecture
- Authorization architecture
- API policy architecture
- TLS architecture
- Secret management
- Input validation
- Rate limiting
- Error security
- Logging
- External security dependencies

---

# 73. Infrastructure Verification

Use:

`Verification Required`

when API security depends on external configuration such as:

- API Manager
- Anypoint Platform
- Load balancer
- WAF
- Identity provider
- Network controls
- Cloud infrastructure

The report must explicitly identify what must be verified.

---

# 74. No Unsupported Security Claims

Do not state:

- "API is unsecured"
- "OAuth is missing"
- "Rate limiting is missing"
- "WAF is missing"
- "API Manager policy is missing"

unless the repository or available deployment evidence confirms the condition.

Use:

`Not evidenced in repository — infrastructure verification required.`

when appropriate.

---

# 75. API Security Finding Format

Every API security finding must contain:

- Finding ID
- Title
- Category
- Severity
- Status
- Location
- Evidence
- Impact
- Recommendation
- Concrete solution
- Verification requirement if applicable
- Priority

Use IDs such as:

`MULE-APISEC-001`

---

# 76. API Security Severity

## Critical

Use for severe exploitable API vulnerabilities such as:

- Unauthenticated access to highly sensitive data
- Authentication bypass
- Authorization bypass
- Exposed production credentials
- Severe injection vulnerability

## High

Use for significant security weaknesses such as:

- Missing authentication on sensitive APIs
- Missing authorization
- Critical sensitive-data exposure
- Significant injection risk
- Weak token validation

## Medium

Use for meaningful but less immediately exploitable issues.

Examples:

- Missing rate limiting on moderate-risk endpoints
- Excessive error disclosure
- Weak input validation
- Missing security headers where relevant

## Low

Use for minor hardening opportunities.

## Warning

Use for:

- Infrastructure-dependent controls
- Potential risks
- Verification requirements

---

# 77. API Security Positive Findings

Recognize meaningful strengths such as:

- Strong OAuth implementation
- Proper JWT validation
- Secure TLS configuration
- Effective authorization
- Secure properties
- Appropriate rate limiting
- Strong input validation
- Controlled error responses
- Good API versioning

Do not create positive findings merely to make the report balanced.

---

# 78. API Security Quality Gate

Before completing the API security review, verify:

- All API entry points were identified.
- Authentication was assessed.
- Authorization was assessed.
- TLS was assessed.
- API policies were considered.
- Secrets were checked.
- Input validation was assessed.
- Sensitive data exposure was assessed.
- Error responses were assessed.
- Rate limiting was considered.
- Webhooks were assessed where applicable.
- Injection risks were assessed.
- CORS was assessed where relevant.
- Logging was assessed.
- External security dependencies were clearly identified.
- Infrastructure-dependent controls were not falsely reported as missing.
- Every finding has a concrete solution.
- Secrets were not copied into the report.

The final question is:

> Can an unauthorized or malicious caller reasonably access, manipulate, overload, or extract sensitive information from this API, and is there sufficient evidence to support the conclusion?
