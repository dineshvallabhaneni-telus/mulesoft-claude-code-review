# Messaging Review Rules

## Purpose

These rules define how messaging integrations in Mule 4 applications must
be reviewed.

Review messaging behavior together with:

- Anypoint MQ
- JMS
- VM
- Kafka or other messaging connectors when present
- message acknowledgement
- redelivery
- retry behavior
- dead-letter queues
- poison messages
- idempotency
- transaction boundaries
- ordering
- concurrency
- batch processing
- Object Store
- external systems
- database operations
- error handling
- MUnit tests
- application configuration

Do not assume exactly-once processing.

Do not assume messages are delivered only once.

Do not assume message ordering unless the messaging platform and
application configuration provide evidence supporting that behavior.

A finding must be supported by repository evidence and must have a
realistic production, business, reliability, data-integrity, or
performance impact.

---

# Messaging Review Principles

Before reporting a messaging finding:

1. Identify the messaging technology.
2. Identify producer and consumer flows.
3. Identify acknowledgement behavior.
4. Identify redelivery behavior.
5. Identify retry behavior.
6. Identify transaction boundaries.
7. Identify error handling.
8. Identify dead-letter behavior.
9. Identify poison-message behavior.
10. Identify idempotency strategy.
11. Identify ordering requirements.
12. Identify concurrency behavior.
13. Identify downstream side effects.
14. Inspect Object Store or persistence mechanisms where applicable.
15. Inspect MUnit coverage.
16. Determine realistic production impact.

If behavior cannot be established from the repository, inspect related
flows, global configurations, properties, deployment configuration, and
tests before reporting the issue.

---

# MSG-001 — Message Loss

## Rule

Flag message processing that can acknowledge, consume, remove, or otherwise
lose a message before the business operation has successfully completed.

Examples:

- acknowledgement before downstream processing
- message considered successfully processed after an error
- on-error-continue causing a failed message to be acknowledged
- transaction commits before required downstream work completes
- message removed from the source without durable recovery

## Severity

CRITICAL

Escalate when the lost message represents:

- financial transactions
- customer orders
- regulatory events
- business-critical records
- irreversible operations

---

# MSG-002 — Duplicate Processing

## Rule

Flag message processing where the same message can be processed multiple
times and the resulting business operation is not safe for duplicates.

Potential causes include:

- redelivery
- consumer restart
- timeout after downstream completion
- acknowledgement failure
- retry
- worker failure
- transaction rollback

## Severity

HIGH

Do not report duplicate delivery itself as a defect.

The finding is the lack of safe handling of duplicate delivery when
duplicate processing can cause a meaningful business impact.

---

# MSG-003 — Missing Idempotency

## Rule

Flag message consumers performing non-idempotent business operations
without an appropriate mechanism to prevent or safely tolerate duplicate
processing.

Possible mechanisms include:

- idempotency key
- message ID tracking
- business key
- unique database constraint
- Object Store
- deduplication mechanism
- downstream idempotency

## Severity

HIGH

Only report when duplicate delivery is realistically possible and the
business operation has duplicate side effects.

---

# MSG-004 — Incorrect Acknowledgement

## Rule

Flag acknowledgement behavior that does not correctly represent whether
message processing succeeded.

Examples:

- acknowledging before business processing
- acknowledging despite unrecoverable failure
- acknowledging after an error was swallowed
- failing to acknowledge successfully processed messages when the
  connector requires explicit acknowledgement

## Severity

HIGH

Escalate to CRITICAL when incorrect acknowledgement can cause
significant message loss.

---

# MSG-005 — Unsafe Retry

## Rule

Flag retries that can cause duplicate or inconsistent business effects.

Consider:

- database writes
- Salesforce updates
- HTTP POST operations
- financial transactions
- file creation
- message publication
- external system updates

## Severity

HIGH

Verify whether the operation is idempotent before reporting.

---

# MSG-006 — Poison Message Handling Missing

## Rule

Flag consumers that can repeatedly receive and fail on the same
unprocessable message without an appropriate recovery strategy.

Potential mechanisms include:

- dead-letter queue
- maximum redelivery count
- quarantine
- failure routing
- operational alerting
- manual recovery process

## Severity

MEDIUM / HIGH

Use HIGH when a poison message can block or significantly degrade
message processing.

---

# MSG-007 — Incorrect Ordering Assumption

## Rule

Flag logic that assumes messages are processed in a specific order when
the messaging platform, connector configuration, concurrency model, or
application architecture does not guarantee that ordering.

Examples:

- update message processed before create message
- dependent events processed concurrently
- multiple consumers processing related messages without ordering
- asynchronous processing that changes event order

## Severity

MEDIUM

Escalate when ordering violations can corrupt business state.

---

# MSG-008 — Incorrect Transaction/Acknowledgement Boundary

## Rule

Flag transaction and acknowledgement boundaries that can produce
inconsistent message/database or message/external-system state.

Examples:

- message acknowledged before database commit
- database committed while message acknowledgement fails
- message acknowledged while downstream transaction is rolled back
- database transaction does not include operations that must be atomic

## Severity

HIGH

Consider whether the architecture intentionally provides eventual
consistency.

Do not assume distributed transactions are always required.

---

# MSG-009 — Missing Dead-Letter Handling

## Rule

Flag messaging flows where permanently failed messages have no
appropriate dead-letter, quarantine, or recovery mechanism when the
messaging platform and business requirements require one.

## Severity

MEDIUM / HIGH

Use HIGH when failed messages can repeatedly block normal processing or
cause significant operational impact.

---

# MSG-010 — Incorrect Dead-Letter Configuration

## Rule

Flag dead-letter handling that can:

- discard messages unexpectedly
- route messages to the wrong destination
- create loops
- lose diagnostic information
- make recovery impossible
- expose sensitive information

## Severity

HIGH

---

# MSG-011 — Redelivery Loop

## Rule

Flag message processing where a failed message can be repeatedly
redelivered without an effective limit or recovery mechanism.

Consider:

- maximum redelivery count
- retry policy
- dead-letter routing
- permanent versus transient errors

## Severity

HIGH

Escalate when repeated redelivery can overload the application or
downstream systems.

---

# MSG-012 — Retry Storm

## Rule

Flag multiple retry or redelivery mechanisms that can multiply message
processing attempts.

Consider:

- connector retry
- until-successful
- application retry
- scheduler retry
- messaging redelivery
- downstream retry

## Severity

HIGH

Potential consequences include:

- downstream overload
- duplicate business operations
- database contention
- message backlog
- worker saturation

---

# MSG-013 — Retry of Permanent Failure

## Rule

Flag retry behavior that repeatedly retries failures that are unlikely
to succeed without changing the input or configuration.

Examples:

- invalid message schema
- missing required business data
- authorization failure
- malformed payload
- permanent validation failure

## Severity

MEDIUM / HIGH

Transient failures should generally be distinguished from permanent
failures.

---

# MSG-014 — Missing Failure Classification

## Rule

Flag message processing that treats all failures identically when the
application needs different handling for:

- transient failures
- validation failures
- business errors
- authentication failures
- authorization failures
- downstream unavailable
- malformed messages

## Severity

MEDIUM

Escalate when incorrect classification causes message loss or repeated
processing.

---

# MSG-015 — Message Acknowledged After Error Continuation

## Rule

Flag flows where `on-error-continue` or equivalent behavior causes the
messaging source to consider a failed message successfully processed.

## Severity

HIGH

This can result in silent message loss.

---

# MSG-016 — Message Failure Without Operational Visibility

## Rule

Flag important message failures that provide no meaningful operational
diagnostic information.

Consider:

- message identifier
- correlation identifier
- failure category
- source/destination
- retry count
- error type

## Severity

MEDIUM

Do not require sensitive message payloads to be logged.

---

# MSG-017 — Sensitive Message Logging

## Rule

Flag logging of message contents or metadata that exposes:

- passwords
- access tokens
- authorization headers
- financial information
- personal information
- confidential business data

## Severity

HIGH / CRITICAL

Coordinate with:

references/security.md

Do not create duplicate findings for the same root cause.

---

# MSG-018 — Message Identifier Not Preserved

## Rule

Flag processing where an available message identifier or correlation
identifier is unnecessarily discarded and this prevents:

- duplicate detection
- tracing
- troubleshooting
- reconciliation

## Severity

LOW / MEDIUM

Only report when the identifier is important to the application's
operational or business behavior.

---

# MSG-019 — Correlation Context Lost

## Rule

Flag asynchronous processing where correlation information required for
tracing or business reconciliation is lost.

Consider:

- correlation ID
- message ID
- business transaction ID
- source event ID

## Severity

LOW / MEDIUM

Escalate when loss of correlation prevents effective production
diagnosis or reconciliation.

---

# MSG-020 — Incorrect Concurrency

## Rule

Flag consumer concurrency that can cause:

- duplicate processing
- race conditions
- ordering violations
- database contention
- downstream rate-limit violations
- resource exhaustion

## Severity

MEDIUM / HIGH

Do not report concurrency itself as a problem.

The finding must identify a realistic adverse effect.

---

# MSG-021 — Excessive Consumer Concurrency

## Rule

Flag consumer concurrency that can exceed the capacity of:

- downstream APIs
- databases
- Salesforce
- message brokers
- application workers

## Severity

MEDIUM / HIGH

Consider:

- connector limits
- API rate limits
- database pool size
- worker resources
- message volume

---

# MSG-022 — Insufficient Consumer Concurrency

## Rule

Flag consumer processing that cannot reasonably keep up with expected
message volume when the repository provides evidence of a production
throughput requirement.

Potential consequences include:

- growing backlog
- SLA violations
- stale data
- downstream synchronization delays

## Severity

MEDIUM

Do not report without evidence of a realistic throughput requirement.

---

# MSG-023 — Unbounded Message Backlog Risk

## Rule

Flag architecture or configuration where message backlog can grow
without effective control, monitoring, scaling, or failure recovery.

Consider:

- consumer throughput
- producer rate
- concurrency
- retry behavior
- downstream availability

## Severity

HIGH

Only report when repository evidence supports the risk.

---

# MSG-024 — Missing Backpressure Consideration

## Rule

Flag processing where downstream systems can be overwhelmed because
message consumption continues without reasonable flow control.

Consider:

- concurrency
- batching
- rate limits
- downstream capacity
- retry behavior

## Severity

MEDIUM / HIGH

---

# MSG-025 — Unsafe Batch Message Processing

## Rule

Flag batch processing where one failure can incorrectly:

- acknowledge successful messages as failed
- lose messages
- duplicate successful messages
- rollback unnecessarily large amounts of work

## Severity

HIGH

Inspect the actual batch acknowledgement and transaction behavior.

---

# MSG-026 — Incorrect Batch Failure Handling

## Rule

Flag batch consumers that do not correctly distinguish between:

- successfully processed messages
- failed messages
- retryable messages
- permanently failed messages

## Severity

HIGH

---

# MSG-027 — Missing Message Deduplication

## Rule

Flag systems where duplicate events are realistically expected but no
deduplication or idempotency mechanism exists.

Consider:

- event ID
- message ID
- business key
- Object Store
- database uniqueness

## Severity

HIGH

Coordinate with:

references/database.md

Do not duplicate MSG-003 when the root cause is the same.

---

# MSG-028 — Incorrect Deduplication Scope

## Rule

Flag deduplication logic that uses an identifier with an inappropriate
scope.

Examples:

- local in-memory state for a multi-worker application
- short retention period for long-lived duplicate risk
- non-unique business field
- identifier that changes across retries

## Severity

HIGH

---

# MSG-029 — Non-Durable Idempotency State

## Rule

Flag idempotency state stored only in memory when processing can occur
across workers, restarts, or deployments.

## Severity

HIGH

Only report when duplicate processing is realistically possible.

---

# MSG-030 — Incorrect Idempotency Expiration

## Rule

Flag idempotency records that expire before the period during which
duplicate delivery can realistically occur.

## Severity

MEDIUM / HIGH

Only report when the messaging platform's delivery/redelivery behavior
supports the finding.

---

# MSG-031 — Message Ordering Dependency Without Enforcement

## Rule

Flag business operations that require ordered events but have no
mechanism to preserve or enforce the required ordering.

## Severity

HIGH

Use when ordering violations can cause incorrect business state.

---

# MSG-032 — Incorrect Partition/Consumer Assumption

## Rule

Where the messaging platform supports partitions, groups, queues, or
similar concepts, flag assumptions about message ownership or ordering
that are not supported by the actual configuration.

## Severity

MEDIUM / HIGH

Only report when the messaging technology provides sufficient evidence.

---

# MSG-033 — Message Transformation Corrupts Metadata

## Rule

Flag message transformations that unnecessarily discard metadata required
for:

- acknowledgement
- correlation
- routing
- tracing
- deduplication
- downstream processing

## Severity

MEDIUM / HIGH

---

# MSG-034 — Incorrect Message Routing

## Rule

Flag routing logic that can send messages to the wrong destination or
incorrectly classify messages.

Consider:

- message type
- event type
- tenant
- environment
- business key
- error category

## Severity

HIGH

---

# MSG-035 — Message Routing Loop

## Rule

Flag routing configurations that can cause a message to repeatedly
circulate between queues, topics, flows, or error destinations.

## Severity

HIGH

Escalate when this can create uncontrolled message volume.

---

# MSG-036 — Missing Schema Validation

## Rule

Flag important message consumers that accept externally produced
messages without appropriate validation when malformed messages can cause
incorrect processing.

Consider:

- required fields
- schema version
- data types
- event type
- business validation

## Severity

MEDIUM / HIGH

Do not require duplicate validation when the upstream platform provides
reliable schema enforcement and repository evidence demonstrates it.

---

# MSG-037 — Incompatible Message Contract

## Rule

Flag producer or consumer changes that are incompatible with the existing
message contract.

Consider:

- removed fields
- renamed fields
- changed data types
- changed required fields
- changed event semantics
- incompatible schema version

## Severity

HIGH

---

# MSG-038 — Missing Message Versioning

## Rule

Flag message contract changes where existing consumers may receive an
incompatible message and there is no visible compatibility or versioning
strategy.

## Severity

MEDIUM / HIGH

Only report when compatibility is required by the architecture.

---

# MSG-039 — Incorrect Message Content Type

## Rule

Flag message processing where content type, encoding, or serialization
behavior can cause incorrect interpretation by consumers.

## Severity

MEDIUM

---

# MSG-040 — Oversized Message

## Rule

Flag messaging behavior that can produce or consume messages large enough
to create realistic:

- memory pressure
- broker limitations
- network overhead
- processing latency
- downstream failures

## Severity

MEDIUM / HIGH

Use repository evidence regarding payload size or broker limits.

---

# MSG-041 — Large Payload Logging

## Rule

Flag logging of complete message payloads when payloads can be large and
the logging provides limited operational value.

## Severity

LOW / MEDIUM

Escalate when sensitive information is exposed.

---

# MSG-042 — Message Publication Without Failure Handling

## Rule

Flag critical message publication where a failed publish can cause:

- lost business events
- inconsistent state
- incomplete processing

Consider:

- retry
- transactional publishing
- outbox pattern
- durable persistence
- reconciliation

## Severity

HIGH

Do not require distributed transactions when the architecture uses an
intentional eventual-consistency pattern.

---

# MSG-043 — Database Commit Before Message Publication

## Rule

Flag workflows where database state is committed but required message
publication can subsequently fail, resulting in inconsistent state, when
no recovery or reconciliation mechanism exists.

## Severity

HIGH

Consider:

- transactional messaging
- outbox pattern
- retry
- reconciliation
- eventual consistency

---

# MSG-044 — Message Publication Before Database Commit

## Rule

Flag workflows where a message is published before the database
transaction commits and consumers can observe business state that may
subsequently roll back.

## Severity

HIGH

Only report when the message semantics require committed database state.

---

# MSG-045 — Missing Outbox or Equivalent Reliability Pattern

## Rule

Where reliable database-to-message publication is a demonstrated
architectural requirement, flag designs that can permanently lose an
event between database commit and message publication without an
appropriate recovery mechanism.

## Severity

HIGH

Do not require the outbox pattern for every database/message integration.

---

# MSG-046 — Incorrect Transaction Scope

## Rule

Flag transaction scopes that do not include the operations that must be
atomic for the messaging business process.

Consider:

- database operations
- message acknowledgement
- message publication
- external side effects

## Severity

HIGH

---

# MSG-047 — Transaction Scope Too Broad

## Rule

Flag transactions that remain open while performing unnecessary:

- HTTP calls
- Salesforce operations
- SFTP operations
- long DataWeave transformations
- unrelated message processing

## Severity

MEDIUM / HIGH

Potential consequences include:

- lock contention
- connection exhaustion
- long transaction duration
- rollback complexity

---

# MSG-048 — Missing External Failure Handling

## Rule

Flag message consumers that do not appropriately handle realistic
downstream failures.

Examples:

- database unavailable
- HTTP timeout
- Salesforce unavailable
- rate limit
- authentication failure
- transient network error

## Severity

MEDIUM / HIGH

---

# MSG-049 — Authentication Failure Retried Indefinitely

## Rule

Flag messaging integrations that continuously retry authentication or
authorization failures without configuration correction or recovery.

## Severity

HIGH

This can create unnecessary downstream load and persistent message
backlog.

---

# MSG-050 — Rate-Limit Violation Risk

## Rule

Flag message consumers whose concurrency, retry, or batch behavior can
realistically exceed downstream rate limits.

Consider:

- HTTP APIs
- Salesforce
- SaaS platforms
- database capacity
- broker limits

## Severity

MEDIUM / HIGH

---

# MSG-051 — Missing Message Recovery Strategy

## Rule

Flag critical message processing where permanently failed messages cannot
be:

- identified
- recovered
- replayed
- quarantined
- reconciled

## Severity

MEDIUM / HIGH

---

# MSG-052 — Unsafe Replay

## Rule

Flag replay or reprocessing mechanisms that can repeat non-idempotent
business operations without appropriate controls.

## Severity

HIGH

Consider:

- duplicate detection
- business state checks
- replay markers
- idempotency keys

---

# MSG-053 — Replay of Permanently Invalid Message

## Rule

Flag recovery processes that repeatedly replay messages known to be
invalid without correction or quarantine.

## Severity

MEDIUM

---

# MSG-054 — Incorrect Message Retention Assumption

## Rule

Flag application behavior that assumes messages remain available for
replay or recovery longer than the configured broker retention period.

## Severity

MEDIUM / HIGH

Only report when repository configuration provides evidence of the
retention behavior.

---

# MSG-055 — Missing Monitoring for Message Backlog

## Rule

Flag critical asynchronous integrations where there is no reasonable
operational visibility into:

- queue depth
- consumer failures
- redelivery
- dead-letter volume
- processing latency

## Severity

MEDIUM

Do not require application code to implement monitoring when monitoring
is demonstrably provided by the deployment platform.

---

# MSG-056 — Missing Alerting for Dead-Letter Messages

## Rule

Flag critical message flows where dead-lettered or quarantined messages
can accumulate without an operational detection mechanism.

## Severity

MEDIUM

---

# MSG-057 — Incorrect Error Classification for Messaging

## Rule

Flag error handling that classifies retryable and non-retryable message
failures incorrectly.

Examples:

- validation failure retried indefinitely
- transient database failure permanently dead-lettered
- authorization failure treated as transient

## Severity

MEDIUM / HIGH

Coordinate with:

references/error-handling.md

---

# MSG-058 — Message Processing Without Business Idempotency

## Rule

Flag consumers that technically identify duplicate messages but still
perform duplicate business operations because the idempotency check is
not connected to the business side effect.

## Severity

HIGH

Example:

- duplicate detection occurs
- processing continues anyway
- downstream write is executed multiple times

---

# MSG-059 — Incorrect Idempotency Check Ordering

## Rule

Flag idempotency implementations where the duplicate check occurs after
the non-idempotent business side effect.

## Severity

HIGH

The idempotency decision must occur before the relevant side effect when
required by the business process.

---

# MSG-060 — Race Condition in Idempotency

## Rule

Flag idempotency implementations where concurrent consumers can both
pass the duplicate check before either records the message as processed.

## Severity

HIGH

Consider:

- Object Store
- database uniqueness
- distributed locking
- atomic operations
- multiple Mule workers

---

# MSG-061 — Incorrect Object Store Idempotency

## Rule

When Object Store is used for message deduplication, flag configurations
or usage that do not provide the required durability, visibility, or
retention characteristics.

Consider:

- persistent versus non-persistent storage
- worker topology
- key uniqueness
- expiration
- deployment behavior

## Severity

HIGH

Only report when repository evidence supports the concern.

---

# MSG-062 — Message Processing State Stored Locally

## Rule

Flag message processing state stored only in local memory when the
application can process messages across:

- multiple workers
- multiple replicas
- restarts
- redeployments

## Severity

HIGH

---

# MSG-063 — Incorrect Acknowledgement After Downstream Timeout

## Rule

Flag processing where a downstream timeout is treated as definite
failure and the message is acknowledged even though the downstream
operation may have completed.

This is particularly important for non-idempotent operations.

## Severity

HIGH

---

# MSG-064 — Duplicate Side Effect After Timeout

## Rule

Flag retry behavior where a timeout does not establish whether the
downstream operation succeeded and the retry can therefore create a
duplicate business effect.

## Severity

HIGH

Consider:

- HTTP POST
- database insert
- Salesforce create
- payment-like operations
- external message publication

---

# MSG-065 — Missing Reconciliation

## Rule

Flag critical asynchronous integrations where ambiguous outcomes can
occur but there is no visible reconciliation mechanism.

Examples:

- message accepted but downstream result unknown
- database committed but event publication uncertain
- external API timeout after request submission

## Severity

MEDIUM / HIGH

Only report when ambiguous outcomes are realistic.

---

# MSG-066 — Incorrect Message Priority Handling

## Rule

Where message priority is part of the business requirement, flag
processing that can violate the required priority semantics.

## Severity

MEDIUM

Do not assume priority requirements without repository evidence.

---

# MSG-067 — Tenant Isolation Failure

## Rule

Flag messaging logic that can route or process one tenant's messages
using another tenant's configuration, credentials, or business context.

## Severity

CRITICAL / HIGH

Only report when multi-tenant behavior is evident from the repository.

---

# MSG-068 — Incorrect Environment Routing

## Rule

Flag message configuration that can publish or consume from the wrong
environment.

Examples:

- test consumer connected to production queue
- production flow publishing to development destination
- unsafe default broker configuration

## Severity

CRITICAL / HIGH

---

# MSG-069 — Hardcoded Messaging Configuration

## Rule

Flag environment-specific messaging values embedded directly in source.

Examples:

- queue names
- topic names
- broker URLs
- ports
- environment-specific credentials

## Severity

MEDIUM

Escalate when secrets are involved.

---

# MSG-070 — Missing Secure Messaging Configuration

## Rule

Flag messaging authentication credentials that are stored outside
appropriate secure configuration mechanisms.

## Severity

HIGH

Coordinate with:

references/security.md

---

# MSG-071 — Incorrect Connector Version Compatibility

## Rule

Flag messaging connector versions that are incompatible with the Mule
runtime or other project dependencies when repository evidence supports
the incompatibility.

## Severity

HIGH

Do not recommend upgrades merely because newer versions exist.

---

# MSG-072 — Missing MUnit Coverage for Message Failure

## Rule

Flag critical message-processing behavior without meaningful tests for:

- acknowledgement failure
- redelivery
- duplicate delivery
- downstream failure
- retry exhaustion
- dead-letter behavior
- idempotency

## Severity

MEDIUM

Do not require every messaging scenario to have an individual test.

---

# MSG-073 — MUnit Test Does Not Verify Message Outcome

## Rule

Flag tests that execute message-processing flows but do not verify
important outcomes such as:

- successful processing
- acknowledgement behavior
- downstream invocation
- duplicate suppression
- error routing
- retry behavior

## Severity

LOW / MEDIUM

---

# MSG-074 — Message Contract Validation Gap

## Rule

Flag important event consumers where malformed or incompatible messages
can reach business processing without appropriate validation.

## Severity

MEDIUM / HIGH

Coordinate with:

references/api.md

---

# MSG-075 — Incorrect Content-Type or Encoding

## Rule

Flag message producers or consumers where content type, encoding, or
serialization configuration can cause consumers to interpret messages
incorrectly.

## Severity

MEDIUM

---

# MSG-076 — Message Size Causes Resource Risk

## Rule

Flag messaging implementations that unnecessarily materialize very large
messages or make multiple copies of large payloads.

Consider:

- DataWeave transformations
- logging
- variables
- batch processing
- Object Store
- downstream calls

## Severity

MEDIUM / HIGH

Coordinate with:

references/dataweave.md

references/performance.md

---

# MSG-077 — Unnecessary Message Transformation

## Rule

Flag transformations that provide no meaningful business or contract
value and materially increase:

- processing time
- memory usage
- complexity

## Severity

LOW / MEDIUM

Do not report stylistic transformation preferences.

---

# MSG-078 — Excessive Message Processing Time

## Rule

Flag message processing that performs unnecessarily long synchronous
operations and can cause:

- acknowledgement timeout
- redelivery
- consumer backlog
- worker saturation

## Severity

MEDIUM / HIGH

Consider downstream calls and transaction duration.

---

# MSG-079 — Blocking Operation in High-Volume Consumer

## Rule

Flag high-volume message consumers performing blocking operations that
can materially restrict throughput.

Examples:

- sequential external calls
- long database operations
- unnecessary synchronous waits

## Severity

MEDIUM / HIGH

Only report when message volume or throughput requirements are supported
by repository evidence.

---

# MSG-080 — Messaging Production Readiness Gap

## Rule

Flag critical messaging integrations that lack one or more essential
operational controls supported by the application's requirements.

Consider:

- failure recovery
- idempotency
- retry strategy
- dead-letter handling
- monitoring
- alerting
- replay
- reconciliation
- operational documentation

## Severity

MEDIUM / HIGH

Do not report missing operational controls when they are demonstrably
provided outside the repository.

---

# Messaging Finding Quality Gate

Before reporting a messaging finding:

1. Identify the messaging technology.
2. Identify the producer or consumer.
3. Inspect source configuration.
4. Inspect acknowledgement behavior.
5. Inspect error handling.
6. Inspect retry and redelivery behavior.
7. Inspect transaction boundaries.
8. Inspect downstream side effects.
9. Inspect idempotency behavior.
10. Inspect dead-letter behavior.
11. Inspect ordering requirements.
12. Inspect concurrency.
13. Inspect message retention.
14. Inspect related Object Store/database usage.
15. Inspect related MUnit tests.
16. Verify whether the issue is already handled.
17. Confirm realistic impact.
18. Confirm severity.
19. Identify exact file and location.

If evidence is insufficient, do not report the issue.

---

# Messaging False-Positive Controls

Do not report:

- duplicate delivery as a defect by itself
- missing idempotency when the operation is demonstrably idempotent
- missing ordering when ordering is not a business requirement
- missing transactions when eventual consistency is intentional
- missing dead-letter queues when the platform provides equivalent
  recovery handling
- missing retry when failures are intentionally propagated
- concurrency simply because multiple consumers exist
- missing monitoring when monitoring is clearly implemented outside the
  repository
- missing outbox patterns when reliable database-to-message atomicity is
  not required
- message size concerns without evidence of problematic payload size
- performance concerns without a reasonable mechanism
- message versioning when compatibility is demonstrably maintained
- duplicate findings for the same underlying idempotency or retry issue

---

# Cross-Reference Rules

Coordinate messaging findings with:

- references/error-handling.md
- references/security.md
- references/database.md
- references/connectors.md
- references/dataweave.md
- references/performance.md
- references/munit.md
- references/api.md

Do not report the same root cause as multiple independent findings unless
the impacts are materially different.

---

# Messaging Finding Format

Use:

**Finding ID:** MSG-001

**Severity:** HIGH

**Category:** MESSAGING

**File:** `src/main/mule/example.xml:125`

**Messaging Technology:** Anypoint MQ / JMS / VM / Kafka / Other

**Flow:** `example-consumer-flow`

**Location:** `message source / processor`

**Problem:**

Describe the messaging problem.

**Evidence:**

Identify the relevant source configuration, flow, processor, error
handler, or test evidence.

**Technical Mechanism:**

Explain how the messaging behavior creates the problem.

**Impact:**

Explain realistic production, business, reliability, data-integrity,
or performance impact.

**Recommendation:**

Provide an actionable remediation approach.

**Confidence:** HIGH / MEDIUM / LOW