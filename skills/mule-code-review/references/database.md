# Database Review Rules

## Purpose

Review MuleSoft database access for:

* SQL injection
* SQL correctness
* query efficiency
* N+1 access patterns
* result-set size
* pagination
* connection pooling
* connection/resource lifecycle
* timeouts
* transaction boundaries
* commit/rollback behavior
* error handling
* concurrency
* data consistency
* database failure behavior

Database findings must be based on repository evidence and a credible
production consequence.

Do not report a database pattern merely because another implementation
could be more efficient.

---

# Database Review Principles

Before reporting a database finding:

1. Identify the database connector.
2. Identify the relevant operation.
3. Inspect the SQL or query expression.
4. Inspect parameterization.
5. Inspect DataWeave used to construct inputs.
6. Inspect referenced properties/configuration.
7. Inspect transaction boundaries.
8. Inspect connection/pool configuration.
9. Inspect timeout configuration.
10. Inspect result handling.
11. Inspect pagination or batching.
12. Inspect surrounding error handling.
13. Inspect calling loops and flow structure.
14. Inspect MUnit/tests where relevant.
15. Determine actual production impact.
16. Assign severity and confidence based on evidence.

Trace database access across flow boundaries rather than inspecting a
single database operation in isolation.

---

# DB-001 — SQL Injection

## Description

User-controlled or otherwise untrusted input is incorporated into SQL in
a way that allows the resulting SQL statement to be altered
unexpectedly.

Potential mechanisms include:

* string concatenation
* expression-based SQL construction
* interpolation into SQL text
* dynamically constructed WHERE clauses without safe parameterization

## Finding Gate

Establish that:

1. untrusted or externally influenced data can reach the SQL expression,
2. the data changes SQL syntax rather than only a bound parameter value,
   and
3. the database operation executes the resulting SQL.

Do not report dynamic SQL automatically as SQL injection.

Dynamic SQL may be legitimate when all structural components are
controlled and values are safely parameterized.

## Evidence Requirements

Identify:

* input source
* SQL construction
* database operation
* parameterization mechanism
* credible injection path

Never include sensitive input values.

## Impact Examples

Potential impacts include:

* unauthorized data access
* data modification
* data deletion
* authentication bypass
* database compromise

---

# DB-002 — Inefficient Query

## Description

A database query or access pattern has a credible performance problem
that can materially affect production behavior.

Potential mechanisms include:

* unnecessary joins
* repeated expensive expressions
* non-selective queries
* functions preventing effective index usage
* unnecessary columns
* avoidable repeated database access
* inefficient filtering
* excessive sorting
* inefficient pagination

## Finding Gate

Do not report a query as inefficient based solely on style.

Evidence should establish a credible mechanism such as:

* large data volume
* repeated execution
* expensive query structure
* missing filtering
* known schema/index evidence
* application execution pattern

Where database schema or execution plans are unavailable, keep the
finding conservative.

## Evidence Requirements

Identify:

* query
* execution location
* relevant access pattern
* data-volume mechanism where known
* production consequence

---

# DB-003 — N+1 Database Access

## Description

The application executes one database query to obtain a collection of
records and then performs additional database queries for individual
records or nested elements, creating potentially excessive query volume.

Typical pattern:

```text
Query parent records
       |
       +--> Query child for record 1
       +--> Query child for record 2
       +--> Query child for record 3
       ...
```

## Finding Gate

The pattern alone is not sufficient.

Establish:

* the outer collection can contain multiple records,
* a database operation occurs inside the iteration or equivalent repeated
  execution path, and
* query volume can grow materially with input size.

Consider whether:

* batching exists
* joins are used
* caching exists
* the result set is bounded
* the number of records is inherently small

## Evidence Requirements

Identify:

* initial query
* iteration mechanism
* repeated query
* query amplification
* credible production impact

---

# DB-004 — Unbounded Result Retrieval

## Description

A database operation retrieves a potentially large or unbounded result
set without adequate filtering, pagination, batching, streaming, or
other controls.

Potential consequences include:

* excessive memory consumption
* long processing times
* database load
* network utilization
* worker instability
* downstream overload

## Finding Gate

Do not report every query without an explicit LIMIT as unsafe.

Consider:

* known or likely data volume
* filtering
* pagination
* streaming
* batch processing
* connector behavior
* downstream processing
* execution frequency

If repository evidence cannot establish potentially large results, do not
create a finding.

## Evidence Requirements

Identify:

* query
* result-set characteristics
* absence/presence of bounding mechanism
* processing behavior
* credible production impact

---

# DB-005 — Unsafe Transaction Behavior

## Description

Transaction configuration or transaction boundaries can produce
incorrect commit/rollback behavior, partial processing, inconsistent
state, or misleading success/failure behavior.

Potential mechanisms include:

* database update outside an intended transaction
* incorrect transaction scope
* rollback not occurring after a database failure
* error continuation causing partial commit
* transaction boundary that does not include related database operations
* assumptions that external systems participate in the same transaction

## Finding Gate

Determine the actual transaction boundary.

Inspect:

* transaction scope
* transaction action
* connector transaction support
* error handling
* nested flow behavior
* commit/rollback behavior
* database operations before and after failures
* external side effects

Do not assume that two operations are transactional merely because they
occur in the same Mule flow.

Do not assume an external HTTP, SaaS, or messaging operation can be
rolled back by a database transaction.

## Evidence Requirements

Identify:

* transaction boundary
* affected database operations
* failure path
* commit/rollback behavior
* resulting consistency problem

---

# DB-006 — Connection/Resource Risk

## Description

Database access creates a credible risk of connection exhaustion,
resource contention, connection leakage, or unsafe connection-pool
behavior.

Potential mechanisms include:

* inappropriate pool size
* excessive concurrency
* long-running queries holding connections
* insufficient connection timeout
* blocked transactions
* resource retention
* connection creation exceeding database capacity

## Finding Gate

Do not report a pool configuration solely because it differs from a
generic recommended value.

Consider:

* connection pool size
* maximum connections
* concurrency
* query duration
* transaction duration
* execution frequency
* deployment scale where known
* database capacity where known
* timeout behavior

A finding requires a credible resource-exhaustion mechanism.

## Evidence Requirements

Identify:

* database configuration
* pool/resource settings
* relevant flow/query
* concurrency or execution mechanism
* production consequence

If workload information is unavailable and impact cannot be established,
record a limitation instead.

---

# SQL Parameterization

Inspect whether variable values are supplied through the database
connector's supported parameterization mechanism.

Distinguish:

**Safe value binding**

```text
SQL structure remains fixed
        +
input supplied as parameter
```

from:

**Potentially unsafe SQL construction**

```text
input
  |
  v
string concatenation/interpolation
  |
  v
SQL statement
```

Do not report SQL injection when the dynamic value is demonstrably
parameterized.

---

# SQL Correctness

Inspect for evidence of:

* incorrect joins
* incorrect predicates
* missing filters
* incorrect update/delete conditions
* incorrect null semantics
* incorrect parameter types
* incorrect ordering
* incorrect aggregation
* accidental broad updates/deletes

Only report correctness defects when repository evidence establishes the
expected behavior and demonstrates the discrepancy.

Do not infer business requirements that are not visible.

---

# Query Efficiency

Consider:

* filtering before retrieval
* appropriate joins
* unnecessary database round trips
* repeated queries
* query execution frequency
* result-set size
* sorting
* aggregation
* pagination

Where indexes or database schema are unavailable, do not claim that a
specific index is missing unless repository evidence establishes the
schema and expected access path.

---

# Pagination and Batching

Inspect operations that can retrieve or process large datasets.

Consider:

* database pagination
* connector pagination
* batch processing
* streaming
* bounded queries
* continuation tokens where applicable

Pagination is not automatically required.

Report a finding only when unbounded processing creates a credible
production consequence.

---

# Timeout Review

Inspect relevant timeout layers, including:

* connection timeout
* query timeout
* response timeout
* application-level timeout
* upstream request timeout

A timeout configured at one layer does not automatically protect all
other layers.

Do not report a missing explicit timeout if an effective safe timeout is
established elsewhere.

---

# Error Handling

Trace database failures through:

* Try scopes
* On Error Continue
* On Error Propagate
* global error handlers
* transaction scopes
* retry mechanisms
* response construction

Consider whether a database failure can result in:

* false success
* partial commit
* lost error context
* duplicate processing
* inconsistent state

Coordinate with the Error Handling reference to avoid duplicate
findings.

---

# Database and External Side Effects

Pay particular attention to flows such as:

```text
Database update
      |
      v
External API call
      |
      v
Message publication
```

Determine whether failure in a later step can leave the database in a
state that is inconsistent with external systems.

Do not assume a single Mule transaction provides distributed
transactionality across unrelated systems.

---

# Concurrency and Locking

Where repository evidence permits, inspect:

* concurrent updates
* transaction isolation
* long-running transactions
* repeated updates
* potential lock contention
* optimistic/pessimistic locking
* duplicate processing

Do not report a locking concern without a credible concurrent execution
path.

---

# Security Coordination

Coordinate database review with:

* Security
* Configuration
* Error Handling
* DataWeave

Use `SEC-007` for injection findings when the primary root cause is
security-related, or `DB-001` when the finding is specifically framed
as a database injection defect.

Avoid duplicate findings for the same root cause, impact, and
remediation.

Never expose:

* database passwords
* connection strings containing secrets
* access tokens
* secure property values

Mask sensitive configuration values in evidence.

---

# Severity Guidance

Severity must reflect actual production impact.

### CRITICAL

Use for:

* severe SQL injection enabling broad unauthorized access or destructive
  database operations
* highly likely catastrophic data loss/corruption

### HIGH

Use for:

* major SQL injection
* severe transaction defects causing substantial data inconsistency
* severe database resource exhaustion
* major query amplification with likely production instability

### MEDIUM

Use for:

* meaningful N+1 access
* realistic unbounded retrieval
* material query inefficiency
* significant transaction-boundary defects
* credible connection/resource risks

### LOW

Use for:

* limited database performance issues
* lower-impact resource/configuration concerns

### NIT

Use only for optional database improvements without material production
impact.

---

# False-Positive Controls

Do not create a database finding when:

* SQL values are safely parameterized
* dynamic SQL structure is fully controlled
* query volume is demonstrably bounded
* result size is demonstrably bounded
* pagination/streaming/batching already mitigates the risk
* transaction behavior is correct for the demonstrated requirement
* connection pooling is appropriate for the known workload
* timeout behavior is safely controlled elsewhere
* another component already mitigates the issue
* expected business behavior is not established
* evidence is insufficient

When evidence is insufficient:

**Do not report the finding.**

Record the limitation where relevant.

---

# Positive Database Indicators

Where supported by evidence, recognize strengths such as:

* parameterized SQL
* appropriate query filtering
* efficient set-based operations
* bounded result retrieval
* appropriate pagination
* controlled connection pooling
* explicit transaction boundaries
* correct rollback behavior
* appropriate database timeouts
* safe error propagation
* effective batching
* avoidance of N+1 access

Positive observations must be evidence-backed.

---

# Required Finding Fields

Any database finding must include:

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
* database secrets
* access tokens
* private keys
* secure property values
* sensitive production data

Sensitive information must be sanitized before inclusion in the review
artifact.