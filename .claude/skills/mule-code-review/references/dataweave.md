# DataWeave Review Rules

## Purpose

These rules define how DataWeave transformations must be reviewed.

Review DataWeave in the context of:

- input payload
- output payload
- schemas
- API contracts
- connector expectations
- downstream consumers
- variables
- attributes
- MIME types
- streaming behavior
- payload size
- runtime version

Do not review DataWeave based only on syntax or style.

A finding must identify a realistic functional, reliability, performance,
security, or maintainability impact.

---

# DataWeave Review Principles

Before reporting a DataWeave issue:

1. Inspect the input structure.
2. Inspect the expected output structure.
3. Inspect related schemas or API specifications.
4. Inspect how the transformation output is consumed.
5. Consider null, missing, empty, and invalid values.
6. Consider realistic payload sizes.
7. Consider Mule runtime/DataWeave compatibility.
8. Determine whether the behavior is actually incorrect.
9. Check whether another component already handles the condition.
10. Avoid reporting stylistic preferences as defects.

Do not assume that a transformation is incorrect simply because another
DataWeave implementation may be shorter or more elegant.

---

# DW-001 — Incorrect Transformation

## Rule

Flag output that does not match the required:

- API contract
- schema
- downstream contract
- business requirement
- connector expectation

## Severity

HIGH

Escalate to CRITICAL when the transformation can cause widespread data
corruption or severe business impact.

## Evidence Required

Identify:

- input
- transformation
- expected output
- actual behavior
- affected consumer

---

# DW-002 — Missing Null Handling

## Rule

Flag realistic null or missing-field scenarios that can cause:

- runtime errors
- incorrect output
- unexpected default behavior
- downstream failures

## Severity

MEDIUM

Escalate when the condition can cause significant production failures.

## Important

Do not require null handling for fields that are demonstrably mandatory
and validated before the transformation.

---

# DW-003 — Incorrect Type Conversion

## Rule

Flag unsafe or incorrect type coercion involving:

- String
- Number
- Boolean
- Date
- DateTime
- LocalDateTime
- Time
- Binary
- Object
- Array

## Examples

Consider:

- invalid numeric conversion
- implicit coercion with unexpected results
- incorrect Boolean interpretation
- incompatible date conversion
- loss of type information

## Severity

MEDIUM

---

# DW-004 — Incorrect Date/Time Handling

## Rule

Flag incorrect handling of:

- timezone
- UTC
- offsets
- daylight-saving transitions
- date formats
- Date vs DateTime
- LocalDateTime
- string-to-date conversion
- date arithmetic

## Severity

MEDIUM

Escalate when incorrect timestamps can affect:

- financial processing
- scheduling
- ordering
- reporting
- reconciliation
- auditability

---

# DW-005 — Incorrect Numeric Handling

## Rule

Flag transformations that can lose meaningful numeric precision or
produce incorrect numeric results.

Consider:

- decimal values
- currency
- large integers
- rounding
- division
- numeric coercion
- floating-point behavior

## Severity

MEDIUM

Escalate when financial or business-critical calculations are affected.

---

# DW-006 — Repeated Expensive Traversal

## Rule

Flag repeated traversal of large arrays or objects when the same data is
scanned multiple times unnecessarily.

Examples:

- repeated `filter`
- repeated `map`
- repeated `filter` followed by repeated `filter`
- repeated lookup operations
- repeated object traversal

## Severity

MEDIUM

Do not flag small collections without a reasonable performance mechanism.

---

# DW-007 — Unnecessary Transformation

## Rule

Flag transformations that provide no meaningful value and introduce
unnecessary:

- processing
- memory usage
- complexity
- conversion risk

## Severity

LOW

Do not flag a transformation merely because it could theoretically be
removed. Confirm that it provides no required contract, type, metadata,
or compatibility behavior.

---

# DW-008 — Excessive Memory Use

## Rule

Flag transformations that unnecessarily materialize very large payloads
or collections in memory.

Consider:

- large JSON/XML payloads
- large CSV files
- large arrays
- repeated object creation
- large intermediate variables
- aggregation operations
- `groupBy`
- `orderBy`
- collection materialization

## Severity

HIGH

Escalate when the application can realistically encounter payload sizes
that can cause:

- OutOfMemoryError
- worker instability
- severe GC pressure
- application restart

---

# DW-009 — Streaming Regression

## Rule

Flag transformations that unnecessarily destroy or prevent streaming
behavior for large-payload processing.

Consider:

- full materialization of streams
- transformations requiring complete collection loading
- operations that force unnecessary buffering
- converting large streaming data into large in-memory structures

## Severity

HIGH

## Evidence Required

Establish that:

1. the input is or can be streamed,
2. the application handles sufficiently large data,
3. the transformation unnecessarily materializes the data,
4. the materialization creates realistic production risk.

---

# DW-010 — Incorrect Stream Reuse

## Rule

Flag reuse of a non-repeatable stream when the same stream is consumed
multiple times and the runtime/application behavior can cause:

- empty payloads
- runtime failures
- incomplete processing

## Severity

HIGH

## Important

Verify whether the stream is actually repeatable before reporting.

Do not assume every Mule payload is non-repeatable.

---

# DW-011 — Inefficient Nested Iteration

## Rule

Flag nested iteration over potentially large collections when the
algorithm can create significant computational complexity.

Consider:

- nested `map`
- nested `filter`
- `some`
- `every`
- `contains`
- repeated lookups
- cross-collection matching

## Severity

MEDIUM

Escalate when realistic data volumes can cause severe latency or resource
consumption.

---

# DW-012 — Incorrect Defaulting

## Rule

Flag `default`, conditional expressions, or fallback logic that
incorrectly changes valid values.

Pay particular attention to:

- `null`
- empty string
- `false`
- `0`
- empty arrays
- empty objects

## Severity

MEDIUM

## Example Risk

A defaulting expression may unintentionally replace a valid `false` or
`0` value with a fallback.

---

# DW-013 — Missing Empty Collection Handling

## Rule

Flag realistic empty-array or empty-object scenarios that produce:

- incorrect output
- runtime errors
- unexpected business behavior

## Severity

LOW

Escalate when empty collections are a normal production scenario and can
cause significant processing failures.

---

# DW-014 — Unnecessary Payload Copies

## Rule

Flag repeated assignment or copying of large payloads or collections
when the copies provide no meaningful functional value.

Consider:

- large variables
- intermediate objects
- repeated transformations
- unnecessary serialization/deserialization

## Severity

MEDIUM

---

# DW-015 — Unmaintainable DataWeave

## Rule

Flag excessively complex DataWeave scripts where decomposition would
materially improve:

- correctness
- testability
- readability
- change safety

## Severity

LOW

Escalate when complexity creates a credible functional or production risk.

Do not report complexity merely because the script is long.

---

# DW-016 — Incorrect Array/Object Semantics

## Rule

Flag transformations that incorrectly treat:

- Array as Object
- Object as Array
- single value as collection
- collection as scalar

when this produces incorrect runtime or business behavior.

## Severity

MEDIUM

---

# DW-017 — Incorrect Key/Field Access

## Rule

Flag incorrect or unsafe access to fields when:

- field names are dynamic
- fields may not exist
- nested objects may be null
- schema differs from assumptions

## Severity

MEDIUM

---

# DW-018 — Incorrect Array Index Assumption

## Rule

Flag transformations that assume an array contains a particular index
without validating the collection size when an empty or shorter array is
a realistic scenario.

## Severity

MEDIUM

---

# DW-019 — Incorrect Filtering Logic

## Rule

Flag filters that unintentionally:

- remove valid records
- retain invalid records
- mishandle nulls
- use incorrect comparison logic
- apply incorrect business conditions

## Severity

HIGH

Escalate when records can be silently lost or incorrectly processed.

---

# DW-020 — Incorrect Grouping or Aggregation

## Rule

Flag incorrect use of:

- `groupBy`
- `reduce`
- aggregation
- distinct operations
- sorting
- deduplication

when the resulting data differs from the required business behavior.

## Severity

HIGH

---

# DW-021 — Incorrect Deduplication

## Rule

Flag transformations that incorrectly identify duplicate records or
fail to remove duplicates when deduplication is required.

Consider:

- identifier selection
- case sensitivity
- null identifiers
- composite keys
- ordering

## Severity

HIGH

---

# DW-022 — Silent Data Loss

## Rule

Flag DataWeave logic that can silently discard:

- records
- fields
- array elements
- invalid records
- null values

when the discarded data is required by the downstream contract or
business process.

## Severity

HIGH

Escalate to CRITICAL when widespread or irreversible data loss is
credible.

---

# DW-023 — Incorrect Conditional Logic

## Rule

Flag `if/else`, `match`, `when`, `otherwise`, or conditional expressions
that can select the wrong processing path.

Consider:

- condition ordering
- overlapping conditions
- missing conditions
- unreachable conditions
- null behavior
- boundary values

## Severity

HIGH

---

# DW-024 — Incorrect String Handling

## Rule

Flag incorrect handling of strings involving:

- trimming
- case sensitivity
- substring operations
- concatenation
- escaping
- encoding
- whitespace
- empty strings

when the behavior affects business or integration correctness.

## Severity

MEDIUM

---

# DW-025 — Incorrect Encoding or Binary Handling

## Rule

Flag incorrect handling of:

- Binary
- Base64
- character encoding
- MIME type
- file content
- multipart content

when it can corrupt data or cause downstream failures.

## Severity

HIGH

---

# DW-026 — Unsafe Dynamic Expression

## Rule

Flag dynamic DataWeave expressions that can produce unexpected behavior
or create security risk through untrusted input.

Consider:

- dynamic field access
- dynamic expressions
- dynamic selectors
- dynamically constructed content
- user-controlled values

## Severity

HIGH

---

# DW-027 — Sensitive Data Exposure

## Rule

Flag DataWeave transformations that unnecessarily expose or propagate:

- passwords
- tokens
- credentials
- authorization information
- private keys
- sensitive personal information

## Severity

HIGH

Escalate to CRITICAL when sensitive credentials or secrets are exposed
to external systems or logs.

---

# DW-028 — Incorrect Schema Handling

## Rule

Flag transformations that do not correctly handle the schema expected
by the application.

Consider:

- missing fields
- additional fields
- required fields
- field types
- nested structures
- arrays
- XML namespaces
- schema evolution

## Severity

HIGH

---

# DW-029 — XML Namespace Handling Error

## Rule

Flag incorrect handling of XML namespaces that can cause:

- missing elements
- incorrect selectors
- invalid output
- downstream integration failures

## Severity

HIGH

---

# DW-030 — CSV Parsing or Generation Error

## Rule

When CSV is used, review:

- headers
- delimiters
- quoting
- escaping
- line endings
- null/empty values
- data types
- embedded delimiters
- embedded quotes
- large-file behavior

Flag behavior that can corrupt records or produce incorrect output.

## Severity

HIGH

---

# DW-031 — Incorrect MIME Type or Output Directive

## Rule

Flag incorrect DataWeave output directives or MIME types when they can
cause downstream processors or external systems to interpret the payload
incorrectly.

Consider:

- JSON
- XML
- CSV
- Java
- Binary
- multipart content

## Severity

MEDIUM

---

# DW-032 — Unnecessary Serialization/Deserialization

## Rule

Flag unnecessary conversion between representations when it adds
meaningful:

- CPU cost
- memory usage
- latency
- data conversion risk

Examples:

- Object → JSON → Object
- String → JSON → String
- Binary → String → Binary

## Severity

MEDIUM

---

# DW-033 — Repeated External-Lookup Pattern

## Rule

Flag DataWeave-driven processing that causes repeated external lookups
or repeated downstream calls when the same information could reasonably
be resolved once.

Consider whether the DataWeave is driving:

- repeated database queries
- repeated HTTP calls
- repeated Salesforce calls
- repeated Object Store operations

## Severity

MEDIUM

## Important

Only report this when the DataWeave/execution relationship is clear from
the repository.

---

# DW-034 — Incorrect Sorting or Ordering

## Rule

Flag transformations where sorting or ordering behavior does not match
the required business or integration contract.

Consider:

- ascending/descending behavior
- null values
- date ordering
- numeric vs string ordering
- stable ordering requirements

## Severity

MEDIUM

---

# DW-035 — Incorrect Case Sensitivity

## Rule

Flag comparisons, lookups, or mappings that incorrectly assume case
sensitivity or case insensitivity.

Examples:

- identifiers
- email addresses
- codes
- status values
- headers
- XML values

## Severity

MEDIUM

---

# DW-036 — Incorrect Boolean Semantics

## Rule

Flag transformations that incorrectly interpret values such as:

- `true`
- `false`
- `"true"`
- `"false"`
- `1`
- `0`
- null
- empty string

when this can change business behavior.

## Severity

MEDIUM

---

# DW-037 — Unnecessary Repeated Conversion

## Rule

Flag repeated conversion of the same value between types when the
conversion creates meaningful:

- CPU overhead
- complexity
- precision risk
- correctness risk

## Severity

LOW

Escalate when performed at high volume.

---

# DW-038 — Large Collection Aggregation Risk

## Rule

Flag use of operations that require complete collection materialization
when collections can realistically become very large.

Consider:

- `groupBy`
- `orderBy`
- `distinctBy`
- `reduce`
- aggregation
- full joins
- large intermediate objects

## Severity

HIGH

---

# DW-039 — Incorrect Error or Fallback Data

## Rule

Flag DataWeave used to construct error responses or fallback payloads
when the resulting structure:

- violates the API contract
- exposes internal information
- loses correlation information
- hides the root cause
- produces misleading client information

## Severity

MEDIUM

Escalate when security or API compatibility is affected.

---

# DW-040 — DataWeave Version Compatibility

## Rule

Flag use of DataWeave features, syntax, modules, or behavior that are
not compatible with the Mule runtime/DataWeave version actually used by
the repository.

## Severity

HIGH

## Evidence Required

Verify compatibility against:

- `pom.xml`
- `mule-artifact.json`
- runtime configuration
- project dependencies

Do not assume the latest DataWeave capabilities are available.

---

# DataWeave Performance Rules

Performance findings must consider:

- realistic payload size
- collection cardinality
- execution frequency
- worker resources
- downstream latency
- memory behavior
- streaming
- algorithmic complexity

Do not report a performance issue solely because a more optimized
implementation exists.

---

# DataWeave Correctness Rules

Correctness findings should be prioritized over stylistic improvements.

A transformation should be considered problematic when it can cause:

- incorrect records
- missing records
- incorrect fields
- incorrect types
- incorrect dates
- incorrect numeric values
- contract violations
- silent data loss
- duplicate data
- incorrect business decisions

---

# DataWeave Security Rules

Review DataWeave for:

- secret propagation
- sensitive data exposure
- unsafe dynamic expressions
- sensitive logging
- insecure transformation of credentials
- unnecessary copying of sensitive payloads

Do not report ordinary business data as sensitive without evidence.

---

# DataWeave Finding Validation

Before reporting a DataWeave finding:

1. Identify the input.
2. Identify the transformation.
3. Identify the expected behavior.
4. Trace the output consumer.
5. Test mentally against null and empty values.
6. Consider realistic payload sizes.
7. Check runtime/DataWeave compatibility.
8. Verify that another component does not already handle the condition.
9. Determine the actual impact.
10. Assign the appropriate severity.

---

# DataWeave Finding Format

Use:

**Finding ID:** DW-001

**Severity:** HIGH

**Category:** DATAWEAVE

**File:** `src/main/resources/dw/order.dwl:15`

**Location:** Transformation producing `order.items`

**Problem:**

Describe the problem.

**Evidence:**

Identify the relevant DataWeave logic and repository evidence.

**Technical Mechanism:**

Explain how the transformation produces the incorrect behavior.

**Impact:**

Explain realistic business or production impact.

**Recommendation:**

Provide an actionable remediation.

**Confidence:** HIGH / MEDIUM / LOW