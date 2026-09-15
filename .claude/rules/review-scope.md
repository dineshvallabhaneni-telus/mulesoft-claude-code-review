# MuleSoft Review Scope

## Purpose

Define the exact application files and directories that are included in the MuleSoft architecture and standards review.

These rules are mandatory.

---

## 1. Application Review Scope

Review the complete contents of the following:

- `pom.xml`
- `mule-artifact.json`
- `src/`

The `src/` directory must be reviewed recursively, including all applicable:

- Mule XML files
- DataWeave files
- MUnit files
- Java source
- Python source
- Properties files
- YAML files
- YML files
- JSON configuration
- Other MuleSoft application resources

Do not assume that a file is irrelevant solely because of its extension.

---

## 2. Recursive Review

The review must cover all applicable files under:

`src/**`

Do not review only the main flows.

Review:

- Nested directories
- Subflows
- Private flows
- Error handlers
- Global configurations
- MUnit tests
- Resources
- Environment configuration
- Supporting source code

---

## 3. Explicitly Excluded Directories

The following directories are outside the MuleSoft application review scope:

- `code-review/`
- `reports/`

Never treat files under these directories as application source.

### `code-review/`

This directory contains the review framework itself.

Do not analyze the following framework resources as MuleSoft application findings:

- Agents
- Skills
- Rules
- Standards
- Prompts
- Scripts
- Framework configuration
- Framework documentation

### `reports/`

This directory contains generated review artifacts.

Do not analyze generated reports as application source.

---

## 4. Files Outside the Defined Scope

Do not report findings based solely on files outside:

- `pom.xml`
- `mule-artifact.json`
- `src/`

unless the file is required to understand an in-scope implementation.

For example, if a referenced dependency or build configuration in `pom.xml` requires examining related information, inspect only what is necessary to accurately understand the in-scope implementation.

Do not expand the review indiscriminately.

---

## 5. Framework Isolation

The review framework must never be evaluated as part of the MuleSoft application.

The following are framework resources:

- `code-review/CLAUDE.md`
- `code-review/.claude/`
- `code-review/prompts/`
- `code-review/standards/`
- `code-review/config/`
- `code-review/scripts/`
- `code-review/.github/`

These must not generate MuleSoft findings.

---

## 6. Generated Output Isolation

The report output directory is:

`reports/`

Generated documents, temporary files, summaries, logs, and other review artifacts under this directory are not application source.

Do not inspect them as part of the MuleSoft review.

---

## 7. No Source Modification

The review is an analysis operation.

Do not modify MuleSoft application source files.

Do not:

- Refactor application code
- Rename application files
- Modify Mule XML
- Modify DataWeave
- Modify configuration
- Modify MUnit tests
- Modify `pom.xml`
- Modify `mule-artifact.json`

unless the task explicitly changes from review to remediation.

The expected application outcome is a review report, not source-code changes.

---

## 8. Evidence Requirement

Every finding must be supported by evidence from the in-scope application.

Do not report:

- Assumptions
- Generic best-practice statements presented as defects
- Issues that cannot be supported by repository evidence
- Findings based solely on excluded framework files

If the repository does not provide enough evidence to determine whether a control exists, report:

`Verification Required`

rather than claiming the control is missing.

---

## 9. External Configuration

Some MuleSoft capabilities may be configured outside the repository, including:

- API Manager policies
- Runtime Manager settings
- CloudHub configuration
- Deployment configuration
- Infrastructure configuration
- External secret management
- Environment variables
- Platform-level security controls

Do not claim that these controls are absent simply because they are not visible in the repository.

Instead distinguish between:

- Confirmed from repository
- Unable to verify from repository

---

## 10. Environment Configuration

When reviewing environment-specific configuration, inspect all applicable configuration files within the defined application scope.

Potential formats include:

- `.properties`
- `.yaml`
- `.yml`
- `.json`

and applicable MuleSoft configuration resources.

Environment names may include:

- DEV
- QA
- UAT
- PROD
- TEST
- SIT
- PERF
- DR

Do not assume that these exact environments exist.

First identify the environment configuration pattern actually used by the application.

---

## 11. Configuration Comparison

When comparing environments:

- Compare configuration keys.
- Compare configuration structure.
- Identify missing keys.
- Identify unexpected additional keys.
- Identify naming inconsistencies.
- Identify structural drift.
- Identify potentially incorrect environment-specific configuration.

Do not automatically report different values as defects.

For example, different database hosts between DEV, QA, UAT, and PROD are normally expected.

The review should determine whether the differences are intentional and appropriate.

---

## 12. Sensitive Information

The review may inspect sensitive configuration to determine whether it is securely implemented.

However, never reproduce sensitive values in:

- Findings
- Reports
- Console output
- `summary.txt`
- Generated documentation

Sensitive information includes:

- Passwords
- API keys
- Client secrets
- Tokens
- Private keys
- Encryption keys
- Credentials
- Sensitive connection strings

Report the existence and location of an exposure without exposing the value.

---

## 13. Review Completeness

Before completing the review, verify that the following were considered:

- `pom.xml`
- `mule-artifact.json`
- Complete `src/` tree
- Mule flows
- Subflows
- Private flows
- Global configurations
- Connectors
- DataWeave
- Error handling
- Logging
- MUnit
- Configuration/property files
- Environment configuration
- Custom code
- Security controls
- API security
- Performance characteristics
- Naming and maintainability
- Duplicate implementation

The review must not stop after examining only the primary Mule XML files.

---

## 14. Scope Boundary Summary

The authoritative application review scope is:

INCLUDE
-------
pom.xml
mule-artifact.json
src/**

EXCLUDE
-------
code-review/**
reports/**

The review must remain within this boundary unless additional information is required solely to correctly interpret an in-scope application implementation.