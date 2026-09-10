# Connector Review Rules

## Purpose

Review MuleSoft connector configurations and usage for reliability,
resource safety, external-system behavior, performance, and operational
compatibility.

For applicable connectors inspect:

* authentication
* authorization where connector-specific
* connection configuration
* timeout
* retry
* reconnection
* pooling
* concurrency
* rate limits
* external call volume
* idempotency
* transaction behavior
* connection/resource lifecycle
* configuration reuse
* connector version
* compatibility
* failure behavior

Connector findings must be based on actual repository evidence and
credible production impact.

Do not report a missing setting merely because a setting exists in an
example or recommended configuration.

---

# Connector Review Principles

Before reporting a connector finding:

1. Identify the connector.
2. Identify its version where available.
3. Inspect the global configuration.
4. Inspect connector operation configuration.
5. Inspect referenced properties.
6. Inspect timeout configuration.
7. Inspect retry/reconnection behavior.
8. Inspect pooling/resource configuration where applicable.
9. Inspect transaction boundaries.
10. Inspect surrounding error handling.
11. Inspect call frequency and concurrency where relevant.
12. Inspect idempotency for side-effecting operations.
13. Inspect tests where relevant.
14. Determine actual production impact.
15. Assign severity and confidence based on evidence.

Connector-specific semantics take precedence over generic assumptions.

---

# CON-001 — Unsafe Connector Configuration

## Description

A connector is configured in a way that creates a meaningful
security, reliability, compatibility, or operational risk.

Potential examples include:

* insecure authentication configuration
* inappropriate connection settings
* unsafe transport configuration
* contradictory global and operation-level configuration
* invalid or incompatible connector settings
* configuration that defeats an intended security or reliability control
* unsafe defaults where repository evidence establishes their impact

## Finding Gate

The finding must identify:

* connector
* configuration
* actual behavior
* production consequence

Do not report a configuration simply because another configuration would
be preferable.

## Evidence Requirements

Identify:

* connector/global configuration
* affected operation
* relevant property or setting
* runtime behavior
* production impact

---

# CON-002 — Missing Timeout

## Description

A connector operation can wait indefinitely or for an unsafe duration
because an effective timeout is absent or materially inappropriate, and
the condition creates a credible production risk.

Potential consequences include:

* thread/resource exhaustion
* blocked flows
* request timeouts at higher layers
* cascading failures
* stalled message processing
* poor failure recovery

## Finding Gate

First determine whether an effective timeout is provided by:

* connector configuration
* operation configuration
* referenced properties
* transport configuration
* platform/runtime behavior
* surrounding application controls

Do not assume that an explicit timeout must exist in every operation.

A finding requires evidence that the effective timeout is absent or
unsafe **and** that this creates meaningful production impact.

## Evidence Requirements

Identify:

* connector
* operation
* effective timeout configuration
* execution context
* credible failure scenario
* production consequence

---

# CON-003 — Unsafe Retry/Reconnection

## Description

Retry or reconnection behavior can create duplicate side effects,
amplify failures, overload a downstream system, delay recovery, or
otherwise create meaningful production risk.

Potential mechanisms include:

* retrying non-idempotent operations
* aggressive retry counts
* insufficient backoff
* retry storms
* reconnect loops
* retrying permanent failures
* retrying after uncertain downstream completion
* multiple overlapping retry mechanisms

## Finding Gate

Retry or reconnection is not inherently a defect.

Determine:

* what operation is being retried
* whether it has side effects
* whether it is idempotent
* what failures trigger retry
* retry count
* delay/backoff
* connector behavior
* application-level retry
* downstream behavior
* transaction interaction

Only report the finding when the repository establishes a credible
production consequence.

## Evidence Requirements

Identify:

* connector
* operation
* retry/reconnection configuration
* triggering failure
* duplicate/amplification mechanism
* affected downstream system
* production impact

---

# CON-004 — Connection/Resource Risk

## Description

Connector usage creates a credible risk involving connection pools,
resource exhaustion, connection leakage, concurrency, or resource
lifecycle.

Potential mechanisms include:

* undersized connection pool
* excessive concurrency
* unbounded connection creation
* inappropriate pool limits
* resource retention
* long-lived blocked connections
* high-volume operations exceeding configured capacity

## Finding Gate

Do not report pool configuration based solely on generic recommended
values.

Consider:

* expected concurrency
* execution frequency
* timeout behavior
* pool size
* connection lifecycle
* workload characteristics
* connector semantics
* deployment scale where known

A finding requires a credible resource-exhaustion mechanism.

## Evidence Requirements

Identify:

* connector
* relevant pool/resource configuration
* concurrency or execution path
* resource lifecycle
* production impact

If workload information is unavailable and impact cannot be established,
record a limitation instead.

---

# CON-005 — Rate-Limit or External-Call Risk

## Description

Connector usage can exceed or materially stress a downstream
system's rate limits or create excessive external-call volume.

Potential mechanisms include:

* connector calls inside large loops
* repeated calls caused by retries
* polling at excessive frequency
* unnecessary duplicate calls
* nested external calls
* fan-out without bounded concurrency
* pagination implemented with excessive requests

## Finding Gate

Do not assume a downstream rate limit exists unless repository evidence
or known connector/service configuration establishes one.

Where a rate limit is visible, assess whether the application can exceed
it.

Where the rate limit is not visible, a finding requires another credible
mechanism demonstrating meaningful external-call risk.

## Evidence Requirements

Identify:

* connector
* external operation
* call location
* repetition mechanism
* estimated or demonstrable call amplification
* downstream constraint where known
* production impact

---

# Authentication and Security

Inspect connector authentication mechanisms such as:

* client credentials
* username/password
* OAuth
* tokens
* certificates
* secure properties
* external credential providers

Never expose credential values.

Coordinate with the Security reference for findings involving:

* secrets in source
* secrets in logs
* TLS weaknesses
* authorization
* sensitive data

Avoid duplicate findings where the security root cause is identical.

---

# Timeout Review

Consider timeouts at all relevant layers:

* connector operation
* HTTP request
* response/read timeout
* connection timeout
* database operation
* messaging operation
* application-level timeout

A timeout configured at one layer does not automatically establish that
all other layers are safe.

Trace the effective behavior before reporting a missing timeout.

---

# Retry and Reconnection Review

Inspect the complete retry path:

```text
Operation
   |
   v
Connector
   |
   +--> Connector retry/reconnection
   |
   +--> Application retry
   |
   +--> Error handler retry
   |
   +--> Upstream/client retry
```

Consider combined retry amplification.

For side-effecting operations, determine whether a failure can occur
after the external system has accepted the request but before Mule
receives confirmation.

This is particularly important for:

* record creation
* payments
* message publication
* updates
* external state changes

Do not assume retry is safe merely because the connector operation
normally succeeds.

---

# Idempotency

For side-effecting connector operations, inspect whether repeated
execution can create:

* duplicate records
* duplicate transactions
* duplicate messages
* repeated updates
* inconsistent external state

Potential controls include:

* idempotency keys
* unique business identifiers
* duplicate detection
* transactional coordination
* downstream idempotency
* application-level safeguards

Do not report an idempotency issue where the operation is inherently
idempotent or another verified control prevents duplicate effects.

---

# Transactions

Inspect whether connector operations participate in transactions where
the repository indicates transactional behavior.

Consider:

* transaction scope
* transaction type
* connector support
* commit/rollback behavior
* external side effects
* database and messaging interaction
* error propagation

Do not assume unrelated external systems participate in the same
transaction.

A transaction finding requires evidence that the actual transaction
boundary creates a meaningful correctness or reliability problem.

---

# Configuration Reuse

Prefer reusable global connector configurations when they provide
consistent behavior and reduce configuration drift.

However, duplication alone is not automatically a finding.

Report duplicated connector configuration only when it creates a
meaningful risk such as:

* inconsistent security settings
* inconsistent timeout behavior
* inconsistent retry behavior
* environment drift
* difficult operational management

---

# Connector Compatibility

Inspect:

* connector version
* Mule runtime compatibility
* Java compatibility
* Mule Maven Plugin compatibility where relevant
* dependency conflicts
* deprecated connector configuration

Do not report an older connector version merely because a newer version
exists.

A compatibility finding requires evidence of an actual or credible
runtime/build/maintenance consequence.

---

# Severity Guidance

Severity must reflect actual production impact.

### CRITICAL

Use only for catastrophic connector consequences such as:

* severe credential/security exposure
* highly likely widespread data corruption or loss
* catastrophic downstream impact

### HIGH

Use for:

* major duplicate side effects
* severe retry amplification
* significant connection/resource exhaustion
* major downstream overload
* severe connector security configuration

### MEDIUM

Use for:

* meaningful timeout risks
* realistic retry/reconnection defects
* material resource risks
* significant external-call amplification

### LOW

Use for:

* limited operational risks
* lower-impact configuration inconsistencies

### NIT

Use only for optional connector improvements without material production
impact.

---

# False-Positive Controls

Do not create a connector finding when:

* the connector configuration is valid and safe
* an effective timeout exists elsewhere
* retry behavior is appropriate for the operation
* the operation is idempotent or adequately protected
* pool/resource limits are appropriate for the demonstrated workload
* no credible rate-limit or external-call problem exists
* configuration duplication creates no meaningful risk
* connector version differences have no demonstrated consequence
* another component already mitigates the concern
* evidence is insufficient

When evidence is insufficient:

**Do not report the finding.**

Record the limitation where relevant.

---

# Positive Connector Indicators

Where supported by evidence, recognize strengths such as:

* reusable global connector configurations
* appropriate timeouts
* bounded retry/reconnection
* safe idempotency controls
* appropriate connection pooling
* controlled external-call volume
* secure credential handling
* compatible connector versions
* appropriate transaction boundaries
* clear separation of connector configuration and application logic

Positive observations must be evidence-backed.

---

# Required Finding Fields

Any connector finding must include:

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

Sensitive information must be sanitized before inclusion in the review
artifact.