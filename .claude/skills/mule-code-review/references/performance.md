# Performance Review Rules

## Purpose

These rules define how performance and scalability must be reviewed in
Mule 4 applications.

Review performance across:

- Mule flows
- DataWeave
- HTTP
- Database
- Salesforce
- Anypoint MQ
- JMS
- SFTP
- File
- Object Store
- Batch
- External APIs
- Connection pools
- Retries
- Logging
- Concurrency
- Memory usage
- Streaming
- Deployment configuration

Performance findings must identify a realistic mechanism that can cause
production impact.

Do not report performance concerns solely because a different implementation
could theoretically be faster.

Do not recommend optimization without evidence of a meaningful workload,
payload size, execution pattern, resource constraint, or scalability risk.

---

## Performance Review Principles

Before reporting a performance finding:

1. Identify the processing pattern.
2. Understand expected payload size where evidence exists.
3. Identify external calls.
4. Identify database operations.
5. Identify DataWeave transformations.
6. Identify loops and collection operations.
7. Identify streaming behavior.
8. Identify memory-intensive operations.
9. Identify concurrency.
10. Identify connection pools where applicable.
11. Identify retry behavior.
12. Identify logging behavior.
13. Identify batch behavior.
14. Identify blocking operations.
15. Identify scalability constraints.
16. Inspect related configuration.
17. Inspect relevant tests where available.
18. Confirm realistic production impact.

If workload characteristics are unknown, do not invent them.

---

## PERF-001 — Large Payload Held Unnecessarily in Memory

### Rule

Flag processing that unnecessarily materializes large payloads in memory.

Examples include:

- converting a stream to an in-memory structure unnecessarily
- storing large payloads in multiple variables
- repeated payload copies
- unnecessary serialization or deserialization
- collecting very large datasets before processing

### Severity

HIGH

Use when repository evidence supports a realistic memory risk.

---

## PERF-002 — Streaming Regression

### Rule

Flag transformations or processors that unnecessarily disable or destroy
streaming behavior for large-payload processing.

Examples include:

- materializing a stream unnecessarily
- converting a streaming source into a large in-memory collection
- operations that force full payload materialization without a business
  requirement

### Severity

HIGH

Coordinate with `references/dataweave.md`.

---

## PERF-003 — N+1 Downstream Calls

### Rule

Flag processing that performs one or more downstream calls for every
element of a collection when the number of calls can grow with input size
and the behavior creates a realistic performance or scalability problem.

Examples include:

- HTTP request inside a loop
- Salesforce call inside a loop
- database query inside a loop
- SFTP operation inside a loop

### Severity

HIGH

Consider batching or bulk APIs where supported.

---

## PERF-004 — Excessive Logging

### Rule

Flag logging that can materially increase processing overhead or I/O.

Examples include:

- logging complete large payloads
- logging the same payload multiple times
- DEBUG logging of high-volume messages in production paths
- repeated serialization for logging

### Severity

MEDIUM

Escalate when sensitive data is also exposed.

Coordinate with `references/security.md`.

---

## PERF-005 — Repeated Expensive DataWeave Traversal

### Rule

Flag repeated traversal, filtering, sorting, grouping, or transformation
of the same large collection when the work can reasonably be avoided.

### Severity

MEDIUM

Do not report simple repeated operations on small collections without
evidence of meaningful impact.

---

## PERF-006 — Unbounded Collection

### Rule

Flag processing that can accumulate an unbounded or very large collection
in memory.

Examples include:

- collecting all records before processing
- accumulating results across an unbounded stream
- reading an unbounded result set
- repeatedly appending to large arrays

### Severity

HIGH

---

## PERF-007 — Sequential Processing Where Parallelization Is Clearly Safe

### Rule

Flag sequential processing when:

- operations are independent
- workload is demonstrably significant
- downstream systems can safely handle concurrency
- ordering is not required
- parallelization provides a meaningful improvement

### Severity

LOW / MEDIUM

Do not recommend parallelization merely because it is possible.

Do not recommend parallelization when it can cause:

- rate-limit violations
- database contention
- ordering problems
- duplicate processing
- resource exhaustion

---

## PERF-008 — Excessive Retry Load

### Rule

Flag retry behavior that can multiply workload and create significant
processing or downstream load.

Consider:

- connector retries
- `until-successful`
- messaging redelivery
- application-level retries
- nested retries

### Severity

HIGH

Coordinate with:

- `references/error-handling.md`
- `references/messaging.md`

---

## PERF-009 — N+1 Database Queries

### Rule

Flag database queries executed repeatedly for individual records when a
set-based query, join, batch operation, or other approach can materially
reduce database calls.

### Severity

HIGH

Coordinate with `references/database.md`.

---

## PERF-010 — Unbounded Database Result Set

### Rule

Flag database operations that can load an unnecessarily large or
unbounded result set into memory.

Consider:

- missing pagination
- missing filtering
- unnecessary `SELECT *`
- large result sets
- batch processing behavior

### Severity

HIGH

---

## PERF-011 — Inefficient Database Query

### Rule

Flag database queries with a realistic performance problem supported by
repository evidence.

Potential indicators include:

- unnecessary joins
- repeated queries
- filtering after data retrieval
- functions preventing efficient index usage
- unnecessary sorting
- retrieving unused columns
- inefficient query structure

### Severity

MEDIUM / HIGH

Do not claim a missing index unless repository evidence supports the
finding.

---

## PERF-012 — Excessive External Calls

### Rule

Flag workflows that make an excessive number of HTTP, Salesforce,
database, SFTP, or other external calls for a single business operation.

Consider:

- number of records
- number of calls per record
- batch APIs
- bulk APIs
- caching
- downstream limits

### Severity

MEDIUM / HIGH

---

## PERF-013 — External Call Inside Large Loop

### Rule

Flag external calls placed inside loops where the number of calls can
grow significantly with input size.

Examples include:

- HTTP request for every record
- Salesforce operation for every record
- database query for every record
- SFTP operation for every record

### Severity

HIGH

Only report when the call pattern creates a realistic scalability risk.

---

## PERF-014 — Blocking Operation in High-Throughput Flow

### Rule

Flag blocking operations in flows that are expected to process high
message or request volumes when the blocking behavior can materially
limit throughput.

Examples include:

- long-running synchronous HTTP calls
- sequential database calls
- file operations
- SFTP operations
- long waits
- unnecessary synchronous dependencies

### Severity

MEDIUM / HIGH

Do not assume that every synchronous operation is a performance defect.

---

## PERF-015 — Excessive Sequential External Calls

### Rule

Flag chains of independent external calls that execute sequentially and
create significant latency when concurrency is clearly safe and
appropriate.

### Severity

MEDIUM

Consider:

- dependency relationships
- downstream rate limits
- ordering
- resource capacity
- failure handling

Do not recommend parallel execution when operations are not independent.

---

## PERF-016 — Connection Pool Exhaustion Risk

### Rule

Flag connector or database configuration that can realistically exhaust
available connections or workers.

Consider:

- pool size
- concurrent requests
- transaction duration
- long-running operations
- connection leaks
- downstream latency

### Severity

HIGH

Do not claim pool exhaustion without evidence of a mechanism.

---

## PERF-017 — Incorrect Connection Pool Configuration

### Rule

Flag connection pool configuration that is clearly inconsistent with
the application's processing characteristics.

Potential issues include:

- excessively small pool
- excessively large pool
- inappropriate validation
- connection lifetime problems
- timeout mismatch

### Severity

MEDIUM

Only report when repository evidence supports the concern.

---

## PERF-018 — Long Transaction Duration

### Rule

Flag transactions that remain open while performing unnecessarily long
operations.

Examples include:

- external HTTP calls
- Salesforce calls
- SFTP operations
- large transformations
- message waits

### Severity

HIGH

Potential consequences include:

- database locks
- connection exhaustion
- rollback overhead
- reduced throughput

Coordinate with:

- `references/database.md`
- `references/messaging.md`

---

## PERF-019 — Excessive Payload Copies

### Rule

Flag repeated copying or storing of large payloads in:

- variables
- attributes
- DataWeave transformations
- logs
- Object Store

### Severity

MEDIUM

Escalate when memory pressure is realistic.

---

## PERF-020 — Unnecessary Serialization

### Rule

Flag repeated serialization and deserialization that provides no required
business or integration value.

Examples include:

- JSON to String to JSON
- XML to String to XML
- repeated format conversion between processors

### Severity

LOW / MEDIUM

Do not report format conversion when required by an external contract.

---

## PERF-021 — Inefficient DataWeave Algorithm

### Rule

Flag DataWeave operations whose computational complexity can become
problematic as collection size grows.

Examples include:

- nested scans
- repeated `filter`
- repeated `find`
- repeated `groupBy`
- repeated sorting
- nested iteration over large collections

### Severity

MEDIUM / HIGH

Coordinate with `references/dataweave.md`.

---

## PERF-022 — Nested Iteration Over Large Collections

### Rule

Flag nested iterations where both collections can grow significantly
and the resulting computational complexity can materially affect
processing time.

### Severity

MEDIUM / HIGH

Do not report nested iteration automatically.

The finding must explain why collection size makes the behavior
problematic.

---

## PERF-023 — Repeated Sorting

### Rule

Flag repeated sorting of the same large collection when sorting can
reasonably be performed once.

### Severity

LOW / MEDIUM

Only report when the collection size or processing frequency makes the
cost meaningful.

---

## PERF-024 — Excessive Collection Materialization

### Rule

Flag transformations that repeatedly convert streaming or iterable data
into complete in-memory collections without a business requirement.

### Severity

HIGH

---

## PERF-025 — Inefficient Batch Configuration

### Rule

Flag batch configuration that can materially reduce throughput or cause
unnecessary resource consumption.

Consider:

- batch size
- block size
- commit frequency
- database calls
- external calls
- memory usage
- failure handling

### Severity

MEDIUM / HIGH

Do not recommend a specific batch size without understanding the workload.

---

## PERF-026 — Batch Processing Causes N+1 Calls

### Rule

Flag batch processing where each record results in separate downstream
operations when bulk processing is available and appropriate.

### Severity

HIGH

---

## PERF-027 — Excessive Object Store Operations

### Rule

Flag frequent Object Store reads or writes that can become a significant
performance bottleneck.

Consider:

- operation frequency
- payload size
- persistence mode
- retention
- access pattern

### Severity

MEDIUM

---

## PERF-028 — Inefficient Cache Usage

### Rule

Flag caching behavior that provides little benefit or creates excessive:

- memory usage
- stale data
- synchronization overhead
- cache churn

### Severity

LOW / MEDIUM

Do not recommend caching unless repeated access to relatively stable data
provides a meaningful performance benefit.

---

## PERF-029 — Missing Caching Where Clearly Beneficial

### Rule

Flag repeated expensive retrieval of stable reference data when:

- the same data is repeatedly requested
- the data changes infrequently
- caching is architecturally appropriate
- repository evidence indicates a meaningful performance impact

### Severity

LOW / MEDIUM

Do not recommend caching merely because it is possible.

---

## PERF-030 — Excessive HTTP Connection Creation

### Rule

Flag HTTP integrations that unnecessarily create or establish connections
repeatedly when reusable connection configuration is appropriate.

### Severity

MEDIUM

Inspect existing HTTP requester or global configuration before reporting.

---

## PERF-031 — Missing HTTP Connection Reuse

### Rule

Flag HTTP configuration that prevents appropriate connection reuse and
creates meaningful connection establishment overhead.

### Severity

MEDIUM

Only report when the connector configuration and workload support the
finding.

---

## PERF-032 — Missing Timeout Causing Resource Retention

### Rule

Flag external operations without an appropriate timeout where an
unresponsive downstream system can hold workers or connections
indefinitely or for an excessive period.

### Severity

HIGH

Coordinate with:

- `references/connectors.md`
- `references/api.md`

---

## PERF-033 — Excessive Timeout

### Rule

Flag timeout configuration that can cause unnecessary resource
retention and backlog when downstream operations become unavailable.

### Severity

MEDIUM

Only report when the timeout is clearly inconsistent with the
application's processing requirements.

---

## PERF-034 — Retry Amplification

### Rule

Flag multiple retry layers that multiply the number of downstream
attempts.

Consider combinations such as:

- messaging redelivery
- Mule retry
- connector retry
- downstream retry

### Severity

HIGH

Calculate or explain the realistic maximum attempt amplification when
possible.

---

## PERF-035 — Retry Storm

### Rule

Flag retry behavior that can cause a large number of failed messages or
requests to repeatedly hit an unavailable downstream system.

Potential consequences include:

- downstream overload
- worker exhaustion
- queue backlog
- connection pool exhaustion
- increased latency

### Severity

HIGH

---

## PERF-036 — Excessive Debug Logging in High-Volume Flow

### Rule

Flag debug-level logging of large payloads or high-frequency events in
production processing paths when it can materially affect throughput or
storage.

### Severity

MEDIUM

Coordinate with `references/security.md`.

---

## PERF-037 — Duplicate Logging

### Rule

Flag the same large payload or exception being logged repeatedly across
multiple layers without meaningful diagnostic value.

### Severity

LOW / MEDIUM

---

## PERF-038 — Excessive Exception Stack Trace Logging

### Rule

Flag repeated stack trace logging for expected or high-volume errors
when it can create significant I/O and log-storage overhead.

### Severity

LOW / MEDIUM

Do not suppress useful diagnostic information merely to reduce logging.

---

## PERF-039 — Inefficient Error Path

### Rule

Flag error handling that performs expensive or repeated processing during
failure scenarios and can amplify resource consumption during an outage.

Examples include:

- repeated serialization
- repeated database lookup
- repeated downstream calls
- large payload logging
- retry inside error handler

### Severity

MEDIUM / HIGH

---

## PERF-040 — Performance Degradation During Downstream Failure

### Rule

Flag architecture where downstream failures can cause resource
consumption to increase instead of decrease.

Examples include:

- retries increase faster than failures resolve
- blocked connections accumulate
- message backlog causes excessive concurrent processing
- failed requests remain active for excessive periods

### Severity

HIGH

---

## PERF-041 — Missing Rate Control

### Rule

Flag high-volume processing that can overwhelm downstream systems because
there is no reasonable control over request or message throughput.

Consider:

- rate limits
- concurrency
- batching
- throttling
- queue depth

### Severity

MEDIUM / HIGH

Only report when workload or downstream constraints provide evidence.

---

## PERF-042 — Excessive Consumer Concurrency

### Rule

Flag message consumers whose concurrency can exceed downstream
capacity.

Consider:

- database pool size
- HTTP connection capacity
- Salesforce limits
- API rate limits
- worker resources

### Severity

HIGH

Coordinate with `references/messaging.md`.

---

## PERF-043 — Insufficient Consumer Concurrency

### Rule

Flag message processing that cannot reasonably meet an established
throughput requirement due to unnecessarily low concurrency.

### Severity

MEDIUM

Only report when throughput requirements or message volume are supported
by repository evidence.

---

## PERF-044 — Unbounded Message Backlog

### Rule

Flag processing where incoming message volume can exceed processing
capacity indefinitely without effective scaling or flow control.

### Severity

HIGH

Coordinate with `references/messaging.md`.

---

## PERF-045 — Large File Processing Without Streaming

### Rule

Flag file or SFTP processing that loads large files completely into
memory when streaming or incremental processing is appropriate.

### Severity

HIGH

---

## PERF-046 — Large Database Export Without Streaming

### Rule

Flag database processing that retrieves very large datasets into memory
when streaming, pagination, or incremental processing is appropriate.

### Severity

HIGH

Coordinate with `references/database.md`.

---

## PERF-047 — Unnecessary Full Dataset Retrieval

### Rule

Flag queries or API calls that retrieve significantly more data than is
required for the business operation.

Examples include:

- unused columns
- unnecessary records
- unnecessary fields
- missing filtering

### Severity

MEDIUM

---

## PERF-048 — Excessive API Payload Size

### Rule

Flag API requests or responses that unnecessarily transfer large payloads
when a materially smaller representation is available and appropriate.

### Severity

MEDIUM

Do not report when the complete payload is required by the contract.

---

## PERF-049 — Missing Pagination

### Rule

Flag API or database integrations that retrieve potentially large
datasets without pagination where the external system or repository
provides evidence that pagination is required.

### Severity

HIGH

Coordinate with:

- `references/api.md`
- `references/database.md`

---

## PERF-050 — Inefficient Polling

### Rule

Flag polling configurations that can generate unnecessary load or cause
significant processing inefficiency.

Consider:

- polling frequency
- empty responses
- duplicate retrieval
- downstream capacity
- expected event volume

### Severity

MEDIUM

---

## PERF-051 — Polling Too Frequently

### Rule

Flag polling intervals that create unnecessary external calls when the
expected business latency does not justify the frequency.

### Severity

LOW / MEDIUM

Do not assume a particular polling interval is incorrect without
business or system requirements.

---

## PERF-052 — Missing Incremental Retrieval

### Rule

Flag integrations that repeatedly retrieve complete datasets instead of
using an available incremental mechanism.

Examples include:

- timestamps
- change tracking
- watermarks
- event IDs
- incremental database queries

### Severity

MEDIUM / HIGH

Only report when repository evidence supports the availability and need
for incremental processing.

---

## PERF-053 — Duplicate External Retrieval

### Rule

Flag repeated retrieval of the same external data within a single
business operation when the data could reasonably be reused.

### Severity

LOW / MEDIUM

---

## PERF-054 — Excessive Transformation Layers

### Rule

Flag multiple unnecessary DataWeave or serialization transformations
that materially increase CPU or memory usage.

### Severity

LOW / MEDIUM

Do not report required transformations between external contracts.

---

## PERF-055 — Inefficient String Construction

### Rule

Flag repeated or unnecessarily expensive string construction for large
payloads or high-frequency processing when it creates meaningful CPU or
memory overhead.

### Severity

LOW

Only report when the impact is realistic.

---

## PERF-056 — Excessive Regular Expression Processing

### Rule

Flag expensive or repeated regular-expression operations over large
payloads or collections when they can materially affect CPU usage.

### Severity

LOW / MEDIUM

Do not report normal regex usage without evidence of a scalability risk.

---

## PERF-057 — CPU-Heavy Transformation in High-Volume Path

### Rule

Flag computationally expensive DataWeave or processing logic in a
high-volume synchronous path when the workload can materially affect
throughput.

### Severity

MEDIUM / HIGH

---

## PERF-058 — Synchronous Dependency Creates Latency Bottleneck

### Rule

Flag synchronous downstream dependencies that materially increase
end-to-end latency and where asynchronous processing is clearly
appropriate based on business requirements.

### Severity

MEDIUM

Do not recommend asynchronous architecture merely because it may be
faster.

---

## PERF-059 — Missing Bulk Operation

### Rule

Flag repeated individual operations when the downstream system provides
a supported bulk operation and using it would materially improve
performance.

Examples include:

- Salesforce bulk APIs
- database batch operations
- HTTP bulk endpoints

### Severity

MEDIUM / HIGH

---

## PERF-060 — Inefficient Salesforce Processing

### Rule

Where Salesforce integration exists, flag patterns that can create
unnecessary API usage or poor throughput.

Consider:

- SOQL inside loops
- DML inside loops
- repeated queries
- missing bulk processing
- unnecessary fields
- pagination
- API limits

### Severity

HIGH

Coordinate with:

- `references/connectors.md`
- `references/database.md`

---

## PERF-061 — Excessive SFTP or File Operations

### Rule

Flag repeated file or SFTP operations that can create unnecessary
network or filesystem overhead.

Examples include:

- repeated directory scans
- opening and closing the same resource unnecessarily
- processing the same file repeatedly
- excessive file metadata operations

### Severity

MEDIUM

---

## PERF-062 — Duplicate File Processing

### Rule

Flag file-processing logic that can repeatedly process the same file due
to inadequate state tracking or race conditions.

### Severity

HIGH

Coordinate with:

- `references/messaging.md`
- `references/connectors.md`

---

## PERF-063 — Inefficient Object Store Access

### Rule

Flag frequent or large Object Store operations that can become a
meaningful performance bottleneck.

Consider:

- large stored values
- high operation frequency
- repeated lookups
- unnecessary serialization

### Severity

MEDIUM

---

## PERF-064 — Excessive Cache Invalidation

### Rule

Flag cache behavior where frequent invalidation prevents effective cache
reuse while introducing additional processing overhead.

### Severity

LOW / MEDIUM

---

## PERF-065 — Cache Stampede

### Rule

Flag cache-miss behavior where many concurrent requests can trigger the
same expensive downstream retrieval simultaneously.

### Severity

MEDIUM / HIGH

Only report when concurrent access and expensive retrieval are evident.

---

## PERF-066 — Resource Leak

### Rule

Flag processing that can fail to release resources such as:

- connections
- streams
- files
- database resources
- connector resources

### Severity

HIGH

Only report when the repository provides evidence of the leak mechanism.

---

## PERF-067 — Excessive Worker or Thread Blocking

### Rule

Flag operations that can unnecessarily block execution resources for
long periods and materially reduce application throughput.

### Severity

HIGH

Do not report normal synchronous processing automatically.

---

## PERF-068 — Performance-Sensitive Configuration Mismatch

### Rule

Flag configuration where runtime, connector, pool, batch, concurrency,
or timeout settings are clearly inconsistent with the application's
processing model.

### Severity

MEDIUM / HIGH

Only report when repository evidence supports the mismatch.

---

## PERF-069 — Performance Regression

### Rule

For Git-based reviews, flag a change that introduces a demonstrable
increase in:

- external calls
- database calls
- payload size
- memory usage
- processing complexity
- retries
- serialization
- logging

For full application reviews, assess the current implementation without
assuming a previous version.

### Severity

MEDIUM / HIGH

---

## PERF-070 — Scalability Bottleneck

### Rule

Flag an architectural or implementation pattern that cannot reasonably
scale with the application's demonstrated workload.

Potential mechanisms include:

- single-threaded bottleneck
- sequential external calls
- unbounded memory usage
- database contention
- downstream API limits
- message backlog
- excessive synchronization

### Severity

HIGH

The finding must explain the scaling mechanism.

---

## PERF-071 — Missing Performance Guardrail

### Rule

Flag critical processing where there is no reasonable control over
potentially unbounded input or workload.

Examples include:

- maximum records
- pagination
- batch size
- payload size
- concurrency
- timeout

### Severity

MEDIUM / HIGH

Only report when an uncontrolled workload is realistically possible.

---

## PERF-072 — Large Payload Stored in Variables

### Rule

Flag unnecessary storage of large payloads in multiple variables when
the data can remain in the payload or be processed incrementally.

### Severity

MEDIUM

---

## PERF-073 — Large Payload Logged Multiple Times

### Rule

Flag large payloads being logged at multiple points in the same flow when
the logging creates meaningful CPU, memory, or I/O overhead.

### Severity

MEDIUM

---

## PERF-074 — Inefficient Error Logging

### Rule

Flag error handlers that serialize or construct large payloads solely
for logging when the information is not required for diagnosis.

### Severity

LOW / MEDIUM

---

## PERF-075 — Performance Issue Hidden by Small Test Data

### Rule

Flag meaningful scalability risks where MUnit tests only use trivial
payload sizes or record counts and therefore do not exercise the
behavior that creates the production risk.

### Severity

LOW / MEDIUM

Do not treat small test data as a performance defect by itself.

---

## PERF-076 — Missing Performance-Relevant Test Scenario

### Rule

Flag critical flows where meaningful performance-related behavior is
untested when repository evidence indicates that the behavior is
important.

Examples include:

- large payload
- large record set
- high message volume
- retry storm
- pagination
- batch processing

### Severity

LOW / MEDIUM

---

# Performance False-Positive Controls

Do not report:

- optimization opportunities without meaningful impact
- parallelization merely because it is possible
- caching merely because it is possible
- asynchronous processing merely because it may reduce latency
- database indexes without evidence
- streaming concerns for genuinely small payloads
- N+1 patterns without realistic collection growth
- sequential processing when ordering is required
- additional logging as a performance issue without meaningful overhead
- connector pooling concerns without evidence
- concurrency concerns without workload or downstream-capacity evidence
- missing pagination when result size is demonstrably bounded
- missing bulk APIs when the downstream contract does not support them
- performance regressions without a reasonable mechanism
- theoretical complexity concerns that cannot affect realistic workloads
- duplicate findings for the same underlying performance problem

---

# Performance Finding Quality Gate

Before reporting a performance finding:

1. Identify the affected flow.
2. Identify the processing pattern.
3. Identify payload or record characteristics when available.
4. Identify external calls.
5. Identify database operations.
6. Identify DataWeave operations.
7. Identify memory behavior.
8. Identify streaming behavior.
9. Identify concurrency.
10. Identify connection and pool behavior.
11. Identify retry behavior.
12. Identify logging.
13. Identify batch behavior.
14. Identify downstream limits.
15. Verify the problem is not already mitigated.
16. Explain the technical mechanism.
17. Explain realistic impact.
18. Confirm severity.
19. Identify exact file and location.

If evidence is insufficient, do not report the issue.

---

# Cross-Reference Rules

Coordinate performance findings with:

- `references/dataweave.md`
- `references/database.md`
- `references/connectors.md`
- `references/messaging.md`
- `references/error-handling.md`
- `references/security.md`
- `references/munit.md`

Do not report the same root cause multiple times unless the impacts are
materially different.

---

# Performance Finding Format

Use the following structure for every performance finding.

**Finding ID:** PERF-001

**Severity:** HIGH

**Category:** PERFORMANCE

**File:** `src/main/mule/example.xml:125`

**Flow:** `example-flow`

**Location:** `processor / transformation / connector`

**Problem:**

Describe the performance problem.

**Evidence:**

Identify the relevant flow, DataWeave, connector configuration,
database query, loop, retry, or other repository evidence.

**Technical Mechanism:**

Explain why the implementation creates additional CPU, memory, I/O,
latency, connection, or throughput cost.

**Impact:**

Explain the realistic production impact.

**Recommendation:**

Provide an actionable remediation approach.

**Confidence:** HIGH / MEDIUM / LOW