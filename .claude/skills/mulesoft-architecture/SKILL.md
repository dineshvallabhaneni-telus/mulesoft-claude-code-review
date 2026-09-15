# MuleSoft Architecture Analysis Skill

## Purpose

Analyze the complete MuleSoft application architecture and provide an evidence-based assessment suitable for a Senior MuleSoft Architect or Enterprise Integration Architect.

The objective is NOT to force the application into a preferred architecture.

The objective is to determine:

- What architecture is actually implemented.
- How the application components interact.
- Whether the architecture is appropriate for the use case.
- Architectural strengths.
- Architectural weaknesses.
- Coupling concerns.
- Scalability concerns.
- Reliability concerns.
- Maintainability concerns.
- Reusability opportunities.
- Performance implications.
- Security implications.
- Recommended architectural improvements.

Every significant architectural problem MUST include a practical solution.

---

# 1. Repository Scope

The MuleSoft application repository is:

${GITHUB_WORKSPACE}

The review framework is:

${GITHUB_WORKSPACE}/code-review

The report directory is:

${GITHUB_WORKSPACE}/reports

Review the complete MuleSoft application available under:

${GITHUB_WORKSPACE}

---

# 2. Exclusions

The following directories MUST NOT be treated as MuleSoft application source:

${GITHUB_WORKSPACE}/code-review/**
${GITHUB_WORKSPACE}/reports/**

Do not report findings against:

- Review agents
- Review skills
- Prompts
- Framework scripts
- Generated reports

---

# 3. Architecture Evidence

Use repository evidence from:

- pom.xml
- mule-artifact.json
- src/main/mule/**
- src/main/resources/**
- src/test/**
- RAML files
- OAS files
- API specifications
- DataWeave
- Connector configurations
- Global configurations
- Properties
- YAML/YML
- Java/custom code
- Python/custom code
- MUnit
- Flow/subflow structure

Do not infer architecture solely from folder names.

---

# 4. Architecture Identification

Determine which architecture style or combination of styles is actually implemented.

Possible architecture patterns include:

- API-led connectivity
- Experience API
- Process API
- System API
- Layered integration
- Point-to-point integration
- Event-driven architecture
- Request/response integration
- Batch processing
- Scheduled processing
- Messaging-based integration
- File-based integration
- Hybrid architecture

An application may legitimately use multiple patterns.

Document the observed architecture rather than forcing a single classification.

---

# 5. API-Led Assessment

If API-led architecture is used, determine whether the implementation reasonably follows:

- Experience layer
- Process layer
- System layer

Identify:

- Experience APIs
- Process APIs
- System APIs
- Reusable services
- Direct system integrations
- API-to-API calls

Report meaningful violations only.

Do not report a missing API layer simply because the application does not require one.

---

# 6. Point-to-Point Integration Assessment

Identify direct integrations such as:

Mule flow → External system

Evaluate whether point-to-point integration is:

- Appropriate.
- Excessive.
- Duplicated.
- Difficult to maintain.
- Creating unnecessary coupling.

If excessive point-to-point coupling exists, recommend an appropriate architectural alternative.

Do not automatically classify point-to-point integration as a defect.

---

# 7. Integration Inventory

Build an internal inventory of major integration components.

Where applicable identify:

| Component | Type | Direction | External System | Protocol | Purpose |
|---|---|---|---|---|---|

Possible protocols:

- HTTP
- HTTPS
- REST
- SOAP
- Database
- JMS
- AMQP
- SFTP
- FTP
- File
- Kafka
- Salesforce
- SAP
- Other MuleSoft-supported connectors

Only report protocols supported by repository evidence.

---

# 8. Application Entry Points

Identify application entry points such as:

- HTTP Listener
- Scheduler
- Batch
- Message Listener
- File Listener
- VM
- JMS
- Queue
- APIkit
- Other event sources

For each major entry point determine:

- Purpose.
- Flow invoked.
- Downstream processing.
- Error handling.
- Security considerations.

---

# 9. Flow Architecture

Analyze major flows and determine:

- Entry point.
- Processing stages.
- Transformations.
- Variables.
- Connector calls.
- Error handling.
- Subflow usage.
- External dependencies.

Identify excessively large or complex flows.

Do not classify a flow as complex solely because it contains many processors.

Consider:

- Branching.
- Nesting.
- Repeated logic.
- Mixed responsibilities.
- Excessive transformations.
- Excessive connector calls.
- Error handling complexity.

---

# 10. Separation of Responsibilities

Evaluate whether flows have clear responsibilities.

Look for inappropriate mixing of:

- API handling
- Business logic
- Transformation
- Database operations
- External service calls
- Logging
- Error handling
- Security processing

If responsibilities are unnecessarily mixed, recommend practical refactoring.

---

# 11. Reusability

Identify reusable components such as:

- Subflows
- Private flows
- Global configurations
- Common error handlers
- Common transformations
- Shared DataWeave modules
- Reusable connector configurations

Identify meaningful duplication.

Do not recommend abstraction merely for the sake of abstraction.

---

# 12. Coupling Assessment

Evaluate coupling between:

- APIs
- Flows
- Subflows
- External systems
- Databases
- Messaging systems
- Configuration
- Shared variables

Look for:

- Hard-coded dependencies.
- Excessive direct dependencies.
- Shared mutable state.
- Tight coupling to external systems.
- Duplicate integrations.

Explain the impact and solution.

---

# 13. Cohesion Assessment

Determine whether each major component has a clear responsibility.

Potential problems include:

- One flow performing unrelated business functions.
- Generic utility flows containing business logic.
- Shared subflows containing unrelated functionality.
- Large flows responsible for multiple domains.

Recommend decomposition only where it materially improves maintainability.

---

# 14. Domain Boundary Assessment

Where business domains can be inferred, identify them.

Examples:

- Customer
- Order
- Payment
- Product
- Inventory
- Employee
- Claims

Evaluate whether unrelated domains are unnecessarily coupled.

Do not invent business domains when they cannot be established.

---

# 15. External System Dependency Assessment

Identify important external systems.

Examples:

- CRM
- ERP
- Database
- Payment gateway
- SaaS
- File system
- Messaging platform
- External APIs

For each major dependency consider:

- Coupling.
- Timeout.
- Retry.
- Error handling.
- Security.
- Availability.
- Performance.

Do not report connector-level configuration issues here if they are already covered by the connector-analysis skill unless there is an architectural implication.

---

# 16. Synchronous vs Asynchronous Architecture

Identify synchronous and asynchronous processing.

Evaluate whether the communication model is appropriate.

Consider:

- User-facing latency.
- Long-running processes.
- Downstream availability.
- Retry requirements.
- Message durability.
- Eventual consistency.
- Failure isolation.

Do not recommend asynchronous processing merely because it is theoretically scalable.

---

# 17. Event-Driven Architecture

If messaging or event-driven processing exists, assess:

- Event producers.
- Event consumers.
- Queue/topic usage.
- Message boundaries.
- Retry.
- Error handling.
- Idempotency.
- Duplicate message handling.
- Dead-letter/error handling where visible.

If infrastructure-level settings cannot be inspected, mark them:

Verification Required

---

# 18. Scheduler and Batch Architecture

If schedulers or batch jobs exist, evaluate:

- Scheduling frequency.
- Processing volume.
- Batch boundaries.
- Parallelism.
- Retry behavior.
- Failure recovery.
- Idempotency.
- Overlapping execution.
- Downstream load.

Do not report scheduling frequency as a problem unless there is evidence of risk.

---

# 19. API Layer Architecture

Where API endpoints exist, assess:

- Resource organization.
- Separation between API layer and implementation.
- Reusability.
- API-to-flow mapping.
- Error handling.
- Transformation responsibilities.
- Security boundaries.

Do not duplicate detailed API security findings from the API security skill.

Only report architectural implications here.

---

# 20. Transformation Architecture

Evaluate where DataWeave transformations occur.

Look for:

- Repeated transformations.
- Large transformation blocks.
- Business logic hidden inside transformations.
- Duplicate mappings.
- Excessive transformation of unchanged payloads.
- Poor separation of transformation and orchestration.

Recommend reusable DataWeave modules where appropriate.

Do not report minor DataWeave style issues here.

---

# 21. Data Flow Assessment

Determine the major data path through the application.

For example:

Client
→ API
→ Mule Flow
→ Validation
→ Transformation
→ Database
→ External API
→ Response

Document important paths in the architecture report.

Do not include every processor.

---

# 22. Dependency Chain Assessment

Identify important chains such as:

API
→ Flow
→ Database
→ External API
→ Another service

Evaluate:

- Number of synchronous dependencies.
- Failure propagation.
- Latency accumulation.
- Retry amplification.
- Availability dependency.

Highlight architectural risks when multiple dependencies create a fragile chain.

---

# 23. Resilience Architecture

Evaluate architectural resilience where repository evidence permits.

Consider:

- Timeout strategy.
- Retry strategy.
- Error isolation.
- Circuit breaker availability where applicable.
- Asynchronous decoupling.
- Idempotency.
- Failure recovery.

Detailed connector timeout/retry findings belong to connector-analysis.

Architectural review should focus on systemic implications.

---

# 24. Scalability Architecture

Evaluate potential scaling constraints.

Consider:

- Stateful processing.
- Shared state.
- Large payloads.
- Sequential processing.
- Synchronous dependency chains.
- In-memory processing.
- Batch design.
- Connection limitations.
- External system bottlenecks.

Only report scalability concerns supported by implementation evidence.

---

# 25. Availability Architecture

Identify potential single points of failure.

Consider:

- Critical external dependencies.
- Centralized processing.
- Shared resources.
- Synchronous dependency chains.
- Missing fallback mechanisms.

Do not claim infrastructure-level high availability is absent unless infrastructure configuration is available.

---

# 26. Security Architecture

At architecture level, consider:

- Security boundaries.
- API entry points.
- External integrations.
- Credential handling.
- Trust boundaries.
- Sensitive data movement.
- TLS requirements.

Detailed credential and API-policy checks belong to security-analysis and api-security-analysis.

Do not duplicate those findings unnecessarily.

---

# 27. Configuration Architecture

Evaluate how configuration is separated from application logic.

Consider:

- Environment-specific configuration.
- Secure properties.
- Hard-coded endpoints.
- Hard-coded credentials.
- Reusable global configuration.

Detailed property analysis belongs to configuration-analysis.

Only report architectural implications here.

---

# 28. Error Architecture

Evaluate whether error handling has a coherent architecture.

Look for:

- Standardized error responses.
- Common error handling.
- Domain-specific errors.
- Connector errors.
- API errors.
- Retryable vs non-retryable errors.

Do not assume all errors should be handled globally.

---

# 29. Observability Architecture

At architecture level consider:

- Correlation ID propagation.
- End-to-end traceability.
- Consistent logging strategy.
- Error visibility.

Detailed logger-level review belongs to logging-analysis.

---

# 30. Custom Code Architecture

Evaluate the architectural role of custom Java/Python code.

Determine whether custom code:

- Represents unavoidable domain logic.
- Provides functionality unavailable natively.
- Creates unnecessary platform dependency.
- Could be replaced by MuleSoft capabilities.

Do not report custom code merely because it exists.

---

# 31. Dependency Architecture

Review pom.xml for architectural dependencies.

Consider:

- Mule runtime version.
- Mule Maven plugin.
- Connector versions.
- Third-party libraries.
- Custom libraries.
- Duplicate dependencies.
- Unnecessary dependencies.

Detailed code/dependency quality may also be handled by mule-code-quality.

Only report architectural implications here.

---

# 32. Reuse Across Applications

Where evidence exists within the repository, identify reusable components.

Potential examples:

- Shared libraries.
- Common modules.
- Common DataWeave functions.
- Reusable APIs.
- Shared connector configurations.

Do not recommend extracting components merely because they are used twice.

---

# 33. Anti-Pattern Detection

Look for meaningful MuleSoft architectural anti-patterns.

Examples:

- Giant monolithic flow.
- Excessive point-to-point integrations.
- Hard-coded environment dependencies.
- Business logic spread across unrelated flows.
- Excessive shared mutable variables.
- Duplicate system integrations.
- Tight synchronous dependency chains.
- Unnecessary custom code.
- Repeated transformation logic.
- Inconsistent error architecture.

Only report anti-patterns when evidence supports them.

---

# 34. Architecture Strengths

Identify meaningful strengths.

Examples:

- Clear separation of concerns.
- Reusable subflows.
- Appropriate API-led architecture.
- Strong system abstraction.
- Good asynchronous decoupling.
- Effective error architecture.
- Good configuration separation.
- Good connector reuse.
- Appropriate batch design.

The final report must be balanced.

---

# 35. Architecture Findings

Architecture findings MUST contain:

- Finding ID
- Title
- Severity
- Location
- Evidence
- Architectural impact
- Recommendation
- Practical solution
- Priority

---

# 36. Severity Guidelines

Architecture findings should generally use:

Critical:
Major architectural risk causing severe production/security impact.

High:
Significant architectural problem affecting reliability, scalability, security, or maintainability.

Medium:
Meaningful architecture improvement.

Low:
Minor architecture improvement.

Warning:
Architecture aspect requiring external verification.

Do not inflate severity.

---

# 37. Architecture Scoring

If an architecture score is required, consider:

- Modularity
- Coupling
- Cohesion
- Reusability
- Scalability
- Reliability
- Maintainability
- Integration design

Do not score based only on number of findings.

Explain significant score drivers.

---

# 38. Architecture Diagram Data

Produce structured information that can be consumed by the Word report generator.

Where possible provide:

## Components

- Name
- Type
- Purpose

## Relationships

- Source
- Target
- Interaction
- Protocol

Example:

Component:
Customer API

Type:
Experience API

Relationship:
Customer API → Customer Process Flow

Interaction:
HTTP request

Do not invent missing relationships.

---

# 39. Architecture Summary

Produce a concise summary containing:

### Architecture Style

What architecture is implemented.

### Main Components

Major components.

### Integration Pattern

How systems communicate.

### Strengths

Important positive characteristics.

### Risks

Important architectural concerns.

### Recommendations

Prioritized improvements.

---

# 40. No Duplicate Reporting

Do not duplicate detailed findings belonging to:

- connector-analysis
- api-security-analysis
- security-analysis
- performance-analysis
- logging-analysis
- configuration-analysis
- munit-analysis
- mule-code-quality
- duplication-analysis

When another skill owns the detailed issue, record only the architectural implication if necessary.

The final report should consolidate related findings.

---

# 41. No Unsupported Claims

Never claim:

- A system is unavailable.
- An API is insecure.
- A policy is missing.
- Infrastructure is not highly available.
- CloudHub is incorrectly configured.

unless the repository contains evidence.

Use:

Verification Required

when the repository cannot establish the fact.

---

# 42. Final Output

Return structured architecture analysis for consumption by the final report generation process.

Include:

## Architecture Summary

## Architecture Style

## Major Components

## Major Integration Relationships

## Architecture Strengths

## Architecture Findings

## Scalability Considerations

## Reliability Considerations

## Reusability Opportunities

## Architectural Recommendations

## Verification Required

## Architecture Score

Do not generate the final `.docx` from this skill.

The `word-report-generation` skill is responsible for the final Word document.

---

# 43. Quality Standard

Before completing this skill, ask:

"Would a Senior MuleSoft Architect consider this a meaningful architecture review?"

If the answer is no:

- Remove trivial observations.
- Improve evidence.
- Strengthen architectural reasoning.
- Add practical solutions.
- Avoid generic best-practice statements.

The objective is architectural insight, not maximum finding count.