# MuleSoft Duplication Analysis Skill

## Purpose

Perform a comprehensive duplication analysis of the MuleSoft application.

Review the application as a:

- Senior MuleSoft Architect
- Senior Technical Lead
- Integration Architect

The objective is to identify meaningful duplication that increases:

- Maintenance effort
- Defect risk
- Configuration drift
- Code complexity
- Runtime overhead
- Inconsistent behavior
- Testing effort

The review must distinguish between:

- True duplication
- Intentional repetition
- Similar but legitimately different implementations

Do not report duplication merely because two pieces of code look similar.

Every meaningful finding MUST include:

- Evidence
- Impact
- Recommendation
- Practical solution

Do not report trivial duplication that has no meaningful architectural or maintenance impact.

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

# 3. Duplication Discovery

Analyze duplication across:

- Flows
- Subflows
- Private flows
- Variables
- Logger statements
- DataWeave transformations
- Connector configurations
- Global configurations
- Error handlers
- Choice branches
- Validation logic
- Retry logic
- HTTP configurations
- Database configurations
- Property definitions
- MUnit setup
- Test data
- Custom Java code
- Custom Python code where present

---

# 4. Flow Duplication

Identify flows that implement substantially identical processing.

Compare:

- Processors
- Order of operations
- Conditions
- Transformations
- Connector calls
- Error handling
- Logging
- Variables

Do not classify two flows as duplicates solely because they contain the same connector.

---

# 5. Near-Duplicate Flows

Identify flows that differ only by small variations.

Examples:

Flow A:

- Validate
- Transform
- HTTP request
- Log

Flow B:

- Validate
- Transform
- HTTP request
- Log

with only endpoint differences.

Determine whether they should share reusable logic.

---

# 6. Subflow Opportunities

Identify repeated processor sequences that could reasonably become a reusable subflow.

Examples:

- Standard validation
- Common error preparation
- Common response mapping
- Common audit logging
- Common header preparation

Do not recommend extracting tiny sequences where abstraction would make the application harder to understand.

---

# 7. Private Flow Opportunities

Determine whether repeated logic is better represented as a private flow rather than duplicated across multiple flows.

Consider:

- Reuse
- Input/output behavior
- Coupling
- Maintainability

---

# 8. Duplicate DataWeave

Identify repeated DataWeave transformations.

Look for:

- Same mappings
- Same filtering logic
- Same formatting logic
- Same null handling
- Same utility functions

Do not report similar mappings when business semantics are different.

---

# 9. DataWeave Utility Opportunities

Determine whether common DataWeave logic could be centralized.

Potential approaches:

- Reusable DataWeave modules
- Functions
- Shared transformations
- Common modules

Recommend the least-complex maintainable approach.

---

# 10. Duplicate Variables

Identify repeated variables that represent the same logical value.

Examples:

- customerId
- custId
- customerIdentifier

Determine whether these are truly the same concept.

Do not report naming differences alone unless they create meaningful inconsistency.

---

# 11. Duplicate Variable Initialization

Identify repeated initialization patterns.

Examples:

vars.transactionId
vars.correlationId
vars.startTime

If the same initialization occurs across many flows, determine whether a reusable mechanism would improve maintainability.

---

# 12. Duplicate Logger Statements

Identify repeated logging patterns.

Examples:

- Same start message
- Same completion message
- Same error message
- Same payload logging

Do not report logging repetition that is appropriate for independent flows.

The logging-analysis skill owns detailed logging recommendations.

---

# 13. Duplicate Connector Configuration

Identify repeated configurations such as:

- HTTP Request
- HTTP Listener
- Database
- SFTP
- Salesforce
- JMS
- Kafka
- VM
- Object Store

Determine whether multiple configurations represent the same logical connection.

Recommend reusable global configurations where appropriate.

The connector-analysis and configuration-analysis skills own detailed connector/configuration findings.

---

# 14. Duplicate Global Configurations

Identify multiple global configurations that appear to represent the same system.

Examples:

customerDbConfig1
customerDbConfig2

when both connect to the same logical database.

Review:

- Endpoint
- Credentials/reference
- Timeout
- Pool
- TLS
- Reconnection

Do not merge configurations if their behavior is intentionally different.

---

# 15. Duplicate Error Handlers

Identify repeated error-handler logic.

Examples:

- Same error mapping
- Same logging
- Same response transformation
- Same error variable initialization

Determine whether a reusable global or shared pattern is appropriate.

Do not recommend abstraction if error semantics differ materially.

---

# 16. Duplicate Choice Logic

Identify repeated conditional logic.

Example:

if status == "ACTIVE"
else if status == "INACTIVE"
else

If identical business rules appear in multiple locations, consider centralizing the rule.

---

# 17. Duplicate Validation

Identify repeated validation rules.

Examples:

- Required customer ID
- Required order ID
- Email format
- Amount validation
- Status validation

Determine whether validation should be centralized.

Do not centralize validations that intentionally apply different business rules.

---

# 18. Duplicate Retry Logic

Identify repeated custom retry implementations.

Examples:

- Same Until Successful settings
- Same retry counter
- Same error handling
- Same delay logic

Determine whether common configuration or reusable logic is appropriate.

Coordinate detailed retry/performance recommendations with performance-analysis.

---

# 19. Duplicate Timeout Configuration

Identify repeated timeout values/configuration across logically related connectors.

Do not assume identical timeout values are bad.

Report duplication only when configuration is unnecessarily repeated and could lead to drift.

---

# 20. Duplicate Property Definitions

Identify logically duplicated properties.

Examples:

customer.api.url
customer.api.base-url

or:

db.connection.timeout
database.timeout

Determine whether they represent the same concept.

Do not report legitimate aliases without evidence.

---

# 21. Duplicate Property Values

Identify repeated hard-coded values across configuration files.

Examples:

Same URL repeated in multiple places.

Determine whether the value should be centralized.

Do not report values that are intentionally repeated and stable constants.

---

# 22. Environment Configuration Duplication

Identify duplicated configuration across:

- DEV
- QA
- UAT
- PROD

Distinguish:

Environment-specific value

from:

Duplicated configuration structure.

Do not report the existence of separate environment files as duplication by itself.

---

# 23. Duplicate Security Configuration

Identify repeated security-related configuration.

Examples:

- Same TLS configuration
- Same authentication configuration
- Same secure property setup

Coordinate detailed security findings with security-analysis.

---

# 24. Duplicate Transformation Logic

Look for repeated transformations between:

- JSON
- XML
- Java objects
- Database results
- API models

Determine whether shared mapping logic would reduce maintenance risk.

---

# 25. Duplicate Response Mapping

Identify repeated response/error mapping.

Examples:

Same:

status
code
message
correlationId

being constructed independently across many flows.

Recommend centralization only where the response contract is genuinely shared.

---

# 26. Duplicate Request Preparation

Identify repeated request-building logic.

Examples:

- Headers
- Query parameters
- Authentication metadata
- Common request body structure

Determine whether reusable request preparation would improve consistency.

---

# 27. Duplicate Integration Calls

Identify cases where multiple flows invoke the same external system using substantially identical logic.

Determine whether a shared integration layer/private flow would improve:

- Consistency
- Error handling
- Logging
- Retry behavior
- Testing

Do not force all integrations through a common abstraction.

---

# 28. Duplicate Business Logic

Identify business rules implemented in multiple locations.

Examples:

- Customer eligibility
- Status calculation
- Amount calculation
- Routing decision
- Date calculation

This is a high-value duplication category.

Recommend centralizing business rules when duplication can cause inconsistent behavior.

---

# 29. Duplicate Constants

Identify repeated constants that should reasonably be centralized.

Examples:

- Status values
- Error codes
- Common headers
- System identifiers

Do not centralize every string in the application.

---

# 30. Duplicate Error Codes

Identify repeated error codes/messages that may have inconsistent meanings.

Look for:

- Same code with different messages
- Different codes representing the same condition
- Repeated hard-coded error structures

Recommend standardization where appropriate.

---

# 31. Duplicate Logging Context

Identify repeated construction of:

- correlationId
- transactionId
- businessId
- operationName

If the same context is manually built in many flows, determine whether a common approach is appropriate.

---

# 32. Duplicate MUnit Setup

Analyze MUnit tests for repeated:

- Mock definitions
- Test data
- Setup
- Assertions
- Variables

Determine whether reusable test utilities would improve maintainability.

Do not over-abstract simple tests.

---

# 33. Duplicate MUnit Tests

Identify tests that validate substantially identical scenarios.

Compare:

- Inputs
- Mock behavior
- Expected output
- Assertions

Do not classify tests as duplicates merely because they use similar setup.

The munit-analysis skill owns detailed testing recommendations.

---

# 34. Duplicate Custom Code

Identify repeated Java/Python/custom implementations of the same functionality.

Examples:

- Same utility method
- Same conversion
- Same validation
- Same formatting

Determine whether the functionality should be:

- Reused
- Centralized
- Replaced with Mule/DataWeave functionality

---

# 35. MuleSoft Built-In Alternative

When duplicate custom code exists, determine whether MuleSoft built-in capabilities can replace it.

Consider:

- DataWeave
- Mule validators
- Choice
- Transform Message
- Built-in connectors
- Mule error handling
- Existing modules

Do not recommend custom code removal if the built-in functionality cannot provide equivalent behavior.

---

# 36. Duplicate Connector Calls

Identify cases where the same external system is called multiple times unnecessarily within a processing path.

Examples:

- Same customer lookup repeated
- Same configuration endpoint queried repeatedly
- Same metadata retrieved multiple times

Determine whether caching, variable reuse, or flow redesign could eliminate unnecessary calls.

Coordinate performance impact with performance-analysis.

---

# 37. Duplicate Database Queries

Identify repeated identical or near-identical database operations.

Consider:

- Same query
- Same parameters
- Same record lookup

Determine whether the result can safely be reused.

Do not recommend reuse when the underlying data may intentionally need to be refreshed.

---

# 38. Duplicate HTTP Calls

Identify repeated calls to the same endpoint with the same or equivalent request.

Consider:

- Same endpoint
- Same parameters
- Same headers
- Same payload

Determine whether duplicate calls are intentional.

---

# 39. Duplicate File Operations

Identify repeated file operations.

Examples:

- Same file lookup
- Same file read
- Same parsing
- Same movement/archive logic

Recommend reusable processing where appropriate.

---

# 40. Duplicate Message Processing

Identify repeated messaging logic.

Examples:

- Same publish preparation
- Same acknowledgment logic
- Same error handling

Determine whether common logic can be reused safely.

---

# 41. Duplication and Performance

Determine whether duplication causes runtime overhead.

Examples:

- Repeated transformations
- Repeated connector calls
- Repeated database queries
- Repeated external API calls
- Repeated large payload serialization

Coordinate detailed performance findings with performance-analysis.

---

# 42. Duplication and Reliability

Determine whether duplicated logic can cause inconsistent behavior.

Examples:

Flow A:

timeout = 10 seconds

Flow B:

timeout = 30 seconds

when both implement the same integration.

Report configuration drift only when it creates meaningful risk.

---

# 43. Duplication and Security

Determine whether duplicated security configuration creates inconsistent protection.

Examples:

- One flow validates authentication
- Another equivalent flow does not

Do not duplicate the full security finding.

Coordinate with security-analysis and api-security-analysis.

---

# 44. Duplication and Logging

Determine whether duplicated logging patterns create:

- Excessive volume
- Inconsistent context
- Duplicate errors

Coordinate detailed logging recommendations with logging-analysis.

---

# 45. Duplication Classification

Classify duplication as:

- Exact duplication
- Near duplication
- Structural duplication
- Configuration duplication
- Logic duplication
- Data duplication
- Test duplication
- Runtime duplication

---

# 46. Duplication Confidence

Assign confidence:

High

when duplication is clearly equivalent.

Medium

when implementations are highly similar but some semantic verification is required.

Low

when static similarity exists but business intent is unclear.

Do not make strong refactoring recommendations for low-confidence duplication.

---

# 47. Finding Format

Every finding MUST contain:

## Finding ID

Example:

MULE-DUP-001

## Title

Concise duplication issue.

## Severity

High / Medium / Low / Warning

## Category

Duplication

## Duplication Type

Exact / Near / Logic / Configuration / Data / Test / Runtime

## Location

Files, flows, or configurations involved.

## Evidence

Explain why the implementations are considered duplicated.

## Impact

Explain maintenance, reliability, performance, or architectural impact.

## Recommendation

What should be consolidated.

## Solution

Provide a practical MuleSoft implementation approach.

## Confidence

High / Medium / Low

## Priority

Immediate / Short Term / Medium Term / Long Term

---

# 48. Severity Guidelines

## High

Duplication creates significant risk of:

- Conflicting business logic
- Production defects
- Security inconsistency
- Major configuration drift
- Significant unnecessary external calls

## Medium

Duplication creates meaningful maintenance or reliability risk.

## Low

Minor duplication with limited impact.

## Warning

Potential duplication requires business-context verification.

Do not inflate severity.

---

# 49. Refactoring Guidance

When recommending consolidation, explain:

- What should be shared.
- Where the shared implementation should live.
- How callers should use it.
- What behavior must remain unchanged.
- What tests should be added.

Do not provide vague recommendations such as:

"Refactor duplicate code."

---

# 50. Avoid Over-Abstraction

Do not recommend a common subflow solely because two processors are identical.

Consider:

- Reuse frequency
- Complexity
- Business semantics
- Coupling
- Future maintainability

A small amount of intentional duplication may be preferable to excessive abstraction.

---

# 51. Duplication Threshold

Use judgment rather than an arbitrary line-count threshold.

Consider duplication significant when:

- It contains meaningful business logic.
- It is repeated across multiple flows.
- Changes must be made in multiple places.
- Implementations can drift.
- It causes repeated external calls.
- It creates inconsistent behavior.

---

# 52. Positive Duplication Observations

Identify good practices such as:

- Shared subflows
- Reusable DataWeave modules
- Centralized configurations
- Common error handling
- Shared validation
- Reusable integration logic
- Centralized business rules

---

# 53. Cross-Skill Boundaries

Detailed findings owned by these skills should not be duplicated unnecessarily:

- mulesoft-architecture
- mule-code-quality
- connector-analysis
- api-security-analysis
- security-analysis
- performance-analysis
- munit-analysis
- configuration-analysis
- logging-analysis

This skill owns duplication and reuse opportunities.

If duplicate connector configurations exist:

- duplication-analysis identifies the duplication.
- connector-analysis owns detailed connector correctness.
- configuration-analysis owns configuration consistency.

If duplicate logging exists:

- duplication-analysis identifies the repeated implementation.
- logging-analysis owns logging quality.

If duplicate tests exist:

- duplication-analysis identifies duplication.
- munit-analysis owns test quality.

The final report reviewer must consolidate duplicate root causes.

---

# 54. No Unsupported Claims

Never claim two implementations are functionally identical solely because they look similar.

Never recommend merging logic without considering:

- Input differences
- Output differences
- Error behavior
- Security behavior
- Transaction behavior
- Business rules
- Environment behavior

Use:

Verification Required

when business intent cannot be established statically.

---

# 55. Duplication Score

Provide a duplication/reuse score based on:

- Flow reuse
- Business logic reuse
- Configuration reuse
- Transformation reuse
- Connector reuse
- Error-handling reuse
- Test reuse
- Unnecessary repeated runtime operations

Do not calculate the score solely from number of duplicate lines.

---

# 56. Final Output

Return structured duplication analysis containing:

## Duplication Summary

## Flow Duplication Assessment

## Subflow/Private Flow Opportunities

## DataWeave Duplication Assessment

## Configuration Duplication Assessment

## Connector Duplication Assessment

## Business Logic Duplication Assessment

## Variable Duplication Assessment

## Error Handling Duplication Assessment

## Logging Duplication Assessment

## Runtime Duplication Assessment

## MUnit Duplication Assessment

## Custom Code Duplication Assessment

## Positive Reuse Observations

## Duplication Findings

## Recommended Refactoring Opportunities

## Verification Required

## Duplication Score

Do not generate the final Word document from this skill.

The word-report-generation skill is responsible for creating the final .docx.

---

# 57. Quality Standard

Before completing the review, ask:

"Would a Senior MuleSoft Architect agree that these are genuine duplication or reuse problems rather than superficial code similarities?"

If not:

- Remove trivial findings.
- Re-check semantic equivalence.
- Avoid over-abstraction.
- Distinguish intentional repetition from problematic duplication.
- Provide practical MuleSoft-specific solutions.
- Prioritize duplication that can cause inconsistent behavior or unnecessary runtime work.

The objective is production-quality duplication analysis, not a generic similarity scan.