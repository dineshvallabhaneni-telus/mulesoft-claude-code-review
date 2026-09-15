# File: standards/naming/naming-standards.md

# MuleSoft Naming Standards

## 1. Purpose

This document defines standards for reviewing naming across MuleSoft applications.

Naming should make the application:

- Easy to understand
- Easy to maintain
- Consistent
- Searchable
- Predictable
- Easy to troubleshoot

Names should communicate intent rather than implementation trivia.

---

## 2. General Principles

Names should be:

- Clear
- Descriptive
- Consistent
- Unambiguous
- Appropriate to the scope
- Aligned with established project terminology

Avoid names that require the reviewer or developer to inspect implementation details before understanding their purpose.

---

## 3. Naming Consistency

A project should use consistent naming conventions across:

- Applications
- Flows
- Subflows
- Variables
- Attributes
- Configuration properties
- DataWeave modules
- API resources
- Error types
- MUnit tests
- Files
- Connectors

Do not introduce a different naming convention without a clear reason.

---

## 4. Application Names

Application names should clearly identify the business capability or integration purpose.

Prefer names such as:

    customer-api

    order-processing-api

    payment-integration

over ambiguous names such as:

    app1

    integration

    project-new

---

## 5. Application Name Characteristics

Application names should generally:

- Be meaningful
- Avoid unnecessary abbreviations
- Use a consistent case convention
- Follow organizational repository conventions

The exact naming format should follow the project's established deployment and repository standards.

---

## 6. Flow Names

Flow names should describe the operation performed by the flow.

Prefer:

    get-customer-flow

    create-order-flow

    process-payment-flow

over:

    flow1

    mainFlow

    process

---

## 7. Flow Naming

A flow name should make its responsibility understandable.

For API flows, names may reflect:

    HTTP method + resource + operation

For example:

    get-customer-flow

    create-customer-flow

For event-driven flows, names may reflect:

    source + business operation

For example:

    order-created-processing-flow

---

## 8. Main Flows

Main flows should have names that communicate their entry-point responsibility.

Avoid generic names such as:

    main

    start

    process

unless the project convention explicitly establishes their meaning.

---

## 9. Subflow Names

Subflows should describe reusable behavior.

Prefer:

    validate-customer-subflow

    build-error-response-subflow

    enrich-order-subflow

over:

    helper1

    common

    utility

---

## 10. Private Flow Names

Private flows should describe the processing responsibility they encapsulate.

Examples:

    lookup-customer

    transform-order-response

    publish-order-event

Avoid names that merely describe their technical mechanism.

---

## 11. Flow Naming and Responsibility

A flow should generally have one understandable responsibility.

If a flow name says:

    process-order

but the flow also performs customer provisioning, payment settlement, notification, and reporting, the name may be too broad.

Consider whether the flow itself has excessive responsibility.

---

## 12. Variables

Variables should have descriptive names.

Prefer:

    customerId

    orderStatus

    paymentResponse

over:

    x

    data

    temp

    value

---

## 13. Variable Naming Convention

Use the project's established variable naming convention consistently.

If camelCase is established, use:

    customerId

    orderDetails

    downstreamResponse

rather than mixing:

    customer_id

    CustomerID

    customer-id

---

## 14. Boolean Variables

Boolean variables should communicate true/false meaning.

Prefer:

    isActive

    hasPermission

    isCustomerValid

    shouldRetry

over:

    active

    permission

    valid

when the boolean meaning could otherwise be ambiguous.

---

## 15. Collection Variables

Collection names should indicate that they contain multiple values.

Prefer:

    customers

    orders

    failedRecords

over:

    customer

    order

when the variable represents a collection.

---

## 16. Singular vs Plural

Use singular names for individual objects and plural names for collections.

Examples:

    customer

    customers

    order

    orders

    error

    errors

---

## 17. Generic Variable Names

Avoid unnecessarily generic names such as:

    data

    result

    response

    object

    item

    temp

when a more meaningful name is available.

Generic names may be acceptable when their scope is extremely small and their meaning is obvious.

---

## 18. Payload Variables

Avoid unnecessary variables named:

    payload

when the variable represents a specific business object.

Prefer:

    customerPayload

    orderRequest

    paymentResponse

when the additional context improves readability.

Do not rename Mule's actual `payload` merely to satisfy a naming preference when no meaningful distinction exists.

---

## 19. Attributes

Attribute-related variables should clearly identify what they represent.

Examples:

    httpStatus

    requestHeaders

    queryParameters

Avoid vague names such as:

    attrs

unless the project convention explicitly uses the abbreviation and the context is clear.

---

## 20. Configuration Properties

Configuration properties should have meaningful names.

Prefer:

    customer.api.baseUrl

    database.connection.timeout

    retry.maxAttempts

over:

    url1

    timeout1

    value

---

## 21. Configuration Naming Hierarchy

Configuration properties should follow a predictable hierarchy.

For example:

    <domain>.<component>.<property>

or the organization's established convention.

Related properties should use related prefixes.

---

## 22. Secrets

Secret property names should clearly indicate their purpose without embedding the actual secret.

Examples:

    client.id

    client.secret

    database.password

The actual secret must not appear in source-controlled configuration.

---

## 23. Environment-Specific Properties

Environment-specific configuration should use a consistent naming model.

Avoid creating inconsistent names such as:

    dev.url

    testEndpoint

    prod_service_url

when a standardized configuration hierarchy is available.

---

## 24. Connector Configuration Names

Named connector configurations should describe their target or purpose.

Prefer:

    customerHttpRequestConfig

    orderDatabaseConfig

    paymentSftpConfig

over:

    httpConfig1

    dbConfig

    config2

---

## 25. Global Elements

Global elements should have names that identify their role.

Examples:

    customerHttpConfig

    primaryDatabaseConfig

    orderQueueConfig

Avoid meaningless generated names where maintainable names can be provided.

---

## 26. HTTP Listener Names

HTTP listener configurations should communicate their role.

Examples:

    apiHttpListener

    customerApiListener

    internalApiListener

---

## 27. HTTP Request Configuration Names

HTTP request configurations should identify the target system.

Examples:

    customerSystemHttpConfig

    paymentProviderHttpConfig

    inventoryApiHttpConfig

Avoid:

    httpConfig

when multiple downstream systems exist.

---

## 28. Database Configuration Names

Database configurations should identify their purpose or system.

Examples:

    customerDatabaseConfig

    reportingDatabaseConfig

    ordersDatabaseConfig

---

## 29. Messaging Configuration Names

Messaging configurations should identify the messaging system or business domain.

Examples:

    orderQueueConfig

    customerEventsConfig

    integrationMessagingConfig

---

## 30. Error Types

Custom error types should have meaningful names.

They should communicate the business or technical failure.

Examples:

    CUSTOMER:NOT_FOUND

    ORDER:INVALID_STATE

    PAYMENT:DECLINED

Avoid generic custom errors such as:

    APP:ERROR

    CUSTOM:FAILURE

when a more precise classification is possible.

---

## 31. Error Type Naming

Custom error types should follow a consistent namespace and identifier convention.

For example:

    DOMAIN:ERROR_NAME

The exact convention should align with the project's Mule error taxonomy.

---

## 32. Error Identifiers

Error identifiers should describe the condition, not the implementation.

Prefer:

    CUSTOMER:NOT_FOUND

over:

    CUSTOMER:DB_SELECT_FAILED

when the external meaning is that the customer does not exist.

---

## 33. API Resource Names

API resources should follow the API specification and use consistent terminology.

Prefer resource-oriented names such as:

    /customers

    /orders

    /payments

Avoid inconsistent singular/plural forms.

---

## 34. API Path Naming

API paths should use a consistent convention for:

- Case
- Pluralization
- Nested resources
- Path parameters

Do not mix styles without a documented reason.

---

## 35. Path Parameters

Path parameter names should clearly identify the resource.

Prefer:

    /customers/{customerId}

    /orders/{orderId}

over:

    /customers/{id}

when the broader API contains multiple resource types and explicit naming improves clarity.

---

## 36. Query Parameters

Query parameter names should be descriptive and consistent.

Examples:

    customerId

    pageSize

    pageNumber

    sortBy

Avoid ambiguous names such as:

    x

    val

    type1

---

## 37. HTTP Methods

HTTP method choice should follow the API contract and standard semantics.

Do not encode the HTTP method into the resource path unnecessarily.

Avoid patterns such as:

    /getCustomer

    /createOrder

when RESTful resource semantics are required by the API design.

---

## 38. DataWeave Module Names

DataWeave modules should have descriptive names.

Examples:

    CustomerTransform.dwl

    ErrorResponse.dwl

    OrderMapping.dwl

Avoid:

    util.dwl

    helper.dwl

    common.dwl

unless their purpose is genuinely broad and established.

---

## 39. DataWeave Function Names

Functions should describe what they return or perform.

Prefer:

    mapCustomerResponse

    buildErrorResponse

    normalizeCustomerName

over:

    process

    handle

    convert

when the more specific intent is known.

---

## 40. DataWeave Variable Names

DataWeave variables should use meaningful names.

Avoid:

    x

    y

    z

    temp

unless the variable is extremely local and obvious.

---

## 41. DataWeave Naming Consistency

Use the same business terminology in DataWeave as in the rest of the application.

If the application consistently uses:

    customerId

do not introduce:

    clientIdentifier

for the same concept without a clear semantic distinction.

---

## 42. XML File Names

Mule configuration XML files should communicate their purpose.

Examples:

    customer-api.xml

    order-processing.xml

    global-config.xml

Avoid meaningless filenames such as:

    new.xml

    test.xml

    config2.xml

---

## 43. XML Configuration Separation

When configuration is separated into multiple files, filenames should indicate their responsibility.

For example:

    global-config.xml

    error-handling.xml

    customer-api.xml

    order-processing.xml

---

## 44. MUnit Test Names

MUnit test names should describe expected behavior.

Prefer:

    shouldReturnCustomerWhenCustomerExists

over:

    testCustomerFlow

---

## 45. MUnit Test Suite Names

Test suites should identify the functionality being tested.

Examples:

    customer-api-test-suite

    order-processing-test-suite

Avoid generic:

    test-suite

---

## 46. Test Resources

Test fixture names should communicate the scenario.

Examples:

    customer-valid.json

    customer-missing-id.json

    downstream-timeout.json

Avoid:

    test1.json

    sample.json

    data.json

when the scenario can be made explicit.

---

## 47. Naming and Business Terminology

Use terminology consistent with:

- API specifications
- Business requirements
- Domain models
- Database terminology
- Event schemas

Do not use multiple names for the same concept without a documented distinction.

---

## 48. Abbreviations

Avoid unnecessary abbreviations.

Prefer:

    customer

    transaction

    configuration

over:

    cust

    txn

    cfg

unless the abbreviation is an established organizational standard.

---

## 49. Common Technical Abbreviations

Common and universally understood abbreviations may be acceptable where the project convention supports them.

Examples may include:

    API

    HTTP

    URL

    ID

Use them consistently.

---

## 50. Acronym Capitalization

Acronym formatting should be consistent.

For example, do not mix:

    customerID

    customerId

    customerid

unless different conventions are intentionally defined.

Choose the project standard and apply it consistently.

---

## 51. Naming Length

Names should be descriptive without becoming unnecessarily verbose.

Prefer:

    paymentProviderResponse

over:

    response

but avoid excessively long names that make expressions difficult to read.

---

## 52. Temporary Names

Temporary variables should still communicate their purpose.

Avoid:

    temp1

    temp2

    tempData

Prefer:

    normalizedCustomer

    filteredOrders

    retryResponse

when those names accurately describe the value.

---

## 53. Constants

Constants should clearly communicate their meaning.

Examples:

    DEFAULT_TIMEOUT

    MAX_RETRY_ATTEMPTS

    DEFAULT_PAGE_SIZE

Follow the project's established constant naming convention.

---

## 54. Magic Values

When a repeated value has business or technical meaning, give it a descriptive name where appropriate.

For example:

    MAX_RETRY_ATTEMPTS

is clearer than repeatedly using:

    3

However, do not create constants for trivial one-off values merely to eliminate literals.

---

## 55. Event Names

Event names should clearly describe the business event.

Prefer:

    CustomerCreated

    OrderSubmitted

    PaymentCompleted

over:

    CustomerEvent

    OrderEvent

    Event1

---

## 56. Queue and Topic Names

Messaging destinations should follow a predictable naming convention.

Examples:

    orders.created

    payments.completed

    customers.updated

The exact convention should follow organizational messaging standards.

---

## 57. Scheduler Names

Schedulers should identify the business process being scheduled.

Prefer:

    nightly-order-reconciliation

    customer-cache-refresh

over:

    scheduler1

    nightly-job

---

## 58. Object Store Names

Object Store keys and stores should use meaningful names.

Examples:

    customer-session-store

    order-idempotency-store

Avoid generic names where multiple stores exist.

---

## 59. Secure Property Names

Secure properties should retain meaningful names while avoiding exposure of actual secret values.

Examples:

    secure::database.password

    secure::api.client.secret

The naming scheme must remain consistent with the application's secure-property mechanism.

---

## 60. Naming and Scope

Names should make scope clear.

A variable with flow-local meaning should not be named as though it were a global application concept.

Similarly, a global configuration should not have a name that implies it belongs to one small flow unless that is intentional.

---

## 61. Naming and Reuse

Reusable components should have names that describe their reusable capability.

Avoid names tied to one caller when the component is intentionally shared.

For example:

    buildStandardErrorResponse

may be preferable to:

    buildCustomerFlowError

if the same component is used across multiple domains.

---

## 62. Naming and Duplication

If two components have nearly identical names, determine whether:

- They represent different concepts.
- The names are too generic.
- The components are duplicates.
- One should be reused.

Naming collisions often indicate architectural ambiguity.

---

## 63. Naming and Security

Names themselves should not expose secrets.

Do not include:

- Passwords
- API keys
- Tokens
- Secret values

in flow names, variable names, filenames, or configuration identifiers.

---

## 64. Naming and Sensitive Data

Avoid names that accidentally imply storing sensitive information in logs or variables when the data should be minimized.

For example, a variable named:

    fullCustomerCreditCardData

should trigger review of both naming and data-handling design.

---

## 65. Naming and Observability

Important operational names should be easy to identify in logs and monitoring.

Flow names, operation names, and error types should help operators determine what failed.

---

## 66. Naming and Error Handling

Error names should make the failure condition understandable.

Avoid generic errors such as:

    PROCESSING_ERROR

when the application can distinguish:

    CUSTOMER:NOT_FOUND

    PAYMENT:TIMEOUT

    ORDER:INVALID_STATE

---

## 67. Naming and API Consistency

API terminology should remain consistent across:

- RAML/OAS
- Flow names
- Variables
- DataWeave
- Error codes
- Documentation
- Tests

A resource called `customers` in the API should not unexpectedly become `clients` in implementation unless the distinction is intentional.

---

## 68. Naming and Connector Configuration

Connector configuration names should make it clear which external system is being used.

This becomes especially important when an application integrates with multiple systems using the same connector type.

---

## 69. Naming and Multiple Environments

Environment names should be consistent.

For example:

    dev
    test
    qa
    prod

or the organization's established naming scheme.

Do not mix:

    development

    DEV

    dev-env

unless the distinction is intentional.

---

## 70. Naming and Versioning

Version identifiers should follow the API and deployment strategy.

Avoid inconsistent forms such as:

    v1

    V2

    version3

unless required by an external contract.

---

## 71. Naming and Deprecated Components

Deprecated components should be clearly identifiable where the project requires it.

Do not silently leave obsolete names that suggest a component is still the preferred implementation.

---

## 72. Naming Quality Smells

Potential naming problems include:

- `flow1`
- `subflow1`
- `temp`
- `data`
- `value`
- `process`
- `helper`
- `common`
- `util`
- `config1`
- `test1`
- Inconsistent capitalization
- Inconsistent pluralization
- Excessive abbreviations
- Multiple names for the same business concept
- Names that expose sensitive information

These are review signals, not automatic defects.

---

## 73. Naming Severity

Do not report every naming inconsistency as a defect.

Consider severity based on impact.

### High

Use high severity only when naming causes or contributes to a serious issue such as:

- Security exposure
- Incorrect configuration
- Ambiguous resource resolution
- Dangerous operational misunderstanding

### Medium

Examples:

- Significant inconsistency across a major component
- Naming that materially impairs maintainability
- Ambiguous names in critical integration logic

### Low

Examples:

- Minor naming inconsistency
- Non-standard abbreviation
- Slightly unclear variable name

---

## 74. Naming Review Checklist

Before completing the naming review, confirm:

- Application names are meaningful.
- Flow names describe responsibilities.
- Subflow names describe reusable behavior.
- Private flows have meaningful names.
- Variables are descriptive.
- Boolean variables communicate boolean meaning.
- Collections use appropriate pluralization.
- Configuration properties follow a consistent hierarchy.
- Connector configurations identify their target or purpose.
- Global elements have meaningful names.
- Custom error types are specific.
- API resources follow consistent terminology.
- Path parameters are clear.
- Query parameters are descriptive.
- DataWeave modules have meaningful names.
- DataWeave functions describe their behavior.
- XML files have meaningful names.
- MUnit tests describe expected behavior.
- Test fixtures identify their scenarios.
- Business terminology is consistent.
- Abbreviations are controlled.
- Acronym capitalization is consistent.
- Temporary variables are still meaningful.
- Constants communicate their purpose.
- Event names describe business events.
- Queue and topic names follow project conventions.
- Scheduler names identify their jobs.
- Object Store names identify their purpose.
- Naming does not expose secrets.
- Naming does not create unnecessary ambiguity.
- Names support operational troubleshooting.
- Deprecated components are identifiable where required.

---

## 75. Naming Quality Gate

The reviewer must be able to answer the following questions:

1. Can a developer understand the purpose of a component from its name?
2. Are naming conventions consistent throughout the application?
3. Are business terms used consistently?
4. Can operators identify important flows and operations from logs and monitoring?
5. Are variables specific enough to avoid ambiguity?
6. Are configuration and connector names clear?
7. Are error types meaningful and specific?
8. Are API resource and parameter names consistent?
9. Are tests and test fixtures easy to identify?
10. Are abbreviations used only where justified?
11. Are names free from sensitive information?
12. Do names reveal any architectural ambiguity or duplicated concepts?

### Final Question

> Can a developer or operator understand what each important component represents without opening its implementation, and does the naming remain consistent with the application's business terminology and technical conventions?