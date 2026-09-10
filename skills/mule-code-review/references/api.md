# API Review Rules

## Purpose

Review MuleSoft API implementations for:

* contract alignment
* request validation
* response correctness
* HTTP methods
* status codes
* headers
* content types
* authentication
* authorization
* error contracts
* timeout behavior
* retry behavior
* idempotency
* backward compatibility
* RAML/OAS alignment

API findings must be based on an API contract or other repository
evidence that establishes the expected behavior.

Do not report an API concern merely because an alternative API design is
possible.

---

# Contract Sources

Where available, establish expected behavior from:

* RAML
* OpenAPI/OAS
* JSON/XML schemas
* API fragments
* examples
* MUnit tests
* integration tests
* documented response structures
* existing consumer-facing implementation
* API policies represented in the repository

If no authoritative contract is available, do not invent one.

Use the review limitation mechanism when contract visibility is
insufficient.

---

# API Review Principles

Before reporting an API finding:

1. Identify the API endpoint/resource.
2. Identify the applicable contract.
3. Inspect the Mule implementation.
4. Inspect request handling.
5. Inspect validation.
6. Inspect response construction.
7. Inspect status-code behavior.
8. Inspect headers and content types.
9. Inspect authentication and authorization.
10. Inspect error handling.
11. Inspect timeout/retry behavior.
12. Inspect idempotency for relevant operations.
13. Inspect affected tests.
14. Determine consumer impact.
15. Assign severity and confidence based on evidence.

Review implementation and contract together.

---

# API-001 — Implementation Does Not Align With Contract

## Description

The Mule implementation materially differs from the visible API contract
in a way that can cause incorrect client behavior.

Potential examples include:

* missing documented response fields
* incorrect request/response structure
* undocumented required fields
* incorrect parameter handling
* incorrect HTTP method
* incorrect content type
* documented behavior not implemented
* implementation accepting/rejecting data contrary to the contract

## Finding Gate

The affected contract must be visible in repository evidence.

The finding must identify:

* contract expectation
* implementation behavior
* material discrepancy
* consumer impact

Do not report differences based on assumptions about what the API
should do.

## Evidence Requirements

Identify:

* API specification
* endpoint/resource
* relevant contract element
* implementation location
* discrepancy
* affected consumer behavior

---

# API-002 — Incorrect Status Code Behavior

## Description

The implementation returns an HTTP status code that materially
misrepresents the outcome or violates the visible API contract.

Potential examples include:

* returning success for a failed operation
* returning the wrong client-error status
* returning a server-error status for a client validation failure
* returning an error status for a successful operation
* inconsistent status behavior across equivalent failure paths

## Finding Gate

The expected status behavior must be established by:

* RAML/OAS
* tests
* explicit application contract
* established implementation behavior

Do not impose a preferred status code without evidence.

## Evidence Requirements

Identify:

* endpoint
* triggering condition
* configured status code
* expected status code
* relevant contract/test evidence
* resulting client impact

## Impact Examples

Potential impacts include:

* clients misinterpreting failures
* incorrect retry behavior
* incorrect monitoring
* broken client workflows

---

# API-003 — Missing Validation

## Description

The API accepts input that the visible contract requires to be
validated, or fails to reject invalid input before it reaches an
operation where the invalid data creates a meaningful consequence.

Potential areas include:

* required fields
* field types
* allowed values
* string lengths
* numeric ranges
* formats
* structural validation
* mutually dependent fields
* path/query parameters

## Finding Gate

The validation requirement must be established by repository evidence.

Do not report missing validation merely because additional validation
could be desirable.

Consider whether:

* API gateway/policy validation exists
* schema validation occurs elsewhere
* downstream systems safely enforce the same constraint
* the application intentionally accepts a broader input model

## Evidence Requirements

Identify:

* endpoint
* input field/parameter
* contract requirement
* validation mechanism
* missing control
* resulting behavior

## Impact Examples

Potential impacts include:

* malformed downstream requests
* incorrect business processing
* avoidable downstream failures
* injection exposure where applicable
* inconsistent API behavior

---

# API-004 — Authentication/Authorization Concern

## Description

The API lacks, incorrectly applies, or can bypass an authentication
or authorization control required by the visible security model.

Potential examples include:

* protected endpoint without authentication
* authorization missing for a protected operation
* security control applied inconsistently
* authorization check that can be bypassed
* sensitive operation accessible to an inappropriate caller

## Finding Gate

The repository must establish that the resource requires the relevant
security control.

Authentication and authorization are separate controls.

Do not treat successful authentication as proof of authorization.

Also inspect API policies and external security configuration where
represented in the repository.

## Evidence Requirements

Identify:

* endpoint/operation
* security requirement
* configured control
* missing/ineffective control
* credible unauthorized access path

Do not report a concern solely because security configuration is not
visible in the Mule flow if it is demonstrably enforced elsewhere.

---

# API-005 — Breaking API Behavior

## Description

A change or implementation introduces behavior that breaks an existing
consumer-visible contract.

Potential examples include:

* removing a response field
* changing a field type
* changing a required field to a different semantic
* removing an endpoint
* changing HTTP method semantics
* changing status-code behavior
* changing error structure
* changing authentication requirements
* narrowing accepted input
* changing idempotency behavior in a consumer-impacting manner

## Finding Gate

A breaking-change finding requires evidence of the prior contract and
the new behavior.

For change reviews, inspect:

* changed files
* previous implementation where available
* API specification
* tests
* affected clients/consumers where visible

For full reviews, only report an existing compatibility defect when the
repository demonstrates the incompatible behavior.

Do not infer consumer impact without evidence.

## Evidence Requirements

Identify:

* prior contract/behavior
* current contract/behavior
* affected endpoint
* incompatible change
* likely or demonstrated consumer impact

---

# API-006 — Incorrect Error Contract

## Description

The API returns an error response that does not conform to its visible
error contract or provides materially inconsistent error behavior.

Potential examples include:

* wrong error response structure
* missing required error fields
* incorrect content type
* undocumented error payload
* inconsistent status/error-body combinations
* exposing internal implementation details where the contract requires a
  sanitized response

## Finding Gate

The expected error contract must be visible in:

* RAML/OAS
* schemas
* examples
* tests
* established API behavior

Do not invent an error schema.

## Evidence Requirements

Identify:

* endpoint
* failure condition
* documented error contract
* implementation response
* discrepancy
* client impact

---

# HTTP Method Review

Inspect whether methods align with the API contract and operation
semantics.

Consider:

* GET
* POST
* PUT
* PATCH
* DELETE
* safe operations
* idempotent operations

Do not report a method as incorrect solely because another HTTP method
could be used.

A finding requires contract or strong repository evidence.

---

# Request Validation

Consider validation of:

* headers
* query parameters
* path parameters
* request body
* content type
* required fields
* field formats
* ranges
* enumerations
* structural constraints

Determine where validation actually occurs before reporting a gap.

Validation may occur in:

* API policies
* APIkit/router behavior
* schema validation
* Mule processors
* reusable validation flows
* downstream controls

---

# Response Review

Inspect:

* response body
* response schema
* status code
* content type
* headers
* empty responses
* pagination metadata where applicable
* error responses

Confirm that the implementation returns behavior consistent with the
visible contract.

---

# Authentication and Authorization

Review:

* API policies
* client credentials
* OAuth configuration
* basic authentication where applicable
* JWT/token handling
* authorization scopes
* role checks
* object/resource authorization

Do not expose credentials, tokens, or secrets in findings.

Coordinate with the security reference for deeper security analysis.

If an API-specific issue is fundamentally a security vulnerability,
avoid creating duplicate findings unless the API contract impact and
security root cause materially differ.

---

# Timeout and Retry Behavior

For APIs invoking downstream systems, inspect:

* request timeout
* response timeout
* retry configuration
* connector retry behavior
* application-level retry
* downstream idempotency
* client retry interaction

Do not report the absence of retries as a defect by itself.

A finding requires evidence that timeout/retry behavior creates a
meaningful production or contract risk.

Consider the possibility of:

* duplicate operations
* excessive latency
* cascading failure
* downstream overload
* client retry amplification

---

# Idempotency

For operations with side effects, consider whether repeated requests
can create unintended duplicate effects.

Relevant operations may include:

* order creation
* payment processing
* record creation
* message publication
* external updates

Do not assume every POST must be idempotent.

Report an idempotency finding only when repository evidence establishes
that duplicate requests can create a meaningful production consequence
and no adequate control exists.

---

# Backward Compatibility

When assessing compatibility, consider:

* additive versus breaking changes
* required versus optional fields
* response field removal
* type changes
* enum restrictions
* status-code changes
* error schema changes
* authentication changes
* endpoint removal
* method changes
* behavior changes

For a compatibility finding, identify the affected contract and the
specific incompatible behavior.

---

# API and Downstream Integration

Trace important API paths into:

* DataWeave
* database operations
* messaging
* external HTTP services
* connectors
* asynchronous processing

Determine whether API-level behavior can produce:

* duplicate operations
* partial processing
* misleading success responses
* inconsistent state
* unhandled downstream failures

Do not duplicate findings when another domain already captures the same
root cause unless the API contract impact is materially distinct.

---

# Severity Guidance

Severity must reflect actual consumer and production impact.

### CRITICAL

Use only for catastrophic API/security consequences such as:

* severe authorization bypass
* widespread destructive behavior
* critical contract failure causing severe data loss/corruption

### HIGH

Use for:

* major breaking API behavior
* severe authentication/authorization weakness
* significant incorrect success/failure signaling
* major contract violations
* substantial consumer-impacting behavior

### MEDIUM

Use for:

* meaningful contract discrepancies
* realistic validation gaps
* incorrect status/error behavior with contained impact
* material idempotency or timeout risks

### LOW

Use for:

* limited consumer impact
* lower-priority contract or operational issues

### NIT

Use only for optional API improvements without material production
impact.

---

# False-Positive Controls

Do not create an API finding when:

* no authoritative contract is available
* the implementation behavior is explicitly allowed by the contract
* validation occurs in another verified component
* authentication/authorization is enforced by a verified external
  mechanism
* status-code behavior is contractually valid
* retry/timeout behavior has no demonstrated material consequence
* idempotency is not required by the operation
* a suspected compatibility issue has no visible prior/current
  contract evidence
* another component already mitigates the issue
* evidence is insufficient

When contract evidence is insufficient:

**Do not report the finding.**

Record the limitation where relevant.

---

# Positive API Indicators

Where supported by evidence, recognize strengths such as:

* clear RAML/OAS alignment
* appropriate request validation
* consistent status codes
* consistent error contracts
* appropriate authentication
* explicit authorization
* safe idempotency controls
* bounded timeout/retry behavior
* backward-compatible evolution
* useful API-level MUnit coverage

Positive observations must be evidence-backed.

---

# Required Finding Fields

Any API finding must include:

* Finding ID
* Severity
* Category
* Title
* File
* Location
* Confidence
* Problem
* Evidence
* Evidence Excerpt
* Impact
* Recommendation

Evidence excerpts must remain faithful to repository content.

Never include:

* passwords
* API keys
* client secrets
* access tokens
* private keys
* authorization headers
* secure property values
* sensitive payload values

Sanitize security-sensitive evidence before inclusion in the report.