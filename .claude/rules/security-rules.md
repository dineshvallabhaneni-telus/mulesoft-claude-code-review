# MuleSoft Security Review Rules

## Purpose

Define the mandatory security review rules for the MuleSoft architecture and standards review.

The security review must identify genuine security risks without exposing sensitive information in the generated report.

---

## 1. Security Review Objectives

Review the MuleSoft application for:

- Credential protection
- Secret management
- Password protection
- Secure configuration
- API security
- Authentication
- Authorization
- TLS/HTTPS
- Sensitive data protection
- Logging security
- Error-response security
- Dependency security
- Secure coding practices
- Configuration security
- External security-control dependencies

The review must consider both implementation security and operational security.

---

## 2. Credentials and Secrets

Search the complete in-scope application for potential secrets, including:

- Passwords
- API keys
- Client IDs
- Client secrets
- Access tokens
- Refresh tokens
- JWT secrets
- Encryption keys
- Private keys
- Certificates
- Database credentials
- SMTP credentials
- Cloud credentials
- OAuth credentials
- Authentication headers
- Connection strings containing credentials

Potential secret locations include:

- `.properties`
- `.yaml`
- `.yml`
- `.json`
- Mule XML
- DataWeave
- Java
- Python
- Configuration files
- POM configuration
- Test resources
- MUnit configuration

---

## 3. Password Protection

All application passwords must be securely protected.

Plain-text passwords must be reported.

Passwords must use the appropriate MuleSoft Secure Configuration Properties mechanism or an approved external secret-management solution where applicable.

Do not consider the following sufficient protection by themselves:

- Base64 encoding
- URL encoding
- Obfuscation
- String concatenation
- Variable indirection
- Splitting a password across multiple properties
- Storing a password in a non-obvious property name

These do not constitute encryption.

---

## 4. Secure Configuration Properties

Where MuleSoft Secure Configuration Properties are used, verify:

- Secure configuration is actually enabled.
- Sensitive properties are stored in the secure configuration mechanism.
- Sensitive values are not duplicated in plain-text configuration.
- The correct secure property syntax is used.
- Sensitive values are not logged.
- Secure property files are appropriately protected.
- Encryption/decryption configuration is appropriate.
- The encryption key is not exposed in source code.

If the repository does not provide sufficient evidence to validate the runtime secret-management configuration, report:

`Verification Required`

rather than claiming the implementation is insecure.

---

## 5. Secret Exposure in Source

Report confirmed secrets committed to source control.

Examples include:

- `password=ActualPassword`
- `client.secret=ActualSecret`
- `api.key=ActualKey`
- Hardcoded authorization tokens
- Hardcoded private keys

Never include the actual value in the report.

Use wording such as:

`A credential appears to be hardcoded in <file> under <property/configuration>.`

Do not reproduce the secret.

---

## 6. Secret Exposure in Logs

Check whether application logging can expose:

- Passwords
- Tokens
- Authorization headers
- API keys
- Client secrets
- Session information
- Sensitive request fields
- Sensitive response fields
- Personal information

Report confirmed exposure risks.

Also review whether payload logging may indirectly expose secrets.

---

## 7. Sensitive Data in Error Responses

Review error handling for accidental exposure of:

- Stack traces
- Internal class names
- Database details
- Credentials
- Tokens
- Internal URLs
- Connection strings
- Infrastructure information
- Sensitive payload data

External/API-facing errors should expose only information appropriate for the consumer.

Internal diagnostic details should remain in controlled logs.

---

## 8. API Authentication

For exposed APIs, determine whether appropriate authentication is implemented.

Consider applicable mechanisms such as:

- OAuth 2.0
- Client ID / Client Secret
- JWT
- Mutual TLS
- Basic authentication where justified
- Other enterprise-approved authentication mechanisms

Do not require one authentication mechanism for every API.

The recommendation must match the API's use case and security requirements.

---

## 9. API Authorization

Authentication alone is not authorization.

Where applicable, review whether the application or platform enforces:

- Role-based access
- Scope-based access
- Permission checks
- Resource-level authorization
- Consumer authorization
- Appropriate policy enforcement

Identify cases where an authenticated consumer may access resources without adequate authorization controls.

---

## 10. API Manager Policies

API security policies may be managed outside the source repository.

Potential controls include:

- Client ID enforcement
- OAuth policies
- JWT validation
- Rate limiting
- SLA policies
- Throttling
- IP restrictions
- CORS
- Security headers
- Mutual TLS

Do not report these controls as missing solely because they are not visible in source code.

Classify them as:

- Confirmed
- Not evident
- Verification Required

based on available evidence.

---

## 11. HTTPS and TLS

Review outbound and inbound integrations for secure transport.

Look for:

- HTTP endpoints carrying sensitive data
- HTTPS endpoints
- TLS configuration
- TLS versions where visible
- Certificate configuration
- Truststores
- Keystores
- Mutual TLS
- Certificate validation

Report confirmed insecure transport where sensitive data is transmitted without appropriate protection.

Do not assume an endpoint is insecure merely because TLS configuration is managed externally.

---

## 12. Certificate and Key Management

Review:

- Keystores
- Truststores
- Certificates
- Private keys
- Certificate paths
- Password protection
- Hardcoded key material

Private keys must never be committed as plain-text source artifacts.

Do not reproduce certificate/private-key contents in the report.

---

## 13. Authentication Headers

Check for hardcoded or improperly managed headers such as:

- `Authorization`
- `X-API-Key`
- `Client-Secret`
- Custom authentication headers

Determine whether values are:

- Securely configured
- Dynamically obtained
- Properly encrypted
- Hardcoded
- Logged

Hardcoded authentication credentials must be reported.

---

## 14. Dependency Security

Review `pom.xml` for security-relevant dependencies.

Consider:

- Known outdated dependencies
- Suspicious dependencies
- Unnecessary dependencies
- Duplicate dependencies
- Multiple versions of the same dependency
- Vulnerable libraries where reliable evidence is available

Do not claim a dependency has a known vulnerability unless reliable vulnerability information is available.

If vulnerability verification cannot be performed, report the need for dependency scanning rather than inventing a vulnerability.

---

## 15. Custom Code Security

Review Java, Python, scripting, and custom modules for:

- Hardcoded credentials
- Unsafe input handling
- Command execution
- File-system access
- Unsafe deserialization
- SQL injection risk
- Header injection
- Path traversal
- Sensitive information exposure
- Weak cryptographic practices
- Unnecessary privileged operations

Determine whether MuleSoft-native capabilities can provide a safer implementation.

---

## 16. Input Validation

Review externally supplied input for appropriate validation.

Consider:

- Query parameters
- URI parameters
- Headers
- Request bodies
- File uploads
- User-controlled values
- Dynamic URLs
- Dynamic database queries
- Dynamic expressions

Identify cases where untrusted input directly controls sensitive operations.

Do not recommend excessive validation that prevents legitimate API behavior.

---

## 17. SQL and Database Security

Where database queries exist, review for:

- SQL injection
- Dynamic query construction
- Parameterization
- Hardcoded credentials
- Excessive privileges where inferable
- Sensitive data exposure
- Unsafe error handling

Prefer parameterized queries where supported.

Do not report SQL injection merely because a query contains dynamic values; inspect how those values are incorporated.

---

## 18. Dynamic URL and Endpoint Security

Review dynamically constructed URLs and endpoints.

Identify risks such as:

- User-controlled hostnames
- User-controlled paths
- SSRF-like behavior
- Unvalidated redirect targets
- Sensitive endpoint exposure

Determine whether endpoint values are trusted and appropriately controlled.

---

## 19. File Handling

Where the application reads or writes files, review:

- Path construction
- User-controlled filenames
- Directory traversal
- Sensitive file exposure
- Temporary file handling
- File permissions where visible
- Credential-containing files

Do not report theoretical path traversal without evidence that untrusted input can influence the path.

---

## 20. XML Security

Review XML processing where applicable.

Consider:

- External entity processing
- Unsafe XML parsing
- XML injection
- Excessive XML payloads
- Untrusted XML content

Only report risks supported by the actual implementation or dependency behavior.

---

## 21. Data Protection

Review handling of sensitive data such as:

- Personally identifiable information
- Financial data
- Authentication information
- Customer data
- Confidential business information

Consider:

- Logging
- Transformation
- Storage
- Transmission
- Error handling
- Temporary storage

The report must identify unnecessary exposure and recommend minimizing sensitive-data handling.

---

## 22. Logging Security

Logging must not expose sensitive information.

Pay particular attention to:

- Full payload logging
- Authorization headers
- Password fields
- Tokens
- API keys
- Client secrets
- Personal information
- Database credentials

If sensitive logging is required for troubleshooting, recommend controlled masking/redaction rather than unrestricted logging.

---

## 23. Secure Error Handling

Errors must not expose internal implementation details to external consumers.

Review:

- Error descriptions
- Error payloads
- HTTP responses
- Exception messages
- Stack traces
- Database errors
- Connector errors

Recommend standardized consumer-safe error responses where appropriate.

---

## 24. Environment Security

Review DEV, QA, UAT, PROD, and other available environment configurations.

Check whether:

- Production secrets are stored securely.
- Environment-specific credentials are separated.
- Non-production credentials are not reused unnecessarily.
- Sensitive values are not committed in plain text.
- Environment configuration follows a consistent secure pattern.

Do not assume identical values across environments are required.

---

## 25. Security Finding Severity

Use the following general guidance:

### Critical

Use only for severe confirmed security exposure.

Examples:

- Production private key committed to source
- Active production credential exposed
- Confirmed authentication bypass with major impact

### High

Examples:

- Plain-text production password
- Significant API authentication weakness
- Sensitive data exposure
- Critical security configuration weakness

### Medium

Examples:

- Weak secret-management implementation
- Sensitive information in logs
- Missing important security validation
- Significant dependency/security configuration concern

### Low

Examples:

- Minor security hardening opportunity
- Non-critical security configuration improvement

### Warning

Use when security cannot be verified from repository evidence.

---

## 26. Credential Rotation

If an actual credential or secret appears to have been committed to source control:

1. Report the exposure.
2. Do not reproduce the credential.
3. Recommend immediate credential rotation.
4. Recommend removing the secret from source control.
5. Recommend using secure configuration/secret management.
6. Consider historical Git exposure where appropriate.

Do not assume that deleting the secret from the latest commit makes the credential safe.

---

## 27. No Secret Reproduction

This rule is mandatory.

Never output actual:

- Passwords
- Tokens
- API keys
- Client secrets
- Private keys
- Encryption keys
- Certificates containing sensitive private material

into:

- `summary.txt`
- Word report
- Console output
- Finding details
- Claude response
- Generated documentation

Use redacted descriptions instead.

---

## 28. Security Finding Quality Gate

Before finalizing a security finding, verify:

- Is the issue supported by repository evidence?
- Is the issue actually exploitable or materially risky?
- Is the severity appropriate?
- Could the control be managed externally?
- Have secrets been excluded from the finding?
- Is the impact explained?
- Is the remediation practical?
- Is credential rotation required?
- Is the finding duplicated elsewhere?

If these questions cannot be answered, classify the issue as `Verification Required` or remove it.

---

## 29. Security Review Completion Criteria

Before completing the security review, verify that the following have been considered:

- Passwords
- Secure properties
- API keys
- Client secrets
- Tokens
- Private keys
- Certificates
- Authentication
- Authorization
- API policies
- TLS
- Logging
- Error handling
- Sensitive data
- Custom code
- Dependencies
- Database access
- File access
- Dynamic endpoints
- Environment configuration

The security review is complete only after these areas have been evaluated against the actual application implementation.