# MuleSoft Finding Taxonomy

## Purpose

This document standardizes how MuleSoft review findings are classified.

Use this document together with:

- `CLAUDE.md`
- `skills/mule-code-review/SKILL.md`
- `review.md`

Severity must be based on actual risk, not on how unusual or undesirable
the implementation appears.

---

# Core Rule

A pattern is NOT automatically a defect.

The reviewer must establish:

Pattern
→ Technical mechanism
→ Failure scenario
→ Realistic impact
→ Severity

---

# CRITICAL

Use only when there is immediate or severe production risk.

Typical examples:

- production credential committed to source
- private key exposed
- severe authorization bypass
- confirmed sensitive data exposure
- likely irreversible data corruption
- likely large-scale data loss
- catastrophic transaction behavior
- catastrophic production outage caused by the implementation

Do NOT use CRITICAL simply because something is insecure in principle.

---

# HIGH

Use when there is significant realistic production impact.

Examples:

## Security

- exploitable authorization bypass
- significant secret exposure
- sensitive information exposed to unauthorized users
- serious TLS/security weakness with demonstrated impact

## Reliability

- message loss
- failure silently acknowledged
- non-idempotent operation retried and capable of duplicate business effect
- poison messages repeatedly processed without recovery
- serious downstream failure masking

## Transactions

- transaction boundary causes partial business commit
- acknowledgement occurs before durable processing
- rollback does not cover required operations

## APIs

- implementation violates an active API contract
- breaking response/request behavior
- incorrect authentication/authorization behavior

## Performance

- credible memory exhaustion risk
- unbounded processing of large data
- severe N+1 external/database behavior
- retry amplification likely to overload downstream systems

---

# MEDIUM

Use when the issue is meaningful but not immediately severe.

Examples:

- important unhandled edge case
- incomplete error mapping
- moderate retry issue
- missing idempotency where duplicate impact is possible but limited
- important MUnit gap
- moderate query inefficiency
- moderate payload memory concern
- configuration problem with production impact
- maintainability problem that increases operational risk

---

# LOW

Use for issues with limited production impact.

Examples:

- minor logging inconsistency
- limited diagnostic information
- low-impact configuration duplication
- small maintainability concern
- minor test gap

---

# NIT

Use only for optional improvements.

Examples:

- naming improvement
- formatting
- minor stylistic consistency
- small simplification

NIT findings should not dominate the review.

---

# Patterns That Must NOT Automatically Become Findings

## Broad Error Handler

Do not report:

`on-error-continue`

as a defect by itself.

Determine:

- which errors it catches
- what happens afterward
- whether the error is logged
- whether the response is correct
- whether data can be lost
- whether callers receive incorrect success

---

## Missing MUnit Test

Do not report every missing test.

Ask:

- Is the behavior business-critical?
- Is the path complex?
- Is there regression risk?
- Is the path currently untested?
- Would a test materially reduce risk?

---

## Hardcoded Value

Do not automatically report every literal.

Differentiate:

Low concern:
- static non-environment value

Potential concern:
- environment-specific URL

High concern:
- credential or secret

---

## DataWeave Complexity

Do not report complexity merely because the transformation is long.

Establish:

- correctness risk
- maintainability risk
- memory risk
- performance mechanism
- duplication

---

## Retry

Do not report retries merely because they exist.

Determine:

- what operation is retried
- whether it is idempotent
- which failures trigger retry
- how many attempts occur
- whether duplicate side effects are possible

---

## Logging

Do not report logging simply because payloads are logged.

Determine whether the payload contains:

- credentials
- tokens
- PII
- sensitive business data
- regulated information

Also consider production volume and operational value.

---

## Synchronous Calls

Do not automatically report synchronous integrations.

Determine:

- dependency chain length
- timeout behavior
- latency
- failure isolation
- scalability
- business requirement

---

## Global Configuration

Do not report global configuration simply because multiple configurations
exist.

Determine whether duplication causes:

- inconsistent behavior
- configuration drift
- security risk
- operational complexity

---

# Severity Escalation

Severity may increase when multiple risk factors combine.

Example:

Non-idempotent POST
+
Automatic retry
+
No duplicate detection
+
Financial transaction

Potential result:

HIGH

But:

Non-idempotent POST
+
No retry
+
No duplicate mechanism
+
Low-impact operation

May be:

MEDIUM or LOW

Severity depends on actual impact.

---

# Finding Deduplication

Combine findings when they represent the same root cause.

Example:

Instead of:

- retry can duplicate orders
- retry can duplicate invoices
- retry can duplicate payments

If caused by the same retry architecture:

Report one architectural finding:

`RETRY-001 — Non-idempotent retry strategy`

Then provide affected flows as evidence.

---

# Confidence

## HIGH

Directly demonstrated.

Example:

A password is visible in a properties file.

## MEDIUM

Strong evidence but dependent on runtime/environment behavior.

## LOW

Important uncertainty remains.

Avoid reporting LOW-confidence issues unless the risk is still meaningful
and clearly explained.

---

# Evidence Hierarchy

Prefer:

1. Actual Mule XML
2. DataWeave
3. API specification
4. Connector configuration
5. Properties
6. Maven configuration
7. MUnit
8. Deployment configuration
9. Documentation
10. Naming/comments

Implementation evidence should override comments or assumptions.

---

# Finding Construction

Use:

## Pattern

What exists?

## Mechanism

How does it behave?

## Scenario

When does the problem occur?

## Impact

What happens?

## Recommendation

How should the risk be reduced?

A finding without a mechanism or impact is usually incomplete.

---

# Architect-Level Rule

The reviewer should distinguish between:

### Defect

Something is demonstrably wrong.

### Risk

Something creates a credible production risk.

### Observation

Something is worth noting but is not necessarily a defect.

### Recommendation

An architectural improvement.

Do not turn every observation or recommendation into a defect.

---

# Final Quality Test

Before finalizing the review ask:

> If this finding were challenged by the development team, could I prove
> it from the repository?

If the answer is no:

Do not report it as a confirmed finding.