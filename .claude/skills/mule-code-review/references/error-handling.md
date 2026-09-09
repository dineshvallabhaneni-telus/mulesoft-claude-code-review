# MuleSoft Error Handling Review Rules

## Purpose

These rules define how Mule 4 error handling must be reviewed.

Review error handling in the context of:

- Mule error types
- error hierarchy
- `on-error-propagate`
- `on-error-continue`
- Try scopes
- global error handlers
- flow-level error handlers
- `until-successful`
- retry behavior
- reconnection
- transactions
- messaging
- HTTP APIs
- downstream failures
- logging
- error responses
- recovery behavior

Do not evaluate an error handler in isolation.

Trace the error from the original failure through:

1. source processor
2. Try scope or flow
3. error handler
4. retry/reconnection behavior
5. transaction behavior
6. downstream response
7. logging/observability
8. message acknowledgement where applicable

---

# Error Handling Review Principles

Before reporting an error-handling finding:

1. Identify the operation that can fail.
2. Identify the Mule error type produced.
3. Identify the active error handler.
4. Determine whether the error is propagated or continued.
5. Check whether another handler catches the error.
6. Inspect retry/reconnection behavior.
7. Inspect transaction boundaries.
8. Inspect API/client response behavior.
9. Inspect messaging acknowledgement/redelivery behavior.
10. Determine realistic business impact.

Do not assume every error must be propagated.

Some errors are intentionally handled and converted into:

- business responses
- default values
- alternate processing paths
- controlled retries
- compensating actions

The review must determine whether the behavior is intentional and
appropriate.

---

# ERR-001 — Error Swallowed

## Rule

Flag errors that are caught and ignored without a valid business or
technical reason.

Examples:

- `on-error-continue` with no meaningful recovery
- error handler that returns a success response
- error handler that logs but does not communicate failure
- failed downstream operation followed by successful completion

## Severity

HIGH

Escalate to CRITICAL when the behavior can cause widespread data loss,
message loss, or false-success processing.

---

# ERR-002 — Incorrect on-error-continue

## Rule

Flag `on-error-continue` when the error should be propagated because the
operation has not actually completed successfully.

Consider:

- API response
- message processing
- database transaction
- downstream side effects
- business completion criteria

## Severity

HIGH

## Important

Do not automatically flag every use of `on-error-continue`.

It can be appropriate when the error is intentionally transformed into a
successful business outcome.

---

# ERR-003 — Incorrect on-error-propagate

## Rule

Flag `on-error-propagate` when the error should intentionally be handled
and converted into a valid business/API outcome.

Examples:

- expected validation failure
- expected business rejection
- controlled fallback
- documented alternate processing path

## Severity

HIGH

---

# ERR-004 — Overly Broad Error Handler

## Rule

Flag broad `ANY` or overly broad error handling when more specific
handling is required to distinguish materially different failures.

Examples:

- authentication failure treated the same as timeout
- validation failure treated the same as infrastructure failure
- database constraint failure treated the same as database outage

## Severity

MEDIUM

Escalate when broad handling causes incorrect responses, retries,
message loss, or security problems.

---

# ERR-005 — Incorrect Error Type

## Rule

Flag error handling based on an incorrect Mule error type or hierarchy.

Consider:

- connector-specific error types
- HTTP errors
- DB errors
- validation errors
- routing errors
- messaging errors
- security errors
- expression errors

## Severity

HIGH

---

# ERR-006 — Lost Root Cause

## Rule

Flag error handling that destroys useful diagnostic information.

Examples:

- replacing the original error with an unrelated generic error
- discarding original description
- discarding cause information
- logging only a generic message
- returning an internal error without preserving diagnostic context

## Severity

MEDIUM

Escalate when loss of diagnostic information materially increases
production recovery time.

---

# ERR-007 — Incorrect HTTP Status

## Rule

Flag mapping of business or technical errors to inappropriate HTTP
status codes.

Consider:

- 2xx
- 4xx
- 5xx
- validation failures
- authentication failures
- authorization failures
- not found
- conflict
- timeout
- downstream failures

## Severity

HIGH

Do not prescribe a specific status code without considering the API
contract and actual business semantics.

---

# ERR-008 — Sensitive Error Exposure

## Rule

Flag error responses exposing:

- stack traces
- credentials
- tokens
- authorization headers
- internal URLs
- database details
- SQL statements containing sensitive information
- filesystem paths
- internal implementation details
- infrastructure details

## Severity

HIGH

Escalate to CRITICAL when credentials, secrets, or security-sensitive
information are exposed externally.

---

# ERR-009 — Retry Without Idempotency

## Rule

Flag retry of an operation that may produce duplicate business effects
when no adequate idempotency mechanism exists.

Consider:

- POST requests
- database writes
- Salesforce updates
- message publishing
- file operations
- external side effects

## Severity

HIGH

---

# ERR-010 — Unlimited or Unsafe Retry

## Rule

Flag retry behavior that can continuously or excessively retry failures
and cause:

- downstream overload
- retry storms
- increased latency
- resource exhaustion
- duplicate operations
- cascading failures

Consider:

- `until-successful`
- connector retry policies
- reconnection
- nested retry mechanisms
- messaging redelivery

## Severity

HIGH

---

# ERR-011 — Incorrect Transaction Behavior

## Rule

Flag error handling that causes unexpected:

- commit
- rollback
- partial completion
- acknowledgement
- persistence

behavior.

Consider:

- database transactions
- JMS transactions
- XA transactions
- message acknowledgement
- Try scopes
- nested scopes
- external side effects

## Severity

HIGH

Escalate when incorrect behavior can cause data corruption or
inconsistent business state.

---

# ERR-012 — Missing Expected Failure Handling

## Rule

Flag realistically expected external-system failures that have no
appropriate handling or recovery strategy.

Examples:

- timeout
- connection failure
- authentication failure
- rate limiting
- downstream 5xx
- database connectivity failure
- message broker failure

## Severity

MEDIUM

Escalate when failure can cause message loss, outage, or data
inconsistency.

---

# ERR-013 — Incorrect Error Hierarchy Matching

## Rule

Flag error handlers whose order or hierarchy causes a more general
handler to intercept errors before a more specific handler can process
them correctly.

Consider Mule error hierarchy and matching behavior.

## Severity

HIGH

---

# ERR-014 — Unreachable Specific Error Handler

## Rule

Flag specific error handlers that cannot execute because an earlier
broader handler captures the same error.

## Severity

MEDIUM

Escalate when the unreachable handler was intended to provide important
recovery, retry, security, or API behavior.

---

# ERR-015 — Error Handler Masks Business Failure

## Rule

Flag error handling that converts a genuine business failure into
apparent success.

Examples:

- failed order update followed by HTTP 200
- failed message processing followed by acknowledgement
- failed persistence followed by success response

## Severity

HIGH

Escalate to CRITICAL for significant data-loss or financial-processing
scenarios.

---

# ERR-016 — Incorrect Error Mapping

## Rule

Flag mapping from internal Mule errors to application/API errors when
the mapping:

- misrepresents the failure
- loses meaningful classification
- returns incorrect client semantics
- exposes internal implementation details

## Severity

HIGH

---

# ERR-017 — Missing Error Mapping

## Rule

Flag externally visible integrations where internal errors are exposed
directly instead of being mapped to an appropriate application/API error
contract.

## Severity

MEDIUM

Escalate when internal details or sensitive information are exposed.

---

# ERR-018 — Duplicate Error Logging

## Rule

Flag error handling that logs the same failure repeatedly at multiple
layers without adding meaningful diagnostic information.

Consider:

- processor-level logging
- Try scope logging
- flow-level logging
- global error handler logging
- API exception logging

## Severity

LOW

Escalate when excessive logging creates significant cost, noise, or
sensitive-data exposure.

---

# ERR-019 — Missing Diagnostic Context

## Rule

Flag error handling that fails to preserve useful diagnostic context
when the application already has a mechanism for:

- correlation ID
- transaction ID
- message ID
- request ID
- business identifier

## Severity

MEDIUM

Do not require a particular correlation mechanism if the application
already has an equivalent approach.

---

# ERR-020 — Sensitive Data in Error Logs

## Rule

Flag error handling that logs:

- passwords
- tokens
- credentials
- authorization headers
- private keys
- sensitive personal information
- sensitive payloads

## Severity

HIGH

Escalate to CRITICAL when credentials or secrets are exposed.

---

# ERR-021 — Retryable Error Treated as Permanent

## Rule

Flag handling that immediately fails or discards an operation for a
temporary failure when repository evidence indicates the operation should
reasonably be retried.

Examples:

- transient network failure
- temporary timeout
- rate limiting
- temporary service unavailability

## Severity

MEDIUM

Escalate when this creates significant message loss or availability
problems.

---

# ERR-022 — Permanent Error Retried

## Rule

Flag retries for failures that are unlikely to succeed through retry and
where repeated attempts create unnecessary:

- latency
- load
- duplicate effects
- downstream pressure

Examples may include:

- invalid request
- schema validation failure
- authentication configuration failure
- deterministic business rejection

## Severity

MEDIUM

Escalate when retries create significant operational impact.

---

# ERR-023 — Nested Retry Amplification

## Rule

Flag multiple retry mechanisms that can multiply the effective retry
count.

Consider combinations of:

- `until-successful`
- connector retry
- reconnection
- messaging redelivery
- scheduler retry
- upstream retries

## Severity

HIGH

## Impact

Potential consequences include:

- retry storms
- duplicate processing
- excessive downstream load
- long request latency

---

# ERR-024 — Retry Without Backoff

## Rule

Flag repeated retry attempts without appropriate delay/backoff when
rapid retries can increase downstream load or worsen an outage.

## Severity

MEDIUM

Escalate when the application can create a retry storm.

---

# ERR-025 — Missing Retry Exhaustion Handling

## Rule

Flag retry mechanisms that do not provide appropriate behavior after
all retry attempts are exhausted.

Consider:

- error propagation
- dead-letter handling
- persistent failure state
- alerting
- business notification
- compensating action

## Severity

HIGH

---

# ERR-026 — Incorrect Reconnection Handling

## Rule

Flag connector reconnection behavior that:

- retries inappropriate failures
- hides persistent configuration failures
- creates excessive reconnect attempts
- does not appropriately surface unrecoverable failures

## Severity

MEDIUM

Escalate when reconnection behavior can cause cascading failures or
resource exhaustion.

---

# ERR-027 — Missing External Failure Isolation

## Rule

Flag error handling where failure of one downstream dependency can
unnecessarily terminate unrelated processing.

Consider:

- sequential external calls
- shared Try scopes
- shared error handlers
- shared transactions
- shared state

## Severity

MEDIUM

Escalate when the result can cause significant outage or data loss.

---

# ERR-028 — Incorrect Partial Success Handling

## Rule

Flag processing where multiple operations can partially succeed but the
error strategy does not define appropriate behavior.

Examples:

- database update succeeds, external update fails
- external update succeeds, message publication fails
- one item succeeds while another fails
- batch contains mixed outcomes

## Severity

HIGH

---

# ERR-029 — Missing Compensation

## Rule

Flag multi-step business operations where rollback is not technically
possible and there is no appropriate compensating action despite a
realistic partial-failure scenario.

## Severity

HIGH

## Important

Do not assume every distributed workflow requires compensation.

Verify the business consistency requirement.

---

# ERR-030 — Incorrect Try Scope Error Handling

## Rule

Flag Try scopes where error handling changes behavior unexpectedly due
to scope boundaries.

Consider:

- which processor is inside the Try scope
- which errors are caught
- variable/payload state
- transaction boundaries
- propagation behavior

## Severity

MEDIUM

Escalate when the scope causes incorrect recovery or data inconsistency.

---

# ERR-031 — Incorrect Batch Error Handling

## Rule

For Batch processing, review:

- record-level errors
- batch-level errors
- failed records
- completion behavior
- retries
- partial success
- reporting
- restart/recovery

Flag behavior that can silently lose failed records or incorrectly mark
processing as successful.

## Severity

HIGH

---

# ERR-032 — Incorrect Messaging Error Handling

## Rule

For messaging flows, verify the relationship between:

- processing
- acknowledgement
- error propagation
- redelivery
- retry
- dead-letter behavior

Flag cases where a message can be acknowledged despite unsuccessful
business processing.

## Severity

HIGH

Escalate to CRITICAL when significant message loss is credible.

---

# ERR-033 — Error Handler Changes Payload Incorrectly

## Rule

Flag error handlers that unintentionally replace or modify the payload,
attributes, or variables in a way that causes:

- incorrect error responses
- loss of diagnostic information
- downstream failures
- incorrect continuation

## Severity

MEDIUM

---

# ERR-034 — Error Handler Performs Unsafe Side Effect

## Rule

Flag error handlers that perform side effects such as:

- database writes
- message publication
- external API calls
- Object Store updates

without appropriate consideration of:

- retries
- idempotency
- transaction boundaries
- duplicate execution

## Severity

HIGH

---

# ERR-035 — Error Handler Recursion

## Rule

Flag error handling that can cause an error handler to trigger another
error path that repeatedly invokes the same or equivalent handler.

## Severity

HIGH

Escalate when it can create:

- infinite processing
- retry loops
- resource exhaustion
- cascading failures

---

# ERR-036 — Missing Operational Alerting

## Rule

Flag critical unrecoverable failures where the repository provides an
operational alerting mechanism but the error path bypasses it.

## Severity

MEDIUM

Do not require a specific alerting technology unless established by the
project.

---

# ERR-037 — Inconsistent Error Contract

## Rule

Flag different API flows or related endpoints that return materially
inconsistent error structures for equivalent error conditions when an
established application error contract exists.

## Severity

MEDIUM

Escalate when clients can reasonably misinterpret the response.

---

# ERR-038 — Internal Error Details Exposed Through Logging Context

## Rule

Flag error handling that places sensitive or internal implementation
details into:

- correlation variables
- error descriptions
- attributes
- custom error objects
- response variables

when those values may later be exposed externally.

## Severity

HIGH

---

# ERR-039 — Error Classification Too Generic

## Rule

Flag custom error mapping that collapses materially different failures
into one generic error when downstream consumers or operational processes
need to distinguish them.

## Severity

MEDIUM

---

# ERR-040 — Error Recovery Without Verification

## Rule

Flag recovery logic that assumes an operation succeeded without actually
verifying the outcome.

Examples:

- retry/fallback assumes success
- alternate path assumes external state was updated
- recovery continues after uncertain transaction outcome

## Severity

HIGH

---

# Error Handling Review Matrix

For each important failure scenario, determine:

| Failure Scenario | Expected Behavior | Actual Behavior | Risk |
|---|---|---|---|
| Validation failure | Business/API rejection | Inspect | Inspect |
| Authentication failure | Fail securely | Inspect | Inspect |
| Authorization failure | Reject request | Inspect | Inspect |
| Timeout | Retry/fail according to policy | Inspect | Inspect |
| Connection failure | Recovery/failure strategy | Inspect | Inspect |
| Downstream 4xx | Business/technical handling | Inspect | Inspect |
| Downstream 5xx | Retry/failure strategy | Inspect | Inspect |
| Database failure | Rollback/recovery | Inspect | Inspect |
| Message failure | Redelivery/DLQ/recovery | Inspect | Inspect |
| Unexpected error | Propagate and observe | Inspect | Inspect |

Do not assume the expected behavior is identical for every application.
Determine it from the repository and API/business context.

---

# Error Handling Review by Scope

Review error handling at each relevant level:

## Processor Level

Check whether the processor can generate errors that require specific
handling.

## Try Scope

Check:

- scope boundary
- error types
- propagation
- payload state
- transaction behavior

## Flow Level

Check:

- business failure behavior
- API response
- message processing
- downstream failure

## Global Error Handler

Check:

- broad interception
- consistent mapping
- logging
- correlation
- sensitive information
- operational behavior

---

# Error Handling Finding Validation

Before reporting an error-handling finding:

1. Identify the original failure.
2. Identify the Mule error type.
3. Identify the matching handler.
4. Trace propagation/continuation.
5. Inspect retry and reconnection.
6. Inspect transaction behavior.
7. Inspect message acknowledgement if applicable.
8. Inspect API response behavior if applicable.
9. Check logging and sensitive information.
10. Check for existing recovery logic.
11. Determine realistic impact.
12. Confirm severity.

If the behavior is intentional and supported by repository evidence,
do not report it as a defect.

---

# Error Handling Finding Format

Use:

**Finding ID:** ERR-001

**Severity:** HIGH

**Category:** ERROR-HANDLING

**File:** `src/main/mule/order.xml:145`

**Location:** `order-processing-flow / Try scope`

**Problem:**

Describe the error-handling problem.

**Evidence:**

Identify the processor, error type, and handler involved.

**Technical Mechanism:**

Explain how Mule processes the error.

**Impact:**

Explain realistic business and production impact.

**Recommendation:**

Provide an actionable remediation.

**Confidence:** HIGH / MEDIUM / LOW