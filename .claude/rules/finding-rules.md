# MuleSoft Review Finding Rules

## Purpose

Define how findings must be identified, evaluated, prioritized, consolidated, and reported during the MuleSoft architecture and standards review.

These rules are mandatory for all reviewers, agents, skills, and the final report generator.

---

## 1. Evidence-Based Findings

Every finding must be based on evidence discovered in the MuleSoft application.

A finding must not be created solely because:

- A different implementation is preferred.
- A generic MuleSoft best practice exists.
- A feature is not visible without sufficient repository evidence.
- A particular design pattern is not being used.
- The implementation differs from the reviewer's personal coding style.

Before reporting a finding, understand the surrounding implementation and its purpose.

---

## 2. Required Finding Information

Every actionable finding must contain:

- Finding ID
- Finding title
- Severity
- Category
- Location
- Evidence
- Description
- Impact
- Recommendation
- Practical solution
- Relevant standard or best practice

Where applicable, also include:

- Affected flow
- Affected connector
- Affected configuration
- Affected environment
- Security impact
- Performance impact
- Maintainability impact
- Production impact
- Suggested remediation priority

---

## 3. Finding ID

Every final finding must have a unique identifier.

Use the following format:

`MSR-<CATEGORY>-<NUMBER>`

Examples:

- `MSR-SEC-001`
- `MSR-API-001`
- `MSR-PERF-001`
- `MSR-CON-001`
- `MSR-MUNIT-001`
- `MSR-CONFIG-001`
- `MSR-LOG-001`
- `MSR-ARCH-001`

The final report must not contain duplicate Finding IDs.

---

## 4. Severity Definitions

### Critical

Use Critical only when there is a severe and credible risk of:

- Major security compromise
- Significant credential exposure
- Severe data loss
- Severe production outage
- Critical architectural failure
- Severe reliability or operational risk

Examples may include:

- Plain-text production credentials
- Exposed private keys
- Severe authentication bypass
- Critical security weakness with clear repository evidence

Do not use Critical simply because an issue is undesirable.

---

### High

Use High when the issue can reasonably result in:

- Significant security exposure
- Major production instability
- Significant performance degradation
- Serious reliability problems
- Major maintainability problems
- Significant operational difficulty
- High business or technical risk

Examples may include:

- Missing critical API security control where repository evidence confirms the control is absent
- Severe connector configuration issue
- Major performance bottleneck
- Important production flow without required resilience

---

### Medium

Use Medium for meaningful issues that should be addressed but do not represent immediate severe risk.

Examples include:

- Significant duplication
- Missing important MUnit coverage
- Poor error handling
- Inefficient DataWeave
- Configuration inconsistencies
- Missing timeout configuration where risk is meaningful
- Maintainability concerns

---

### Low

Use Low for minor issues or improvement opportunities.

Examples include:

- Minor naming inconsistency
- Small maintainability improvement
- Limited duplication
- Minor logging improvement

Low findings should still provide useful remediation.

---

### Warning

Use Warning when attention is required but the repository evidence does not justify classifying the condition as a confirmed defect.

Examples:

- Missing MUnit coverage
- External API Manager policy cannot be verified
- External runtime security configuration cannot be verified
- Environment configuration requires verification
- Potentially unused property that may be dynamically referenced

A Warning must explain what should be verified or improved.

---

### Informational

Use Informational for:

- Positive observations
- Architectural observations
- Useful context
- Good practices
- Non-actionable recommendations

Do not use Informational to inflate the number of findings.

---

## 5. Do Not Over-Report

The purpose of the review is to identify meaningful risks and improvement opportunities.

Do not report every possible imperfection.

Do not create findings for:

- Harmless formatting differences
- Personal style preferences
- Trivial repetition
- Cosmetic differences with no meaningful impact
- Correct environment-specific values
- Intentional architectural decisions
- Necessary duplication
- Normal MuleSoft implementation patterns
- Generic recommendations without evidence

Prioritize quality over quantity.

---

## 6. Confirm Before Reporting

Before creating a finding:

1. Locate the relevant implementation.
2. Understand its context.
3. Determine whether the behavior is intentional.
4. Check related flows/configurations/components.
5. Determine the actual risk.
6. Determine whether the issue is already mitigated elsewhere.
7. Determine whether the issue is externally configured.
8. Collect supporting evidence.
9. Determine the appropriate severity.
10. Provide a practical solution.

Do not report a finding after examining only one isolated line when the surrounding implementation could change the conclusion.

---

## 7. Evidence Rules

Evidence should identify the actual implementation that caused the finding.

Good evidence includes:

- File path
- Flow name
- Configuration name
- Connector
- Property key
- Component
- Relevant code/configuration
- Specific implementation behavior

Do not fabricate evidence.

Do not invent:

- File names
- Flow names
- Line numbers
- Configuration names
- Property names
- Connector usage
- MUnit tests
- Security controls

If exact line numbers are not reliably available, omit them.

---

## 8. No Secret Disclosure

Never include actual sensitive values in a finding.

Never report:

- Password values
- API keys
- Tokens
- Client secrets
- Private keys
- Encryption keys
- Secure property values

Instead report:

- File location
- Property name
- Type of secret
- Security problem
- Recommended remediation

Example:

`application-prod.yaml contains a database password in plain text.`

Do not include the password itself.

---

## 9. Every Problem Requires a Solution

A finding is incomplete if it only states that something is wrong.

Every problem or warning must provide a practical solution.

The solution should explain:

- What should change
- Why it should change
- Where the change should be made
- The recommended MuleSoft approach
- Important implementation considerations

Avoid vague recommendations such as:

- "Improve this."
- "Follow best practices."
- "Optimize this."
- "Use better security."

Instead provide actionable remediation.

---

## 10. Solution Quality

Solutions must be appropriate for the actual implementation.

Do not recommend:

- Unnecessary rewrites
- Unnecessary new components
- Over-engineering
- Technologies not justified by the application
- Architecture changes without explaining the benefit
- Performance optimizations without evidence of a relevant bottleneck

Prefer the simplest solution that appropriately addresses the identified problem.

---

## 11. Duplicate Finding Prevention

Multiple specialist reviewers may identify the same underlying issue.

The final reviewer must consolidate duplicate findings.

For example, if:

- Security Reviewer identifies plain-text password
- Configuration Reviewer identifies the same plain-text password

the final report must contain one consolidated security finding.

Do not create two separate findings for the same root cause.

---

## 12. Root Cause over Symptoms

Prefer reporting the underlying problem rather than multiple symptoms.

Example:

If one connector configuration is duplicated across ten flows, do not create ten separate findings.

Create one finding identifying:

- The duplicated configuration
- The affected flows
- The architectural impact
- The recommended centralized configuration

---

## 13. Related Findings

Separate findings may be created when problems are genuinely different.

For example:

1. Missing connector timeout
2. Missing retry strategy
3. Plain-text credentials

These may be separate findings because they represent different risks and remediation actions.

However, if they are all consequences of the same configuration design problem, consider consolidating them.

---

## 14. Positive Findings

The review should identify meaningful positive practices where appropriate.

Examples:

- Good global connector configuration reuse
- Strong MUnit coverage
- Effective error handling
- Good secure-property implementation
- Appropriate correlation ID usage
- Efficient DataWeave
- Good API security controls
- Strong architecture separation

Positive observations should be concise.

Do not create excessive positive findings simply to make the report appear balanced.

---

## 15. MUnit Findings

Missing MUnit coverage should normally be reported as a Warning.

The finding should identify:

- Flow/process without appropriate tests
- Why the flow is important
- Risk of missing automated validation
- Recommended test scenarios
- Suggested MUnit implementation approach

Do not invent coverage percentages.

Only report numeric coverage when reliable coverage information is available.

---

## 16. Security Findings

Security issues must be prioritized appropriately.

Examples include:

- Plain-text passwords
- Unprotected credentials
- Exposed tokens
- Sensitive information in logs
- Weak API security
- Sensitive information in error responses
- Insecure configuration

All passwords and sensitive credentials must be protected using the approved MuleSoft Secure Configuration Properties mechanism.

Never expose the actual credential in the report.

If a real credential appears to be exposed, recommend rotating it as part of remediation.

---

## 17. API Security Findings

Do not assume that an API is unsecured merely because API Manager policies are not present in the repository.

Classify the situation appropriately:

### Confirmed

Repository evidence demonstrates that the required control is absent or incorrectly implemented.

### Verification Required

The repository does not contain sufficient evidence because the control may be managed externally.

### Satisfactory

Repository evidence demonstrates appropriate security implementation.

Do not convert "not visible in source" into a confirmed security vulnerability without evidence.

---

## 18. Performance Findings

Performance findings must be based on identifiable implementation characteristics.

Examples include:

- Repeated unnecessary connector calls
- Inefficient transformations
- Large payload duplication
- Missing streaming where clearly appropriate
- Poor connection management
- Missing timeout configuration
- Inefficient sequential processing
- Excessive logging
- Unnecessary repeated DataWeave processing

Do not claim a performance problem merely because an optimization could theoretically exist.

Explain the expected impact.

---

## 19. Connector Findings

Connector findings should consider the specific connector and usage pattern.

Review:

- Global configuration
- Duplicate configuration
- Timeout
- Retry/reconnection
- Pooling
- Authentication
- Resource management
- Performance
- Error handling

Do not recommend connector settings that are inappropriate for the connector or workload.

---

## 20. Configuration Findings

Configuration findings should consider:

- Property usage
- Environment consistency
- Duplicate configuration
- Missing configuration
- Hardcoded values
- Secure properties
- Configuration drift

Do not classify legitimate environment-specific values as defects.

For potentially unused properties, verify whether they may be dynamically referenced before reporting them.

---

## 21. Logging Findings

Logging findings should focus on operational usefulness.

Assess whether production support can determine:

- What happened
- Where processing occurred
- Which transaction was involved
- Where failure occurred
- Which external system was involved

Also consider:

- Excessive logging
- Missing logging
- Incorrect log levels
- Duplicate logging
- Sensitive data exposure
- Payload logging

Do not recommend logging complete payloads by default.

---

## 22. Architecture Findings

Architecture findings must be based on the architecture actually implemented.

Do not penalize an application merely because it does not use a particular architecture pattern.

If recommending architectural changes, explain:

- Current architecture
- Observed limitation
- Business/technical impact
- Recommended architecture
- Migration or implementation approach

---

## 23. Finding Priority

When multiple findings exist, prioritize according to:

1. Security
2. Production reliability
3. Data protection
4. API security
5. Performance
6. Resilience
7. Architecture
8. Maintainability
9. Testing
10. Naming/style

Severity and priority are not necessarily identical.

A Medium issue affecting a critical production flow may deserve higher remediation priority than a High issue in an unused component.

Use technical context.

---

## 24. Finding Consolidation

Before generating the final report:

1. Collect findings from all reviewers.
2. Remove duplicates.
3. Merge related findings where appropriate.
4. Validate evidence.
5. Validate severity.
6. Validate recommendations.
7. Validate solutions.
8. Ensure each Finding ID is unique.
9. Ensure no finding exposes secrets.
10. Ensure insignificant findings are removed.

The final report must represent a coherent architectural assessment rather than a collection of independent agent outputs.

---

## 25. Final Finding Quality Gate

A finding must not appear in the final report unless it answers all applicable questions:

- What is wrong?
- Where is it?
- What evidence supports it?
- Why does it matter?
- What is the impact?
- How severe is it?
- What should be done?
- How should it be fixed?
- Is the recommendation appropriate for this application?

If these questions cannot be answered, downgrade the finding to a Warning/Verification Required or remove it.

---

## 26. Review Objective

The objective is not to produce the largest possible number of findings.

The objective is to produce a technically accurate, architect-level assessment that gives the development and architecture teams a clear understanding of:

- What is working well
- What is risky
- What should be improved
- Why it matters
- How to fix it
- What should be prioritized first