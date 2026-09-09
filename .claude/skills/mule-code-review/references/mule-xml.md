# Mule XML Review Rules

## Purpose

These rules define how Mule 4 XML configuration and flow definitions must
be reviewed.

The objective is to identify Mule XML issues that can affect:

- runtime correctness
- processor execution order
- error handling
- transaction behavior
- message processing
- configuration correctness
- maintainability
- performance
- reliability
- deployment behavior
- testability

Only report issues supported by repository evidence.

Do not report XML style preferences unless they create meaningful technical
or operational impact.

---

# XML-001 — Invalid Configuration

## Rule

Flag Mule XML configuration that is invalid, malformed, unsupported, or
likely to fail application validation or startup.

Consider:

- invalid Mule namespaces
- invalid processor configuration
- invalid attributes
- invalid element nesting
- unsupported configuration
- incompatible connector configuration

## Severity

HIGH

Escalate to CRITICAL only when the invalid configuration prevents the
application from starting or causes catastrophic production impact.

---

# XML-002 — Incorrect Processor Ordering

## Rule

Flag processors whose ordering changes or breaks intended behavior.

Consider ordering of:

- validation
- variable assignment
- transformations
- logging
- connector calls
- error handling
- transactions
- acknowledgements
- routing
- response construction

## Severity

HIGH

---

# XML-003 — Unused Variables

## Rule

Flag variables introduced without a meaningful use when repository
evidence confirms they are unnecessary.

Consider:

- `set-variable`
- `set-payload`
- variables created in scopes
- variables overwritten before use

## Severity

LOW

Escalate when unnecessary variables cause incorrect behavior or excessive
memory usage.

---

# XML-004 — Unused Configuration

## Rule

Flag global configurations that are demonstrably no longer referenced.

Examples include:

- HTTP listener configurations
- HTTP request configurations
- database configurations
- connector configurations
- object store configurations

## Severity

LOW

Do not report configurations whose usage is resolved indirectly unless
repository evidence confirms they are unused.

---

# XML-005 — Duplicate Configuration

## Rule

Flag duplicate global connector or configuration definitions when they
provide the same purpose and create unnecessary configuration complexity.

## Severity

LOW

Escalate when duplicate configurations can cause inconsistent runtime
behavior.

Coordinate with:

- `references/connectors.md`

---

# XML-006 — Hardcoded Environment Value

## Rule

Flag environment-specific values embedded directly in Mule XML.

Examples include:

- URLs
- hostnames
- ports
- database names
- usernames
- credentials
- environment identifiers
- queue names
- bucket names
- organization identifiers

## Severity

MEDIUM

Escalate to HIGH or CRITICAL when the hardcoded value contains a secret.

Coordinate with:

- `references/security.md`
- `references/configuration.md`

---

# XML-007 — Deprecated Configuration

## Rule

Flag deprecated or incompatible Mule or connector configuration when the
repository's actual Mule runtime and connector versions make the issue
relevant.

## Severity

MEDIUM

Do not flag deprecated functionality merely because a newer alternative
exists.

Verify applicability to the project's actual versions.

---

# XML-008 — Configuration Inconsistency

## Rule

Flag configuration that conflicts with established project conventions
without a documented or technically justified reason.

Examples include:

- inconsistent timeout strategy
- inconsistent error configuration
- inconsistent listener configuration
- inconsistent connection settings

## Severity

LOW

Escalate when the inconsistency creates a meaningful production risk.

---

# XML-009 — Incorrect Flow Reference

## Rule

Flag incorrect or unsafe use of:

- `flow-ref`
- subflows
- private flows
- referenced flows

Consider:

- incorrect target flow
- unexpected variable behavior
- unexpected payload changes
- hidden side effects
- error propagation

## Severity

HIGH

---

# XML-010 — Incorrect Subflow Usage

## Rule

Flag subflows when their behavior requires characteristics that make a
regular flow more appropriate.

Examples include requirements for:

- independent error handling
- separate transaction boundaries
- independent processing lifecycle

## Severity

MEDIUM

Coordinate with:

- `references/mule-architecture.md`
- `references/error-handling.md`

---

# XML-011 — Incorrect Scope Usage

## Rule

Flag inappropriate use of scopes such as:

- `try`
- `choice`
- `scatter-gather`
- `foreach`
- `parallel-foreach`
- `until-successful`
- `async`
- `transactional`
- batch scopes

when the scope changes behavior in an unintended way.

## Severity

HIGH

---

# XML-012 — Incorrect Variable Scope

## Rule

Flag variable usage that relies on incorrect assumptions about variable
availability or propagation.

Consider:

- flow scope
- subflow invocation
- flow references
- routing scopes
- error handlers
- asynchronous processing

## Severity

HIGH

---

# XML-013 — Unexpected Payload Mutation

## Rule

Flag processors that unexpectedly modify the payload when downstream
processors depend on the original payload.

Consider:

- transformations
- connector operations
- `set-payload`
- flow references
- subflows

## Severity

HIGH

---

# XML-014 — Unexpected Attribute Mutation

## Rule

Flag processors that unexpectedly replace or modify message attributes
when downstream logic depends on them.

## Severity

MEDIUM / HIGH

---

# XML-015 — Incorrect Choice Routing

## Rule

Flag `choice` routing conditions that can:

- select the wrong branch
- make a branch unreachable
- overlap unexpectedly
- omit a required scenario

## Severity

HIGH

---

# XML-016 — Missing Default Routing

## Rule

Flag routing logic where an unexpected input can result in no meaningful
processing when a default or explicit failure path is required.

## Severity

MEDIUM

Do not require a default branch when the absence of a match is an
intentional and valid business behavior.

---

# XML-017 — Unreachable Processor

## Rule

Flag processors that cannot execute because of:

- unconditional routing
- earlier termination
- error propagation
- impossible conditions
- flow structure

## Severity

MEDIUM

---

# XML-018 — Incorrect Error Handler Placement

## Rule

Flag error handlers configured at an incorrect scope or location such
that expected errors are not handled as intended.

Consider:

- flow-level error handlers
- `try` scopes
- referenced flows
- subflows
- connector operations

## Severity

HIGH

Coordinate with:

- `references/error-handling.md`

---

# XML-019 — Broad Error Handling

## Rule

Flag XML configurations that catch broad errors without sufficient
justification or specific handling.

Examples include:

- `ANY`
- overly broad error handlers
- generic exception handling

## Severity

MEDIUM

Coordinate with:

- `references/error-handling.md`

---

# XML-020 — Incorrect on-error-continue Usage

## Rule

Flag `on-error-continue` when continuing execution can create:

- false success
- message loss
- inconsistent state
- incorrect API responses
- duplicate processing

## Severity

HIGH

---

# XML-021 — Incorrect on-error-propagate Usage

## Rule

Flag `on-error-propagate` when propagation causes an incorrect business
or API outcome.

## Severity

HIGH

---

# XML-022 — Incorrect Try Scope Usage

## Rule

Flag `try` scopes that create incorrect:

- error boundaries
- transaction boundaries
- retry behavior
- variable behavior
- payload handling

## Severity

HIGH

---

# XML-023 — Unsafe Retry Scope

## Rule

Flag XML retry configuration that can cause:

- duplicate business operations
- downstream overload
- message duplication
- transaction inconsistency

Consider:

- `until-successful`
- connector retry configuration
- reconnection
- message redelivery

## Severity

HIGH

Coordinate with:

- `references/error-handling.md`
- `references/messaging.md`
- `references/connectors.md`

---

# XML-024 — Incorrect Transaction Configuration

## Rule

Flag transaction configuration that creates incorrect commit or rollback
behavior.

Consider:

- transactional scopes
- database operations
- messaging acknowledgement
- connector transactions
- error propagation

## Severity

HIGH

---

# XML-025 — Incorrect Flow Transaction Boundary

## Rule

Flag transaction boundaries that include operations that should not be
part of the same transaction or exclude operations that require atomicity.

## Severity

HIGH

---

# XML-026 — Unnecessary Sequential Processing

## Rule

Flag sequential processing when independent operations are unnecessarily
serialized and there is a demonstrated performance or throughput impact.

## Severity

LOW / MEDIUM

Do not recommend parallelization merely because it is technically
possible.

---

# XML-027 — Unsafe Parallel Processing

## Rule

Flag parallel processing when concurrent execution can cause:

- race conditions
- duplicate updates
- ordering problems
- shared-state corruption
- downstream overload

## Severity

HIGH

---

# XML-028 — Incorrect Foreach Usage

## Rule

Flag `foreach` usage that can cause:

- incorrect payload assumptions
- lost original payload
- excessive memory usage
- incorrect aggregation
- unexpected variable behavior

## Severity

MEDIUM / HIGH

---

# XML-029 — Incorrect Parallel Foreach Usage

## Rule

Flag `parallel-foreach` when concurrent processing can produce incorrect
business behavior or unsafe external-system interaction.

## Severity

HIGH

---

# XML-030 — Incorrect Scatter-Gather Usage

## Rule

Flag `scatter-gather` when:

- routes have unsafe side effects
- partial failures are mishandled
- aggregation is incorrect
- response ordering is incorrectly assumed
- downstream systems cannot safely handle concurrent requests

## Severity

HIGH

---

# XML-031 — Incorrect Async Scope Usage

## Rule

Flag `async` processing when the application incorrectly assumes that:

- processing completes before the parent flow
- errors propagate synchronously
- variables remain available
- transaction context is preserved

## Severity

HIGH

---

# XML-032 — Incorrect Until-Successful Usage

## Rule

Flag `until-successful` when retry behavior can cause:

- duplicate side effects
- excessive downstream calls
- delayed failure detection
- incorrect business outcomes

## Severity

HIGH

---

# XML-033 — Missing Timeout Configuration

## Rule

Flag external operations without an appropriate timeout strategy when
the operation can block processing indefinitely or for an unacceptable
duration.

Consider:

- HTTP
- database
- messaging
- Salesforce
- SFTP
- external APIs

## Severity

MEDIUM

Coordinate with:

- `references/connectors.md`
- `references/api.md`

---

# XML-034 — Incorrect Timeout Configuration

## Rule

Flag timeout values that are demonstrably inconsistent with the
integration's expected behavior and can cause:

- premature failures
- excessive blocking
- resource exhaustion

## Severity

MEDIUM

Do not flag timeout values merely because another value could be chosen.

---

# XML-035 — Missing Reconnection Strategy

## Rule

Flag connector configurations without appropriate reconnection behavior
when transient connection failures are realistically expected.

## Severity

MEDIUM

Only report when the integration's failure model warrants it.

Coordinate with:

- `references/connectors.md`

---

# XML-036 — Incorrect Reconnection Strategy

## Rule

Flag reconnection configuration that can cause:

- excessive connection attempts
- delayed failure detection
- downstream overload
- prolonged resource consumption

## Severity

MEDIUM / HIGH

---

# XML-037 — Hardcoded Expression Logic

## Rule

Flag large or complex business logic embedded directly inside Mule XML
expressions when it materially reduces readability or maintainability.

## Severity

LOW / MEDIUM

Do not report simple expressions merely because they are inline.

---

# XML-038 — Complex Expression in XML

## Rule

Flag overly complex expressions in attributes or processors when moving
the logic to an appropriate DataWeave module or reusable component would
materially improve correctness or testability.

## Severity

LOW

Coordinate with:

- `references/dataweave.md`

---

# XML-039 — Duplicate Flow Logic

## Rule

Flag substantially duplicated processing logic across Mule XML flows.

## Severity

MEDIUM

Do not flag intentionally similar flows when their behavior is materially
different.

Coordinate with:

- `references/mule-architecture.md`

---

# XML-040 — God Flow

## Rule

Flag flows that combine multiple unrelated business responsibilities
and become difficult to:

- understand
- test
- troubleshoot
- maintain

## Severity

MEDIUM

Coordinate with:

- `references/mule-architecture.md`

---

# XML-041 — Excessive Flow Nesting

## Rule

Flag deeply nested scopes, routers, error handlers, or processors when
the nesting materially reduces readability or makes behavior difficult to
reason about.

## Severity

MEDIUM

---

# XML-042 — Excessive Flow Complexity

## Rule

Flag flows with excessive:

- branching
- nested scopes
- transformations
- external calls
- error paths
- responsibilities

when complexity creates meaningful correctness or maintainability risk.

## Severity

MEDIUM

---

# XML-043 — Hidden Side Effect

## Rule

Flag reusable flows or subflows that unexpectedly:

- modify payload
- modify variables
- modify attributes
- update external systems
- publish messages
- change state

when callers are likely to assume the component is side-effect free.

## Severity

MEDIUM

---

# XML-044 — Missing Explicit Configuration

## Rule

Flag important behavior that depends on implicit defaults when explicit
configuration is necessary to make production behavior predictable.

Examples may include:

- timeouts
- retry behavior
- acknowledgement behavior
- transaction behavior

## Severity

LOW / MEDIUM

Do not report every default configuration as a defect.

---

# XML-045 — Incorrect Listener Configuration

## Rule

Flag HTTP listener configuration that can cause:

- incorrect routing
- incorrect protocol behavior
- insecure exposure
- unexpected port binding
- incorrect response behavior

## Severity

HIGH

Coordinate with:

- `references/api.md`
- `references/security.md`

---

# XML-046 — Incorrect Request Configuration

## Rule

Flag HTTP request configuration that can cause:

- incorrect target URL
- incorrect method
- incorrect headers
- incorrect response handling
- unsafe timeout/retry behavior

## Severity

HIGH

---

# XML-047 — Incorrect Response Configuration

## Rule

Flag response configuration that produces:

- incorrect status codes
- incorrect headers
- incorrect content types
- incorrect payloads
- inconsistent API behavior

## Severity

HIGH

---

# XML-048 — Incorrect Routing Expression

## Rule

Flag routing expressions that can:

- select incorrect paths
- fail for null values
- fail for unexpected types
- produce unreachable branches

## Severity

HIGH

Coordinate with:

- `references/dataweave.md`

---

# XML-049 — Missing Validation Processor

## Rule

Flag missing validation when repository evidence demonstrates that
invalid input can reach business processing and cause an incorrect or
unsafe outcome.

## Severity

MEDIUM

Do not require validation when validation is already enforced by:

- API specification
- connector
- DataWeave
- downstream service
- existing application logic

---

# XML-050 — Incorrect Validation Placement

## Rule

Flag validation that occurs after processing that should have been
protected by the validation.

## Severity

MEDIUM / HIGH

---

# XML-051 — Unnecessary Payload Transformation

## Rule

Flag XML processors that transform payloads unnecessarily and create
additional processing or memory overhead.

## Severity

LOW / MEDIUM

Coordinate with:

- `references/dataweave.md`
- `references/performance.md`

---

# XML-052 — Excessive Payload Copying

## Rule

Flag repeated payload assignments or transformations that unnecessarily
materialize large payloads.

## Severity

MEDIUM

---

# XML-053 — Streaming Disruption

## Rule

Flag Mule XML configuration that unnecessarily converts or materializes
a stream when large-payload processing depends on streaming.

## Severity

HIGH

Coordinate with:

- `references/dataweave.md`
- `references/performance.md`

---

# XML-054 — Incorrect Object Store Usage

## Rule

Flag Object Store configuration or usage that can cause:

- incorrect persistence assumptions
- duplicate processing
- data loss
- excessive storage
- incorrect expiration behavior

## Severity

HIGH

Coordinate with:

- `references/connectors.md`
- `references/messaging.md`

---

# XML-055 — Incorrect Scheduler Configuration

## Rule

Flag scheduler configuration that can cause:

- unintended execution frequency
- overlapping executions
- duplicate processing
- unexpected timezone behavior

## Severity

MEDIUM / HIGH

---

# XML-056 — Scheduler Timezone Risk

## Rule

Flag scheduled processing where timezone behavior is ambiguous or
incorrect and can affect business execution.

## Severity

MEDIUM

Only report when timezone behavior materially affects processing.

---

# XML-057 — Incorrect Batch Configuration

## Rule

Flag Batch configuration that can cause:

- incorrect record processing
- excessive memory usage
- incorrect aggregation
- retry problems
- duplicate processing
- incomplete failure handling

## Severity

HIGH

Coordinate with:

- `references/performance.md`
- `references/messaging.md`

---

# XML-058 — Batch Error Handling Problem

## Rule

Flag Batch error handling that incorrectly treats failed records or
causes successful records to be lost or incorrectly reprocessed.

## Severity

HIGH

---

# XML-059 — Incorrect Flow Name or Identifier

## Rule

Flag misleading or inconsistent flow identifiers when they materially
affect:

- operational troubleshooting
- monitoring
- error diagnosis
- maintainability

## Severity

LOW

---

# XML-060 — Inconsistent Global Configuration Usage

## Rule

Flag flows that bypass established global configurations without a
documented technical reason.

Examples include:

- creating a new HTTP configuration instead of reusing an existing one
- duplicating database connection settings
- inconsistent connector configuration

## Severity

LOW / MEDIUM

---

# XML-061 — Incorrect Global Configuration Reference

## Rule

Flag references to global configurations that are:

- incorrect
- incompatible
- unintended
- inconsistent with the operation

## Severity

HIGH

---

# XML-062 — Configuration Override Risk

## Rule

Flag local processor configuration that unexpectedly overrides important
global configuration.

Consider:

- timeout
- authentication
- TLS
- retry
- reconnection
- response behavior

## Severity

MEDIUM / HIGH

---

# XML-063 — Missing Error Response Configuration

## Rule

Flag API-facing flows where errors can reach clients without an
appropriate response contract.

## Severity

HIGH

Coordinate with:

- `references/error-handling.md`
- `references/api.md`

---

# XML-064 — Incorrect Transactional Scope

## Rule

Flag transactional scopes that include non-transactional external
operations and create a false assumption of atomicity.

## Severity

HIGH

---

# XML-065 — Incorrect Acknowledgement Ordering

## Rule

Flag message-processing flows where acknowledgement can occur before
business processing has successfully completed.

## Severity

CRITICAL / HIGH

Coordinate with:

- `references/messaging.md`

---

# XML-066 — Message Processing Without Failure Boundary

## Rule

Flag message consumers where failures can cause:

- message loss
- uncontrolled redelivery
- duplicate processing
- poison-message loops

## Severity

HIGH

---

# XML-067 — Incorrect Concurrency Configuration

## Rule

Flag concurrency configuration that can cause:

- race conditions
- resource exhaustion
- downstream overload
- ordering violations
- duplicate processing

## Severity

HIGH

---

# XML-068 — Resource Exhaustion Risk

## Rule

Flag XML configuration that can create unbounded or excessive:

- concurrency
- retries
- queue processing
- collection processing
- external requests

## Severity

HIGH

Coordinate with:

- `references/performance.md`
- `references/messaging.md`

---

# XML-069 — Incorrect Flow Termination

## Rule

Flag flow termination behavior that can produce:

- false success
- incomplete processing
- message loss
- incorrect API responses

## Severity

HIGH

---

# XML-070 — Missing Explicit Failure Path

## Rule

Flag important processing paths where unexpected conditions can result
in no meaningful success or failure outcome.

## Severity

MEDIUM

Only report when the missing failure path can create a realistic
production issue.

---

# XML-071 — Incorrect Component Scope

## Rule

Flag components placed inside or outside a scope when their execution
context materially changes behavior.

Examples include:

- logger inside retry
- connector inside transaction
- acknowledgement inside error handler
- transformation outside required scope

## Severity

MEDIUM / HIGH

---

# XML-072 — Incorrect Error Mapping

## Rule

Flag XML error mappings that convert an error into an incorrect or
misleading application error.

## Severity

HIGH

Coordinate with:

- `references/error-handling.md`

---

# XML-073 — Incorrect Secure Configuration Reference

## Rule

Flag Mule XML that references sensitive configuration incorrectly or
bypasses the project's established secure-property mechanism.

## Severity

HIGH

Coordinate with:

- `references/security.md`

---

# XML-074 — Insecure TLS Configuration

## Rule

Flag Mule XML that disables or weakens TLS security.

Examples include:

- disabled certificate validation
- disabled hostname verification
- insecure trust configuration

## Severity

CRITICAL

Coordinate with:

- `references/security.md`

---

# XML-075 — Plain HTTP for Sensitive Integration

## Rule

Flag use of plain HTTP where the integration handles sensitive data or
requires transport security.

## Severity

HIGH

Coordinate with:

- `references/security.md`

---

# XML-076 — Incorrect API Authentication Configuration

## Rule

Flag HTTP listener or request configuration where authentication is
incorrectly configured, missing, or unintentionally bypassed.

## Severity

HIGH / CRITICAL

Coordinate with:

- `references/api.md`
- `references/security.md`

---

# XML-077 — Incorrect Authorization Configuration

## Rule

Flag protected operations where authorization controls are absent,
misconfigured, or bypassable.

## Severity

HIGH / CRITICAL

Coordinate with:

- `references/api.md`
- `references/security.md`

---

# XML-078 — Hardcoded Credential Reference

## Rule

Flag credentials embedded directly in Mule XML rather than using the
established secure configuration mechanism.

## Severity

CRITICAL

Coordinate with:

- `references/security.md`

---

# XML-079 — Incorrect Expression Language Usage

## Rule

Flag expressions that can fail because of:

- incorrect syntax
- incorrect variable references
- incorrect attribute references
- incorrect type assumptions
- null handling problems

## Severity

HIGH

---

# XML-080 — Expression With Hidden Side Effect

## Rule

Flag expressions or configuration that perform unexpected state changes
or external operations when the surrounding code implies a read-only
operation.

## Severity

MEDIUM

---

# XML-081 — Duplicate Processor

## Rule

Flag duplicate processors where the repeated execution provides no
meaningful behavior and can cause unnecessary:

- external calls
- transformations
- logging
- state changes

## Severity

MEDIUM

---

# XML-082 — Unnecessary External Call

## Rule

Flag XML flows that make an external call that does not contribute to
the required business outcome.

## Severity

MEDIUM / HIGH

---

# XML-083 — External Call Before Validation

## Rule

Flag external calls that occur before required input validation and can
cause unnecessary or unsafe downstream processing.

## Severity

MEDIUM / HIGH

---

# XML-084 — Incorrect Flow Refactoring Boundary

## Rule

Flag flow extraction into a subflow or private flow when the extraction
changes:

- error behavior
- transaction behavior
- variable behavior
- payload behavior
- operational visibility

## Severity

MEDIUM / HIGH

---

# XML-085 — Missing Reusable Flow Boundary

## Rule

Flag substantial repeated processing where a reusable flow or subflow would
materially improve maintainability without creating inappropriate
coupling.

## Severity

LOW / MEDIUM

Do not report duplication when reuse would make the design more complex.

---

# XML-086 — Excessive XML Complexity

## Rule

Flag XML that is technically valid but unnecessarily complex to the point
that it creates meaningful:

- correctness risk
- testing difficulty
- operational difficulty
- maintenance risk

## Severity

MEDIUM

---

# XML-087 — XML Structure Inconsistent With Project Convention

## Rule

Flag materially inconsistent XML organization when it creates meaningful
maintenance or operational risk.

## Severity

LOW

Do not report cosmetic formatting differences.

---

# XML-088 — Missing Documentation for Complex Behavior

## Rule

Flag unusually complex or non-obvious Mule behavior where the absence of
documentation creates meaningful operational or maintenance risk.

## Severity

LOW

Do not require comments for straightforward Mule configuration.

---

# XML-089 — Incorrect Namespace or Module Declaration

## Rule

Flag namespace or module declarations that are:

- invalid
- inconsistent with the actual configuration
- unnecessary and potentially misleading
- incompatible with the project's Mule runtime

## Severity

HIGH / LOW

Use HIGH when runtime validation or behavior is affected.

---

# XML-090 — XML Configuration That Prevents Testing

## Rule

Flag Mule XML structure or configuration that unnecessarily prevents
meaningful MUnit testing.

Examples include:

- excessive hardcoded dependencies
- tightly coupled global state
- unmockable external interactions
- hidden side effects

## Severity

LOW / MEDIUM

Coordinate with:

- `references/munit.md`
- `references/mule-architecture.md`

---

# XML False-Positive Controls

Do not report:

- valid XML formatting differences
- simple inline expressions
- every variable declaration
- every global configuration
- every subflow
- every use of `choice`
- every sequential operation
- every timeout value without evidence of impact
- every deprecated feature without checking runtime relevance
- every duplicate-looking configuration without verifying actual purpose
- every processor that could theoretically be refactored
- every flow that could theoretically be split
- every sequential operation that could theoretically be parallelized
- every `on-error-continue` without examining the business outcome
- every `on-error-propagate` without examining the API/business contract
- every global configuration that is not directly referenced in one file
- stylistic XML preferences without production impact

---

# XML Finding Quality Gate

Before reporting a Mule XML finding:

1. Inspect the complete affected flow.
2. Inspect referenced subflows/private flows.
3. Inspect referenced global configurations.
4. Inspect related DataWeave.
5. Inspect related error handling.
6. Inspect related API contracts.
7. Inspect connector configuration.
8. Determine runtime behavior.
9. Determine realistic impact.
10. Check whether another component already handles the issue.
11. Confirm severity.
12. Identify exact file and location.
13. Provide actionable remediation.

If the issue cannot be substantiated, do not report it.

---

# XML Finding Format

Use the following structure for every Mule XML finding.

**Finding ID:** XML-001

**Severity:** HIGH

**Category:** MULE-XML

**File:** `src/main/mule/example.xml:123`

**Location:** Flow / Processor / Scope / Global Configuration

**Problem:**

Describe the Mule XML problem.

**Evidence:**

Identify the relevant XML configuration or processing sequence.

**Impact:**

Explain the realistic runtime, reliability, security, performance, or
maintainability impact.

**Recommendation:**

Provide an actionable remediation approach.

**Confidence:** HIGH / MEDIUM / LOW