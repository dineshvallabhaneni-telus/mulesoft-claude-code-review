# DataWeave Review Rules

## Purpose

Review DataWeave transformations for:

* transformation correctness
* data integrity
* null and missing-field behavior
* type safety
* date/time correctness
* timezone correctness
* numeric correctness
* collection handling
* memory behavior
* streaming behavior
* transformation efficiency
* unnecessary payload copying
* production reliability

DataWeave findings must be based on actual transformation semantics and
repository evidence.

Do not report a finding merely because an alternative DataWeave
implementation appears cleaner or shorter.

---

# Review Areas

Inspect, where applicable:

* input payload structure
* output payload structure
* field mappings
* conditional expressions
* null handling
* missing fields
* default values
* type coercion
* explicit type conversion
* date/time parsing
* timezone conversion
* numeric calculations
* decimal precision
* collection traversal
* nested iteration
* filtering
* grouping
* joins
* recursive processing
* repeated expressions
* payload copies
* intermediate variables
* streaming
* large payload handling
* DataWeave modules
* imported functions
* externalized DataWeave scripts

Review DataWeave together with the flows that consume its input and
output.

---

# DataWeave Review Principles

Before reporting a finding:

1. Identify the DataWeave script or expression.
2. Determine the actual input structure.
3. Determine the expected output structure where repository evidence
   exists.
4. Inspect upstream transformations.
5. Inspect downstream consumers.
6. Inspect relevant API specifications or schemas.
7. Inspect related variables and attributes.
8. Determine actual DataWeave behavior.
9. Check whether null/default/error handling exists elsewhere.
10. Check whether tests cover the relevant behavior.
11. Determine actual production impact.
12. Assign severity and confidence based on evidence.

Do not infer an expected business transformation when the repository
does not establish it.

---

# DW-001 — Incorrect Transformation Behavior

## Description

A DataWeave transformation produces incorrect, incomplete, or
unexpected output for an input that the application can realistically
receive.

Potential examples include:

* incorrect field mapping
* dropped required fields
* incorrect conditional logic
* incorrect filtering
* incorrect grouping
* incorrect array/object construction
* incorrect use of variables
* incorrect handling of nested structures
* incorrect transformation of values

## Finding Gate

The expected behavior must be established by repository evidence such
as:

* API specifications
* schemas
* downstream contracts
* tests
* adjacent implementation
* configuration
* clearly established application behavior

Do not report a transformation as incorrect solely because another
output shape appears preferable.

## Evidence Requirements

Identify:

* DataWeave file or expression
* relevant input
* transformation logic
* expected behavior
* actual resulting behavior
* supporting contract/test/evidence

## Impact Examples

Potential impacts include:

* incorrect downstream requests
* malformed responses
* data loss
* data corruption
* failed integrations
* incorrect business processing

---

# DW-002 — Unsafe Null or Missing-Field Handling

## Description

DataWeave assumes the presence of a value or field when null or missing
input is realistically possible and the resulting behavior creates a
meaningful risk.

Potential examples include:

* dereferencing a potentially absent field
* iterating over a potentially null collection
* accessing nested fields without appropriate safeguards
* assuming optional API fields are always present
* treating null as an expected object/value without handling it

## Finding Gate

The field must be realistically capable of being:

* absent
* null
* empty
* structurally different

based on repository evidence or an established external contract.

Do not report null-handling concerns for fields demonstrably guaranteed
by the application contract.

## Evidence Requirements

Identify:

* affected expression
* field or collection
* source structure
* null/missing possibility
* resulting DataWeave behavior
* relevant tests or contract evidence

## Impact Examples

Potential impacts include:

* transformation failure
* unexpected error propagation
* dropped records
* failed API requests
* incomplete processing

---

# DW-003 — Incorrect Type Conversion

## Description

A DataWeave expression performs an unsafe, incorrect, lossy, or
contract-incompatible type conversion.

Potential areas include:

* String to Number
* Number to String
* String to Boolean
* date/time conversion
* numeric precision
* locale-sensitive conversion
* implicit coercion
* incompatible type assumptions

## Finding Gate

The conversion must create a realistic behavioral risk.

Do not report explicit type conversion merely because it could be
written differently.

## Evidence Requirements

Identify:

* source type
* target type
* conversion expression
* relevant format/locale where applicable
* downstream expectation
* resulting behavior

## Impact Examples

Potential impacts include:

* rejected requests
* incorrect values
* precision loss
* failed comparisons
* malformed data
* downstream contract violations

---

# DW-004 — Potential Memory Problem

## Description

DataWeave processing creates a credible risk of excessive memory usage,
resource exhaustion, or unsafe processing of large payloads.

Potential mechanisms include:

* materializing very large collections
* unnecessary full-payload copies
* repeated transformations of large datasets
* nested operations that significantly increase intermediate data
* collecting streaming data into memory without justification
* constructing disproportionately large intermediate structures

## Finding Gate

Do not report this finding solely because:

* a payload is large
* an array is used
* a transformation contains loops
* a script contains multiple variables
* the code looks complex

There must be a credible mechanism connecting the implementation to
potential memory pressure.

Where possible, establish:

* payload scale
* collection size
* intermediate object growth
* streaming behavior
* downstream consumption
* deployment/resource constraints

## Evidence Requirements

Identify:

* affected DataWeave
* relevant operation
* data structure
* memory-growth mechanism
* streaming/materialization behavior
* realistic production scenario

## Impact Examples

Potential impacts include:

* excessive heap usage
* garbage-collection pressure
* application slowdown
* out-of-memory failures
* worker instability

---

# DW-005 — Inefficient Transformation With Production Impact

## Description

A DataWeave transformation performs unnecessary or disproportionately
expensive work that creates a meaningful production performance impact.

Potential mechanisms include:

* repeated traversal of large collections
* avoidable nested iteration
* repeated computation
* unnecessary serialization/deserialization
* redundant transformations
* unnecessary payload reconstruction
* inefficient filtering or joining
* repeated evaluation of expensive expressions

## Finding Gate

An inefficient implementation is not automatically a finding.

The issue must have a credible mechanism and meaningful production
impact.

Consider:

* input size
* execution frequency
* algorithmic behavior
* number of traversals
* nested iteration
* concurrency
* latency requirements
* resource consumption

Do not report a performance issue merely because the implementation
could be optimized.

## Evidence Requirements

Identify:

* affected DataWeave
* expensive operation
* relevant collection/payload
* execution frequency where available
* performance mechanism
* expected production consequence

## Impact Examples

Potential impacts include:

* increased latency
* reduced throughput
* increased CPU consumption
* increased memory consumption
* worker saturation
* timeout risk

---

# DW-006 — Date/Time or Timezone Defect

## Description

DataWeave date, time, datetime, timezone, or formatting logic produces
incorrect temporal behavior.

Potential examples include:

* incorrect timezone assumptions
* unintended UTC/local-time conversion
* loss of timezone information
* incorrect parsing format
* incorrect date arithmetic
* daylight-saving-related behavior
* comparison of incompatible temporal types
* formatting that changes semantic meaning

## Finding Gate

A finding requires evidence of an actual or realistic temporal
behavior problem.

Do not report timezone concerns merely because UTC is not explicitly
used.

The application's contract, deployment model, connector behavior, or
business requirement must establish why the timezone matters.

## Evidence Requirements

Identify:

* affected DataWeave expression
* source temporal value
* target temporal value
* timezone/format behavior
* relevant API or integration contract
* actual or expected discrepancy

## Impact Examples

Potential impacts include:

* incorrect timestamps
* incorrect scheduling
* rejected downstream values
* incorrect date filtering
* data inconsistency
* reporting discrepancies

---

# Collection and Nested Traversal Analysis

When reviewing collection operations, consider:

* collection size
* number of traversals
* nested iteration
* filtering before expansion
* grouping behavior
* intermediate collections
* duplicate processing
* streaming compatibility

Nested iteration is not inherently defective.

Report it only when repository evidence supports a credible correctness,
memory, or performance consequence.

---

# Streaming and Large Payloads

Consider whether the application:

* receives large payloads
* processes large files
* handles streaming input
* preserves streaming where appropriate
* materializes data unnecessarily
* sends large transformed payloads downstream

Do not assume streaming is required for every transformation.

The finding must be tied to actual payload characteristics and
application behavior.

---

# DataWeave and Contract Alignment

Where available, compare DataWeave behavior against:

* RAML
* OAS
* JSON/XML schemas
* connector expectations
* database schemas
* messaging contracts
* MUnit assertions
* downstream integration requirements

Contract evidence takes precedence over assumptions about intended
output.

---

# Severity Guidance

Rate DataWeave findings according to demonstrated production impact.

### CRITICAL

Use only for catastrophic transformation consequences such as:

* widespread data corruption
* severe data loss
* critical processing failure

### HIGH

Use for substantial issues such as:

* major data corruption
* widespread transformation failure
* severe memory exhaustion
* critical integration failure

### MEDIUM

Use for meaningful:

* functional defects
* realistic edge-case failures
* material performance issues
* important data-handling problems

### LOW

Use for limited production impact.

### NIT

Use only for optional optimization or readability improvements that do
not represent material production risk.

---

# False-Positive Controls

Do not create a DataWeave finding when:

* the expected behavior is not established
* null is demonstrably impossible
* a conversion is valid for the actual input contract
* a transformation is inefficient only in theory
* collection size is small or bounded by evidence
* streaming is not required by the actual workload
* timezone behavior is valid for the application's contract
* another component already handles the relevant condition
* tests or contracts demonstrate the implementation is correct
* evidence is insufficient

When evidence is insufficient:

**Do not report the finding.**

---

# Positive DataWeave Indicators

Where supported by evidence, recognize strengths such as:

* explicit and correct type conversion
* defensive null handling
* contract-aligned transformations
* appropriate date/time handling
* efficient collection processing
* appropriate streaming
* limited intermediate materialization
* reusable DataWeave modules
* clear transformation structure
* strong MUnit coverage of transformation edge cases

Positive observations must be evidence-backed.

---

# Required Finding Fields

Any DataWeave finding must include:

* Finding ID
* Severity
* Category
* Title
* File
* Location
* Confidence
* Problem
* Evidence
* Evidence Excerpt
* Impact
* Recommendation

Evidence excerpts must remain faithful to repository content.

Sanitize:

* passwords
* tokens
* API keys
* private keys
* secure property values
* authorization headers
* other secrets

Never include secret values in the report.