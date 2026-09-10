# Logging and Observability Review Rules

## Purpose

Review MuleSoft logging and observability for:

* sensitive-data protection
* diagnostic usefulness
* correlation and traceability
* log-level correctness
* exception visibility
* operational context
* logging volume
* duplicate logging
* production performance
* incident troubleshooting

Logging findings must be evidence-based.

Do not report missing logging merely because additional logs could be
useful when operational requirements are unknown.

---

# Review Areas

Inspect, where applicable:

* Logger processors
* log levels
* log messages
* correlation IDs
* trace identifiers
* request identifiers
* business identifiers where appropriate
* exception information
* error types
* error descriptions
* flow/component context
* payload logging
* attributes logging
* variables logging
* authentication headers
* credentials
* tokens
* PII
* confidential data
* repeated logging
* logging inside loops
* logging inside high-frequency flows
* logging in error handlers
* logging at retry boundaries

Review logging together with error handling and integration behavior.

---

# Logging Review Principles

Before reporting a logging finding:

1. Identify the logger or missing diagnostic context.
2. Inspect the value/expression being logged.
3. Trace the source of the logged data.
4. Determine whether sensitive information can reach the log.
5. Determine the execution context.
6. Inspect correlation/trace information.
7. Inspect error handling.
8. Inspect log levels.
9. Consider execution frequency.
10. Consider payload size.
11. Check whether the same event is logged elsewhere.
12. Determine actual operational or production impact.
13. Assign severity and confidence based on evidence.

Do not treat a preferred logging style as a defect.

---

# LOG-001 — Sensitive Information Logged

## Description

The application logs sensitive information that should not be present in
operational logs.

Potential information includes:

* passwords
* API keys
* access tokens
* authorization headers
* client secrets
* private keys
* PII
* financial information
* confidential business data
* secure property values
* sensitive payload fields

## Finding Gate

The review must establish both:

1. the information is sensitive, and
2. the information can reach a log destination.

Do not report a logger as sensitive merely because its expression
references a generic payload or variable.

## Evidence Requirements

Identify:

* logger location
* sensitive data source
* logging expression
* exposure path

Never reproduce the sensitive value.

Use:

`[REDACTED]`

where necessary.

## Impact Examples

Potential impacts include:

* credential disclosure
* privacy breach
* unauthorized access
* compliance exposure
* sensitive-data leakage

---

# LOG-002 — Full Payload Logged Without Sufficient Justification

## Description

The application logs an entire payload or large data structure where
doing so creates a meaningful security, performance, storage, or
operational risk and there is no evidence supporting the requirement.

Potential mechanisms include:

* logging `payload` directly
* logging complete HTTP requests/responses
* logging large collections
* logging complete message bodies
* logging payloads at high-frequency execution points

## Finding Gate

Full-payload logging is not automatically a defect.

Consider:

* whether the payload contains sensitive information
* payload size
* execution frequency
* environment
* log level
* operational necessity
* whether a targeted subset would provide equivalent diagnostic value

If operational requirements are unknown, do not assume full-payload
logging is prohibited.

A finding requires a credible production consequence.

## Evidence Requirements

Identify:

* logger
* payload/data being logged
* execution context
* approximate size or frequency where available
* resulting risk

## Impact Examples

Potential impacts include:

* excessive log volume
* increased storage consumption
* performance degradation
* sensitive-data exposure
* increased incident-response exposure

---

# LOG-003 — Meaningful Operational Context Missing

## Description

A production-critical operation lacks diagnostic context necessary to
identify or correlate failures, and the absence creates a meaningful
operational risk.

Potential context includes:

* correlation ID
* trace ID
* flow/component identifier
* transaction/business identifier
* relevant external-system identifier
* error type
* meaningful failure context

## Finding Gate

Do not report missing logging merely because more information could be
added.

The finding requires evidence that:

* the operation is operationally significant,
* a failure or investigation scenario is realistic, and
* the available logs cannot reasonably identify or correlate the event.

Where operational requirements are unknown, record a limitation rather
than creating a finding.

## Evidence Requirements

Identify:

* affected flow/operation
* existing diagnostic logging
* missing context
* realistic troubleshooting scenario
* operational consequence

## Impact Examples

Potential impacts include:

* difficult incident correlation
* longer troubleshooting time
* inability to trace a transaction
* poor failure diagnosis
* reduced operational visibility

---

# LOG-004 — Excessive Logging Creates Production Risk

## Description

Logging volume or placement creates a credible production risk through
excessive CPU, I/O, storage, latency, or log-ingestion load.

Potential mechanisms include:

* logging inside high-volume loops
* repeated logging during retries
* verbose logging on high-frequency endpoints
* large payload logging
* duplicate logging at multiple layers
* excessive exception logging
* repeated serialization for logging

## Finding Gate

Do not report excessive logging solely because multiple Logger
processors exist.

Establish a credible mechanism involving factors such as:

* execution frequency
* loop size
* retry count
* payload size
* log level
* serialization cost
* deployment scale

## Evidence Requirements

Identify:

* logger location
* execution context
* repetition mechanism
* data volume where available
* production consequence

## Impact Examples

Potential impacts include:

* increased latency
* CPU consumption
* I/O pressure
* log-storage growth
* log-ingestion throttling
* increased operational cost

---

# Correlation and Traceability

For important synchronous and asynchronous operations, consider whether
logs can be correlated across:

* inbound request
* internal flows
* flow references
* retries
* outbound requests
* messaging
* asynchronous processing
* error handling

Do not require a specific correlation implementation unless the
repository or operational context establishes the requirement.

---

# Error and Exception Logging

Inspect whether important failures retain useful context such as:

* error type
* meaningful description
* relevant flow/component
* correlation information
* external-system context
* sanitized diagnostic information

Do not require stack traces or complete exception objects in every log.

Consider whether logging duplicates the same exception at multiple
layers.

---

# Log Level Review

Consider whether logging is placed at an appropriate level for its
purpose.

Potential concerns include:

* verbose diagnostic data permanently emitted at high operational volume
* critical failures logged only at an inappropriate low-severity level
* sensitive data logged at any level
* expected control-flow conditions logged as errors

A log-level difference is not automatically a finding.

The level must create a meaningful operational consequence.

---

# Duplicate Logging

Multiple components may legitimately log the same event at different
boundaries.

Do not report duplicate logging merely because similar messages exist.

Report it only when duplication creates a meaningful consequence such
as:

* substantial log amplification
* misleading incident counts
* repeated sensitive-data exposure
* significant operational noise

---

# Logging in Loops and Retries

Pay particular attention to logging inside:

* `foreach`
* batch processing
* retry scopes
* reconnection attempts
* polling flows
* message consumers

Determine whether the number of log entries can grow materially with:

* record count
* retry count
* concurrency
* polling frequency

Do not assume that logging inside a loop is unsafe without a credible
production mechanism.

---

# Security Coordination

Coordinate logging review with:

* Security
* Error Handling
* Configuration

If a logger exposes a secret, use `SEC-002` for the primary security
finding where appropriate and avoid creating a duplicate `LOG-001` unless
the logging-specific root cause or remediation materially differs.

Similarly, sensitive error responses should normally be evaluated under
the appropriate security/error-handling finding rather than duplicated
solely because a logger is involved.

---

# Severity Guidance

Severity must reflect actual production impact.

### CRITICAL

Use only for catastrophic exposure or operational consequences such as:

* highly privileged credential exposure
* widespread sensitive-data disclosure

### HIGH

Use for:

* significant secret exposure
* major PII/confidential-data exposure
* severe log amplification causing meaningful production instability

### MEDIUM

Use for:

* meaningful sensitive-data exposure with contained scope
* material logging-related performance/storage risk
* significant diagnostic gaps affecting critical operations

### LOW

Use for:

* limited operational visibility gaps
* lower-impact logging inefficiencies

### NIT

Use only for optional logging improvements without material production
impact.

---

# False-Positive Controls

Do not create a logging finding when:

* the logged value is not sensitive
* sensitive data is appropriately masked
* full-payload logging is justified by known operational requirements
* logging volume has no credible production consequence
* correlation context is available elsewhere
* operational requirements are unknown
* duplicate logging has no meaningful impact
* another control already mitigates the concern
* evidence is insufficient

When evidence is insufficient:

**Do not report the finding.**

---

# Positive Logging Indicators

Where supported by evidence, recognize strengths such as:

* sensitive values masked
* credentials excluded from logs
* meaningful correlation IDs
* useful error context
* appropriate log levels
* targeted rather than full-payload logging
* consistent operational event logging
* appropriate retry/error visibility
* controlled logging volume
* clear flow/component context

Positive observations must be evidence-backed.

---

# Required Finding Fields

Any logging finding must include:

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
* client secrets
* access tokens
* private keys
* authorization headers
* secure property values
* sensitive payload values

Sensitive information must be sanitized before inclusion in the review
artifact.