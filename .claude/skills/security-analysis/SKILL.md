# MuleSoft Security Analysis Skill

## Purpose

Perform a comprehensive application-level security review of the complete MuleSoft application.

Review the application as a:

- Senior MuleSoft Security Architect
- Enterprise Security Architect
- Senior MuleSoft Architect
- Senior Technical Lead

The objective is to identify meaningful security weaknesses across application code, configuration, dependencies, credentials, secrets, data handling, cryptography, logging, custom code, and integration behavior.

The review must be evidence-based.

Every meaningful security finding MUST include:

- Evidence
- Security impact
- Severity
- Practical remediation
- Recommended solution

Do not create findings simply because a generic security best practice is not explicitly visible.

---

# 1. Repository Scope

The MuleSoft application is:

${GITHUB_WORKSPACE}

The code-review framework is:

${GITHUB_WORKSPACE}/code-review

The reports directory is:

${GITHUB_WORKSPACE}/reports

Review the complete MuleSoft application.

---

# 2. Mandatory Exclusions

Do NOT review these directories as MuleSoft application source:

${GITHUB_WORKSPACE}/code-review/**
${GITHUB_WORKSPACE}/reports/**

Do not report findings against:

- Review agents
- Skills
- Prompt files
- Framework scripts
- Generated reports

---

# 3. Security Review Scope

The review MUST consider:

- Credentials
- Passwords
- Secrets
- API keys
- Tokens
- Secure properties
- Encryption
- TLS
- Certificates
- Sensitive data
- Logging
- Error handling
- Input handling
- Output handling
- Dependencies
- Custom Java
- Custom Python
- File access
- Database access
- External integrations
- Configuration
- Environment properties
- Mule application metadata

API-specific security is primarily owned by:

api-security-analysis

Connector-specific security is primarily owned by:

connector-analysis

Avoid duplicate findings while still reporting security implications.

---

# 4. Security Principles

Apply these principles:

- Least privilege
- Defense in depth
- Secure by default
- No plaintext secrets
- Explicit trust boundaries
- Strong authentication
- Appropriate authorization
- Encryption in transit
- Encryption at rest where applicable
- Minimal sensitive data exposure
- Secure error handling
- Secure logging
- Input validation
- Safe output handling
- Dependency hygiene

Do not apply a principle mechanically when the implementation does not require it.

---

# 5. Secret Discovery

Search the complete application for potential secrets including:

- Passwords
- API keys
- Client secrets
- Access tokens
- Refresh tokens
- Private keys
- Connection strings
- Database credentials
- SSH credentials
- Certificates containing private material
- Authentication headers
- Embedded credentials

Inspect:

- XML
- DataWeave
- Java
- Python
- Properties
- YAML
- YML
- JSON
- RAML
- OAS
- Maven configuration
- mule-artifact.json

---

# 6. Secret Detection

Look for patterns such as:

- password=
- passwd=
- secret=
- client_secret=
- api_key=
- apikey=
- token=
- access_token=
- private_key=
- authorization=
- bearer
- username/password combinations

Do not treat every occurrence of these words as a confirmed secret.

Verify the surrounding context.

---

# 7. Secret Redaction

NEVER include actual secret values in the report.

If evidence contains a secret, replace it with:

[REDACTED]

Do not place secrets into:

- summary.txt
- Word document
- console output
- generated charts
- temporary report files

---

# 8. Password Security

All passwords must be securely protected.

Evaluate whether passwords are:

- Plaintext
- Encoded only
- Encrypted
- Stored in secure properties
- Referenced through secure configuration

Base64 encoding is NOT encryption.

Do not classify an encrypted secure property as plaintext simply because the encrypted value is visible.

---

# 9. MuleSoft Secure Properties

Determine whether MuleSoft secure properties are used appropriately.

Inspect:

- Secure configuration properties.
- Secure property placeholders.
- mule-artifact.json.
- Property files.
- YAML/YML configuration.

Verify that sensitive values are protected.

If the repository references encrypted properties but the decryption key is external:

Do not claim the key is missing.

---

# 10. Encryption Requirements

Sensitive credentials must be encrypted/protected.

Evaluate:

- Passwords
- API secrets
- Client secrets
- Sensitive tokens
- Private key material
- Other credentials

Report plaintext sensitive values as security findings.

Do not require encryption for non-sensitive configuration.

---

# 11. Encryption vs Encoding

Distinguish:

- Encryption
- Hashing
- Encoding
- Obfuscation

Do not treat:

- Base64
- URL encoding
- Hex encoding

as encryption.

---

# 12. Cryptographic Practices

Where cryptography is implemented, review:

- Algorithm choice
- Key handling
- Key storage
- Initialization vectors where applicable
- Password hashing
- Randomness
- Certificate validation

Do not recommend specific algorithms without understanding the use case.

Avoid recommending custom cryptography when MuleSoft/platform capabilities can provide the required security.

---

# 13. TLS

Review application-visible TLS configuration.

Consider:

- HTTPS
- TLS contexts
- Truststores
- Keystores
- Certificate configuration
- Mutual TLS
- Secure outbound integrations

Do not claim infrastructure-level TLS is missing if TLS termination may happen outside the repository.

Use:

Verification Required

when appropriate.

---

# 14. Certificate Handling

Review:

- Certificate files
- Truststores
- Keystores
- Certificate references
- Password protection

Look for:

- Private keys committed to source control.
- Insecure certificate validation.
- Disabled verification.
- Trust-all configurations.

Do not report a certificate as expired unless expiration can be established from available evidence.

---

# 15. Trust-All Configuration

Look for configurations that:

- Trust all certificates.
- Disable hostname verification.
- Disable certificate validation.
- Bypass TLS validation.

These are potentially serious findings.

Severity depends on:

- Environment.
- Endpoint.
- Data sensitivity.
- Exposure.

Provide a practical secure TLS configuration recommendation.

---

# 16. Authentication Credentials

Review authentication mechanisms used throughout the application.

Examples:

- Basic authentication
- OAuth
- Client credentials
- API keys
- Username/password
- SSH keys
- Database credentials
- Mutual TLS

Evaluate credential storage and handling.

Do not report authentication mechanism choice as a vulnerability without evidence.

---

# 17. Authorization

Review application-level authorization where visible.

Consider:

- Roles
- Scopes
- Permissions
- Resource ownership
- Tenant boundaries
- Administrative operations

API-specific authorization is owned by:

api-security-analysis

Do not duplicate detailed API findings unnecessarily.

---

# 18. Least Privilege

Evaluate whether integrations appear to use excessive privileges where evidence exists.

Examples:

- Database user with broad privileges.
- Administrative API credentials for normal operations.
- Excessive filesystem access.

Do not infer privileges that cannot be established from repository evidence.

If actual external privileges cannot be inspected:

Verification Required

---

# 19. Sensitive Data Identification

Identify sensitive information handled by the application.

Examples:

- PII
- Financial data
- Credentials
- Authentication tokens
- Customer information
- Employee information
- Health-related information
- Confidential business information

Do not assume data classification without evidence.

---

# 20. Sensitive Data in Logs

Check whether sensitive information may be logged.

Look for:

- Passwords
- Tokens
- Authorization headers
- API keys
- Full payloads containing sensitive data
- Personal information
- Financial information

Do not reproduce sensitive values.

Detailed logging review belongs to:

logging-analysis

---

# 21. Sensitive Data in Errors

Review whether error handling may expose:

- Stack traces
- Credentials
- SQL
- Internal hostnames
- File paths
- Tokens
- Payloads
- Internal implementation details

Recommend standardized safe error responses.

---

# 22. Sensitive Data in Responses

Evaluate whether application responses expose unnecessary:

- Internal fields
- Credentials
- Tokens
- Database information
- Internal identifiers
- Technical details

API-specific response security belongs to:

api-security-analysis

---

# 23. Data Transformation Security

Review DataWeave and transformations for:

- Accidental secret propagation.
- Sensitive field exposure.
- Unnecessary copying of sensitive data.
- Unsafe dynamic evaluation.
- Data leakage.

Do not report ordinary transformations as security problems.

---

# 24. Input Validation

Review application inputs for:

- Unsafe assumptions.
- Missing validation.
- Unexpected types.
- Unbounded data.
- Injection opportunities.

Consider inputs from:

- HTTP
- Files
- Databases
- Messaging
- External APIs
- Properties

API-specific validation belongs to:

api-security-analysis

---

# 25. Injection Security

Review for:

- SQL injection
- Command injection
- Expression injection
- XPath injection
- XML injection
- LDAP injection
- Script injection

Only report confirmed or credible risks.

Do not report theoretical injection solely because user input exists.

---

# 26. Database Security

Where database access exists, review:

- Credential protection.
- SQL construction.
- Parameterization.
- Dynamic queries.
- Sensitive data handling.
- Excessive privileges where visible.

Do not duplicate connector configuration findings from connector-analysis.

---

# 27. File Security

Review file operations for:

- Path traversal.
- Unsafe dynamic paths.
- Untrusted filenames.
- Sensitive file access.
- Temporary file handling.
- File permissions where visible.

Only report credible risks supported by implementation.

---

# 28. Path Traversal

Look for externally controlled values used to construct file paths.

Potentially dangerous patterns include:

- User-controlled filenames.
- Dynamic directory traversal.
- Relative path manipulation.

Recommend:

- Input validation.
- Canonicalization.
- Allowlisting.
- Controlled directories.

Do not report a finding if the path is demonstrably fixed and trusted.

---

# 29. Command Execution

Identify:

- Shell commands
- OS commands
- Java Runtime execution
- Process execution
- Script invocation

Determine whether untrusted input can influence commands.

Custom code must be reviewed carefully.

---

# 30. Custom Java Security

Review Java code for:

- Hard-coded credentials.
- Unsafe deserialization.
- Command execution.
- Dynamic class loading.
- Insecure cryptography.
- Unsafe file operations.
- Sensitive logging.
- Network security bypass.

Do not report custom Java merely because it exists.

---

# 31. Custom Python Security

If Python is used, review:

- Credential handling.
- Command execution.
- Input handling.
- File access.
- Dependency usage.
- Sensitive logging.

Do not assume Python itself is insecure.

---

# 32. Dependency Security

Review:

- pom.xml
- Third-party libraries
- Mule modules
- Connector versions

Look for:

- Known vulnerable dependencies where evidence is available.
- Suspicious or unnecessary dependencies.
- Duplicate libraries.
- Unmaintained custom dependencies where evidence supports concern.

Do not claim a CVE without reliable evidence.

If current vulnerability status cannot be established from repository data:

Verification Required

---

# 33. Maven Repository Security

Review dependency repositories for:

- HTTP repositories.
- Untrusted repositories.
- Unnecessary repositories.
- Credentials embedded in configuration.

Prefer secure repository access.

Do not report a repository as malicious without evidence.

---

# 34. Environment Configuration

Review environment-specific configuration for:

- Secrets.
- Credentials.
- Sensitive endpoints.
- Insecure defaults.

Files may include:

- dev.properties
- qa.properties
- uat.properties
- prod.properties
- dev.yaml
- qa.yaml
- uat.yaml
- prod.yaml
- Other environment configuration

Do not assume environment names follow a specific convention.

---

# 35. Configuration Drift

Compare security-relevant configuration across environments.

Look for:

- DEV secured but PROD insecure.
- QA using different authentication.
- PROD missing required secure properties.
- Different TLS settings.
- Different credential mechanisms.

Do not report ordinary environment-specific values as security problems.

---

# 36. Secure Defaults

Evaluate whether default configuration is secure.

Examples:

- Debug enabled.
- Excessive logging.
- Development credentials.
- Insecure protocol.
- Disabled validation.

Do not report development-only settings as production vulnerabilities unless they can affect production.

---

# 37. Debug Configuration

Look for:

- Debug logging.
- Development endpoints.
- API consoles.
- Test endpoints.
- Mock integrations.
- Temporary bypasses.

Determine whether production exposure is possible.

---

# 38. API Console / Documentation Exposure

Where API consoles or documentation endpoints exist, determine whether they expose sensitive implementation information.

Do not automatically classify API documentation as a vulnerability.

Consider whether the endpoint is intended for:

- Development
- Internal users
- Public consumers

---

# 39. CORS Security

Where CORS is configured, evaluate:

- Wildcard origins.
- Credentials.
- Allowed methods.
- Allowed headers.

API-specific CORS findings belong primarily to:

api-security-analysis

Avoid duplicate findings.

---

# 40. Security Headers

Where application-level HTTP responses are controlled, consider relevant security headers.

Do not require browser security headers for non-browser APIs without justification.

---

# 41. Session and Token Security

Where sessions or tokens exist, evaluate:

- Storage.
- Propagation.
- Logging.
- Exposure.
- Expiration handling.
- Validation.

Do not assume a specific token mechanism without evidence.

---

# 42. Replay and Idempotency Security

For sensitive state-changing operations, consider:

- Duplicate requests.
- Replay.
- Idempotency.
- Request identifiers.

Do not require idempotency for every API or integration.

---

# 43. Logging Security

Review whether logs could expose sensitive information.

Consider:

- Credentials.
- Tokens.
- Personal information.
- Financial information.
- Full payloads.

Detailed logging findings belong to:

logging-analysis

---

# 44. Error Handling Security

Review whether errors expose internal implementation details.

Look for:

- Stack traces.
- Java exception details.
- SQL exceptions.
- Internal URLs.
- File paths.
- Connector credentials.

Recommend safe external error responses while preserving useful internal diagnostics.

---

# 45. Secure Property File Consistency

Verify that sensitive configuration uses the appropriate secure-property mechanism consistently across environments.

If:

DEV → secure

QA → plaintext

UAT → secure

PROD → secure

the QA inconsistency should be reported.

---

# 46. Secrets in Version Control

If secrets are found in tracked application files:

- Report the exposure.
- Redact the value.
- Recommend removing the secret.
- Recommend secure property management.
- Recommend rotating the exposed credential.

Do not assume that deleting the value from the current branch removes it from Git history.

Where history cannot be inspected, state:

"Credential rotation and Git-history remediation should be considered because the current repository review does not establish whether the value existed in prior commits."

---

# 47. Credential Rotation

When a real credential is exposed, recommend:

1. Immediate credential rotation.
2. Removal from source.
3. Secure property replacement.
4. Review of Git history.
5. Audit of systems accessed by the credential.

Never attempt to use discovered credentials.

---

# 48. Secret Scanning False Positives

Avoid reporting:

- Example placeholders.
- Documentation examples.
- Clearly fake credentials.
- Test values that are demonstrably non-sensitive.

If uncertain:

Verification Required

---

# 49. Security Architecture

Evaluate security boundaries such as:

Client
→ API Gateway
→ Mule Application
→ External Systems

Consider:

- Authentication.
- Authorization.
- Encryption.
- Secrets.
- Sensitive data.

Do not invent infrastructure components.

---

# 50. Security Findings

Every security finding MUST contain:

## Finding ID

Example:

MULE-SEC-001

## Title

Concise security issue.

## Severity

Critical / High / Medium / Low / Warning

## Category

Security

## Location

Exact file/configuration/flow.

## Evidence

Observed implementation.

## Risk

Potential security impact.

## Recommendation

What should change.

## Solution

Practical remediation steps.

## Priority

Immediate / Short Term / Medium Term / Long Term

---

# 51. Severity Guidelines

## Critical

Confirmed severe vulnerability with significant security or business impact.

Examples:

- Exposed production credential.
- Critical authentication bypass.
- Remote code execution.
- Severe unauthorized access to sensitive data.

## High

Significant exploitable security weakness.

## Medium

Meaningful security weakness requiring remediation.

## Low

Minor security improvement.

## Warning

Control cannot be established from repository evidence.

Do not inflate severity.

---

# 52. Security Finding Evidence

Evidence should contain:

- File.
- Configuration/flow.
- Relevant implementation detail.

Never include:

- Password values.
- API keys.
- Tokens.
- Private key material.

Redact them.

---

# 53. Security Solutions

Solutions must be actionable.

Bad:

"Encrypt the password."

Good:

"Move the database password into the MuleSoft secure properties mechanism, reference the encrypted property from the global Database Configuration, remove the plaintext value from the application configuration, and rotate the previously exposed credential."

---

# 54. Positive Security Observations

Identify meaningful security strengths such as:

- Secure properties.
- Proper TLS.
- Strong authentication.
- Good authorization.
- No secrets in source.
- Safe error handling.
- Appropriate input validation.
- Secure connector configuration.

The final report must be balanced.

---

# 55. Security Assessment

Provide structured output containing:

## Security Summary

## Secret Management Assessment

## Password Protection Assessment

## Encryption Assessment

## TLS Assessment

## Authentication Assessment

## Authorization Assessment

## Sensitive Data Assessment

## Input Security Assessment

## Dependency Security Assessment

## Custom Code Security Assessment

## Configuration Security Assessment

## Positive Security Observations

## Security Findings

## Immediate Security Actions

## Verification Required

## Security Score

---

# 56. Cross-Skill Boundaries

Detailed findings owned by these skills should not be duplicated unnecessarily:

- mulesoft-architecture
- mule-code-quality
- connector-analysis
- api-security-analysis
- performance-analysis
- munit-analysis
- configuration-analysis
- logging-analysis
- duplication-analysis

This skill owns application-wide security concerns.

API-specific security belongs primarily to:

api-security-analysis

Connector-specific security belongs primarily to:

connector-analysis

The final report reviewer must consolidate duplicate root causes.

---

# 57. No Unsupported Claims

Never claim:

- A WAF is missing.
- API Manager policy is missing.
- Infrastructure TLS is missing.
- Network segmentation is missing.
- A dependency has a CVE.
- A certificate is expired.

unless the available evidence supports the statement.

Use:

Verification Required

when external verification is necessary.

---

# 58. No Secret Exposure

Under no circumstances should this skill:

- Print discovered secrets.
- Copy credentials into reports.
- Include tokens in examples.
- Include private keys in findings.
- Store secrets in generated artifacts.

Always redact sensitive values.

---

# 59. Final Output

Return structured security analysis for consumption by the report-generation process.

Do not generate the final Word document from this skill.

The word-report-generation skill is responsible for creating:

${GITHUB_WORKSPACE}/reports/mulesoft-standards-review_<timestamp>.docx

---

# 60. Quality Standard

Before completing the review, ask:

"Would an Enterprise Security Architect trust this assessment as a production security review?"

If not:

- Remove theoretical findings.
- Re-check evidence.
- Separate confirmed issues from verification requirements.
- Ensure every finding has a practical solution.
- Redact all sensitive information.
- Consolidate duplicates.
- Prioritize exploitable and business-relevant risks.

The objective is a credible security assessment, not a generic security checklist.