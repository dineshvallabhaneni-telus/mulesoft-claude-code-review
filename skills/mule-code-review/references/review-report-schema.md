# CODE REVIEW DOCUMENT SCHEMA

## Document Type

Professional Software / API / Integration Code Review Report

## Purpose

Define the complete structure, content, visual style, tables, severity indicators, assessment rules, structured review contract, and validation requirements for the generated Microsoft Word document.

This document is the authoritative report contract for:

* `scripts/validate_review.py`
* `scripts/generate_report.py`

Claude must produce structured review data that conforms to this contract.

The Word document generator must render the validated structured review according to this contract.

---

# DOCUMENT DESIGN

The report must be:

* professional
* executive-friendly
* technically detailed
* evidence-based
* visually structured
* easy to scan
* consistent
* suitable for production review and management decision-making

Use:

* color-coded severity indicators
* textual status badges
* structured tables
* finding cards
* evidence/code blocks
* risk summaries
* readiness matrices
* remediation priority tables
* architecture diagrams where useful
* consistent section numbering
* clear page hierarchy
* readable headers and footers

Never guess unavailable information.

Use exactly:

`Not Identified`

when information is unavailable.

Use exactly:

`Not Assessed`

when an area could not reasonably be assessed.

Use exactly:

`Not Applicable`

when the area does not apply.

These statuses must not be converted into findings without supporting evidence.

---

# CONTROLLED VALUES

## Severity

Allowed values:

* `CRITICAL`
* `HIGH`
* `MEDIUM`
* `LOW`
* `NIT`

## Confidence

Allowed values:

* `HIGH`
* `MEDIUM`
* `LOW`

## Category Assessment Rating

Allowed values:

* `STRONG`
* `ADEQUATE`
* `WEAK`
* `INADEQUATE`
* `NOT ASSESSED`

## Production Readiness

Allowed values:

* `READY`
* `PARTIAL`
* `NOT READY`
* `NOT APPLICABLE`
* `NOT ASSESSED`

## Review Coverage Status

Allowed values:

* `COMPLETED`
* `PARTIAL`
* `LIMITED`
* `NOT APPLICABLE`
* `NOT ASSESSED`
* `FAILED`

## Overall Risk

Allowed values:

* `CRITICAL`
* `HIGH`
* `MEDIUM`
* `LOW`

## Overall Recommendation

Allowed values:

* `APPROVE`
* `APPROVE WITH MINOR CHANGES`
* `CHANGES REQUIRED`
* `HIGH RISK`

Unsupported values are invalid.

---

# COLOR SYSTEM

## Finding Severity

| Status   | Color     |
| -------- | --------- |
| CRITICAL | `#C62828` |
| HIGH     | `#EF6C00` |
| MEDIUM   | `#F9A825` |
| LOW      | `#2E7D32` |
| NIT      | `#1565C0` |

## Category Assessment

| Status       | Color     |
| ------------ | --------- |
| STRONG       | `#2E7D32` |
| ADEQUATE     | `#66BB6A` |
| WEAK         | `#EF6C00` |
| INADEQUATE   | `#C62828` |
| NOT ASSESSED | `#757575` |

## Production Readiness

| Status         | Color     |
| -------------- | --------- |
| READY          | `#2E7D32` |
| PARTIAL        | `#F9A825` |
| NOT READY      | `#C62828` |
| NOT APPLICABLE | `#757575` |
| NOT ASSESSED   | `#757575` |

## General Document Colors

| Element             | Color     |
| ------------------- | --------- |
| Primary Header      | `#17365D` |
| Secondary Header    | `#D9EAF7` |
| Table Header        | `#D9EAF7` |
| Evidence Background | `#F4F4F4` |
| Border              | `#B7B7B7` |
| Body Text           | `#222222` |
| Muted Text          | `#666666` |

Always display textual status in addition to color.

Do not rely on color alone to communicate severity or status.

---

# COVER PAGE

## Title

`CODE REVIEW REPORT`

## Subtitle

`[Application Name]`

## Information

Display:

* Application
* Repository
* Branch
* Commit / Version
* Runtime
* Java Version
* Build Version
* Deployment Model
* Review Type
* Review Date
* Reviewer
* Total Findings

Unavailable values must use the appropriate missing-information status.

Display prominently:

* Overall Risk
* Overall Recommendation

Also include finding distribution by severity.

---

# 1. EXECUTIVE SUMMARY

## 1.0 Overall Assessment

Include:

* Overall Risk
* Overall Recommendation
* Executive Summary

The executive summary should address:

* application quality
* significant risks
* meaningful strengths
* production-readiness concerns
* remediation requirements
* release recommendation

The summary must be derived from the validated review data.

It must not contradict the validated findings.

---

## 1.1 Review Scope

Include:

* review type
* review scope
* included areas
* excluded areas
* limitations

---

## 1.2 Review Methodology

Use:

| Step | Review Activity        | Purpose                                      |
| ---- | ---------------------- | -------------------------------------------- |
| 1    | Application Discovery  | Understand application                       |
| 2    | Architecture Review    | Assess architecture                          |
| 3    | Security Review        | Identify security risks                      |
| 4    | Integration Review     | Assess dependencies and integration behavior |
| 5    | Data Review            | Assess data handling                         |
| 6    | Error Handling Review  | Evaluate failure behavior                    |
| 7    | Performance Review     | Identify performance risks                   |
| 8    | Testing Review         | Assess test coverage and effectiveness       |
| 9    | Maintainability Review | Assess maintainability                       |
| 10   | Production Readiness   | Assess release readiness                     |
| 11   | Risk Reconciliation    | Establish final verdict                      |

---

## 1.3 Findings by Severity

Calculate automatically from the validated finding inventory.

| Severity |      Count | Status |
| -------- | ---------: | ------ |
| CRITICAL | calculated | 🔴     |
| HIGH     | calculated | 🟠     |
| MEDIUM   | calculated | 🟡     |
| LOW      | calculated | 🟢     |
| NIT      | calculated | 🔵     |
| TOTAL    | calculated |        |

Counts must exactly match the complete findings inventory.

---

## 1.4 Findings by Category

Calculate automatically.

| Category        | Finding Count | Risk       |
| --------------- | ------------: | ---------- |
| Security        |    calculated | calculated |
| Architecture    |    calculated | calculated |
| API             |    calculated | calculated |
| Database        |    calculated | calculated |
| Performance     |    calculated | calculated |
| Error Handling  |    calculated | calculated |
| Configuration   |    calculated | calculated |
| Testing         |    calculated | calculated |
| Maintainability |    calculated | calculated |
| Other           |    calculated | calculated |

Categories with zero findings must still be represented where required by the report.

---

# 2. APPLICATION INVENTORY

## 2.0 Application Inventory

| Area                | Assessment |
| ------------------- | ---------- |
| Application Type    | value      |
| Runtime             | value      |
| Main Flows          | value      |
| APIs                | value      |
| Data Stores         | value      |
| External Services   | value      |
| Messaging           | value      |
| Deployment Model    | value      |
| Configuration Model | value      |
| Testing Structure   | value      |

---

## 2.1 Technology Stack

| Component    | Version | Evidence | Notes |
| ------------ | ------- | -------- | ----- |
| Runtime      | value   | evidence | notes |
| HTTP/API     | value   | evidence | notes |
| Database     | value   | evidence | notes |
| Messaging    | value   | evidence | notes |
| Build System | value   | evidence | notes |
| Testing      | value   | evidence | notes |
| Other        | value   | evidence | notes |

Evidence must reference actual repository material.

---

## 2.2 Architecture Summary

Describe:

* major components
* entry points
* processing flows
* data access
* external integrations
* error boundaries
* security boundaries
* configuration boundaries
* architectural concerns

Architecture diagrams may be included when they materially improve understanding.

Architecture diagrams must be based only on actual repository evidence.

Do not invent components, relationships, or infrastructure.

---

## 2.3 Integration Inventory

| Source | Target | Mechanism | Mode  | Retry | Transaction | Risk   |
| ------ | ------ | --------- | ----- | ----- | ----------- | ------ |
| value  | value  | value     | value | value | value       | status |

Use `Not Identified`, `Not Assessed`, or `Not Applicable` when appropriate.

---

# 3. FINDINGS

Every material finding must contain:

* ID
* Severity
* Category
* Title
* Location
* Confidence
* Problem
* Evidence
* Evidence Excerpt
* Impact
* Recommendation

The underlying structured finding must also retain the source file/location information required by the validation contract.

## Finding Ordering

Order findings by:

1. Severity, highest to lowest
2. Finding ID

Severity order:

`CRITICAL → HIGH → MEDIUM → LOW → NIT`

---

## Finding Sections

Create:

### 3.1 Critical Findings

### 3.2 High Findings

### 3.3 Medium Findings

### 3.4 Low Findings

### 3.5 Nit Findings

### 3.6 Invalid / Unclassified Findings

If a severity has no findings, display:

`No [Severity] findings identified.`

Invalid or unclassified findings must never silently disappear.

If validation rejects them, the review must fail validation rather than allowing them to be presented as valid findings.

---

## Finding Card

Each finding card must contain:

| Attribute  | Value      |
| ---------- | ---------- |
| Finding ID | ID         |
| Severity   | severity   |
| Category   | category   |
| Location   | location   |
| Confidence | confidence |

Then display:

### Problem

Finding problem statement.

### Evidence

Repository evidence supporting the finding.

### Evidence Excerpt

Relevant sanitized source excerpt where available.

### Impact

Production or technical impact.

### Recommendation

Actionable remediation.

Evidence excerpts must not expose secrets or sensitive credentials.

---

# 4. CATEGORY ASSESSMENTS

Always include:

1. Security
2. Architecture
3. Application Structure
4. Error Handling
5. Data Transformation
6. API Design
7. Connectors
8. Database
9. Messaging
10. Performance
11. Logging and Observability
12. Testing
13. Build and Dependency Management
14. Configuration
15. Maintainability

Each category must have a valid assessment status.

Rating values:

* `STRONG`
* `ADEQUATE`
* `WEAK`
* `INADEQUATE`
* `NOT ASSESSED`

Use `Not Applicable` in the content where the report schema permits applicability status, but do not substitute an unsupported rating value for a category field that requires the controlled rating enumeration.

---

## Category Assessment Template

| Attribute      | Result |
| -------------- | ------ |
| Rating         | value  |
| Evidence Level | value  |
| Key Concern    | value  |

Then include:

### Summary

Category assessment summary.

### Positive Observations

Meaningful evidence-backed strengths.

### Gaps

Evidence-backed gaps or limitations.

Do not convert a category weakness into a finding unless the finding itself satisfies the finding evidence requirements.

---

# 5. PRODUCTION READINESS ASSESSMENT

## 5.0 Overall Readiness

Allowed values:

* `READY`
* `PARTIAL`
* `NOT READY`
* `NOT APPLICABLE`
* `NOT ASSESSED`

Include an evidence-based summary.

The readiness result must be consistent with the validated findings and production-readiness assessment.

---

## 5.1 Readiness Dimensions

| Dimension           | Status | Notes |
| ------------------- | ------ | ----- |
| Security            | value  | notes |
| Reliability         | value  | notes |
| Error Recovery      | value  | notes |
| Idempotency         | value  | notes |
| Observability       | value  | notes |
| Performance         | value  | notes |
| Scalability         | value  | notes |
| Configuration       | value  | notes |
| Testing             | value  | notes |
| Operational Support | value  | notes |

---

## 5.2 Positive Observations

| Positive Observation | Supporting Evidence |
| -------------------- | ------------------- |
| observation          | evidence            |

Only meaningful, evidence-backed observations should be included.

---

# 6. RISK AND RECOMMENDATION

## 6.1 Risk Summary

| Priority | Risk Theme | Impact | Related Findings |
| -------- | ---------- | ------ | ---------------- |
| 1        | value      | value  | IDs              |

Sort by production impact.

Risk themes must be traceable to findings or clearly documented review evidence.

---

## 6.2 Remediation Priorities

Maximum:

`10`

| Priority | Remediation | Impact | Related Findings |
| -------- | ----------- | ------ | ---------------- |
| 1        | action      | impact | IDs              |

Ranking principle:

**Production impact > severity alone**

Severity is still a major input, but remediation priority should consider the practical production consequences and dependencies between remediations.

Do not create more than 10 remediation priorities.

---

## 6.3 Review Limitations

| Area | Limitation | Reason | Effect |
| ---- | ---------- | ------ | ------ |
| area | limitation | reason | effect |

Limitations must clearly distinguish unavailable evidence from confirmed defects.

---

## 6.4 Overall Risk and Recommendation

Include:

* Overall Risk
* Overall Recommendation
* Recommendation Rationale

The result must satisfy the verdict reconciliation rules.

---

# APPENDIX A — COMPLETE FINDINGS INVENTORY

Every valid finding must appear exactly once in the complete findings inventory.

| ID | Severity | Category | Confidence | Title | Location |
| -- | -------- | -------- | ---------- | ----- | -------- |

The appendix is a reconciliation view of the detailed findings.

It must not introduce findings that do not exist in the primary finding inventory.

Include:

* Detailed Findings
* Appendix Findings
* Reconciliation Status

Reconciliation must be programmatically validated.

---

# APPENDIX B — FINDING EVIDENCE DETAIL

For each finding:

### ID — Title

#### Evidence

Evidence supporting the finding.

#### Evidence Context

Additional context required to understand the evidence.

Evidence must remain faithful to repository evidence.

Evidence must be sanitized.

No secrets may appear in this appendix.

---

# APPENDIX C — REVIEW COVERAGE AND BOUNDARIES

## C.1 Review Coverage

| Review Area           | Status    | Notes |
| --------------------- | --------- | ----- |
| Application Discovery | COMPLETED | notes |
| Architecture Analysis | COMPLETED | notes |
| Security Analysis     | COMPLETED | notes |
| Database Analysis     | COMPLETED | notes |
| Messaging Analysis    | status    | notes |
| Performance Analysis  | status    | notes |
| Testing Analysis      | status    | notes |

Allowed status values:

* `COMPLETED`
* `PARTIAL`
* `LIMITED`
* `NOT APPLICABLE`
* `NOT ASSESSED`
* `FAILED`

Every required review area must be accounted for.

---

## C.2 Review Controls

| Control                             | Status    |
| ----------------------------------- | --------- |
| Review conducted in read-only mode  | CONFIRMED |
| Application source was not modified | CONFIRMED |
| No source changes introduced        | CONFIRMED |
| No dependency changes introduced    | CONFIRMED |
| No remediation performed            | CONFIRMED |
| Findings are evidence-backed        | CONFIRMED |
| Unverifiable areas recorded         | CONFIRMED |
| Finding counts reconciled           | CONFIRMED |
| Final verdict reconciled            | CONFIRMED |

A control must not be marked `CONFIRMED` when the corresponding validation has failed.

---

# VERDICT RECONCILIATION

The final verdict is derived from the complete validated finding inventory.

| Findings Present | Minimum Risk | Minimum Recommendation     |
| ---------------- | ------------ | -------------------------- |
| Any CRITICAL     | CRITICAL     | HIGH RISK                  |
| Any HIGH         | HIGH         | CHANGES REQUIRED           |
| Any MEDIUM       | MEDIUM       | CHANGES REQUIRED           |
| LOW or NIT only  | LOW          | APPROVE WITH MINOR CHANGES |
| No findings      | LOW          | APPROVE                    |

## Rules

1. A more severe verdict is allowed.
2. A less severe verdict must be raised to the minimum required level.
3. The originally stated verdict may be retained as input data, but the final reconciled verdict is authoritative.
4. The report must explain any reconciliation that changes the stated verdict.
5. The final verdict must be consistent with the validated findings.
6. The validator must enforce these rules.
7. Report generation must use the reconciled verdict rather than an unvalidated verdict.

---

# STRUCTURED REVIEW DATA CONTRACT

The structured review is the authoritative input to validation and report generation.

At minimum, the structured review must contain:

## Review Metadata

* application
* repository
* branch
* commit/version
* runtime
* Java version
* build version
* deployment model
* review type
* review date
* reviewer

Unavailable metadata must use the appropriate missing-information classification.

## Application Inventory

Must contain the information required by Section 2.

## Findings

Each finding must contain:

* `id`
* `severity`
* `category`
* `title`
* `location`
* `confidence`
* `problem`
* `evidence`
* `evidence_excerpt`
* `impact`
* `recommendation`

Where required by the implementation contract, file information must be retained separately or as part of `location`.

## Category Assessments

Every required category must have an assessment.

## Production Readiness

Must contain:

* overall readiness
* readiness dimensions
* supporting notes
* positive observations where applicable

## Risk and Recommendation

Must contain:

* risk summary
* remediation priorities
* limitations
* overall risk
* overall recommendation
* recommendation rationale

## Coverage

Must contain:

* review coverage
* review controls

---

# DATA INTEGRITY RULES

The validator must ensure:

1. Every finding has a unique ID.
2. Every finding uses an allowed severity.
3. Every finding uses an allowed confidence.
4. Every finding has a category.
5. Every finding has a title.
6. Every finding has a location.
7. Every material finding has evidence.
8. Every material finding has impact.
9. Every material finding has a recommendation.
10. Finding counts match the actual finding inventory.
11. Severity counts match the actual finding inventory.
12. Category counts match the actual finding inventory.
13. Appendix A contains exactly the same finding IDs as the primary findings.
14. Appendix B contains evidence for every finding.
15. No duplicate finding IDs exist.
16. No invalid severity values exist.
17. No invalid confidence values exist.
18. Required category assessments exist.
19. Required production-readiness dimensions exist.
20. The final verdict satisfies reconciliation rules.
21. Remediation priorities do not exceed 10.
22. Required limitations are recorded where applicable.
23. Required review coverage is recorded.
24. Secrets are not present in report evidence.
25. The generated report contains exactly one final report artifact.

---

# DOCUMENT VALIDATION

Verify that the generated Word document contains:

* Cover Page
* Executive Summary
* Application Inventory
* Findings
* Category Assessments
* Production Readiness
* Risk and Recommendation
* Appendix A
* Appendix B
* Appendix C

No required section may be silently omitted.

---

## Finding Validation

Verify that every finding contains:

* ID
* severity
* category
* location
* confidence
* evidence
* impact
* recommendation

Verify that:

* finding IDs are unique
* severity values are valid
* confidence values are valid
* categories are valid
* evidence is present
* evidence is sanitized
* findings are reconciled

---

## Reconciliation Validation

Verify:

* severity counts match
* category counts match
* Appendix A matches the primary finding inventory
* Appendix B matches the primary finding inventory
* risk is reconciled
* recommendation is reconciled
* production readiness is consistent
* limitations are documented
* coverage is documented

---

## Visual Validation

Verify:

* severity colors are consistent
* status colors are consistent
* textual status accompanies color
* tables are readable
* finding cards are visually distinct
* evidence blocks are visually distinct
* headings are numbered
* required sections are present
* page breaks are reasonable
* headers and footers are consistent
* no content is clipped or unreadable
* no required finding is hidden or omitted

---

# REPORT GENERATION PRINCIPLES

The Word generator owns document formatting.

Claude must not manually construct the Word document.

The generator must:

* consume validated structured review data
* apply the defined color system
* generate all required sections
* calculate presentation counts from the finding inventory
* render findings in severity order
* render category assessments
* render production-readiness assessment
* render risk and recommendation
* render remediation priorities
* render limitations
* render all required appendices
* perform final filename generation

The final output must use:

`reports/CODE_REVIEW_REPORT_<YYYYMMDD-HHMMSS>.docx`

Only the generated Word document is the official review artifact.

---

# REPORT RECONCILIATION PRINCIPLE

There must be one authoritative finding inventory.

The same finding inventory drives:

* executive severity counts
* category counts
* detailed finding cards
* risk summary
* remediation priorities
* Appendix A
* Appendix B
* final risk reconciliation
* final recommendation reconciliation

No section may maintain an independent finding count.

This prevents contradictory numbers or verdicts within the report.

---

# FINAL REPORT QUALITY STANDARD

The final report must allow a technically qualified reviewer to answer:

1. What application was reviewed?
2. What was reviewed?
3. What was not reviewed?
4. What evidence was available?
5. What are the material risks?
6. Where is each risk located?
7. What evidence supports each finding?
8. What is the production impact?
9. How confident is each finding?
10. What should be remediated first?
11. Is the application production-ready?
12. What is the overall risk?
13. What is the release recommendation?
14. Are all findings and verdicts internally reconciled?

If these questions cannot be answered from the generated report, the report is incomplete.