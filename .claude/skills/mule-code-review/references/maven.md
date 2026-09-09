# Maven Review Rules

## Purpose

These rules define how Maven configuration must be reviewed in Mule 4
applications.

The objective is to identify Maven-related issues that can affect:

- Mule runtime compatibility
- Java compatibility
- connector compatibility
- application packaging
- build reliability
- dependency correctness
- deployment
- maintainability
- security
- production stability

Do not recommend dependency or plugin upgrades merely because newer
versions exist.

Only report compatibility or security issues when supported by repository
evidence or reliable dependency metadata.

---

## Maven Review Principles

Before reporting a Maven finding:

1. Inspect `pom.xml`.
2. Inspect `mule-artifact.json`.
3. Determine the Mule runtime version.
4. Determine the Java version.
5. Identify the Mule Maven Plugin version.
6. Identify connector versions.
7. Inspect application dependencies.
8. Inspect plugin configuration.
9. Inspect dependency scopes.
10. Inspect repositories when relevant.
11. Inspect packaging configuration.
12. Inspect related Maven profiles.
13. Determine whether the configuration is actually used.
14. Verify compatibility before reporting an issue.

Do not report dependency problems merely because versions are old.

Do not recommend upgrades unless:

- explicitly requested, or
- required to resolve a demonstrated compatibility or security problem.

---

# MAVEN-001 — Runtime Incompatibility

## Rule

Flag Maven configuration that is incompatible with the Mule runtime used by
the application.

Consider:

- Mule runtime version
- Mule Maven Plugin version
- Java version
- application dependencies
- connector compatibility

## Severity

HIGH

Escalate when the application cannot reliably build, deploy, or start.

---

# MAVEN-002 — Connector Incompatibility

## Rule

Flag connector versions that are incompatible with:

- the Mule runtime
- Java version
- Mule Maven Plugin
- other required application components

## Severity

HIGH

---

# MAVEN-003 — Unexpected Dependency Upgrade

## Rule

Flag dependency changes that unexpectedly upgrade a dependency and may
introduce:

- compatibility problems
- behavioral changes
- security concerns
- transitive dependency changes

## Severity

MEDIUM

Do not report a normal version change as a defect when the change is
intentional and compatible.

---

# MAVEN-004 — Duplicate Dependency

## Rule

Flag duplicate dependencies that create unnecessary or potentially
conflicting dependency resolution.

Consider:

- same artifact declared multiple times
- conflicting versions
- duplicate connector dependencies
- duplicate libraries

## Severity

LOW

Escalate when the duplication creates an actual runtime or build problem.

---

# MAVEN-005 — Unnecessary Dependency

## Rule

Flag dependencies that are demonstrably unused and materially increase
application complexity, packaging size, or dependency risk.

## Severity

LOW

Do not report a dependency as unnecessary solely because its usage is not
obvious from a quick search.

Inspect configuration and transitive usage where appropriate.

---

# MAVEN-006 — Plugin/Version Inconsistency

## Rule

Flag inconsistent or incompatible Maven plugin configuration.

Consider:

- Mule Maven Plugin
- compiler configuration
- packaging plugins
- testing plugins
- version properties
- duplicate plugin declarations

## Severity

MEDIUM

---

# MAVEN-007 — Java Version Incompatibility

## Rule

Flag Java configuration that is incompatible with the Mule runtime,
Mule Maven Plugin, connector versions, or application dependencies.

Consider:

- `maven.compiler.source`
- `maven.compiler.target`
- `maven.compiler.release`
- Java runtime configuration
- Mule runtime requirements

## Severity

HIGH

---

# MAVEN-008 — Conflicting Dependency Versions

## Rule

Flag multiple versions of the same dependency when Maven dependency
resolution can result in an unintended or incompatible version.

Consider:

- direct dependencies
- transitive dependencies
- connector dependencies
- shared libraries

## Severity

MEDIUM / HIGH

Escalate when there is evidence of runtime incompatibility.

---

# MAVEN-009 — Unsafe Transitive Dependency

## Rule

Flag a transitive dependency that introduces a known security or
compatibility concern when repository or dependency evidence supports the
finding.

## Severity

HIGH

Do not report vulnerabilities based solely on a dependency name without
verifying the affected version and applicability.

---

# MAVEN-010 — Dependency Scope Misconfiguration

## Rule

Flag dependencies using an inappropriate Maven scope that can cause:

- missing runtime dependencies
- unnecessary packaging
- test dependencies included in production
- compile-time/runtime mismatch

Consider:

- `compile`
- `provided`
- `runtime`
- `test`

## Severity

MEDIUM

Escalate when deployment or runtime behavior is affected.

---

# MAVEN-011 — Missing Required Dependency

## Rule

Flag application configuration that references a Mule module, connector,
library, or dependency that is required but not correctly declared.

## Severity

HIGH

Only report when repository evidence demonstrates that the dependency is
required.

---

# MAVEN-012 — Incorrect Mule Maven Plugin Configuration

## Rule

Flag Mule Maven Plugin configuration that can cause incorrect:

- packaging
- deployment
- application validation
- runtime compatibility
- artifact generation

## Severity

HIGH

---

# MAVEN-013 — Missing Mule Maven Plugin Configuration

## Rule

Flag missing Mule Maven Plugin configuration when the project structure
or build process clearly requires it.

## Severity

MEDIUM

Do not assume every project requires identical plugin configuration.

Inspect the actual build strategy.

---

# MAVEN-014 — Incorrect Packaging Configuration

## Rule

Flag Maven packaging configuration that can produce an invalid or
incomplete Mule application artifact.

Consider:

- packaging type
- Mule application packaging
- resource inclusion
- dependency packaging
- generated artifacts

## Severity

HIGH

---

# MAVEN-015 — Missing Resource Inclusion

## Rule

Flag Maven configuration that excludes resources required by the Mule
application.

Examples include:

- properties
- secure properties
- DataWeave
- schemas
- API specifications
- templates
- certificates when intentionally packaged

## Severity

HIGH

Only report when repository evidence shows the resource is required.

---

# MAVEN-016 — Incorrect Resource Filtering

## Rule

Flag Maven resource filtering that can modify Mule configuration,
DataWeave, properties, schemas, or other resources unexpectedly.

## Severity

MEDIUM

Escalate when filtering can corrupt application configuration or runtime
behavior.

---

# MAVEN-017 — Build Profile Risk

## Rule

Flag Maven profiles that can cause materially different application
behavior without clear or reliable configuration.

Consider:

- environment profiles
- deployment profiles
- property overrides
- dependency changes
- plugin changes

## Severity

MEDIUM

---

# MAVEN-018 — Environment Configuration in Maven

## Rule

Flag environment-specific values embedded in Maven configuration when
the project's established configuration strategy expects deployment-time
or secure configuration.

Examples include:

- credentials
- environment URLs
- database credentials
- API secrets
- environment-specific endpoints

## Severity

HIGH

Coordinate with:

- `references/security.md`
- `references/configuration.md`

---

# MAVEN-019 — Credentials in Maven Configuration

## Rule

Flag credentials, tokens, passwords, client secrets, or private keys
committed directly into `pom.xml` or Maven configuration.

## Severity

CRITICAL

---

# MAVEN-020 — Insecure Repository Configuration

## Rule

Flag Maven repositories or plugin repositories using insecure transport
when secure transport is required.

Examples include:

- HTTP repository URLs
- untrusted repository sources

## Severity

HIGH

Only report when the configuration creates a meaningful security risk.

---

# MAVEN-021 — Unnecessary Repository

## Rule

Flag unnecessary custom Maven repositories that materially increase:

- dependency supply-chain risk
- build complexity
- reproducibility risk

## Severity

MEDIUM

Do not report required organization repositories without evidence of risk.

---

# MAVEN-022 — Repository Resolution Ambiguity

## Rule

Flag repository configurations where the same dependency could resolve
from multiple unexpected repositories and produce inconsistent builds.

## Severity

MEDIUM

---

# MAVEN-023 — Version Property Inconsistency

## Rule

Flag Maven properties that define conflicting or inconsistent versions
for the same technology.

Examples include:

- multiple Mule runtime version properties
- conflicting connector versions
- duplicated Java version properties

## Severity

LOW / MEDIUM

Escalate when the inconsistency can produce an actual build or runtime
problem.

---

# MAVEN-024 — Hardcoded Repeated Version

## Rule

Flag repeated dependency or plugin versions when centralization would
materially reduce version drift or compatibility risk.

## Severity

LOW

Do not report simple version declarations merely because they are not
properties.

---

# MAVEN-025 — Dependency Management Conflict

## Rule

Flag `dependencyManagement` configuration that overrides dependency
versions unexpectedly or creates incompatible resolution.

## Severity

MEDIUM / HIGH

---

# MAVEN-026 — Plugin Execution Conflict

## Rule

Flag multiple Maven plugin executions that can:

- execute the same lifecycle operation incorrectly
- package the application multiple times
- run tests unexpectedly
- modify generated artifacts incorrectly

## Severity

MEDIUM

---

# MAVEN-027 — Test Plugin Misconfiguration

## Rule

Flag Maven test configuration that prevents MUnit tests from reliably
executing or causes important tests to be skipped.

## Severity

HIGH

Coordinate with `references/munit.md`.

---

# MAVEN-028 — Build Reproducibility Risk

## Rule

Flag Maven configuration that can cause materially different builds
from the same source.

Consider:

- dynamic dependency versions
- uncontrolled repositories
- environment-dependent resolution
- unstable plugin versions
- unpinned important dependencies

## Severity

MEDIUM

Do not require every transitive dependency to be manually pinned.

---

# MAVEN-029 — Dynamic Dependency Version

## Rule

Flag dynamic versions such as ranges or uncontrolled version selectors
when they can cause non-reproducible or unexpected builds.

## Severity

MEDIUM

---

# MAVEN-030 — Snapshot Dependency Risk

## Rule

Flag production applications that rely on snapshot dependencies when
there is evidence that the snapshot dependency can cause unstable or
non-reproducible builds.

## Severity

MEDIUM / HIGH

Do not automatically classify every snapshot dependency as a defect.

---

# MAVEN-031 — Unnecessary Test/Runtime Packaging

## Rule

Flag test-only or development-only dependencies that are unintentionally
included in the production artifact.

## Severity

MEDIUM

---

# MAVEN-032 — Oversized Dependency Footprint

## Rule

Flag unnecessary dependencies that materially increase:

- application artifact size
- startup time
- dependency conflict risk
- security exposure

## Severity

LOW / MEDIUM

Only report when the impact is meaningful.

---

# MAVEN-033 — Dependency Conflict With Mule Runtime

## Rule

Flag manually added libraries that override or conflict with libraries
provided by the Mule runtime or Mule modules.

## Severity

HIGH

Only report when there is evidence of an actual or likely compatibility
problem.

---

# MAVEN-034 — Incorrect Dependency Exclusion

## Rule

Flag exclusions that remove a dependency required by:

- Mule runtime
- connector
- application code
- test framework

## Severity

HIGH

---

# MAVEN-035 — Excessive Dependency Exclusions

## Rule

Flag unnecessary dependency exclusions that create:

- maintenance complexity
- fragile dependency resolution
- unexpected runtime behavior

## Severity

LOW / MEDIUM

---

# MAVEN-036 — Missing Dependency Security Review

## Rule

Flag significant third-party dependencies with known security concerns
when repository evidence or authoritative vulnerability information
supports the finding.

## Severity

HIGH

Do not report vulnerabilities without verifying the affected dependency
version.

---

# MAVEN-037 — Incompatible Compiler Configuration

## Rule

Flag compiler settings that can produce bytecode incompatible with the
Java runtime used by Mule.

## Severity

HIGH

---

# MAVEN-038 — Incorrect Encoding Configuration

## Rule

Flag Maven build configuration that can cause inconsistent character
encoding when the application depends on a specific encoding.

## Severity

LOW / MEDIUM

Only report when the configuration can materially affect application
behavior.

---

# MAVEN-039 — Build Plugin Version Risk

## Rule

Flag Maven plugins with versions that are demonstrably incompatible with
the project's Java, Mule runtime, or build environment.

## Severity

MEDIUM / HIGH

Do not flag old plugin versions solely because newer versions exist.

---

# MAVEN-040 — Deployment Configuration Conflict

## Rule

Flag Maven deployment configuration that conflicts with the application's
actual deployment model.

Consider:

- CloudHub
- Runtime Fabric
- standalone Mule runtime
- hybrid deployment
- organization-specific deployment configuration

## Severity

HIGH

Only report when repository evidence demonstrates a conflict.

---

# Maven False-Positive Controls

Do not report:

- old dependencies merely because newer versions exist
- dependency upgrades merely because they are not the latest
- required organization repositories without evidence of risk
- duplicate-looking dependencies that serve different purposes
- intentionally pinned dependency versions
- snapshot dependencies without meaningful production risk
- missing Maven profiles when profiles are not required
- version properties merely because they are not centralized
- every transitive dependency as a security problem
- dependency vulnerabilities without verifying affected versions
- Maven configuration that is unused
- stylistic POM preferences without production impact
- plugin versions solely because newer versions are available

---

# Maven Finding Quality Gate

Before reporting a Maven finding:

1. Inspect `pom.xml`.
2. Identify the affected dependency or plugin.
3. Determine its actual version.
4. Determine Mule runtime version.
5. Determine Java version.
6. Inspect related configuration.
7. Determine whether the dependency/plugin is actually used.
8. Verify compatibility.
9. Verify production impact.
10. Check whether another configuration already addresses the issue.
11. Confirm severity.
12. Identify the exact POM location.
13. Provide actionable remediation.

If the issue cannot be substantiated, do not report it.

---

# Maven Finding Format

Use the following structure for every Maven finding.

**Finding ID:** MAVEN-001

**Severity:** HIGH

**Category:** MAVEN

**File:** `pom.xml:120`

**Location:** Dependency / Plugin / Profile / Property

**Problem:**

Describe the Maven configuration problem.

**Evidence:**

Identify the relevant dependency, plugin, version, property, or
configuration.

**Impact:**

Explain the realistic build, deployment, runtime, security, or
maintainability impact.

**Recommendation:**

Provide an actionable remediation approach.

**Confidence:** HIGH / MEDIUM / LOW