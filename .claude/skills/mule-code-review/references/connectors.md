# MuleSoft Connector Review Rules

## Purpose

These rules define how MuleSoft connectors and external-system
integrations must be reviewed.

Applicable connectors may include:

- HTTP
- Database
- Salesforce
- Anypoint MQ
- JMS
- SFTP
- File
- Object Store
- SAP
- Email
- VM
- FTP
- other MuleSoft-supported connectors

Review connector configuration together with:

- global configurations
- flow implementation
- error handling
- retry behavior
- reconnection
- transactions
- authentication
- timeout configuration
- DataWeave
- MUnit
- Maven dependencies
- downstream system behavior

Do not report connector configuration issues based solely on personal
preference.

---

# Connector Review Principles

Before reporting a connector finding:

1. Identify the connector.
2. Identify its version.
3. Identify the global configuration.
4. Inspect how the connector is used.
5. Inspect timeout behavior.
6. Inspect retry/reconnection behavior.
7. Inspect transaction behavior where applicable.
8. Inspect authentication.
9. Inspect external-system failure handling.
10. Inspect performance/resource behavior.
11. Inspect related tests.
12. Determine realistic production impact.

If the connector behavior cannot be established from repository evidence,
inspect related configuration and implementation before reporting.

---

# CON-001 — Incorrect Connector Configuration

## Rule

Flag connector configuration that is invalid, inconsistent with the
connector version, or incompatible with the application's intended
behavior.

Examples:

- invalid operation configuration
- incompatible parameter values
- incorrect connection configuration
- incorrect authentication configuration
- incorrect resource settings
- incompatible transport settings

## Severity

HIGH

Escalate to CRITICAL when the configuration creates a severe security,
data-loss, or availability risk.

---

# CON-002 — Duplicate Global Connector Configuration

## Rule

Flag substantially duplicated global connector configurations when an
existing configuration should be reused.

Consider:

- identical database configurations
- identical HTTP requester configurations
- duplicate Salesforce configurations
- duplicate MQ/JMS configurations

## Severity

LOW

Escalate when duplication creates inconsistent behavior or operational
risk.

Do not report merely because multiple configurations exist.

Different credentials, endpoints, connection pools, or business purposes
may legitimately require separate configurations.

---

# CON-003 — Missing Timeout

## Rule

Flag connector operations that can block indefinitely or for an
uncontrolled duration when an appropriate timeout strategy is required.

Consider:

- connection timeout
- response timeout
- read timeout
- request timeout
- operation timeout
- transaction timeout

## Severity

MEDIUM

Escalate to HIGH when missing timeout behavior can realistically cause:

- thread exhaustion
- worker saturation
- cascading failures
- prolonged message blocking
- severe availability impact

---

# CON-004 — Unsafe Retry

## Rule

Flag retry behavior that can:

- duplicate business operations
- overload downstream systems
- repeat non-idempotent writes
- create inconsistent state
- amplify an existing outage

Review:

- retry count
- retry interval
- backoff
- error types
- operation semantics
- idempotency
- downstream behavior

## Severity

HIGH

---

# CON-005 — Missing Reconnection Strategy

## Rule

Flag missing or inappropriate reconnection behavior when the connector
is expected to recover from transient connection failures.

Consider:

- connection-oriented protocols
- database connections
- messaging brokers
- Salesforce
- SFTP
- external HTTP services
- network instability

## Severity

MEDIUM

Only flag when the integration's failure model warrants a reconnection
strategy.

Do not require reconnection configuration for every connector.

---

# CON-006 — Excessive External Calls

## Rule

Flag flows that make an unnecessarily high number of downstream calls
for a single business operation.

Consider:

- sequential calls
- repeated lookups
- unnecessary validation calls
- avoidable downstream round trips
- calls inside loops

## Severity

MEDIUM / HIGH

Use HIGH when the call volume can realistically cause:

- severe latency
- rate-limit exhaustion
- downstream overload
- production instability

---

# CON-007 — N+1 External Calls

## Rule

Flag connector calls performed once for every item in a collection
when a bulk, batch, query, or aggregation approach is reasonably
available and the collection can become large.

Examples:

- database query per record
- Salesforce call per record
- HTTP request per item
- MQ operation per item

## Severity

HIGH

Do not report when the downstream system requires one operation per
business item and no reasonable batching mechanism exists.

---

# CON-008 — Missing Idempotency

## Rule

Flag connector operations that can be executed more than once and can
produce duplicate business effects without an appropriate idempotency
strategy.

Consider:

- message redelivery
- retry
- network ambiguity
- scheduler retries
- batch retries
- client retries
- connector reconnection

## Severity

HIGH

Do not report when duplicate execution is demonstrably safe.

---

# CON-009 — Incorrect Transaction Boundary

## Rule

Flag transaction boundaries that can cause incorrect commit or rollback
behavior.

Consider:

- database transactions
- JMS transactions
- XA transactions
- message acknowledgement
- connector operations
- nested scopes
- error handlers

## Severity

HIGH

Escalate when incorrect transaction behavior can cause:

- data loss
- duplicate processing
- partial updates
- inconsistent systems

---

# CON-010 — Connector Version Incompatibility

## Rule

Flag connector versions that are incompatible with:

- Mule runtime
- Java version
- Mule Maven Plugin
- other project dependencies

## Severity

HIGH

Do not recommend upgrades merely because newer versions exist.

Only report compatibility problems supported by repository evidence.

---

# CON-011 — Incorrect Authentication Configuration

## Rule

Flag connector authentication that is:

- missing
- incorrectly configured
- inconsistent with the application's security model
- using credentials from insecure locations
- using expired/unsupported authentication mechanisms when evidence exists

## Severity

HIGH

Escalate to CRITICAL when credentials are exposed or authentication can
be bypassed.

---

# CON-012 — Hardcoded Connector Credentials

## Rule

Flag credentials embedded directly in:

- Mule XML
- properties
- DataWeave
- Maven configuration
- deployment configuration
- connector configuration

Consider:

- passwords
- API keys
- client secrets
- access tokens
- private keys

## Severity

CRITICAL

Coordinate with `security.md` for the security finding.

Do not create duplicate findings when the same secret exposure is
already reported as a security finding.

---

# CON-013 — Insecure Connector Transport

## Rule

Flag connector communication using insecure transport when secure
transport is required.

Examples:

- HTTP instead of HTTPS
- insecure FTP instead of SFTP
- weak transport configuration

## Severity

HIGH

Escalate to CRITICAL when sensitive information can be intercepted or
credentials exposed.

---

# CON-014 — TLS Validation Weakness

## Rule

Flag connector configurations that weaken TLS security.

Examples:

- disabled certificate validation
- disabled hostname verification
- trust-all configuration
- insecure TLS protocols
- inappropriate truststore configuration

## Severity

CRITICAL

---

# CON-015 — Excessive Connector Permissions

## Rule

Flag connector credentials or integration identities with permissions
substantially beyond what the application requires when repository
evidence supports the finding.

Examples:

- database account with unnecessary write access
- Salesforce integration with excessive object permissions
- cloud/service identity with unnecessary administrative privileges

## Severity

HIGH

Do not assume permissions that cannot be verified from repository
evidence.

---

# CON-016 — Missing Connection Pooling

## Rule

Flag connector configurations that repeatedly establish expensive
connections when appropriate connection pooling is required.

Consider:

- database connections
- HTTP connections
- messaging connections
- other connection-oriented integrations

## Severity

MEDIUM

Do not require pooling where the connector or workload does not benefit
from it.

---

# CON-017 — Incorrect Connection Pool Configuration

## Rule

Flag pooling configuration that can cause:

- connection exhaustion
- excessive connection creation
- idle resource buildup
- poor concurrency
- downstream overload

Consider:

- maximum pool size
- minimum pool size
- idle timeout
- validation
- connection lifetime

## Severity

MEDIUM

Escalate when resource exhaustion is realistic.

---

# CON-018 — Resource Leak

## Rule

Flag connector usage that can fail to release or properly manage
resources.

Examples:

- connections
- streams
- cursors
- files
- sessions
- temporary resources

## Severity

HIGH

Escalate when repeated execution can exhaust worker or connector
resources.

---

# CON-019 — Large Result Set

## Rule

Flag connector operations that load potentially very large result sets
into memory without appropriate controls.

Consider:

- database queries
- Salesforce queries
- HTTP responses
- file transfers
- messaging operations

## Severity

HIGH

Consider:

- pagination
- streaming
- batching
- limits
- incremental processing

---

# CON-020 — Missing Pagination

## Rule

Flag connector operations that retrieve potentially unbounded datasets
without appropriate pagination when the downstream system supports or
requires it.

## Severity

MEDIUM

Escalate when large result sets can realistically cause:

- memory exhaustion
- excessive latency
- API limit exhaustion
- worker saturation

Do not require pagination for inherently bounded datasets.

---

# CON-021 — Unsafe Batch Size

## Rule

Flag batch operations using unnecessarily large or uncontrolled batch
sizes that can cause:

- memory pressure
- transaction growth
- downstream rejection
- timeout
- partial failure
- rate-limit issues

## Severity

MEDIUM

Escalate to HIGH when production failure is likely.

---

# CON-022 — Incorrect Connector Error Handling

## Rule

Flag connector errors that are:

- swallowed
- incorrectly classified
- incorrectly mapped
- retried unnecessarily
- retried insufficiently
- returned incorrectly to API clients
- treated as successful processing

## Severity

HIGH

Coordinate with `error-handling.md`.

Do not create duplicate findings for the same root cause.

---

# CON-023 — Connector Error Type Misclassification

## Rule

Flag handling based on an incorrect Mule connector error type.

Examples:

- treating authentication failure as a transient error
- retrying validation errors
- treating timeout as successful completion
- treating permanent downstream errors as transient

## Severity

HIGH

---

# CON-024 — Retry Amplification

## Rule

Flag multiple retry mechanisms that can multiply downstream requests.

Consider:

- connector retry
- `until-successful`
- API gateway retry
- client retry
- scheduler retry
- messaging redelivery

## Severity

HIGH

Potential consequences include:

- retry storms
- duplicate processing
- downstream overload
- severe latency

---

# CON-025 — Missing Backoff

## Rule

Flag retry behavior that repeatedly retries a failing downstream
system without appropriate delay/backoff when rapid retries can worsen
the failure.

## Severity

MEDIUM

Escalate when the behavior can realistically create a retry storm.

---

# CON-026 — Rate Limit Risk

## Rule

Flag connector usage that can realistically exceed downstream:

- API limits
- concurrency limits
- request quotas
- database capacity
- messaging throughput

Consider:

- loops
- parallel processing
- retries
- schedulers
- batch processing

## Severity

HIGH

---

# CON-027 — Missing Rate Limit Handling

## Rule

Flag integrations that do not appropriately handle known downstream
rate-limit responses when rate limiting is part of the external
system's behavior.

Consider:

- HTTP 429
- Salesforce limits
- API quotas
- MQ throttling
- database connection limits

## Severity

MEDIUM

Escalate when rate-limit failures can cause message loss or prolonged
outage.

---

# CON-028 — Incorrect Handling of Downstream 4xx

## Rule

Flag integrations that incorrectly retry or treat permanent
downstream client/business errors as transient failures.

Examples:

- invalid request
- validation failure
- unauthorized request
- forbidden operation
- missing resource

## Severity

MEDIUM / HIGH

---

# CON-029 — Incorrect Handling of Downstream 5xx

## Rule

Flag integrations that fail to appropriately handle transient
downstream server failures.

Consider:

- retry
- backoff
- circuit protection
- error propagation
- dead-letter behavior

## Severity

MEDIUM / HIGH

Only report when the application's failure model warrants the behavior.

---

# CON-030 — Authentication Token Lifecycle Problem

## Rule

Flag connector integrations where authentication tokens are:

- unnecessarily requested repeatedly
- not refreshed appropriately
- cached unsafely
- exposed
- used after expiration

## Severity

HIGH

---

# CON-031 — Unnecessary Authentication Calls

## Rule

Flag flows that repeatedly authenticate with a downstream service when
the connector supports safe token/session reuse.

## Severity

MEDIUM

Escalate when this causes significant latency, rate-limit consumption,
or downstream load.

---

# CON-032 — Connector Configuration Duplication

## Rule

Flag repeated connector configuration embedded directly within flows
when a reusable global configuration would materially improve
consistency or operational management.

## Severity

LOW

Do not report simple differences that legitimately require separate
configurations.

---

# CON-033 — Environment Configuration Hardcoded

## Rule

Flag environment-specific connector values embedded directly in source.

Examples:

- URLs
- hostnames
- ports
- usernames
- queue names
- Salesforce endpoints
- SFTP locations
- database URLs

## Severity

MEDIUM

Escalate when credentials or secrets are involved.

---

# CON-034 — Incorrect Environment Resolution

## Rule

Flag connector configuration where environment-specific properties may
resolve incorrectly or where the application can connect to the wrong
environment.

Consider:

- property placeholders
- secure properties
- deployment variables
- default values
- environment selection

## Severity

HIGH

---

# CON-035 — Unsafe Default Connector Configuration

## Rule

Flag defaults that can cause production integrations to connect to:

- development systems
- test systems
- localhost
- unintended endpoints
- insecure endpoints

## Severity

HIGH

---

# CON-036 — Incorrect Database Connector Usage

## Rule

For Database Connector usage, review:

- SQL correctness
- parameterization
- connection pooling
- transactions
- result-set size
- pagination
- timeouts
- commit/rollback
- batch operations

## Severity

Use the severity appropriate to the specific issue.

Refer to:

`references/database.md`

for database-specific rules.

---

# CON-037 — Incorrect Salesforce Connector Usage

## Rule

For Salesforce integrations, review where applicable:

- API limits
- bulk operations
- query limits
- pagination
- authentication
- retry behavior
- duplicate processing
- object permissions
- large result sets
- batch sizing

## Severity

Use the severity appropriate to the specific issue.

---

# CON-038 — Incorrect Messaging Connector Usage

## Rule

For messaging connectors, review:

- acknowledgement
- redelivery
- duplicate processing
- visibility/lock duration
- dead-letter handling
- ordering
- retry
- transactions
- poison messages

## Severity

Use the severity appropriate to the specific issue.

Refer to:

`references/messaging.md`

---

# CON-039 — Incorrect HTTP Request Connector Usage

## Rule

For HTTP Request usage, review:

- connection timeout
- response timeout
- authentication
- TLS
- retry
- idempotency
- connection reuse
- headers
- status-code handling
- payload size
- downstream rate limits

## Severity

Use the severity appropriate to the specific issue.

Refer to:

`references/api.md`

for API-specific behavior.

---

# CON-040 — Incorrect SFTP/File Connector Usage

## Rule

For file-based integrations, review:

- secure transport
- file naming
- duplicate processing
- atomicity
- partial files
- polling behavior
- file locking
- archive behavior
- error recovery
- large file handling
- streaming

## Severity

Use the severity appropriate to the specific issue.

---

# CON-041 — Incorrect Object Store Usage

## Rule

For Object Store usage, review:

- key uniqueness
- expiration
- persistence requirements
- duplicate processing
- concurrency
- object size
- error handling
- sensitive data storage
- environment separation

## Severity

Use the severity appropriate to the specific issue.

---

# CON-042 — Connector Operation Inside Unbounded Loop

## Rule

Flag connector operations executed inside loops where the collection
can become large or unbounded and the operation can cause significant
resource or downstream impact.

## Severity

HIGH

Consider:

- N+1 behavior
- rate limits
- transaction duration
- memory
- latency
- retry amplification

---

# CON-043 — Sequential Calls Where Bulk Operation Exists

## Rule

Flag sequential connector calls when the external system provides a
reasonable bulk/batch operation that would materially reduce calls and
improve reliability or performance.

## Severity

MEDIUM

Do not report when individual operations are required by business
semantics.

---

# CON-044 — Unnecessary Parallel Connector Calls

## Rule

Flag excessive parallel connector execution when it can cause:

- downstream overload
- rate-limit violations
- connection exhaustion
- transaction contention
- unpredictable ordering

## Severity

HIGH

Do not report parallelism merely because sequential execution is another
possible design.

---

# CON-045 — Incorrect Connector Concurrency

## Rule

Flag connector concurrency configuration that exceeds what the
downstream system or application can safely support.

Consider:

- pool size
- worker concurrency
- parallel-for-each
- batch concurrency
- rate limits

## Severity

HIGH

---

# CON-046 — Missing Downstream Circuit Protection

## Rule

Flag integrations where repeated calls to an unavailable or severely
degraded downstream system can cause cascading failures and no
appropriate protection exists.

Consider:

- circuit breaker patterns
- bounded retries
- backoff
- queue-based decoupling
- timeout controls

## Severity

MEDIUM

Only report when the architecture and failure model support the concern.

---

# CON-047 — Synchronous External Dependency Risk

## Rule

Flag synchronous connector dependencies where an unreliable or slow
external system creates significant availability coupling.

## Severity

MEDIUM

Escalate to HIGH when downstream failure can realistically exhaust
application resources or cause widespread outage.

Do not prescribe asynchronous processing solely as an architectural
preference.

---

# CON-048 — Missing External Failure Recovery

## Rule

Flag integrations with realistic external failure scenarios but no
appropriate recovery strategy.

Examples:

- connection failure
- timeout
- authentication failure
- throttling
- downstream outage
- transient network failure

## Severity

MEDIUM / HIGH

---

# CON-049 — Incorrect Message Acknowledgement

## Rule

For messaging connectors, flag acknowledgement behavior that can cause:

- message loss
- premature acknowledgement
- repeated redelivery
- acknowledgement after incomplete processing

## Severity

CRITICAL / HIGH

Use CRITICAL when message loss is likely.

---

# CON-050 — Incorrect Dead-Letter Handling

## Rule

Flag messaging integrations where permanently failing messages can be
redelivered indefinitely or lost without appropriate dead-letter or
failure handling.

## Severity

HIGH

Only report when the messaging platform and application behavior support
the concern.

---

# CON-051 — Poison Message Risk

## Rule

Flag messages that can repeatedly fail processing without an effective
mechanism to prevent continuous redelivery.

## Severity

HIGH

---

# CON-052 — Incorrect Connector Transaction Scope

## Rule

Flag transactions that incorrectly include or exclude external
connector operations.

Consider:

- transaction boundaries
- XA
- local transactions
- message acknowledgement
- database commits
- downstream calls

## Severity

HIGH

---

# CON-053 — Long-Running Connector Transaction

## Rule

Flag transactions that remain open while performing slow or unrelated
external operations.

Potential consequences:

- connection exhaustion
- lock contention
- transaction timeout
- rollback complexity

## Severity

HIGH

---

# CON-054 — Connector Streaming Disabled

## Rule

Flag connector configuration or usage that unnecessarily materializes
large data instead of using streaming or incremental processing when
streaming is appropriate.

## Severity

HIGH

Coordinate with:

`references/dataweave.md`

---

# CON-055 — Incorrect Stream Consumption

## Rule

Flag connector operations that consume non-repeatable streams and later
attempt to reuse them without an appropriate repeatable stream strategy.

## Severity

HIGH

---

# CON-056 — Excessive Connector Logging

## Rule

Flag logging around connector operations that records:

- complete payloads
- credentials
- tokens
- authorization headers
- large responses
- sensitive downstream data

when such logging provides limited diagnostic value.

## Severity

MEDIUM

Escalate to HIGH/CRITICAL when sensitive information is exposed.

Coordinate with:

`references/security.md`

---

# CON-057 — Connector Observability Gap

## Rule

Flag critical external integrations where established application
observability requires information such as:

- correlation ID
- operation
- downstream system
- latency
- outcome
- retry count
- error classification

but sufficient diagnostic information is unavailable.

## Severity

LOW / MEDIUM

Escalate when production support is materially affected.

---

# CON-058 — Missing Connector Metrics

## Rule

Flag important integrations where the architecture requires operational
metrics but connector activity cannot reasonably be monitored.

Consider:

- request count
- success/failure
- latency
- retry count
- throttling
- connection failures

## Severity

LOW

Escalate when the integration is business-critical.

---

# CON-059 — Connector Dependency Not Tested

## Rule

Flag important connector failure behavior that is not meaningfully
tested when the behavior represents significant production risk.

Consider:

- timeout
- authentication failure
- downstream 4xx/5xx
- connection failure
- redelivery
- retry exhaustion

## Severity

MEDIUM

Do not require every connector operation to have an exhaustive test.

---

# CON-060 — Connector Configuration Drift

## Rule

Flag materially inconsistent configuration patterns for the same
external system when they can cause different runtime behavior.

Consider:

- timeout differences
- authentication differences
- retry differences
- endpoint differences
- TLS differences

## Severity

MEDIUM

---

# Connector-Specific Review Matrix

For each important connector integration, evaluate:

| Area | Review |
|---|---|
| Connector | Identify connector and operation |
| Version | Verify dependency version |
| Global configuration | Verify reuse and correctness |
| Authentication | Verify security |
| Endpoint | Verify environment resolution |
| TLS | Verify secure transport |
| Timeout | Verify bounded execution |
| Retry | Verify safety |
| Reconnection | Verify recovery |
| Pooling | Verify resource management |
| Transactions | Verify boundaries |
| Idempotency | Verify duplicate behavior |
| Rate limits | Verify downstream limits |
| Pagination | Verify large-result handling |
| Streaming | Verify large-payload behavior |
| Concurrency | Verify downstream capacity |
| Error handling | Verify failure behavior |
| Observability | Verify diagnostics |
| Testing | Verify failure-path coverage |

---

# Connector Review by Integration Type

## HTTP

Review:

- timeout
- TLS
- authentication
- retry
- idempotency
- status handling
- headers
- rate limits
- connection reuse
- payload size

## Database

Review:

- pooling
- transactions
- parameterized queries
- result-set size
- pagination
- timeout
- connection leaks

Refer to:

`references/database.md`

## Salesforce

Review:

- authentication
- API limits
- query pagination
- bulk APIs
- retry
- duplicate processing
- permissions
- large result sets

## Messaging

Review:

- acknowledgement
- redelivery
- duplicate processing
- ordering
- dead-letter behavior
- transactions
- retry

Refer to:

`references/messaging.md`

## SFTP / File

Review:

- secure transport
- file locking
- duplicate files
- partial files
- polling
- archive
- large files
- streaming
- failure recovery

## Object Store

Review:

- key design
- expiration
- persistence
- concurrency
- duplicate processing
- sensitive data
- environment isolation

## SAP / Enterprise Connectors

Review:

- connection management
- transaction behavior
- timeout
- retry
- large data
- batching
- authentication
- downstream availability

---

# Connector Finding Quality Gate

Before reporting a connector finding:

1. Identify the connector.
2. Identify the operation.
3. Inspect the global configuration.
4. Inspect connector version.
5. Inspect related properties.
6. Inspect error handling.
7. Inspect retry/reconnection.
8. Inspect transaction behavior.
9. Inspect downstream impact.
10. Inspect related tests.
11. Verify the issue is not already handled elsewhere.
12. Confirm realistic production impact.
13. Confirm severity.
14. Identify exact file/location.

If evidence is insufficient, do not report the issue.

---

# Connector False-Positive Controls

Do not report:

- missing reconnection for every connector
- connection pooling for every connector
- pagination for inherently bounded data
- rate limiting for every integration
- circuit breakers for every downstream service
- asynchronous processing solely as an architectural preference
- duplicate global configurations when they have legitimate purposes
- retries without first understanding the connector and operation
- missing idempotency when duplicate execution is demonstrably safe
- performance concerns without a reasonable mechanism

---

# Cross-Reference Rules

Connector findings should be coordinated with other review references.

Use:

- `references/security.md` for credentials, TLS, secrets, and security
- `references/error-handling.md` for error propagation and error types
- `references/dataweave.md` for transformation and streaming behavior
- `references/database.md` for database-specific concerns
- `references/messaging.md` for messaging semantics
- `references/api.md` for public API behavior
- `references/performance.md` for application-wide performance concerns
- `references/munit.md` for connector test coverage

Do not report the same root cause as multiple independent findings unless
the impacts are materially different.

---

# Connector Finding Format

Use:

**Finding ID:** CON-001

**Severity:** HIGH

**Category:** CONNECTOR

**File:** `src/main/mule/example.xml:125`

**Connector:** HTTP Request

**Operation:** Request

**Location:** `flow-name / processor`

**Problem:**

Describe the connector problem.

**Evidence:**

Identify the configuration and implementation evidence.

**Technical Mechanism:**

Explain how the connector behaves and why the configuration creates the
problem.

**Impact:**

Explain realistic production, business, security, reliability, or
performance impact.

**Recommendation:**

Provide an actionable remediation approach.

**Confidence:** HIGH / MEDIUM / LOW