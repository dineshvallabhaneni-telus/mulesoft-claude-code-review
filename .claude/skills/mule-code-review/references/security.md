# MuleSoft Security Review Rules

## Purpose

These rules define how MuleSoft applications must be reviewed for
security vulnerabilities and insecure configuration.

Review security in the context of:

- Mule flows
- Mule XML
- DataWeave
- HTTP APIs
- RAML/OAS
- HTTP Request
- HTTP Listener
- Database
- Salesforce
- Messaging
- SFTP
- Object Store
- secure properties
- TLS
- authentication
- authorization
- logging
- error handling
- Maven dependencies
- deployment configuration

Do not report a security issue based only on a theoretical possibility.

A finding must be supported by repository evidence and must identify a
realistic attack path, exposure, or security weakness.

---

# Security Review Principles

Before reporting a security finding:

1. Identify the sensitive asset or protected operation.
2. Identify where the value or permission originates.
3. Trace how it is stored, transmitted, logged, or exposed.
4. Determine whether an existing security control already protects it.
5. Inspect related configuration and global configurations.
6. Inspect API specifications and authentication configuration.
7. Determine whether the issue is actually exploitable or operationally
   significant.
8. Identify the realistic impact.
9. Assign severity based on evidence.

Do not report:

- obvious placeholders
- example credentials
- documentation-only values
- intentionally public configuration
- test values without meaningful security impact

as real secrets unless repository evidence supports the conclusion.

---

# SEC-001 — Hardcoded Password

## Rule

Flag passwords committed directly into:

- Mule XML
- DataWeave
- properties
- Maven configuration
- deployment configuration
- source code
- test configuration

when the value represents an actual credential.

## Severity

CRITICAL

---

# SEC-002 — Hardcoded API Key

## Rule

Flag API keys committed directly into application source or configuration
when they provide access to an actual external service.

## Severity

CRITICAL

---

# SEC-003 — Hardcoded OAuth/Client Secret

## Rule

Flag OAuth client secrets, client credentials, or equivalent secrets
stored directly in source-controlled application files.

## Severity

CRITICAL

---

# SEC-004 — Hardcoded Access Token

## Rule

Flag access tokens, bearer tokens, refresh tokens, or equivalent
authentication material committed to the repository.

## Severity

CRITICAL

---

# SEC-005 — Private Key Committed

## Rule

Flag private keys, private certificates, keystores containing private
credentials, or equivalent sensitive cryptographic material committed
to source control.

## Severity

CRITICAL

---

# SEC-006 — Secret in Logs

## Rule

Flag logging of:

- passwords
- API keys
- OAuth secrets
- access tokens
- refresh tokens
- private keys
- encryption keys
- credentials

## Severity

CRITICAL

---

# SEC-007 — Authorization Header Logged

## Rule

Flag logging of:

- `Authorization`
- `Proxy-Authorization`
- bearer tokens
- Basic authentication credentials
- equivalent authentication headers

## Severity

CRITICAL

---

# SEC-008 — Sensitive Payload Logged

## Rule

Flag logging of sensitive payload data when the payload contains
credentials, financial information, personal information, authentication
data, or other sensitive business information.

## Severity

HIGH

Escalate when the logged data contains credentials or security secrets.

---

# SEC-009 — PII Logged

## Rule

Flag unnecessary logging of personally identifiable information such as:

- government identifiers
- financial information
- personal contact information
- addresses
- identity information
- authentication information
- other sensitive personal data

when repository evidence indicates the data is sensitive.

## Severity

HIGH

Do not classify ordinary business data as PII without evidence.

---

# SEC-010 — Insecure HTTP Transport

## Rule

Flag HTTP rather than HTTPS when transport security is required.

Consider:

- inbound APIs
- outbound HTTP Request
- external services
- authentication endpoints
- sensitive data transmission

## Severity

HIGH

Do not flag localhost, test-only, or explicitly non-sensitive internal
traffic without evidence that transport security is required.

---

# SEC-011 — TLS Validation Weakened

## Rule

Flag:

- disabled certificate validation
- disabled hostname verification
- trust-all certificates
- insecure TLS configuration
- equivalent mechanisms that bypass certificate validation

## Severity

CRITICAL

---

# SEC-012 — Secret Stored Outside Secure Configuration

## Rule

Flag sensitive values stored in ordinary source-controlled properties
or configuration when the project provides or should use:

- secure configuration properties
- environment-injected secrets
- deployment-time secrets
- external secret management

## Severity

HIGH

Do not automatically classify every configuration value as a secret.

---

# SEC-013 — Excessive Permissions

## Rule

Flag credentials, integration users, API clients, or service accounts
granted substantially more access than required when repository evidence
supports the finding.

Consider:

- Salesforce permissions
- database users
- API scopes
- OAuth scopes
- cloud roles
- messaging permissions
- SFTP permissions

## Severity

HIGH

---

# SEC-014 — Missing Authorization

## Rule

Flag protected operations that authenticate a caller but do not enforce
appropriate authorization.

Distinguish:

- authentication — who the caller is
- authorization — what the caller is allowed to do

## Severity

HIGH

Escalate to CRITICAL when unauthorized users can perform highly
privileged or sensitive operations.

---

# SEC-015 — Injection Vulnerability

## Rule

Check dynamically constructed inputs for injection risks involving:

- SQL
- expressions
- headers
- URLs
- commands
- queries
- filters
- downstream request content

## Severity

CRITICAL / HIGH

Use CRITICAL when exploitation can provide broad unauthorized access,
data modification, credential compromise, or remote code execution.

---

# SEC-016 — Hardcoded Credential in Test Code

## Rule

Flag real credentials committed in:

- MUnit tests
- test properties
- test resources
- mock configuration
- test fixtures

## Severity

HIGH

Escalate to CRITICAL when the credential provides real production or
privileged access.

---

# SEC-017 — Secret in API Specification

## Rule

Flag real secrets or authentication credentials embedded in:

- RAML
- OAS
- examples
- API fragments
- API documentation

## Severity

CRITICAL

Do not flag documented placeholder values such as clearly identified
examples.

---

# SEC-018 — Credential Propagation to Untrusted Destination

## Rule

Flag flows that forward credentials, tokens, authorization headers, or
other authentication material to downstream systems without evidence
that the destination is authorized to receive them.

## Severity

CRITICAL

---

# SEC-019 — Unnecessary Credential Propagation

## Rule

Flag flows that forward authentication information to downstream systems
when the downstream integration does not require it.

Consider:

- Authorization headers
- cookies
- client certificates
- access tokens
- API keys

## Severity

HIGH

---

# SEC-020 — Authentication Missing

## Rule

Flag externally accessible protected APIs or operations that have no
appropriate authentication mechanism when repository evidence indicates
authentication is required.

## Severity

HIGH

Escalate to CRITICAL for sensitive or privileged operations.

---

# SEC-021 — Weak Authentication Configuration

## Rule

Flag authentication configurations that use materially weaker controls
than required by the application's security model.

Consider:

- weak authentication schemes
- static credentials where stronger mechanisms are established
- inappropriate credential reuse
- insecure authentication flows

## Severity

HIGH

Do not prescribe a specific authentication mechanism without considering
the application's architecture and requirements.

---

# SEC-022 — Broken Authorization Boundary

## Rule

Flag cases where authorization is performed at an incorrect level and
allows a caller to access or modify resources belonging to another user,
tenant, account, or business context.

Consider:

- object-level authorization
- tenant isolation
- account identifiers
- path parameters
- query parameters
- request body identifiers

## Severity

CRITICAL

---

# SEC-023 — Missing Tenant Isolation

## Rule

For multi-tenant applications, flag flows that allow one tenant to
access or modify another tenant's data when tenant isolation is required.

## Severity

CRITICAL

Only apply this rule when multi-tenancy is established by repository
evidence.

---

# SEC-024 — Sensitive Data Returned to Client

## Rule

Flag API responses that unnecessarily expose:

- passwords
- credentials
- tokens
- internal identifiers
- security configuration
- sensitive personal information
- internal system details

## Severity

HIGH

Escalate when credentials or authentication material are exposed.

---

# SEC-025 — Sensitive Data in Error Response

## Rule

Flag error responses exposing:

- stack traces
- SQL statements
- internal URLs
- filesystem paths
- credentials
- tokens
- internal hostnames
- infrastructure details
- implementation details

## Severity

HIGH

---

# SEC-026 — Sensitive Data in Variables or Attributes

## Rule

Flag unnecessary storage of sensitive information in:

- Mule variables
- attributes
- payloads
- logging context
- custom error objects

when the data can later be exposed or propagated unnecessarily.

## Severity

MEDIUM

Escalate when credentials or secrets are involved.

---

# SEC-027 — Insecure Cookie Handling

## Rule

For HTTP APIs using cookies, flag missing or inappropriate security
attributes when applicable.

Consider:

- Secure
- HttpOnly
- SameSite
- domain
- path
- expiration

## Severity

HIGH

Only apply when the application actually uses browser/client cookies.

---

# SEC-028 — CORS Misconfiguration

## Rule

For browser-accessible APIs, flag overly permissive CORS configuration
when it creates a realistic security risk.

Consider:

- wildcard origins
- credentialed requests
- unrestricted methods
- unrestricted headers

## Severity

MEDIUM

Escalate when sensitive authenticated operations are exposed.

Do not flag CORS configuration when the API is not browser-accessible
without evidence that CORS is relevant.

---

# SEC-029 — Missing Rate Limiting / Abuse Protection

## Rule

Flag externally accessible sensitive or expensive operations when the
repository provides no reasonable protection against uncontrolled
request volume and a realistic abuse scenario exists.

Consider:

- authentication endpoints
- expensive operations
- search APIs
- file processing
- resource-intensive integrations

## Severity

MEDIUM

Do not require rate limiting for every API.

---

# SEC-030 — Server-Side Request Forgery Risk

## Rule

Flag outbound HTTP requests where an attacker can control the target URL,
host, or equivalent destination and the application does not appropriately
restrict allowed destinations.

## Severity

HIGH

Escalate when internal services, metadata endpoints, or privileged
network resources could be reached.

---

# SEC-031 — Unsafe Dynamic URL Construction

## Rule

Flag dynamic URL construction where untrusted input can alter:

- host
- scheme
- port
- path
- query parameters

and create a security boundary violation.

## Severity

HIGH

---

# SEC-032 — XML Security Weakness

## Rule

When processing untrusted XML, review for unsafe XML parser behavior,
including risks associated with:

- external entity processing
- external resource resolution
- unsafe parser configuration

## Severity

HIGH

Only report when the repository and runtime configuration provide
evidence of an actual exposure.

---

# SEC-033 — Unsafe File Path Handling

## Rule

Flag file or SFTP operations where untrusted input can control file paths
and potentially access unintended files or directories.

Consider:

- path traversal
- filename construction
- directory selection
- archive extraction

## Severity

HIGH

---

# SEC-034 — Unsafe Header Propagation

## Rule

Flag forwarding of untrusted or sensitive HTTP headers when it can:

- bypass downstream security controls
- inject headers
- leak authentication information
- alter security-sensitive behavior

## Severity

HIGH

---

# SEC-035 — Missing Input Validation

## Rule

Flag security-sensitive inputs that are accepted without appropriate
validation when untrusted input can affect:

- authorization
- resource identifiers
- SQL
- URLs
- file paths
- downstream requests
- business security rules

## Severity

HIGH

Do not require validation for every field.

Focus on security-sensitive input.

---

# SEC-036 — Trusting Client-Supplied Security Context

## Rule

Flag authorization decisions based solely on client-controlled values
such as:

- user ID
- role
- tenant ID
- account ID
- privilege flag

when the application does not verify the value through a trusted
security context.

## Severity

CRITICAL

---

# SEC-037 — Insecure Secret Rotation Design

## Rule

Flag designs where credentials or secrets require source-code changes
or application redeployment unnecessarily when the existing architecture
supports secure runtime/deployment configuration.

## Severity

MEDIUM

Escalate when rotation requires exposing or committing secrets.

---

# SEC-038 — Encryption Key Exposure

## Rule

Flag encryption/decryption keys or key material stored in:

- source code
- ordinary properties
- logs
- payloads
- API responses

without appropriate protection.

## Severity

CRITICAL

---

# SEC-039 — Weak Cryptographic Configuration

## Rule

Flag obsolete or materially weak cryptographic configuration when
repository evidence demonstrates its use for security-sensitive data.

Consider:

- weak algorithms
- weak key sizes
- insecure cipher configuration
- deprecated protocols

## Severity

HIGH

Do not report based solely on the existence of an old algorithm in an
unused dependency.

---

# SEC-040 — Insecure Password Handling

## Rule

Flag application behavior that:

- logs passwords
- returns passwords
- stores plaintext passwords unnecessarily
- transmits passwords insecurely
- copies passwords into unnecessary variables or payloads

## Severity

CRITICAL

---

# SEC-041 — Sensitive Data Stored in Object Store

## Rule

Flag sensitive credentials, tokens, or highly sensitive information
stored in Object Store without appropriate protection when repository
evidence indicates unauthorized access could expose the data.

## Severity

HIGH

---

# SEC-042 — Sensitive Data Stored in Persistent Messaging

## Rule

Flag unnecessary inclusion of secrets or highly sensitive data in
persistent messages, queues, or dead-letter queues.

Consider:

- credentials
- tokens
- authorization headers
- personal information
- financial information

## Severity

HIGH

---

# SEC-043 — Secret Exposure Through Dead-Letter Handling

## Rule

Flag messaging error handling where failed messages containing secrets
or sensitive information are persisted or exposed through dead-letter
mechanisms without appropriate protection.

## Severity

HIGH

---

# SEC-044 — Sensitive Data in Debug Logging

## Rule

Flag debug or trace logging that exposes sensitive data even when normal
production logging does not.

Consider:

- payload logging
- attributes
- headers
- variables
- connector responses
- error objects

## Severity

HIGH

---

# SEC-045 — Security Control Bypassed in Error Path

## Rule

Flag error or fallback paths that bypass security controls enforced on
the normal processing path.

Examples:

- authorization performed only on success path
- fallback endpoint without authentication
- error route exposing protected information
- alternate flow bypassing validation

## Severity

CRITICAL

---

# SEC-046 — Security Control Bypassed in Alternate Flow

## Rule

Flag alternate processing paths, retry flows, batch flows, scheduled
flows, or administrative flows that access protected resources without
the security controls applied to the primary flow.

## Severity

HIGH

---

# SEC-047 — Insecure Administrative Endpoint

## Rule

Flag administrative, diagnostic, health, replay, retry, or operational
endpoints that expose sensitive capabilities without appropriate access
controls.

## Severity

CRITICAL

---

# SEC-048 — Dependency Security Risk

## Rule

Flag dependencies or plugins with known security vulnerabilities when:

1. the vulnerable dependency is actually used or materially present,
2. the vulnerability is relevant to the application,
3. repository evidence supports the finding.

## Severity

HIGH

Escalate according to actual exploitability and impact.

Do not report a dependency merely because a newer version exists.

---

# SEC-049 — Insecure Deployment Configuration

## Rule

Flag deployment configuration that exposes or weakens security controls.

Consider:

- plaintext secrets
- insecure environment variables
- exposed management endpoints
- insecure TLS configuration
- excessive runtime permissions
- publicly exposed internal services

## Severity

HIGH

---

# SEC-050 — Security-Sensitive Configuration Exposed

## Rule

Flag source-controlled configuration containing sensitive security
configuration that should not be publicly or broadly accessible.

Examples:

- truststore passwords
- keystore passwords
- encryption configuration
- privileged endpoints
- service account configuration

## Severity

HIGH

---

# Security Finding Validation

Before reporting a security finding:

1. Identify the protected asset or operation.
2. Identify the source of the sensitive value or permission.
3. Trace where it is used.
4. Inspect related Mule XML.
5. Inspect DataWeave if applicable.
6. Inspect properties and secure properties.
7. Inspect API specifications.
8. Inspect global configurations.
9. Inspect error handling and logging.
10. Determine whether an existing security control already mitigates it.
11. Determine exploitability or realistic exposure.
12. Determine business impact.
13. Assign severity.

If the finding cannot be substantiated, do not report it.

---

# Security Severity Guidance

## CRITICAL

Use for issues such as:

- exposed production credentials
- exposed private keys
- access tokens
- authorization bypass
- tenant isolation failure
- credential disclosure
- severe injection vulnerabilities
- security controls completely bypassed
- severe unauthorized access

## HIGH

Use for:

- sensitive information exposure
- missing authentication
- meaningful authorization weaknesses
- insecure transport
- SSRF
- unsafe file access
- security-relevant input validation problems
- significant dependency vulnerabilities

## MEDIUM

Use for:

- limited security hardening issues
- operational security weaknesses
- moderate information exposure
- abuse protection gaps where impact is limited

## LOW

Use only for minor security improvements with limited practical impact.

## NIT

Do not report security NITs unless they provide meaningful security value.

---

# Security False-Positive Controls

Do not report as real secrets without evidence:

- `password`
- `client-secret`
- `api-key`
- `token`
- `username`

when they are clearly:

- placeholders
- examples
- test-only dummy values
- environment variable references
- secure-property references

Examples such as:

```text
${secure::client.secret}
${api.key}
${env.CLIENT_SECRET}