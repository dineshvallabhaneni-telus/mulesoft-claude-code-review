# File: standards/performance/performance-standards.md

# MuleSoft Performance Standards

## 1. Purpose

This document defines standards for reviewing performance in MuleSoft applications.

The review must determine whether application behavior is:

- Efficient
- Scalable
- Resource-conscious
- Appropriate for expected workload
- Resilient under failure
- Appropriate for synchronous and asynchronous processing
- Free from obvious unnecessary processing

Performance findings should be based on observable code patterns and reasonable workload assumptions.

Do not report a performance issue solely because an alternative implementation could theoretically be faster.

---

## 2. General Principles

Performance reviews should consider:

- CPU usage
- Memory usage
- Network calls
- Database operations
- Payload size
- Streaming
- Concurrency
- Transformation complexity
- Retry behavior
- Logging overhead
- External system limits
- Batch size
- Application throughput
- Response latency

Optimize meaningful bottlenecks rather than performing premature micro-optimization.

---

## 3. Performance and Correctness

Performance improvements must not compromise:

- Data correctness
- Error handling
- Security
- Transaction integrity
- Idempotency
- API contracts

A faster implementation that produces incorrect results is not an improvement.

---

## 4. Payload Size

Large payloads can significantly affect:

- Memory consumption
- Network bandwidth
- Serialization/deserialization
- Transformation time
- Garbage collection
- Response latency

Review whether the application unnecessarily transfers or duplicates large payloads.

---

## 5. Payload Duplication

Avoid unnecessary copies of large payloads.

Potential concerns include:

- Repeated transformations
- Converting payloads between formats unnecessarily
- Storing large payloads in multiple variables
- Repeated serialization
- Logging complete payloads

---

## 6. Large Payload Transformations

Complex transformations over large payloads may consume significant CPU and memory.

Review:

- Number of transformations
- Collection size
- Nested iterations
- Repeated filtering
- Repeated sorting
- Repeated serialization

---

## 7. DataWeave Performance

DataWeave transformations should avoid unnecessary repeated work.

Potential concerns include:

- Recalculating the same expression repeatedly
- Repeated filtering of the same collection
- Repeated `map`/`filter` operations where a single pass is practical
- Expensive transformations inside loops
- Converting large payloads unnecessarily

Do not optimize simple transformations solely for theoretical gains.

---

## 8. Nested Iteration

Nested iteration can create significant computational cost for large collections.

For example:

    orders map (order) ->
        customers filter (customer) ->
            customer.id == order.customerId

may become expensive as both collections grow.

Where appropriate, consider more efficient lookup strategies.

---

## 9. Repeated Searches

Avoid repeatedly searching the same large collection when the result can be reused.

Review whether:

- A lookup can be performed once.
- Results can be stored safely.
- Data can be indexed or keyed.
- Processing can be reorganized.

---

## 10. Large Collections

Large collections should be processed with appropriate memory and throughput considerations.

Review whether the application:

- Loads everything into memory unnecessarily
- Uses streaming where appropriate
- Processes data in batches
- Uses pagination
- Performs repeated transformations

---

## 11. Streaming

Streaming can reduce memory consumption when processing large datasets.

Consider streaming for:

- Large files
- Large HTTP responses
- Large database result sets
- Large message payloads

Do not force streaming where the processing requires random access or materialization.

---

## 12. Streaming Compatibility

Some operations require the payload to be fully materialized.

Review whether transformations or processors unintentionally consume or disable streaming.

---

## 13. File Processing

Large files should not automatically be loaded entirely into memory.

Review:

- File size
- Streaming
- Batch processing
- Temporary storage
- Repeated reads

---

## 14. Database Queries

Database performance should be reviewed carefully.

Potential concerns include:

- Unbounded queries
- Missing filtering
- Excessive columns
- Repeated queries
- Queries inside loops
- Large result sets
- Lack of pagination

---

## 15. Select Only Required Columns

Avoid retrieving large numbers of database columns when only a small subset is needed.

For example, prefer a query that retrieves required fields rather than:

    SELECT *

when the application needs only a few columns.

---

## 16. Database Pagination

Large result sets should use pagination or another bounded retrieval strategy where appropriate.

Avoid loading millions of rows into application memory.

---

## 17. Database Queries Inside Loops

Queries inside loops can create an N+1 query pattern.

For example:

    for each customer
        query database for orders

can result in hundreds or thousands of database calls.

Review whether data can be retrieved more efficiently.

---

## 18. N+1 Query Pattern

Potential N+1 patterns should be treated as significant performance risks when collection size can be large.

Possible alternatives include:

- Bulk query
- Join
- Batch retrieval
- Cached lookup
- Preloading required data

The correct solution depends on the data model and workload.

---

## 19. Database Connection Usage

Review whether connections are:

- Properly managed
- Reused through the connector pool
- Configured appropriately
- Released after use

Avoid unnecessary creation of connections.

---

## 20. Connection Pooling

Connection pools should be sized according to:

- Application concurrency
- Database capacity
- Transaction duration
- Expected workload

Do not simply maximize pool size.

---

## 21. Excessive Database Calls

Repeated database calls for the same information should be reviewed.

Examples:

- Fetching configuration repeatedly
- Re-querying unchanged reference data
- Calling the same lookup for every record

Consider caching or preloading when appropriate.

---

## 22. Database Transactions

Long-running transactions can:

- Hold database locks
- Reduce throughput
- Increase contention
- Increase rollback cost

Keep transaction scope as small as correctness permits.

---

## 23. HTTP Calls

External HTTP calls can dominate application latency.

Review:

- Number of calls
- Sequential vs parallel execution
- Timeouts
- Payload size
- Connection reuse
- Retry behavior

---

## 24. Sequential HTTP Calls

Sequential downstream calls may create unnecessary latency when the calls are independent.

For example:

    call A
    -> call B
    -> call C

may be slower than parallel processing when A, B, and C do not depend on one another.

Do not parallelize operations that have ordering or transactional dependencies.

---

## 25. Parallel Processing

Parallel processing can improve throughput when operations are independent.

However, excessive concurrency can cause:

- Thread contention
- Memory pressure
- Downstream overload
- Connection pool exhaustion
- Rate-limit violations

---

## 26. Scatter-Gather

Scatter-Gather can be useful for independent operations.

Review:

- Number of routes
- Payload size
- Downstream capacity
- Error handling
- Aggregation overhead

Do not use Scatter-Gather merely because parallelism is available.

---

## 27. Parallel For Each

Parallel For Each should be used carefully.

Review whether:

- Records are independent.
- Order matters.
- Shared state exists.
- Downstream systems can handle concurrency.
- Database connection limits can support it.

---

## 28. Concurrency Limits

Concurrency should be bounded when downstream systems or local resources have finite capacity.

Avoid unrestricted parallel processing against:

- Databases
- APIs
- Messaging systems
- File systems

---

## 29. HTTP Connection Reuse

HTTP configurations should be reused where appropriate rather than creating unnecessary connection setup overhead.

---

## 30. HTTP Timeouts

Every external HTTP dependency should have appropriate timeout behavior.

Infinite or excessively long timeouts can:

- Consume threads
- Increase memory usage
- Reduce throughput
- Cause cascading failures

---

## 31. Retry Performance

Retries increase load and latency.

Review:

- Maximum attempts
- Backoff
- Jitter where appropriate
- Retryable errors
- Total request duration

Avoid aggressive retry loops.

---

## 32. Retry Storms

When a downstream system fails, simultaneous retries can increase the load on that system.

Potential mitigations include:

- Exponential backoff
- Jitter
- Maximum retry limits
- Circuit-breaking strategies where appropriate

---

## 33. Timeout and Retry Interaction

Timeouts and retries should be evaluated together.

For example:

    timeout = 60 seconds
    retries = 5

may result in a potentially very long request duration.

Review total worst-case latency.

---

## 34. Circuit Breaking

For unstable external dependencies, circuit-breaking patterns may prevent repeated calls to an unavailable system.

Use where justified by the architecture and available platform capabilities.

Do not require circuit breakers for every downstream dependency.

---

## 35. API Response Size

APIs should avoid returning unnecessarily large responses.

Consider:

- Pagination
- Filtering
- Field selection
- Compression where appropriate

---

## 36. API Pagination

Collection endpoints should support pagination when result sets can become large.

Avoid unbounded API responses.

---

## 37. API Request Size

Large inbound requests should be validated against reasonable limits.

Large requests can cause:

- Memory pressure
- Long processing time
- Increased network cost
- Denial-of-service risk

---

## 38. API Filtering

Where consumers may request large datasets, server-side filtering should be preferred over retrieving all records and filtering in Mule.

---

## 39. Caching

Caching may improve performance for data that:

- Changes infrequently
- Is expensive to retrieve
- Can tolerate some staleness
- Is safe to share

Do not cache data that requires real-time consistency unless the design explicitly supports it.

---

## 40. Cache Invalidation

Caching introduces consistency concerns.

Review:

- TTL
- Invalidation strategy
- Stale-data tolerance
- Cache scope
- Memory consumption

A cache without an appropriate invalidation strategy can create correctness problems.

---

## 41. Reference Data

Reference data can sometimes be cached.

Examples:

- Country codes
- Static configuration
- Product mappings
- Non-sensitive lookup data

Review whether caching is appropriate and whether updates must be reflected immediately.

---

## 42. Cache Size

Unbounded caches can cause memory pressure.

Caches should have reasonable limits or eviction strategies.

---

## 43. Object Store Usage

Object Store can be useful for persistence or state management, but should not automatically be used as a high-speed cache.

Review:

- Data size
- Access frequency
- TTL
- Serialization
- Concurrency

---

## 44. Logging Performance

Logging can materially affect application performance.

Potential issues include:

- Logging full payloads
- Logging inside high-volume loops
- Serializing large objects
- Excessive DEBUG logging
- Repeated stack traces

---

## 45. Error Logging

Errors should be logged appropriately without repeatedly serializing large payloads.

Do not log the same large payload at multiple layers.

---

## 46. Transformation Logging

Avoid logging intermediate transformation results unless they provide meaningful diagnostic value.

---

## 47. Batch Processing

Large workloads should use batch processing where appropriate.

Batch processing can:

- Bound memory usage
- Improve throughput
- Support failure isolation
- Reduce repeated overhead

The correct batch strategy depends on workload and downstream constraints.

---

## 48. Batch Size

Batch size should balance:

- Memory
- Throughput
- Downstream capacity
- Failure recovery
- Transaction duration

Larger batches are not automatically faster.

---

## 49. Batch Failure Behavior

Performance improvements must not cause excessive reprocessing.

If one record fails and the entire batch is repeatedly reprocessed, throughput can degrade significantly.

---

## 50. Message Processing

Message consumers should process messages efficiently while respecting downstream capacity.

Review:

- Consumer concurrency
- Batch size
- Acknowledgment behavior
- Redelivery
- Dead-letter handling

---

## 51. Consumer Concurrency

Increasing consumer concurrency may improve throughput but can overload:

- Database
- APIs
- Queues
- CPU
- Memory

Tune concurrency based on the complete processing chain.

---

## 52. Backpressure

Applications should avoid accepting work significantly faster than downstream systems can process it.

Review whether the design provides appropriate:

- Queueing
- Rate limiting
- Concurrency limits
- Batch sizing

---

## 53. Rate Limits

External APIs may impose rate limits.

Review whether the application:

- Controls request rate
- Handles `429` responses
- Uses appropriate backoff
- Avoids unnecessary repeated calls

---

## 54. Scheduled Processing

Scheduled jobs should avoid overlapping executions when the processing time can exceed the schedule interval.

For example:

    schedule every 5 minutes
    processing takes 20 minutes

may result in overlapping work depending on the configuration and design.

---

## 55. Duplicate Scheduled Processing

Overlapping scheduled jobs can cause:

- Duplicate records
- Concurrent updates
- Database contention
- Downstream overload

Review whether concurrency must be controlled.

---

## 56. Large Loops

Large loops should be reviewed for:

- Database calls
- HTTP calls
- Transformations
- Logging
- Memory accumulation

A loop that performs several expensive operations per record can become a major bottleneck.

---

## 57. Loop Work Reduction

Move invariant work outside loops where practical.

For example, if a transformation or lookup does not depend on the current record, calculate it once rather than for every record.

---

## 58. Repeated Configuration Lookup

Avoid repeatedly resolving the same configuration or property inside high-volume processing when it can be safely resolved once.

---

## 59. Repeated Transformation

If the same transformation is applied repeatedly to unchanged data, consider whether the result can be reused.

---

## 60. Serialization

Repeated conversion between formats can create unnecessary CPU and memory overhead.

Examples:

    JSON -> String -> JSON

    XML -> String -> XML

Review whether intermediate conversions are actually required.

---

## 61. Content-Type Conversions

Avoid unnecessary conversion between:

- JSON
- XML
- CSV
- String
- Binary

when the downstream operation can consume the existing representation.

---

## 62. Binary Data

Binary data should not be converted to text unnecessarily.

Examples include:

- Images
- PDFs
- Archives
- Large files

Such conversions can significantly increase memory usage.

---

## 63. Compression

Compression may reduce network transfer size but increases CPU usage.

Use it when the tradeoff is beneficial for the workload.

Do not assume compression is always an optimization.

---

## 64. Regular Expressions

Complex regular expressions can become expensive when applied to large payloads or large collections.

Review repeated regex operations and potentially expensive patterns.

---

## 65. Sorting

Sorting large collections can be computationally expensive.

Review whether sorting is:

- Required
- Performed repeatedly
- Done at the most efficient layer

If a database can efficiently sort the data as part of a bounded query, consider whether that is preferable.

---

## 66. Filtering

Filtering should occur as close as practical to the data source when it substantially reduces data transfer.

For example, prefer database-side filtering over:

    SELECT all rows
    -> Mule filters rows

when the database can efficiently apply the required condition.

---

## 67. Aggregation

Large aggregations should be reviewed for memory consumption.

Where appropriate, perform aggregation in the data source or incrementally rather than materializing unnecessarily large collections.

---

## 68. Pagination vs Full Retrieval

Do not retrieve all records simply to process a small subset.

Use:

- Pagination
- Filtering
- Incremental processing

where appropriate.

---

## 69. API Composition

API composition can create performance problems when one request triggers many downstream calls.

Review:

- Number of downstream calls
- Sequential latency
- Parallelism
- Caching
- Payload sizes

---

## 70. Fan-Out

A single inbound request that generates many downstream requests can create a fan-out performance risk.

Examples:

    1 request
    -> 100 downstream requests

Review whether bulk operations or batching are possible.

---

## 71. Fan-In

Aggregating many downstream responses can increase:

- Memory
- Latency
- Transformation cost

Review whether all responses are required.

---

## 72. Downstream Capacity

Performance must be evaluated across the entire integration chain.

An application may be able to process 1,000 requests per second while the downstream system can process only 100.

Do not optimize the Mule application in isolation.

---

## 73. Connection Pool Exhaustion

Potential signs include:

- Excessive concurrency
- Long transactions
- Slow queries
- Long HTTP calls
- Too many parallel operations

Review whether concurrency aligns with connection-pool capacity.

---

## 74. Thread Blocking

Long-running blocking operations can reduce available processing capacity.

Examples:

- Slow database calls
- Long HTTP timeouts
- Blocking file operations
- External service waits

Review whether the architecture appropriately handles these operations.

---

## 75. Timeout Cascades

A slow downstream dependency can cause upstream requests to remain active.

This can consume:

- Threads
- Connections
- Memory

Review timeout propagation and overall request duration.

---

## 76. Memory Retention

Potential memory issues include:

- Large payloads stored in variables
- Large collections retained across scopes
- Large cached values
- Accumulated batch results
- Unnecessary payload duplication

---

## 77. Variable Scope

Avoid storing large objects in broader scopes than necessary.

A value needed only temporarily should not remain available throughout a long-running flow if that causes unnecessary memory retention.

---

## 78. Large Error Context

Do not attach unnecessarily large payloads or objects to errors simply to provide debugging context.

Error objects and logs should remain manageable.

---

## 79. Resource Cleanup

Ensure resources are properly released.

Examples:

- Streams
- Files
- Connections
- Temporary resources

Resource leaks can degrade performance over time.

---

## 80. File System Usage

Avoid excessive temporary file creation.

Review:

- File size
- File count
- Cleanup
- Disk capacity
- Concurrent file operations

---

## 81. Temporary Storage

Temporary storage should not become an unbounded accumulation point.

Ensure temporary files or artifacts have a cleanup strategy.

---

## 82. Performance and Security

Performance optimizations must not weaken security.

Examples of unacceptable optimization:

- Disabling TLS validation
- Removing authentication
- Logging sensitive payloads
- Increasing resource limits without considering abuse
- Removing validation to improve throughput

---

## 83. Performance and Reliability

An optimization that increases failure probability is not automatically beneficial.

Review whether increased concurrency or batching could create:

- Timeouts
- Rate-limit failures
- Connection exhaustion
- Retry storms

---

## 84. Performance and Error Handling

Error handling itself should not create excessive processing.

Avoid:

- Multiple retries across multiple layers
- Repeated transformations of failed payloads
- Large error payloads
- Excessive stack-trace logging

---

## 85. Performance and Observability

Performance optimizations should not remove the information needed to diagnose problems.

Maintain appropriate:

- Correlation IDs
- Timing information
- Error information
- Operational metrics

---

## 86. Performance Measurement

Performance findings should distinguish between:

- Clearly inefficient code
- Potential scalability concerns
- Actual measured bottlenecks

When performance data is unavailable, describe findings as risks rather than measured facts.

---

## 87. Performance Claims

Do not claim that an implementation is slow without evidence or a clear complexity/resource concern.

Prefer wording such as:

    This introduces an N+1 database access pattern that can scale linearly with the number of records.

over:

    This is slow.

---

## 88. Complexity

Consider algorithmic complexity where collection sizes can become significant.

Potential concerns include:

- Nested loops
- Repeated searches
- Repeated sorting
- Repeated filtering
- Quadratic behavior

Do not over-optimize small bounded collections.

---

## 89. Bounded vs Unbounded Workloads

A performance concern is more significant when the input size is:

- User-controlled
- Potentially very large
- Continuously growing
- Dependent on external systems

Small, explicitly bounded workloads generally require less optimization.

---

## 90. Performance Review Checklist

Before completing the performance review, confirm:

- Large payloads are handled appropriately.
- Unnecessary payload duplication is avoided.
- Large transformations are reasonable.
- Nested iteration is reviewed.
- Repeated searches are minimized.
- Streaming is considered where appropriate.
- Large files are not unnecessarily loaded into memory.
- Database queries are bounded.
- `SELECT *` is avoided where unnecessary.
- Pagination is used where appropriate.
- N+1 database patterns are avoided.
- Database connections are appropriately managed.
- Connection pools are not obviously undersized or oversized.
- Repeated database calls are reviewed.
- Long transactions are avoided where possible.
- HTTP calls are appropriately designed.
- Independent downstream calls are not unnecessarily sequential.
- Parallelism is bounded.
- HTTP timeouts are configured.
- Retry behavior is bounded.
- Retry storms are avoided.
- API responses are appropriately sized.
- API requests have reasonable limits.
- Caching is used only where appropriate.
- Cache invalidation is considered.
- Batch processing is appropriate for large workloads.
- Batch size is reasonable.
- Message consumer concurrency is controlled.
- Backpressure is considered.
- Rate limits are respected.
- Scheduled jobs cannot unintentionally overlap.
- Expensive work is not repeated inside loops unnecessarily.
- Serialization is not unnecessarily repeated.
- Binary data is not unnecessarily converted to text.
- Logging does not create excessive overhead.
- Temporary files are cleaned up.
- Large objects are not retained unnecessarily.
- Resource cleanup is handled.
- Performance optimizations do not weaken security.
- Performance optimizations do not compromise correctness.

---

## 91. Performance Quality Gate

The reviewer must be able to answer the following questions:

1. Can the application handle the expected workload without obvious unnecessary processing?
2. Are large payloads and collections handled safely?
3. Are database and HTTP calls bounded and efficient?
4. Are N+1 access patterns avoided?
5. Is concurrency controlled?
6. Are retries and timeouts bounded?
7. Could a downstream failure create a resource-exhaustion cascade?
8. Are large files and streams handled appropriately?
9. Are unnecessary serialization and payload copies avoided?
10. Is logging appropriately sized for production workloads?
11. Are scheduled, batch, and message workloads scalable?
12. Are caches used appropriately and safely?
13. Could performance behavior degrade significantly as input size grows?
14. Are optimizations based on a meaningful workload or complexity concern?
15. Do performance improvements preserve correctness, security, and reliability?

### Final Question

> As workload, payload size, concurrency, and downstream latency increase, does the application continue to use CPU, memory, connections, and network resources in a controlled and predictable way?