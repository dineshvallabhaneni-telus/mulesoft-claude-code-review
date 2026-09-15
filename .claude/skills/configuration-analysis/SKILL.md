# MuleSoft Configuration Analysis Skill

## Purpose

Perform a comprehensive configuration review of the MuleSoft application.

Review the application as a:

- Senior MuleSoft Architect
- Enterprise Integration Architect
- Senior Technical Lead

The objective is to determine whether application configuration is:

- Correct
- Consistent
- Secure
- Maintainable
- Environment-aware
- Reusable
- Operationally appropriate
- Performance-aware

The review must be evidence-based.

Do not report configuration differences merely because values differ between environments. Distinguish intentional environment-specific values from genuine configuration inconsistencies.

Every meaningful finding MUST include:

- Evidence
- Impact
- Severity
- Recommendation
- Practical solution

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

Do NOT review these directories as application source:

${GITHUB_WORKSPACE}/code-review/**
${GITHUB_WORKSPACE}/reports/**

Do not report findings against:

- Review agents
- Review skills
- Prompt files
- Framework scripts
- Generated reports

---

# 3. Configuration Discovery

Identify all application configuration sources.

Review at minimum:

- pom.xml
- mule-artifact.json
- XML configuration files
- .properties
- .yaml
- .yml
- .json
- Secure property configuration
- Environment-specific configuration
- Maven profiles
- Resource files
- Connector global configurations
- TLS configurations
- Application properties
- Runtime configuration references

Do not assume configuration files only use .properties.

---

# 4. Configuration Inventory

Build an internal inventory containing:

| Configuration | File | Environment | Type | Sensitive | Referenced | Assessment |
|---|---|---|---|---|---|---|

Identify:

- Global configurations
- Environment properties
- Secure properties
- Connector configurations
- Runtime properties
- Application settings

---

# 5. Property File Discovery

Search for:

- *.properties
- *.yaml
- *.yml

Also identify property-like files referenced through Maven or Mule configuration.

Do not assume naming conventions.

---

# 6. Environment Discovery

Identify available environments.

Examples:

- DEV
- QA
- SIT
- INT
- UAT
- PREPROD
- PROD

Do not assume all environments exist.

Determine environments from repository evidence.

---

# 7. Environment Consistency

Compare environment configuration.

Determine whether the same logical properties exist across environments.

Example:

DEV:

db.host
db.port
db.username
db.password

QA:

db.host
db.port
db.username
db.password

PROD:

db.host
db.port
db.username

If PROD is missing a required property, report it.

---

# 8. Environment-Specific Differences

Do NOT report legitimate differences such as:

- Hostnames
- Ports
- Database names
- Queue names
- API URLs
- Environment-specific identifiers

Report only differences that create:

- Runtime risk
- Security risk
- Reliability risk
- Performance risk
- Deployment inconsistency

---

# 9. Missing Properties

Identify properties referenced by the application but not defined in the expected configuration.

Example:

${db.host}

but no corresponding property is found.

Classify according to evidence:

- Confirmed Missing
- Potentially Supplied Externally
- Verification Required

Do not report externally supplied runtime properties as missing unless repository evidence indicates they are required locally.

---

# 10. Unused Properties

Identify properties that appear to be defined but are not referenced by the application.

Check references across:

- XML
- DataWeave
- Java
- Python
- Maven
- Configuration files

Do not report a property as unused if dynamic resolution may be occurring and cannot be established statically.

Use:

Potentially Unused

when appropriate.

---

# 11. Property Naming Standards

Review naming consistency.

Examples:

db.host
db.port
api.customer.base-url

Look for:

- Inconsistent separators
- Inconsistent abbreviations
- Ambiguous names
- Duplicate concepts with different names

Do not impose a naming convention without considering the existing application standard.

---

# 12. Duplicate Properties

Identify logically duplicate properties.

Example:

customer.api.url
customer.api.baseUrl

If both represent the same endpoint, determine whether duplication creates maintenance risk.

Do not report different environment values as duplicates.

---

# 13. Duplicate Configuration

Identify duplicate global configurations such as:

- HTTP Request Config
- HTTP Listener Config
- Database Config
- SFTP Config
- TLS Context
- Salesforce Config
- Messaging Config

Where multiple configurations represent the same logical connection, report the duplication.

Recommend reuse of a global configuration where appropriate.

---

# 14. Global Configuration Usage

Verify that connectors use appropriate global configurations.

Review whether connector operations:

- Reference global configuration
- Duplicate configuration inline unnecessarily
- Use inconsistent settings

Do not require global configuration when the connector intentionally supports local configuration and reuse is not beneficial.

---

# 15. Global Configuration Naming

Evaluate whether global configurations have clear names.

Examples:

HTTP_Request_Config
Customer_API_HTTP_Config
DB_Config
Customer_DB_Config

Avoid reporting naming style as a finding unless it materially affects maintainability.

---

# 16. Connector Configuration Consistency

Compare configuration usage across flows.

Look for:

- Same endpoint with different timeout
- Same database with different pool settings
- Same SFTP server with different reconnect behavior
- Same API using inconsistent TLS configuration

Coordinate with connector-analysis.

Configuration-analysis owns consistency.

---

# 17. Timeout Configuration

Review timeout settings where configured.

Consider:

- HTTP response timeout
- Connection timeout
- Database timeout
- SFTP timeout
- Messaging timeout

Do not declare a timeout value incorrect without workload/context evidence.

Report:

- Missing critical timeout where indefinite waiting is plausible
- Obvious inconsistency
- Extreme configuration that creates a credible risk

---

# 18. Retry Configuration

Review retry settings.

Consider:

- Retry count
- Retry interval
- Backoff
- Maximum attempts
- Retry scope

Identify inconsistent or potentially excessive retry configuration.

Do not require retries for every connector.

---

# 19. Retry Safety

Determine whether retrying an operation may cause duplicate side effects.

Examples:

- POST request
- Database insert
- Payment operation
- Message publishing

Where idempotency is not visible, report:

Verification Required

rather than assuming it is unsafe.

---

# 20. Connection Pool Configuration

Where pooling exists, review:

- Max pool size
- Min pool size
- Max idle time
- Connection timeout
- Validation
- Reconnection

Do not claim a pool size is incorrect without runtime/workload evidence.

---

# 21. Pool Configuration Consistency

Compare pool configuration for the same logical systems across flows/environments.

Identify:

- Duplicate pool configurations
- Inconsistent pool sizes
- Different timeout behavior

Coordinate with:

performance-analysis

for performance implications.

---

# 22. TLS Configuration

Review:

- TLS contexts
- Keystores
- Truststores
- TLS versions where visible
- Certificate references
- Client authentication

Check whether sensitive passwords are securely configured.

Do not report infrastructure-level TLS gaps that cannot be established from repository evidence.

---

# 23. Secure Property Configuration

Determine whether secure properties are configured appropriately.

Look for:

- Secure configuration property modules
- Encrypted property values
- Secure property references
- Environment-specific secure property files

Sensitive credentials should not appear in plaintext.

Detailed security findings belong to:

security-analysis

---

# 24. Plaintext Sensitive Configuration

Identify plaintext:

- Passwords
- API keys
- Client secrets
- Tokens
- Private key passwords

Do not reproduce actual values.

Use:

[REDACTED]

in evidence.

---

# 25. YAML Configuration

Review .yaml and .yml files with the same rigor as .properties.

Evaluate:

- Environment consistency
- Naming
- References
- Duplicate values
- Unused properties
- Sensitive information
- Type consistency

---

# 26. YAML Type Consistency

Look for inconsistent types across environments.

Example:

DEV:

timeout: 30000

PROD:

timeout: "30000"

or:

enabled: true

versus:

enabled: "true"

Determine whether the Mule application expects a particular type.

---

# 27. Property Value Consistency

Look for values that should logically have the same configuration but differ unexpectedly.

Examples:

- Same API timeout
- Same retry policy
- Same protocol
- Same TLS behavior

Do not report legitimate environment-specific values.

---

# 28. Boolean Configuration

Check boolean properties for consistency.

Examples:

enabled=true
enabled=false

Determine whether the difference is intentional.

Do not classify environment-specific feature flags as defects without evidence.

---

# 29. Numeric Configuration

Review numeric configuration for:

- Timeouts
- Retry counts
- Pool sizes
- Batch sizes
- Polling intervals

Do not recommend arbitrary values.

Use workload-based recommendations.

---

# 30. URL Configuration

Review endpoint configuration.

Look for:

- Hard-coded URLs
- Duplicate URLs
- Environment-specific URLs incorrectly embedded in source
- HTTP instead of HTTPS where security is expected

Do not report localhost URLs automatically as defects.

Determine whether they are development/test configuration.

---

# 31. Hard-Coded Environment Values

Identify values that should normally be externalized.

Examples:

- Hostnames
- Ports
- Credentials
- API endpoints
- Queue names

Recommend property externalization where appropriate.

Do not externalize constants that are genuinely application logic.

---

# 32. Hard-Coded Credentials

Any credential embedded directly in:

- XML
- Java
- Python
- DataWeave
- JSON
- YAML
- Properties

should be reviewed as a security issue.

Primary owner:

security-analysis

Configuration-analysis should identify the configuration problem without duplicating the full security finding.

---

# 33. Mule Artifact Configuration

Review:

mule-artifact.json

Evaluate:

- Runtime version
- Application name
- Secure properties
- Classloader configuration where relevant
- Exported resources
- Configuration consistency

Do not report valid runtime-specific configuration as incorrect without evidence.

---

# 34. Runtime Version

Review the Mule runtime version declared by the application.

Look for:

- Obsolete versions
- Inconsistent runtime references
- Version mismatch with project dependencies

Do not claim a runtime version is unsupported without reliable evidence.

If current support status cannot be established:

Verification Required

---

# 35. Maven Configuration

Review pom.xml for:

- Mule Maven Plugin
- Runtime version
- Dependencies
- Profiles
- Repositories
- Plugin configuration
- Properties
- Build configuration

Do not duplicate dependency security analysis unless configuration itself creates the issue.

---

# 36. Maven Profiles

Review Maven profiles for:

- Environment-specific configuration
- Duplicate configuration
- Inconsistent versions
- Hard-coded credentials
- Unexpected deployment behavior

Ensure environment-specific configuration is understandable.

---

# 37. Dependency Version Properties

Look for centralized version properties.

Example:

<mule.runtime.version>...</mule.runtime.version>

Avoid duplicating versions throughout pom.xml.

---

# 38. Plugin Configuration

Review important Maven plugin configuration.

Look for:

- Duplicate configuration
- Inconsistent versions
- Hard-coded values
- Build behavior that differs unexpectedly between environments

Do not report harmless formatting differences.

---

# 39. Resource Naming

Review configuration resource naming.

Look for:

- Inconsistent environment names
- Ambiguous names
- Duplicate names
- Names that do not indicate purpose

Naming findings should be reported only when they materially affect maintainability.

---

# 40. Configuration File Naming

Review:

- .properties
- .yaml
- .yml

file naming consistency.

Examples:

- dev.properties
- qa.properties
- uat.properties
- prod.properties

Do not require a particular naming convention.

Identify inconsistency only when it causes confusion or deployment risk.

---

# 41. Environment Property Completeness

Produce an internal comparison matrix:

| Property | DEV | QA | UAT | PROD | Consistent | Sensitive |
|---|---|---|---|---|---|---|

Only include environments that actually exist.

---

# 42. Environment Drift

Identify configuration drift that could cause:

- Production failures
- Unexpected behavior
- Security weaknesses
- Performance differences
- Deployment failures

Do not report legitimate endpoint/name differences as drift.

---

# 43. Configuration Defaults

Review default values.

Look for:

- Unsafe defaults
- Development defaults
- Missing production values
- Empty values
- Null values

Determine whether defaults are appropriate.

---

# 44. Empty Configuration

Identify configuration such as:

- Empty URL
- Empty credential
- Empty timeout
- Empty required property

Determine whether it is intentional.

Do not report optional empty properties as defects.

---

# 45. Configuration Documentation

Evaluate whether important configuration is understandable.

Consider:

- Naming
- Comments
- Environment mapping
- Purpose

Do not require comments for every property.

---

# 46. Configuration Maintainability

Look for:

- Excessive duplication
- Scattered configuration
- Unclear property ownership
- Inconsistent naming
- Hard-coded values
- Environment coupling

Provide practical restructuring recommendations.

---

# 47. Configuration Security Boundary

Separate:

Application configuration

from:

Secret configuration

from:

Environment-specific configuration.

Recommend appropriate separation where evidence supports it.

---

# 48. Configuration and Performance

Identify configuration that can materially affect performance:

- Pool sizes
- Timeouts
- Retry
- Polling interval
- Batch size
- Concurrency

Do not duplicate detailed performance findings.

Coordinate with:

performance-analysis

---

# 49. Configuration and Reliability

Evaluate configuration that affects reliability:

- Retry
- Reconnection
- Timeout
- Failover
- Polling
- Error handling

Provide practical recommendations.

---

# 50. Configuration Findings

Every finding MUST contain:

## Finding ID

Example:

MULE-CONFIG-001

## Title

Concise configuration issue.

## Severity

High / Medium / Low / Warning

## Category

Configuration

## Location

Exact file/configuration.

## Evidence

Observed configuration.

## Impact

Why it matters.

## Recommendation

What should change.

## Solution

Practical implementation approach.

## Priority

Immediate / Short Term / Medium Term / Long Term

---

# 51. Severity Guidelines

## High

Configuration inconsistency or error likely to cause:

- Production outage
- Major deployment failure
- Significant security exposure

## Medium

Meaningful reliability, maintainability, or operational issue.

## Low

Minor configuration improvement.

## Warning

Configuration cannot be fully validated statically.

Do not inflate severity.

---

# 52. Unused Property Findings

When identifying unused properties, include:

- Property name
- File
- Environment
- Search scope
- Why it appears unused

Do not expose sensitive values.

---

# 53. Missing Property Findings

When identifying missing properties, include:

- Property reference
- File/flow
- Expected environment
- Evidence
- Potential runtime impact
- Recommended definition

If runtime injection is possible, classify as:

Verification Required

---

# 54. Environment Consistency Findings

When environments differ unexpectedly, provide:

- Property
- Environments affected
- Observed difference
- Expected behavior
- Recommended standard

Do not expose credentials.

---

# 55. Positive Configuration Observations

Identify good practices such as:

- Centralized global configurations
- Secure properties
- Consistent environment configuration
- Reusable connector configurations
- Clear property naming
- Proper externalization
- Appropriate timeout/retry configuration
- Clean Maven profiles

---

# 56. Cross-Skill Boundaries

Detailed findings owned by these skills should not be duplicated unnecessarily:

- mulesoft-architecture
- mule-code-quality
- connector-analysis
- api-security-analysis
- security-analysis
- performance-analysis
- munit-analysis
- logging-analysis
- duplication-analysis

This skill owns configuration structure, consistency, and maintainability.

If a plaintext password is found:

- configuration-analysis identifies the configuration issue.
- security-analysis owns the security severity and remediation.

If a pool configuration causes performance concerns:

- configuration-analysis identifies the configuration.
- performance-analysis owns the performance impact.

The final report reviewer must consolidate duplicate root causes.

---

# 57. No Unsupported Claims

Never claim:

- A property is definitely unused when dynamic resolution may exist.
- A runtime property is missing when it may be externally supplied.
- A pool size is incorrect without workload evidence.
- A timeout is incorrect without context.
- An environment difference is a defect simply because values differ.

Use:

Potentially Unused

or:

Verification Required

where appropriate.

---

# 58. Configuration Score

Provide a configuration score based on:

- Environment consistency
- Property management
- Global configuration reuse
- Secure configuration
- Naming
- Duplication
- Maintainability
- Runtime configuration
- Timeout/retry consistency

Do not calculate the score solely from finding count.

---

# 59. Final Output

Return structured configuration analysis containing:

## Configuration Summary

## Configuration Inventory

## Environment Inventory

## Property File Assessment

## Environment Consistency Assessment

## Unused Property Assessment

## Missing Property Assessment

## Global Configuration Assessment

## Timeout Assessment

## Retry Assessment

## Pool Configuration Assessment

## TLS Configuration Assessment

## Maven Configuration Assessment

## Mule Artifact Configuration Assessment

## Positive Configuration Observations

## Configuration Findings

## Recommended Configuration Improvements

## Verification Required

## Configuration Score

Do not generate the final Word document from this skill.

The word-report-generation skill is responsible for creating the final .docx.

---

# 60. Quality Standard

Before completing the review, ask:

"Would a Senior MuleSoft Architect trust this configuration assessment for a production application?"

If not:

- Remove trivial findings.
- Re-check property references.
- Distinguish legitimate environment differences from drift.
- Avoid arbitrary configuration recommendations.
- Protect all sensitive values.
- Provide practical solutions.
- Clearly identify static-analysis limitations.
- Prioritize issues that can affect deployment, reliability, security, performance, or maintainability.

The objective is production-quality configuration analysis, not a generic configuration checklist.