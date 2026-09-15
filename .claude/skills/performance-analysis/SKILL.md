# MuleSoft Performance Analysis Skill

## Purpose

Perform a comprehensive performance review of the MuleSoft application.

Review the application as a:

- Senior MuleSoft Architect
- Performance Architect
- Senior Technical Lead

The objective is to identify realistic performance bottlenecks, inefficient implementation patterns, resource consumption risks, scalability concerns, and opportunities to optimize the MuleSoft application.

The review must be evidence-based.

Do not report every possible optimization.

Only report a performance issue when:

- There is evidence in the implementation.
- There is a credible performance risk.
- The optimization provides meaningful value.
- The recommendation is technically appropriate.

Every meaningful finding MUST include a practical solution.

---

# 1. Repository Scope

The MuleSoft application is:

${GITHUB_WORKSPACE}

The code-review framework is:

${GITHUB_WORKSPACE}/code-review

The reports directory is:

${GITHUB_WORKSPACE}/reports

Review the complete MuleSoft application.

---

# 2. Mandatory Exclusions

Do NOT review these directories as application source:

${GITHUB_WORKSPACE}/code-review/**
${GITHUB_WORKSPACE}/reports/**

Do not report findings against:

- Review agents
- Skills
- Prompt files
- Framework scripts
- Generated reports

---

# 3. Performance Review Areas

Review:

- Flow design
- Subflows
- Flow references
- Loops
- For Each
- Parallel For Each
- Until Successful
- Async processing
- Batch processing
- Scatter-Gather
- Choice logic
- DataWeave
- Payload transformations
- Variables
- Repeated transformations
- Repeated connector calls
- Database access
- HTTP calls
- File operations
- Messaging
- Streaming
- Pagination
- Bulk processing
- Connection pooling
- Timeout configuration
- Retry configuration
- Memory consumption
- Large payload handling
- Thread/resource usage
- Duplicate processing
- Custom Java
- Custom Python

---

# 4. Performance Review Philosophy

Do not optimize code simply because an alternative exists.

Evaluate:

- Expected workload.
- Data volume.
- Frequency.
- Concurrency.
- Downstream capacity.
- Memory requirements.
- Latency requirements.
- Maintainability.

When workload information is unavailable, explicitly state the limitation.

Use:

Verification Required

when runtime metrics or infrastructure configuration are required.

---

# 5. Architecture-Level Performance

Evaluate whether the overall integration architecture is appropriate.

Consider:

- Synchronous vs asynchronous processing.
- Request-response vs fire-and-forget.
- Batch processing.
- Event-driven processing.
- Sequential vs parallel execution.
- Excessive downstream calls.
- Unnecessary transformations.
- Large in-memory payloads.

Do not recommend asynchronous architecture simply because it may be faster.

The recommendation must fit the business interaction.

---

# 6. Sequential Processing

Identify flows performing independent operations sequentially.

Example:

Call A
→ Call B
→ Call C

where B and C do not depend on A.

Determine whether parallel processing could reduce latency.

Possible solution:

Use Parallel For Each or Scatter-Gather where:

- Operations are independent.
- Downstream systems can handle concurrency.
- Ordering is not required.
- Failure semantics are understood.

Do not recommend parallelism where operations have dependencies.

---

# 7. Parallel Processing

Review existing parallel processing for:

- Excessive concurrency.
- Downstream overload.
- Thread consumption.
- Ordering requirements.
- Error handling.
- Shared mutable state.

Parallelism is not automatically an optimization.

---

# 8. Scatter-Gather

Review Scatter-Gather usage.

Evaluate:

- Number of routes.
- Payload size.
- Route independence.
- Timeout behavior.
- Error handling.
- Memory usage.

Identify cases where Scatter-Gather creates excessive memory or downstream load.

---

# 9. For Each

Review For Each loops.

Look for:

- Connector call inside every iteration.
- Expensive DataWeave transformation inside every iteration.
- Repeated lookup.
- Repeated configuration access.
- Repeated database calls.

Determine whether:

- Bulk operation.
- Batch processing.
- Caching.
- Pre-fetching.
- Parallel processing

could improve performance.

Do not recommend parallelization blindly.

---

# 10. Nested Loops

Identify nested loops such as:

For Each
  → For Each
    → Connector Call

Evaluate potential computational and integration complexity.

If complexity grows significantly with input size, report the risk.

Provide a concrete alternative where possible.

---

# 11. Repeated Connector Calls

Look for repeated calls to:

- Database
- HTTP APIs
- Salesforce
- SFTP
- Other SaaS systems
- Messaging systems

Examples:

For Each item
→ HTTP Request

For Each item
→ Database Select

Evaluate whether the operation could use:

- Batch APIs.
- Bulk APIs.
- Batch database operations.
- Query pre-fetching.
- Caching.
- Pagination.
- Consolidated requests.

---

# 12. N+1 Integration Pattern

Identify patterns where one request retrieves a collection and then makes an additional downstream request for every item.

Example:

Get 1,000 customers
→ Call customer detail API 1,000 times

Report this as a performance concern when evidence supports it.

Possible solutions:

- Bulk API.
- Batch endpoint.
- Aggregated query.
- Pre-fetch.
- Cache.
- Parallelization where safe.

---

# 13. Database Performance

Review:

- Query frequency.
- Queries inside loops.
- Repeated queries.
- Large result sets.
- Pagination.
- Batch operations.
- Transactions.
- Connection pooling.
- Query parameterization.
- Unnecessary database round trips.

Do not attempt to fully replace database query optimization owned by another specialist unless performance is the concern.

---

# 14. Database Queries Inside Loops

A query executed for every item is a potential performance issue.

Example:

For Each
  → SELECT ...

Evaluate whether data can be retrieved once.

Possible solutions:

- Single query.
- IN query.
- Join.
- Batch operation.
- Pre-fetch.
- Cache.

Do not recommend a single query when the business logic requires independent queries.

---

# 15. Large Database Result Sets

Look for queries retrieving potentially large datasets.

Evaluate:

- Pagination.
- Streaming.
- Filtering.
- Selected columns.
- Batch processing.

Avoid recommending retrieval of entire datasets into memory.

---

# 16. Database Connection Pooling

Review:

- Pool configuration.
- Maximum pool size.
- Minimum pool size.
- Connection timeout.
- Idle timeout.
- Reconnection.

Do not declare pool sizes incorrect without workload evidence.

If sizing cannot be validated:

Verification Required

---

# 17. HTTP Performance

Review HTTP calls for:

- Sequential downstream calls.
- Repeated requests.
- Large payloads.
- Missing pagination.
- Excessive retries.
- Long timeouts.
- Missing connection reuse.
- Unnecessary transformations.

Do not report timeout configuration as a performance issue merely because it is absent.

---

# 18. HTTP Connection Reuse

Determine whether the application appropriately reuses HTTP connections through global configuration where applicable.

Repeated creation of connections can create unnecessary overhead.

Where relevant recommend:

- Reusable global HTTP configuration.
- Appropriate connection pooling.
- Appropriate timeout values.

---

# 19. HTTP Retry Amplification

Evaluate whether retry configuration can multiply downstream traffic.

Example:

100 requests
× 3 retries
= up to 400 attempts

Consider:

- Retry count.
- Backoff.
- Concurrency.
- Downstream rate limits.

Report retry amplification when it creates a credible risk.

---

# 20. Retry and Idempotency

Retries on non-idempotent operations may cause:

- Duplicate records.
- Duplicate transactions.
- Duplicate messages.
- Increased downstream load.

Evaluate both performance and correctness.

Coordinate with connector-analysis and API security analysis where appropriate.

---

# 21. Timeout Strategy

Review timeout settings for:

- HTTP.
- Database.
- SFTP.
- Messaging.
- Other connectors.

Very long timeouts can:

- Tie up resources.
- Increase thread occupancy.
- Cause request accumulation.

Very short timeouts can:

- Increase retries.
- Cause unnecessary failures.
- Increase downstream traffic.

Recommendations must be contextual.

---

# 22. DataWeave Performance

Review transformations for:

- Repeated transformations.
- Large payload transformations.
- Multiple passes over the same data.
- Expensive operations inside loops.
- Unnecessary conversions.
- Excessive string manipulation.
- Repeated filtering.
- Repeated sorting.

Do not optimize readable DataWeave unnecessarily.

---

# 23. DataWeave Inside Loops

Identify expensive transformations executed repeatedly.

Example:

For Each
  → Transform Message
      → large filtering/sorting operation

Determine whether the transformation can be performed once outside the loop.

---

# 24. Repeated DataWeave Transformations

Look for:

Transform
→ Transform
→ Transform
→ Transform

where multiple transformations could reasonably be consolidated.

Do not recommend consolidation if each transformation:

- Has a clear purpose.
- Improves readability.
- Is small.
- Does not materially affect performance.

---

# 25. Payload Size

Evaluate large payload handling.

Look for:

- Entire large files loaded into memory.
- Entire large HTTP responses held in memory.
- Large database results.
- Large arrays duplicated through transformations.

Recommend:

- Streaming.
- Pagination.
- Batch processing.
- Chunking.

where appropriate.

---

# 26. Streaming

Evaluate whether streaming would reduce memory usage for:

- Large files.
- Large HTTP responses.
- Database results.
- Large message payloads.

Do not recommend streaming for every payload.

---

# 27. Streaming Pitfalls

Review whether streaming is accidentally defeated by operations that require full materialization.

Look for:

- Converting streams into large arrays.
- Repeated payload access.
- Large aggregation.
- Multiple full traversals.

Report only when evidence supports meaningful memory impact.

---

# 28. Variable Usage

Review:

- Large variables.
- Repeated variable copies.
- Variables containing large payloads.
- Variables maintained through long flows.

Do not report ordinary variables as performance problems.

---

# 29. Duplicate Variables

Coordinate with:

duplication-analysis

for duplicate variable detection.

This skill should focus on the performance impact.

Examples:

- Multiple large copies of the same payload.
- Repeated construction of identical datasets.

---

# 30. Logging Performance

Review logging that may negatively affect performance.

Examples:

- Logging entire payloads.
- Logging large collections.
- Excessive logs inside loops.
- Debug-level payload logging in production.

Detailed logging quality belongs to:

logging-analysis

Report here only when there is meaningful performance impact.

---

# 31. Logging Inside Loops

Identify:

For Each
→ Logger

or similar patterns.

Determine whether logging volume could become excessive for large workloads.

Recommend:

- Aggregated logging.
- Summary metrics.
- Appropriate log levels.

Do not remove useful business/audit logging without considering operational requirements.

---

# 32. File Processing

Review file operations for:

- Large files.
- Repeated reads.
- Repeated writes.
- Temporary file creation.
- Sequential file processing.
- Polling frequency.
- Duplicate file processing.

Consider:

- Streaming.
- Batch processing.
- Appropriate polling intervals.
- File locking.
- Event-driven alternatives where appropriate.

---

# 33. SFTP/FTP Performance

Where applicable evaluate:

- Connection reuse.
- Directory listing frequency.
- File download strategy.
- File size.
- Streaming.
- Parallel transfers.
- Polling interval.

Do not recommend aggressive parallel transfers without considering server capacity.

---

# 34. Messaging Performance

Review:

- Consumer concurrency.
- Batch consumption.
- Message size.
- Redelivery.
- Retry.
- Acknowledgement behavior.
- Queue polling.

Do not assume higher concurrency is always better.

---

# 35. Batch Processing

Identify workloads suitable for Batch Job.

Consider:

- Large record volumes.
- Independent records.
- Batch aggregation.
- Error isolation.
- Record-level processing.

Do not recommend Batch Job for simple request-response APIs.

---

# 36. Until Successful

Review Until Successful usage.

Potential problems:

- High retry counts.
- Long retry intervals.
- Large payloads.
- Non-idempotent operations.
- Blocking request threads.

Evaluate whether asynchronous processing or a more appropriate retry strategy is better.

---

# 37. Async Scope

Review Async scope usage.

Consider:

- Memory.
- Error handling.
- Ordering.
- Transaction boundaries.
- Backpressure.
- Unbounded workload.

Do not recommend Async simply to make the flow appear faster.

---

# 38. VM / Internal Messaging

If VM or internal messaging is used, review:

- Queue size.
- Consumer concurrency.
- Message persistence where applicable.
- Backpressure.
- Retry.
- Error handling.

Do not report infrastructure behavior that cannot be established from source.

---

# 39. Caching

Identify repeated expensive lookups where caching may provide value.

Potential candidates:

- Reference data.
- Static configuration.
- Slowly changing metadata.

Do not recommend caching:

- Frequently changing transactional data.
- Security-sensitive data without considering invalidation.
- Data where stale values create correctness problems.

---

# 40. Cache Invalidation

If caching is used, evaluate:

- TTL.
- Invalidation.
- Staleness.
- Memory usage.
- Cache size.

Do not report a cache as incorrect without understanding the business requirement.

---

# 41. Duplicate External Calls

Identify repeated calls that retrieve identical or equivalent information.

Example:

Flow A → Customer API
Flow B → Customer API
Flow C → Customer API

If consolidation/caching is feasible, report the performance opportunity.

Do not assume flows should share data if isolation is intentional.

---

# 42. Performance Bottleneck Ranking

Rank performance findings by likely impact.

Prioritize:

1. Excessive downstream calls.
2. Large memory consumption.
3. Blocking/long-running operations.
4. Inefficient database access.
5. Excessive retries.
6. Poor concurrency design.
7. Large payload transformations.
8. Inefficient file processing.
9. Excessive logging.
10. Minor optimizations.

---

# 43. Scalability

Evaluate whether the implementation can scale with:

- Number of requests.
- Number of records.
- Payload size.
- Concurrent users.
- Downstream latency.

Consider whether performance degrades linearly or disproportionately as workload increases.

---

# 44. Backpressure

Look for situations where upstream traffic can grow faster than downstream processing.

Examples:

API
→ Slow downstream API

Queue
→ Slow consumer

File poller
→ Processing slower than arrival rate

Evaluate:

- Queueing.
- Concurrency.
- Throttling.
- Retry.
- Resource consumption.

---

# 45. Resource Exhaustion

Look for potential:

- Memory exhaustion.
- Thread exhaustion.
- Connection pool exhaustion.
- File descriptor exhaustion.
- Queue growth.

Do not claim actual exhaustion without runtime evidence.

Use:

Potential Risk

when based on code/configuration.

---

# 46. Performance Anti-Patterns

Look for:

- N+1 calls.
- Connector calls inside loops.
- Large payload materialization.
- Excessive retries.
- Sequential independent calls.
- Repeated expensive transformations.
- Excessive logging.
- Unbounded concurrency.
- Excessive connection creation.
- Full dataset retrieval.
- Repeated identical lookups.

---

# 47. Performance Recommendations

Every recommendation must explain:

- Problem.
- Why it impacts performance.
- Proposed optimization.
- Expected benefit.
- Trade-offs.
- Implementation approach.

Do not promise a specific percentage improvement without performance testing.

---

# 48. Performance Testing Recommendations

Where a finding requires validation, recommend appropriate testing.

Examples:

- Load test.
- Stress test.
- Endurance test.
- Concurrency test.
- Large payload test.
- Failure/retry test.

Identify what metric should be measured.

Examples:

- Response time.
- Throughput.
- CPU.
- Memory.
- Connection utilization.
- Queue depth.
- Error rate.

---

# 49. Runtime Evidence Limitations

The repository review cannot establish actual:

- CPU.
- Memory.
- Throughput.
- Latency.
- Thread utilization.
- Connection utilization.
- Queue depth.

Do not pretend these values are known.

Clearly distinguish:

Code-level observation

from:

Runtime verification required

---

# 50. Performance Findings

Every performance finding MUST contain:

## Finding ID

Example:

MULE-PERF-001

## Title

Concise performance issue.

## Severity

Critical / High / Medium / Low / Warning

## Category

Performance

## Location

File, flow, operation, or configuration.

## Evidence

Observed implementation.

## Performance Impact

Explain the likely impact.

## Recommendation

What should change.

## Solution

Practical implementation approach.

## Expected Benefit

Describe qualitatively unless measured data exists.

## Trade-offs

Mention relevant trade-offs.

## Validation

Explain how to verify the improvement.

## Priority

Immediate / Short Term / Medium Term / Long Term

---

# 51. Severity Guidelines

## Critical

Severe performance problem likely to cause production outage or major resource exhaustion.

## High

Significant performance/scalability risk.

## Medium

Meaningful optimization opportunity or bottleneck.

## Low

Minor optimization.

## Warning

Potential concern requiring runtime/load validation.

Do not inflate severity.

---

# 52. Performance Score

Provide a performance score based on evidence.

Consider:

- Architecture.
- Resource usage.
- Connector efficiency.
- Database efficiency.
- DataWeave efficiency.
- Concurrency.
- Scalability.
- Large payload handling.
- Retry behavior.

Do not calculate the score from the number of findings alone.

---

# 53. Positive Performance Observations

Identify good practices such as:

- Appropriate streaming.
- Efficient bulk processing.
- Reusable connector configurations.
- Sensible connection pooling.
- Appropriate parallel processing.
- Good pagination.
- Controlled retries.
- Efficient transformations.
- Good separation of synchronous/asynchronous work.

The report should not be purely negative.

---

# 54. Cross-Skill Boundaries

Detailed findings owned by these skills should not be duplicated unnecessarily:

- mulesoft-architecture
- mule-code-quality
- connector-analysis
- api-security-analysis
- security-analysis
- munit-analysis
- configuration-analysis
- logging-analysis
- duplication-analysis

This skill owns performance implications.

If a connector configuration causes a performance issue:

- connector-analysis may identify the configuration.
- performance-analysis explains the performance impact.

The final report reviewer should consolidate duplicate root causes.

---

# 55. No Unsupported Claims

Never claim:

- The application cannot handle production load.
- A pool is too small.
- A timeout is incorrect.
- A particular architecture is too slow.
- A connector is a bottleneck.

without sufficient evidence.

Use:

Potential Risk

or:

Verification Required

where appropriate.

---

# 56. Final Output

Return structured performance analysis containing:

## Performance Summary

## Architecture Performance Assessment

## Flow Performance Assessment

## Connector Performance Assessment

## Database Performance Assessment

## DataWeave Performance Assessment

## Memory Assessment

## Concurrency Assessment

## Scalability Assessment

## Positive Performance Observations

## Performance Findings

## Optimization Recommendations

## Runtime Validation Required

## Performance Score

Do not generate the final Word document from this skill.

The word-report-generation skill creates the final `.docx`.

---

# 57. Quality Standard

Before completing the review, ask:

"Would a Senior MuleSoft Architect trust these recommendations for a production performance review?"

If not:

- Remove speculative findings.
- Re-check evidence.
- Consider workload assumptions.
- Distinguish code evidence from runtime evidence.
- Provide practical solutions.
- Explain trade-offs.
- Avoid arbitrary configuration values.
- Prioritize meaningful bottlenecks.

The objective is production-quality performance analysis, not a generic optimization checklist.