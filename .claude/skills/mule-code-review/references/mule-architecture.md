# MuleSoft Architecture Review Rules

## Purpose

This reference defines architecture-specific rules for reviewing Mule 4
applications.

Use these rules when assessing:

- flow design
- flow responsibilities
- subflows
- private flows
- reusable components
- global configurations
- coupling
- integration boundaries
- synchronous/asynchronous design
- side effects
- testability
- scalability
- maintainability

These rules supplement:

- `CLAUDE.md`
- `skills/mule-code-review/SKILL.md`
- `review.md`
- `finding-taxonomy.md`

---

# Architecture Review Principles

Architecture findings must be based on the actual application.

Do not flag a design simply because another architecture is possible.

Consider:

- business responsibility
- runtime behavior
- error handling
- transaction boundaries
- retry behavior
- external dependencies
- testability
- operational impact
- scalability

Before reporting an architecture finding, inspect related flows,
subflows, private flows, global configurations, and downstream dependencies.

---

# ARCH-001 — Excessive Flow Complexity

## Rule

Flag flows containing excessive:

- branching
- nesting
- transformations
- error-handling branches
- conditional logic
- processor chains
- unrelated responsibilities

when the complexity creates meaningful:

- maintenance risk
- testing difficulty
- functional risk
- operational risk

## Evidence

Look for:

- deeply nested scopes
- many conditional branches
- large processor chains
- multiple unrelated processing stages
- complex embedded DataWeave
- repeated error-handling logic

## Severity

MEDIUM

Escalate only when complexity demonstrably creates significant production
or correctness risk.

## Do Not Flag

Do not flag a long flow merely because it contains many processors.

---

# ARCH-002 — God Flow

## Rule

Flag a flow that performs multiple unrelated business responsibilities
and becomes difficult to understand, test, or change safely.

## Indicators

A flow may:

- receive an API request
- perform unrelated validation
- transform multiple unrelated domains
- update several unrelated systems
- perform unrelated database operations
- publish unrelated messages
- contain unrelated business decisions

## Severity

MEDIUM

## Evidence Required

Identify the distinct responsibilities and explain why their coupling
creates a meaningful risk.

---

# ARCH-003 — Duplicate Business Logic

## Rule

Flag substantially duplicated business logic across flows when
duplication creates:

- inconsistent behavior
- maintenance risk
- defect risk
- configuration drift

## Evidence

Identify:

- affected flows
- duplicated logic
- whether the behavior is actually business logic
- why reuse would materially reduce risk

## Severity

MEDIUM

## Do Not Flag

Do not flag small repeated expressions or legitimate flow-specific logic.

---

# ARCH-004 — Incorrect Abstraction

## Rule

Flag abstractions that increase complexity without providing meaningful
reuse or separation of responsibility.

Examples:

- unnecessary subflows
- excessive indirection
- abstractions used only once without meaningful benefit
- deeply nested reusable components
- abstractions that hide important business behavior

## Severity

LOW

Escalate when abstraction materially increases production risk.

---

# ARCH-005 — Incorrect Use of Subflow

## Rule

Flag use of a subflow when the invoked behavior requires independent:

- error handling
- transaction boundaries
- execution behavior
- lifecycle behavior
- testing isolation

and a flow/private flow would better represent the required behavior.

## Severity

MEDIUM

## Important

Do not report this merely because a private flow could also be used.

Establish why the current execution model creates a real issue.

---

# ARCH-006 — Missing Reusable Configuration

## Rule

Flag repeated connector configuration when an established global
configuration should clearly be reused and duplication creates:

- configuration drift
- inconsistent timeout behavior
- inconsistent authentication
- operational complexity

## Severity

LOW

Escalate if duplicated configuration creates security or reliability risk.

---

# ARCH-007 — Hidden Side Effects

## Rule

Flag reusable components whose side effects are not obvious from their
responsibility and can unexpectedly:

- modify payload
- modify variables
- modify attributes
- modify Object Store state
- write to databases
- publish messages
- call external systems
- change application state

## Severity

MEDIUM

## Evidence

Identify:

- component
- expected responsibility
- hidden side effect
- caller(s)
- resulting risk

---

# ARCH-008 — Tight Coupling

## Rule

Flag unnecessary coupling between unrelated integrations or business
operations when a failure or change in one component can unnecessarily
impact another.

Consider:

- shared state
- shared configuration
- synchronous dependency
- shared database assumptions
- shared error handling
- shared transaction boundaries
- shared business logic

## Severity

MEDIUM

---

# ARCH-009 — Unnecessary Synchronous Dependency

## Rule

Flag synchronous downstream dependencies when the repository provides
evidence that synchronous execution creates avoidable:

- availability coupling
- latency
- timeout propagation
- scalability constraints
- failure propagation

and asynchronous processing would materially reduce the risk.

## Severity

MEDIUM

## Important

Do not automatically recommend asynchronous architecture.

Consider:

- business response requirements
- ordering
- consistency
- transaction requirements
- downstream capabilities
- existing messaging infrastructure

---

# ARCH-010 — Poor Testability

## Rule

Flag designs that make meaningful testing unnecessarily difficult.

Examples:

- excessive hidden side effects
- tightly coupled external calls
- business logic embedded deeply in orchestration
- difficult-to-isolate components
- excessive global state
- logic that cannot reasonably be mocked or verified

## Severity

LOW

Escalate only when poor testability creates meaningful regression or
production risk.

---

# ARCH-011 — Excessive Flow Nesting

## Rule

Flag deeply nested:

- Try scopes
- Choice scopes
- For Each
- Scatter-Gather
- Until Successful
- Batch processing
- error handlers

when nesting materially reduces readability or makes failure behavior
difficult to reason about.

## Severity

MEDIUM

## Review Carefully

Nested scopes are not inherently wrong.

Determine whether nesting creates ambiguity around:

- error propagation
- transaction behavior
- retry
- variable scope
- payload state

---

# ARCH-012 — Mixed Technical and Business Responsibilities

## Rule

Flag flows that combine too many unrelated concerns such as:

- API transport
- authentication logic
- business rules
- database access
- external-system orchestration
- message publishing
- response formatting
- infrastructure concerns

when separation would materially improve:

- correctness
- testability
- maintainability
- change safety

## Severity

MEDIUM

---

# ARCH-013 — Excessive Shared State

## Rule

Flag unnecessary dependence on:

- flow variables
- session-like state
- Object Store
- shared configuration
- global state

when state creates:

- concurrency risk
- ordering assumptions
- difficult debugging
- hidden dependencies
- test isolation problems

## Severity

MEDIUM

---

# ARCH-014 — Unclear Integration Boundary

## Rule

Flag integration boundaries where responsibilities are unclear between:

- API layer
- orchestration layer
- transformation
- business processing
- persistence
- messaging
- external systems

when the unclear boundary creates meaningful:

- coupling
- duplicate logic
- error-handling problems
- testing problems
- ownership problems

## Severity

MEDIUM

---

# ARCH-015 — Excessive Orchestration Coupling

## Rule

Flag orchestration that requires one flow to coordinate too many
independent downstream systems synchronously or sequentially when this
creates significant:

- latency
- availability coupling
- failure propagation
- timeout risk
- operational complexity

## Severity

MEDIUM

Escalate when the orchestration can cause significant production
outages or data inconsistency.

---

# ARCH-016 — Missing Failure Isolation

## Rule

Flag architecture where failure of one downstream integration can
unnecessarily prevent unrelated processing.

Consider:

- sequential calls
- shared error handlers
- shared transactions
- shared queues
- shared state
- synchronous dependency chains

## Severity

HIGH when failure can cause significant message loss, data loss,
cascading failure, or major outage.

Otherwise:

MEDIUM

---

# ARCH-017 — Inappropriate Parallelization

## Rule

Flag parallel execution when the repository demonstrates that parallel
processing can cause:

- race conditions
- ordering violations
- duplicate updates
- transaction problems
- downstream throttling
- inconsistent shared state

## Severity

HIGH when data integrity can be affected.

Otherwise:

MEDIUM

---

# ARCH-018 — Unnecessary Sequential Processing

## Rule

Flag clearly independent operations executed sequentially when the
repository provides evidence that the design causes meaningful:

- latency
- throughput limitations
- timeout risk

## Severity

MEDIUM

## Important

Do not recommend parallelization when operations have:

- ordering requirements
- shared state
- transaction dependencies
- downstream rate limits
- business dependencies

---

# ARCH-019 — Missing Idempotency Boundary

## Rule

Flag integration architecture where an operation can reasonably be
retried or redelivered but there is no identifiable idempotency mechanism
and duplicate business effects are possible.

Consider:

- HTTP retries
- messaging redelivery
- scheduler retries
- Until Successful
- connector reconnection
- batch restart

## Severity

HIGH when duplicate processing can create significant business impact.

Otherwise:

MEDIUM

---

# ARCH-020 — Unclear Transaction Boundary

## Rule

Flag architecture where it is unclear whether related operations must
succeed or fail together and the current implementation can produce
partial business state.

Consider:

- database operations
- message acknowledgement
- external calls
- Object Store updates
- multiple downstream systems

## Severity

HIGH when partial completion can cause significant data inconsistency.

Otherwise:

MEDIUM

---

# ARCH-021 — Excessive External Dependency Chain

## Rule

Flag long synchronous chains of external dependencies when each
dependency adds:

- latency
- failure probability
- timeout risk
- availability coupling

## Severity

MEDIUM

Escalate when the chain creates credible cascading failure or severe
availability risk.

---

# ARCH-022 — Missing Resilience Boundary

## Rule

Flag critical external integrations without appropriate evidence of:

- timeout
- retry where appropriate
- reconnection
- failure handling
- fallback
- dead-letter behavior
- durable recovery

## Severity

MEDIUM

Escalate to HIGH when failure can cause significant message/data loss
or outage.

Do not require every integration to implement every resilience pattern.

---

# ARCH-023 — Unbounded Integration Fan-Out

## Rule

Flag flows that create a large or unbounded number of downstream calls
based on input records or collection size.

Consider:

- For Each
- nested For Each
- database queries
- HTTP requests
- Salesforce operations
- messaging operations

## Severity

MEDIUM

Escalate when the behavior can reasonably exhaust:

- memory
- connection pools
- downstream limits
- API quotas

---

# ARCH-024 — Architecture-Level Duplication

## Rule

Flag repeated architectural patterns that create inconsistent behavior,
such as multiple independent implementations of:

- error mapping
- authentication
- retry policy
- correlation handling
- configuration
- API response handling

## Severity

MEDIUM

Use this rule when duplication exists at an architectural level rather
than simply repeated code.

---

# ARCH-025 — Configuration Coupling

## Rule

Flag architecture that relies on multiple components sharing implicit
configuration assumptions.

Examples:

- one property controlling unrelated flows
- shared timeout with unrelated integrations
- shared credentials across unrelated systems
- environment configuration that cannot be changed independently

## Severity

MEDIUM

Escalate if this creates security or production deployment risk.

---

# ARCH-026 — Inappropriate Reuse

## Rule

Flag reuse that combines components with materially different:

- business semantics
- error behavior
- transaction requirements
- lifecycle
- security requirements

when reuse causes hidden coupling or incorrect behavior.

## Severity

MEDIUM

---

# ARCH-027 — Missing Separation of External System Concerns

## Rule

Flag direct coupling of business orchestration to external-system-specific
details when it materially increases:

- change impact
- test complexity
- duplication
- integration coupling

## Severity

LOW

Escalate when changes to one external system can unexpectedly affect
unrelated business behavior.

---

# ARCH-028 — Architecture Creates Data Integrity Risk

## Rule

Flag architecture where sequencing, concurrency, retries, transactions,
or failure handling can create inconsistent business state.

Examples:

- update A succeeds and update B fails
- message acknowledged before persistence
- external side effect occurs before transaction rollback
- parallel updates race
- retry duplicates a write

## Severity

HIGH

Escalate to CRITICAL when likely impact is severe or widespread.

---

# ARCH-029 — Architecture Creates Message Loss Risk

## Rule

Flag architecture where messages can be:

- acknowledged too early
- dropped on error
- lost during restart
- removed without durable processing
- consumed without recovery

## Severity

HIGH

Escalate to CRITICAL for severe/high-volume data loss scenarios.

---

# ARCH-030 — Architecture Creates Cascading Failure Risk

## Rule

Flag architecture where failure in one external system can propagate
through multiple flows or services and cause widespread failure.

Consider:

- synchronous dependency chains
- retry storms
- shared resources
- shared connection pools
- shared queues
- common error handling
- lack of isolation

## Severity

HIGH

Escalate to CRITICAL only when catastrophic production impact is
credible and strongly evidenced.

---

# Architecture Review Decision Rules

## Do Not Automatically Flag

Do not automatically report:

- long flows
- many processors
- subflows
- private flows
- global configurations
- synchronous HTTP calls
- sequential processing
- reusable components
- shared configuration
- Choice scopes
- Try scopes
- Object Store
- Batch

Each must be evaluated against actual behavior and production impact.

---

# Architecture Finding Validation

Before reporting an architecture finding:

1. Identify the affected component.
2. Identify the architectural pattern.
3. Trace execution.
4. Inspect related components.
5. Determine failure behavior.
6. Determine business impact.
7. Check for existing mitigation.
8. Assign severity.
9. Provide actionable remediation.

---

# Architecture Finding Format

Use:

**Finding ID:** ARCH-001

**Severity:** MEDIUM

**Category:** ARCHITECTURE

**File:** `src/main/mule/order.xml:120-250`

**Component:** `order-processing-flow`

**Problem:**

Describe the architectural problem.

**Evidence:**

Identify the repository evidence.

**Technical Mechanism:**

Explain how the architecture produces the problem.

**Impact:**

Explain realistic production/business impact.

**Recommendation:**

Provide an architecture-level remediation.

**Confidence:** HIGH / MEDIUM / LOW

---

# Final Architecture Assessment

The final report should summarize:

- architecture strengths
- architecture risks
- coupling
- failure isolation
- transaction boundaries
- retry/idempotency
- scalability
- testability
- maintainability

Do not convert every architectural recommendation into a finding.

Distinguish:

- confirmed defect
- production risk
- observation
- strategic recommendation