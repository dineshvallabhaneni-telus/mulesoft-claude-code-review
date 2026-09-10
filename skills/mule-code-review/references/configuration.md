# Configuration Review Rules

## Purpose

Review MuleSoft application configuration for:

* environment separation
* property resolution
* secure property usage
* hardcoded environment-specific values
* credentials
* URLs and endpoints
* ports
* identifiers
* deployment configuration
* configuration duplication
* configuration precedence
* configuration consistency
* operational portability

The objective is to identify configuration problems that create a
credible security, deployment, reliability, or operational risk.

Do not treat every literal value as a configuration defect.

---

# Configuration Review Principles

Before reporting a configuration finding:

1. Identify configuration files and property sources.
2. Inspect how properties are referenced by Mule flows.
3. Inspect global configurations.
4. Inspect secure properties configuration where present.
5. Inspect environment-specific files or profiles where available.
6. Inspect deployment configuration where available.
7. Trace important values from definition to consumption.
8. Determine whether values are intentionally constant or environment
   dependent.
9. Determine whether configuration resolution is consistent.
10. Assess the actual production consequence.
11. Assign severity and confidence based on evidence.

Do not assume a particular deployment platform.

Do not assume deployment configuration exists.

---

# CFG-001 — Environment-Specific Value Hardcoded

## Description

An environment-specific value is embedded directly in application source
or configuration instead of being externally configurable.

Potential examples include:

* environment-specific URLs
* hostnames
* ports
* queue/topic names
* database identifiers
* external service endpoints
* tenant identifiers
* deployment-specific paths
* environment-specific feature settings

## Finding Gate

Establish:

1. the value is environment-specific,
2. the value is hardcoded rather than resolved through configuration,
3. different environments reasonably require different values, and
4. the hardcoding creates a credible deployment or operational risk.

Do not report constants merely because they are literals.

Examples that are generally not sufficient by themselves:

```text
HTTP method = GET
timeout unit = SECONDS
business status = ACTIVE
```

## Evidence Requirements

Identify:

* affected file
* configuration/value
* consuming component
* evidence that the value is environment-dependent
* deployment or operational consequence

---

# CFG-002 — Credential Configuration Concern

## Description

Credentials or authentication material are configured in a manner that
creates a security or operational risk.

Potential concerns include:

* credentials directly embedded in source
* credentials stored in ordinary properties without appropriate protection
* insecure credential references
* credentials duplicated across configuration
* authentication material exposed through deployment configuration
* secure property configuration that is not actually used by the consuming
  component

Coordinate with the Security reference for secret exposure.

## Finding Gate

Establish the actual configuration mechanism.

Do not report a credential concern merely because:

* a username exists,
* a property contains a non-secret identifier,
* a secure property mechanism exists,
* an authentication configuration is visible.

If a secret is present, never include its value in the report.

Use sanitized evidence such as:

```text
password = [REDACTED]
```

or:

```text
secure::db.password
```

where appropriate.

## Evidence Requirements

Identify:

* authentication configuration
* property source
* consuming connector/global configuration
* protection mechanism
* actual security/operational consequence

---

# CFG-003 — Configuration Duplication Creates Risk

## Description

The same operational configuration is duplicated across multiple files,
flows, or global configurations in a way that can result in inconsistent
behavior or difficult operational changes.

Potential examples include duplicated:

* endpoints
* timeout values
* retry settings
* connection settings
* queue/topic names
* feature settings
* environment-specific identifiers

## Finding Gate

Duplication becomes a finding only when evidence demonstrates a credible
risk such as:

* inconsistent values,
* configuration drift,
* one component being updated while another is not,
* environment-specific behavior becoming inconsistent,
* operational changes requiring error-prone manual updates.

Do not report simple repetition when it has no meaningful consequence.

## Evidence Requirements

Identify:

* duplicated configuration
* affected files/components
* differences or synchronization risk
* resulting operational impact

---

# CFG-004 — Environment Separation Concern

## Description

Application configuration does not provide adequate separation between
environments where repository evidence establishes that separation is
required.

Potential concerns include:

* development endpoint used by production configuration
* production values embedded in source
* environment-specific settings mixed together
* configuration profiles not clearly separated
* deployment configuration overriding application settings unexpectedly
* inconsistent property resolution across environments

## Finding Gate

Establish:

1. multiple environments or environment-specific behavior are visible,
2. the relevant configuration is not adequately separated, and
3. the configuration creates a credible deployment or production risk.

Do not invent environment names or deployment models.

If only one environment is visible, do not assume that additional
environments exist.

---

# Configuration Resolution

Trace important properties through their lifecycle:

```text
Property Source
      |
      v
Property Resolution
      |
      v
Global Configuration
      |
      v
Flow / Connector
      |
      v
Runtime Behavior
```

Inspect for:

* unresolved properties
* inconsistent property names
* incorrect property references
* conflicting property sources
* unexpected defaults
* environment overrides
* secure-property resolution
* configuration precedence

Only create a finding when the evidence demonstrates a meaningful
consequence.

---

# Secure Properties

Where secure properties are used, inspect:

* secure property configuration
* referenced keys
* consuming components
* encrypted/protected values
* consistency of property names
* environment-specific secure property handling

A secure-properties file existing in the repository is not itself a
finding.

Conversely, merely defining secure properties does not prove that
credentials are protected.

Trace actual consumption where relevant.

Never expose secure property values.

---

# URLs and Endpoints

Inspect:

* HTTP listener addresses
* HTTP request URLs
* database hosts
* messaging endpoints
* SaaS endpoints
* external service URLs

Determine whether each value is:

* intentionally constant,
* environment-specific,
* externally configurable.

Do not report a URL simply because it is written as a literal.

For example, a publicly documented fixed third-party endpoint may be an
intentional constant.

---

# Ports

Inspect hardcoded ports and listener configuration.

A hardcoded port is not automatically a finding.

Report only when:

* the port is environment-specific,
* deployment requires different values,
* or the configuration creates a demonstrated operational conflict.

---

# Identifiers

Inspect values such as:

* queue names
* topic names
* database/schema identifiers
* client/application identifiers
* tenant identifiers
* environment identifiers

Determine whether they are:

* business constants,
* globally fixed identifiers,
* environment-specific configuration.

Do not classify business constants as environment-specific without
evidence.

---

# Deployment Configuration

Where deployment configuration exists, inspect:

* target environment
* runtime
* worker/resource settings
* environment variables
* secure configuration
* property overrides
* deployment-specific endpoints
* application configuration precedence

Do not assume a deployment configuration file exists.

If deployment configuration is unavailable and this materially limits
assessment, record:

**Not Identified**

or document the limitation as appropriate.

---

# Configuration Duplication

Distinguish between:

**Intentional duplication**

Values intentionally repeated because they represent independent
configuration.

**Risk-producing duplication**

Values that must remain synchronized and where divergence can alter
application behavior.

Only the second should normally become a finding.

---

# Cross-Domain Coordination

Avoid duplicate findings with other review domains.

Use:

* `CFG-*` for configuration architecture and environment separation.
* `SEC-*` for security weaknesses involving exposed or inadequately
  protected secrets.
* `CON-*` for connector runtime/configuration behavior.
* `MAVEN-*` for Maven/build/dependency configuration.
* `XML-*` for Mule XML configuration behavior.

If one root cause produces multiple symptoms, prefer one consolidated
finding unless the impacts or remediation materially differ.

---

# Severity Guidance

Severity must reflect the actual consequence.

## CRITICAL

Rarely appropriate.

Use only when configuration creates a highly credible catastrophic
security or production consequence.

## HIGH

Use for:

* production credentials exposed through configuration
* production environment connected to an unintended critical endpoint
* configuration capable of causing major deployment or security failure
* severe environment separation failure

## MEDIUM

Use for:

* meaningful environment-specific hardcoding
* material configuration drift risk
* important credential configuration weakness
* configuration inconsistency capable of affecting production behavior

## LOW

Use for:

* limited configuration portability concerns
* localized duplication with operational impact
* lower-impact environment management issues

## NIT

Use only for optional configuration cleanup without material risk.

---

# Confidence Guidance

## HIGH

The configuration problem and its consequence are directly demonstrated.

## MEDIUM

The configuration concern is strongly supported, but deployment or
environment context is incomplete.

## LOW

Use only when the concern is meaningful but important configuration
context is unavailable.

Avoid LOW-confidence findings where the issue depends primarily on
assumptions about deployment practices.

---

# False-Positive Controls

Do not create a configuration finding when:

* a literal value is intentionally constant,
* an endpoint is demonstrably environment-independent,
* secure properties are correctly configured and consumed,
* configuration duplication has no meaningful consequence,
* deployment configuration is simply not present in the repository,
* an environment is not visible and cannot reasonably be inferred,
* a preferred configuration pattern is not required by the application,
* evidence is insufficient.

When evidence is insufficient:

**Do not report the finding.**

Record the limitation where relevant.

---

# Positive Configuration Indicators

Where supported by evidence, recognize strengths such as:

* environment-specific values externalized
* secure properties correctly used
* consistent property naming
* centralized reusable configuration
* clear environment separation
* minimal configuration duplication
* predictable property resolution
* deployment configuration aligned with application configuration

Positive observations must be evidence-backed.

---

# Required Finding Fields

Any configuration finding must include:

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
* access tokens
* private keys
* authorization headers
* secure property values
* connection strings containing credentials

Sensitive information must be sanitized before inclusion in the review
artifact.