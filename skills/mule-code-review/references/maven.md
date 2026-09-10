# Maven and Dependency Review Rules

## Purpose

Review MuleSoft Maven configuration and dependencies for:

* Mule runtime compatibility
* Java compatibility
* Mule Maven Plugin compatibility
* connector compatibility
* dependency conflicts
* duplicate dependencies
* unnecessary dependencies
* plugin configuration
* dependency scope
* transitive dependency risks
* version alignment
* build reproducibility
* packaging/deployment compatibility

The objective is to identify dependency or build configuration issues that
create a credible functional, security, reliability, or deployment risk.

Do not recommend upgrades merely because newer versions exist.

---

# Maven Review Principles

Before reporting a Maven finding:

1. Inspect `pom.xml`.
2. Identify Mule runtime version.
3. Identify Java version.
4. Identify Mule Maven Plugin version.
5. Identify Mule connector versions.
6. Inspect direct dependencies.
7. Inspect relevant transitive dependencies where available.
8. Inspect dependency scopes.
9. Inspect plugin configuration.
10. Inspect packaging configuration.
11. Inspect repositories where relevant.
12. Inspect deployment configuration where relevant.
13. Check compatibility relationships.
14. Determine actual or credible production/build impact.
15. Assign severity and confidence based on evidence.

Do not evaluate dependencies solely by age.

---

# MAVEN-001 — Runtime/Plugin Compatibility Concern

## Description

The configured Mule runtime, Java version, Mule Maven Plugin, connector,
or related build component has a compatibility relationship that can
cause build failure, deployment failure, unsupported runtime behavior, or
other meaningful production risk.

Potential areas include:

* incompatible Java/runtime combination
* incompatible Mule Maven Plugin/runtime combination
* connector/runtime incompatibility
* plugin configuration incompatible with packaging/deployment
* runtime version mismatch between build and deployment configuration

## Finding Gate

A finding requires evidence of an actual or strongly supported
compatibility concern.

Use available repository evidence such as:

* `pom.xml`
* Maven plugin configuration
* runtime configuration
* deployment configuration
* explicit version constraints
* dependency metadata
* documented compatibility information available to the review process

Do not report:

> “Version X is old.”

An older version is not automatically a defect.

## Evidence Requirements

Identify:

* affected component
* configured version(s)
* compatibility relationship
* evidence supporting the concern
* build/deployment/runtime impact

---

# MAVEN-002 — Dependency Conflict

## Description

Multiple dependencies introduce incompatible or conflicting versions of
the same library or component, creating a credible risk of:

* runtime linkage failure
* class loading problems
* unexpected behavior
* connector incompatibility
* security-relevant dependency behavior

## Finding Gate

Establish an actual dependency conflict using repository/build evidence.

Useful evidence includes:

* Maven dependency tree
* duplicate/conflicting artifacts
* explicit exclusions
* version overrides
* incompatible transitive dependencies

Do not report two different versions merely because Maven resolves them
through normal dependency management.

A finding should identify why the resolved dependency graph creates a
meaningful risk.

## Evidence Requirements

Identify:

* affected artifact
* conflicting versions
* dependency paths where available
* effective/resolved version where available
* production/build consequence

---

# MAVEN-003 — Duplicate Dependency

## Description

The same dependency is declared redundantly in a way that creates
maintenance, configuration, or build risk.

Examples include:

* identical dependency declarations
* redundant declarations with conflicting versions
* duplicate dependency blocks that obscure effective configuration

## Finding Gate

A duplicate declaration should only become a finding when repository
evidence shows that it creates meaningful:

* version ambiguity
* maintenance risk
* build behavior
* configuration confusion

Do not report harmless Maven declarations solely because they are
redundant.

Where the duplication has no material consequence, prefer a lower
severity or do not report it.

## Evidence Requirements

Identify:

* duplicate declaration(s)
* artifact
* versions/scopes
* resulting behavior or maintenance consequence

---

# MAVEN-004 — Unsafe Dependency Configuration

## Description

A dependency or Maven configuration creates a credible production risk
through unsafe scope, packaging, exclusion, override, repository, or
plugin behavior.

Potential mechanisms include:

* required dependency excluded from packaging
* runtime dependency incorrectly scoped
* test-only dependency used by production code
* incompatible version forced through dependency management
* unsafe transitive dependency override
* plugin configuration producing an incorrect application artifact
* repository configuration creating unreliable or non-reproducible builds

## Finding Gate

Establish:

1. the relevant Maven configuration,
2. how it affects the resulting artifact/build/runtime,
3. a credible consequence.

Do not report unusual Maven configuration as unsafe merely because it
differs from a preferred implementation.

---

# Mule Runtime Review

Inspect:

* Mule runtime version
* runtime scope/configuration
* application packaging
* deployment configuration
* Java version
* compatibility with connectors and plugins

Determine whether the build configuration and deployment configuration
refer to a consistent runtime.

If the deployment runtime is not visible, do not invent it.

Record a limitation where the missing deployment information materially
limits compatibility assessment.

---

# Java Compatibility

Inspect:

* Java version in Maven configuration
* compiler/source/target settings
* runtime configuration where available
* dependencies requiring particular Java versions
* Mule runtime compatibility

Do not report a Java version solely because a newer version exists.

Report only when repository evidence establishes a compatibility,
build, runtime, support, or deployment concern.

---

# Mule Maven Plugin

Inspect:

* plugin version
* configuration
* packaging
* deployment configuration
* runtime settings
* classifier/artifact behavior
* deployment target configuration where visible

Look for mismatches between:

* Mule runtime
* Java
* plugin
* application packaging
* deployment target

Do not assume the deployment platform when it is not visible.

---

# Connector Dependencies

For Mule connectors inspect:

* connector version
* Mule runtime compatibility
* Java compatibility where relevant
* related transitive dependencies
* configuration compatibility

Coordinate with the Connector reference.

Use:

* `MAVEN-001` for build/runtime compatibility problems
* `CON-*` for connector runtime/configuration behavior

Avoid duplicate findings for the same root cause.

---

# Dependency Versions

Do not use age alone as a finding criterion.

The following is insufficient:

```text id="x1j9qd"
Dependency version is not the latest available.
```

A dependency version becomes relevant when repository evidence establishes:

* incompatibility
* known unsafe configuration
* conflicting dependency resolution
* build failure
* runtime failure
* deployment failure
* materially relevant vulnerability information available to the
  review process

If security vulnerability information is not available, do not claim
that a dependency is vulnerable merely because it is old.

---

# Dependency Scopes

Inspect whether dependencies use appropriate scopes such as:

* compile
* provided
* runtime
* test
* system where present

Consider whether a scope can cause:

* missing runtime classes
* unnecessary packaging
* test-only dependencies leaking into production
* incompatible container/runtime behavior

Report only when the scope creates a credible consequence.

---

# Transitive Dependencies

Where dependency-tree evidence is available, inspect:

* multiple versions of the same artifact
* dependency mediation
* exclusions
* forced versions
* connector transitive dependencies

Do not report every transitive dependency.

Prioritize conflicts that can affect:

* runtime linkage
* connector behavior
* application startup
* build reproducibility
* security

---

# Plugin Configuration

Inspect Maven plugins that materially affect:

* compilation
* packaging
* Mule application packaging
* testing
* deployment
* code generation

Consider whether plugin configuration can produce:

* incorrect artifact
* missing resources
* incompatible packaging
* build failure
* deployment failure

Do not report optional plugin improvements as defects.

---

# Build Reproducibility

Where repository evidence permits, inspect:

* explicit versions
* version properties
* dependency management
* repositories
* plugin versions
* dynamic version declarations
* SNAPSHOT dependencies

Potential risks include:

* non-reproducible builds
* unexpected dependency changes
* inconsistent artifacts

Do not report dynamic versions without establishing a meaningful
reproducibility or deployment consequence.

---

# Dependency Conflicts and Runtime Behavior

A dependency conflict should be evaluated against actual application
usage.

Consider:

* whether the conflicting library is loaded at runtime,
* whether the affected connector is used,
* whether classes/packages overlap,
* whether Maven resolves one version deterministically,
* whether the resolved version is compatible.

A dependency tree containing multiple paths to the same library is not
automatically a defect.

---

# Security Coordination

Dependency security concerns may overlap with the Security review.

Do not claim a known vulnerability unless the required vulnerability
evidence is actually available.

Where a dependency configuration creates a security concern:

* use the most appropriate finding category,
* avoid duplicate findings,
* preserve evidence,
* do not expose sensitive dependency or repository credentials.

Never expose:

* repository credentials
* tokens
* private keys
* passwords
* secure property values

---

# Severity Guidance

Severity must reflect actual production/build impact.

## CRITICAL

Use only for highly credible issues likely to cause:

* catastrophic runtime/deployment failure
* severe security consequence supported by evidence

## HIGH

Use for:

* major runtime incompatibility
* severe dependency conflict
* build/deployment configuration likely to prevent production deployment
* dependency configuration causing major production behavior risk

## MEDIUM

Use for:

* meaningful dependency conflicts
* credible runtime/plugin compatibility problems
* material packaging/configuration risks
* important reproducibility problems

## LOW

Use for:

* limited dependency/configuration concerns
* lower-impact build maintainability issues

## NIT

Use only for optional Maven cleanup with no material production impact.

---

# Confidence Guidance

## HIGH

Use when the compatibility/conflict/configuration problem is directly
demonstrated by repository/build evidence.

## MEDIUM

Use when the mechanism is strong but complete deployment/runtime context
is unavailable.

## LOW

Use only when the potential consequence is meaningful but important
compatibility or dependency evidence is missing.

Avoid LOW-confidence findings when the concern is primarily speculative.

---

# False-Positive Controls

Do not create a Maven finding when:

* a dependency is simply old,
* a newer version exists,
* multiple dependency paths resolve safely,
* Maven dependency mediation produces a known compatible result,
* a duplicate declaration has no meaningful consequence,
* a plugin version differs from a preferred version without a demonstrated
  compatibility problem,
* a connector version is not the latest,
* deployment/runtime information is unavailable and no compatibility
  problem can be established,
* an optional build improvement has no production impact,
* evidence is insufficient.

When evidence is insufficient:

**Do not report the finding.**

Record the limitation where relevant.

---

# Positive Maven Indicators

Where supported by evidence, recognize strengths such as:

* consistent runtime and Java configuration
* compatible Mule Maven Plugin
* controlled dependency versions
* clean dependency tree
* appropriate dependency scopes
* explicit plugin versions
* reproducible build configuration
* appropriate exclusions
* consistent connector versions
* clean packaging configuration

Positive observations must be evidence-backed.

---

# Required Finding Fields

Any Maven finding must include:

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

* repository credentials
* passwords
* API keys
* access tokens
* private keys
* secure property values

Sensitive information must be sanitized before inclusion in the review
artifact.