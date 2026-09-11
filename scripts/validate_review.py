#!/usr/bin/env python3

import json
import sys
from pathlib import Path
from collections import Counter


ROOT = Path.cwd()
EXECUTION = ROOT / "workspace" / "execution"

INPUT = EXECUTION / "review.json"
OUTPUT = EXECUTION / "validated-review.json"


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


def fail(message):
    print(f"VALIDATION FAILED: {message}")
    sys.exit(1)


def minimum_verdict(findings):
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


def main():
    if not INPUT.exists():
        fail(f"Missing {INPUT}")

    try:
        review = json.loads(
            INPUT.read_text(encoding="utf-8")
        )
    except Exception as exc:
        fail(f"Invalid JSON: {exc}")

    if not isinstance(review, dict):
        fail("Review must be a JSON object")

    findings = review.get("findings", [])

    if not isinstance(findings, list):
        fail("findings must be an array")

    ids = set()

    for index, finding in enumerate(findings, 1):
        if not isinstance(finding, dict):
            fail(
                f"Finding {index} must be an object"
            )

        missing = (
            REQUIRED_FINDING_FIELDS
            - finding.keys()
        )

        if missing:
            fail(
                f"Finding {index} missing fields: "
                f"{sorted(missing)}"
            )

        finding_id = finding["id"]

        if finding_id in ids:
            fail(
                f"Duplicate finding ID: {finding_id}"
            )

        ids.add(finding_id)

        severity = finding["severity"]

        if severity not in ALLOWED_SEVERITIES:
            fail(
                f"Invalid severity for {finding_id}: "
                f"{severity}"
            )

        confidence = finding["confidence"]

        if confidence not in ALLOWED_CONFIDENCE:
            fail(
                f"Invalid confidence for {finding_id}: "
                f"{confidence}"
            )

    severity_counts = Counter(
        finding["severity"]
        for finding in findings
    )

    risk, minimum_recommendation = minimum_verdict(
        findings
    )

    stated_risk = review.get(
        "overallRisk",
        "LOW",
    )

    stated_recommendation = review.get(
        "overallRecommendation",
        "APPROVE",
    )

    if stated_recommendation not in ALLOWED_RECOMMENDATIONS:
        fail(
            "Invalid overallRecommendation: "
            f"{stated_recommendation}"
        )

    recommendation_order = {
        "APPROVE": 0,
        "APPROVE WITH MINOR CHANGES": 1,
        "CHANGES REQUIRED": 2,
        "HIGH RISK": 3,
    }

    stated_rank = recommendation_order[
        stated_recommendation
    ]

    minimum_rank = recommendation_order[
        minimum_recommendation
    ]

    reconciliation_required = (
        stated_rank < minimum_rank
    )

    if reconciliation_required:
        review["originalOverallRisk"] = stated_risk
        review["originalOverallRecommendation"] = (
            stated_recommendation
        )

        review["overallRisk"] = risk
        review["overallRecommendation"] = (
            minimum_recommendation
        )

        review["verdictReconciliation"] = {
            "required": True,
            "reason": (
                "The stated verdict was less severe "
                "than the evidence-supported minimum."
            ),
            "minimumRisk": risk,
            "minimumRecommendation":
                minimum_recommendation,
        }

    else:
        review["verdictReconciliation"] = {
            "required": False,
            "minimumRisk": risk,
            "minimumRecommendation":
                minimum_recommendation,
        }

    review["calculatedFindingCounts"] = {
        "CRITICAL": severity_counts.get(
            "CRITICAL", 0
        ),
        "HIGH": severity_counts.get(
            "HIGH", 0
        ),
        "MEDIUM": severity_counts.get(
            "MEDIUM", 0
        ),
        "LOW": severity_counts.get(
            "LOW", 0
        ),
        "NIT": severity_counts.get(
            "NIT", 0
        ),
        "TOTAL": len(findings),
    }

    review["validation"] = {
        "status": "PASSED",
        "findingCount": len(findings),
        "uniqueFindingIds": len(ids),
        "verdictReconciled":
            reconciliation_required,
    }

    OUTPUT.write_text(
        json.dumps(
            review,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"Validation passed: {OUTPUT}"
    )


if __name__ == "__main__":
    main()