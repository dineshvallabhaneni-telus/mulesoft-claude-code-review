# MuleSoft API Security Analysis Skill

## Purpose

Perform a comprehensive API security review of the MuleSoft application.

Review the application as a:

- Senior MuleSoft Architect
- API Security Architect
- Senior Technical Lead

The objective is to determine whether APIs are appropriately protected against:

- Unauthorized access
- Authentication failures
- Authorization failures
- Token misuse
- Credential exposure
- Transport-layer attacks
- Excessive access
- Missing policy enforcement
- Insecure headers
- Unsafe input handling
- API abuse
- Information leakage

Review both:

- API implementation
- API security configuration visible in the repository

Do not assume an API is secure merely because authentication exists.

Every meaningful finding MUST include:

- Evidence
- Impact
- Recommendation
- Practical solution

Do not report a security problem without providing a remediation approach.

Do not invent policies or gateway configuration that cannot be established from the repository.

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

Also inspect:

- RAML files
- OAS/OpenAPI files
- API specifications
- API configuration files
- HTTP Listener configuration
- APIkit configuration
- Security-related properties
- Policy-related configuration visible in the repository

---

# 4. API Discovery

Identify all API implementations.

Look for:

- HTTP Listener
- APIkit Router
- APIkit Console
- RAML
- OpenAPI
- OAS
- REST endpoints
- SOAP endpoints where applicable

Build an internal inventory:

| API | Resource | Method | Flow | Authentication | Authorization | TLS | Policies/Evidence | Assessment |
|---|---|---|---|---|---|---|---|---|

---

# 5. API Specification Review

Review RAML/OAS/API specifications for:

- Authentication requirements
- Authorization requirements
- Security schemes
- Sensitive operations
- Input constraints
- Required parameters
- Response definitions
- Error definitions

Determine whether the implementation appears aligned with the API contract.

Do not report specification style issues unless they affect security.

---

# 6. Public vs Protected APIs

Determine whether each API endpoint appears to require protection.

Classify endpoints as:

- Public
- Authenticated
- Authorized
- Internal
- Administrative
- Health/diagnostic
- Callback/webhook

Do not assume every endpoint must use identical security.

---

# 7. Authentication

Identify authentication mechanisms.

Examples:

- OAuth 2.0
- Client ID enforcement
- Client ID/Client Secret
- JWT
- Basic authentication
- Mutual TLS
- Custom authentication
- API gateway policies

Determine whether authentication is consistently applied to protected endpoints.

---

# 8. Missing Authentication

Report protected endpoints that appear accessible without authentication.

High-value examples:

- Customer data
- Orders
- Payments
- Administrative operations
- Data modification
- Internal integration endpoints

Do not report intentionally public endpoints.

---

# 9. Authentication Consistency

Compare equivalent endpoints.

Look for:

Endpoint A:

Authentication required

Endpoint B:

No authentication

when both appear to expose the same security boundary.

---

# 10. Authorization

Authentication proves identity.

Authorization determines what the authenticated caller may do.

Review whether authorization is addressed where business requirements require it.

Look for:

- Role-based access
- Scope-based access
- Permission checks
- Resource ownership checks
- Administrative privileges

Do not assume authentication alone provides authorization.

---

# 11. Missing Authorization

Identify sensitive operations where authenticated users may potentially perform actions without sufficient authorization.

Examples:

- Access another customer's data
- Modify another user's resources
- Administrative operations
- Privileged configuration
- Financial operations

If authorization is implemented outside the repository, state:

Verification Required

---

# 12. Object-Level Authorization

Review APIs accepting resource identifiers.

Examples:

GET /customers/{customerId}

GET /orders/{orderId}

Determine whether the implementation appears to verify that the caller is permitted to access the requested object.

This is particularly important for preventing:

- IDOR
- BOLA
- Unauthorized object access

Do not claim vulnerability without sufficient evidence.

---

# 13. Function-Level Authorization

Review administrative or privileged operations.

Examples:

- Delete
- Approve
- Cancel
- Update security settings
- Administrative operations

Determine whether elevated authorization appears to be enforced.

---

# 14. Scope Validation

If OAuth/JWT scopes are used, determine whether scopes appear to map appropriately to operations.

Examples:

read:customer

write:customer

admin:customer

Do not require a particular scope naming convention.

---

# 15. JWT Validation

If JWT is used, review visible configuration for:

- Signature validation
- Issuer validation
- Audience validation
- Expiration validation
- Required claims
- Algorithm restrictions

Do not claim a JWT vulnerability if validation is performed externally and cannot be seen.

Use:

Verification Required

---

# 16. Token Handling

Review whether tokens are:

- Logged
- Stored unnecessarily
- Passed insecurely
- Exposed in URLs
- Included in error responses

Never reproduce real token values.

Use:

[REDACTED]

---

# 17. Authorization Header Protection

Ensure the application does not log:

- Authorization
- Bearer tokens
- API keys
- Client secrets

Coordinate detailed logging findings with logging-analysis.

---

# 18. Client ID / Client Secret

Review usage of:

- Client ID
- Client Secret
- API key
- Application key

Determine whether secrets are:

- Securely stored
- Externalized
- Encrypted
- Properly referenced

Detailed secret handling belongs to security-analysis.

---

# 19. API Key Security

If API keys are used, determine whether they are:

- Validated
- Securely transmitted
- Stored securely
- Not exposed in logs

Do not report API key authentication as inherently insecure.

Evaluate whether it is appropriate for the API's risk profile.

---

# 20. Basic Authentication

If Basic authentication is used, determine whether:

- HTTPS is enforced
- Credentials are securely stored
- Credentials are not logged

Do not claim Basic authentication is automatically unacceptable.

Explain the risk and context.

---

# 21. Mutual TLS

Where mTLS is used, review:

- TLS configuration
- Client certificate validation
- Truststore
- Keystore
- Certificate management references

Do not expose certificate/private-key contents.

---

# 22. HTTPS Enforcement

Determine whether protected APIs use HTTPS.

Identify:

- HTTP listener
- HTTPS listener
- TLS configuration

If HTTP is intentionally used behind a trusted gateway/load balancer, state:

"Transport security at the external boundary requires verification."

Do not claim end-to-end HTTPS solely from application source.

---

# 23. TLS Configuration

Review visible TLS configuration for:

- Protocol versions
- Cipher configuration where present
- Truststore
- Keystore
- Certificate validation

Do not recommend weak/strong cipher lists without evidence and platform compatibility.

---

# 24. Certificate Handling

Review:

- Keystore references
- Truststore references
- Certificate locations
- Password handling

Determine whether certificates are:

- Externalized
- Properly protected
- Hard-coded
- Stored in source control

Coordinate credential findings with security-analysis.

---

# 25. API Gateway Policies

Look for evidence of policies such as:

- Client ID enforcement
- OAuth
- JWT validation
- Rate limiting
- Spike control
- IP allow/deny
- CORS
- Threat protection
- Header policies
- Message logging policies

Do not claim a policy is missing solely because it is not defined inside the application repository.

Use:

Verification Required

when policies are managed externally.

---

# 26. Rate Limiting

Determine whether public or sensitive APIs have protection against excessive requests.

Potential controls:

- Rate limiting
- SLA-based policies
- Spike control
- Quotas

Do not recommend rate limiting for every internal API automatically.

Consider:

- Exposure
- Business criticality
- Traffic pattern
- Downstream capacity

---

# 27. Denial-of-Service Protection

Review application-level controls against resource exhaustion.

Examples:

- Large request payloads
- Large query parameters
- Excessive page sizes
- Expensive operations
- Unbounded processing

Do not claim full DoS protection can be validated from application source.

---

# 28. Request Size Limits

Determine whether API requests have reasonable size limits where supported.

Pay particular attention to:

- File uploads
- Large JSON
- XML
- Multipart requests

Do not recommend arbitrary values without business requirements.

---

# 29. Response Size

Review whether APIs may return unnecessarily large datasets.

Consider:

- Pagination
- Maximum page size
- Filtering
- Field selection

Coordinate performance implications with performance-analysis.

---

# 30. Pagination

For collection APIs determine whether pagination is used where large result sets are possible.

Examples:

GET /customers

GET /orders

Do not require pagination for inherently small collections.

---

# 31. Input Validation

Review API input validation.

Look for:

- Required fields
- Data types
- Length
- Format
- Range
- Enumeration
- Business validation

Do not rely solely on DataWeave assumptions for externally supplied data.

---

# 32. Injection Risks

Review inputs used in:

- SQL
- Dynamic expressions
- URLs
- File paths
- Commands
- Scripts

Pay particular attention to dynamic SQL.

Recommend parameterized queries where applicable.

Do not report hypothetical injection without identifying a real data flow.

---

# 33. Dynamic SQL

Identify:

- String concatenation
- Dynamic SQL construction
- User-controlled query fragments

Determine whether parameters are safely bound.

This skill owns API-facing security implications; detailed database analysis may also be relevant to security-analysis.

---

# 34. Path Traversal

For APIs accepting file names or paths, determine whether user input could influence filesystem access.

Look for:

- `../`
- Dynamic file paths
- User-controlled directory names

Do not claim exploitability without a clear data flow.

---

# 35. SSRF

Review APIs that accept URLs or hostnames and then make outbound requests.

Determine whether user-controlled destinations are allowed.

Potential risks:

- Internal service access
- Metadata service access
- Private network access

Recommend:

- Allowlisting
- Destination validation
- Network controls

where applicable.

---

# 36. Open Redirect

Identify APIs that redirect users based on user-controlled URLs.

Determine whether destinations are validated.

---

# 37. CORS

Review CORS configuration where present.

Look for:

- Wildcard origins
- Credentialed requests
- Unnecessary methods
- Unnecessary headers

Do not report wildcard CORS automatically.

Consider whether the API is browser-facing.

---

# 38. Security Headers

Review relevant response headers where configurable.

Potential headers include:

- Strict-Transport-Security
- Content-Security-Policy
- X-Content-Type-Options
- Referrer-Policy

Do not require browser-oriented headers for APIs where they provide no meaningful value.

---

# 39. Error Information Disclosure

Review API error responses for:

- Stack traces
- Internal class names
- File paths
- Database errors
- Connection strings
- Internal hostnames
- Secrets

Errors should expose useful client information without revealing internal implementation details.

---

# 40. Exception Response Consistency

Review whether API errors have consistent structures.

Potential fields:

- code
- message
- correlationId
- timestamp
- details where safe

Do not expose internal stack traces.

---

# 41. Sensitive Data in Responses

Review whether APIs return unnecessary:

- Passwords
- Tokens
- Secrets
- Internal credentials
- Sensitive personal information

Report excessive exposure where evidence exists.

---

# 42. Sensitive Data in Requests

Determine whether sensitive information is transmitted appropriately.

Pay attention to:

- Passwords in query strings
- Tokens in URLs
- Sensitive information in GET parameters

Recommend secure alternatives where applicable.

---

# 43. API Logging Boundary

Review API logging for:

- Authentication headers
- Tokens
- Sensitive request bodies
- Sensitive response bodies

Coordinate detailed logging analysis with logging-analysis.

---

# 44. Health Endpoints

Identify:

- Health
- Readiness
- Liveness
- Diagnostic

endpoints.

Determine whether they expose sensitive information.

Health endpoints may intentionally be public/internal depending on architecture.

Do not automatically require authentication.

---

# 45. API Console

If APIkit Console or similar API documentation UI is enabled, determine whether it is exposed in production.

Consider:

- Internal-only access
- Authentication
- Disabled production access

Do not claim exposure without evidence.

---

# 46. API Documentation

Review whether API documentation reveals:

- Internal endpoints
- Credentials
- Internal hostnames
- Sensitive implementation details

Do not report normal API documentation as a security problem.

---

# 47. Webhooks

Identify webhook endpoints.

Review:

- Authentication
- Signature validation
- Replay protection
- Input validation
- Idempotency

If signature validation is external or not visible:

Verification Required

---

# 48. Replay Protection

For security-sensitive APIs/webhooks determine whether replay attacks are considered.

Potential mechanisms:

- Nonce
- Timestamp
- Idempotency key
- Signature
- Token expiration

Do not require replay protection for every endpoint.

---

# 49. Idempotency

For POST/payment/order/transaction operations, determine whether idempotency is addressed where retries or duplicate requests could cause business impact.

Do not claim missing idempotency without understanding business behavior.

---

# 50. HTTP Methods

Review whether endpoints use appropriate methods.

Examples:

- GET for retrieval
- POST for creation/actions
- PUT/PATCH for updates
- DELETE for deletion

Do not classify non-standard method usage as a security issue automatically.

---

# 51. HTTP Method Restrictions

Determine whether endpoints unexpectedly accept methods they do not need.

Potentially unnecessary:

- PUT
- DELETE
- PATCH

Only report when this increases actual security or functional risk.

---

# 52. API Versioning

Review API versioning where multiple API versions exist.

Look for:

- Inconsistent security
- Old unsecured versions
- Deprecated endpoints still exposed

Do not report versioning style as a security problem unless security is affected.

---

# 53. Deprecated API Security

Identify older API versions that may not receive the same security controls as current versions.

Recommend:

- Deprecation
- Retirement
- Consistent security policies

---

# 54. Internal API Exposure

Identify APIs that appear intended for internal use.

Review whether they are accidentally exposed through:

- Public HTTP listeners
- External gateways
- Missing authentication

Do not claim public exposure without infrastructure evidence.

---

# 55. Administrative APIs

Identify administrative operations.

These should generally have stronger controls.

Examples:

- Configuration changes
- User administration
- Data deletion
- Replay operations
- Operational controls

---

# 56. Security Configuration Consistency

Compare equivalent APIs.

Look for inconsistent:

- Authentication
- Authorization
- TLS
- Policies
- Rate limits
- Input validation

---

# 57. Environment Security Consistency

Compare:

- DEV
- QA
- UAT
- PROD

Determine whether production has stronger security controls where appropriate.

Do not assume development must have identical security behavior.

---

# 58. API Security Finding Format

Every finding MUST contain:

## Finding ID

Example:

MULE-APISEC-001

## Title

Concise security issue.

## Severity

Critical / High / Medium / Low / Warning

## Category

API Security

## API

API name or endpoint.

## Location

File, flow, configuration, or specification.

## Evidence

Observed implementation.

## Risk

Explain the realistic security impact.

## Recommendation

What should change.

## Solution

Provide concrete MuleSoft/API security implementation guidance.

## Verification

If infrastructure or gateway configuration must be checked.

## Priority

Immediate / Short Term / Medium Term / Long Term

---

# 59. Severity Guidelines

## Critical

Potential for:

- Unauthenticated access to highly sensitive functionality
- Credential compromise
- Severe data exposure
- Remote compromise through an identifiable security path

## High

Significant unauthorized access, data exposure, or security control failure.

## Medium

Meaningful security weakness with limited or conditional impact.

## Low

Minor security improvement.

## Warning

Potential weakness requiring environment/business verification.

Do not inflate severity.

---

# 60. Security Evidence Rules

Every security finding must identify the evidence.

Example:

"HTTP Listener `customer-api-listener` exposes `/customers/{id}` and no authentication configuration is visible in the application."

Do not state:

"API is insecure."

without evidence.

---

# 61. External Gateway Verification

If API security policies are managed outside the repository, clearly distinguish:

Repository Evidence

from:

Infrastructure Verification Required

Example:

"Application source does not show authentication enforcement. Verify whether API Manager/Gateway applies an authentication policy before deployment."

Do not automatically classify this as a confirmed vulnerability.

---

# 62. Positive API Security Observations

Identify good practices such as:

- Authentication enforced
- Authorization checks
- Secure TLS
- Secure secret references
- Input validation
- Rate limiting
- Secure error responses
- API policies
- Strong webhook validation
- Idempotency controls
- Secure CORS configuration

---

# 63. Cross-Skill Boundaries

Detailed findings owned by these skills should not be duplicated unnecessarily:

- mulesoft-architecture
- mule-code-quality
- connector-analysis
- security-analysis
- performance-analysis
- munit-analysis
- configuration-analysis
- logging-analysis
- duplication-analysis
- word-report-generation

This skill owns API-specific security.

If a password is stored in plain text:

- api-security-analysis identifies the API security exposure.
- security-analysis owns the detailed secret/password remediation.

If a token is logged:

- api-security-analysis identifies the API security risk.
- logging-analysis owns the detailed logging remediation.

If TLS configuration is incorrect:

- api-security-analysis identifies API transport implications.
- connector-analysis/security-analysis owns detailed TLS configuration.

The final report reviewer must consolidate duplicate root causes.

---

# 64. No Unsupported Claims

Never claim:

- An API is public without infrastructure evidence.
- Gateway policies are absent merely because they are not in the repository.
- JWT validation is missing when it may be externally enforced.
- CORS is insecure without considering browser usage.
- Rate limiting is mandatory for every endpoint.
- Authorization is missing without considering external enforcement.

Use:

Verification Required

where appropriate.

---

# 65. API Security Score

Provide an API security score based on:

- Authentication
- Authorization
- Transport security
- Token handling
- Input validation
- Error handling
- Sensitive-data protection
- API policy coverage
- Rate limiting
- Webhook security
- Security consistency

Do not calculate the score solely from finding count.

---

# 66. Final Output

Return structured API security analysis containing:

## API Security Summary

## API Inventory

## Authentication Assessment

## Authorization Assessment

## JWT/OAuth Assessment

## API Key/Client ID Assessment

## TLS Assessment

## API Policy Assessment

## Rate Limiting Assessment

## Input Validation Assessment

## Injection Assessment

## CORS Assessment

## Error Disclosure Assessment

## Sensitive Data Exposure Assessment

## Webhook Assessment

## Idempotency Assessment

## Health/Diagnostic Endpoint Assessment

## API Security Findings

## Recommended API Security Improvements

## Positive Security Practices

## Infrastructure Verification Required

## API Security Score

Do not generate the final Word document from this skill.

The word-report-generation skill is responsible for creating the final .docx.

---

# 67. Quality Standard

Before completing the review, ask:

"Would an API Security Architect consider these findings credible, evidence-based, and actionable?"

If not:

- Remove speculative findings.
- Identify the exact API and security boundary.
- Distinguish application controls from gateway controls.
- Avoid claiming external controls are absent without evidence.
- Provide concrete MuleSoft/API security solutions.
- Prioritize realistic attack paths and sensitive operations.

The objective is production-quality API security analysis, not a generic OWASP checklist.