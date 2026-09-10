# Performance Review Rules

## Purpose

Review MuleSoft applications for performance risks that can materially
affect:

* memory consumption
* CPU utilization
* throughput
* latency
* worker stability
* downstream systems
* database load
* message-processing capacity
* scalability
* operational reliability

Performance findings must be based on repository evidence and a
credible technical mechanism.

Do not report speculative performance concerns as confirmed defects.

---

# Performance Classification

Every material performance observation must be classified as one of:

## CONFIRMED

Repository behavior directly demonstrates the problematic processing
pattern and its production impact can reasonably be established from the
available evidence.

Examples:

* a collection is iterated and an external request is made for every
  element
* an unbounded database result is loaded into memory
* the full payload is repeatedly copied or transformed
* a retry configuration can demonstrably multiply external calls

## MECHANISM-BASED RISK

The repository demonstrates a technically credible performance
mechanism, but runtime measurements, production volumes, or infrastructure
capacity are unavailable.

Examples:

* a potentially large payload is fully materialized
* a nested transformation has complexity that can grow significantly
* sequential processing is used where the visible workload can scale

These findings must clearly state the missing runtime evidence.

## SPECULATIVE

There is insufficient evidence to establish a credible production
mechanism.

Speculative observations must **not** be reported as findings.

Where useful, record the uncertainty as a review limitation.

---

# Performance Review Principles

Before reporting a performance finding:

1. Identify the relevant flow.
2. Identify the workload/input.
3. Determine whether workload size is bounded or unbounded.
4. Inspect DataWeave transformations.
5. Inspect loops and repeated operations.
6. Inspect external calls.
7. Inspect database calls.
8. Inspect payload handling and streaming.
9. Inspect logging.
10. Inspect retries.
11. Inspect concurrency and parallelism.
12. Inspect blocking operations.
13. Inspect downstream dependencies.
14. Inspect configuration affecting resource consumption.
15. Determine scaling behavior.
16. Determine production impact.
17. Assign classification, severity, and confidence.

Performance analysis should consider the entire processing path.

---

# PERF-001 — Large Payload Memory Risk

## Description

Application processing can require excessive memory because large payloads
are fully materialized, duplicated, transformed repeatedly, or otherwise
held in memory unnecessarily.

Potential mechanisms include:

* non-streaming processing
* repeated payload copies
* multiple large intermediate structures
* materialization of large collections
* full payload logging
* large aggregation operations
* conversion of streaming data into in-memory structures

## Finding Gate

Establish:

* potentially large input,
* an operation that materializes or duplicates that input,
* a credible memory-growth mechanism,
* and meaningful production impact.

Do not report large payload risk merely because the application processes
HTTP or messaging payloads.

Consider whether:

* payload size is bounded
* streaming is already enabled
* the connector provides streaming
* processing is incremental
* the transformation necessarily requires materialization

## Evidence Requirements

Identify:

* source flow
* payload-handling operation
* streaming configuration where relevant
* materialization/copy mechanism
* credible memory consequence

---

# PERF-002 — N+1 External Calls

## Description

An external service is called repeatedly for individual elements of a
collection, causing request volume to grow with input size.

Typical pattern:

```text id="x7v3ka"
Retrieve collection
       |
       +--> HTTP/API call for item 1
       +--> HTTP/API call for item 2
       +--> HTTP/API call for item 3
       ...
```

## Finding Gate

Establish:

1. a collection can contain multiple elements,
2. an external call occurs within repeated processing,
3. call volume grows with collection size, and
4. the resulting latency, load, rate-limit, or reliability impact is
   meaningful.

Consider:

* batching APIs
* bulk endpoints
* caching
* concurrency
* bounded collection size
* rate limits
* retry behavior

Do not report N+1 merely because a call occurs inside a loop.

## Evidence Requirements

Identify:

* collection source
* iteration mechanism
* external connector/request
* expected call amplification
* production impact

---

# PERF-003 — N+1 Database Calls

## Description

A database operation is executed repeatedly for individual records or
nested elements, causing database query volume to grow with input size.

This finding may overlap with `DB-003`.

## Finding Gate

Use `PERF-003` when the primary concern is performance/scalability.

Use `DB-003` when the primary concern is the database access pattern.

Do not create both findings unless the root causes, impacts, or
remediation actions materially differ.

Establish:

* repeated database execution,
* collection-driven growth,
* meaningful query amplification,
* credible production impact.

## Evidence Requirements

Identify:

* initial collection/query
* iteration
* repeated database operation
* query amplification
* production consequence

---

# PERF-004 — Unbounded Processing

## Description

Application processing can grow without an effective bound, creating a
credible risk of excessive execution time, memory consumption, worker
utilization, downstream load, or operational instability.

Potential mechanisms include:

* unbounded collections
* unbounded pagination
* processing all available records
* unbounded message accumulation
* unrestricted recursive processing
* unbounded polling
* large batch sizes
* loops without meaningful termination controls

## Finding Gate

Establish:

* what can grow,
* why it can grow,
* how processing scales,
* what resource is consumed,
* and what production consequence can occur.

Do not report an operation as unbounded when an effective limit exists
elsewhere in the processing path.

Inspect:

* query limits
* pagination
* batch size
* maximum records
* streaming
* queue limits
* timeout controls
* upstream constraints

---

# PERF-005 — Excessive Logging

## Description

Logging behavior creates measurable or credible production overhead
through excessive volume, expensive payload serialization, repeated
logging, or inappropriate log levels.

This finding may overlap with `LOG-004`.

## Finding Gate

Establish a meaningful production mechanism such as:

* full payload logging on high-volume flows
* logging inside large collection loops
* repeated logging of the same event
* expensive serialization performed only for logging
* debug/trace logging enabled for production-scale processing

Do not report logging merely because multiple log statements exist.

## Evidence Requirements

Identify:

* logging location
* execution frequency
* logged data/operation
* likely overhead
* production consequence

Use `LOG-004` when the primary issue is logging/observability.

Use `PERF-005` when the primary issue is measurable or credible
performance/resource overhead.

Avoid duplicate findings unless the concerns materially differ.

---

# PERF-006 — Inefficient Processing

## Description

Processing logic performs unnecessary or inefficient work that can
materially affect production performance.

Potential mechanisms include:

* repeated transformations
* unnecessary serialization/deserialization
* repeated parsing
* redundant collection traversal
* nested iteration with avoidable complexity
* sequential processing of independent work
* unnecessary payload reconstruction
* repeated lookups
* blocking operations
* avoidable intermediate structures

## Finding Gate

Do not report an implementation simply because it is not optimal.

Establish:

1. the unnecessary or inefficient operation,
2. how its cost grows with workload,
3. why the work is avoidable or materially inefficient, and
4. a credible production consequence.

Where possible, describe complexity qualitatively or quantitatively,
for example:

```text id="8r6h1s"
O(n)
O(n²)
O(n × external-call-cost)
```

Only use complexity notation when the repository behavior supports it.

---

# DataWeave Performance

Coordinate performance analysis with the DataWeave reference.

Inspect:

* nested `map`
* nested `filter`
* repeated `map`/`filter` passes
* `groupBy`
* `orderBy`
* `distinctBy`
* joins
* flattening
* repeated parsing
* repeated transformations
* large intermediate objects
* streaming compatibility

Do not assume a particular DataWeave operation is inefficient without
considering input size and actual execution context.

A transformation that is appropriate for a small bounded collection may
be inappropriate for a large unbounded collection.

---

# Streaming

Determine whether the processing path preserves streaming where it
matters.

Inspect:

* source connector
* transformation behavior
* downstream processors
* collection materialization
* repeated payload access
* operations requiring full materialization

Do not report missing streaming solely because streaming is not
explicitly configured.

First determine whether:

* input can be large,
* the connector supports streaming,
* downstream processing benefits from it,
* and the current implementation creates materialization risk.

---

# Payload Copies

Inspect for:

* assigning large payloads to multiple variables
* unnecessary transformations between equivalent formats
* repeated serialization
* reconstruction of large objects
* retaining large values longer than required

A variable assignment is not automatically a memory defect.

Report only when there is a credible materialization or retention
mechanism with meaningful impact.

---

# External Call Performance

Inspect:

* repeated HTTP/API calls
* sequential calls
* connection configuration
* timeout
* retry
* rate limits
* batching
* caching
* concurrency

Consider whether performance problems can also create reliability
problems.

For example:

```text id="v0x3pn"
Large input
   |
   v
Sequential external calls
   |
   v
Long execution time
   |
   v
Timeout
   |
   v
Retry
   |
   v
Duplicate external calls
```

When multiple findings describe the same root cause, select the most
appropriate finding and avoid duplication.

---

# Sequential Processing

Sequential processing is not automatically a defect.

Before reporting a sequential-processing concern, establish:

* operations are independent,
* workload can scale materially,
* parallel processing is technically appropriate,
* downstream systems can safely support concurrency,
* ordering is not required,
* concurrency would provide meaningful benefit.

Do not recommend parallelization where it could introduce:

* ordering problems
* race conditions
* duplicate processing
* rate-limit violations
* database contention
* resource exhaustion

---

# Concurrency

Inspect:

* parallel scopes
* asynchronous processing
* concurrent consumers
* worker concurrency
* batch concurrency
* shared mutable state
* downstream capacity

Consider both sides of concurrency:

**Too little concurrency**

* poor throughput
* unnecessary latency

**Too much concurrency**

* resource exhaustion
* downstream overload
* rate-limit breaches
* connection exhaustion
* database contention

A concurrency setting is not inherently correct or incorrect.

---

# Blocking Operations

Inspect for operations that can block processing for significant
periods, including:

* slow external calls
* database operations
* file operations
* synchronous polling
* long waits
* inefficient loops

Establish the timeout and failure behavior where relevant.

Do not report a blocking operation solely because it is synchronous.

---

# Retry and Performance Amplification

Coordinate with Error Handling and Connector/Messaging references.

Inspect whether:

* retries multiply external calls,
* retries multiply database operations,
* redelivery multiplies processing,
* retry storms can occur,
* backoff is absent or insufficient,
* permanent failures consume significant worker capacity.

When the primary defect is unsafe retry behavior, use the appropriate
`ERR-004`, `CON-003`, or `MSG-004` finding instead of creating a
duplicate performance finding.

Use a performance finding when the distinct production concern is
resource/throughput impact.

---

# Database Coordination

Coordinate with:

* `DB-002` — Inefficient query
* `DB-003` — N+1 database access
* `DB-004` — Unbounded result retrieval
* `DB-006` — Connection/resource risk

Do not duplicate findings where the same root cause and remediation
apply.

---

# Logging Coordination

Coordinate with:

* `LOG-001`
* `LOG-002`
* `LOG-004`

Sensitive information remains a security/logging concern even when it
also creates performance overhead.

Do not expose sensitive payloads merely to demonstrate logging volume.

---

# Performance Evidence Hierarchy

Prefer evidence in this order:

1. Directly observable repository behavior
2. Explicit workload/configuration limits
3. Flow and connector execution patterns
4. DataWeave processing structure
5. Dependency/configuration evidence
6. Strong technical mechanism
7. Runtime measurements, when available
8. Assumptions

Assumptions alone must not support a performance finding.

If runtime metrics are unavailable, explicitly distinguish a
mechanism-based risk from a confirmed performance defect.

---

# Severity Guidance

Severity must reflect actual production impact.

## CRITICAL

Use only for highly credible performance behavior likely to cause:

* widespread worker failure
* severe resource exhaustion
* major production outage
* catastrophic downstream overload

## HIGH

Use for:

* severe memory exhaustion risk
* major unbounded processing
* severe N+1 amplification
* highly likely worker instability
* severe downstream overload

## MEDIUM

Use for:

* meaningful N+1 processing
* credible large-payload memory risk
* material unbounded processing
* significant inefficient processing
* meaningful excessive logging overhead
* substantial throughput/latency degradation

## LOW

Use for:

* limited performance concerns
* lower-impact inefficiencies
* localized optimization opportunities with some production relevance

## NIT

Use only for optional optimization without material production impact.

---

# Confidence Guidance

## HIGH

Use when:

* the problematic processing path is directly visible,
* the scaling mechanism is clear,
* relevant configuration is visible,
* and the production consequence is strongly established.

## MEDIUM

Use when:

* the mechanism is clear,
* but workload, runtime measurements, or infrastructure capacity are
  unavailable.

## LOW

Use only when the risk is meaningful but important repository evidence is
missing.

Avoid LOW-confidence performance findings unless the potential impact
justifies surfacing the uncertainty.

---

# False-Positive Controls

Do not create a performance finding when:

* workload is demonstrably bounded,
* streaming already mitigates the memory concern,
* pagination/batching already bounds processing,
* caching or batching eliminates the repeated-call concern,
* the collection is known to be small from repository evidence,
* concurrency is intentionally constrained for correctness,
* sequential processing is required by ordering or dependency constraints,
* retries are appropriately bounded,
* logging volume is justified and bounded,
* another component already mitigates the performance risk,
* the issue is purely theoretical,
* runtime behavior cannot support the claimed impact,
* evidence is insufficient.

When evidence is insufficient:

**Do not report the finding.**

Record the limitation where relevant.

---

# Positive Performance Indicators

Where supported by evidence, recognize strengths such as:

* streaming large payloads
* bounded result retrieval
* effective pagination
* efficient set-based database access
* batching
* appropriate concurrency
* controlled retry/backoff
* efficient DataWeave transformations
* avoidance of unnecessary payload copies
* appropriate external-call aggregation
* caching where justified
* controlled logging
* explicit workload limits

Positive observations must be evidence-backed.

---

# Required Finding Fields

Any performance finding must include:

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
* Performance Classification

`Performance Classification` must be one of:

* CONFIRMED
* MECHANISM-BASED RISK

`SPECULATIVE` observations must not be included as findings.

Evidence excerpts must remain faithful to repository content.

Never include:

* passwords
* API keys
* access tokens
* private keys
* authorization headers
* secure property values
* sensitive production payloads

Sensitive information must be sanitized before inclusion in the review
artifact.