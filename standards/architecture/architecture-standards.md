# MuleSoft Architecture Standards

## 1. Purpose

This document defines the architecture standards used to evaluate MuleSoft applications.

The review must assess the application from the perspective of:

- Senior MuleSoft Architect
- Enterprise Integration Architect
- Senior Technical Lead

The objective is not to enforce one architecture style on every application.

The objective is to determine whether the implemented architecture is:

- Appropriate for the business purpose
- Clearly structured
- Maintainable
- Scalable
- Secure
- Resilient
- Observable
- Reusable
- Testable
- Operationally supportable

Architecture findings must be evidence-based.

Do not report an architectural concern simply because another architecture style exists.

---

# 2. Architecture Assessment Principles

The reviewer must evaluate:

1. Separation of responsibilities
2. Application boundaries
3. API boundaries
4. Integration boundaries
5. Flow decomposition
6. Reusability
7. Coupling
8. Cohesion
9. Error-handling architecture
10. Configuration architecture
11. Security architecture
12. Performance architecture
13. Scalability
14. Resilience
15. Observability
16. Testability
17. Environment separation
18. Deployment considerations
19. Maintainability
20. Extensibility

---

# 3. Architecture Discovery

The reviewer must determine the architecture from repository evidence.

Consider:

- APIs
- Listeners
- APIkit routers
- Flows
- Subflows
- Connectors
- Databases
- Messaging systems
- External systems
- Data transformations
- Batch jobs
- Scheduled flows
- Error handling
- Configuration
- Security controls

Do not infer architecture solely from:

- Application name
- Folder name
- API name
- Developer comments

---

# 4. Supported Architecture Patterns

The application may use one or more of:

- API-led connectivity
- System API
- Process API
- Experience API
- Layered architecture
- Event-driven architecture
- Request-response integration
- Asynchronous messaging
- Batch processing
- File-based integration
- Orchestration
- Choreography
- Hybrid architecture

Multiple patterns may legitimately coexist.

---

# 5. API-Led Connectivity

Where API-led connectivity is used, evaluate whether responsibilities are reasonably separated between:

## Experience Layer

Responsible primarily for consumer-specific experience.

Examples:

- Consumer-specific payload
- Consumer-specific orchestration
- Consumer-specific interaction model

## Process Layer

Responsible primarily for:

- Business orchestration
- Business processes
- Aggregation
- Transformation
- Reusable business logic

## System Layer

Responsible primarily for:

- System connectivity
- System-specific data access
- System-specific operations

Do not require all three layers when the application does not need them.

---

# 6. Layering Principle

A layer should have a clear responsibility.

Avoid:

- Business logic duplicated across layers
- System-specific logic leaking into experience flows
- Consumer-specific behavior embedded in system integrations
- Database-specific logic scattered across APIs

Report architectural leakage when it materially affects maintainability or reuse.

---

# 7. API Boundary

API boundaries should be meaningful.

An API should expose a coherent business capability rather than simply exposing internal implementation details.

Avoid unnecessary endpoints such as:

- One endpoint per database table
- Direct database CRUD exposure
- Internal implementation endpoints exposed externally

Only report this when repository evidence supports the concern.

---

# 8. System API Boundary

System integrations should abstract the underlying system where appropriate.

A System API may encapsulate:

- Database
- Salesforce
- SAP
- Mainframe
- SFTP
- External service

The API should prevent unnecessary coupling between consumers and the underlying system.

---

# 9. Process API Boundary

Process APIs should contain meaningful business orchestration.

Avoid process APIs that simply:

- Proxy one endpoint without adding business value
- Duplicate system logic
- Contain unrelated business processes

Do not require a Process API for every integration.

---

# 10. Experience API Boundary

Experience APIs should be optimized for consumer needs.

Avoid excessive consumer-specific logic in reusable System APIs.

Do not duplicate large portions of business logic between Experience APIs.

---

# 11. Flow Responsibility

Each major flow should have a clear responsibility.

Avoid "God flows" containing:

- Routing
- Validation
- Transformation
- Database logic
- External calls
- Business rules
- Error handling
- Logging
- Response construction

all in one extremely complex flow.

Recommend decomposition only when complexity materially affects maintainability.

---

# 12. Flow Cohesion

A flow should contain logically related processing.

High cohesion is preferred.

Avoid unrelated business operations being combined into one flow simply for convenience.

---

# 13. Coupling

Minimize unnecessary coupling between:

- APIs
- Flows
- Subflows
- Systems
- Data models
- Configuration
- Environment values

Identify tight coupling that makes change difficult or increases failure propagation.

---

# 14. Reusability

Common integration logic should be reusable where appropriate.

Examples:

- Shared authentication
- Common error mapping
- Common logging
- Shared transformation
- Connector configuration
- Common validation

Do not abstract trivial one-time logic unnecessarily.

---

# 15. Abstraction

Abstraction should reduce complexity.

Do not create:

- Excessive subflows
- Deep abstraction chains
- Generic utility flows
- Abstractions with only one trivial caller

Abstraction must provide measurable maintainability or reuse benefits.

---

# 16. Subflow Usage

Subflows should represent reusable or logically grouped behavior.

Avoid:

- Excessive nesting
- Subflows that contain one trivial processor without benefit
- Deep chains that make execution difficult to follow

---

# 17. Flow References

Use flow references appropriately for reusable processing.

Consider whether:

- Flow reference is necessary
- Subflow would be sufficient
- The called flow has independent lifecycle/error semantics

Do not treat one mechanism as universally superior.

---

# 18. Error-Handling Architecture

Error handling should be intentionally designed.

Review:

- Global error strategy
- Flow-level handlers
- Try scopes
- Error types
- Retry strategy
- Error mapping
- Client responses
- Operational alerts
- Dead-letter handling where applicable

Avoid inconsistent error behavior across similar APIs.

---

# 19. Error Propagation

Errors should not be silently swallowed.

Pay particular attention to:

`On Error Continue`

when used around:

- Database operations
- External API calls
- Financial transactions
- Data persistence
- Critical business processing

Do not report every `On Error Continue`.

Assess whether the error is intentionally recoverable.

---

# 20. Error Mapping

Map technical errors into appropriate business/API errors where required.

Avoid exposing:

- Stack traces
- Internal exceptions
- Database errors
- Connection details
- Internal hostnames

---

# 21. Resilience Architecture

Evaluate whether important external dependencies have appropriate resilience mechanisms.

Consider:

- Timeout
- Retry
- Reconnection
- Circuit breaker where available
- Rate limiting
- Bulkhead behavior
- Dead-letter processing
- Idempotency

Do not recommend every resilience pattern for every application.

---

# 22. Retry Architecture

Retries must consider:

- Idempotency
- Error type
- Downstream capacity
- Backoff
- Maximum attempts
- Total execution time

Avoid:

- Infinite retries
- Rapid retry loops
- Retrying permanent business errors

---

# 23. Idempotency

Critical operations should consider duplicate execution.

Especially:

- Payments
- Orders
- Customer creation
- Data updates
- Message processing

Potential approaches:

- Idempotency keys
- Unique business identifiers
- Duplicate detection
- Transaction controls

Do not mandate idempotency where duplicate execution has no meaningful impact.

---

# 24. Synchronous Architecture

For synchronous flows evaluate:

- End-to-end latency
- Downstream dependencies
- Timeout chain
- Payload size
- Retry behavior
- User/API SLA

Avoid long synchronous chains when they create unacceptable latency or reliability risk.

---

# 25. Asynchronous Architecture

Use asynchronous processing where appropriate for:

- Long-running processes
- High-volume workloads
- Event-driven processes
- Decoupling
- Retryable background processing

Do not recommend asynchronous processing merely because it is scalable.

Consider:

- Ordering
- Delivery semantics
- Monitoring
- Error handling
- Operational complexity

---

# 26. Messaging Architecture

For messaging-based applications review:

- Producer/consumer boundaries
- Delivery semantics
- Retry
- Dead-letter handling
- Ordering
- Idempotency
- Consumer concurrency
- Back-pressure

---

# 27. Batch Architecture

For batch applications review:

- Batch boundaries
- Record processing
- Failure isolation
- Restartability
- Aggregation
- Memory usage
- Streaming
- Concurrency

Avoid loading unnecessarily large datasets into memory.

---

# 28. Scheduled Flows

Review scheduled processes for:

- Duplicate execution
- Overlapping executions
- Failure recovery
- Locking where needed
- Idempotency
- Monitoring

Consider what happens if one execution takes longer than the schedule interval.

---

# 29. External System Boundaries

Identify every important external dependency.

Examples:

- Database
- Salesforce
- SAP
- SFTP
- REST API
- SOAP service
- Kafka
- JMS
- Cloud service

Evaluate whether each boundary has appropriate:

- Timeout
- Error handling
- Security
- Configuration
- Monitoring

---

# 30. Dependency Isolation

A failure in one external system should not unnecessarily destabilize unrelated processing.

Look for:

- Shared critical dependencies
- Unbounded retries
- Synchronous dependency chains
- Missing isolation
- Excessive coupling

---

# 31. Data Transformation Boundary

Transformation should occur at appropriate architectural boundaries.

Avoid:

- Repeated transformations
- Multiple unnecessary conversions
- Consumer-specific transformation inside System APIs
- System-specific data structures leaking into consumer APIs

---

# 32. Canonical Data Models

A canonical model may be appropriate when multiple systems share common business concepts.

However, do not introduce a canonical model automatically.

Evaluate:

- Number of systems
- Reuse
- Transformation complexity
- Governance requirements
- Maintenance cost

---

# 33. Direct System Coupling

Identify consumer applications that appear tightly coupled to:

- Database schemas
- Vendor-specific payloads
- Internal system identifiers
- Internal implementation details

Recommend abstraction when it provides meaningful decoupling.

---

# 34. Database Architecture

Review whether the application architecture appropriately separates:

- Database access
- Business orchestration
- API presentation

Avoid exposing database structure directly through public APIs.

---

# 35. Shared Database Access

Identify whether multiple unrelated APIs directly manipulate the same database.

This may create:

- Tight coupling
- Data ownership ambiguity
- Transaction complexity
- Schema-change risk

Report only when evidence suggests architectural impact.

---

# 36. Transaction Boundaries

Transaction scope should be as small as practical.

Avoid holding transactions open while performing:

- Slow HTTP calls
- SFTP operations
- Long transformations
- User interaction
- Unbounded processing

---

# 37. Distributed Transactions

Do not assume distributed transactions are required.

Evaluate whether the architecture appropriately handles operations across multiple systems.

Possible approaches:

- Compensation
- Eventual consistency
- Idempotency
- Saga-like orchestration

Recommend based on actual business behavior.

---

# 38. Configuration Architecture

Environment-specific values should be externalized.

Examples:

- Hosts
- Ports
- URLs
- Credentials
- Queue names
- Database names
- File paths

Avoid hard-coded environment-specific values in Mule flows.

---

# 39. Secure Configuration

Sensitive configuration should use appropriate secure mechanisms.

Examples:

- Secure Configuration Properties
- Runtime-managed properties
- Secret-management systems

Do not expose credentials in source.

---

# 40. Environment Separation

Architecture should support:

- DEV
- QA
- UAT
- PROD

without requiring source-code modifications for normal environment changes.

---

# 41. Scalability

Evaluate scalability based on:

- Request volume
- Concurrency
- Payload size
- External dependency capacity
- Database capacity
- Connection pools
- Runtime workers
- Messaging throughput

Do not claim scalability solely from flow structure.

---

# 42. Horizontal Scalability

Where multiple workers/instances may run concurrently, evaluate:

- Shared state
- Object Store usage
- File access
- Scheduling
- Duplicate processing
- Idempotency

Avoid assumptions about deployment topology.

---

# 43. Stateful Design

Minimize unnecessary application state.

Identify state stored in:

- Static variables
- Local files
- In-memory structures
- Worker-local state

where this could break horizontal scaling.

---

# 44. Object Store Architecture

Object Store may be appropriate for:

- Short-lived state
- Idempotency
- Caching
- Coordination

Do not use Object Store as a substitute for a proper database when durable business data is required.

---

# 45. Caching Architecture

Caching may be appropriate for:

- Stable reference data
- Expensive read-only operations
- Frequently requested information

Evaluate:

- TTL
- Invalidation
- Consistency
- Memory usage
- Sensitive data

Do not recommend caching data that requires real-time consistency unless the business accepts stale data.

---

# 46. Performance Architecture

Architecture should avoid:

- Excessive sequential calls
- Repeated external lookups
- Large in-memory payloads
- Excessive logging
- Unnecessary transformations
- Excessive parallelism

Performance optimizations must preserve correctness.

---

# 47. Parallel Processing

Parallel processing may improve throughput.

However, evaluate:

- Ordering requirements
- Shared state
- Downstream capacity
- Rate limits
- Connection pools
- Thread usage
- Error aggregation

Do not recommend parallelization blindly.

---

# 48. Streaming Architecture

Streaming should be considered for large:

- Files
- HTTP payloads
- Database results
- Message payloads

Do not introduce streaming where the complete payload is genuinely required in memory.

---

# 49. Observability Architecture

Production integrations should provide enough information to determine:

- What happened
- Which flow processed it
- Which external system was called
- Whether it succeeded
- Why it failed
- How long important operations took
- How to correlate related requests

---

# 50. Correlation IDs

API and integration flows should preserve or generate correlation identifiers where appropriate.

Correlation information should flow across important downstream calls when possible.

---

# 51. Logging Architecture

Logging should be:

- Consistent
- Structured where appropriate
- Actionable
- Secure
- Correlatable

Avoid logging complete payloads by default.

---

# 52. Security Architecture

Evaluate security boundaries across:

- API
- Mule application
- Connectors
- External systems
- Configuration
- Secrets
- Data

Do not treat API authentication as the entire security architecture.

---

# 53. Least Privilege Architecture

Integration identities should have only the permissions required for their responsibilities.

Where permissions cannot be established from source:

`Verification Required`

---

# 54. API Security Architecture

API security should consider:

- Authentication
- Authorization
- TLS
- Rate limiting
- Input validation
- Error handling
- Sensitive data
- Policies

Detailed API security findings belong to the API security skill.

---

# 55. Testability

Architecture should make important behavior testable.

Avoid designs where business logic is tightly embedded in:

- External system calls
- Static configuration
- Large monolithic flows

Prefer appropriately separable logic.

---

# 56. MUnit Architecture

Important business logic should be reasonably testable using MUnit.

Architecture should not unnecessarily prevent:

- Mocking external dependencies
- Verifying flow behavior
- Testing error paths
- Testing transformations

---

# 57. Reusable Error Handling

Where the application has consistent error-handling requirements, consider shared patterns.

Avoid duplicating complex error mapping in every flow.

---

# 58. Reusable Logging

Where common logging requirements exist, consider reusable mechanisms.

Do not abstract every logger into a subflow if it makes debugging harder.

---

# 59. Naming Architecture

Names should reflect architectural responsibility.

Examples:

- `customer-system-api`
- `customer-process-api`
- `customer-experience-api`

Only use such naming when the application actually follows those architectural roles.

---

# 60. Naming Consistency

Flow and API naming should be consistent across:

- Files
- XML
- API specifications
- Properties
- Documentation
- MUnit tests

---

# 61. Deployment Architecture

Where deployment information is visible, review:

- Runtime compatibility
- Worker assumptions
- Environment configuration
- External dependencies
- Scaling considerations

Do not infer exact CloudHub/runtime architecture without evidence.

---

# 62. Runtime Compatibility

Review:

- Mule runtime version
- Java version
- Connector compatibility
- Maven plugin compatibility

Do not recommend runtime upgrades without considering connector compatibility.

---

# 63. Operational Supportability

Architecture should allow support teams to:

- Trace requests
- Identify failures
- Identify dependencies
- Understand retry behavior
- Identify failed records
- Diagnose connector problems

---

# 64. Failure Isolation

A failure in one operation should not unnecessarily cause:

- Unrelated requests to fail
- Entire batch processing to fail
- Other integrations to stop

Assess whether isolation is appropriate.

---

# 65. Back-Pressure

For high-volume integrations, consider whether the architecture can control workload when downstream systems slow down.

Potential mechanisms:

- Queueing
- Rate limiting
- Controlled concurrency
- Batch processing
- Backoff

Do not require explicit back-pressure controls for low-volume synchronous applications.

---

# 66. External API Dependencies

For external APIs evaluate:

- Rate limits
- Timeouts
- Retries
- Authentication
- Versioning
- Failure behavior

Infrastructure limits may require verification.

---

# 67. Versioning

APIs and reusable interfaces should have an appropriate versioning strategy.

Avoid breaking existing consumers without an intentional migration strategy.

---

# 68. Backward Compatibility

When API changes are identified, evaluate:

- Existing consumers
- Contract compatibility
- Required migration
- Versioning

Do not report internal implementation changes as API compatibility issues unless they affect consumers.

---

# 69. Anti-Pattern: God Application

Avoid applications that combine unrelated domains into one Mule application.

Potential indicators:

- Many unrelated APIs
- Many unrelated external systems
- Shared global state
- Large number of unrelated flows

Do not recommend splitting an application solely based on flow count.

Consider:

- Deployment independence
- Ownership
- Scaling
- Security
- Release cadence
- Domain boundaries

---

# 70. Anti-Pattern: God Flow

A flow should be considered a potential God Flow when it combines many unrelated responsibilities and becomes difficult to:

- Understand
- Test
- Change
- Troubleshoot

Provide a decomposition strategy.

---

# 71. Anti-Pattern: Excessive Custom Code

Custom code should not replace MuleSoft capabilities without justification.

Review whether custom code can reasonably be replaced by:

- DataWeave
- Mule processors
- Connectors
- Standard modules

---

# 72. Anti-Pattern: Configuration Duplication

Repeated connector/global configuration should be evaluated for consolidation.

Do not merge configurations that intentionally represent different systems.

---

# 73. Anti-Pattern: Hard-Coded Environment Behavior

Avoid source changes between environments for:

- URLs
- Credentials
- Paths
- Queues
- Database configuration

Use configuration externalization.

---

# 74. Anti-Pattern: Tight Synchronous Chains

A long synchronous chain of external calls can increase:

- Latency
- Failure probability
- Resource consumption
- Timeout complexity

Consider asynchronous or orchestration alternatives only where business semantics allow.

---

# 75. Anti-Pattern: Excessive Parallelism

Parallel execution is not automatically an optimization.

Report potential problems when it can cause:

- Rate-limit violations
- Connection exhaustion
- Database overload
- Ordering problems
- Duplicate processing

---

# 76. Architecture Finding Requirements

Architecture findings must include:

- Finding ID
- Category
- Severity
- Location
- Evidence
- Impact
- Recommendation
- Solution
- Verification where required
- Priority

Example ID:

`MULE-ARCH-001`

---

# 77. Architecture Severity

## Critical

Architecture creates an immediate and severe production, security, or data-integrity risk.

## High

Architecture materially threatens:

- Reliability
- Scalability
- Security
- Maintainability
- Data integrity

## Medium

Meaningful architectural weakness requiring planned improvement.

## Low

Minor architecture improvement.

## Warning

Potential concern requiring business or infrastructure validation.

---

# 78. Architecture Score

Assess architecture across:

- Layering
- Cohesion
- Coupling
- Reusability
- Resilience
- Scalability
- Security
- Observability
- Testability
- Maintainability

The score must reflect architectural quality, not the raw number of findings.

---

# 79. Architecture Report Requirements

The final report must contain:

## Architecture Summary

Describe the architecture actually implemented.

## Architecture Diagram

Show major components and integrations where possible.

## Architecture Strengths

Identify demonstrated good practices.

## Architecture Concerns

Identify meaningful architectural weaknesses.

## Integration Patterns

Describe:

- Synchronous
- Asynchronous
- Batch
- Event-driven
- Request-response
- File-based

where applicable.

## Dependency Map

Identify important external systems.

## Security Architecture

Summarize security boundaries.

## Resilience Architecture

Summarize timeout/retry/error-handling patterns.

## Scalability Architecture

Explain scalability considerations.

## Observability Architecture

Explain logging and traceability.

## Architecture Recommendations

Provide prioritized improvements.

## Architecture Score

Provide the overall architecture assessment.

---

# 80. No Unsupported Architecture Claims

Do not state:

- "This application is API-led"
- "This is a System API"
- "This is a Process API"
- "This is event-driven"
- "This is scalable"
- "This is highly available"

unless repository evidence supports the conclusion.

Use:

`Verification Required`

when deployment or infrastructure information is unavailable.

---

# 81. Architecture Review Quality Gate

Before completing the architecture review, confirm:

- The actual architecture has been identified.
- Major flows have been examined.
- External systems have been identified.
- API boundaries have been evaluated.
- Coupling has been considered.
- Reuse has been considered.
- Error architecture has been reviewed.
- Security architecture has been reviewed.
- Performance architecture has been reviewed.
- Scalability has been considered.
- Observability has been considered.
- Testability has been considered.
- Findings have concrete solutions.
- Speculative findings have been removed.

The final question is:

> Would a Senior MuleSoft Architect be comfortable approving this architecture for production, and if not, exactly what must change?
