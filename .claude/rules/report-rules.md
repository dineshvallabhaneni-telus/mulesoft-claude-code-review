# MuleSoft Review Report Rules

## Purpose

Define the mandatory rules for creating the final Microsoft Word (`.docx`) architecture and standards review report.

The final report must be professional, visually clear, technically accurate, evidence-based, and suitable for review by architects, technical leads, engineering managers, and project stakeholders.

---

## 1. Required Deliverable

The primary deliverable is a Microsoft Word document:

`mulesoft-standards-review_<timestamp>.docx`

The document must be created under:

`${GITHUB_WORKSPACE}/reports/`

The report must be a real `.docx` file.

Do not treat:

- Markdown
- HTML
- Plain text
- `summary.txt`
- PDF

as the final deliverable.

The final deliverable is the Word document.

---

## 2. Report Audience

The report must be suitable for:

- Enterprise Architects
- MuleSoft Architects
- Senior Technical Leads
- Senior Developers
- Engineering Managers
- Project Managers
- Technical Support Teams
- Security Teams

The report must contain both:

- Executive-level information
- Detailed technical evidence

Technical detail should not overwhelm the executive summary.

---

## 3. Report Structure

Use the following structure where applicable:

1. Cover Page
2. Table of Contents
3. Executive Summary
4. Overall Assessment
5. Architecture Overview
6. Architecture Diagram
7. Application Inventory
8. MuleSoft Standards Assessment
9. API Security Assessment
10. Security Assessment
11. Connector Assessment
12. Configuration and Property Assessment
13. Performance Assessment
14. Logging and Observability Assessment
15. Error Handling Assessment
16. DataWeave Assessment
17. MUnit Assessment
18. Custom Code Assessment
19. Duplication Assessment
20. Naming and Maintainability Assessment
21. Findings Summary
22. Detailed Findings
23. Recommended MUnit Test Scenarios
24. Remediation Roadmap
25. Positive Observations
26. Final Architect Assessment

Do not create empty sections.

If a category is not applicable, either omit it or state briefly that it was not applicable.

---

## 4. Cover Page

The cover page should contain:

- Report title
- MuleSoft application/repository name where identifiable
- Review date
- Review timestamp
- Branch reviewed
- Review scope
- Framework version where available
- Overall assessment

Example title:

`MuleSoft Architecture & Standards Review`

The cover page should look professional and should not expose secrets or sensitive configuration values.

---

## 5. Executive Summary

The executive summary must provide a concise overview of the application quality.

Include:

- Overall assessment
- Major strengths
- Major risks
- Critical findings count
- High findings count
- Medium findings count
- Low findings count
- Warning count
- Key architecture observations
- Security posture
- Performance posture
- Testing posture
- Top remediation priorities

Do not fabricate metrics.

Counts must be derived from the actual final findings.

---

## 6. Overall Assessment

Provide an overall assessment based on the actual review.

Possible assessment labels include:

- Strong
- Good
- Satisfactory
- Needs Improvement
- High Risk
- Critical Risk

The assessment must be justified by evidence.

Do not assign a poor rating merely because minor findings exist.

---

## 7. Architecture Section

The architecture section must explain the architecture actually identified in the application.

Include where applicable:

- Architecture style
- API-led characteristics
- System API / Process API / Experience API characteristics
- Integration boundaries
- External systems
- Data flow
- Synchronous/asynchronous patterns
- Reusable components
- Error-handling architecture
- Configuration architecture
- Security boundaries
- Major dependencies
- Architectural strengths
- Architectural weaknesses

Do not claim that an architecture pattern exists without evidence.

---

## 8. Architecture Diagram

The report should contain a professional architecture diagram when sufficient information exists.

The diagram may represent:

- Mule application
- API layer
- Flows
- External systems
- Databases
- Queues
- HTTP endpoints
- SaaS systems
- Other connectors
- Data movement

Use the actual repository evidence.

Do not invent systems or dependencies.

If the architecture cannot be determined reliably, state the limitation instead of fabricating a diagram.

---

## 9. Application Inventory

Provide a useful inventory where practical.

Examples include:

- Number/type of Mule configuration files
- Number of flows
- Number of subflows
- Number of private flows
- Connectors
- Global configurations
- MUnit test files
- Property files
- YAML files
- Custom Java
- Custom Python
- APIs/endpoints
- Environment configurations

Only report values that can be reliably derived.

---

## 10. Findings Summary

Provide a visual summary of findings.

Recommended presentation:

| Severity | Count |
|---|---:|
| Critical | N |
| High | N |
| Medium | N |
| Low | N |
| Warning | N |

Counts must exactly match the detailed findings.

Do not manually estimate counts.

---

## 11. Charts

Use charts when they provide useful information.

Appropriate examples include:

- Findings by severity
- Findings by category
- Architecture component distribution
- Connector usage
- MUnit coverage when reliable data exists
- Remediation priority distribution

Pie charts, bar charts, doughnut charts, and other appropriate visualizations may be used.

Do not create charts merely for decoration.

Do not create a chart when there is insufficient data.

Never fabricate chart data.

---

## 12. Category Assessment

Where sufficient evidence exists, provide an assessment for major categories:

- Architecture
- Security
- API Security
- Connectors
- Performance
- Configuration
- Logging
- Error Handling
- DataWeave
- MUnit
- Maintainability
- Custom Code

The assessment should be supported by findings and observations.

---

## 13. Detailed Finding Format

Each detailed finding should contain:

### Finding ID

Example:

`MSR-SEC-001`

### Title

Clear and concise description.

### Severity

One of:

- Critical
- High
- Medium
- Low
- Warning
- Informational

### Category

Examples:

- Security
- API Security
- Architecture
- Performance
- Connector
- Configuration
- Logging
- MUnit
- Maintainability

### Location

Include:

- File
- Flow/configuration
- Component
- Property
- Other useful location information

### Evidence

Describe what was found.

Do not reproduce secrets.

### Impact

Explain the technical/business/operational consequence.

### Recommendation

Explain what should be changed.

### Solution

Provide a practical implementation approach.

### Priority

Indicate remediation priority where useful.

---

## 14. Finding Tables

Use visually clear tables for findings.

Recommended columns:

| ID | Severity | Category | Finding | Location |
|---|---|---|---|---|

For detailed findings, use a structured layout rather than extremely wide tables.

Avoid tables so wide that the content becomes unreadable.

---

## 15. Severity Colors

Use consistent visual severity indicators.

Recommended colors:

- Critical: Dark Red
- High: Red
- Medium: Orange
- Low: Yellow/Amber
- Warning: Blue
- Informational: Gray or Green

Maintain sufficient contrast and readability.

Do not use color as the only indicator of severity.

Always include the severity text.

---

## 16. Positive Observations

Include meaningful positive observations.

Examples:

- Strong connector reuse
- Good secure configuration
- Good API security
- Strong error handling
- Good MUnit coverage
- Effective logging
- Appropriate architecture separation
- Efficient DataWeave

Do not exaggerate positive observations.

Do not claim "best practice" without evidence.

---

## 17. MUnit Section

The MUnit section must include:

- Existing MUnit test coverage observations
- Important flows with tests
- Important flows without tests
- Test quality observations
- Missing negative-path tests
- Missing error-path tests
- Missing edge-case tests
- Recommended test scenarios

If MUnit coverage percentage is unavailable, do not invent one.

When coverage is missing, identify the relevant flows and recommend tests.

---

## 18. Recommended MUnit Test Scenarios

For important untested flows, provide practical scenarios.

Example format:

| Flow | Scenario | Expected Result | Priority |
|---|---|---|---|

Scenarios may include:

- Successful processing
- Invalid request
- Authentication failure
- Downstream failure
- Timeout
- Retry exhaustion
- Error handling
- Empty payload
- Invalid data
- Boundary conditions

Only recommend scenarios relevant to the actual implementation.

---

## 19. Connector Section

Summarize connector usage.

Where useful, include:

| Connector | Usage | Global Config | Timeout | Retry | Pooling | Assessment |
|---|---|---|---|---|---|---|

Do not claim a configuration is missing if it is managed externally or inherited through a valid MuleSoft mechanism.

---

## 20. Configuration Section

Summarize:

- Property files
- YAML files
- Environment files
- Secure property usage
- Unused properties
- Missing properties
- Environment inconsistencies
- Duplicate configurations

Do not expose sensitive values.

When identifying a sensitive property, show only the property name/location.

---

## 21. Security Section

Security findings must be summarized clearly.

Include:

- Credential protection
- Secure property usage
- API authentication
- API authorization
- TLS
- Sensitive data handling
- Logging security
- Error-response security
- Secret exposure
- Dependency security where verified

Do not reproduce secrets.

---

## 22. Performance Section

Summarize meaningful performance concerns.

Include:

- Identified bottlenecks
- Connector performance
- Connection management
- Timeouts
- Retries
- Pooling
- DataWeave efficiency
- Streaming
- Large payload handling
- Repeated downstream calls
- Duplicate processing
- Logging overhead

Do not present theoretical optimizations as confirmed performance defects.

---

## 23. Logging and Observability Section

Assess whether production support can understand application execution.

Include:

- Flow traceability
- Correlation ID
- Important business/process logging
- Error logging
- Downstream integration visibility
- Sensitive data protection
- Excessive logging
- Missing operational logging

Explain how observability can be improved.

---

## 24. Remediation Roadmap

Provide a prioritized remediation roadmap.

Recommended grouping:

### Immediate

Critical/high-risk issues requiring prompt action.

### Short Term

Important issues that should be addressed in the near term.

### Medium Term

Architectural and maintainability improvements.

### Long Term

Optimization and strategic improvements.

The roadmap must be derived from actual findings.

Do not create roadmap items unrelated to findings.

---

## 25. Remediation Priority

Prioritize based on:

1. Security impact
2. Production risk
3. Business impact
4. Data protection
5. Reliability
6. Performance
7. Architecture
8. Maintainability
9. Testing
10. Cosmetic improvements

Do not prioritize purely by finding count.

---

## 26. Report Accuracy

The report must contain only information supported by the review.

Never fabricate:

- Findings
- Metrics
- Coverage
- Architecture components
- Systems
- Connector configurations
- Security controls
- Performance measurements
- Test results

If information cannot be verified, state:

`Unable to verify from repository evidence.`

or:

`Verification Required.`

---

## 27. Source References

Where practical, findings should identify the source location.

Examples:

- `src/main/mule/order-api.xml`
- `src/main/resources/application.yaml`
- `pom.xml`
- `mule-artifact.json`

Include flow/configuration names when available.

Do not fabricate line numbers.

---

## 28. Report Formatting

The Word document should use:

- Consistent fonts
- Professional headings
- Appropriate spacing
- Page breaks
- Header/footer
- Page numbers
- Tables
- Severity styling
- Section numbering where appropriate
- Consistent colors
- Readable charts
- Professional cover page

Avoid:

- Excessive colors
- Excessive decorative elements
- Tiny fonts
- Extremely wide tables
- Dense unformatted text
- Large unnecessary blank spaces

---

## 29. Header and Footer

Where practical, include:

Header:

`MuleSoft Architecture & Standards Review`

Footer:

- Application name
- Review date
- Page number

Do not include secrets or sensitive configuration.

---

## 30. Table of Contents

Include a table of contents when supported by the document-generation mechanism.

The table of contents should correspond to actual report headings.

Do not manually fabricate page numbers.

---

## 31. Report Validation

After generating the `.docx`, validate that:

1. The file exists.
2. The file has a `.docx` extension.
3. The file is not empty.
4. The document can be opened/read by the available validation mechanism.
5. Required major sections are present.
6. Finding counts are consistent.
7. No sensitive values were accidentally included.
8. Charts/tables are not obviously broken.
9. The output filename follows the required convention.

If validation fails, correct the report before declaring completion.

---

## 32. Output Location

The final report must be created at:

`${GITHUB_WORKSPACE}/reports/mulesoft-standards-review_<timestamp>.docx`

The timestamp must be filesystem-safe.

Do not place the final report inside:

- `code-review/`
- Temporary directories
- The MuleSoft source tree

unless required temporarily during generation.

The final artifact must be under `reports/`.

---

## 33. Final Response

After successful report creation and validation, the final response must clearly provide the absolute report location.

Use:

`Download full report: <absolute-path-to-docx>`

Do not claim successful report generation if the file does not exist.

Do not provide only the findings in the final response.

The `.docx` is the primary deliverable.

---

## 34. Artifact Compatibility

The report must be generated in a format that GitHub Actions can upload directly as an artifact.

The final file must therefore remain a normal `.docx` file and must not require manual conversion after the Claude review completes.

---

## 35. Final Quality Gate

Before completing the report, verify:

- Architecture is documented.
- Architecture diagram is included when evidence permits.
- Findings are consolidated.
- Findings have severity.
- Findings have evidence.
- Findings have impact.
- Findings have solutions.
- Security findings do not expose secrets.
- Connector review is represented.
- Configuration review is represented.
- Performance review is represented.
- Logging review is represented.
- API security review is represented.
- MUnit review is represented.
- Custom code review is represented.
- Duplication review is represented.
- Naming/maintainability review is represented.
- Remediation roadmap is included.
- Positive observations are included where appropriate.
- Finding counts are accurate.
- The Word document exists.
- The Word document has been validated.
- The final absolute path is reported.