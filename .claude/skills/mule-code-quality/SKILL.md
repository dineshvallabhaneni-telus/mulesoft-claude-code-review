# MuleSoft Code Quality Analysis Skill

## Purpose

Perform a comprehensive MuleSoft code-quality review of the application.

Review the application as a:

- Senior MuleSoft Architect
- Senior Technical Lead
- Integration Architect

The objective is to determine whether the MuleSoft implementation is:

- Clean
- Maintainable
- Readable
- Consistent
- Robust
- Modular
- Correctly designed
- Aligned with MuleSoft development best practices

The review must go beyond formatting.

Review:

- Naming
- Flow design
- XML structure
- DataWeave
- Variables
- Attributes
- Error handling
- Validation
- Routing
- Transformations
- Maintainability
- Complexity
- Code smells
- Custom code
- Resource organization

Do not report trivial stylistic differences unless they materially affect maintainability or consistency.

Every meaningful finding MUST include:

- Evidence
- Impact
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

# 3. Application Files

Review at minimum:

- pom.xml
- mule-artifact.json
- src/main/mule/**
- src/main/resources/**
- src/main/java/**
- src/main/python/**
- src/test/**

Review other source directories if they are part of the MuleSoft application.

---

# 4. Naming Standards

Review naming of:

- Applications
- Files
- Flows
- Subflows
- Private flows
- Variables
- Attributes
- Global configurations
- Parameters
- DataWeave functions
- DataWeave modules
- Java classes
- Java methods
- Python files/functions
- Property files
- Resources

Naming should clearly communicate purpose.

---

# 5. Flow Naming

Flow names should indicate business or technical purpose.

Prefer:

processCustomerOrder

over:

flow1

or:

processData

Report ambiguous names when they make maintenance difficult.

Do not enforce a particular naming style if the project already has a consistent standard.

---

# 6. File Naming

Review Mule XML file names.

Look for:

- Generic names
- Inconsistent naming
- Names unrelated to functionality
- Duplicate/ambiguous names

Examples of weak names:

- common.xml
- test.xml
- temp.xml
- flow.xml

Only report when the naming materially reduces maintainability.

---

# 7. Folder Organization

Evaluate whether source files are logically organized.

Consider separation by:

- API
- Domain
- Integration
- Shared utilities
- Global configuration
- Error handling
- Security
- Resources

Do not force a particular architecture if the current structure is coherent.

---

# 8. Flow Size

Identify excessively large flows.

Consider:

- Number of processors
- Nested scopes
- Conditional complexity
- Transformation complexity
- Error handling complexity

Do not use an arbitrary processor-count threshold.

Assess readability and maintainability.

---

# 9. Flow Complexity

Identify flows with excessive:

- Choice branches
- Nested scopes
- Nested Try scopes
- For Each nesting
- Conditional expressions
- Transformations
- Error handling

Explain how complexity affects maintenance.

---

# 10. Nested Flow Complexity

Identify deeply nested structures such as:

Flow
  Try
    Choice
      For Each
        Try
          Choice

Deep nesting should be reported only when it materially reduces readability or increases defect risk.

---

# 11. Modularization

Determine whether large processing logic can reasonably be separated into:

- Private flows
- Subflows
- Reusable DataWeave functions
- Modules

Do not recommend splitting every flow into small pieces.

---

# 12. Reusable Logic

Identify logic that is clearly reusable.

Examples:

- Common validation
- Common response creation
- Common error mapping
- Common header preparation
- Common transformation

Coordinate duplication findings with duplication-analysis.

---

# 13. Variables

Review variable usage.

Look for:

- Excessive variables
- Variables used only once
- Variables that could be replaced by expressions
- Variables carrying large payloads
- Confusing variable names
- Variables overwritten unnecessarily

Do not report a variable merely because it exists.

---

# 14. Variable Naming

Variable names should communicate purpose.

Avoid:

- temp
- data
- result
- obj
- x
- var1

unless context makes them genuinely clear.

---

# 15. Variable Scope

Review whether variables are created at an appropriate scope.

Look for:

- Variables unnecessarily created at broad scope
- Variables overwritten unexpectedly
- Variables used across unrelated processing
- Confusing variable lifecycle

---

# 16. Attributes

Review attribute usage.

Determine whether attributes are:

- Used appropriately
- Preserved where needed
- Recreated unnecessarily
- Confused with payload or variables

Do not report valid Mule event behavior as a defect.

---

# 17. Payload Management

Review payload manipulation.

Look for:

- Unnecessary payload conversions
- Repeated transformations
- Large payload duplication
- Payload being transformed back and forth unnecessarily

Coordinate performance impact with performance-analysis.

---

# 18. DataWeave Quality

Review DataWeave for:

- Readability
- Correctness
- Reusability
- Null handling
- Type handling
- Complexity
- Hard-coded values
- Repeated logic

---

# 19. DataWeave Naming

Review:

- Variables
- Functions
- Parameters
- Modules

Names should communicate intent.

Avoid unexplained abbreviations.

---

# 20. DataWeave Complexity

Identify excessively complex DataWeave.

Examples:

- Very long expressions
- Deep nested maps
- Multiple nested conditionals
- Repeated transformations
- Difficult-to-follow functions

Recommend simplification or modularization.

---

# 21. DataWeave Null Handling

Review handling of:

- Null
- Missing fields
- Empty strings
- Empty arrays
- Empty objects

Do not report null handling as a defect unless the implementation creates a realistic failure or incorrect result.

---

# 22. Data Type Handling

Review potential type problems involving:

- String
- Number
- Boolean
- Date
- DateTime
- Array
- Object
- Null

Identify implicit conversions that may produce unexpected behavior.

---

# 23. Hard-Coded Values

Identify hard-coded values that should reasonably be configurable.

Examples:

- URLs
- Ports
- Timeouts
- Retry counts
- Environment identifiers
- Queue names
- File paths

Do not externalize true constants unnecessarily.

---

# 24. Magic Values

Identify unexplained:

- Numbers
- Strings
- Status codes
- Error codes
- Retry values
- Timeout values

Recommend named constants or properties where appropriate.

---

# 25. Expression Complexity

Review expressions embedded directly inside processors.

If expressions become difficult to read or maintain, recommend:

- Named variables
- DataWeave functions
- Reusable modules
- Private flows

Use judgment.

---

# 26. Choice Routing

Review Choice scopes.

Look for:

- Too many branches
- Duplicate conditions
- Complex conditions
- Unreachable branches
- Missing default behavior where appropriate

Do not report a large Choice solely because it has many branches.

---

# 27. Conditional Logic

Review:

- `if`
- `else`
- `else if`
- Choice
- Filters
- Expressions

Look for:

- Duplicate conditions
- Contradictory conditions
- Unreachable logic
- Complex nested conditions

---

# 28. Unreachable Logic

Identify processors or branches that appear unreachable.

Examples:

- Condition can never be true
- Branch is shadowed by previous condition
- Processor follows unconditional termination

Use:

Verification Required

if static analysis cannot prove reachability.

---

# 29. Default Branches

Where routing requires a fallback, determine whether a default path exists.

Examples:

- Choice
- Routing
- Dynamic configuration

Do not require a default branch when absence is intentionally handled elsewhere.

---

# 30. Error Handling

Review:

- On Error Continue
- On Error Propagate
- Try
- Error handlers
- Global error handlers

Look for:

- Swallowed errors
- Excessive duplication
- Incorrect error scope
- Generic error handling
- Missing contextual response

Detailed error-analysis may overlap with architecture and logging.

---

# 31. Swallowed Errors

Identify errors that appear to be caught and ignored.

Examples:

On Error Continue

with no meaningful:

- Response
- Logging
- Recovery
- Compensation

Do not report intentional error handling if the flow clearly implements a valid fallback.

---

# 32. Error Type Handling

Review whether errors are handled at an appropriate level.

Look for:

- Overly broad error handling
- Generic ANY errors when specific handling is possible
- Incorrectly grouped errors

Do not require specific error types where behavior is intentionally identical.

---

# 33. Validation

Review validation of important inputs.

Look for:

- Missing required fields
- Invalid formats
- Invalid ranges
- Invalid states
- Missing identifiers

Do not duplicate API security findings.

---

# 34. Validation Location

Validation should occur at an appropriate boundary.

Examples:

- API input validation near entry
- Business validation before business operation
- Connector-specific validation before integration

Avoid unnecessary repeated validation.

---

# 35. Connector Error Handling

Review whether important connector calls have appropriate error behavior.

Examples:

- HTTP
- Database
- SFTP
- Messaging
- Salesforce

Detailed connector configuration belongs to connector-analysis.

---

# 36. Transaction Handling

Review transaction-related processing where visible.

Look for:

- Incorrect transaction scope
- Operations that should be atomic but are not
- Long transaction boundaries
- Unnecessary transaction scope

Do not claim transactional correctness without sufficient implementation evidence.

---

# 37. Transaction Boundaries

Determine whether transaction scope matches business behavior.

Consider:

- Database operations
- Messaging
- Multiple side effects

If business semantics are unclear, use:

Verification Required

---

# 38. Loop Quality

Review:

- For Each
- Parallel For Each
- Until Successful
- Batch
- Iterative processing

Look for:

- Unnecessary nested loops
- Expensive operations inside loops
- Repeated connector calls
- Excessive logging
- Large payload operations

Coordinate performance findings with performance-analysis.

---

# 39. Loop Variable Naming

Loop variables should clearly identify what they represent.

Avoid generic names such as:

item

data

x

when more descriptive names are practical.

Do not report simple `item` usage as a defect automatically.

---

# 40. Parallel Processing

Review Parallel For Each and parallel patterns.

Determine whether:

- Operations are independent
- Shared state creates risk
- Ordering matters
- External systems can handle concurrency

Detailed performance analysis belongs to performance-analysis.

---

# 41. Async Processing

Review asynchronous processing.

Look for:

- Lost errors
- Missing correlation
- Shared mutable state
- Unexpected ordering assumptions

Do not classify asynchronous processing as bad by default.

---

# 42. Scheduler Design

Review scheduled flows.

Look for:

- Long-running work
- Overlapping executions
- Missing safeguards
- Unclear error handling
- Hard-coded scheduling behavior

Do not claim overlapping execution is possible unless configuration/evidence supports it.

---

# 43. File Processing

Review file-processing logic.

Look for:

- Duplicate file processing
- Hard-coded paths
- Missing archive/error handling
- Large file handling
- Inefficient transformations

Detailed connector configuration belongs to connector-analysis.

---

# 44. API Flow Quality

Review API flows for:

- Clear separation of concerns
- Validation
- Business logic separation
- Response handling
- Error handling
- Reusable integration logic

---

# 45. API Layer Separation

Determine whether API implementation unnecessarily mixes:

- Transport
- Validation
- Business logic
- Integration
- Persistence

Where separation would materially improve maintainability, recommend a layered design.

---

# 46. Business Logic Separation

Business rules should not be unnecessarily embedded inside:

- HTTP listener configuration
- Connector configuration
- Logging
- Error response formatting

Recommend separation where complexity warrants it.

---

# 47. Integration Layer Separation

External integration logic should be reusable where appropriate.

Avoid duplicating:

- Request construction
- Authentication
- Connector invocation
- Response mapping
- Error mapping

Coordinate duplication findings with duplication-analysis.

---

# 48. Utility Logic

Identify utility functions that are:

- Repeated
- Overly complex
- Misplaced
- Implemented using unnecessary custom code

Consider MuleSoft/DataWeave built-in capabilities before recommending custom utility code.

---

# 49. Custom Java

Identify Java code.

Review whether custom Java is:

- Necessary
- Maintainable
- Properly isolated
- Reusable
- Exception-safe

Determine whether MuleSoft/DataWeave can replace simple custom Java functionality.

Do not recommend removing Java solely because it is custom.

---

# 50. Custom Python

Identify Python/custom scripting where present.

Review:

- Necessity
- Maintainability
- Error handling
- Security
- Deployment implications

Determine whether MuleSoft/DataWeave built-in functionality can replace simple custom code.

---

# 51. Resource Usage

Review resource references.

Look for:

- Hard-coded paths
- Incorrect resource references
- Duplicate resources
- Unused resources
- Environment coupling

Do not claim a resource is unused when dynamic references may exist.

---

# 52. Comments

Evaluate comments.

Good comments explain:

- Why
- Business constraint
- Non-obvious behavior
- Workaround
- Important architectural decision

Avoid requiring comments for obvious code.

---

# 53. Dead Code

Identify:

- Unused flows
- Unused subflows
- Unreachable branches
- Commented-out production code
- Unused variables
- Unused resources

Use:

Potentially Unused

when static analysis cannot prove usage.

---

# 54. Commented-Out Code

Report large blocks of commented-out executable code when they create maintenance confusion.

Recommend removing obsolete code and relying on source control history.

Do not report ordinary comments.

---

# 55. XML Quality

Review Mule XML for:

- Clear structure
- Consistent formatting
- Excessive nesting
- Duplicate namespaces
- Unnecessary configuration
- Maintainability

Do not report formatting-only issues unless they materially reduce readability.

---

# 56. Namespace Management

Review whether XML namespaces are:

- Correct
- Necessary
- Consistently declared

Do not report valid namespace declarations as unnecessary without evidence.

---

# 57. Processor Ordering

Review processor sequence.

Identify ordering that appears suspicious.

Examples:

- Transformation occurs before validation when validation expects original structure
- Logging occurs after data is destroyed
- Connector call occurs before required validation

Use evidence from implementation.

---

# 58. Side Effects

Identify side effects such as:

- Database writes
- External API calls
- File writes
- Message publishing

Review whether they occur at appropriate points in the flow.

---

# 59. Idempotency Indicators

For operations that may be retried or replayed, consider whether the implementation appears idempotent.

Examples:

- Database insert
- Message publish
- External POST

Do not claim an operation is non-idempotent without evidence.

Use:

Verification Required

when necessary.

---

# 60. Maintainability Smells

Identify:

- Giant flows
- Giant DataWeave scripts
- Excessive nesting
- Repeated logic
- Generic naming
- Hard-coded configuration
- Broad error handling
- Complex expressions
- Unnecessary custom code

Prioritize meaningful issues.

---

# 61. Code Quality Finding Format

Every finding MUST contain:

## Finding ID

Example:

MULE-CODE-001

## Title

Concise code-quality issue.

## Severity

High / Medium / Low / Warning

## Category

Code Quality

## Location

Exact file, flow, processor, or function.

## Evidence

Observed implementation.

## Impact

Explain why it matters.

## Recommendation

What should be changed.

## Solution

Provide practical MuleSoft-specific implementation guidance.

## Priority

Immediate / Short Term / Medium Term / Long Term

---

# 62. Severity Guidelines

## High

Code-quality problem likely to cause:

- Production defects
- Data corruption
- Major maintainability problems
- Serious runtime behavior problems

## Medium

Meaningful maintainability, reliability, or correctness issue.

## Low

Minor improvement.

## Warning

Potential issue requiring verification.

Do not inflate severity.

---

# 63. Naming Findings

Do not create separate findings for every poor name.

Group related naming problems where appropriate.

Example:

"Flow and variable naming is inconsistent across the customer domain."

Then provide representative evidence and a naming standard.

---

# 64. Code Quality Solutions

Solutions must be actionable.

Weak:

"Improve code quality."

Strong:

"Extract the repeated customer validation and response construction into a reusable private flow, leaving the API flow responsible for transport-level validation and delegation."

---

# 65. Positive Code Quality Observations

Identify good practices such as:

- Clear flow naming
- Good modularization
- Appropriate DataWeave usage
- Clean error handling
- Proper validation
- Reusable components
- Clear separation of API/business/integration concerns
- Minimal custom code
- Maintainable transformations

---

# 66. Cross-Skill Boundaries

Detailed findings owned by these skills should not be duplicated unnecessarily:

- mulesoft-architecture
- connector-analysis
- api-security-analysis
- security-analysis
- performance-analysis
- munit-analysis
- configuration-analysis
- logging-analysis
- duplication-analysis
- word-report-generation

This skill owns general MuleSoft implementation quality and maintainability.

If duplicate logic is identified:

- mule-code-quality may identify the maintainability concern.
- duplication-analysis owns the detailed duplication finding.

If a connector is incorrectly configured:

- connector-analysis owns the connector finding.

If a performance issue is identified:

- performance-analysis owns the detailed performance finding.

If a security problem is identified:

- security-analysis owns the security finding.

The final report reviewer must consolidate duplicate root causes.

---

# 67. No Unsupported Claims

Never claim:

- A flow is incorrect without implementation evidence.
- A custom Java implementation is unnecessary without identifying a viable MuleSoft alternative.
- A transaction is incorrect without understanding the business operation.
- A variable is unnecessary solely because it is assigned once.
- A flow is too large solely because it contains many processors.

Use:

Verification Required

where static analysis cannot establish intent.

---

# 68. Code Quality Score

Provide a code-quality score based on:

- Readability
- Naming
- Modularity
- Maintainability
- DataWeave quality
- Error handling
- Validation
- Complexity
- Custom code usage
- Separation of concerns
- Dead-code indicators

Do not calculate the score solely from finding count.

---

# 69. Final Output

Return structured code-quality analysis containing:

## Code Quality Summary

## Naming Assessment

## Flow Structure Assessment

## Modularity Assessment

## Variable Assessment

## Attribute Assessment

## DataWeave Assessment

## Error Handling Assessment

## Validation Assessment

## Routing Assessment

## Loop Assessment

## Transaction Assessment

## Custom Java Assessment

## Custom Python Assessment

## Resource Assessment

## Dead Code Assessment

## Maintainability Assessment

## Positive Code Quality Observations

## Code Quality Findings

## Recommended Refactoring

## Verification Required

## Code Quality Score

Do not generate the final Word document from this skill.

The word-report-generation skill is responsible for creating the final .docx.

---

# 70. Quality Standard

Before completing the review, ask:

"Would a Senior MuleSoft Architect consider these findings meaningful for long-term production maintainability and reliability?"

If not:

- Remove trivial style findings.
- Re-check the implementation.
- Avoid arbitrary coding rules.
- Distinguish real defects from preferences.
- Provide MuleSoft-specific solutions.
- Prioritize correctness, maintainability, reliability, and architectural clarity.

The objective is production-quality MuleSoft code review, not a generic static-analysis checklist.