# Database Review Rules

## Purpose

These rules define how database integrations in Mule 4 applications must
be reviewed.

Review database behavior together with:

- Database Connector configuration
- SQL statements
- DataWeave transformations
- transaction scopes
- error handling
- retry behavior
- connection pooling
- pagination
- batch processing
- MUnit tests
- application properties
- secure configuration
- external system behavior

Do not report database issues based solely on coding preference.

A finding must be supported by repository evidence and have a realistic
production, security, correctness, reliability, or performance impact.

---

# Database Review Principles

Before reporting a database finding:

1. Identify the database operation.
2. Inspect the SQL.
3. Inspect the Database Connector configuration.
4. Inspect connection pooling.
5. Inspect timeout configuration.
6. Inspect transaction boundaries.
7. Inspect error handling.
8. Inspect retry behavior.
9. Inspect result-set size.
10. Inspect pagination or batching.
11. Inspect related DataWeave processing.
12. Inspect MUnit coverage.
13. Determine realistic production impact.

If database behavior cannot be established from the repository, inspect
related flows, properties, configuration, and tests before reporting.

---

# DB-001 — SQL Injection

## Rule

Flag SQL statements where untrusted or externally controlled input is
dynamically concatenated into SQL in a way that can alter query
semantics.

Examples:

- string concatenation with HTTP parameters
- dynamically constructed WHERE clauses
- user-controlled ORDER BY clauses
- user-controlled table or column names
- unsafe DataWeave-generated SQL

Prefer parameterized queries where supported.

## Severity

CRITICAL

Use HIGH when exploitability or exposure is constrained but the injection
risk is still real.

Do not report dynamic SQL merely because it is dynamic.

Verify whether the input is:

- parameterized
- validated
- allowlisted
- otherwise safely constrained

---

# DB-002 — Missing Transaction Boundary

## Rule

Flag missing transaction boundaries when multiple database operations
must succeed or fail atomically to preserve business consistency.

Examples:

- insert followed by update that must be atomic
- multiple related writes
- debit/credit operations
- state update plus business record creation

## Severity

HIGH

Do not require a transaction for independent operations.

---

# DB-003 — Incorrect Transaction Boundary

## Rule

Flag transaction boundaries that can produce:

- partial commits
- unexpected rollbacks
- inconsistent database state
- incorrect message/database coordination

Consider:

- Try scopes
- transaction configuration
- Database Connector operations
- messaging operations
- error handlers
- nested transactions

## Severity

HIGH

Escalate when incorrect behavior can cause data corruption or loss.

---

# DB-004 — N+1 Database Queries

## Rule

Flag database queries executed once per item in a collection when a
reasonable set-based, bulk, join, or batch approach exists.

Example:

    for each customer
        SELECT customer details

when the same information could reasonably be retrieved using a single
query.

## Severity

HIGH

Consider:

- collection size
- query complexity
- database capacity
- network latency
- production volume

Do not report when the individual query is required by business
semantics and no reasonable set-based alternative exists.

---

# DB-005 — Unbounded Result Set

## Rule

Flag queries that can return potentially unbounded or excessively large
datasets without appropriate controls.

Consider:

- missing WHERE clause
- missing LIMIT
- missing pagination
- large table scans
- full-table retrieval
- large historical datasets

## Severity

HIGH

Potential consequences include:

- memory exhaustion
- worker saturation
- long response times
- database load
- application instability

---

# DB-006 — Missing Pagination

## Rule

Flag database queries retrieving potentially large datasets without
pagination when pagination is appropriate for the use case.

Consider:

- API endpoints
- scheduled integrations
- batch processing
- reporting flows
- synchronization processes

## Severity

MEDIUM

Escalate to HIGH when large datasets can realistically cause production
failure.

Do not require pagination for inherently bounded datasets.

---

# DB-007 — Missing Timeout

## Rule

Flag database operations without an appropriate timeout strategy when
queries or connections can block indefinitely or for an uncontrolled
duration.

Consider:

- connection timeout
- query timeout
- response timeout
- transaction timeout
- pool acquisition timeout

## Severity

MEDIUM

Escalate to HIGH when missing timeouts can realistically cause:

- thread exhaustion
- connection exhaustion
- worker saturation
- cascading failures

---

# DB-008 — Inefficient Query

## Rule

Flag queries that have a reasonable mechanism for causing unnecessary
database load.

Examples:

- unnecessary full-table scans
- repeated queries
- avoidable joins
- selecting unnecessary columns
- inefficient filtering
- missing appropriate filtering
- functions preventing index usage
- inefficient sorting
- excessive aggregation

## Severity

MEDIUM / HIGH

Use HIGH when production data volume makes the performance impact
significant.

Do not claim that a query is inefficient without a reasonable mechanism
or repository evidence.

---

# DB-009 — Missing Query Parameterization

## Rule

Flag database operations where values that can be safely supplied as
parameters are instead constructed directly into SQL.

This rule overlaps with SQL injection but may also identify unsafe query
construction that is not currently exploitable.

## Severity

HIGH

If the issue is directly exploitable as SQL injection, report DB-001
instead of creating a duplicate finding.

---

# DB-010 — Excessive Selected Columns

## Rule

Flag queries that retrieve substantially more columns than required by
the application when this materially increases:

- network traffic
- database work
- memory consumption
- transformation cost

## Severity

LOW / MEDIUM

Only report when the impact is meaningful.

Do not report simply because SELECT * is stylistically undesirable.

---

# DB-011 — Missing WHERE Clause

## Rule

Flag UPDATE or DELETE statements without an appropriate restriction when
the operation can affect unintended rows.

## Severity

CRITICAL / HIGH

Use CRITICAL when repository evidence indicates a realistic possibility
of widespread destructive data modification.

---

# DB-012 — Unsafe UPDATE or DELETE

## Rule

Flag data modification statements where:

- predicates are incomplete
- identifiers are not sufficiently constrained
- business keys are ambiguous
- multiple rows can be unintentionally modified

## Severity

HIGH

Escalate when data corruption or large-scale modification is realistic.

---

# DB-013 — Incorrect Row Count Assumption

## Rule

Flag code that assumes a query or update affects exactly one row when
the SQL or schema does not guarantee that behavior.

Examples:

- treating zero rows as success
- treating multiple rows as impossible
- ignoring affected-row count for critical updates

## Severity

MEDIUM / HIGH

Use HIGH when incorrect assumptions can corrupt business state.

---

# DB-014 — Missing Existence/Concurrency Check

## Rule

Flag database operations that can incorrectly overwrite or duplicate
data because concurrent updates or existing records are not considered.

Consider:

- race conditions
- duplicate inserts
- check-then-insert patterns
- optimistic locking
- unique constraints
- concurrent message processing

## Severity

HIGH

Only report when concurrent execution is realistic.

---

# DB-015 — Duplicate Insert Risk

## Rule

Flag database writes that can create duplicate business records when
the operation may be retried or redelivered and no appropriate
idempotency or uniqueness mechanism exists.

Consider:

- messaging redelivery
- until-successful
- scheduler retries
- network timeouts
- application retries

## Severity

HIGH

Coordinate with:

- references/connectors.md
- references/messaging.md

Do not create duplicate findings for the same root cause.

---

# DB-016 — Missing Unique Constraint Dependency

## Rule

Flag application logic that relies on uniqueness but has no visible
database or application mechanism enforcing the uniqueness when
concurrent processing can violate the assumption.

Examples:

- check-then-insert
- business identifier uniqueness
- duplicate external reference

## Severity

MEDIUM / HIGH

Only report when repository evidence supports the uniqueness requirement.

---

# DB-017 — Long-Running Transaction

## Rule

Flag transactions that remain open while performing:

- slow external calls
- unnecessary DataWeave processing
- messaging operations
- file operations
- unrelated business logic

Potential consequences:

- database locks
- connection exhaustion
- transaction timeouts
- contention
- rollback complexity

## Severity

HIGH

---

# DB-018 — Transaction Scope Too Broad

## Rule

Flag transaction scopes that include operations that do not need to
participate in the database transaction.

Consider:

- HTTP calls
- Salesforce calls
- SFTP
- messaging
- long transformations

## Severity

MEDIUM / HIGH

Escalate when the scope can realistically cause lock contention or
transaction failure.

---

# DB-019 — Transaction Scope Too Narrow

## Rule

Flag transaction scopes that exclude database operations that must be
atomic for business correctness.

## Severity

HIGH

---

# DB-020 — Incorrect Rollback Behavior

## Rule

Flag error handling that allows failed database operations to commit or
prevents required rollback.

Consider:

- on-error-continue
- on-error-propagate
- Try scopes
- transaction configuration
- connector error types

## Severity

HIGH

Coordinate with:

references/error-handling.md

---

# DB-021 — Retry of Database Write

## Rule

Flag automatic retries of database writes when the operation may have
completed before a timeout or connection failure and retrying can create
duplicate or inconsistent data.

## Severity

HIGH

Consider:

- idempotency
- unique constraints
- transaction behavior
- affected-row checks

---

# DB-022 — Unsafe Database Retry

## Rule

Flag retry behavior that retries permanent database errors.

Examples:

- SQL syntax errors
- constraint violations
- invalid data
- authorization failures

## Severity

MEDIUM / HIGH

Retries should generally target transient failures.

---

# DB-023 — Retry Storm

## Rule

Flag multiple retry mechanisms that can multiply database load.

Consider:

- connector retry
- until-successful
- application retry
- scheduler retry
- messaging redelivery

## Severity

HIGH

Potential consequences:

- database overload
- connection exhaustion
- increased lock contention
- cascading failures

---

# DB-024 — Connection Pool Exhaustion Risk

## Rule

Flag connection pool configuration or usage that can realistically
exhaust available database connections.

Consider:

- maximum pool size
- concurrency
- long-running transactions
- slow queries
- leaked resources
- parallel processing

## Severity

HIGH

---

# DB-025 — Incorrect Connection Pool Configuration

## Rule

Flag pool settings that can cause:

- excessive connection creation
- connection starvation
- excessive idle connections
- database overload
- poor application concurrency

## Severity

MEDIUM

Escalate when production instability is likely.

---

# DB-026 — Connection Resource Leak

## Rule

Flag database usage that can fail to properly release connections,
cursors, statements, or other resources.

## Severity

HIGH

Potential consequences:

- pool exhaustion
- application degradation
- eventual outage

---

# DB-027 — Excessive Database Calls

## Rule

Flag flows that perform significantly more database operations than
required for a business transaction.

Examples:

- repeated lookup of the same data
- duplicate queries
- unnecessary validation queries
- repeated existence checks

## Severity

MEDIUM

Escalate to HIGH when the database impact is significant.

---

# DB-028 — Unnecessary Database Round Trip

## Rule

Flag database calls where equivalent information is already available
in the payload, variables, or previous query results and the additional
call provides no meaningful business value.

## Severity

LOW / MEDIUM

Only report when the extra operation has meaningful performance or
reliability impact.

---

# DB-029 — Missing Batch Processing

## Rule

Flag large numbers of individual database writes when a safe batch
operation could materially reduce database round trips.

## Severity

MEDIUM

Escalate when large production volumes make the behavior problematic.

Do not report when individual transactions or operations are required
by business semantics.

---

# DB-030 — Unsafe Batch Size

## Rule

Flag database batch operations with excessively large or uncontrolled
batch sizes that can cause:

- memory pressure
- long transactions
- lock contention
- transaction timeouts
- database overload

## Severity

MEDIUM / HIGH

---

# DB-031 — Missing Index Evidence

## Rule

Flag queries that rely on filtering or joining large datasets where
available repository/database evidence indicates required indexes are
missing.

## Severity

MEDIUM / HIGH

Only report when there is evidence supporting the indexing concern.

Do not assume an index is missing simply because the schema is not
available.

---

# DB-032 — Function Preventing Efficient Index Usage

## Rule

Flag query predicates that apply functions or transformations to indexed
columns in a way that can prevent efficient index usage, when this is
relevant to the database engine.

## Severity

MEDIUM

Only report when the database technology and query behavior support the
finding.

---

# DB-033 — Incorrect NULL Handling

## Rule

Flag SQL or application logic that incorrectly handles database NULL
values.

Consider:

- NULL comparisons
- default values
- nullable columns
- DataWeave conversion
- API response mapping

## Severity

MEDIUM

---

# DB-034 — Incorrect Data Type Handling

## Rule

Flag mismatches between database types and application/DataWeave types
that can cause:

- precision loss
- truncation
- conversion errors
- incorrect comparisons

Consider:

- decimal values
- timestamps
- dates
- UUIDs
- large integers
- binary data

## Severity

MEDIUM

---

# DB-035 — Incorrect Date/Time Handling

## Rule

Flag database date/time handling that can cause:

- timezone shifts
- incorrect comparisons
- loss of timezone information
- incorrect persistence
- incorrect API output

## Severity

MEDIUM

---

# DB-036 — Sensitive Data Exposure

## Rule

Flag database queries, logs, or transformations that unnecessarily expose:

- passwords
- tokens
- personal information
- financial information
- authentication data
- other sensitive business data

## Severity

HIGH

Coordinate with:

references/security.md

Do not duplicate the same root cause.

---

# DB-037 — Database Credentials Exposed

## Rule

Flag database credentials committed in:

- Mule XML
- properties
- DataWeave
- Maven configuration
- deployment configuration
- source code

## Severity

CRITICAL

Coordinate with:

references/security.md

---

# DB-038 — Incorrect Database Error Mapping

## Rule

Flag database errors that are mapped to incorrect application/API
responses.

Examples:

- constraint violation returned as HTTP 500 when a business conflict
  should be represented differently
- authentication failure treated as successful processing
- timeout exposed as a validation error

## Severity

MEDIUM / HIGH

Coordinate with:

references/error-handling.md

---

# DB-039 — Sensitive Database Error Exposure

## Rule

Flag database errors returned to external clients containing:

- SQL statements
- schema information
- table names
- database hostnames
- stack traces
- connection details
- internal implementation details

## Severity

HIGH

---

# DB-040 — Missing Database Failure Handling

## Rule

Flag important database operations that do not appropriately handle
realistic failures such as:

- connection failure
- timeout
- deadlock
- constraint violation
- unavailable database
- transient network failure

## Severity

MEDIUM / HIGH

Only report when the failure scenario is realistic and the application
requires explicit handling.

---

# DB-041 — Deadlock Risk

## Rule

Flag database access patterns that can realistically create deadlocks.

Consider:

- inconsistent lock ordering
- long transactions
- concurrent updates
- large update scopes
- multiple tables updated in different orders

## Severity

HIGH

Only report when repository evidence supports the risk.

---

# DB-042 — Lock Contention Risk

## Rule

Flag operations that can unnecessarily hold database locks for long
periods.

Examples:

- large transactions
- external calls inside transactions
- large updates
- long-running queries

## Severity

MEDIUM / HIGH

---

# DB-043 — Full Table Modification Risk

## Rule

Flag UPDATE or DELETE operations that can modify an entire table when
the business operation appears intended to target a subset of records.

## Severity

CRITICAL / HIGH

Use CRITICAL when catastrophic data modification is realistically
possible.

---

# DB-044 — Missing Optimistic Concurrency Protection

## Rule

Flag updates to shared business records where concurrent modification
can silently overwrite changes and no appropriate concurrency mechanism
exists.

Consider:

- version columns
- timestamps
- conditional updates
- database locking

## Severity

MEDIUM / HIGH

Only report when concurrent updates are realistic.

---

# DB-045 — Incorrect Generated Key Handling

## Rule

Flag insert operations where generated database identifiers are:

- ignored when required
- incorrectly retrieved
- incorrectly mapped
- associated with the wrong record

## Severity

MEDIUM / HIGH

---

# DB-046 — Incorrect Stored Procedure Usage

## Rule

Where stored procedures are used, review:

- parameter handling
- transaction behavior
- result-set handling
- error propagation
- timeout
- output parameters
- large results

## Severity

Use the severity appropriate to the actual issue.

---

# DB-047 — Database Operation Inside Unbounded Loop

## Rule

Flag database operations performed inside loops where the collection
can become large or unbounded.

Consider:

- N+1 queries
- N+1 writes
- transaction duration
- connection usage
- database load

## Severity

HIGH

---

# DB-048 — Missing Result Limiting

## Rule

Flag queries where the business operation requires only a limited number
of records but the query retrieves substantially more data.

Examples:

- existence checks retrieving full rows
- lookup requiring one record but retrieving all matches
- latest-record lookup without limiting results

## Severity

MEDIUM

---

# DB-049 — Inefficient Existence Check

## Rule

Flag existence checks that retrieve complete records or large result
sets when the application only needs to know whether a record exists.

## Severity

LOW / MEDIUM

Only report when the query cost is meaningful.

---

# DB-050 — Database Schema/Contract Mismatch

## Rule

Flag application SQL or mappings that are inconsistent with the
repository's available database schema, migrations, DDL, or documented
database contract.

Examples:

- nonexistent column
- incorrect column type
- incorrect table name
- incorrect constraint assumption

## Severity

HIGH

Only report when repository evidence supports the mismatch.

---

# DB-051 — Migration Compatibility Risk

## Rule

Where database migrations or schema changes are included, flag changes
that can break the currently deployed application.

Consider:

- column removal
- type changes
- non-null constraints
- incompatible indexes
- incompatible stored procedures
- deployment ordering

## Severity

HIGH

Only review migrations when they are present in the repository.

---

# DB-052 — Backward-Incompatible Schema Change

## Rule

Flag database schema changes that are incompatible with existing
application versions when rolling deployment or backward compatibility
is required by the repository's deployment model.

## Severity

HIGH

Do not assume zero-downtime deployment requirements without evidence.

---

# DB-053 — Missing Database Test Coverage

## Rule

Flag important database failure or transaction behavior that lacks
meaningful MUnit coverage when the behavior represents significant
production risk.

Consider:

- rollback
- duplicate insert
- constraint violation
- timeout
- database unavailable
- empty result
- multiple result rows

## Severity

MEDIUM

Do not require every SQL statement to have a dedicated test.

---

# DB-054 — Test That Does Not Verify Database Behavior

## Rule

Flag tests that execute database-related flows but do not meaningfully
assert:

- returned data
- affected records
- transaction outcome
- error behavior
- important business conditions

## Severity

LOW / MEDIUM

---

# DB-055 — Database Logging of Sensitive Data

## Rule

Flag logging that exposes:

- SQL containing sensitive values
- database credentials
- personal information
- financial information
- authentication information

## Severity

HIGH / CRITICAL

Coordinate with:

references/security.md

---

# DB-056 — Environment-Specific Database Configuration Hardcoded

## Rule

Flag database-specific environment values embedded directly in source.

Examples:

- database host
- database name
- port
- schema
- username
- environment-specific JDBC URL

## Severity

MEDIUM

Escalate when credentials or secrets are involved.

---

# DB-057 — Incorrect Database Environment Resolution

## Rule

Flag configuration that can cause an application to connect to the
wrong environment.

Examples:

- production deployment resolving test database
- missing environment property
- unsafe default database
- incorrect property precedence

## Severity

CRITICAL / HIGH

---

# DB-058 — Unsafe Database Default

## Rule

Flag defaults that can cause accidental connection to:

- localhost
- development database
- test database
- unintended production database

## Severity

HIGH

Escalate when destructive operations could be executed against the
wrong environment.

---

# DB-059 — Excessive Database Logging

## Rule

Flag unnecessary logging of complete SQL statements or large query
results when it provides limited diagnostic value.

## Severity

LOW / MEDIUM

Escalate when sensitive information is exposed.

---

# DB-060 — Database Observability Gap

## Rule

Flag critical database integrations where important operational
diagnostics are unavailable.

Consider:

- query/operation identification
- execution duration
- timeout
- failure type
- retry count
- transaction failures
- connection failures

## Severity

LOW / MEDIUM

Do not require SQL or sensitive data to be logged.

---

# Database Finding Quality Gate

Before reporting a database finding:

1. Identify the database operation.
2. Inspect the SQL.
3. Inspect parameters.
4. Inspect the connector configuration.
5. Inspect transaction scope.
6. Inspect error handling.
7. Inspect retry behavior.
8. Inspect result-set behavior.
9. Inspect pagination/batching.
10. Inspect connection pooling.
11. Inspect related DataWeave.
12. Inspect related tests.
13. Verify whether the issue is already handled.
14. Confirm realistic impact.
15. Confirm severity.
16. Identify exact file and location.

If evidence is insufficient, do not report the issue.

---

# Database False-Positive Controls

Do not report:

- missing transactions for independent operations
- pagination for inherently small/bounded datasets
- missing indexes without evidence
- query performance concerns without a reasonable mechanism
- connection pooling issues without workload/resource evidence
- retry concerns without understanding transaction/idempotency behavior
- concurrency problems when concurrent execution is not realistic
- SQL style preferences without production impact
- SELECT * solely as a style issue
- database schema concerns when the schema is unavailable and cannot be
  inferred reliably

---

# Cross-Reference Rules

Coordinate database findings with:

- references/security.md
- references/error-handling.md
- references/connectors.md
- references/dataweave.md
- references/messaging.md
- references/performance.md
- references/munit.md

Do not report the same root cause as multiple independent findings unless
the impacts are materially different.

---

# Database Finding Format

Use:

**Finding ID:** DB-001

**Severity:** HIGH

**Category:** DATABASE

**File:** `src/main/mule/example.xml:125`

**Database Operation:** Select / Insert / Update / Delete / Stored Procedure

**Location:** `flow-name / processor`

**Problem:**

Describe the database problem.

**Evidence:**

Identify the SQL, configuration, or implementation evidence.

**Technical Mechanism:**

Explain why the database behavior creates the problem.

**Impact:**

Explain realistic production, business, security, reliability, or
performance impact.

**Recommendation:**

Provide an actionable remediation approach.

**Confidence:** HIGH / MEDIUM / LOW