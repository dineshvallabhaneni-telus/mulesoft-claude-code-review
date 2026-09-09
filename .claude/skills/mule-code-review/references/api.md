# MuleSoft API Review Rules

## Purpose

These rules define how MuleSoft APIs must be reviewed.

Review APIs in the context of:

- RAML
- OAS/OpenAPI
- APIkit
- HTTP Listener
- HTTP Request
- Mule flows
- DataWeave
- authentication
- authorization
- request validation
- response contracts
- error contracts
- status codes
- headers
- timeouts
- retries
- idempotency
- pagination
- versioning
- backward compatibility
- downstream integrations

Do not review an API implementation independently from its API contract.

When RAML/OAS is available, compare:

1. API specification
2. Mule implementation
3. DataWeave transformations
4. HTTP configuration
5. tests

---

# API Review Principles

Before reporting an API finding:

1. Identify the API endpoint.
2. Identify the API specification.
3. Identify the Mule flow implementing the endpoint.
4. Compare request contract with implementation.
5. Compare response contract with implementation.
6. Inspect authentication and authorization.
7. Inspect error handling.
8. Inspect timeout and retry behavior.
9. Inspect downstream dependencies.
10. Determine backward compatibility.
11. Determine realistic client/business impact.

Do not report a contract violation when the specification itself is
missing or ambiguous unless repository evidence establishes the expected
behavior.

---

# API-001 — Breaking API Change

## Rule

Flag incompatible changes to an existing API contract.

Consider:

- removing endpoints
- changing HTTP methods
- removing required fields
- changing field types
- changing response structures
- changing URI paths
- changing required query parameters
- changing authentication requirements
- changing error contracts
- changing semantics of existing fields

## Severity

HIGH

Escalate to CRITICAL when a change can cause widespread production
client failures or security regression.

---

# API-002 — Incorrect HTTP Method

## Rule

Flag implementation using an HTTP method that does not match the API
contract or intended resource semantics.

Consider:

- GET
- POST
- PUT
- PATCH
- DELETE

## Severity

HIGH

---

# API-003 — Incorrect HTTP Status

## Rule

Flag API responses using inappropriate HTTP status codes for the
documented or established API contract.

Consider:

- successful responses
- validation failures
- authentication failures
- authorization failures
- not found
- conflicts
- rate limiting
- downstream failures
- server errors

## Severity

HIGH

Do not prescribe a status code based solely on personal preference.

---

# API-004 — Missing Request Validation

## Rule

Flag missing validation for required:

- request fields
- query parameters
- URI parameters
- headers
- content types
- formats
- business constraints

when the API contract or implementation requires validation.

## Severity

MEDIUM

Escalate when missing validation can cause:

- data corruption
- security vulnerabilities
- downstream failures
- significant business errors

---

# API-005 — Incorrect Response Schema

## Rule

Flag responses that do not match the documented API schema.

Consider:

- missing required fields
- incorrect field names
- incorrect field types
- incorrect nesting
- unexpected structure
- invalid arrays
- incorrect null handling

## Severity

HIGH

---

# API-006 — Authentication Regression

## Rule

Flag an API change that weakens or removes an existing authentication
control.

Examples:

- protected endpoint becomes unauthenticated
- authentication validation is bypassed
- alternate route bypasses authentication
- authentication is applied only to some execution paths

## Severity

CRITICAL / HIGH

Use CRITICAL when unauthorized access to sensitive functionality is
credible.

---

# API-007 — Authorization Regression

## Rule

Flag API changes that weaken or bypass authorization controls.

Consider:

- role checks
- scopes
- resource ownership
- tenant isolation
- account boundaries
- object-level authorization

## Severity

CRITICAL / HIGH

Use CRITICAL when unauthorized users can access or modify sensitive
resources.

---

# API-008 — Missing Timeout

## Rule

Flag external HTTP operations without an appropriate timeout strategy.

Consider:

- connection timeout
- response/read timeout
- request timeout
- downstream service behavior

## Severity

MEDIUM

Escalate when missing timeout behavior can cause:

- thread exhaustion
- worker saturation
- cascading failures
- severe latency

---

# API-009 — Unsafe Retry

## Rule

Flag HTTP retries where the operation is not safely idempotent or where
retry behavior can create duplicate business effects.

Consider:

- POST
- PUT
- PATCH
- DELETE
- downstream side effects
- payment/order operations
- message publication

## Severity

HIGH

Do not assume GET is always safe to retry if the implementation causes
side effects.

---

# API-010 — Incorrect Content Type

## Rule

Flag incorrect or inconsistent request/response content types.

Consider:

- `application/json`
- `application/xml`
- `text/csv`
- `multipart/form-data`
- binary content
- vendor-specific media types

## Severity

MEDIUM

Escalate when clients cannot correctly consume the response.

---

# API-011 — Sensitive Headers Exposed

## Rule

Flag APIs that expose or unnecessarily return sensitive headers such as:

- Authorization
- proxy authorization
- session credentials
- internal security headers
- downstream authentication information

## Severity

HIGH

Escalate to CRITICAL when credentials or tokens are exposed.

---

# API-012 — Error Contract Inconsistency

## Rule

Flag inconsistent error responses across equivalent API operations when
an established error contract exists.

Consider:

- response structure
- error codes
- messages
- correlation IDs
- HTTP status
- validation errors
- downstream failures

## Severity

MEDIUM

Escalate when clients can reasonably misinterpret the response.

---

# API-013 — Missing API Versioning Strategy

## Rule

Flag incompatible API changes where no appropriate versioning or
migration strategy exists.

Consider:

- URI versioning
- header/media-type versioning
- API Manager policies
- documented compatibility strategy

## Severity

MEDIUM

Do not require versioning for every API.

Apply when the API has established consumers or breaking changes are
otherwise likely.

---

# API-014 — Incorrect Path Parameter Handling

## Rule

Flag URI/path parameter handling that can cause:

- incorrect resource selection
- missing validation
- authorization bypass
- injection
- unexpected downstream behavior

## Severity

HIGH

---

# API-015 — Incorrect Query Parameter Handling

## Rule

Flag query parameter handling that can cause:

- incorrect filtering
- unexpected defaults
- injection
- excessive resource consumption
- incorrect pagination
- security boundary violations

## Severity

MEDIUM

Escalate when security or data-access controls are affected.

---

# API-016 — Missing Pagination

## Rule

Flag APIs that return potentially unbounded collections without an
appropriate pagination strategy when large result sets are realistic.

Consider:

- page size
- maximum page size
- cursor-based pagination
- offset pagination
- total counts
- continuation links

## Severity

MEDIUM

Escalate when unbounded responses can cause memory, latency, or
availability problems.

Do not require pagination for inherently small or bounded collections.

---

# API-017 — Unsafe Pagination Limits

## Rule

Flag pagination implementations that allow clients to request
unreasonably large result sets without appropriate limits.

## Severity

MEDIUM

Escalate when this can realistically cause resource exhaustion.

---

# API-018 — Incorrect Idempotency Behavior

## Rule

Flag APIs performing business side effects where repeated requests can
create duplicate processing and no appropriate idempotency mechanism
exists when one is required.

Consider:

- order creation
- payment processing
- message publication
- external updates
- file creation

## Severity

HIGH

---

# API-019 — Missing Idempotency Support

## Rule

Flag operations where network retries, client retries, or gateway
retries can realistically produce duplicate business effects and the
API architecture provides no appropriate way to prevent or detect
duplicates.

## Severity

HIGH

Do not require idempotency for operations where duplicate execution is
explicitly safe.

---

# API-020 — Incorrect Conditional Request Handling

## Rule

When the API supports conditional requests, flag incorrect handling of:

- ETag
- If-Match
- If-None-Match
- If-Modified-Since
- related concurrency controls

when it can cause stale updates or incorrect caching behavior.

## Severity

MEDIUM

---

# API-021 — Missing Concurrency Protection

## Rule

Flag APIs performing updates where concurrent requests can overwrite
each other's changes and no appropriate concurrency strategy exists when
the business process requires protection.

Consider:

- optimistic locking
- version fields
- ETags
- database locking
- conflict detection

## Severity

HIGH

Only report when concurrent updates are a realistic business scenario.

---

# API-022 — Incorrect Authentication Header Handling

## Rule

Flag APIs that:

- fail to validate required authentication headers
- forward authentication headers unnecessarily
- overwrite authentication headers incorrectly
- expose authentication headers in responses or logs

## Severity

HIGH

Escalate when credentials or tokens are exposed.

---

# API-023 — Missing Correlation Information

## Rule

Flag APIs where the established application architecture requires
correlation information but the API does not:

- accept it
- generate it
- propagate it
- return it where appropriate

## Severity

LOW

Escalate to MEDIUM when the absence materially affects production
diagnostics.

Do not require a specific correlation mechanism unless the application
uses one.

---

# API-024 — Incorrect Header Propagation

## Rule

Flag unnecessary or unsafe propagation of inbound headers to downstream
systems.

Consider:

- Authorization
- cookies
- internal headers
- tracing headers
- client-controlled headers
- security-sensitive headers

## Severity

HIGH

---

# API-025 — Missing Response Header Controls

## Rule

Flag missing security-relevant response headers when the API's exposure
model makes them necessary.

Consider:

- security headers
- caching controls
- content type
- content disposition
- browser-related security controls

## Severity

LOW / MEDIUM

Do not require a fixed header set for every API.

---

# API-026 — Incorrect Cache-Control Behavior

## Rule

Flag API responses that can incorrectly cache sensitive or user-specific
data.

Consider:

- authentication context
- PII
- financial data
- authorization scope
- shared proxies
- browser caches

## Severity

HIGH

---

# API-027 — Unsafe CORS Configuration

## Rule

Flag overly permissive CORS configuration for browser-accessible APIs
when it creates a realistic security risk.

Consider:

- wildcard origins
- credentialed requests
- unrestricted methods
- unrestricted headers

## Severity

MEDIUM

Escalate when sensitive authenticated operations are exposed.

Do not apply when CORS is not relevant to the API.

---

# API-028 — Missing Rate Limiting / Abuse Protection

## Rule

Flag externally accessible sensitive or resource-intensive operations
when uncontrolled request volume creates a realistic abuse or
availability risk.

Consider:

- authentication endpoints
- expensive searches
- large file processing
- bulk operations
- expensive downstream integrations

## Severity

MEDIUM

Do not require rate limiting for every API.

---

# API-029 — Unbounded Request Size

## Rule

Flag APIs that accept potentially large payloads without appropriate
limits when large requests can cause:

- memory exhaustion
- worker saturation
- excessive processing
- downstream failures

## Severity

MEDIUM

Escalate when resource exhaustion is realistically exploitable.

---

# API-030 — Missing Content Negotiation Handling

## Rule

Flag APIs that advertise or accept multiple representations but the
implementation does not correctly handle the declared media types.

Consider:

- `Accept`
- `Content-Type`
- vendor media types
- JSON/XML alternatives

## Severity

MEDIUM

---

# API-031 — Incorrect Optional/Required Field Semantics

## Rule

Flag mismatch between API specification and implementation regarding:

- required fields
- optional fields
- nullable fields
- default values

## Severity

MEDIUM

Escalate when the mismatch causes client failures or data corruption.

---

# API-032 — Incorrect Default Value

## Rule

Flag implementation defaults that differ from the API contract or change
business behavior unexpectedly.

Consider:

- query parameter defaults
- request fields
- pagination
- filtering
- sorting

## Severity

MEDIUM

---

# API-033 — Incorrect API Parameter Type

## Rule

Flag mismatch between API specification and implementation for:

- string
- integer
- number
- boolean
- date
- date-time
- arrays
- objects

## Severity

MEDIUM

Escalate when clients can send valid contract-compliant requests that
the implementation incorrectly rejects or processes.

---

# API-034 — Incorrect API Error Mapping

## Rule

Flag API error handling that maps internal Mule or connector errors to
incorrect external API responses.

Consider:

- downstream 4xx
- downstream 5xx
- timeout
- database failure
- validation failure
- authentication failure

## Severity

HIGH

---

# API-035 — Internal Error Exposure

## Rule

Flag API responses exposing:

- stack traces
- SQL
- internal hostnames
- internal URLs
- filesystem paths
- connector details
- implementation details

## Severity

HIGH

Escalate when credentials or security-sensitive information are exposed.

---

# API-036 — Downstream Error Leaked Directly

## Rule

Flag APIs that expose raw downstream error responses without validating
that the response is safe and compatible with the API's public contract.

## Severity

HIGH

---

# API-037 — Downstream Timeout Propagation

## Rule

Flag API flows where downstream timeout behavior can cause the client
request to remain blocked for an excessive or uncontrolled duration.

Consider:

- HTTP Request timeout
- connection timeout
- retry duration
- nested retries
- upstream gateway timeout

## Severity

MEDIUM

Escalate when thread/worker exhaustion is realistic.

---

# API-038 — Retry Amplification

## Rule

Flag API designs where retries can occur at multiple layers and multiply
the number of downstream requests.

Consider:

- client retry
- API gateway retry
- Mule retry
- connector retry
- downstream retry

## Severity

HIGH

Potential consequences include:

- duplicate processing
- retry storms
- excessive downstream load
- severe latency

---

# API-039 — Synchronous Dependency Risk

## Rule

Flag synchronous API flows that depend on slow or unreliable downstream
systems when the resulting availability coupling creates a realistic
production risk.

## Severity

MEDIUM

Escalate when a downstream outage can make the entire API unavailable
without an appropriate fallback strategy.

Do not prescribe asynchronous processing solely as an architectural
preference.

---

# API-040 — Missing Downstream Failure Handling

## Rule

Flag API flows that do not appropriately handle realistic downstream:

- timeout
- connection failure
- 4xx
- 5xx
- rate limiting
- authentication failure

## Severity

HIGH

---

# API-041 — Incorrect API Security Policy Assumption

## Rule

Flag implementations that assume authentication or authorization is
provided by an external API gateway/policy when repository evidence
shows that the application itself must enforce the control.

## Severity

HIGH

Do not report when the repository clearly establishes the external
security boundary.

---

# API-042 — Security Control Bypass Through Alternate Endpoint

## Rule

Flag alternate routes, legacy endpoints, administrative endpoints,
fallback flows, or error routes that expose functionality without the
security controls applied to the primary endpoint.

## Severity

CRITICAL

---

# API-043 — HTTP Method Override Risk

## Rule

Flag support for method override mechanisms when untrusted clients can
use them to bypass security or authorization assumptions.

## Severity

HIGH

Only apply when method override behavior is actually present.

---

# API-044 — Mass Assignment / Uncontrolled Field Mapping

## Rule

Flag APIs that map client-supplied fields directly into sensitive domain
or persistence objects when clients can modify fields they should not
control.

Consider:

- ownership fields
- account IDs
- tenant IDs
- status
- approval flags
- privilege fields
- internal identifiers

## Severity

HIGH

Escalate to CRITICAL when this enables privilege escalation or
unauthorized data modification.

---

# API-045 — Unsafe Resource Identifier Handling

## Rule

Flag APIs that trust client-supplied resource identifiers without
appropriate validation and authorization.

Examples:

- customer ID
- account ID
- order ID
- file ID
- tenant ID

## Severity

HIGH

Escalate to CRITICAL when this creates cross-user or cross-tenant access.

---

# API-046 — Incorrect API Version Compatibility

## Rule

Flag implementation behavior that is incompatible with the API version
declared by the specification or deployment configuration.

Consider:

- base paths
- version headers
- API Manager configuration
- RAML/OAS version
- flow routing

## Severity

MEDIUM

---

# API-047 — API Specification / Implementation Drift

## Rule

Flag meaningful differences between RAML/OAS and Mule implementation.

Consider:

- endpoints
- methods
- parameters
- request bodies
- responses
- status codes
- schemas
- security requirements

## Severity

HIGH

---

# API-048 — Undocumented Endpoint

## Rule

Flag externally accessible endpoints implemented in Mule that are not
represented in the authoritative API specification when the application
uses a formal API contract.

## Severity

MEDIUM

Escalate when the undocumented endpoint exposes sensitive functionality.

---

# API-049 — Unused Contract Endpoint

## Rule

Flag API specification endpoints that appear to have no corresponding
implementation when the specification is expected to represent deployed
functionality.

## Severity

LOW

Escalate when clients can reasonably depend on the missing endpoint.

---

# API-050 — Inconsistent Resource Semantics

## Rule

Flag related API endpoints that use materially inconsistent semantics
for equivalent operations.

Examples:

- inconsistent status codes
- inconsistent filtering behavior
- inconsistent pagination
- inconsistent field naming
- inconsistent error structures

## Severity

MEDIUM

---

# API-051 — Unsafe Bulk Operation

## Rule

Flag bulk APIs that can process large numbers of records without
appropriate controls for:

- payload size
- processing limits
- timeout
- partial failure
- idempotency
- resource consumption

## Severity

HIGH

---

# API-052 — Incorrect Partial Success Contract

## Rule

Flag bulk or multi-record APIs where some records can succeed and others
fail but the API contract does not clearly represent the outcome.

## Severity

HIGH

---

# API-053 — Missing API Deprecation Strategy

## Rule

Flag removal or retirement of an API contract without evidence of an
appropriate deprecation or migration strategy when existing consumers
are likely.

## Severity

MEDIUM

---

# API-054 — Incorrect HEAD/OPTIONS Handling

## Rule

Where HEAD or OPTIONS is supported or required, flag implementation that
returns incorrect behavior or exposes unintended information.

## Severity

LOW / MEDIUM

Only apply when these methods are relevant to the API.

---

# API-055 — Unsafe File Upload Handling

## Rule

For APIs accepting files, review:

- file size
- file type
- content validation
- filename handling
- path handling
- storage behavior
- malware/security controls where applicable
- downstream processing

Flag realistic security or availability risks.

## Severity

HIGH

---

# API-056 — Missing Request Size or Processing Limits

## Rule

Flag endpoints performing expensive processing without reasonable
limits on:

- request size
- collection size
- batch size
- recursion/depth
- processing duration

when uncontrolled input can cause resource exhaustion.

## Severity

MEDIUM

---

# API-057 — Incorrect HTTP Header Case/Value Semantics

## Rule

Flag implementation assumptions about HTTP headers that can cause
incorrect behavior due to:

- case handling
- multiple values
- whitespace
- encoding
- client-controlled values

## Severity

LOW / MEDIUM

Only report when the behavior affects correctness or security.

---

# API-058 — Missing API Observability

## Rule

Flag APIs where established project observability requires information
such as:

- correlation ID
- request ID
- endpoint
- outcome
- latency
- downstream failure

but the API implementation does not provide sufficient diagnostic
information.

## Severity

LOW

Escalate to MEDIUM when production support is materially affected.

---

# API-059 — Excessive API Logging

## Rule

Flag API logging that unnecessarily records:

- complete request payloads
- complete response payloads
- sensitive headers
- large binary content

when the logging provides limited diagnostic value.

## Severity

MEDIUM

Escalate when sensitive information is exposed.

---

# API-060 — Incorrect API Contract for Null Values

## Rule

Flag mismatch between the API specification and implementation regarding
nullability and missing values.

Consider:

- omitted fields
- explicit null
- empty string
- empty array
- empty object

## Severity

MEDIUM

---

# API-061 — Incorrect API Encoding

## Rule

Flag incorrect character encoding or content encoding behavior that can
corrupt API data.

Consider:

- UTF-8
- XML encoding
- URL encoding
- Base64
- compressed content

## Severity

MEDIUM

---

# API-062 — Incorrect Caching of Sensitive Responses

## Rule

Flag cacheable API responses containing sensitive or user-specific data
when caching could expose one user's data to another user.

## Severity

HIGH

---

# API-063 — Missing Conflict Handling

## Rule

Flag APIs performing create/update operations where conflicts are a
realistic scenario but the implementation has no appropriate conflict
handling.

Consider:

- duplicate identifiers
- concurrent updates
- unique constraints
- idempotency conflicts

## Severity

MEDIUM

---

# API-064 — Incorrect Authentication Error Semantics

## Rule

Flag authentication failures that return success responses or otherwise
misrepresent authentication state.

## Severity

HIGH

---

# API-065 — Incorrect Authorization Error Semantics

## Rule

Flag authorization failures that are incorrectly represented as
successful operations or expose information about protected resources.

## Severity

HIGH

---

# API-066 — Sensitive Resource Enumeration

## Rule

Flag APIs where response differences allow unauthenticated or
unauthorized callers to reliably determine the existence of protected
resources.

Consider:

- customer IDs
- account IDs
- order IDs
- usernames
- files
- internal records

## Severity

HIGH

---

# API-067 — Missing API Input Normalization

## Rule

Flag security-sensitive or business-critical inputs where inconsistent
normalization can cause validation, authorization, or routing bypasses.

Consider:

- whitespace
- case
- Unicode
- encoding
- duplicate parameters

## Severity

MEDIUM

---

# API-068 — Duplicate Parameter Ambiguity

## Rule

Flag APIs that behave unpredictably when clients submit duplicate query,
header, or form parameters and different layers may interpret them
differently.

## Severity

MEDIUM

Only apply when the repository shows such inputs can affect security or
business behavior.

---

# API-069 — Untrusted Forwarding of Query Parameters

## Rule

Flag forwarding of client-controlled query parameters to downstream
systems when those parameters can alter:

- authorization
- filtering
- resource selection
- administrative behavior
- downstream security controls

## Severity

HIGH

---

# API-070 — Incorrect API Response on Downstream Success Ambiguity

## Rule

Flag APIs that report success when the downstream operation's final
outcome is uncertain.

Examples:

- timeout after a non-idempotent write
- connection failure after request transmission
- asynchronous operation treated as synchronous success

## Severity

HIGH

---

# API Contract Review Matrix

For each important endpoint, evaluate:

| Area | Specification | Implementation | Result |
|---|---|---|---|
| Method | Inspect | Inspect | Match / Mismatch |
| Path | Inspect | Inspect | Match / Mismatch |
| Authentication | Inspect | Inspect | Match / Mismatch |
| Authorization | Inspect | Inspect | Match / Mismatch |
| Parameters | Inspect | Inspect | Match / Mismatch |
| Request schema | Inspect | Inspect | Match / Mismatch |
| Response schema | Inspect | Inspect | Match / Mismatch |
| Status codes | Inspect | Inspect | Match / Mismatch |
| Error contract | Inspect | Inspect | Match / Mismatch |
| Content type | Inspect | Inspect | Match / Mismatch |
| Timeout | Inspect | Inspect | Appropriate / Risk |
| Retry | Inspect | Inspect | Safe / Risk |
| Idempotency | Inspect | Inspect | Appropriate / Risk |
| Pagination | Inspect | Inspect | Appropriate / Risk |
| Versioning | Inspect | Inspect | Appropriate / Risk |

---

# API Review by Endpoint Type

## GET

Review:

- authorization
- filtering
- pagination
- caching
- resource enumeration
- response size
- query parameters

## POST

Review:

- validation
- idempotency
- duplicate creation
- authorization
- retry behavior
- response status

## PUT

Review:

- idempotency
- full replacement semantics
- concurrency
- authorization
- retry behavior

## PATCH

Review:

- partial update semantics
- field authorization
- validation
- concurrency
- idempotency

## DELETE

Review:

- authorization
- idempotency
- resource existence
- cascading effects
- retry behavior

---

# API Finding Validation

Before reporting an API finding:

1. Identify the endpoint.
2. Inspect RAML/OAS when available.
3. Inspect the Mule implementation.
4. Inspect DataWeave request/response mappings.
5. Inspect authentication.
6. Inspect authorization.
7. Inspect error handling.
8. Inspect downstream calls.
9. Inspect timeout and retry behavior.
10. Inspect tests.
11. Determine compatibility impact.
12. Determine realistic business impact.
13. Confirm severity.

If the issue cannot be substantiated, do not report it.

---

# API Severity Guidance

## CRITICAL

Use for:

- authentication bypass
- authorization bypass
- cross-tenant access
- severe sensitive-data exposure
- critical API injection
- protected resource access without authorization

## HIGH

Use for:

- breaking API changes
- incorrect response contracts
- unsafe retries
- idempotency failures
- significant validation gaps
- sensitive information exposure
- major downstream failure problems

## MEDIUM

Use for:

- meaningful contract inconsistencies
- missing pagination
- timeout concerns
- moderate resilience issues
- observability gaps
- configuration weaknesses

## LOW

Use for:

- minor contract improvements
- limited documentation/consistency problems
- low-impact operational improvements

## NIT

Only report when the improvement provides meaningful value.

---

# API False-Positive Controls

Do not report:

- API versioning as mandatory for every API
- pagination for inherently bounded collections
- rate limiting for every endpoint
- asynchronous processing solely as an architectural preference
- CORS when the API is not browser-accessible
- idempotency when duplicate execution is demonstrably safe
- authentication/authorization controls already enforced by a verified
  external security boundary

without repository evidence.

---

# API Finding Format

Use:

**Finding ID:** API-001

**Severity:** HIGH

**Category:** API

**File:** `src/main/mule/api.xml:125`

**Location:** `GET /orders/{id}`

**Problem:**

Describe the API problem.

**Evidence:**

Identify the API specification and implementation evidence.

**Contract Impact:**

Explain how the implementation differs from the documented contract.

**Technical Mechanism:**

Explain how the behavior occurs.

**Impact:**

Explain realistic client, business, security, or production impact.

**Recommendation:**

Provide an actionable remediation.

**Confidence:** HIGH / MEDIUM / LOW