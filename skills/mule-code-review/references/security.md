# Security Review Rules

## Purpose

Review MuleSoft applications for security weaknesses involving:

* secrets and credentials
* authentication
* authorization
* transport security
* sensitive data
* injection
* excessive permissions
* secure properties
* logging
* external integrations
* API exposure
* configuration

Security findings must be evidence-based and tied to an actual or
credible security impact.

Never expose secret values or sensitive data in the review report.

---

# Security Review Principles

Before reporting a security finding:

1. Identify the security-sensitive resource or behavior.
2. Inspect surrounding implementation.
3. Inspect related global configurations.
4. Inspect properties and secure properties.
5. Trace relevant data flows.
6. Inspect API specifications and policies where available.
7. Inspect authentication and authorization controls.
8. Inspect logging and error handling.
9. Determine whether another control mitigates the issue.
10. Establish the actual exposure or attack path.
11. Determine production/security impact.
12. Assign severity and confidence based on evidence.

The existence of a credential, HTTP endpoint, or sensitive field is not
automatically a vulnerability.

---

# SEC-001 — Secret Exposed in Source

## Description

A secret or credential is directly embedded in source code or another
repository-controlled artifact in a manner that exposes the secret to
unauthorized repository users or source-management systems.

Potential examples include:

* passwords
* API keys
* client secrets
* access tokens
* private keys
* database credentials
* embedded authentication headers
* hardcoded credentials in Mule XML
* credentials embedded in DataWeave
* secrets committed to configuration files

## Finding Gate

A finding requires evidence that the value is actually secret material
or credential data.

Do not classify:

* usernames
* public identifiers
* non-secret configuration
* documented example values
* intentionally public values

as secrets without supporting evidence.

## Evidence Requirements

Identify:

* file
* structural location
* type of secret
* exposure mechanism

Never reproduce the secret value.

Use a masked representation such as:

`[REDACTED SECRET]`

## Impact Examples

Potential impacts include:

* credential compromise
* unauthorized access
* repository leakage
* lateral movement
* service impersonation

---

# SEC-002 — Secret Exposed in Logs

## Description

Application logging writes credentials, tokens, authorization headers,
private keys, or other secret material to an operational log destination.

Potential sources include:

* Logger processors
* error handlers
* HTTP request/response logging
* payload logging
* DataWeave-generated log messages
* exception details

## Finding Gate

The review must establish a data path by which secret material can reach
the log.

Do not report a logging concern solely because a logger exists.

## Evidence Requirements

Identify:

* logger
* source of sensitive value
* logging expression
* destination where known
* exposure mechanism

Never reproduce the secret.

## Impact Examples

Potential impacts include:

* credential disclosure
* unauthorized access
* log aggregation exposure
* compliance/security incident

---

# SEC-003 — Sensitive Data Exposed

## Description

Sensitive information is exposed to an inappropriate destination,
consumer, log, response, message, or integration.

Potential information includes:

* PII
* financial information
* authentication information
* personal identifiers
* confidential business data
* sensitive payload fields

## Finding Gate

The data must be demonstrably sensitive or protected, and the review
must establish an inappropriate exposure path.

Do not assume that every customer or business field is sensitive without
supporting evidence.

## Evidence Requirements

Identify:

* sensitive data type
* source
* processing path
* destination
* exposure mechanism
* applicable contract/control where available

Do not reproduce sensitive values.

## Impact Examples

Potential impacts include:

* privacy breach
* unauthorized disclosure
* regulatory exposure
* data leakage

---

# SEC-004 — Authentication Weakness

## Description

Authentication controls are absent, incorrectly configured, bypassable,
or materially weaker than required by the application's exposed
interface or integration contract.

Potential areas include:

* unauthenticated protected endpoints
* weak authentication configuration
* missing authentication enforcement
* credentials transmitted insecurely
* authentication checks that can be bypassed

## Finding Gate

The application must expose a resource that requires authentication or
repository evidence must establish an authentication requirement.

Do not assume every HTTP listener requires authentication.

## Evidence Requirements

Identify:

* exposed endpoint/resource
* authentication mechanism
* configuration
* relevant policy or implementation
* bypass or weakness

## Impact Examples

Potential impacts include:

* unauthorized access
* account/service impersonation
* protected data exposure
* unauthorized operations

---

# SEC-005 — Authorization Weakness

## Description

An authenticated caller can access or perform operations beyond the
permissions established by the application's authorization model.

Potential examples include:

* missing authorization checks
* object-level authorization gaps
* privilege escalation
* insufficient role enforcement
* authorization applied to some paths but not equivalent paths

## Finding Gate

Authentication is not authorization.

A finding requires evidence of:

* a protected resource/action
* the expected authorization boundary
* the missing or ineffective control
* a credible unauthorized access path

Do not report missing authorization when the authorization control is
implemented elsewhere and evidence confirms it applies.

## Evidence Requirements

Identify:

* endpoint or operation
* caller/security context
* authorization control
* missing or bypassable check
* affected resource/action

## Impact Examples

Potential impacts include:

* unauthorized data access
* privilege escalation
* unauthorized modification
* cross-tenant data exposure

---

# SEC-006 — TLS/Security Configuration Weakness

## Description

Transport or security configuration creates a meaningful risk to
confidentiality, integrity, or authentication.

Potential examples include:

* insecure HTTP for sensitive communication
* disabled or weakened TLS verification
* inappropriate TLS protocol configuration
* unsafe trust configuration
* inappropriate certificate validation
* insecure client/server transport settings

## Finding Gate

The configuration must create an actual or credible security weakness.

Do not report:

* HTTP used for a deliberately non-sensitive local endpoint
* TLS settings without evidence of security impact
* certificate configuration merely because it differs from a preferred
  implementation

Consider the communication path, data sensitivity, deployment
environment, and actual configuration.

## Evidence Requirements

Identify:

* listener/request configuration
* TLS/security configuration
* communication destination
* sensitive data or authentication context where relevant
* resulting security consequence

## Impact Examples

Potential impacts include:

* credential interception
* traffic interception
* man-in-the-middle attacks
* data disclosure
* loss of transport integrity

---

# SEC-007 — Injection Risk

## Description

Untrusted or insufficiently controlled input reaches an interpreter,
query language, command, expression, or other executable context in a
way that can alter intended behavior.

Potential areas include:

* SQL
* dynamic query construction
* expression evaluation
* command execution
* scripting
* dynamic resource identifiers
* other interpreter-based operations

## Finding Gate

A finding requires a credible data-flow path:

**Untrusted input → executable/interpreted context → altered behavior**

Do not report injection solely because:

* string concatenation exists
* a query is dynamically constructed
* user input is present
* DataWeave constructs a string

Determine whether the target mechanism interprets the resulting value
as executable/query syntax.

## Evidence Requirements

Identify:

* untrusted input source
* transformation/data flow
* target interpreter/query
* missing validation/parameterization/control
* possible altered behavior

## Impact Examples

Potential impacts include:

* unauthorized database access
* data modification
* data disclosure
* query manipulation
* command execution

---

# Secure Properties

Inspect:

* secure property configuration
* secret references
* encryption configuration
* environment-specific secret injection
* accidental duplication of secrets into plain properties
* secret values referenced from source

Do not report secure-property usage as a weakness.

A finding requires evidence that secrets bypass, undermine, or are
incorrectly handled by the secure-property mechanism.

---

# Excessive Permissions

Where deployment or integration configuration provides permissions,
inspect whether the application receives privileges materially beyond
what its demonstrated operations require.

Consider:

* database privileges
* cloud/service permissions
* API scopes
* messaging permissions
* filesystem permissions
* deployment/runtime permissions

Do not report least-privilege concerns when the required permissions
cannot reasonably be established from repository evidence.

If required permissions are unknown, record the limitation rather than
inventing a finding.

---

# Sensitive Data Flow

Trace sensitive data through:

* inbound APIs
* variables
* payloads
* DataWeave transformations
* logs
* database operations
* messaging
* outbound APIs
* error responses

Determine whether sensitive data reaches a destination that is
inappropriate for its classification.

Do not reproduce sensitive payload values in findings.

---

# Authentication and Authorization Boundaries

Review security boundaries across:

* HTTP listeners
* API implementations
* API policies where represented in the repository
* flow references
* private flows
* outbound integrations
* administrative endpoints

Do not assume a private flow is itself an authorization boundary.

Trace how externally controlled input reaches protected operations.

---

# Security Severity Guidance

Severity must reflect exploitability and production impact.

### CRITICAL

Use for issues such as:

* exposed highly privileged credentials
* severe authorization bypass
* critical secret exposure
* broadly exploitable vulnerabilities with catastrophic impact

### HIGH

Use for issues such as:

* meaningful credential exposure
* major authorization weakness
* exploitable injection
* significant sensitive-data exposure
* severe TLS weakness affecting sensitive traffic

### MEDIUM

Use for:

* meaningful but constrained security weaknesses
* limited authorization gaps
* contained sensitive-data exposure
* lower-impact injection risks

### LOW

Use for:

* limited security exposure
* defense-in-depth gaps with constrained impact

### NIT

Use only for optional security improvements that do not represent a
material security risk.

---

# False-Positive Controls

Do not create a security finding when:

* the value is not demonstrably secret
* the secret is correctly externalized and protected
* sensitive data remains within an appropriate security boundary
* authentication is enforced by a verified external mechanism
* authorization is implemented in another verified component
* TLS configuration is appropriate for the actual communication
* parameterization/escaping prevents the suspected injection
* another security control mitigates the issue
* repository evidence is insufficient to establish the vulnerability

When evidence is insufficient:

**Do not report the finding.**

Record the limitation where relevant.

---

# Evidence and Secret Handling

Security evidence must demonstrate the issue without disclosing the
sensitive material.

Never include:

* passwords
* API keys
* client secrets
* access tokens
* private keys
* authorization headers
* secure property values
* full sensitive payloads

Use descriptions such as:

* `[REDACTED PASSWORD]`
* `[REDACTED API KEY]`
* `[REDACTED TOKEN]`
* `[REDACTED PRIVATE KEY]`
* `[REDACTED SENSITIVE DATA]`

Do not place secret values in:

* findings
* evidence excerpts
* logs
* generated JSON
* report appendices
* final chat output

---

# Positive Security Indicators

Where supported by evidence, recognize strengths such as:

* secure properties used correctly
* secrets externalized
* appropriate authentication
* explicit authorization controls
* parameterized database operations
* appropriate TLS configuration
* sanitized error responses
* sensitive data excluded from logs
* least-privilege configuration
* controlled API exposure

Positive observations must be supported by repository evidence.

---

# Required Finding Fields

Any security finding must include:

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

Evidence excerpts must be sanitized before inclusion in the review
artifact.