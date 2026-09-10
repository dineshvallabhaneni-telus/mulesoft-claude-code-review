# Mule XML Review Rules

## Purpose

Review Mule 4 XML configuration and flow definitions for correctness,
runtime behavior, maintainability, configuration consistency, and
production risk.

The review must account for Mule XML semantics and cross-file
relationships.

XML findings must be based on actual repository evidence.

XML style preferences alone are not findings.

---

# Review Areas

Inspect, where applicable:

* processor ordering
* global configuration
* flow references
* private flows
* subflows
* scopes
* routing
* variables
* payload manipulation
* attributes
* error handlers
* configuration reuse
* configuration duplication
* hardcoded values
* environment-specific values
* deprecated configuration
* unused configuration
* contradictory configuration
* flow-level configuration
* connector configuration
* listener configuration
* request configuration
* transaction configuration
* retry/reconnection configuration

Review related XML files and referenced configuration together.

Do not evaluate an XML element in isolation when its behavior depends
on another flow, global configuration, property, or referenced component.

---

# XML Review Principles

Before reporting an XML finding:

1. Identify the affected XML element or flow.
2. Inspect surrounding processors.
3. Trace relevant flow references.
4. Inspect referenced global configuration.
5. Inspect related properties and configuration files.
6. Determine actual Mule runtime behavior.
7. Check for environment-specific overrides.
8. Check whether another configuration or component mitigates the issue.
9. Determine actual production impact.
10. Assign severity and confidence based on evidence.

Do not report a finding merely because a configuration could be
implemented differently.

---

# XML-001 — Incorrect Processor Ordering

## Description

Processors are ordered in a way that creates incorrect or unintended
runtime behavior.

Potential examples include:

* transformation occurring after a processor that requires the transformed payload
* variables being initialized after their first required use
* payload mutation occurring before a processor that depends on the original payload
* validation occurring after an irreversible side effect
* acknowledgement or completion behavior occurring before required processing
* error-sensitive operations being placed outside the intended error boundary

## Finding Gate

Processor ordering is only a finding when the ordering causes or can
reasonably cause incorrect behavior.

Do not report ordering solely because another sequence appears cleaner.

## Evidence Requirements

Identify:

* affected flow
* processors involved
* their execution order
* payload/attribute/variable state where relevant
* downstream processor dependency
* actual or strongly supported runtime consequence

## Impact Examples

Potential impacts include:

* incorrect data processing
* failed requests
* invalid downstream calls
* lost or incomplete processing
* unintended side effects
* inconsistent behavior

---

# XML-002 — Unsafe or Inconsistent Global Configuration

## Description

A global Mule configuration creates a material production risk or is
inconsistent with the behavior required by its consumers.

Potential areas include:

* HTTP listener configuration
* HTTP request configuration
* TLS configuration
* connection providers
* database configuration
* messaging configuration
* transaction configuration
* retry/reconnection configuration
* timeouts
* response/error behavior
* shared connector configuration

## Finding Gate

Do not report configuration differences merely because multiple
configurations exist.

The configuration must create a meaningful behavioral,
reliability, security, or operational risk.

## Evidence Requirements

Identify:

* global configuration
* affected consumers
* relevant attributes
* related properties
* actual configuration interaction
* resulting runtime behavior
* production impact

## Impact Examples

Potential impacts include:

* insecure communication
* inconsistent runtime behavior
* unavailable downstream systems causing failures
* excessive timeout duration
* inappropriate retry behavior
* connection instability
* inconsistent API behavior

---

# XML-003 — Hardcoded Environment-Specific Configuration

## Description

Environment-specific configuration is embedded directly in Mule XML
in a way that creates a meaningful deployment, security, or operational
risk.

Potential examples include hardcoded:

* hostnames
* ports
* URLs
* environment identifiers
* queue/topic names
* database endpoints
* file paths
* tenant identifiers
* operational thresholds

## Finding Gate

Not every literal value is a finding.

Do not report:

* static constants
* legitimate protocol values
* harmless application constants
* values intentionally fixed by design

A finding requires evidence that the value is environment-specific
and that hardcoding it creates a meaningful risk.

Secrets must be handled under the security review rules and must never
be printed.

## Evidence Requirements

Identify:

* affected XML element
* hardcoded value, sanitized where necessary
* expected configuration mechanism where evidenced
* deployment/environment relationship
* actual production consequence

## Impact Examples

Potential impacts include:

* deployment failure between environments
* accidental connection to the wrong system
* environment-specific behavior being deployed incorrectly
* difficult operational changes
* configuration drift

---

# XML-004 — Unused or Contradictory Configuration

## Description

Mule configuration contains elements that are demonstrably unused,
contradictory, or inconsistent with the application's actual behavior
and that create a meaningful operational or maintenance risk.

Potential examples include:

* global configuration with no consumers
* properties that conflict with active configuration
* duplicate settings with different effective values
* configuration that is overridden unexpectedly
* stale configuration affecting deployment behavior
* contradictory listener/request settings

## Finding Gate

Do not report unused configuration solely because no reference was
found in one file.

Before reporting:

1. Search the complete repository for references.
2. Inspect indirect references.
3. Inspect property substitution.
4. Inspect flow references and global references.
5. Consider framework/plugin behavior where relevant.
6. Determine whether the configuration is actually inactive.
7. Determine whether its presence creates a meaningful risk.

Unused configuration without a material consequence may be recorded as
a maintainability observation rather than a finding.

## Evidence Requirements

Identify:

* configuration element
* all relevant references searched
* conflicting or unused relationship
* related configuration
* actual or likely operational consequence

## Impact Examples

Potential impacts include:

* configuration drift
* deployment confusion
* incorrect assumptions during operations
* accidental future activation
* inconsistent runtime behavior
* maintenance errors

---

# XML-005 — Flow Configuration Creating Runtime Risk

## Description

Flow-level Mule XML configuration creates a material runtime,
reliability, performance, or operational risk that is not better
classified by another XML finding.

Potential areas include:

* listener behavior
* request configuration
* timeout configuration
* reconnection
* retry behavior
* transaction settings
* streaming configuration
* concurrency-related configuration
* scheduler configuration
* batch configuration
* acknowledgement behavior
* error handling configuration

## Finding Gate

Use this finding only when:

* the configuration has a meaningful runtime consequence, and
* the issue does not more appropriately belong to a specialized domain
  such as security, messaging, database, performance, or error handling.

Do not use XML-005 as a generic catch-all for configuration concerns.

## Evidence Requirements

Identify:

* affected flow
* exact configuration
* related global configuration
* relevant downstream behavior
* runtime consequence
* production impact

## Impact Examples

Potential impacts include:

* request failures
* resource exhaustion
* unexpected retries
* duplicate processing
* transaction failures
* timeout-related outages
* reduced throughput
* scheduler or batch execution problems

---

# Processor and Runtime Semantics

When evaluating Mule XML, consider:

* execution order
* payload changes
* attributes
* variables
* scopes
* error propagation
* flow references
* subflows
* transactions
* streaming
* asynchronous execution
* connector behavior
* retry/reconnection behavior
* acknowledgement behavior

Do not claim runtime behavior unless supported by Mule semantics and
the repository configuration.

---

# Cross-File Evidence

XML analysis must consider relationships across:

* Mule XML files
* global configuration
* properties files
* secure properties configuration
* DataWeave
* API specifications
* connector configuration
* MUnit tests
* Maven dependencies
* deployment configuration

A finding must not be created from an incomplete single-file view when
the relevant behavior is defined elsewhere.

---

# Severity Guidance

Rate XML findings according to demonstrated production impact.

### CRITICAL

Use only for catastrophic consequences such as:

* severe security exposure
* likely widespread data loss
* catastrophic runtime failure

### HIGH

Use for substantial risks such as:

* major production outage
* significant data corruption/loss
* severe transaction/retry behavior
* serious environment misconfiguration
* major runtime failure

### MEDIUM

Use for meaningful but contained:

* functional defects
* reliability issues
* configuration problems
* operational risks

### LOW

Use for limited production or operational impact.

### NIT

Use only for optional improvements with no material production risk.

Do not increase severity merely because the XML appears complex.

---

# False-Positive Controls

Do not create an XML finding when:

* the concern is purely stylistic
* the configuration is valid and intentional
* a hardcoded value is a legitimate constant
* a global configuration is referenced indirectly
* apparent duplication is intentional and harmless
* an unused element has no meaningful consequence
* another component already mitigates the concern
* the runtime behavior cannot be established
* evidence is incomplete

When evidence is insufficient:

**Do not report the finding.**

---

# Positive XML Indicators

Where supported by repository evidence, recognize strengths such as:

* clear processor sequencing
* appropriate use of flow references
* centralized reusable configuration
* environment-specific values externalized
* consistent connector configuration
* explicit timeout/reconnection settings
* appropriate transaction configuration
* clean separation of global and flow-level configuration
* minimal configuration duplication
* understandable flow structure

Positive observations must be evidence-backed.

---

# Required Finding Fields

Any XML finding must include:

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

Evidence excerpts must be faithful to repository content and must not
expose secrets, credentials, tokens, private keys, or secure property
values.