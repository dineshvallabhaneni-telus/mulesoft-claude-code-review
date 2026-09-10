# Error Handling Review Rules

## Purpose

Review Mule 4 error handling for:

* correctness
* error propagation
* failure isolation
* retry safety
* transaction behavior
* root-cause preservation
* HTTP response correctness
* operational diagnosability
* security of error responses

The review must consider actual Mule 4 error semantics and the
relationship between flows, scopes, connectors, transactions, and error
handlers.

Error-handling patterns are not findings merely because another pattern
could be used.

---

# Review Areas

Inspect, where applicable:

* error types
* error hierarchy
* `on-error-propagate`
* `on-error-continue`
* Try scopes
* flow-level error handlers
* global error handlers
* error mapping
* error type matching
* retry scopes
* reconnection
* connector retry behavior
* transaction interaction
* transaction rollback
* HTTP response handling
* HTTP error responses
* error payloads
* error attributes
* root-cause preservation
* logging of failures
* sensitive information exposure
* downstream failure handling
* asynchronous failure handling

Trace errors across flow boundaries rather than reviewing handlers in
isolation.

---

# Error Handling Principles

Before reporting an error-handling finding:

1. Identify the operation that can fail.
2. Identify its error type or error family where possible.
3. Trace the applicable error handler.
4. Determine whether the handler is local, scoped, flow-level, or global.
5. Determine whether the error is propagated or continued.
6. Inspect retry and reconnection behavior.
7. Inspect transaction boundaries where applicable.
8. Inspect HTTP response behavior where applicable.
9. Determine whether the root cause remains diagnosable.
10. Check for compensating controls.
11. Determine actual production impact.
12. Assign severity and confidence based on evidence.

Do not infer error behavior solely from the existence of an error
handler.

---

# ERR-001 — Error Swallowed

## Description

An error is caught or handled in a way that prevents the appropriate
failure signal from reaching the caller, transaction boundary, message
processing mechanism, or operational monitoring.

Typical mechanisms include inappropriate use of:

* `on-error-continue`
* broad error handlers
* conditional error handling
* logging without propagation
* converting failure into an apparently successful result

## Finding Gate

`on-error-continue` is not inherently defective.

Report this finding only when continuing the flow or returning success
creates a meaningful functional, reliability, transaction, messaging,
or operational consequence.

## Evidence Requirements

Identify:

* failing processor
* applicable error handler
* error behavior
* resulting payload/response/state
* downstream or caller behavior
* monitoring/acknowledgement implications where applicable

## Impact Examples

Potential impacts include:

* false success responses
* lost failures
* unprocessed records
* incorrect acknowledgements
* committed partial work
* missing operational alerts

---

# ERR-002 — Incorrect Error Propagation

## Description

An error is propagated or continued at an incorrect boundary, causing
behavior inconsistent with the application's execution or failure model.

Potential examples include:

* an error propagated when a local recovery mechanism is required
* an error continued when the caller must receive failure
* an error crossing a flow boundary incorrectly
* transaction rollback not occurring as required
* an error response not matching the failure condition

## Finding Gate

The finding must establish what the correct boundary should be from
repository evidence.

Do not report propagation merely because a different error-handling
strategy is possible.

## Evidence Requirements

Identify:

* source operation
* error type
* handler
* flow/scope boundary
* transaction boundary where applicable
* resulting runtime behavior
* expected behavior based on contract or application design

## Impact Examples

Potential impacts include:

* partial processing
* transaction inconsistency
* incorrect client response
* failed recovery
* inconsistent downstream state

---

# ERR-003 — Overly Broad Error Handling

## Description

An error handler catches a broader class of errors than is appropriate
and applies the same behavior to materially different failures,
creating a production risk.

Potential examples include:

* broad matching that treats transient and permanent failures alike
* broad handling that suppresses unexpected programming errors
* generic recovery for unrelated connector failures
* global handling that masks context-specific errors

## Finding Gate

Broad handling alone is not a defect.

There must be evidence that materially different errors receive
inappropriate treatment.

## Evidence Requirements

Identify:

* error matcher or handler
* error types covered
* differing failure conditions
* common handling behavior
* resulting consequence

## Impact Examples

Potential impacts include:

* retrying non-retryable errors
* swallowing programming defects
* inappropriate HTTP responses
* incorrect transaction behavior
* prolonged outages
* difficult diagnosis

---

# ERR-004 — Unsafe Retry

## Description

Retry or reconnection behavior can cause duplicate side effects,
message loss, excessive load, or another material production failure.

Potential mechanisms include:

* retrying non-idempotent operations
* retrying after an uncertain downstream outcome
* retrying without appropriate limits
* retrying permanent failures
* nested retry mechanisms multiplying attempts
* retrying within inappropriate transaction boundaries
* aggressive retry causing downstream overload

## Finding Gate

Retry is not inherently unsafe.

The finding requires a credible mechanism connecting the retry behavior
to a production consequence.

Consider:

* operation idempotency
* retry count
* retry interval
* backoff
* timeout
* transaction behavior
* acknowledgement behavior
* connector semantics
* downstream side effects

## Evidence Requirements

Identify:

* retry/reconnection configuration
* operation being retried
* side effects
* retry conditions
* limits/backoff where available
* transaction context
* duplicate/loss or overload mechanism

## Impact Examples

Potential impacts include:

* duplicate records
* duplicate payments/orders/updates
* message duplication
* downstream throttling
* cascading failures
* excessive latency
* data inconsistency

---

# ERR-005 — Root Cause Lost

## Description

Error handling removes, replaces, or obscures information required to
diagnose the original failure.

Potential mechanisms include:

* replacing the original error with an unrelated generic error
* logging only a generic message
* discarding useful error attributes
* returning an error response without preserving diagnostic context
* wrapping errors without retaining meaningful cause information

## Finding Gate

Not every sanitized or simplified error response loses the root cause.

A finding requires evidence that useful diagnostic information is
actually lost from the appropriate operational or technical context.

## Evidence Requirements

Identify:

* original error
* error transformation or replacement
* resulting error
* logging behavior
* response behavior
* information that is no longer available

## Impact Examples

Potential impacts include:

* difficult incident diagnosis
* longer recovery time
* inability to distinguish failure causes
* inadequate operational monitoring

---

# ERR-006 — Sensitive Error Information Exposed

## Description

Error handling exposes sensitive internal information to an
unauthorized or inappropriate consumer.

Potential information includes:

* credentials
* tokens
* connection strings
* internal hostnames where sensitive
* SQL statements containing sensitive values
* stack traces
* internal filesystem paths
* secure property values
* authorization headers
* sensitive payload data

## Finding Gate

A finding requires evidence that sensitive information can actually
reach an externally visible or otherwise inappropriate destination.

Do not report an exposure merely because sensitive information exists
internally.

## Evidence Requirements

Identify:

* error source
* handler
* response/logging destination
* exposed information type
* relevant configuration
* actual exposure path

Never reproduce the sensitive value itself.

Use a sanitized description instead.

## Impact Examples

Potential impacts include:

* credential disclosure
* information leakage
* increased attack surface
* exposure of internal implementation details
* privacy or compliance risk

---

# Error Propagation Semantics

When reviewing Mule 4 error handling, explicitly consider the behavior
of:

* `on-error-propagate`
* `on-error-continue`
* Try scopes
* flow-level error handlers
* global error handlers
* flow references
* transactions

Determine whether the error:

* remains an error
* is handled locally
* propagates to a caller
* causes transaction rollback where applicable
* allows processing to continue
* affects acknowledgement or redelivery

Do not make runtime claims without sufficient technical evidence.

---

# HTTP Error Handling

For HTTP-facing flows, inspect:

* status codes
* response payload
* error response structure
* error-to-status mapping
* propagation behavior
* exposure of internal errors
* consistency with API contracts

A technically correct internal error does not automatically imply an
appropriate HTTP response.

Report only contract or behaviorally significant issues.

---

# Transaction Interaction

Where transactions exist, inspect:

* transaction boundaries
* failing operations
* error handlers
* propagation behavior
* rollback behavior
* retry behavior
* side effects outside the transaction

Do not assume that catching an error automatically means a transaction
is committed or rolled back. Determine the actual configured behavior.

---

# Retry and Reconnection Analysis

When retry/reconnection behavior exists, consider:

* whether the operation is idempotent
* whether the downstream outcome is known
* maximum attempts
* delay/backoff
* timeout interaction
* connector-level retries
* application-level retries
* nested retry behavior
* transaction interaction

Multiple retry layers should be analyzed together.

Do not report retry duplication unless it creates a credible production
consequence.

---

# Severity Guidance

Severity must reflect actual production impact.

### CRITICAL

Use for catastrophic consequences such as:

* severe sensitive-information exposure
* widespread data loss
* widespread data corruption
* catastrophic transaction/failure behavior

### HIGH

Use for substantial issues such as:

* significant message/data loss
* duplicate processing with material business impact
* major transaction defects
* severe error suppression
* significant information exposure
* unsafe retries causing major production impact

### MEDIUM

Use for meaningful but contained:

* incorrect error responses
* recovery failures
* diagnosability issues
* realistic retry problems
* partial processing risks

### LOW

Use for limited operational impact.

### NIT

Use only for optional improvements that do not represent material
production risk.

---

# False-Positive Controls

Do not create an error-handling finding when:

* `on-error-continue` is intentionally used and its behavior is correct
* propagation is consistent with the application contract
* a broad handler is correctly scoped and safe
* retry applies only to safe/idempotent operations
* root-cause information remains available through appropriate logging
  or error context
* an error response intentionally sanitizes internal details
* a transaction boundary is correctly configured
* another component provides the required recovery mechanism
* evidence is insufficient to establish runtime behavior or impact

When evidence is insufficient:

**Do not report the finding.**

---

# Positive Error-Handling Indicators

Where supported by evidence, recognize strengths such as:

* specific error-type handling
* appropriate use of `on-error-propagate`
* intentional and safe use of `on-error-continue`
* correct transaction rollback behavior
* bounded and safe retries
* preserved diagnostic context
* sanitized external error responses
* consistent HTTP error mapping
* appropriate recovery boundaries
* useful operational logging

Positive observations must be evidence-backed.

---

# Required Finding Fields

Any error-handling finding must include:

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

Never expose:

* passwords
* API keys
* access tokens
* private keys
* secure property values
* authorization headers
* sensitive payload values

Sensitive information must be described without reproducing its value.