# File: standards/configuration/configuration-standards.md

# MuleSoft Configuration Standards

## 1. Purpose

This document defines standards for reviewing configuration in MuleSoft applications.

The review must determine whether application configuration is:

- Correct
- Secure
- Environment-independent
- Maintainable
- Consistent
- Externalized appropriately
- Safe for deployment
- Free from exposed secrets
- Easy to understand and operate

The review must inspect configuration across:

- Mule XML files
- `.properties` files
- `.yaml` files
- `.yml` files
- Secure properties
- Maven configuration
- Runtime configuration
- Connector configuration
- Environment-specific configuration

Do not report a configuration difference as a defect simply because another configuration approach exists.

---

## 2. Configuration Principles

Configuration should be separated from application logic when the value:

- Changes between environments
- Contains deployment-specific information
- Contains credentials
- Controls operational behavior
- Is expected to be changed without modifying application code

Examples include:

- URLs
- Hosts
- Ports
- Credentials
- Database names
- Queue names
- Timeouts
- Retry counts
- File paths
- Feature flags

---

## 3. Environment Separation

The same application artifact should be deployable to different environments without modifying application logic.

Typical environments may include:

- Development
- Test
- QA
- UAT
- Production

Environment-specific values should be supplied through configuration.

Avoid patterns where developers must edit Mule XML before every deployment.

---

## 4. Property Files

Properties should be stored in appropriate configuration files.

Examples:

- `application.properties`
- `application-dev.properties`
- `application-test.properties`
- `application-prod.properties`

The exact naming convention may vary by project.

The important requirement is that environment-specific configuration remains separate from application logic.

---

## 5. YAML Configuration

YAML configuration may be used where appropriate.

Review:

- `.yaml`
- `.yml`

Ensure that YAML configuration follows the same security and environment-separation requirements as properties files.

Do not assume YAML configuration is automatically secure because it is not part of the Mule XML.

---

## 6. Configuration Hierarchy

Configuration should have a predictable precedence model.

Review whether developers can clearly determine which value is used when multiple configuration sources exist.

Avoid ambiguous configurations where:

- The same property appears in multiple files.
- Environment variables override values unexpectedly.
- Secure and non-secure properties use the same key.
- Deployment-specific values are difficult to identify.

---

## 7. Property Naming

Configuration properties should use descriptive and consistent names.

Prefer:

    customer.api.base-url
    customer.api.timeout
    customer.api.client-id

over:

    url1
    timeout1
    value
    config

---

## 8. URL Configuration

External service URLs should normally be externalized.

Examples:

    customer.api.url
    payment.api.url
    crm.api.url

Avoid hard-coded environment-specific URLs inside Mule flows.

---

## 9. Host and Port Configuration

Hosts and ports that differ by environment should be configurable.

Avoid hard-coded values such as:

    localhost
    dev-server
    qa-server
    production-host

unless they are intentionally fixed by the application design.

---

## 10. Credentials

Credentials must never be stored directly in source-controlled application configuration.

This includes:

- Passwords
- API keys
- Client secrets
- Access tokens
- Refresh tokens
- Private keys
- Database passwords

Use secure configuration mechanisms or approved secret-management systems.

---

## 11. Secure Properties

Sensitive properties should use MuleSoft secure properties or an approved external secret-management mechanism.

Review:

- Encryption
- Key management
- Property references
- Deployment configuration
- Plain-text duplicates

Do not consider a property secure merely because the property name contains words such as `password` or `secret`.

---

## 12. Encryption Keys

Encryption keys must not be committed alongside encrypted configuration when doing so would allow unauthorized decryption.

Review how encryption keys are supplied during deployment.

Avoid hard-coded encryption keys.

---

## 13. Plain-Text Secret Detection

Search all configuration files for possible secrets.

Examples:

- `password=`
- `client_secret=`
- `clientSecret=`
- `apiKey=`
- `token=`
- `access_token=`
- `privateKey=`

A property name alone is not proof of a secret.

The reviewer must inspect the actual value and context.

---

## 14. Duplicate Secrets

Check for secrets duplicated across:

- Mule XML
- Properties
- YAML
- Maven files
- CI/CD configuration
- Test configuration
- Documentation

A secret should have a single controlled source wherever practical.

---

## 15. Test Credentials

Test credentials must not accidentally be used by production configuration.

Review:

- Test property files
- Local configuration
- MUnit configuration
- Maven profiles
- Deployment profiles

Ensure environment selection is explicit and predictable.

---

## 16. Default Values

Default values should be used carefully.

A default value is acceptable when:

- It is safe
- It is environment-independent
- It does not expose a secret
- It does not create insecure behavior

Do not provide insecure defaults for security-sensitive settings.

---

## 17. Security-Sensitive Defaults

Avoid defaults such as:

    password=admin
    username=admin
    tls.enabled=false
    authentication.enabled=false

unless they are strictly isolated to a controlled test environment and cannot affect production.

---

## 18. Timeout Configuration

Timeouts should be configurable where operational requirements differ between environments.

Review:

- HTTP timeout
- Connection timeout
- Database timeout
- Response timeout
- Messaging timeout

Avoid arbitrary large timeout values.

---

## 19. Retry Configuration

Retry values should be configurable when operational requirements differ.

Review:

- Maximum retries
- Retry interval
- Backoff
- Reconnection attempts

Avoid unlimited retries.

---

## 20. Feature Flags

Feature flags should have:

- Descriptive names
- Safe defaults
- Clear ownership
- Predictable behavior

Avoid scattering feature-flag logic throughout unrelated flows.

---

## 21. Boolean Properties

Boolean configuration should be clear and consistent.

Prefer:

    feature.enabled=true

over ambiguous values such as:

    feature=1

unless the project's configuration standard explicitly requires numeric values.

---

## 22. Numeric Configuration

Numeric configuration should be validated where incorrect values could cause failures.

Examples:

- Timeout
- Retry count
- Batch size
- Pool size
- Maximum records

Avoid negative or zero values when the application does not support them.

---

## 23. Configuration Validation

Critical configuration should be validated during application startup or before use where practical.

Examples:

- Required URL
- Required credentials
- Required database configuration
- Required encryption key
- Required queue name

Fail early when required configuration is missing.

---

## 24. Optional Configuration

Optional configuration should have safe and documented defaults.

Do not silently fall back to an unsafe value when an optional configuration is missing.

---

## 25. Connector Configuration

Connector-specific configuration should be externalized when it varies by environment.

Examples:

- HTTP base URLs
- Database connection properties
- SFTP hosts
- Queue names
- Salesforce endpoints

---

## 26. Database Configuration

Database configuration should not contain hard-coded credentials.

Review:

- URL
- Host
- Port
- Database name
- Username
- Password
- TLS configuration
- Pool settings

Sensitive values must be protected.

---

## 27. Messaging Configuration

Messaging configuration should externalize environment-specific values.

Examples:

- Queue names
- Exchange names
- Broker URL
- Virtual host
- Connection properties

Review whether development and production destinations can be accidentally mixed.

---

## 28. File Path Configuration

Environment-specific file paths should be externalized.

Avoid hard-coded paths such as:

    /tmp/application
    C:\application\data
    /opt/dev/files

unless the path is intentionally fixed and documented.

---

## 29. Path Security

Configuration-controlled file paths must not allow untrusted input to escape the intended directory.

Review for path traversal risks where configuration values interact with runtime input.

---

## 30. API Configuration

API-related configuration should include appropriate values for:

- Base URL
- Timeout
- Authentication
- Client ID
- Client secret
- TLS
- Retry behavior

Avoid embedding these values directly in flow logic.

---

## 31. API Security Configuration

Security-related API configuration must be reviewed separately against:

- API security standards
- Security standards
- API security analysis skill

Examples include:

- OAuth configuration
- Client credentials
- JWT settings
- TLS
- Policy-related configuration

---

## 32. Logging Configuration

Logging configuration should be environment-aware.

For example:

- Development may allow DEBUG.
- Production should normally use appropriate operational levels.

Avoid enabling verbose sensitive-data logging in production.

---

## 33. Log Level Configuration

Log levels should be configurable where appropriate.

Avoid hard-coding production logging behavior if operational configuration is expected to control it.

Do not enable DEBUG simply to make troubleshooting easier without considering sensitive-data exposure and performance.

---

## 34. Sensitive Logging Configuration

Configuration should not cause sensitive information to be logged.

Review:

- Payload logging
- HTTP headers
- Authentication information
- Database statements
- Tokens
- Credentials

---

## 35. Maven Configuration

Review `pom.xml` for configuration that affects deployment or runtime behavior.

Check:

- Properties
- Profiles
- Dependencies
- Plugin configuration
- Environment values
- Credentials
- Repository configuration

---

## 36. Maven Profiles

Maven profiles should have clear purposes.

Avoid ambiguous profile names such as:

    profile1
    test2
    newProfile

Prefer descriptive names such as:

    dev
    qa
    production

where appropriate.

---

## 37. Maven Credentials

Do not hard-code credentials in:

- `pom.xml`
- Maven profiles
- Plugin configuration
- Repository configuration

Use approved credential-management mechanisms.

---

## 38. Repository Configuration

Review configured Maven repositories.

Avoid unnecessary repositories.

Be cautious with unknown or untrusted repositories because dependencies obtained from them can introduce supply-chain risk.

---

## 39. Dependency Versions

Configuration should use controlled dependency versions.

Avoid uncontrolled version ranges where reproducibility is important.

---

## 40. Environment Variable Usage

Environment variables may be used for deployment-specific values.

Review:

- Naming
- Required values
- Secret handling
- Defaults
- Deployment configuration

Do not expose secrets through logs or diagnostic output.

---

## 41. Configuration Documentation

Important configuration should be documented.

Documentation should explain:

- Purpose
- Expected format
- Required/optional status
- Environment differences
- Security requirements

Do not document actual production secrets.

---

## 42. Configuration Comments

Comments should explain non-obvious configuration decisions.

Avoid comments that simply restate the property name.

Good:

    # Production timeout increased because the downstream service
    # performs long-running report generation.

Avoid:

    # Timeout
    customer.api.timeout=30000

---

## 43. Configuration Consistency

Similar configuration properties should follow consistent naming and structure.

For example:

    customer.api.url
    customer.api.timeout
    customer.api.client-id

is preferable to mixing unrelated naming styles.

---

## 44. Unused Configuration

Identify properties that are:

- Never referenced
- Obsolete
- Duplicated
- Left over from previous implementations

Unused configuration should be removed unless there is evidence it is intentionally retained.

---

## 45. Missing Configuration

Identify configuration references that do not have a corresponding defined value.

Examples:

- Missing property
- Incorrect property name
- Incorrect environment file
- Missing deployment variable

A missing required property should be reported when it can cause deployment or runtime failure.

---

## 46. Typographical Errors

Check for inconsistencies such as:

    customer.api.url

being referenced as:

    customer.api.baseUrl

A configuration mismatch may cause runtime failures.

---

## 47. Configuration Type Safety

Where possible, configuration values should be interpreted using the correct type.

Examples:

- Boolean
- Integer
- Decimal
- Duration
- String

Do not assume every configuration value is a string when the application expects another type.

---

## 48. Sensitive Configuration in Git

Never commit:

- Production passwords
- Private keys
- Access tokens
- Client secrets
- Database passwords
- Cloud credentials

If a real credential is discovered, treat it as a security incident and recommend rotation rather than merely removing it from the file.

---

## 49. Example Configuration

Example or template configuration may contain placeholders.

Prefer:

    customer.api.url=${CUSTOMER_API_URL}

over embedding a real production endpoint or secret in documentation.

---

## 50. Local Development Configuration

Local developer configuration should not be committed if it contains:

- Personal credentials
- Local secrets
- Private certificates
- Machine-specific paths

Provide safe templates where needed.

---

## 51. Configuration Templates

Templates should clearly indicate required values.

Example:

    customer.api.url=${CUSTOMER_API_URL}
    customer.api.client-id=${CUSTOMER_API_CLIENT_ID}
    customer.api.client-secret=${CUSTOMER_API_CLIENT_SECRET}

Do not populate templates with real credentials.

---

## 52. Production Configuration

Production configuration should receive stronger scrutiny.

Review:

- Secrets
- TLS
- Authentication
- URLs
- Database settings
- Logging
- Timeouts
- Retry behavior
- Resource limits

Production configuration must not accidentally use development or test settings.

---

## 53. Configuration Precedence

When multiple sources can define the same setting, the precedence must be understood.

Review potential conflicts between:

- Default properties
- Environment properties
- Secure properties
- Environment variables
- Runtime properties
- Maven profiles

Unexpected precedence can create deployment defects.

---

## 54. Configuration Drift

Check whether equivalent environments have materially different configuration without documented justification.

Examples:

- Different timeout values
- Different security settings
- Different retry policies
- Different connector endpoints

Configuration differences should be intentional.

---

## 55. Configuration and Security

Configuration must not weaken security between environments without a deliberate reason.

Examples of concerns:

- TLS disabled in production
- Authentication disabled
- Debug logging enabled
- Weak credentials
- Certificate validation disabled

---

## 56. Configuration and Performance

Review configuration that materially affects performance.

Examples:

- Connection pool size
- Batch size
- Retry count
- Timeout
- Threading
- Pagination size
- Streaming

Do not recommend changing performance settings without evidence.

---

## 57. Configuration and Availability

Review settings that can affect application availability.

Examples:

- Connection limits
- Retry behavior
- Timeout
- Reconnection
- Pool exhaustion
- Queue configuration

---

## 58. Configuration and Resilience

Configuration should support appropriate resilience.

Review:

- Retry limits
- Backoff
- Timeout
- Reconnection
- Circuit-breaking configuration where applicable
- Dead-letter configuration

Avoid configurations that can create retry storms.

---

## 59. Configuration Review Checklist

Before completing the configuration review, confirm:

- Environment-specific values are externalized.
- URLs are not unnecessarily hard-coded.
- Credentials are not hard-coded.
- Secrets are protected.
- Encryption keys are protected.
- `.properties` files were reviewed.
- `.yaml` files were reviewed.
- `.yml` files were reviewed.
- Mule XML configuration was reviewed.
- Maven configuration was reviewed.
- Environment variables were considered.
- Production configuration cannot accidentally use test values.
- Required properties exist.
- Property references match property definitions.
- Unused properties were considered.
- Duplicate properties were considered.
- Configuration naming is consistent.
- Timeouts are appropriate.
- Retry values are bounded.
- Logging configuration does not expose sensitive information.
- TLS configuration is appropriate.
- Certificate validation is preserved.
- Database configuration is secure.
- Messaging configuration is environment-safe.
- File paths are appropriate.
- Configuration-controlled destinations cannot be manipulated by untrusted input.
- Configuration differences between environments are intentional.
- No real secrets are present in source control.

---

## 60. Configuration Quality Gate

The reviewer must be able to answer the following questions:

1. Can the same application artifact be deployed safely across environments?
2. Are all environment-specific values externalized?
3. Are credentials and secrets protected?
4. Are encryption keys protected?
5. Can production accidentally use test or development configuration?
6. Are all required properties defined?
7. Are all property references valid?
8. Are configuration files consistent with each other?
9. Are connector settings configured appropriately?
10. Are timeout and retry values reasonable?
11. Is logging configuration safe?
12. Is TLS configuration secure?
13. Are database and messaging settings protected?
14. Are configuration-controlled file paths safe?
15. Is Maven configuration free from exposed credentials?
16. Are unused and duplicate properties identified?
17. Is configuration understandable to another developer or operator?
18. Can configuration changes be made without modifying application logic?

### Final Question

> Can this application be deployed to development, test, and production using controlled configuration changes without modifying code, exposing secrets, weakening security, or introducing unexpected runtime behavior?