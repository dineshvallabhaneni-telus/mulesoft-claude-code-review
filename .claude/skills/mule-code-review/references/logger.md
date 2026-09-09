# Logging Review Rules

## Purpose

These rules define how logging must be reviewed in Mule 4 applications.

The objective is to determine whether application logging provides useful
operational diagnostics without introducing:

- security exposure
- PII exposure
- excessive log volume
- performance problems
- misleading diagnostics
- loss of correlation information
- unnecessary duplication
- production support difficulties

Logging findings must be based on actual repository evidence.

Do not require logging merely for the sake of increasing log volume.

---

## Logging Review Principles

Before reporting a logging finding:

1. Inspect the logger configuration.
2. Inspect the message being logged.
3. Inspect the surrounding flow.
4. Inspect error handling.
5. Determine whether the flow is production-facing.
6. Determine whether the logged information is sensitive.
7. Determine expected execution frequency.
8. Determine whether correlation information is preserved.
9. Check whether the same information is logged elsewhere.
10. Assess the operational value of the log.
11. Assess performance and storage implications.
12. Confirm the finding is not already handled elsewhere.

Do not report logging issues merely because a different logging format
could be used.

---

# LOG-001 — Sensitive Information

## Rule

Flag logging of sensitive information including:

- passwords
- access tokens
- API keys
- client secrets
- authorization headers
- private keys
- database credentials
- encryption keys
- sensitive personal information
- confidential business information
- sensitive request or response payloads

## Severity

HIGH / CRITICAL

Use CRITICAL when the logged information provides direct access to
credentials, authentication material, or other secrets.

Use HIGH for sensitive information that creates meaningful privacy or
confidentiality risk.

Coordinate with:

- `references/security.md`

---

# LOG-002 — Full Payload Logging

## Rule

Flag full payload logging when the payload can contain:

- sensitive information
- PII
- credentials
- confidential business data
- very large data
- binary data
- high-volume integration messages

Consider whether logging the complete payload is necessary for
diagnostics.

## Severity

MEDIUM

Escalate when sensitive information is exposed.

---

# LOG-003 — Excessive Logging

## Rule

Flag logging that can generate excessive volume in production paths.

Examples include:

- logging every record in a large batch
- logging every message in a high-throughput queue
- logging large payloads repeatedly
- logging inside large collection loops
- repeated DEBUG/INFO logging in frequently executed processors

## Severity

LOW / MEDIUM

Escalate when the logging can materially affect:

- application performance
- storage costs
- log ingestion
- operational usability

---

# LOG-004 — Missing Useful Error Context

## Rule

Flag errors that cannot be diagnosed effectively because important
context is missing.

Useful context may include:

- correlation identifier
- business identifier
- operation name
- external system
- endpoint
- error type
- relevant non-sensitive request information
- processing stage

Do not require sensitive payload information to provide context.

## Severity

MEDIUM

---

# LOG-005 — Correlation Identifier Loss

## Rule

Flag integration paths where correlation information is unexpectedly
lost or not propagated when it is required for operational tracing.

Consider:

- HTTP flows
- asynchronous messaging
- batch processing
- subflows
- external system calls
- error handlers

## Severity

MEDIUM

Only report when the application has an established or necessary
correlation strategy.

---

# LOG-006 — Misleading Log Level

## Rule

Flag messages logged at a level that does not accurately represent the
operational significance of the event.

Examples:

- production failures logged only at DEBUG
- severe integration failures logged as INFO
- normal business events logged as ERROR
- expected validation failures logged as ERROR without justification

## Severity

LOW

Escalate when incorrect levels materially affect incident detection or
operational support.

---

# LOG-007 — Sensitive Exception Details

## Rule

Flag exception logging or error responses that expose:

- passwords
- tokens
- credentials
- internal URLs
- database connection information
- SQL details containing sensitive data
- internal infrastructure information
- stack traces to unauthorized clients
- confidential implementation details

## Severity

HIGH

Coordinate with:

- `references/security.md`
- `references/error-handling.md`

---

# LOG-008 — Duplicate Logging

## Rule

Flag the same error being logged repeatedly at multiple layers without
meaningful additional context.

Common examples include:

- connector logs the failure
- flow logs the same failure
- global error handler logs the same failure
- API layer logs the same failure again

## Severity

LOW

Escalate when duplicate logging creates significant production noise.

---

# LOG-009 — Logging Secrets Through Variables

## Rule

Flag logger expressions that indirectly expose sensitive values stored
in variables, attributes, payloads, or properties.

Examples include logging:

- `vars.accessToken`
- `vars.clientSecret`
- authorization headers
- secure property values
- credential-containing attributes

## Severity

CRITICAL / HIGH

Do not report merely because a variable exists.

Verify that the sensitive value can actually reach the logger.

---

# LOG-010 — Authorization Header Logging

## Rule

Flag logging of HTTP authorization headers or equivalent authentication
metadata.

Examples include:

- `Authorization`
- Bearer tokens
- Basic authentication credentials
- API authentication headers

## Severity

CRITICAL

Coordinate with:

- `references/security.md`

---

# LOG-011 — Sensitive HTTP Header Logging

## Rule

Flag logging of HTTP headers that can contain sensitive information.

Examples include:

- authorization headers
- cookies
- session identifiers
- API keys
- client credentials
- security tokens

## Severity

HIGH

---

# LOG-012 — Sensitive Request Logging

## Rule

Flag request logging where the request can contain sensitive fields such
as:

- passwords
- payment information
- personal information
- credentials
- tokens
- confidential business data

## Severity

HIGH

Do not report generic request logging without evidence that the request
contains sensitive information.

---

# LOG-013 — Sensitive Response Logging

## Rule

Flag response logging where downstream responses can contain:

- credentials
- tokens
- PII
- confidential information
- internal system information

## Severity

HIGH

---

# LOG-014 — Binary Payload Logging

## Rule

Flag logging of binary payloads or large binary content where logging
provides little diagnostic value and can cause excessive memory usage or
log volume.

Examples include:

- files
- images
- documents
- large attachments
- binary messages

## Severity

MEDIUM

---

# LOG-015 — Logging Inside Large Loops

## Rule

Flag logging inside loops that process potentially large collections when
the log volume can become excessive.

Examples include:

- Batch records
- large database results
- large API collections
- message lists

## Severity

MEDIUM

Only report when the collection size can realistically become large.

---

# LOG-016 — Logging Inside High-Throughput Flow

## Rule

Flag high-frequency logging in flows that can process a large number of
requests or messages.

Consider:

- queue consumers
- APIs with high request volume
- polling flows
- streaming flows
- batch processing

## Severity

LOW / MEDIUM

---

# LOG-017 — Logging Payload Multiple Times

## Rule

Flag the same large or sensitive payload being logged repeatedly within
the same processing path.

## Severity

MEDIUM

---

# LOG-018 — Missing Integration Context

## Rule

Flag important external-system failures where logs do not identify the
integration context necessary for troubleshooting.

Useful information may include:

- external system name
- operation
- endpoint identifier
- business transaction identifier
- correlation identifier
- retry attempt

Do not log secrets or sensitive payloads merely to provide context.

## Severity

MEDIUM

---

# LOG-019 — Missing Retry Context

## Rule

For retry-enabled integrations, flag logs that do not provide enough
information to determine:

- that a retry occurred
- retry attempt
- operation being retried
- eventual success or failure

## Severity

LOW / MEDIUM

Only report when retry behavior is operationally important.

---

# LOG-020 — Missing Failure Context

## Rule

Flag error logs that identify only that an error occurred but provide no
useful information about:

- operation
- flow
- external dependency
- error type
- business context

## Severity

MEDIUM

---

# LOG-021 — Incorrect Correlation Propagation

## Rule

Flag flows that overwrite, remove, or replace correlation information
without a valid reason.

## Severity

MEDIUM

Only report when the behavior materially affects distributed tracing or
incident investigation.

---

# LOG-022 — Correlation Identifier Logged as Sensitive Data

## Rule

Do not automatically classify correlation identifiers as secrets.

Only flag them when repository evidence demonstrates that the identifier
contains or exposes sensitive information.

## Severity

LOW / MEDIUM

---

# LOG-023 — Debug Logging Enabled in Production Configuration

## Rule

Flag production configuration that enables unnecessarily verbose
logging when it can create significant:

- log volume
- performance impact
- sensitive-data exposure
- operational noise

## Severity

MEDIUM

Do not report DEBUG logging merely because DEBUG exists in the application.

---

# LOG-024 — Production Logging Configuration Missing

## Rule

Flag applications where production logging configuration is required
for operational support but is absent or materially incomplete.

Consider:

- log levels
- appenders
- structured logging
- correlation information
- error output

## Severity

LOW / MEDIUM

Only report when repository evidence shows that the missing configuration
creates an operational problem.

---

# LOG-025 — Incorrect Logger Configuration

## Rule

Flag logger configuration that can cause:

- logs to be lost
- incorrect log routing
- unexpected log levels
- excessive logging
- inconsistent production behavior

## Severity

MEDIUM

---

# LOG-026 — Logging Sensitive Properties

## Rule

Flag logger expressions that expose values loaded from:

- secure properties
- environment variables
- deployment secrets
- credential configuration

## Severity

CRITICAL / HIGH

---

# LOG-027 — Logging Database Credentials

## Rule

Flag logs containing:

- database usernames when sensitive
- database passwords
- JDBC credentials
- connection strings containing credentials

## Severity

CRITICAL

---

# LOG-028 — Logging SQL With Sensitive Values

## Rule

Flag SQL logging that exposes sensitive parameter values or confidential
business data.

## Severity

HIGH

Do not automatically flag SQL statement logging when the statement
contains no sensitive information and provides meaningful diagnostic
value.

---

# LOG-029 — Logging External Authentication Data

## Rule

Flag logs containing authentication material exchanged with external
systems.

Examples include:

- OAuth tokens
- client secrets
- API keys
- signed authentication data
- session credentials

## Severity

CRITICAL

---

# LOG-030 — Logging PII

## Rule

Flag unnecessary logging of personally identifiable information when
the information is not required for operational diagnosis.

Examples include:

- full names
- email addresses
- phone numbers
- addresses
- government identifiers
- customer identifiers
- financial information

## Severity

HIGH

The exact severity depends on the sensitivity and exposure.

---

# LOG-031 — Excessive Stack Trace Logging

## Rule

Flag repeated or unnecessary stack trace logging when the same exception
is already captured elsewhere and the additional stack trace provides no
meaningful diagnostic value.

## Severity

LOW / MEDIUM

Do not suppress stack traces when they are necessary for diagnosing an
unexpected technical failure.

---

# LOG-032 — Stack Trace Exposed to API Client

## Rule

Flag API responses that expose internal stack traces or exception
details to clients.

## Severity

HIGH

Coordinate with:

- `references/error-handling.md`
- `references/api.md`
- `references/security.md`

---

# LOG-033 — Internal Infrastructure Exposure

## Rule

Flag logs or client-visible errors exposing unnecessary internal
infrastructure details.

Examples include:

- internal hostnames
- internal IP addresses
- database server names
- internal filesystem paths
- cloud infrastructure identifiers
- internal service topology

## Severity

MEDIUM / HIGH

Escalate when the information creates a meaningful security risk.

---

# LOG-034 — Log Message Without Actionable Context

## Rule

Flag log messages that provide insufficient information for an operator
to understand what failed or what action may be required.

Avoid messages such as:

- generic failure messages
- unexplained error codes
- "processing failed" without context

## Severity

LOW / MEDIUM

---

# LOG-035 — Incorrect Success Logging

## Rule

Flag logging that indicates successful processing when the operation has
not actually completed successfully.

Examples include:

- logging success before downstream processing completes
- logging success before transaction commit
- logging successful publication before acknowledgement

## Severity

MEDIUM / HIGH

Escalate when the misleading log can cause operators to incorrectly
believe a business transaction succeeded.

---

# LOG-036 — Missing Completion Logging for Critical Processing

## Rule

Flag important long-running or asynchronous operations where there is no
sufficient operational evidence that processing completed.

Consider:

- batch processing
- asynchronous messages
- scheduled jobs
- long-running integrations

## Severity

LOW / MEDIUM

Only report when completion visibility is important for operations.

---

# LOG-037 — Incorrect Error Logging After Error Continuation

## Rule

Flag flows where an error is continued but logging does not clearly
indicate that processing continued or what business outcome occurred.

## Severity

MEDIUM

Coordinate with:

- `references/error-handling.md`

---

# LOG-038 — Error Logged Without Correlation Context

## Rule

Flag important errors where the log does not preserve enough correlation
information to connect the error with the originating request or message.

## Severity

MEDIUM

Only report when correlation tracking is part of the application's
operational model.

---

# LOG-039 — Logging Every DataWeave Transformation

## Rule

Flag unnecessary logging of intermediate DataWeave payloads or variables
when it produces significant log volume or exposes unnecessary data.

## Severity

LOW / MEDIUM

---

# LOG-040 — Logging Inside Error Recovery Loops

## Rule

Flag repeated logging inside retry or recovery loops when the volume can
become excessive.

## Severity

MEDIUM

Coordinate with:

- `references/error-handling.md`
- `references/performance.md`

---

# LOG-041 — Inconsistent Logging Strategy

## Rule

Flag materially inconsistent logging approaches across equivalent flows
when the inconsistency makes production diagnosis difficult.

Examples include:

- different correlation formats
- inconsistent operation identifiers
- inconsistent error context
- materially different log levels

## Severity

LOW

Do not report minor formatting differences.

---

# LOG-042 — Missing Structured Context

## Rule

Flag important production integrations where unstructured logging makes
critical operational information difficult to search or correlate.

Consider:

- correlation ID
- flow name
- operation
- business identifier
- external system
- error type

## Severity

LOW / MEDIUM

Only report when structured or consistent context is clearly required by
the application's operational model.

---

# LOG-043 — Logging Environment-Specific Secrets

## Rule

Flag logging of values resolved from:

- environment variables
- secure property files
- deployment properties
- secret-management systems

when those values contain sensitive information.

## Severity

CRITICAL / HIGH

---

# LOG-044 — Logging Configuration Values With Credentials

## Rule

Flag logging of configuration objects or connection settings that include
credentials or other secrets.

## Severity

CRITICAL / HIGH

---

# LOG-045 — Excessive Logger Calls in Batch Processing

## Rule

Flag per-record logging in large Batch jobs when it can create
substantial operational overhead.

## Severity

MEDIUM

Do not report per-record logging when the batch size is demonstrably small
and the logging is operationally justified.

---

# LOG-046 — Excessive Logger Calls in Message Consumers

## Rule

Flag high-volume message consumers that log multiple messages for every
successful message when the logging provides little operational value.

## Severity

LOW / MEDIUM

---

# LOG-047 — Missing Failure Classification

## Rule

Flag important errors where logs do not distinguish between materially
different failure categories when that distinction is necessary for
operations.

Examples include:

- validation failure
- authentication failure
- authorization failure
- downstream timeout
- database failure
- retry exhaustion

## Severity

LOW / MEDIUM

---

# LOG-048 — Misleading Retry Logging

## Rule

Flag retry logging that incorrectly indicates:

- retry occurred when it did not
- retry succeeded when it did not
- all retries were exhausted when they were not

## Severity

MEDIUM

---

# LOG-049 — Missing Dead-Letter Context

## Rule

For messaging flows using dead-letter or poison-message handling, flag
logs that do not provide enough information to diagnose why a message was
dead-lettered.

## Severity

MEDIUM

Coordinate with:

- `references/messaging.md`

---

# LOG-050 — Logging Business Data Without Operational Need

## Rule

Flag unnecessary logging of business data where a smaller identifier or
summary would provide equivalent diagnostic value.

## Severity

LOW / MEDIUM

---

# Logging False-Positive Controls

Do not report:

- every logger statement as excessive
- every payload logger as a security issue without evidence of sensitive
  content
- correlation IDs as secrets automatically
- DEBUG logging merely because DEBUG exists
- stack traces that are necessary for diagnosing failures
- detailed logs in intentionally diagnostic flows without evidence of
  production impact
- integration tests that intentionally log diagnostic information
- structured logging merely because the application uses plain text logs
- different log message wording when operational meaning is equivalent
- every missing log message as a defect
- required operational context as "excessive logging"
- business identifiers as PII without evidence
- duplicate logs when each layer provides materially different context

---

# Logging Finding Quality Gate

Before reporting a logging finding:

1. Identify the logger.
2. Inspect the expression being logged.
3. Inspect the surrounding flow.
4. Determine whether the value can contain sensitive information.
5. Determine expected execution frequency.
6. Determine whether the log is production-facing.
7. Check error handling.
8. Check correlation behavior.
9. Check whether another layer already logs the information.
10. Determine operational impact.
11. Confirm severity.
12. Identify exact file and location.
13. Provide actionable remediation.

If the issue cannot be substantiated, do not report it.

---

# Logging Finding Format

Use the following structure for every logging finding.

**Finding ID:** LOG-001

**Severity:** HIGH

**Category:** LOGGING

**File:** `src/main/mule/example.xml:123`

**Location:** Logger / Error Handler / Configuration

**Problem:**

Describe the logging problem.

**Evidence:**

Identify the exact logger expression, configuration, or processing path.

**Impact:**

Explain the realistic security, operational, performance, privacy, or
diagnostic impact.

**Recommendation:**

Provide an actionable remediation approach.

**Confidence:** HIGH / MEDIUM / LOW