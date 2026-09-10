# Messaging Review Rules

## Purpose

Review MuleSoft messaging integrations for reliable message processing,
acknowledgement behavior, redelivery, duplicate processing, idempotency,
retry behavior, dead-letter handling, ordering, and transaction
boundaries.

Messaging findings must be based on:

* actual connector configuration
* message-consumer behavior
* acknowledgement configuration
* retry/redelivery configuration
* transaction configuration
* error handling
* downstream processing
* visible business behavior

Never assume exactly-once processing without evidence.

---

# Supported Messaging Patterns

Where applicable, inspect messaging systems such as:

* JMS
* Anypoint MQ
* Kafka
* AMQP
* VM
* other broker/queue integrations visible in the repository

Connector-specific semantics take precedence over generic messaging
assumptions.

---

# Messaging Review Principles

Before reporting a messaging finding:

1. Identify the messaging connector/broker.
2. Identify the producer or consumer.
3. Inspect acknowledgement behavior.
4. Inspect acknowledgement timing/boundary.
5. Inspect redelivery configuration.
6. Inspect retry configuration.
7. Inspect dead-letter handling.
8. Inspect error handling.
9. Inspect transaction boundaries.
10. Inspect downstream side effects.
11. Inspect idempotency controls.
12. Inspect ordering requirements where visible.
13. Inspect concurrency where relevant.
14. Inspect MUnit/tests where available.
15. Determine the actual failure scenario.
16. Determine production/business impact.
17. Assign severity and confidence based on evidence.

Trace the complete message lifecycle rather than reviewing the consumer
in isolation.

---

# Message Lifecycle

Where applicable, reason about the lifecycle as:

```text id="8j1f4k"
Message Published
       |
       v
Message Received
       |
       v
Acknowledgement Boundary
       |
       v
Processing
       |
       +---- Success
       |
       +---- Failure
               |
               +--> Retry / Redelivery
               |
               +--> Dead Letter
               |
               +--> Rejection / Failure
```

The exact behavior depends on the messaging connector and configuration.

Do not generalize connector behavior without verifying the applicable
semantics.

---

# MSG-001 — Message Acknowledgement Risk

## Description

Message acknowledgement behavior can cause a message to be considered
successfully processed before its required processing has completed, or
can prevent appropriate acknowledgement after processing succeeds.

Potential consequences include:

* message loss
* duplicate processing
* premature acknowledgement
* unnecessary redelivery
* inconsistent downstream state

## Finding Gate

Establish:

* when acknowledgement occurs,
* what processing occurs before/after acknowledgement,
* what happens when processing fails,
* whether the broker redelivers,
* whether transaction semantics affect acknowledgement.

Do not assume acknowledgement occurs at a particular point without
connector-specific evidence.

## Evidence Requirements

Identify:

* consumer configuration
* acknowledgement mode/behavior
* processing boundary
* failure path
* resulting consequence

---

# MSG-002 — Duplicate Processing Risk

## Description

A message can be processed more than once under realistic failure,
redelivery, retry, or acknowledgement scenarios, creating a meaningful
production consequence.

Potential mechanisms include:

* acknowledgement after a side effect fails
* consumer timeout followed by redelivery
* retry after uncertain completion
* connector redelivery
* application-level retry
* transaction rollback
* consumer restart

Duplicate delivery is not automatically a defect.

## Finding Gate

Establish:

1. a credible duplicate-delivery or duplicate-execution path,
2. a side effect that can occur more than once, and
3. insufficient protection against the duplicate effect.

Consider:

* idempotency
* unique business keys
* duplicate detection
* transactional controls
* downstream idempotency

## Evidence Requirements

Identify:

* message source
* duplicate mechanism
* processing operation
* side effect
* missing/insufficient control
* production impact

---

# MSG-003 — Missing Idempotency Where Required by Visible Behavior

## Description

Message processing performs a side effect that can be repeated because
of normal messaging failure/redelivery behavior, but no adequate
idempotency control is present.

Potential side effects include:

* record creation
* payment processing
* order submission
* external API updates
* message publication
* file creation
* business-state changes

## Finding Gate

Idempotency must be relevant to the demonstrated behavior.

Establish:

* duplicate execution is possible,
* the operation is not inherently idempotent,
* repeated execution has a meaningful consequence, and
* no adequate control exists.

Do not assume every message consumer requires an application-level
idempotency mechanism.

## Evidence Requirements

Identify:

* message consumer
* side-effecting operation
* duplicate path
* absence of idempotency control
* resulting business impact

---

# MSG-004 — Unsafe Retry

## Description

Retry behavior can cause message amplification, duplicate side effects,
downstream overload, processing delays, or repeated handling of messages
that cannot succeed.

Potential mechanisms include:

* retrying permanent failures
* retrying non-idempotent operations
* excessive retry counts
* insufficient delay/backoff
* application retry combined with broker redelivery
* retry storms
* retrying after uncertain completion

## Finding Gate

Inspect the complete retry chain, including:

* connector retry
* broker redelivery
* application-level retry
* error-handler retry
* downstream retry
* upstream/client retry where relevant

Do not assume retry is unsafe merely because it exists.

The finding must establish a credible production consequence.

## Evidence Requirements

Identify:

* retry configuration
* triggering error
* retry count/frequency
* delay/backoff where available
* downstream operation
* duplicate/amplification mechanism
* impact

---

# MSG-005 — Message Loss Risk

## Description

A realistic failure path can cause a message to be permanently lost
without successful processing or appropriate recovery.

Potential mechanisms include:

* acknowledgement before durable processing
* incorrect acknowledgement behavior
* error continuation combined with successful acknowledgement
* failed transaction/rollback semantics
* missing dead-letter/recovery path where required
* consumer behavior that discards failed messages

## Finding Gate

A message-loss finding requires a demonstrable or strongly supported
path where:

1. the message is no longer available for processing, and
2. the required business operation has not completed successfully, and
3. no adequate recovery mechanism exists.

Do not report missing dead-letter handling by itself.

Dead-letter behavior depends on the broker, connector, operational model,
and failure requirements.

## Evidence Requirements

Identify:

* message source
* acknowledgement/recovery behavior
* failure scenario
* point at which the message can become unrecoverable
* absence of recovery
* business impact

---

# Dead-Letter Handling

Inspect:

* dead-letter queue/topic configuration
* maximum redelivery count
* failure routing
* poison-message handling
* operational visibility
* replay/recovery mechanism where visible

A dead-letter queue is not automatically required.

Report a finding only when the repository establishes that failed
messages have no adequate recovery path and that this creates meaningful
risk.

---

# Poison Messages

Consider messages that repeatedly fail because of:

* invalid schema
* malformed payload
* unsupported values
* permanent downstream/business errors
* transformation errors

Determine whether such messages can:

* block processing
* consume retry capacity
* create repeated logs
* delay healthy messages
* remain indefinitely in the retry path

Do not report poison-message risk without a credible repeated-failure
mechanism.

---

# Ordering

Where message ordering is a visible business requirement, inspect:

* concurrency
* parallel processing
* partitioning
* consumer configuration
* acknowledgement behavior
* retry/redelivery behavior

Do not assume global ordering is required.

A finding requires evidence that:

1. ordering matters,
2. the implementation can violate the required ordering, and
3. the violation has meaningful impact.

---

# Transactions

Inspect messaging transactions together with:

* database transactions
* acknowledgement
* commit/rollback
* error propagation
* downstream side effects

Do not assume that a transaction provides distributed atomicity across
unrelated systems.

For example:

```text id="q8w2ps"
Message
   |
   v
Database update
   |
   v
External HTTP call
```

A database transaction does not automatically roll back an external
HTTP side effect.

Report a transaction finding only when the actual boundary creates a
material correctness or reliability problem.

---

# Acknowledgement and Error Handling

Trace how these interact:

* `on-error-continue`
* `on-error-propagate`
* Try scopes
* global error handlers
* retry scopes
* transaction scopes

Consider whether an error is:

* propagated appropriately
* swallowed
* acknowledged
* redelivered
* routed to dead letter
* retried unnecessarily

Coordinate with the Error Handling reference to avoid duplicate
findings.

---

# Producer Review

For message producers, inspect:

* publication failure handling
* retry behavior
* duplicate publication
* transaction behavior
* ordering where required
* message persistence/durability where visible
* serialization/schema compatibility

Do not assume a successful local flow means the message was durably
accepted by the broker unless the connector semantics establish that.

---

# Consumer Concurrency

Where applicable, inspect:

* concurrent consumers
* worker concurrency
* parallel processing
* shared resources
* ordering constraints
* database contention
* downstream rate limits

Do not report concurrency merely because multiple consumers exist.

A finding requires a credible correctness, resource, or downstream-impact
mechanism.

---

# Schema and Message Compatibility

Where schemas/contracts are visible, consider:

* required fields
* field compatibility
* serialization format
* version changes
* producer/consumer compatibility

Do not invent message contracts.

If the expected schema is not visible, record a limitation where
appropriate.

---

# Idempotency Controls

Potential controls include:

* unique business keys
* idempotency keys
* duplicate detection
* database uniqueness constraints
* Object Store/state tracking
* downstream idempotency
* transactional processing

Do not assume a specific control is required when another verified
mechanism provides equivalent protection.

---

# Severity Guidance

Severity must reflect actual business and production impact.

### CRITICAL

Use for:

* highly likely widespread message loss
* catastrophic duplicate side effects
* severe corruption of business state

### HIGH

Use for:

* significant message loss
* major duplicate processing
* severe unsafe retry amplification
* critical acknowledgement defects
* substantial transaction/recovery failures

### MEDIUM

Use for:

* meaningful duplicate-processing risk
* realistic idempotency gaps
* material retry problems
* significant poison-message handling gaps
* credible ordering violations

### LOW

Use for:

* limited messaging reliability concerns
* lower-impact operational recovery gaps

### NIT

Use only for optional messaging improvements without material
production impact.

---

# False-Positive Controls

Do not create a messaging finding when:

* acknowledgement behavior is correct for the connector
* duplicate delivery is possible but processing is safely idempotent
* retries are appropriately bounded and safe
* dead-letter behavior is intentionally handled elsewhere
* ordering is not a demonstrated business requirement
* transactions correctly cover the required operations
* poison messages cannot create the claimed production consequence
* another component provides the required recovery/control
* exactly-once behavior is not being claimed without evidence
* evidence is insufficient

When evidence is insufficient:

**Do not report the finding.**

Record the limitation where relevant.

---

# Positive Messaging Indicators

Where supported by evidence, recognize strengths such as:

* correct acknowledgement boundaries
* safe redelivery handling
* explicit idempotency controls
* bounded retries
* appropriate dead-letter handling
* poison-message isolation
* correct transaction boundaries
* controlled concurrency
* appropriate ordering controls
* durable publication/consumption behavior
* strong MUnit coverage for failure and redelivery scenarios

Positive observations must be evidence-backed.

---

# Required Finding Fields

Any messaging finding must include:

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
* access tokens
* private keys
* authorization headers
* secure property values
* sensitive message payloads

Sensitive information must be sanitized before inclusion in the review
artifact.