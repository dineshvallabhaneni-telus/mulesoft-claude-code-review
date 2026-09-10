#!/usr/bin/env python3

"""
Validate and reconcile the structured MuleSoft code review.

Execution model:

    APPLICATION_ROOT = MuleSoft application repository (read-only)
    FRAMEWORK_ROOT   = mulesoft-claude-code-review repository (writable)

Input:
    $FRAMEWORK_ROOT/workspace/execution/review.json

Output:
    $FRAMEWORK_ROOT/workspace/execution/validated-review.json

This script validates Claude's structured review but does not perform
technical code-review judgments itself.
"""

import json
import os
import re
import sys
from collections import Counter
from pathlib import Path


# ---------------------------------------------------------------------------
# ROOTS
# ---------------------------------------------------------------------------

def resolve_root(name: str, default: Path) -> Path:
    value = os.environ.get(name)

    if value:
        return Path(value).expanduser().resolve()

    return default.resolve()


SCRIPT_DIR = Path(__file__).resolve().parent
FRAMEWORK_ROOT = resolve_root(
    "FRAMEWORK_ROOT",
    SCRIPT_DIR.parent,
)

APPLICATION_ROOT = resolve_root(
    "APPLICATION_ROOT",
    Path.cwd(),
)

EXECUTION = FRAMEWORK_ROOT / "workspace" / "execution"

INPUT = EXECUTION / "review.json"
OUTPUT = EXECUTION / "validated-review.json"


# ---------------------------------------------------------------------------
# ALLOWED VALUES
# ---------------------------------------------------------------------------

ALLOWED_SEVERITIES = {
    "CRITICAL",
    "HIGH",
    "MEDIUM",
    "LOW",
    "NIT",
}

ALLOWED_CONFIDENCE = {
    "HIGH",
    "MEDIUM",
    "LOW",
}

ALLOWED_RECOMMENDATIONS = {
    "HIGH RISK",
    "CHANGES REQUIRED",
    "APPROVE WITH MINOR CHANGES",
    "APPROVE",
}

ALLOWED_RISKS = {
    "CRITICAL",
    "HIGH",
    "MEDIUM",
    "LOW",
}

ALLOWED_CATEGORIES = {
    "Architecture",
    "Application Structure",
    "Mule XML",
    "Data Transformation",
    "DataWeave",
    "Error Handling",
    "Security",
    "API",
    "API Design",
    "Connectors",
    "Database",
    "Messaging",
    "Performance",
    "Logging",
    "Logging and Observability",
    "Testing",
    "MUnit",
    "Build and Dependency Management",
    "Maven",
    "Configuration",
    "Maintainability",
    "Production Readiness",
    "Other",
}

REQUIRED_FINDING_FIELDS = {
    "id",
    "severity",
    "category",
    "title",
    "location",
    "confidence",
    "problem",
    "evidence",
    "impact",
    "recommendation",
}

OPTIONAL_FINDING_FIELDS = {
    "file",
    "evidenceExcerpt",
    "evidenceContext",
    "references",
}

# Approved finding-ID families from the finalized review references.
FINDING_ID_PATTERNS = [
    r"^ARCH-\d{3}$",
    r"^XML-\d{3}$",
    r"^DW-\d{3}$",
    r"^ERR-\d{3}$",
    r"^SEC-\d{3}$",
    r"^API-\d{3}$",
    r"^LOG-\d{3}$",
    r"^CON-\d{3}$",
    r"^DB-\d{3}$",
    r"^MSG-\d{3}$",
    r"^PERF-\d{3}$",
    r"^MUNIT-\d{3}$",
    r"^MAVEN-\d{3}$",
    r"^CFG-\d{3}$",
]

CATEGORY_PREFIXES = {
    "ARCH": {
        "Architecture",
        "Application Structure",
    },
    "XML": {
        "Mule XML",
    },
    "DW": {
        "Data Transformation",
        "DataWeave",
    },
    "ERR": {
        "Error Handling",
    },
    "SEC": {
        "Security",
    },
    "API": {
        "API",
        "API Design",
    },
    "LOG": {
        "Logging",
        "Logging and Observability",
    },
    "CON": {
        "Connectors",
    },
    "DB": {
        "Database",
    },
    "MSG": {
        "Messaging",
    },
    "PERF": {
        "Performance",
    },
    "MUNIT": {
        "Testing",
        "MUnit",
    },
    "MAVEN": {
        "Build and Dependency Management",
        "Maven",
    },
    "CFG": {
        "Configuration",
    },
}


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def fail(message: str) -> None:
    print(f"VALIDATION FAILED: {message}", file=sys.stderr)
    sys.exit(1)


def warn(message: str) -> None:
    print(f"VALIDATION WARNING: {message}")


def require_mapping(value, name: str) -> dict:
    if not isinstance(value, dict):
        fail(f"{name} must be an object")

    return value


def require_string(
    value,
    field_name: str,
    finding_id: str,
    allow_empty: bool = False,
) -> None:
    if not isinstance(value, str):
        fail(
            f"{finding_id}: {field_name} must be a string"
        )

    if not allow_empty and not value.strip():
        fail(
            f"{finding_id}: {field_name} must not be empty"
        )


def validate_finding_id(finding_id: str) -> None:
    if not isinstance(finding_id, str):
        fail("Finding ID must be a string")

    if not any(
        re.match(pattern, finding_id)
        for pattern in FINDING_ID_PATTERNS
    ):
        fail(
            f"Invalid finding ID: {finding_id}. "
            "Finding IDs must use an approved reference format."
        )


def finding_prefix(finding_id: str) -> str:
    return finding_id.split("-", 1)[0]


def normalize_text(value) -> str:
    if value is None:
        return ""

    if isinstance(value, str):
        return re.sub(
            r"\s+",
            " ",
            value.strip().lower(),
        )

    return re.sub(
        r"\s+",
        " ",
        str(value).strip().lower(),
    )


def finding_signature(finding: dict) -> tuple:
    """
    Used to detect likely duplicate findings.

    The signature intentionally excludes evidence location because
    multiple occurrences may represent the same root cause.
    """

    return (
        normalize_text(finding.get("category")),
        normalize_text(finding.get("title")),
        normalize_text(finding.get("problem")),
        normalize_text(finding.get("recommendation")),
    )


def minimum_verdict(findings: list) -> tuple:
    severities = {
        finding.get("severity")
        for finding in findings
    }

    if "CRITICAL" in severities:
        return "CRITICAL", "HIGH RISK"

    if "HIGH" in severities:
        return "HIGH", "CHANGES REQUIRED"

    if "MEDIUM" in severities:
        return "MEDIUM", "CHANGES REQUIRED"

    if "LOW" in severities or "NIT" in severities:
        return "LOW", "APPROVE WITH MINOR CHANGES"

    return "LOW", "APPROVE"


def risk_rank(risk: str) -> int:
    return {
        "LOW": 0,
        "MEDIUM": 1,
        "HIGH": 2,
        "CRITICAL": 3,
    }.get(risk, -1)


def recommendation_rank(recommendation: str) -> int:
    return {
        "APPROVE": 0,
        "APPROVE WITH MINOR CHANGES": 1,
        "CHANGES REQUIRED": 2,
        "HIGH RISK": 3,
    }.get(recommendation, -1)


def validate_category(category: str, finding_id: str) -> None:
    if category not in ALLOWED_CATEGORIES:
        fail(
            f"{finding_id}: invalid category '{category}'"
        )

    prefix = finding_prefix(finding_id)

    expected_categories = CATEGORY_PREFIXES.get(prefix)

    if expected_categories and category not in expected_categories:
        fail(
            f"{finding_id}: category '{category}' does not match "
            f"finding-ID family '{prefix}'"
        )


def validate_evidence(finding: dict) -> None:
    finding_id = finding["id"]

    evidence = finding.get("evidence")

    if isinstance(evidence, str):
        if not evidence.strip():
            fail(
                f"{finding_id}: evidence must not be empty"
            )

    elif isinstance(evidence, list):
        if not evidence:
            fail(
                f"{finding_id}: evidence array must not be empty"
            )

        for index, item in enumerate(evidence):
            if isinstance(item, str):
                if not item.strip():
                    fail(
                        f"{finding_id}: evidence[{index}] "
                        "must not be empty"
                    )
            elif isinstance(item, dict):
                if not item:
                    fail(
                        f"{finding_id}: evidence[{index}] "
                        "must not be empty"
                    )
            else:
                fail(
                    f"{finding_id}: evidence[{index}] "
                    "must be a string or object"
                )

    elif isinstance(evidence, dict):
        if not evidence:
            fail(
                f"{finding_id}: evidence object must not be empty"
            )

    else:
        fail(
            f"{finding_id}: evidence must be a non-empty "
            "string, array, or object"
        )


def validate_location(finding: dict) -> None:
    finding_id = finding["id"]

    location = finding["location"]

    require_string(
        location,
        "location",
        finding_id,
    )

    lowered = location.lower()

    if "line 0" in lowered:
        fail(
            f"{finding_id}: invalid location appears to use "
            "a fabricated line number"
        )


def validate_finding(finding: dict) -> None:
    if not isinstance(finding, dict):
        fail("Each finding must be an object")

    missing = REQUIRED_FINDING_FIELDS - finding.keys()

    if missing:
        fail(
            "Finding missing fields: "
            f"{sorted(missing)}"
        )

    finding_id = finding["id"]

    validate_finding_id(finding_id)

    severity = finding["severity"]

    if severity not in ALLOWED_SEVERITIES:
        fail(
            f"{finding_id}: invalid severity '{severity}'"
        )

    confidence = finding["confidence"]

    if confidence not in ALLOWED_CONFIDENCE:
        fail(
            f"{finding_id}: invalid confidence '{confidence}'"
        )

    category = finding["category"]

    require_string(
        category,
        "category",
        finding_id,
    )

    validate_category(
        category,
        finding_id,
    )

    require_string(
        finding["title"],
        "title",
        finding_id,
    )

    validate_location(finding)

    for field in (
        "problem",
        "impact",
        "recommendation",
    ):
        require_string(
            finding[field],
            field,
            finding_id,
        )

    validate_evidence(finding)

    if "file" in finding and finding["file"] is not None:
        require_string(
            finding["file"],
            "file",
            finding_id,
        )

    if "evidenceExcerpt" in finding:
        excerpt = finding["evidenceExcerpt"]

        if excerpt is not None and not isinstance(
            excerpt,
            str,
        ):
            fail(
                f"{finding_id}: evidenceExcerpt must be a string"
            )

    if "references" in finding:
        references = finding["references"]

        if not isinstance(
            references,
            (list, str),
        ):
            fail(
                f"{finding_id}: references must be "
                "a string or array"
            )


def validate_declared_counts(
    review: dict,
    severity_counts: Counter,
) -> None:
    declared = review.get("findingCounts")

    if declared is None:
        return

    if not isinstance(declared, dict):
        fail("findingCounts must be an object")

    expected = {
        "CRITICAL": severity_counts.get("CRITICAL", 0),
        "HIGH": severity_counts.get("HIGH", 0),
        "MEDIUM": severity_counts.get("MEDIUM", 0),
        "LOW": severity_counts.get("LOW", 0),
        "NIT": severity_counts.get("NIT", 0),
        "TOTAL": sum(severity_counts.values()),
    }

    for key, expected_value in expected.items():
        if key not in declared:
            continue

        actual_value = declared[key]

        if actual_value != expected_value:
            fail(
                f"Finding count mismatch for {key}: "
                f"declared={actual_value}, "
                f"calculated={expected_value}"
            )


def calculate_category_counts(
    findings: list,
) -> Counter:
    return Counter(
        finding["category"]
        for finding in findings
    )


def validate_category_counts(
    review: dict,
    findings: list,
) -> None:
    declared = review.get("categoryCounts")

    if declared is None:
        return

    if not isinstance(declared, dict):
        fail("categoryCounts must be an object")

    calculated = calculate_category_counts(
        findings
    )

    for category, declared_value in declared.items():
        if not isinstance(declared_value, int):
            fail(
                f"categoryCounts['{category}'] must be an integer"
            )

        calculated_value = calculated.get(
            category,
            0,
        )

        if declared_value != calculated_value:
            fail(
                f"Category count mismatch for '{category}': "
                f"declared={declared_value}, "
                f"calculated={calculated_value}"
            )


def validate_appendix_reconciliation(
    review: dict,
    findings: list,
) -> None:
    appendix = review.get(
        "appendixA",
    )

    if appendix is None:
        return

    if not isinstance(appendix, dict):
        fail("appendixA must be an object")

    appendix_findings = appendix.get(
        "findings",
    )

    if appendix_findings is None:
        return

    if not isinstance(
        appendix_findings,
        list,
    ):
        fail(
            "appendixA.findings must be an array"
        )

    detailed_ids = [
        finding["id"]
        for finding in findings
    ]

    appendix_ids = []

    for item in appendix_findings:
        if isinstance(item, str):
            appendix_ids.append(item)
        elif isinstance(item, dict):
            item_id = item.get("id")

            if not item_id:
                fail(
                    "Appendix A finding entry is missing ID"
                )

            appendix_ids.append(item_id)
        else:
            fail(
                "Appendix A finding entries must be "
                "strings or objects"
            )

    if Counter(detailed_ids) != Counter(
        appendix_ids
    ):
        fail(
            "Appendix A finding inventory does not "
            "match detailed findings"
        )

    appendix["reconciliationStatus"] = "RECONCILED"


def validate_evidence_appendix(
    review: dict,
    findings: list,
) -> None:
    appendix = review.get(
        "appendixB",
    )

    if appendix is None:
        return

    if not isinstance(appendix, dict):
        fail("appendixB must be an object")

    entries = appendix.get(
        "findings",
    )

    if entries is None:
        return

    if not isinstance(entries, list):
        fail(
            "appendixB.findings must be an array"
        )

    finding_ids = {
        finding["id"]
        for finding in findings
    }

    appendix_ids = set()

    for entry in entries:
        if not isinstance(entry, dict):
            fail(
                "Appendix B entries must be objects"
            )

        entry_id = entry.get("id")

        if not entry_id:
            fail(
                "Appendix B entry missing finding ID"
            )

        if entry_id not in finding_ids:
            fail(
                f"Appendix B references unknown finding "
                f"ID: {entry_id}"
            )

        appendix_ids.add(entry_id)

    if appendix_ids != finding_ids:
        missing = sorted(
            finding_ids - appendix_ids
        )

        if missing:
            fail(
                "Appendix B is missing evidence for "
                f"findings: {missing}"
            )


def validate_limitations(review: dict) -> None:
    limitations = review.get(
        "limitations",
    )

    if limitations is None:
        warn(
            "No limitations section supplied. "
            "Ensure the final report records review boundaries."
        )
        return

    if not isinstance(
        limitations,
        (list, dict, str),
    ):
        fail(
            "limitations must be a string, array, or object"
        )


def validate_coverage(review: dict) -> None:
    coverage = review.get(
        "coverage",
    )

    if coverage is None:
        warn(
            "No review coverage section supplied."
        )
        return

    if not isinstance(
        coverage,
        (list, dict),
    ):
        fail(
            "coverage must be an array or object"
        )


def validate_final_verdict_fields(
    review: dict,
) -> tuple:
    stated_risk = review.get(
        "overallRisk",
        "LOW",
    )

    stated_recommendation = review.get(
        "overallRecommendation",
        "APPROVE",
    )

    if stated_risk not in ALLOWED_RISKS:
        fail(
            f"Invalid overallRisk: {stated_risk}"
        )

    if stated_recommendation not in ALLOWED_RECOMMENDATIONS:
        fail(
            "Invalid overallRecommendation: "
            f"{stated_recommendation}"
        )

    return stated_risk, stated_recommendation


def reconcile_verdict(
    review: dict,
    findings: list,
) -> None:
    stated_risk, stated_recommendation = (
        validate_final_verdict_fields(
            review
        )
    )

    minimum_risk, minimum_recommendation = (
        minimum_verdict(findings)
    )

    risk_is_less_severe = (
        risk_rank(stated_risk)
        < risk_rank(minimum_risk)
    )

    recommendation_is_less_severe = (
        recommendation_rank(stated_recommendation)
        < recommendation_rank(minimum_recommendation)
    )

    if risk_is_less_severe or recommendation_is_less_severe:
        review["originalOverallRisk"] = stated_risk

        review["originalOverallRecommendation"] = (
            stated_recommendation
        )

        review["overallRisk"] = (
            minimum_risk
            if risk_is_less_severe
            else stated_risk
        )

        review["overallRecommendation"] = (
            minimum_recommendation
            if recommendation_is_less_severe
            else stated_recommendation
        )

        review["verdictReconciliation"] = {
            "required": True,
            "reason": (
                "The originally stated verdict was less "
                "severe than the evidence-supported minimum."
            ),
            "originalRisk": stated_risk,
            "originalRecommendation": (
                stated_recommendation
            ),
            "minimumRisk": minimum_risk,
            "minimumRecommendation": (
                minimum_recommendation
            ),
            "finalRisk": review["overallRisk"],
            "finalRecommendation": (
                review["overallRecommendation"]
            ),
        }

    else:
        review["verdictReconciliation"] = {
            "required": False,
            "originalRisk": stated_risk,
            "originalRecommendation": (
                stated_recommendation
            ),
            "minimumRisk": minimum_risk,
            "minimumRecommendation": (
                minimum_recommendation
            ),
            "finalRisk": stated_risk,
            "finalRecommendation": (
                stated_recommendation
            ),
        }


def validate_environment() -> None:
    if not FRAMEWORK_ROOT.exists():
        fail(
            f"FRAMEWORK_ROOT does not exist: "
            f"{FRAMEWORK_ROOT}"
        )

    if not APPLICATION_ROOT.exists():
        fail(
            f"APPLICATION_ROOT does not exist: "
            f"{APPLICATION_ROOT}"
        )

    EXECUTION.mkdir(
        parents=True,
        exist_ok=True,
    )


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main() -> None:
    validate_environment()

    if not INPUT.exists():
        fail(
            f"Missing review input: {INPUT}"
        )

    try:
        review = json.loads(
            INPUT.read_text(
                encoding="utf-8",
            )
        )
    except json.JSONDecodeError as exc:
        fail(
            f"Invalid JSON in {INPUT}: {exc}"
        )
    except OSError as exc:
        fail(
            f"Unable to read {INPUT}: {exc}"
        )

    if not isinstance(review, dict):
        fail(
            "Review root must be a JSON object"
        )

    findings = review.get(
        "findings",
        [],
    )

    if not isinstance(findings, list):
        fail(
            "findings must be an array"
        )

    # ---------------------------------------------------------------
    # Validate findings
    # ---------------------------------------------------------------

    finding_ids = []
    signatures = {}

    for finding in findings:
        validate_finding(finding)

        finding_id = finding["id"]

        if finding_id in finding_ids:
            fail(
                f"Duplicate finding ID: {finding_id}"
            )

        finding_ids.append(finding_id)

        signature = finding_signature(
            finding
        )

        if signature in signatures:
            existing_id = signatures[signature]

            fail(
                "Likely duplicate findings detected: "
                f"{existing_id} and {finding_id}. "
                "Same category/title/problem/remediation."
            )

        signatures[signature] = finding_id

    # ---------------------------------------------------------------
    # Counts
    # ---------------------------------------------------------------

    severity_counts = Counter(
        finding["severity"]
        for finding in findings
    )

    category_counts = Counter(
        finding["category"]
        for finding in findings
    )

    validate_declared_counts(
        review,
        severity_counts,
    )

    validate_category_counts(
        review,
        findings,
    )

    # ---------------------------------------------------------------
    # Appendices
    # ---------------------------------------------------------------

    validate_appendix_reconciliation(
        review,
        findings,
    )

    validate_evidence_appendix(
        review,
        findings,
    )

    # ---------------------------------------------------------------
    # Review metadata
    # ---------------------------------------------------------------

    application = review.get(
        "application",
        {},
    )

    if application and not isinstance(
        application,
        dict,
    ):
        fail(
            "application must be an object"
        )

    review_type = review.get(
        "reviewType",
        "FULL_APPLICATION",
    )

    if not isinstance(
        review_type,
        str,
    ):
        fail(
            "reviewType must be a string"
        )

    validate_limitations(review)
    validate_coverage(review)

    # ---------------------------------------------------------------
    # Final verdict reconciliation
    # ---------------------------------------------------------------

    reconcile_verdict(
        review,
        findings,
    )

    # ---------------------------------------------------------------
    # Calculated metadata
    # ---------------------------------------------------------------

    review["calculatedFindingCounts"] = {
        "CRITICAL": severity_counts.get(
            "CRITICAL",
            0,
        ),
        "HIGH": severity_counts.get(
            "HIGH",
            0,
        ),
        "MEDIUM": severity_counts.get(
            "MEDIUM",
            0,
        ),
        "LOW": severity_counts.get(
            "LOW",
            0,
        ),
        "NIT": severity_counts.get(
            "NIT",
            0,
        ),
        "TOTAL": len(findings),
    }

    review["calculatedCategoryCounts"] = dict(
        sorted(
            category_counts.items()
        )
    )

    review["validation"] = {
        "status": "PASSED",
        "applicationRoot": str(
            APPLICATION_ROOT
        ),
        "frameworkRoot": str(
            FRAMEWORK_ROOT
        ),
        "findingCount": len(findings),
        "uniqueFindingIds": len(
            finding_ids
        ),
        "uniqueFindingSignatures": len(
            signatures
        ),
        "findingCountsValidated": True,
        "categoryCountsValidated": True,
        "verdictReconciled": True,
        "sourceModificationPerformed": False,
    }

    # ---------------------------------------------------------------
    # Write only inside framework root
    # ---------------------------------------------------------------

    try:
        OUTPUT.write_text(
            json.dumps(
                review,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
    except OSError as exc:
        fail(
            f"Unable to write validated review: {exc}"
        )

    print(
        "Validation passed: "
        f"{OUTPUT}"
    )


if __name__ == "__main__":
    main()