Application:
${GITHUB_WORKSPACE}/application

Framework:
${GITHUB_WORKSPACE}/code-review

Reports:
${GITHUB_WORKSPACE}/reports

src
pom.xml
artifact.json
code-review/
│
├── CLAUDE.md
│
├── .claude/
│   ├── agents/
│   │   ├── architecture-reviewer.md
│   │   ├── mule-code-reviewer.md
│   │   ├── connector-reviewer.md
│   │   ├── security-reviewer.md
│   │   ├── api-security-reviewer.md
│   │   ├── performance-reviewer.md
│   │   ├── munit-reviewer.md
│   │   ├── configuration-reviewer.md
│   │   ├── logging-reviewer.md
│   │   └── report-reviewer.md
│   │
│   ├── skills/
│   │   ├── mulesoft-architecture/
│   │   │   └── SKILL.md
│   │   ├── mule-code-quality/
│   │   │   └── SKILL.md
│   │   ├── connector-analysis/
│   │   │   └── SKILL.md
│   │   ├── api-security-analysis/
│   │   │   └── SKILL.md
│   │   ├── security-analysis/
│   │   │   └── SKILL.md
│   │   ├── performance-analysis/
│   │   │   └── SKILL.md
│   │   ├── munit-analysis/
│   │   │   └── SKILL.md
│   │   ├── configuration-analysis/
│   │   │   └── SKILL.md
│   │   ├── logging-analysis/
│   │   │   └── SKILL.md
│   │   ├── duplication-analysis/
│   │   │   └── SKILL.md
│   │   └── word-report-generation/
│   │       └── SKILL.md
│   │
│   └── rules/
│       ├── review-scope.md
│       ├── finding-rules.md
│       ├── security-rules.md
│       └── report-rules.md
│
├── prompts/
│   └── mulesoft-review.md
│
├── standards/
│   ├── architecture/
│   │   └── architecture-standards.md
│   ├── api-security/
│   │   └── api-security-standards.md
│   ├── coding/
│   │   └── coding-standards.md
│   ├── connectors/
│   │   └── connector-standards.md
│   ├── configuration/
│   │   └── configuration-standards.md
│   ├── dataweave/
│   │   └── dataweave-standards.md
│   ├── error-handling/
│   │   └── error-handling-standards.md
│   ├── logging/
│   │   └── logging-standards.md
│   ├── munit/
│   │   └── munit-standards.md
│   ├── naming/
│   │   └── naming-standards.md
│   ├── performance/
│   │   └── performance-standards.md
│   └── security/
│       └── security-standards.md
│
├── config/
│   └── review-config.yaml
│
├── scripts/
│   ├── prepare-workspace.sh
│   ├── run-review.sh
│   └── validate-report.sh
│
├── .github/
│   └── workflows/
│       └── mulesoft-code-review.yml
│
├── README.md
└── VERSION

# MuleSoft Enterprise Code Review Framework

## Overview

The MuleSoft Enterprise Code Review Framework is an automated, evidence-based review framework for MuleSoft applications.

It evaluates applications against enterprise standards across:

- Architecture
- MuleSoft code quality
- Connectors
- API security
- Application security
- Performance
- Configuration
- Logging and observability
- Error handling
- MUnit
- DataWeave
- Naming
- Duplication
- Maintainability
- Operational supportability

The framework is designed to answer:

> If a Senior MuleSoft Architect and Senior Technical Lead were responsible for approving this application for production, what would they need to know, what would they challenge, and what would they require to be fixed?

The review focuses on meaningful, evidence-based findings and practical remediation rather than generic checklist compliance.

---

## Repository Structure

    code-review/
    │
    ├── CLAUDE.md
    │
    ├── .claude/
    │   ├── agents/
    │   │   ├── architecture-reviewer.md
    │   │   ├── mule-code-reviewer.md
    │   │   ├── connector-reviewer.md
    │   │   ├── security-reviewer.md
    │   │   ├── api-security-reviewer.md
    │   │   ├── performance-reviewer.md
    │   │   ├── munit-reviewer.md
    │   │   ├── configuration-reviewer.md
    │   │   ├── logging-reviewer.md
    │   │   └── report-reviewer.md
    │   │
    │   ├── skills/
    │   │   ├── mulesoft-architecture/
    │   │   ├── mule-code-quality/
    │   │   ├── connector-analysis/
    │   │   ├── api-security-analysis/
    │   │   ├── security-analysis/
    │   │   ├── performance-analysis/
    │   │   ├── munit-analysis/
    │   │   ├── configuration-analysis/
    │   │   ├── logging-analysis/
    │   │   ├── duplication-analysis/
    │   │   └── word-report-generation/
    │   │
    │   └── rules/
    │       ├── review-scope.md
    │       ├── finding-rules.md
    │       ├── security-rules.md
    │       └── report-rules.md
    │
    ├── prompts/
    │   └── mulesoft-review.md
    │
    ├── standards/
    │   ├── architecture/
    │   ├── api-security/
    │   ├── coding/
    │   ├── connectors/
    │   ├── configuration/
    │   ├── dataweave/
    │   ├── error-handling/
    │   ├── logging/
    │   ├── munit/
    │   ├── naming/
    │   ├── performance/
    │   └── security/
    │
    ├── config/
    │   └── review-config.yaml
    │
    ├── scripts/
    │   ├── prepare-workspace.sh
    │   ├── run-review.sh
    │   └── validate-report.sh
    │
    ├── .github/
    │   └── workflows/
    │       └── mulesoft-code-review.yml
    │
    ├── README.md
    └── VERSION

---

## Framework Components

### CLAUDE.md

Defines the overall operating instructions for the MuleSoft review framework.

It establishes:

- Review objectives
- Repository scope
- Mandatory exclusions
- Review priorities
- Evidence requirements
- Finding requirements
- Security requirements
- Reporting requirements
- Completion criteria

---

## Specialist Agents

The framework uses specialist agents for focused analysis.

### Architecture Reviewer

Reviews:

- Application architecture
- API layering
- Integration patterns
- Flow architecture
- Coupling
- Reusability
- Architectural anti-patterns
- Architectural risks

### Mule Code Reviewer

Reviews:

- Mule implementation
- Flow design
- Subflows
- Variables
- DataWeave
- Naming
- Error handling
- Maintainability
- Custom code
- Dependencies
- MuleSoft implementation practices

### Connector Reviewer

Reviews:

- Connector configuration
- Authentication
- TLS
- Timeout
- Retry
- Reconnection
- Pooling
- Reuse
- Performance
- Duplicate connector configurations

### Security Reviewer

Reviews:

- Credentials
- Secrets
- Sensitive configuration
- Authentication
- Authorization
- TLS
- Sensitive logging
- Secret handling
- Security weaknesses

### API Security Reviewer

Reviews:

- API authentication
- Authorization
- OAuth/JWT
- Client ID enforcement
- Input validation
- API policies
- TLS
- Rate limiting
- CORS
- Error disclosure
- Webhook security

### Performance Reviewer

Reviews:

- Connector calls inside loops
- Repeated downstream calls
- Payload handling
- Streaming
- DataWeave performance
- Database access
- Connection pools
- Timeouts
- Retries
- Concurrency
- Parallel processing
- Batching

### MUnit Reviewer

Reviews:

- Test coverage
- Assertions
- Mocks
- Verify calls
- Happy paths
- Error paths
- Negative scenarios
- Edge cases
- Connector failures
- Transformation failures

### Configuration Reviewer

Reviews:

- Properties
- YAML
- YML
- Environment configuration
- Secure properties
- Duplicate properties
- Missing properties
- Hard-coded values
- Environment consistency

### Logging Reviewer

Reviews:

- Correlation IDs
- Flow traceability
- Error logging
- Business context
- Payload logging
- Sensitive information
- Log levels
- Duplicate logging
- Operational troubleshooting

### Report Reviewer

Performs final validation of:

- Findings
- Evidence
- Severity
- Deduplication
- Statistics
- Architecture
- Charts
- Word document quality
- Secret exposure
- Overall report quality

---

## Review Skills

The framework provides dedicated skills for:

- MuleSoft architecture
- Mule code quality
- Connector analysis
- API security analysis
- Security analysis
- Performance analysis
- MUnit analysis
- Configuration analysis
- Logging analysis
- Duplication analysis
- Word report generation

Skills provide focused review methodology and should be applied whenever relevant.

---

## Standards

The framework evaluates the application using standards covering:

- Architecture
- API security
- Coding
- Connectors
- Configuration
- DataWeave
- Error handling
- Logging
- MUnit
- Naming
- Performance
- Security

A standards deviation is not automatically a finding.

The reviewer must determine whether the deviation creates meaningful:

- Security impact
- Reliability impact
- Performance impact
- Maintainability impact
- Operational impact
- Architectural impact
- Production risk

---

## Review Scope

The MuleSoft application is expected to be available at:

    ${GITHUB_WORKSPACE}

The review framework is located at:

    ${GITHUB_WORKSPACE}/code-review

The report output directory is:

    ${GITHUB_WORKSPACE}/reports

The review includes, where present:

- `pom.xml`
- `mule-artifact.json`
- All Mule XML files
- All DataWeave files
- Java source
- Python source
- RAML
- OpenAPI/OAS
- `.properties`
- `.yaml`
- `.yml`
- Relevant JSON configuration
- XML configuration
- MUnit tests
- Connector configurations
- Global configurations
- Supporting application configuration

---

## Mandatory Exclusions

The following paths must never be reviewed as MuleSoft application source:

    ${GITHUB_WORKSPACE}/code-review/**
    ${GITHUB_WORKSPACE}/reports/**

The review must also exclude:

- Review agents
- Review skills
- Review rules
- Review prompts
- Review standards
- Framework configuration
- Framework scripts
- Temporary review files
- Generated reports

The purpose of these exclusions is to prevent findings from being generated against the review framework itself.

---

## Review Process

The review follows this general sequence:

1. Discover the application structure.
2. Identify APIs and application entry points.
3. Identify flows and subflows.
4. Identify connectors and global configurations.
5. Identify configuration and environment files.
6. Identify custom Java/Python code.
7. Analyze architecture.
8. Analyze security.
9. Analyze API security.
10. Analyze performance.
11. Analyze error handling.
12. Analyze logging.
13. Analyze MUnit coverage.
14. Analyze duplication.
15. Apply relevant standards.
16. Correlate findings across specialist reviews.
17. Remove duplicate findings.
18. Validate severity.
19. Produce application assessment.
20. Generate the Word report.
21. Validate the Word report.
22. Return the exact report path.

The Word report must not be generated until the source review is substantially complete.

---

## Evidence-Based Review

Every finding must be supported by evidence.

Evidence should identify, where applicable:

- File
- Flow
- Subflow
- Processor
- Configuration
- Property
- Relevant implementation
- Observed behavior

Findings should not include unnecessarily large source-code excerpts.

Secrets must never be included in findings.

If evidence depends on infrastructure, runtime configuration, deployment configuration, or business context that cannot be established from the repository, use:

    Verification Required

---

## Finding Requirements

Every finding must contain:

- Finding ID
- Title
- Category
- Severity
- Location
- Evidence
- Impact
- Recommendation
- Solution
- Verification, when required
- Priority

Example structure:

    Finding ID: MULE-SEC-001

    Title: Plain-text credential

    Category: Security

    Severity: Critical

    Location: src/main/resources/application.properties

    Evidence:
    A credential is stored directly in application configuration.

    Impact:
    Repository access may expose a production-sensitive credential.

    Recommendation:
    Remove the exposed credential and migrate the application to secure configuration.

    Solution:
    Rotate the credential, remove it from source control, configure secure property
    management, update runtime configuration, and review repository history.

    Verification:
    Confirm that the credential has been rotated and is no longer active.

    Priority:
    Immediate

---

## Severity Model

### Critical

Use only for severe issues such as:

- Active credential exposure
- Severe unauthorized access
- Critical data exposure
- Highly exploitable production risk
- Major production availability risk

### High

Use for significant:

- Security risks
- Reliability risks
- Data integrity risks
- Performance bottlenecks
- Architectural risks
- Production stability risks

### Medium

Use for meaningful but non-critical issues.

### Low

Use for minor improvements with useful technical benefit.

### Warning

Use primarily for:

- Missing MUnit coverage
- Verification-required items
- Infrastructure-dependent concerns
- Business-context-dependent concerns

Severity must not be inflated merely to increase the importance of a finding.

---

## Security

The framework checks for:

- Plain-text passwords
- API keys
- Client secrets
- Access tokens
- Refresh tokens
- Private keys
- Cloud credentials
- Database credentials
- SFTP credentials
- Encryption keys
- Sensitive logging
- Insecure URLs
- Unsafe authentication patterns
- Sensitive data exposure

Actual secrets must never be included in the final report.

Use:

    [REDACTED]

when referring to sensitive values.

If a credential is discovered in source control, remediation must address the exposure itself.

Recommended remediation includes:

1. Remove the secret from application source.
2. Rotate or revoke the exposed credential.
3. Store the replacement securely.
4. Update runtime configuration.
5. Review repository history when necessary.

---

## API Security

API reviews consider:

- Authentication
- Authorization
- OAuth/JWT
- Client ID enforcement
- TLS
- Input validation
- API policies
- Rate limiting
- CORS
- Sensitive data
- Error disclosure
- Webhook security
- Idempotency
- API version security

External API Manager or Gateway controls cannot be assumed to be missing simply because they are not present in the source repository.

If they cannot be verified, use:

    Verification Required

---

## Connector Review

Every applicable connector should be evaluated for:

- Global configuration
- Authentication
- TLS
- Timeout
- Retry
- Reconnection
- Pooling
- Concurrency
- Streaming
- Error handling
- Environment configuration
- Duplicate configuration
- Performance

Connector recommendations must be based on actual connector behavior and integration requirements.

Do not recommend arbitrary timeout, retry, or pool values without considering:

- Downstream capacity
- SLA
- Expected concurrency
- Retry behavior
- Runtime characteristics

---

## Performance Review

The framework considers:

- Connector calls inside loops
- Repeated external calls
- Duplicate downstream calls
- Large payload materialization
- Missing streaming
- Poor batching
- Missing bulk operations
- Excessive parallelism
- Inefficient database access
- Repeated DataWeave transformations
- Excessive variables
- Payload logging
- Connection pooling
- Retry behavior
- Timeout behavior
- Memory consumption

Performance recommendations must explain:

- Why the behavior matters
- Expected impact
- Recommended solution
- Risks and trade-offs

Parallel processing must not be recommended where it could violate:

- Ordering requirements
- Transaction behavior
- Rate limits
- Downstream capacity
- Business rules

---

## Configuration Review

Configuration review includes:

- `.properties`
- `.yaml`
- `.yml`
- JSON configuration
- XML configuration
- Secure properties
- Environment-specific configuration

The review considers:

- Unused properties
- Duplicate properties
- Missing properties
- Inconsistent property names
- Hard-coded environment values
- Sensitive properties
- Environment drift
- Secure-property coverage

Environment-specific values are expected to differ.

The review focuses on structural inconsistency and meaningful configuration problems rather than legitimate environment-specific differences.

---

## Logging Review

The framework evaluates whether logging provides sufficient operational visibility.

Areas include:

- Correlation ID
- Flow traceability
- Business context
- Important processing events
- External system interactions
- Error context
- Processing duration where useful
- Log levels
- Payload logging
- Header logging
- Sensitive information
- Duplicate logging
- Logging performance

The framework does not require logging after every Mule processor.

Full payload logging should not be recommended indiscriminately.

---

## Error Handling Review

The framework evaluates:

- Global error handlers
- Flow-level error handlers
- Try scopes
- On Error Continue
- On Error Propagate
- Error mapping
- Retry handling
- Dead-letter handling where applicable
- API error responses

`On Error Continue` is not automatically a defect.

The reviewer must determine whether the behavior is intentional and appropriate for the business flow.

---

## MUnit Review

The framework evaluates coverage of important application behavior.

Relevant scenarios include:

- Happy path
- Invalid input
- Connector failure
- Timeout
- Authentication failure
- Downstream 4xx
- Downstream 5xx
- Empty response
- Null values
- Transformation failure
- Error handler behavior
- Edge cases

Missing coverage is normally reported as:

    Warning

unless the absence of testing creates a more serious risk.

---

## Custom Code Review

The framework identifies custom:

- Java
- Python
- Scripts
- Extensions
- Utility implementations

Where appropriate, the reviewer considers whether the implementation could be replaced with:

- DataWeave
- Mule processors
- MuleSoft connectors
- Standard modules
- Built-in MuleSoft capabilities

Custom code is not considered a problem simply because a built-in alternative exists.

Replacement recommendations must explain:

- Current behavior
- Proposed alternative
- Benefits
- Migration considerations
- Trade-offs
- Whether replacement is actually recommended

---

## Duplication Review

The framework looks for meaningful duplication across:

- Flows
- Subflows
- Logic blocks
- Transformations
- Connector calls
- Variables
- Logger patterns
- Error handling
- Connector configurations
- Properties

Harmless repetition should not be reported.

A duplication finding should explain the consolidation opportunity and expected benefit.

---

## Architecture Review

The framework identifies the architecture actually implemented by the application.

Potential patterns include:

- API-led connectivity
- Experience APIs
- Process APIs
- System APIs
- Layered integration
- Point-to-point integration
- Event-driven architecture
- Batch processing
- Scheduled processing
- Messaging
- Synchronous integration
- Asynchronous integration
- Hybrid integration
- Orchestration
- Choreography

Architecture must be based on repository evidence.

The review must not impose an architecture simply because it is considered a common MuleSoft pattern.

---

## Architecture Diagram

Where sufficient evidence exists, the final report should contain an architecture representation showing relevant components such as:

- Consumers
- APIs
- Mule flows
- Application layers
- External systems
- Databases
- Messaging systems
- SaaS systems
- File systems
- Major data movement
- Security boundaries

The framework must not invent systems or integrations.

If architecture evidence is incomplete, state:

    Architecture evidence incomplete — infrastructure verification required.

---

## Positive Observations

The final report should identify meaningful strengths when supported by evidence.

Examples include:

- Strong API security
- Good global connector reuse
- Secure property implementation
- Effective error handling
- Good MUnit coverage
- Effective logging
- Good flow decomposition
- Good DataWeave practices
- Strong environment separation
- Appropriate architecture
- Good operational supportability

Positive observations must be evidence-based.

---

## Executive Summary

The final Word report must include an executive summary covering:

- Overall assessment
- Architecture assessment
- Security assessment
- Performance assessment
- Maintainability assessment
- Test coverage assessment
- Top risks
- Top recommendations
- Overall score

The summary should be suitable for both:

- Technical leadership
- Senior engineers

---

## Overall Score

The application score should consider multiple dimensions:

- Architecture
- Code quality
- Connectors
- API security
- Security
- Performance
- Configuration
- Logging
- MUnit
- Maintainability

The score must not be calculated simply from the number of findings.

Severity and business/technical impact should influence the assessment.

---

## Risk Summary

The final report should provide a risk summary containing:

| ID | Category | Severity | Finding | Impact | Solution |
|---|---|---|---|---|---|

Only actual findings should appear in this table.

---

## Remediation Roadmap

Recommendations should be organized into:

### Immediate

Critical and high-risk issues.

### Short Term

Important reliability, security, performance, testing, and configuration improvements.

### Medium Term

Architectural and maintainability improvements.

### Long Term

Strategic modernization opportunities.

---

## Word Report

The final deliverable must be a `.docx`.

The expected filename is:

    mulesoft-standards-review_<timestamp>.docx

The expected output directory is:

    ${GITHUB_WORKSPACE}/reports/

The report should be suitable for:

- Architecture review
- Technical leadership
- Client review
- Production readiness assessment

Where useful, the document may contain:

- Cover page
- Table of contents
- Executive summary
- Severity tables
- Architecture diagrams
- Scorecards
- Bar charts
- Finding distribution charts
- Risk heatmaps
- Remediation roadmap
- Tables
- Headers and footers
- Page numbers
- Consistent typography and colors

Visual elements must represent actual review data.

---

## Severity Colors

The recommended visual convention is:

- Critical: Dark red
- High: Red
- Medium: Orange
- Low: Yellow/amber
- Warning: Blue/gray
- Positive: Green

The report must remain readable and accessible.

---

## GitHub Actions

The framework includes:

    .github/workflows/mulesoft-code-review.yml

The workflow is responsible for:

1. Checking out the application.
2. Preparing the review workspace.
3. Executing the review.
4. Validating the generated report.
5. Uploading the `.docx` report as a GitHub Actions artifact.

The Claude review process itself must not upload the GitHub Actions artifact.

---

## Local Scripts

The framework provides:

    scripts/prepare-workspace.sh
    scripts/run-review.sh
    scripts/validate-report.sh

These scripts support:

- Workspace preparation
- Review execution
- Report validation

The scripts should respect the configured workspace and output locations.

---

## Report Validation

Before completion, the generated report must be validated for:

1. File existence
2. Readability
3. Executive summary
4. Architecture details
5. Finding solutions
6. Consistent severity representation
7. Chart and table rendering
8. Secret exposure
9. Framework-file exclusion
10. Correct filename
11. Finding deduplication
12. Evidence-based statistics
13. Evidence-based architecture
14. Overall report quality

The review must not claim successful completion until validation succeeds.

---

## Completion Criteria

A review is complete only when:

- MuleSoft source has been reviewed.
- Applicable specialist agents have completed.
- Applicable skills have been applied.
- Relevant standards have been evaluated.
- Findings have been consolidated.
- Duplicate findings have been removed.
- Severity has been validated.
- The Word document has been generated.
- The Word document has been validated.
- No secrets are exposed.
- No review-framework files appear as application findings.
- Statistics are evidence-based.
- Architecture information is evidence-based.
- The exact `.docx` path is known.

The final response should provide the absolute report path.

Example:

    Download full report: /github/workspace/reports/mulesoft-standards-review_20260911_153045.docx

---

## Final Principle

The framework is intended to provide a production-oriented MuleSoft assessment.

Every reported issue should have:

- Evidence
- A reason it matters
- Practical impact
- A recommended action
- A concrete solution

Do not report problems merely to increase finding counts.

Do not fabricate architecture, infrastructure controls, statistics, security controls, performance characteristics, or test coverage.

Focus on:

- Real problems
- Real risks
- Real evidence
- Practical solutions
- Production readiness
- Security
- Performance
- Maintainability
- Operational supportability