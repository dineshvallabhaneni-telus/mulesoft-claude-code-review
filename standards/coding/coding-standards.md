# File: standards/coding/coding-standards.md

# MuleSoft Coding Standards

## 1. Purpose

This document defines coding standards for MuleSoft applications.

The review must evaluate whether MuleSoft code is:

- Readable
- Maintainable
- Consistent
- Efficient
- Testable
- Reusable
- Secure
- Understandable by another developer
- Aligned with MuleSoft development practices

The review must focus on meaningful code-quality issues.

Do not report stylistic preferences as defects unless they materially affect maintainability, reliability, security, or consistency.

---

## 2. General Coding Principles

MuleSoft code should follow:

- Single responsibility
- Clear naming
- Appropriate abstraction
- Minimal duplication
- Simple control flow
- Explicit error handling
- Appropriate reuse
- Secure configuration
- Predictable behavior

Prefer simple implementations over unnecessarily complex designs.

---

## 3. Readability

Code should be easy for another MuleSoft developer to understand.

Review:

- Flow structure
- Processor ordering
- Variable names
- Configuration names
- DataWeave expressions
- Error handling
- Conditional logic

Avoid unnecessarily complex expressions.

---

## 4. Naming

Names must clearly communicate purpose.

Review naming for:

- Flows
- Subflows
- Variables
- Attributes
- Configurations
- Global elements
- Error handlers
- HTTP requests
- Connectors

Avoid names such as:

- flow1
- testFlow
- temp
- data
- value
- obj
- var1

unless their scope and meaning are obvious.

---

## 5. Flow Naming

Flow names should describe the business or technical operation.

Prefer:

    get-customer-flow

over:

    flow1

For APIs, names should align with the API contract and architectural responsibility.

---

## 6. Subflow Naming

Subflow names should describe the reusable behavior.

Examples:

- validate-customer
- build-error-response
- log-request
- map-customer-response

Avoid generic names such as:

- common-flow
- utility
- helper

when they do not communicate purpose.

---

## 7. Variable Naming

Variables should have meaningful names.

Prefer:

    customerId
    customerResponse
    requestPayload
    correlationId

over:

    x
    data
    obj
    temp
    result

---

## 8. Attribute Usage

Use attributes appropriately.

Avoid unnecessarily copying attributes into variables when the attribute itself is sufficient.

Do not overwrite attributes without understanding downstream impact.

---

## 9. Variable Scope

Variables should be created at the narrowest reasonable scope.

Avoid creating global/shared state when local state is sufficient.

Review variables that:

- Are overwritten repeatedly
- Are passed through many flows
- Contain large payloads
- Contain sensitive information

---

## 10. Payload Management

Avoid unnecessary payload transformations and copies.

Consider:

- Payload size
- Streaming
- Memory consumption
- Number of transformations
- Connector behavior

Do not create intermediate payloads unless they provide meaningful value.

---

## 11. DataWeave Usage

DataWeave should be preferred for transformation and data manipulation where appropriate.

Avoid custom code when equivalent DataWeave functionality is:

- Clearer
- Simpler
- More maintainable
- Supported by MuleSoft

---

## 12. DataWeave Readability

DataWeave scripts should be understandable.

Avoid extremely large expressions containing unrelated logic.

Consider separating complex transformations when doing so improves readability and testability.

---

## 13. DataWeave Functions

Reusable DataWeave functions may be used for repeated transformation logic.

Do not create functions for trivial one-line expressions unless reuse or readability benefits.

---

## 14. Null Handling

Code should intentionally handle possible null values.

Review:

- Missing fields
- Null payloads
- Optional attributes
- Empty arrays
- Missing query parameters
- Missing headers

Avoid unexpected runtime failures caused by null assumptions.

---

## 15. Empty Values

Distinguish appropriately between:

- null
- Empty string
- Empty array
- Empty object
- Missing field

Do not treat all empty values as equivalent unless business rules explicitly allow it.

---

## 16. Conditional Logic

Conditional logic should be clear.

Avoid deeply nested:

- if/else
- choice
- when
- otherwise

structures.

Consider decomposition when complexity materially affects readability.

---

## 17. Choice Router

Choice routers should contain logically related conditions.

Avoid a single Choice router with a very large number of unrelated conditions.

---

## 18. Expression Complexity

Avoid expressions that attempt to perform too many responsibilities at once.

For example, a single expression should not unnecessarily combine:

- Validation
- Transformation
- Filtering
- Business rules
- Error handling

when separation would improve clarity.

---

## 19. Duplicate Logic

Identify repeated code such as:

- Same transformations
- Same validation
- Same error mapping
- Same logging
- Same connector configuration

Consider reuse when duplication creates maintenance risk.

Do not abstract code simply because it appears twice if the behavior is intentionally different.

---

## 20. Dead Code

Identify:

- Unused flows
- Unused subflows
- Unused variables
- Unreachable Choice branches
- Obsolete configurations
- Commented-out implementations

Dead code should be removed unless there is evidence it is intentionally retained.

---

## 21. Comments

Comments should explain:

- Why something is done
- Important business constraints
- Non-obvious technical behavior
- Workarounds
- External limitations

Avoid comments that merely restate the code.

Good comment:

    Use the external CRM identifier because the internal customer ID
    is not accepted by the downstream system.

---

## 22. TODO and FIXME Comments

Review unresolved:

- TODO
- FIXME
- HACK
- TEMP

Do not automatically report every TODO.

Report when the item indicates:

- Security risk
- Incomplete implementation
- Known production defect
- Missing error handling
- Temporary workaround with material impact

---

## 23. Magic Values

Avoid unexplained hard-coded values.

Examples:

- Timeout values
- Retry counts
- Status codes
- File paths
- URLs
- Business thresholds
- Limits

Where appropriate, externalize configurable values.

---

## 24. Hard-Coded URLs

Environment-specific URLs should not normally be hard-coded in Mule flows.

Prefer configuration properties.

---

## 25. Hard-Coded Credentials

Credentials must never be hard-coded.

This includes:

- Passwords
- API keys
- Tokens
- Client secrets
- Private keys

This is a security finding and must also be reviewed against the security standards.

---

## 26. Hard-Coded Business Rules

Business rules should be explicit and maintainable.

Avoid scattering important business thresholds throughout multiple flows.

Where appropriate, centralize or externalize business configuration.

---

## 27. Global Elements

Global elements should be used appropriately.

Examples:

- HTTP Listener Config
- HTTP Request Config
- Database Config
- Salesforce Config
- TLS Config

Avoid duplicating identical global configurations unnecessarily.

---

## 28. Connector Configuration

Connector configurations should be reusable where appropriate.

Review:

- Duplicate configurations
- Connection settings
- Timeouts
- Reconnection
- TLS
- Authentication

Do not merge configurations that intentionally represent different external systems.

---

## 29. HTTP Requests

HTTP Request operations should have appropriate:

- Timeout
- Response handling
- Error handling
- Authentication
- TLS
- Retry behavior

Do not assume connector defaults are always appropriate.

---

## 30. HTTP Request Naming

HTTP request configurations should clearly identify the target system.

Prefer:

    customerSystemHttpRequestConfig

over:

    httpRequestConfig1

---

## 31. Database Operations

Database operations should use appropriate:

- Parameterization
- Connection configuration
- Timeout
- Transaction handling
- Error handling

Avoid unnecessary database calls.

---

## 32. Database Query Construction

Do not construct SQL by concatenating untrusted input.

Prefer parameterized queries.

This should also be reported under security review when applicable.

---

## 33. Repeated Database Calls

Identify patterns such as:

    for each record
        query database

when a bulk operation or more efficient query could reasonably be used.

Do not assume bulk processing is always superior; consider data size and business requirements.

---

## 34. Connector Error Handling

Connector operations should have intentional error handling.

Review:

- Connection errors
- Timeout errors
- Authentication errors
- Validation errors
- Business errors
- Retryable errors

---

## 35. Error Types

Use specific Mule error types where appropriate.

Avoid catching all errors when only a specific category is expected.

---

## 36. Broad Error Handling

Be cautious with:

    MULE:ANY

or equivalent broad error handling.

Broad handlers may hide unexpected failures.

Use them when a deliberate centralized strategy requires it.

---

## 37. Error Propagation

Do not silently suppress important errors.

Pay particular attention to:

- On Error Continue
- Empty error handlers
- Logging without propagation
- Returning successful responses after failures

---

## 38. Try Scope

Try scopes should have a clear purpose.

Avoid wrapping extremely large portions of a flow in one Try scope when more precise error boundaries would improve behavior.

---

## 39. Retry Logic

Retry only errors that are reasonably transient.

Potentially retryable:

- Connection timeout
- Temporary network failure
- Temporary downstream unavailability

Usually not retryable:

- Invalid request
- Authentication failure
- Validation failure
- Business rule violation

---

## 40. Retry Configuration

Retry behavior should consider:

- Maximum attempts
- Backoff
- Timeout
- Idempotency
- Downstream capacity

Avoid infinite retry behavior.

---

## 41. Logging

Logging must provide useful operational information without exposing sensitive information.

Review:

- Log level
- Message clarity
- Correlation ID
- Error context
- Sensitive data masking

Detailed logging requirements are covered by the logging standards and logging skill.

---

## 42. Logging Payloads

Do not log complete payloads by default.

Especially avoid logging:

- Passwords
- Tokens
- API keys
- Personal data
- Financial data
- Authentication headers

---

## 43. Log Levels

Use appropriate log levels.

Typical levels:

- DEBUG
- INFO
- WARN
- ERROR

Avoid using ERROR for normal business events.

Avoid excessive DEBUG logging in production.

---

## 44. Correlation IDs

Important flows should preserve or establish correlation information.

Correlation IDs should help trace a transaction across:

- API
- Mule flows
- External calls
- Errors

---

## 45. Sensitive Variables

Sensitive values should not be unnecessarily stored in variables.

If sensitive values must exist temporarily, minimize their lifetime and prevent them from being logged.

---

## 46. Configuration Properties

Environment-specific configuration should be externalized.

Examples:

- URLs
- Hosts
- Ports
- Credentials
- Queue names
- Database names
- Paths

---

## 47. Property File Formats

Configuration may exist in:

- .properties
- .yaml
- .yml

The review must inspect all applicable configuration files.

Do not assume configuration exists only in .properties files.

---

## 48. Secure Properties

Sensitive configuration should use MuleSoft secure configuration mechanisms where appropriate.

Review whether:

- Sensitive values are encrypted.
- Encryption keys are protected.
- Plain-text duplicates exist.
- Secure property placeholders are used correctly.

---

## 49. XML Structure

Mule XML should remain readable.

Avoid excessively large flows when decomposition would materially improve maintainability.

---

## 50. Processor Ordering

Processors should appear in a logical order.

A typical flow may follow:

1. Receive request
2. Validate
3. Authenticate/authorize where applicable
4. Transform
5. Invoke dependency
6. Process response
7. Return response

Actual ordering depends on business requirements.

---

## 51. Validation

Validate input as early as practical.

Validation should occur before expensive processing when possible.

Do not perform expensive external calls before determining that basic required input is valid.

---

## 52. Business Validation

Business validation should be explicit.

Examples:

- Customer exists
- Order amount is valid
- Status transition is allowed
- Required business relationship exists

Do not hide significant business rules inside unrelated transformation logic.

---

## 53. Technical Validation

Technical validation includes:

- Schema
- Data type
- Format
- Required fields
- Size
- Encoding

Keep technical validation distinguishable from business validation where useful.

---

## 54. Transformation Boundaries

Perform transformations at appropriate integration boundaries.

Avoid repeatedly converting:

    JSON -> XML -> JSON -> XML

without a clear reason.

---

## 55. Payload Format

Use formats appropriate to the interface.

Examples:

- JSON for REST APIs
- XML for SOAP
- CSV for file integrations
- Binary for binary data

Do not convert formats unnecessarily.

---

## 56. Streaming

Use streaming when processing potentially large payloads and when the complete payload is not required in memory.

Avoid disabling streaming unnecessarily.

---

## 57. Large Payloads

Review operations involving:

- Large files
- Large database results
- Large API requests
- Large API responses

Look for unnecessary in-memory processing.

---

## 58. For Each

Use For Each when each record must be processed individually.

Avoid unnecessary For Each when a connector supports a more efficient bulk operation.

---

## 59. Batch Processing

Use Batch where appropriate for large record-oriented workloads.

Evaluate:

- Record size
- Failure handling
- Throughput
- Memory
- Restartability

---

## 60. Parallel For Each

Parallel processing should only be used when concurrency is safe.

Consider:

- Ordering
- Shared state
- Downstream rate limits
- Database capacity
- Thread usage
- Duplicate operations

---

## 61. Scatter-Gather

Scatter-Gather can improve parallel execution but may increase:

- Resource consumption
- Downstream load
- Failure complexity

Use it when parallel calls provide meaningful benefit.

---

## 62. Choice Conditions

Conditions should be:

- Clear
- Deterministic
- Testable

Avoid duplicating complex expressions across multiple branches.

---

## 63. Dynamic Configuration

Dynamic configuration should be used carefully.

Avoid allowing untrusted input to control:

- URLs
- File paths
- SQL
- Expressions
- Connector configuration

---

## 64. Custom Java Code

Custom Java should only be introduced when it provides meaningful value.

Before using custom Java, consider whether MuleSoft or DataWeave already provides the required functionality.

---

## 65. Custom Scripts

Scripts should be reviewed for:

- Security
- Maintainability
- Dependency management
- Error handling
- Input validation

Avoid arbitrary script execution based on user input.

---

## 66. Dependency Management

Dependencies should be:

- Necessary
- Supported
- Versioned
- Maintained

Avoid unused dependencies.

---

## 67. Dependency Versions

Avoid unnecessarily old or unsupported versions when evidence indicates a security or compatibility concern.

Do not recommend upgrades solely because a newer version exists.

---

## 68. Maven Configuration

Review:

- Mule Maven plugin
- Dependencies
- Repositories
- Profiles
- Build configuration

Look for:

- Unnecessary dependencies
- Inconsistent versions
- Hard-coded environment configuration
- Sensitive credentials

---

## 69. Build Reproducibility

Build configuration should support reproducible deployments.

Avoid uncontrolled dependency versions where practical.

---

## 70. Resource Naming

Resources should use consistent naming.

Examples:

- Flow XML files
- DataWeave files
- Properties
- YAML configuration
- RAML/OAS files
- MUnit suites

---

## 71. File Organization

Project files should be organized logically.

Typical areas include:

    src/main/mule
    src/main/resources
    src/test/munit

Do not require an exact directory structure when the Maven/Mule project is otherwise valid.

---

## 72. DataWeave Externalization

Large or reusable DataWeave scripts may be externalized into .dwl files when this improves readability and testability.

Do not externalize trivial transformations unnecessarily.

---

## 73. API Specification Organization

API specifications should be separated from implementation where appropriate.

Avoid embedding large API contracts unnecessarily inside implementation files.

---

## 74. Reusable Configuration

Use shared configuration for common settings where appropriate.

Avoid duplicating:

- TLS configuration
- HTTP request configuration
- Database configuration
- Common connection properties

---

## 75. Code Duplication

Code duplication should be evaluated based on:

- Number of occurrences
- Complexity
- Maintenance cost
- Likelihood of future change

Two small similar expressions do not automatically justify abstraction.

---

## 76. Copy-Paste Integration Logic

Repeated integration logic should be reviewed carefully.

Examples:

- Same authentication sequence
- Same error mapping
- Same transformation
- Same validation
- Same logging sequence

Consider reusable subflows or modules when appropriate.

---

## 77. Maintainability

Code should be maintainable by developers who did not originally create it.

Consider:

- Complexity
- Naming
- Documentation
- Duplication
- Structure
- Error handling
- Configuration

---

## 78. Complexity

Potential complexity indicators include:

- Very large flows
- Deep nesting
- Many Choice branches
- Large DataWeave scripts
- Many variables
- Multiple transformations
- Multiple external calls
- Complex error handling

Complexity alone is not a defect.

Report complexity when it creates a measurable maintainability risk.

---

## 79. Single Responsibility

A flow, subflow, transformation, or module should have a coherent responsibility.

Avoid combining unrelated responsibilities.

---

## 80. Separation of Concerns

Separate where appropriate:

- Transport
- Validation
- Business logic
- Transformation
- External connectivity
- Error handling
- Logging

Do not over-engineer simple integrations.

---

## 81. Reuse vs Abstraction

Reuse is beneficial when it reduces maintenance.

Over-abstraction can create:

- Difficult debugging
- Deep call chains
- Hidden behavior
- Reduced readability

Prefer the simplest abstraction that provides meaningful value.

---

## 82. Security-Critical Code

Security-sensitive logic should be especially clear.

Examples:

- Authentication
- Authorization
- Token validation
- Encryption
- Secret handling
- Input validation

Avoid complex hidden behavior in security-critical code.

---

## 83. Concurrency Safety

Where flows can execute concurrently, review:

- Shared state
- Variables
- Object Store
- Files
- Database operations
- External resources

Avoid assumptions that only one request will execute at a time unless explicitly guaranteed.

---

## 84. File Operations

File operations should consider:

- Path validation
- File locking
- Duplicate processing
- Cleanup
- Permissions
- Large files
- Concurrent access

---

## 85. Temporary Files

Temporary files should be:

- Securely created
- Properly cleaned up
- Protected from unauthorized access

Avoid storing sensitive data unnecessarily in temporary files.

---

## 86. Resource Cleanup

Ensure resources are properly managed where applicable.

Examples:

- Files
- Connections
- Streams
- Temporary data

---

## 87. Timeouts

External operations should have appropriate timeout behavior.

Review:

- HTTP requests
- Database calls
- Messaging
- File operations
- External connectors

Do not use extremely large timeout values merely to avoid failures.

---

## 88. Configuration Consistency

Similar configurations should follow consistent patterns unless there is an intentional difference.

---

## 89. Environment Behavior

Code should behave consistently across environments while allowing configuration differences through external configuration.

Avoid environment checks such as:

    if environment == "PROD"

unless genuinely required.

---

## 90. Production Debugging

Do not leave development-only behavior enabled in production.

Examples:

- Debug endpoints
- Verbose payload logging
- Test credentials
- Mock responses
- Hard-coded test data

---

## 91. Test Code Separation

Test-only code should remain separated from production implementation.

Review:

- MUnit tests
- Mock data
- Test configurations
- Test listeners

---

## 92. Testability

Code should allow important logic to be tested independently.

Avoid unnecessary coupling to external systems.

---

## 93. MUnit Compatibility

Flows should be structured so that external dependencies can reasonably be mocked or verified.

---

## 94. API Contract Compliance

Implementation should follow the declared API contract.

Review:

- Paths
- Methods
- Parameters
- Request schemas
- Response schemas
- Status codes
- Security requirements

---

## 95. HTTP Response Construction

Responses should be built consistently.

Avoid manually duplicating response construction across many flows when a reusable pattern is appropriate.

---

## 96. Error Response Construction

Error responses should be:

- Consistent
- Sanitized
- Consumer-friendly
- Correlatable

---

## 97. HTTP Headers

Only expose headers that are required.

Avoid leaking internal implementation information through response headers.

---

## 98. Secure Coding Quality Gate

Before completing the coding review, confirm:

- No hard-coded credentials were missed.
- No sensitive values are logged.
- Input is appropriately validated.
- SQL is parameterized where required.
- Dynamic URLs are controlled.
- File paths are validated.
- Error handling is intentional.
- Retry behavior is appropriate.
- Large payload handling is considered.
- Streaming is used where appropriate.
- Concurrency risks were considered.
- Configuration is externalized.
- `.properties`, `.yaml`, and `.yml` configuration files were reviewed.
- Duplicate logic was considered.
- Dead code was considered.
- Naming is understandable.
- Complex flows were assessed.
- Custom code has a clear justification.
- Findings are evidence-based.

The final question is:

> Can another experienced MuleSoft developer understand, maintain, test, troubleshoot, and safely modify this code without needing undocumented knowledge from the original developer?