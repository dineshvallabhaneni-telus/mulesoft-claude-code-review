#!/usr/bin/env python3

"""
Collect repository evidence for the MuleSoft code review framework.

Execution model:
    The script is executed with the MuleSoft application root as the
    current working directory.

Purpose:
    - Read application source/configuration only.
    - Collect structural evidence and review signals.
    - Never modify application source files.
    - Write exactly one structured evidence file:
          workspace/execution/review-evidence.json

This script does NOT determine findings. It only collects evidence
that the review agent can subsequently validate.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT = Path.cwd()

EXECUTION_DIR = ROOT / "workspace" / "execution"
OUTPUT_FILE = EXECUTION_DIR / "review-evidence.json"

EXECUTION_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ---------------------------------------------------------------------------
# Repository exclusions
# ---------------------------------------------------------------------------

IGNORE_DIRS = {
    ".git",
    ".idea",
    ".vscode",
    "target",
    "node_modules",
    "reports",
    "workspace",
}


# ---------------------------------------------------------------------------
# Source file types
# ---------------------------------------------------------------------------

SOURCE_EXTENSIONS = {
    ".xml",
    ".dwl",
    ".raml",
    ".yaml",
    ".yml",
    ".json",
    ".properties",
    ".java",
}


# ---------------------------------------------------------------------------
# Sensitive-value protection
# ---------------------------------------------------------------------------

SECRET_PATTERNS = [
    re.compile(
        r"(?i)(password|passwd|secret|client[_-]?secret|api[_-]?key|"
        r"access[_-]?token|private[_-]?key)\s*[:=]\s*([^\s,;\"']+)"
    ),
    re.compile(
        r"(?i)(authorization)\s*[:=]\s*(Bearer\s+)?([^\s,;\"']+)"
    ),
]


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""
    return datetime.now(timezone.utc).isoformat()


def safe_read(path: Path) -> str:
    """
    Read a text file without allowing an unreadable file to terminate
    the evidence collection process.
    """
    try:
        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )
    except Exception:
        return ""


def is_ignored(path: Path) -> bool:
    """Return True when any path component belongs to an ignored directory."""
    return any(
        part in IGNORE_DIRS
        for part in path.parts
    )


def iter_source_files() -> Iterable[Path]:
    """
    Yield review-relevant application files.

    Files under generated/excluded directories are never inspected.
    """
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue

        if is_ignored(path):
            continue

        if path.suffix.lower() not in SOURCE_EXTENSIONS:
            continue

        yield path


def relative_path(path: Path) -> str:
    """Return a repository-relative POSIX-style path."""
    return path.relative_to(ROOT).as_posix()


# ---------------------------------------------------------------------------
# Sensitive-data masking
# ---------------------------------------------------------------------------

def mask_sensitive_text(text: str) -> str:
    """
    Mask likely secret values before evidence is written.

    The evidence collector may identify that a sensitive configuration
    exists, but must never persist the actual secret value.
    """
    masked = text

    for pattern in SECRET_PATTERNS:
        def replace(match: re.Match) -> str:
            groups = match.groups()

            if len(groups) == 2:
                return f"{groups[0]}=<MASKED>"

            if len(groups) == 3:
                return f"{groups[0]}={groups[1] or ''}<MASKED>"

            return "<MASKED>"

        masked = pattern.sub(replace, masked)

    return masked


# ---------------------------------------------------------------------------
# Line evidence
# ---------------------------------------------------------------------------

def line_matches(
    text: str,
    patterns: List[str],
    max_matches: int = 100,
) -> List[Dict]:
    """
    Find matching source lines.

    Evidence is deliberately limited to prevent oversized JSON artifacts.
    """
    matches: List[Dict] = []

    lines = text.splitlines()

    for line_number, line in enumerate(lines, start=1):
        for pattern in patterns:
            try:
                matched = re.search(
                    pattern,
                    line,
                    re.IGNORECASE,
                )
            except re.error:
                matched = None

            if not matched:
                continue

            matches.append(
                {
                    "line": line_number,
                    "text": mask_sensitive_text(
                        line[:500]
                    ),
                    "pattern": pattern,
                }
            )

            if len(matches) >= max_matches:
                return matches

    return matches


# ---------------------------------------------------------------------------
# Review signal patterns
# ---------------------------------------------------------------------------

PATTERNS = {
    "security": [
        r"\bpassword\b",
        r"\bpasswd\b",
        r"\bclient.?secret\b",
        r"\bapi.?key\b",
        r"\baccess.?token\b",
        r"\bprivate.?key\b",
        r"\bauthorization\b",
        r"\bbearer\b",
        r"\bcredential\b",
        r"\bsecret\b",
        r"secure::",
        r"secure-properties",
        r"tls:context",
        r"trust-store",
        r"key-store",
    ],
    "errorHandling": [
        r"on-error-continue",
        r"on-error-propagate",
        r"error-handler",
        r"<try\b",
        r"<until-successful\b",
        r"error-mapping",
        r"raise-error",
    ],
    "logging": [
        r"<logger\b",
        r"\blog\(",
        r"\blogger\b",
    ],
    "retry": [
        r"until-successful",
        r"\bretry\b",
        r"reconnection",
        r"reconnect",
        r"maxRetries",
        r"retryCount",
    ],
    "transactions": [
        r"\btransaction\b",
        r"\btransactional\b",
        r"transactionType",
        r"action=\"[A-Z_]+\"",
    ],
    "database": [
        r"<db:",
        r"\bdb:",
        r"\bselect\s+",
        r"\binsert\s+",
        r"\bupdate\s+",
        r"\bdelete\s+",
        r"\bcall\s+",
        r"queryTimeout",
        r"maxPoolSize",
        r"connectionTimeout",
    ],
    "messaging": [
        r"jms:",
        r"amqp:",
        r"kafka:",
        r"anypoint-mq:",
        r"vm:",
        r"acknowledg",
        r"redeliver",
        r"dead.?letter",
        r"dlq",
    ],
    "api": [
        r"http:listener",
        r"http:request",
        r"\braml\b",
        r"\bopenapi\b",
        r"\boas\b",
        r"statusCode",
        r"status-code",
        r"response",
        r"request",
        r"authentication",
        r"authorization",
    ],
    "connectors": [
        r"http:request",
        r"db:",
        r"jms:",
        r"amqp:",
        r"kafka:",
        r"anypoint-mq:",
        r"sftp:",
        r"ftp:",
        r"salesforce:",
        r"objectstore:",
        r"file:",
        r"vm:",
    ],
    "configuration": [
        r"configuration-properties",
        r"global-property",
        r"secure-properties",
        r"\$\{[^}]+\}",
        r"secure::",
        r"host=",
        r"port=",
        r"url=",
        r"username=",
        r"password=",
    ],
    "flowStructure": [
        r"<flow\b",
        r"<sub-flow\b",
        r"<private-flow\b",
        r"flow-ref",
        r"choice",
        r"scatter-gather",
        r"parallel-foreach",
        r"foreach",
        r"async",
        r"until-successful",
        r"try",
    ],
    "dataWeave": [
        r"%dw\s+2\.",
        r"output\s+application/",
        r"output\s+application/json",
        r"payload",
        r"vars\.",
        r"attributes",
        r"\bmap\b",
        r"\bmapObject\b",
        r"\bflatMap\b",
        r"\bfilter\b",
        r"\bgroupBy\b",
        r"\bflatten\b",
        r"\bpluck\b",
        r"\bdefault\b",
        r"\bas\s+[A-Za-z]",
    ],
    "scheduling": [
        r"scheduler",
        r"fixed-frequency",
        r"cron",
        r"poll:",
    ],
    "batch": [
        r"batch:",
        r"batch-job",
        r"batch:step",
        r"batch:aggregator",
    ],
    "objectStore": [
        r"objectstore:",
        r"object-store",
        r"objectStore",
    ],
}


# ---------------------------------------------------------------------------
# File classification
# ---------------------------------------------------------------------------

def classify_file(path: Path) -> List[str]:
    """Return useful semantic classifications for a source file."""
    suffix = path.suffix.lower()
    name = path.name.lower()
    relative = relative_path(path).lower()

    classifications: List[str] = []

    if suffix == ".xml":
        classifications.append("xml")

        if "munit" in relative or "test" in name:
            classifications.append("munit")

    elif suffix == ".dwl":
        classifications.append("dataweave")

    elif suffix == ".raml":
        classifications.append("raml")

    elif suffix in {".yaml", ".yml", ".json"}:
        classifications.append("api-spec-candidate")

    elif suffix == ".properties":
        classifications.append("properties")

    elif suffix == ".java":
        classifications.append("java")

    return classifications


# ---------------------------------------------------------------------------
# Repository-level feature detection
# ---------------------------------------------------------------------------

def detect_repository_features(
    file_contents: Dict[str, str],
) -> Dict[str, bool]:
    """Detect application capabilities from actual source evidence."""

    combined = "\n".join(
        file_contents.values()
    )

    return {
        "httpListener": bool(
            re.search(
                r"http:listener",
                combined,
                re.IGNORECASE,
            )
        ),
        "httpRequest": bool(
            re.search(
                r"http:request",
                combined,
                re.IGNORECASE,
            )
        ),
        "database": bool(
            re.search(
                r"(?:<db:|\bdb:)",
                combined,
                re.IGNORECASE,
            )
        ),
        "messaging": bool(
            re.search(
                r"(?:jms:|amqp:|kafka:|anypoint-mq:|vm:)",
                combined,
                re.IGNORECASE,
            )
        ),
        "scheduler": bool(
            re.search(
                r"scheduler",
                combined,
                re.IGNORECASE,
            )
        ),
        "batch": bool(
            re.search(
                r"batch:",
                combined,
                re.IGNORECASE,
            )
        ),
        "objectStore": bool(
            re.search(
                r"(?:objectstore:|object-store|objectStore)",
                combined,
                re.IGNORECASE,
            )
        ),
        "salesforce": bool(
            re.search(
                r"salesforce",
                combined,
                re.IGNORECASE,
            )
        ),
        "munit": bool(
            re.search(
                r"(?:munit:|munit|munit-tools:)",
                combined,
                re.IGNORECASE,
            )
        ),
        "secureProperties": bool(
            re.search(
                r"(?:secure-properties|secure::)",
                combined,
                re.IGNORECASE,
            )
        ),
        "tls": bool(
            re.search(
                r"(?:tls:context|tls:client|tls:server)",
                combined,
                re.IGNORECASE,
            )
        ),
        "transactions": bool(
            re.search(
                r"(?:transaction|transactional)",
                combined,
                re.IGNORECASE,
            )
        ),
    }


# ---------------------------------------------------------------------------
# Main collector
# ---------------------------------------------------------------------------

def main() -> None:
    files = sorted(
        iter_source_files(),
        key=lambda path: relative_path(path),
    )

    evidence_files: List[Dict] = []
    file_contents: Dict[str, str] = {}

    signals = {
        category: []
        for category in PATTERNS
    }

    total_lines = 0
    total_bytes = 0

    for path in files:
        text = safe_read(path)
        relative = relative_path(path)

        file_contents[relative] = text

        try:
            size = path.stat().st_size
        except OSError:
            size = 0

        line_count = len(text.splitlines())

        total_lines += line_count
        total_bytes += size

        evidence_files.append(
            {
                "path": relative,
                "extension": path.suffix.lower(),
                "size": size,
                "lineCount": line_count,
                "classifications": classify_file(path),
            }
        )

        for category, patterns in PATTERNS.items():
            matches = line_matches(
                text,
                patterns,
                max_matches=100,
            )

            if not matches:
                continue

            signals[category].append(
                {
                    "file": relative,
                    "matches": matches,
                }
            )

    repository_features = detect_repository_features(
        file_contents
    )

    extension_counts: Dict[str, int] = {}

    for file_entry in evidence_files:
        extension = file_entry["extension"]

        extension_counts[extension] = (
            extension_counts.get(extension, 0) + 1
        )

    evidence = {
        "generatedAt": utc_now(),

        "sourceReadOnly": True,

        "execution": {
            "applicationRoot": str(ROOT),
            "executionDirectory": str(EXECUTION_DIR),
            "outputFile": str(OUTPUT_FILE),
        },

        "repository": {
            "fileCount": len(evidence_files),
            "totalLines": total_lines,
            "totalBytes": total_bytes,
            "extensionCounts": extension_counts,
            "features": repository_features,
        },

        "files": evidence_files,

        "signals": signals,

        "limitations": [
            (
                "This artifact contains discovery and signal evidence; "
                "signals are not findings."
            ),
            (
                "Runtime behavior that cannot be established from "
                "repository evidence is not classified as confirmed."
            ),
            (
                "Sensitive values detected during collection are masked "
                "before evidence is written."
            ),
        ],
    }

    OUTPUT_FILE.write_text(
        json.dumps(
            evidence,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(
        f"Evidence written to {OUTPUT_FILE}"
    )

    print(
        f"Files scanned: {len(evidence_files)}"
    )

    print(
        f"Lines scanned: {total_lines}"
    )


if __name__ == "__main__":
    main()