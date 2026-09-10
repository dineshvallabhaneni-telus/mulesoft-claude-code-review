# Mule Architecture Review Rules

## Purpose

Review Mule application architecture for:

* maintainability
* coupling
* reliability
* scalability
* testability
* operational behavior
* separation of responsibilities
* failure isolation

Architecture findings must be based on actual application behavior and repository evidence.

Architectural preferences alone are not findings.

---

# Review Areas

Inspect, where applicable:

* flow boundaries
* private flows
* subflows
* flow references
* reusable components
* orchestration
* synchronous dependencies
* asynchronous processing
* side effects
* transaction boundaries
* coupling
* duplicated logic
* abstraction boundaries
* error boundaries
* failure isolation
* testability
* shared components
* configuration dependencies
* downstream dependencies

Review architecture across related files rather than evaluating individual flows in isolation.

---

# Architectural Analysis Principles

Before reporting an architecture finding:

1. Identify the affected component or flow.
2. Trace its important flow references and dependencies.
3. Inspect related global configuration.
4. Identify downstream systems and side effects.
5. Determine transaction and error boundaries.
6. Determine whether the design creates an actual production consequence.
7. Check for existing controls or compensating mechanisms.
8. Assess whether the concern is architectural or merely stylistic.
9. Assign severity and confidence based on evidence.

Do not report an architectural concern solely because another design would be cleaner.

Do not infer architectural requirements that are not supported by repository evidence.

---

# ARCH-001 — Excessive Flow Complexity

## Description

A flow has excessive structural or behavioral complexity that creates a meaningful risk to:

* correctness
* maintainability
* testing
* error handling
* operational support
* change safety

Complexity may result from combinations of:

* deeply nested scopes
* excessive branching
* multiple responsibilities
* repeated transformations
* intertwined error paths
* numerous side effects
* difficult-to-follow orchestration
* excessive conditional behavior
* tightly coupled processing stages

## Finding Gate

Do not report this finding solely because:

* a flow is long
* a flow contains many processors
* a flow contains many branches
* the implementation could be refactored

There must be evidence that the complexity creates a meaningful technical or production risk.

## Evidence Requirements

Identify:

* affected flow
* relevant processors/scopes
* branching or nesting structure
* responsibilities handled by the flow
* related error handling
* relevant downstream interactions
* evidence of the resulting risk

## Impact Examples

Potential impacts include:

* difficult defect isolation
* inadequate testability
* increased regression risk
* incorrect error handling
* difficult operational troubleshooting
* unsafe changes

The impact must be demonstrated or strongly supported by repository evidence.

---

# ARCH-002 — Duplicated Business Logic

## Description

The same meaningful business behavior is implemented independently in multiple locations, creating a material risk of behavioral divergence.

Examples may include repeated:

* business rules
* transformation logic
* validation logic
* routing decisions
* enrichment behavior
* calculation logic

## Finding Gate

Do not report duplication merely because:

* two processors look similar
* two flows contain similar XML
* common Mule constructs are repeated

The duplicated behavior must represent meaningful logic where divergence can create a production or maintenance consequence.

## Evidence Requirements

Identify:

* affected flows/components
* duplicated logic
* relevant processors or DataWeave
* similarities demonstrating the duplication
* evidence that the implementations can diverge
* actual or likely impact

## Impact Examples

Potential impacts include:

* inconsistent business behavior
* inconsistent validation
* inconsistent data transformation
* defects being fixed in one location but not another
* increased regression risk

---

# ARCH-003 — Tight Coupling Creating Meaningful Production Risk

## Description

Components are coupled in a way that creates a material production risk involving:

* reliability
* deployability
* failure isolation
* scalability
* change safety
* operational recovery

Examples may include:

* unnecessary dependency on a synchronous downstream system
* shared components that create broad failure propagation
* tightly coupled configuration boundaries
* architectural dependencies that prevent independent failure handling
* orchestration that causes unrelated operations to fail together

## Finding Gate

Do not report coupling merely because components interact.

Mule applications inherently contain dependencies.

The finding requires evidence that the coupling creates a meaningful production consequence.

## Evidence Requirements

Identify:

* coupled components
* dependency relationship
* relevant flow/configuration
* downstream behavior
* failure propagation
* operational consequence

## Impact Examples

Potential impacts include:

* cascading failures
* broad blast radius
* inability to isolate failures
* reduced scalability
* difficult recovery
* unsafe deployments
* unnecessary availability dependencies

---

# ARCH-004 — Incorrect Abstraction Creating Behavioral Risk

## Description

An abstraction, shared component, reusable subflow, private flow, or flow-reference boundary is inappropriate for the behavior being implemented and creates a material risk.

Examples may include:

* shared logic containing context-specific behavior
* abstraction hiding important error semantics
* inappropriate reuse across incompatible execution paths
* shared state or configuration producing unintended behavior
* abstraction that causes side effects to occur unexpectedly
* reuse that prevents correct transaction or error boundaries

## Finding Gate

Do not report an abstraction simply because it is:

* unconventional
* verbose
* not optimally reusable
* different from a preferred architecture

The abstraction must create a demonstrable or strongly supported behavioral risk.

## Evidence Requirements

Identify:

* abstraction/component
* callers or consumers
* shared behavior
* relevant configuration
* transaction/error context where applicable
* behavioral consequence

## Impact Examples

Potential impacts include:

* incorrect processing
* unintended side effects
* inconsistent error handling
* transaction boundary violations
* unexpected behavior between callers
* difficult-to-diagnose production failures

---

# ARCH-005 — Synchronous Dependency Creating Meaningful Reliability Risk

## Description

A synchronous dependency on another component or external system creates a material reliability or availability risk.

Examples may include:

* request flow blocked by a downstream service
* synchronous orchestration across multiple external systems
* long-running synchronous operations
* critical processing dependent on immediate downstream availability
* synchronous dependency without adequate timeout/failure handling

## Finding Gate

Synchronous processing is not inherently defective.

Do not report this finding merely because a flow uses:

* HTTP Request
* Database operations
* synchronous connectors
* flow references

The finding requires evidence that the synchronous dependency creates a meaningful reliability risk.

## Evidence Requirements

Identify:

* affected flow
* synchronous processor
* downstream dependency
* timeout configuration where available
* retry/reconnection behavior where relevant
* error handling
* transaction context where relevant
* evidence of the resulting reliability risk

## Impact Examples

Potential impacts include:

* request latency amplification
* cascading failures
* unavailable downstream systems causing upstream failure
* thread/resource exhaustion
* reduced throughput
* prolonged recovery
* failure propagation across integration boundaries

---

# Architecture Severity Guidance

Architecture findings should be severity-rated according to demonstrated production impact.

### CRITICAL

Use only when architectural behavior can plausibly cause catastrophic consequences such as significant data loss, severe security exposure, or widespread system failure.

### HIGH

Use when architecture creates substantial production risk, such as:

* major failure propagation
* significant data integrity risk
* severe availability impact
* critical processing dependency with inadequate resilience

### MEDIUM

Use when architecture creates meaningful but contained production or operational risk.

### LOW

Use for limited production impact or lower-priority architectural weaknesses.

### NIT

Use only for optional improvements that do not represent material production risk.

Architecture quality alone does not determine severity.

---

# Evidence Quality

Prefer evidence that demonstrates actual relationships and behavior, including:

* flow definitions
* flow references
* processor sequences
* global configurations
* connector configuration
* transaction boundaries
* error handlers
* DataWeave modules
* repeated implementations
* MUnit relationships
* deployment configuration

Where possible, connect the architectural issue to a realistic execution or failure scenario.

---

# False-Positive Controls

Do not create an architecture finding when:

* the concern is purely stylistic
* the flow is long but understandable and appropriately structured
* duplication is trivial and non-business-critical
* components are coupled in an intentional and reasonable way
* synchronous processing is appropriate for the API contract
* a reusable abstraction is unusual but behaviorally correct
* an apparent risk is already mitigated elsewhere
* evidence is insufficient to establish production impact

When evidence is insufficient, do not manufacture a finding.

---

# Positive Architecture Indicators

Where supported by evidence, recognize strengths such as:

* clear flow boundaries
* appropriate separation of responsibilities
* effective reuse
* well-defined error boundaries
* appropriate synchronous/asynchronous design
* sensible transaction boundaries
* limited failure blast radius
* testable orchestration
* appropriate abstraction
* clear integration boundaries

Positive observations must remain evidence-based.

---

# Required Finding Fields

Any architecture finding must include:

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

Evidence excerpts must be faithful to the repository and must not expose secrets.