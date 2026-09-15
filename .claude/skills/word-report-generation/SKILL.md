# Word Report Generation Skill

## Purpose

Generate a professional, executive-quality Microsoft Word document containing the complete MuleSoft Standards Review.

The final deliverable MUST be a `.docx` file.

The report must be visually polished and suitable for sharing with:

- Enterprise Architects
- MuleSoft Architects
- Senior Technical Leads
- Development Teams
- Engineering Managers
- Project Managers
- Technical Stakeholders

The report must not be a simple text dump of findings.

It should look like a professionally prepared architecture and technical assessment.

---

# 1. Output Location

The final document MUST be created under:

${GITHUB_WORKSPACE}/reports/

The filename MUST follow:

mulesoft-standards-review_<timestamp>.docx

Example:

mulesoft-standards-review_20260911_143025.docx

Use a timestamp that is safe for filenames.

Do not overwrite an existing report unless explicitly instructed.

---

# 2. Primary Responsibility

You are responsible for generating the Word document from the completed review information.

The report should contain:

- Executive summary
- Architecture assessment
- Application overview
- MuleSoft standards assessment
- Security assessment
- API security assessment
- Connector assessment
- Configuration assessment
- Logging assessment
- Performance assessment
- Error handling assessment
- MUnit assessment
- Custom code assessment
- Detailed findings
- Positive observations
- Remediation roadmap
- Final scorecard

---

# 3. Source Information

Use the review information produced by the MuleSoft review agents.

Relevant review areas include:

- mule-code-reviewer
- logging-reviewer
- munit-reviewer
- other applicable review outputs
- final review/validation information

Do not invent review results.

If a value cannot be established from the repository or review output, use:

Not Available

or:

Verification Required

where appropriate.

---

# 4. Repository Scope

The MuleSoft application is:

${GITHUB_WORKSPACE}

The code-review framework is:

${GITHUB_WORKSPACE}/code-review

Reports are:

${GITHUB_WORKSPACE}/reports

The following MUST NOT be treated as MuleSoft application source:

${GITHUB_WORKSPACE}/code-review/**
${GITHUB_WORKSPACE}/reports/**

---

# 5. Report Design Philosophy

The document should be:

- Professional
- Modern
- Clean
- Executive-friendly
- Technical enough for architects
- Easy to navigate
- Visually attractive
- Evidence-based
- Action-oriented

Avoid:

- Excessive decoration
- Excessive colors
- Huge paragraphs
- Repeating the same finding
- Unnecessary screenshots
- Unnecessary tables
- Fake metrics
- Fabricated charts

---

# 6. Recommended Document Structure

Create the report using this structure where applicable:

1. Cover Page
2. Document Control
3. Executive Summary
4. Overall Assessment Dashboard
5. Scope and Methodology
6. Application Overview
7. Architecture Assessment
8. MuleSoft Standards Assessment
9. Code Quality Assessment
10. API Assessment
11. Connector Assessment
12. Security Assessment
13. Performance Assessment
14. Logging Assessment
15. Error Handling Assessment
16. Configuration and Properties Assessment
17. MUnit/Test Coverage Assessment
18. Custom Code Assessment
19. Detailed Findings
20. Positive Observations
21. Remediation Roadmap
22. Final Scorecard
23. Appendix

Do not create empty sections.

If a section is not applicable, omit it or explicitly state:

Not Applicable

---

# 7. Cover Page

The cover page should contain:

# MuleSoft Standards Review

Subtitle:

Architecture, Code Quality, Security, Performance and Production Readiness Assessment

Include:

- Application name
- Review date
- Git branch
- Commit SHA if available
- Reviewer: MuleSoft Architecture Review
- Confidentiality classification if appropriate

Use a professional visual design.

---

# 8. Document Control

Include a small table containing:

| Field | Value |
|---|---|
| Application | Application name |
| Branch | develop |
| Review Date | Date |
| Commit | Commit SHA |
| Review Type | MuleSoft Standards Review |
| Scope | Full application |
| Report Version | Version |

Only populate values that can be determined.

---

# 9. Executive Summary

The Executive Summary must be concise.

It should communicate:

- Overall architecture
- Overall health
- Major strengths
- Major risks
- Security posture
- Performance posture
- Testing posture
- Highest-priority actions

Do not place every finding here.

The executive summary should allow a senior stakeholder to understand the application within a few minutes.

---

# 10. Overall Assessment Dashboard

Create a visual dashboard.

Include, where data exists:

- Overall score
- Critical findings
- High findings
- Medium findings
- Low findings
- Warnings
- MUnit coverage
- Connector count
- Flow count
- Global configuration count

Do not fabricate metrics.

---

# 11. Scorecard

Create category scores where sufficient information exists.

Recommended categories:

- Architecture
- Code Quality
- Security
- API
- Connectors
- Performance
- Logging
- Configuration
- Error Handling
- MUnit
- Maintainability

Scores may use:

0–100

or:

Excellent
Good
Needs Improvement
Poor

Use one consistent scoring methodology.

Explain the methodology briefly.

---

# 12. Score Calculation

Do not randomly assign scores.

Scores should reflect actual findings.

For example:

Excellent:
No significant findings.

Good:
Minor issues with no major production risk.

Needs Improvement:
Several meaningful findings.

Poor:
High-risk or widespread issues.

Critical findings must materially affect the relevant category score.

---

# 13. Severity Distribution

Create a visual severity distribution.

Preferred chart:

Doughnut or pie chart.

Categories:

- Critical
- High
- Medium
- Low
- Warning

Use actual finding counts.

Do not create a chart when there is insufficient data.

---

# 14. Findings by Category

Create a chart showing findings by category.

Possible categories:

- Architecture
- Security
- Performance
- Code Quality
- Connector
- Configuration
- Logging
- API
- MUnit
- Error Handling
- Maintainability

Use actual counts.

---

# 15. Architecture Assessment

Describe the architecture discovered from the repository.

Include:

- Architecture style
- Main application layers
- APIs
- Flows
- External systems
- Databases
- Messaging
- File integrations
- SaaS integrations
- Transformation layers

Clearly distinguish observed architecture from recommendations.

---

# 16. Architecture Diagram

Create a professional architecture diagram where sufficient information exists.

The diagram should show:

- Application/API entry point
- Main Mule flows
- Processing layer
- Downstream systems
- Databases
- Messaging
- External APIs
- File systems
- Important integrations

Use arrows to represent major data/integration relationships.

Do not invent systems.

If architecture information is insufficient, provide a textual architecture summary instead.

---

# 17. Architecture Diagram Design

Use professional colors.

Recommended:

Application/API:
Blue

Mule processing:
Purple

Database:
Green

External systems:
Orange

Messaging:
Teal

Files:
Gray

Security:
Red accent

Keep the diagram readable.

Do not overcrowd the page.

---

# 18. MuleSoft Standards Assessment

Provide an overview of:

- Naming
- Flow design
- Reusability
- DataWeave
- Configuration
- Error handling
- Connector usage
- Maintainability

Use concise tables and visual indicators.

---

# 19. Connector Assessment

Create a connector summary.

Recommended table:

| Connector | Usage | Global Config | Timeout | Retry | Pooling | TLS | Assessment |
|---|---:|---|---|---|---|---|---|

Only include applicable columns.

Highlight meaningful problems.

Do not mark a setting as missing if it is not applicable.

---

# 20. Global Configuration Assessment

Summarize:

- Number of global configurations
- Connector configuration reuse
- Duplicate configurations
- Missing configuration concerns
- Authentication configuration
- TLS configuration
- Timeout configuration
- Pooling configuration

---

# 21. Security Assessment

Provide a dedicated security section.

Include:

- Secure properties
- Password protection
- Credentials
- Tokens
- API security
- TLS
- Sensitive logging
- Input validation
- Error exposure

Use clear severity indicators.

---

# 22. Password Security

If passwords are properly protected:

Show:

PASS

If plaintext passwords are found:

Show:

FAIL

and provide:

- Location
- Evidence summary
- Risk
- Recommended MuleSoft secure property approach

Never print the actual password.

---

# 23. API Security

Summarize:

- Authentication
- Authorization
- TLS
- API policies
- Input validation
- Rate limiting
- Error responses

If external API Manager policies cannot be verified:

Display:

Verification Required

Do not state that API security is missing without evidence.

---

# 24. Performance Assessment

Include:

- Major performance findings
- Duplicate downstream calls
- Sequential calls
- Parallelization opportunities
- DataWeave inefficiencies
- Large payload handling
- Streaming
- Pagination
- Batch processing
- Timeout configuration
- Retry behavior
- Connection pooling
- Logging overhead

Provide practical recommendations.

---

# 25. Performance Opportunity Table

Use:

| Area | Observation | Impact | Recommendation | Priority |
|---|---|---|---|---|

Do not list trivial optimization ideas.

---

# 26. Logging Assessment

Include:

- Logging coverage
- Correlation ID
- Error logging
- Flow traceability
- Sensitive information
- Payload logging
- Log levels
- Duplicate logging
- Logging performance

Provide a concise assessment.

---

# 27. Error Handling Assessment

Include:

- Global error handlers
- Flow-level error handlers
- On Error Continue
- On Error Propagate
- Retry
- Error mapping
- API error responses
- Error logging

Highlight meaningful gaps.

---

# 28. Configuration and Properties

Review:

- .properties
- .yaml
- .yml
- JSON configuration where applicable
- Secure properties
- DEV
- QA
- UAT
- PROD
- Other environments

Show environment consistency where useful.

---

# 29. Environment Comparison Table

Where environment files exist, provide:

| Property Key | DEV | QA | UAT | PROD | Assessment |
|---|---|---|---|---|---|

Do not expose:

- Passwords
- Tokens
- API keys
- Secrets

Replace sensitive values with:

[REDACTED]

For large property files, summarize rather than printing every property.

---

# 30. Unused Property Assessment

Provide:

- Potential unused properties
- Evidence
- Confidence
- Recommendation

If usage cannot be determined:

Verification Required

Do not present uncertain results as confirmed.

---

# 31. MUnit Assessment

Include:

- Total test suites
- Total tests
- Covered flows
- Uncovered important flows
- Assertions
- Mocks
- Negative tests
- Error scenarios

Where coverage percentage can be reliably calculated, show it.

---

# 32. MUnit Coverage Chart

If meaningful data exists, create a chart:

Covered
Uncovered

Use a doughnut chart or bar chart.

Do not fabricate percentages.

---

# 33. MUnit Recommendations

For important uncovered flows, provide:

| Flow | Missing Test Coverage | Recommended Test |
|---|---|---|

Recommended tests may include:

- Happy path
- Invalid input
- Connector failure
- Timeout
- Authentication failure
- Business error
- Empty payload
- Null value
- Error handler

---

# 34. Custom Code Assessment

Summarize:

- Java files
- Python files
- Other custom code
- Purpose
- Native MuleSoft replacement opportunity

Use:

| Custom Code | Purpose | MuleSoft Alternative | Recommendation |
|---|---|---|---|

Do not recommend removal when custom code is justified.

---

# 35. Detailed Findings

Every actionable finding should have a dedicated presentation.

Use:

### Finding ID — Title

Then:

| Attribute | Value |
|---|---|
| Severity | High |
| Category | Security |
| Priority | Immediate |
| Location | file.xml / flow |
| Status | Open |

Then include:

### Evidence

What was found.

### Impact

Why it matters.

### Recommendation

What should change.

### Solution

How to implement the improvement.

---

# 36. Finding Severity Colors

Use consistent colors.

Critical:
Dark red

High:
Red

Medium:
Orange

Low:
Blue

Warning:
Amber

Informational:
Gray

Do not use bright colors that reduce readability.

---

# 37. Finding Tables

Do not create unnecessarily wide tables.

If a table contains too many columns, split it into multiple tables.

Landscape orientation may be used for wide technical tables.

---

# 38. Positive Observations

Create a dedicated section.

Highlight meaningful strengths.

Examples:

- Good global connector reuse.
- Strong secure configuration.
- Good error handling.
- Good MUnit coverage.
- Effective correlation IDs.
- Strong API architecture.
- Good DataWeave organization.
- Good environment separation.

---

# 39. Remediation Roadmap

Create a prioritized roadmap.

## Immediate

Critical and high-risk findings.

## Short Term

Important medium-risk findings.

## Medium Term

Maintainability and architecture improvements.

## Long Term

Strategic improvements.

Use a table:

| Priority | Finding | Action | Expected Benefit |
|---|---|---|---|

---

# 40. Final Scorecard

Create a final summary table:

| Category | Score | Status | Key Observation |
|---|---:|---|---|

Categories:

- Architecture
- Code Quality
- Security
- API
- Connectors
- Performance
- Logging
- Configuration
- Error Handling
- MUnit
- Maintainability

---

# 41. Appendix

Include useful technical information that is too detailed for the executive sections.

Possible contents:

- Flow inventory
- Connector inventory
- Global configuration inventory
- MUnit inventory
- Configuration inventory
- Custom code inventory
- Finding index

Do not include sensitive information.

---

# 42. No Unnecessary Reporting

The final document must not become a dump of every observation.

Do not report:

- Trivial formatting preferences.
- Harmless naming differences.
- Every possible optimization.
- Theoretical vulnerabilities.
- Unsupported architecture assumptions.
- Duplicate findings.
- Issues without evidence.

The goal is high-quality architectural guidance.

---

# 43. Every Problem Needs a Solution

Do not create a finding that only says:

"Problem detected."

Every finding must explain:

1. What is wrong.
2. Why it matters.
3. How to fix it.
4. What MuleSoft capability or pattern should be considered.
5. Expected benefit.

---

# 44. No Fabricated Data

Never invent:

- Finding counts
- Scores
- MUnit coverage
- Connector counts
- Flow counts
- Architecture components
- Performance metrics
- Security status

Use actual repository/review evidence.

---

# 45. No Secret Exposure

Before saving the Word document, verify that the report does not contain actual:

- Passwords
- API keys
- Access tokens
- Client secrets
- Private keys
- Authorization headers
- Sensitive credentials

Redact sensitive values.

Use:

[REDACTED]

---

# 46. Document Quality

The generated Word document must:

- Open successfully.
- Contain valid Word content.
- Use consistent headings.
- Use readable fonts.
- Use professional colors.
- Contain properly formatted tables.
- Contain charts where useful.
- Contain page numbers.
- Contain headers/footers where appropriate.
- Avoid broken tables.
- Avoid clipped text.
- Avoid overlapping elements.
- Avoid empty pages.
- Avoid excessive whitespace.

---

# 47. Recommended Typography

Use a modern professional font.

Preferred:

Aptos

or:

Calibri

Suggested sizing:

Title:
28–32 pt

Section heading:
18–22 pt

Subheading:
14–16 pt

Body:
10–11 pt

Table:
9–10 pt

Do not make the report unnecessarily large.

---

# 48. Color Palette

Use a consistent corporate-style palette.

Recommended:

Primary:
#1F4E78

Secondary:
#5B9BD5

Accent:
#70AD47

Warning:
#FFC000

High Risk:
#C00000

Critical:
#7F0000

Neutral:
#595959

Light background:
#F3F6F9

Use color primarily for:

- Headings
- Severity indicators
- Charts
- Table headers
- Callout boxes

---

# 49. Tables

Tables should:

- Have clear headers.
- Use alternating row shading where useful.
- Keep text readable.
- Avoid excessive columns.
- Repeat header rows when tables span pages.
- Use appropriate column widths.

Avoid huge tables containing entire source files.

---

# 50. Charts

Charts should be used when they communicate information better than a table.

Good candidates:

- Severity distribution
- Findings by category
- MUnit coverage
- Scorecard
- Environment comparison
- Connector distribution

Do not add charts purely for decoration.

---

# 51. Pie/Doughnut Charts

Use pie/doughnut charts for:

- Severity distribution
- MUnit covered vs uncovered

Do not use pie charts for many categories.

For many categories use a bar chart.

---

# 52. Bar Charts

Use bar charts for:

- Findings by category
- Score by category
- Connector usage
- Environment differences

Ensure labels remain readable.

---

# 53. Architecture Visualization

Where possible, create a clean architecture visualization.

Use:

- Rounded rectangles
- Consistent colors
- Arrows
- Short labels
- Grouped systems

Avoid extremely detailed processor-level diagrams.

The architecture diagram should communicate architecture, not replace the source code.

---

# 54. Page Layout

Use:

- Portrait for normal sections.
- Landscape for very wide tables or architecture diagrams.

Maintain reasonable margins.

Do not create extremely narrow text columns.

---

# 55. Header and Footer

Header may contain:

MuleSoft Standards Review

Footer should contain:

- Confidentiality label if appropriate.
- Report date.
- Page number.

Example:

MuleSoft Standards Review | Confidential | Page 12

---

# 56. Table of Contents

Create a Table of Contents using actual heading styles.

The document should have navigable headings where supported.

Do not manually type page numbers into the table of contents.

---

# 57. Executive Readability

A senior stakeholder should be able to understand:

- Overall health
- Major risks
- Architecture
- Security
- Performance
- Testing
- Recommended actions

without reading every detailed finding.

---

# 58. Technical Readability

A developer should be able to use the detailed findings to understand:

- Where the problem exists.
- Why it matters.
- What should change.
- How to implement the solution.

---

# 59. Report Validation Before Completion

Before considering document generation complete, verify:

- File exists.
- File extension is `.docx`.
- File is under reports/.
- Filename contains timestamp.
- Document opens.
- Cover page exists.
- Executive summary exists.
- Architecture section exists.
- Security section exists.
- Performance section exists.
- Connector section exists.
- Logging section exists.
- Error handling section exists.
- Configuration section exists.
- MUnit section exists.
- Custom code section exists where applicable.
- Detailed findings exist where findings exist.
- Positive observations exist.
- Remediation roadmap exists.
- Scorecard exists.
- Charts contain real data.
- Statistics are consistent.
- No secrets are present.
- No fabricated information exists.

---

# 60. Final Response Requirement

After successfully generating the Word document, return the exact location.

The response MUST include:

Download full report: <absolute path>

Example:

Download full report: /home/runner/work/my-repo/my-repo/reports/mulesoft-standards-review_20260911_143025.docx

Do not claim the document exists until it has actually been created successfully.

The final path returned MUST point to the actual generated `.docx` file.