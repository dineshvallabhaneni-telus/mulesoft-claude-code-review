# File: standards/dataweave/dataweave-standards.md

# MuleSoft DataWeave Standards

## 1. Purpose

This document defines standards for reviewing DataWeave code in MuleSoft applications.

The review must determine whether DataWeave is:

- Correct
- Readable
- Maintainable
- Efficient
- Testable
- Secure
- Consistent
- Appropriate for the transformation requirement

The review must focus on meaningful issues.

Do not report a DataWeave expression merely because another implementation style is possible.

---

## 2. General Principles

DataWeave should be:

- Clear
- Predictable
- Explicit where necessary
- Reusable where appropriate
- Efficient for expected payload sizes
- Easy to test
- Easy to troubleshoot

Prefer the simplest implementation that correctly satisfies the requirement.

---

## 3. Appropriate Use of DataWeave

Use DataWeave for:

- Data transformation
- Filtering
- Mapping
- Aggregation
- Data normalization
- Formatting
- Data extraction
- Data validation where appropriate

Avoid using DataWeave for responsibilities better handled by:

- Connectors
- Configuration
- Error handling
- Authentication
- External systems
- Dedicated application components

---

## 4. Readability

DataWeave scripts should be understandable to another MuleSoft developer.

Review:

- Variable names
- Function names
- Mapping structure
- Conditional logic
- Selectors
- Filters
- Complex expressions

Avoid unnecessarily compressed or cryptic expressions.

---

## 5. Naming

Use descriptive names for:

- Variables
- Functions
- Parameters
- Local values
- Output fields

Prefer:

    customerId

over:

    id1

Prefer:

    activeCustomers

over:

    data2

---

## 6. Variable Naming

Variables should communicate what they contain.

Examples:

    customerResponse
    orderItems
    filteredCustomers
    totalAmount

Avoid generic names such as:

    data
    result
    temp
    obj
    x

unless the scope is trivial and the meaning is obvious.

---

## 7. Function Naming

Functions should describe their behavior.

Prefer:

    calculateTotal

    normalizeCustomer

    buildAddress

over:

    process

    handle

    doSomething

---

## 8. Function Responsibility

Functions should have a focused responsibility.

Avoid functions that simultaneously:

- Validate
- Transform
- Filter
- Aggregate
- Format
- Apply unrelated business rules

when separating those responsibilities would improve maintainability.

---

## 9. Reusable Functions

Create reusable functions when the same transformation logic is used multiple times.

Do not create abstractions solely to reduce a few lines of code.

Evaluate:

- Reuse
- Complexity
- Readability
- Maintenance cost
- Testability

---

## 10. External DataWeave Files

Large or reusable transformations may be moved into `.dwl` files.

This is particularly useful when:

- A transformation is large.
- A transformation is reused.
- Unit testing is beneficial.
- Inline XML becomes difficult to read.

Do not externalize trivial expressions unnecessarily.

---

## 11. DataWeave Modules

Reusable DataWeave modules may be used for common functions.

Examples:

- Date utilities
- String utilities
- Validation helpers
- Common mapping functions

Modules should contain logically related functionality.

Avoid creating generic utility modules containing unrelated functions.

---

## 12. Input Validation

Validate required input before performing transformations that depend on it.

Consider:

- Null payload
- Missing fields
- Incorrect data types
- Invalid values
- Empty collections

---

## 13. Null Handling

DataWeave transformations must intentionally handle possible null values.

Review expressions involving:

- Nested selectors
- Arrays
- Objects
- Optional fields
- External responses

Avoid assumptions that optional fields always exist.

---

## 14. Missing Fields

A missing field and a field containing `null` are not necessarily equivalent.

The implementation should intentionally handle both cases where business requirements distinguish them.

---

## 15. Empty Collections

Consider how transformations behave when an array is empty.

Examples:

- `map`
- `filter`
- `reduce`
- `groupBy`
- `orderBy`

Ensure the output remains valid for zero-record input.

---

## 16. Empty Strings

Do not automatically treat:

- `null`
- `""`
- `" "`
- missing field

as equivalent.

Apply business rules explicitly.

---

## 17. Type Handling

DataWeave expressions should use appropriate types.

Review:

- String
- Number
- Boolean
- Date
- DateTime
- LocalDateTime
- Array
- Object
- Binary

Avoid unnecessary conversions.

---

## 18. Type Coercion

Do not rely on implicit type coercion when it could produce unexpected results.

Explicitly convert values when required for correctness.

---

## 19. String Conversion

Avoid unnecessary conversions such as:

    value as String

followed by converting the value back to another type.

Keep data in its appropriate type for as long as practical.

---

## 20. Numeric Calculations

Numeric calculations should use appropriate numeric types.

Review:

- Decimal precision
- Currency calculations
- Rounding
- Null values
- String-to-number conversions

Do not use string operations for numerical calculations.

---

## 21. Currency

Currency calculations should explicitly address:

- Precision
- Rounding
- Currency code
- Decimal behavior

Do not assume floating-point behavior is appropriate for financial calculations.

---

## 22. Date Handling

Dates should be handled using appropriate DataWeave date/time types.

Avoid manipulating dates through arbitrary string operations when native date functions are available.

---

## 23. Time Zones

DateTime transformations should explicitly consider time zones when business behavior depends on them.

Avoid silently converting timestamps between time zones.

---

## 24. Date Formatting

Use explicit date formats when converting dates to strings.

Avoid relying on ambiguous or environment-dependent formatting.

---

## 25. Input and Output Formats

The transformation should clearly define the expected input and output formats.

Examples:

- JSON
- XML
- CSV
- Java objects
- Binary

Avoid unnecessary format conversions.

---

## 26. JSON Transformations

JSON mappings should:

- Preserve required fields
- Handle optional fields
- Use appropriate data types
- Avoid unnecessary intermediate transformations

---

## 27. XML Transformations

XML transformations should consider:

- Namespaces
- Attributes
- Repeated elements
- Optional nodes
- Empty elements
- Schema expectations

Do not assume XML namespaces can be ignored.

---

## 28. XML Namespaces

Namespaces must be handled explicitly where required.

Avoid selectors that accidentally depend on a namespace structure that may change.

---

## 29. CSV Transformations

CSV processing should consider:

- Headers
- Delimiters
- Quoting
- Encoding
- Missing fields
- Large files

Do not assume all CSV files use the same formatting conventions.

---

## 30. Mapping

Use `map` when transforming each element of a collection.

The transformation should clearly communicate the resulting structure.

---

## 31. Filtering

Use `filter` when selecting records based on conditions.

Conditions should be readable and avoid unnecessary repeated expressions.

---

## 32. Map and Filter Ordering

Consider whether filtering can safely occur before mapping.

For example, when only a subset of records is required, filtering earlier may reduce processing.

Do not reorder operations when doing so changes business behavior.

---

## 33. Reduce

Use `reduce` for meaningful aggregation or accumulation.

Avoid complex `reduce` expressions when simpler operations provide the same behavior.

---

## 34. Grouping

Use `groupBy` when grouping data is required.

Ensure grouping keys:

- Are deterministic
- Handle null values appropriately
- Have the expected type

---

## 35. Distinct Values

Use appropriate DataWeave functions for deduplication.

Do not implement manual duplicate detection when a native operation provides clearer behavior.

---

## 36. Sorting

Sorting should only be performed when required.

Avoid sorting large collections unnecessarily.

---

## 37. Repeated Traversal

Review transformations that repeatedly iterate over the same large collection.

Consider whether the logic can be simplified to reduce unnecessary processing.

Do not optimize prematurely when payloads are small and readability would suffer.

---

## 38. Payload Size

DataWeave transformations should consider payload size.

For large payloads, review:

- Streaming
- Multiple traversals
- Intermediate variables
- Materialization
- Large arrays
- Large string conversions

---

## 39. Streaming

Streaming should be preserved where the processing model supports it and the entire dataset does not need to be materialized.

Avoid operations that unnecessarily force large streams into memory.

---

## 40. Binary Data

Binary data should not be unnecessarily converted to strings.

Review:

- Encoding
- Decoding
- Base64
- File content
- Attachments

Avoid unnecessary binary-to-string-to-binary conversions.

---

## 41. Base64

Base64 encoding should only be used when required by the target protocol or business requirement.

Remember that Base64 is encoding, not encryption.

Do not treat Base64 as a security mechanism.

---

## 42. Sensitive Data

DataWeave transformations handling sensitive information should avoid unnecessary copies or exposure.

Sensitive information may include:

- Passwords
- Tokens
- API keys
- Personal data
- Financial data
- Authentication information

---

## 43. Sensitive Output

Do not accidentally include sensitive input fields in output objects.

Review mappings carefully when transforming objects containing security-sensitive fields.

---

## 44. Data Masking

When sensitive values must appear in logs or diagnostic output, use appropriate masking.

Do not expose complete:

- Passwords
- Tokens
- Authorization headers
- API keys
- Financial identifiers

---

## 45. Dynamic Expressions

Dynamic expressions must be carefully controlled.

Do not allow untrusted input to dynamically determine:

- File paths
- URLs
- Queries
- Expressions
- Class names
- Resource locations

Dynamic behavior may introduce injection or unauthorized-access risks.

---

## 46. SQL Construction

Do not construct SQL queries through unsafe string concatenation.

Prefer parameterized database operations.

DataWeave should not be used to bypass connector security controls.

---

## 47. Expression Injection

Do not evaluate arbitrary expressions generated from user input.

User-controlled data should remain data, not executable expressions.

---

## 48. XML/HTML Construction

When constructing XML or HTML from external input, ensure that values are safely represented in the target format.

Avoid manually constructing markup when native DataWeave structures provide safer and clearer behavior.

---

## 49. Regular Expressions

Regular expressions should be used carefully.

Review:

- Complexity
- Readability
- Input size
- Backtracking behavior
- Validation correctness

Avoid unnecessarily complex regular expressions.

---

## 50. Regular Expression Security

Be cautious of expressions that can cause excessive processing for malicious or unexpectedly large input.

Review complex patterns for potential denial-of-service behavior.

---

## 51. Default Values

Use default values when they represent a legitimate business or technical default.

Do not silently replace invalid or missing data with values that could produce incorrect business behavior.

---

## 52. Conditional Expressions

Conditional logic should be simple and readable.

Avoid deeply nested expressions.

Prefer clear intermediate values or functions when complexity becomes significant.

---

## 53. Pattern Matching

Use pattern matching where it improves clarity.

Do not use advanced syntax merely to make code shorter.

Readability is more important than minimizing line count.

---

## 54. Selectors

Selectors should be clear and safe.

Review:

- Nested selectors
- Dynamic selectors
- Array indexing
- Optional fields
- Null behavior

---

## 55. Array Indexing

Avoid assuming an array always contains an element at a specific index.

For example, accessing the first element should consider the possibility of an empty array.

---

## 56. Object Selectors

Object selectors should handle missing properties where appropriate.

Do not assume every external response contains every field.

---

## 57. Conditional Field Creation

Only create fields conditionally when the target contract allows optional fields.

Do not accidentally produce structurally invalid payloads.

---

## 58. Output Schema

The resulting DataWeave output should conform to the expected schema.

Review:

- Field names
- Field types
- Required fields
- Optional fields
- Nested structure
- Arrays
- Namespaces
- Formatting

---

## 59. Contract Compatibility

If DataWeave produces an API or integration response, verify compatibility with the declared contract.

The transformation should not silently:

- Rename fields
- Remove required fields
- Change types
- Change status-related content

---

## 60. Repeated Expressions

Avoid repeating complex expressions.

For example, if the same expensive or complicated calculation is used multiple times, consider assigning it to a meaningful variable.

---

## 61. Intermediate Variables

Intermediate variables are encouraged when they improve:

- Readability
- Reuse
- Debugging
- Testability

Do not create variables for trivial expressions that reduce clarity.

---

## 62. Large Inline Transformations

Very large inline DataWeave blocks should be reviewed.

Consider externalizing them when:

- They are difficult to understand.
- They contain multiple logical responsibilities.
- They are reused.
- They require independent testing.

---

## 63. Comments

Comments should explain non-obvious behavior.

Good comments explain:

- Why a transformation is necessary
- External system limitations
- Business-specific mapping decisions
- Workarounds

Avoid comments that simply restate the expression.

---

## 64. Hard-Coded Values

Avoid unexplained hard-coded business values.

Examples:

- Status codes
- Thresholds
- Limits
- Business categories

Externalize values when they are expected to change independently from code.

---

## 65. Business Rules

Important business rules should be identifiable.

Avoid hiding significant business logic inside a complex one-line transformation.

---

## 66. Transformation Duplication

Identify repeated transformation logic across:

- Flows
- Subflows
- `.dwl` files
- Modules

Consider reuse when duplication creates maintenance risk.

---

## 67. Copy-Paste Mapping

Large copy-pasted mappings should be reviewed.

However, do not abstract mappings simply because fields look similar.

Consider whether the mapping rules are expected to evolve independently.

---

## 68. DataWeave Imports

Imports should be:

- Necessary
- Clear
- Consistent

Remove unused imports where they create maintenance noise.

---

## 69. Namespace Imports

XML namespace declarations should be appropriate to the transformation.

Avoid unnecessary namespace declarations.

---

## 70. Module Dependencies

DataWeave modules should only depend on required modules.

Avoid unnecessary dependencies that make transformations harder to understand or deploy.

---

## 71. Compatibility

DataWeave syntax and modules should be compatible with the Mule runtime version used by the application.

Do not recommend syntax changes without considering runtime compatibility.

---

## 72. Runtime Compatibility

Review transformations for:

- Runtime-specific behavior
- Deprecated functions
- Unsupported syntax
- Module compatibility

A valid DataWeave expression must also be valid for the application's target runtime.

---

## 73. Error Handling

DataWeave should not silently hide transformation failures.

Review use of:

- `try`
- `default`
- Conditional fallback
- Error handling functions

A fallback should not convert invalid data into a successful result unless that behavior is intentional.

---

## 74. Default vs Error

Do not use `default` simply to suppress errors.

For example, replacing invalid required data with an arbitrary default may hide a data-quality problem.

---

## 75. Error Messages

Where DataWeave-generated validation or error information is exposed, messages should be:

- Clear
- Safe
- Useful
- Free of sensitive internal information

---

## 76. Performance Considerations

Potential performance concerns include:

- Repeated full collection traversal
- Repeated expensive functions
- Large intermediate structures
- Unnecessary sorting
- Unnecessary conversions
- Excessive string manipulation
- Unnecessary serialization

Only report performance issues when they are credible for the expected workload.

---

## 77. Premature Optimization

Do not optimize DataWeave at the expense of readability without evidence.

A simple transformation is often preferable to a highly optimized but difficult-to-maintain implementation.

---

## 78. Testability

Important DataWeave transformations should be independently testable.

Consider tests for:

- Normal input
- Empty input
- Null input
- Missing fields
- Invalid values
- Boundary values
- Large collections
- Unexpected external responses

---

## 79. Edge Cases

Review transformations for:

- Empty arrays
- Null values
- Missing fields
- Duplicate records
- Negative numbers
- Zero values
- Large numbers
- Invalid dates
- Invalid formats
- Unexpected types

---

## 80. Boundary Conditions

Pay particular attention to:

- Maximum values
- Minimum values
- Empty collections
- Single-element collections
- Large collections
- Date boundaries
- Time-zone boundaries

---

## 81. Data Quality

DataWeave should not silently corrupt or discard data.

Review operations such as:

- Filtering
- Grouping
- Deduplication
- Type conversion
- Truncation
- Defaulting

Ensure data loss is intentional.

---

## 82. Field Renaming

Field renaming should be explicit and consistent.

Avoid accidental renaming caused by ambiguous selectors or dynamic mapping.

---

## 83. Field Removal

Removing fields should be intentional.

This is especially important when transforming:

- API requests
- API responses
- Customer data
- Financial data
- Security-related objects

---

## 84. Additional Fields

Avoid accidentally exposing internal fields in external API responses.

Review mappings from internal objects to public contracts.

---

## 85. Sensitive Field Propagation

When mapping objects, ensure sensitive internal fields are not propagated to:

- External APIs
- Logs
- Messages
- Files
- Responses

---

## 86. Input Trust Boundary

Treat incoming data as untrusted until validated.

DataWeave transformations should not assume:

- Correct type
- Correct format
- Required field presence
- Safe string contents
- Valid identifiers

---

## 87. Output Trust Boundary

External systems may return unexpected or malicious data.

Validate and safely transform external responses before exposing them to other systems.

---

## 88. DataWeave Review Checklist

Before completing the DataWeave review, confirm:

- Transformations are readable.
- Variable names are meaningful.
- Functions have clear responsibilities.
- Null handling is intentional.
- Missing fields are considered.
- Empty collections are handled.
- Types are appropriate.
- Date/time handling is correct.
- Time zones are considered.
- Numeric and currency calculations are safe.
- Unnecessary conversions are avoided.
- Large payload handling is considered.
- Streaming is preserved where appropriate.
- Sensitive fields are not accidentally exposed.
- Dynamic expressions are controlled.
- SQL is not constructed unsafely.
- Regular expressions are reasonable.
- Hard-coded business values are justified.
- Duplicate transformations were considered.
- Large transformations were considered for externalization.
- Output matches the expected contract.
- Runtime compatibility was considered.
- Errors are not silently suppressed.
- Default values do not hide invalid data.
- Performance concerns were considered.
- Testability was considered.
- Edge cases were considered.

---

## 89. DataWeave Quality Gate

The reviewer must be able to answer the following questions:

1. Is the transformation easy to understand?
2. Are input assumptions explicit?
3. Are null and missing values handled correctly?
4. Are output types and structures correct?
5. Are business rules visible and maintainable?
6. Is sensitive data protected?
7. Are dynamic expressions safe?
8. Is the transformation efficient for expected payload sizes?
9. Is unnecessary data conversion avoided?
10. Are large collections handled appropriately?
11. Is the transformation testable?
12. Does the implementation match the API or integration contract?
13. Is the DataWeave syntax compatible with the target Mule runtime?
14. Are duplicate transformations minimized where appropriate?
15. Are errors handled without hiding data-quality problems?

### Final Question

> Does this DataWeave transformation produce the correct output reliably and securely while remaining understandable, testable, and efficient for the expected data volume?