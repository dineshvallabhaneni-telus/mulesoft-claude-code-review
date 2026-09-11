#!/usr/bin/env python3

import json
import os
import re
from pathlib import Path
from datetime import datetime


APPLICATION_ROOT = Path(
    os.environ.get(
        "APPLICATION_ROOT",
        Path.cwd(),
    )
).resolve()

EXECUTION = (
    APPLICATION_ROOT
    / "workspace"
    / "execution"
)

EXECUTION.mkdir(
    parents=True,
    exist_ok=True,
)


IGNORE_DIRS = {
    ".git",
    ".idea",
    ".vscode",
    "target",
    "node_modules",
    "reports",
    "workspace",
}


SOURCE_EXTENSIONS = {
    ".xml",
    ".dwl",
    ".raml",
    ".yaml",
    ".yml",
    ".json",
    ".properties",
    ".java",
    ".md",
}


def iter_source_files():
    for path in APPLICATION_ROOT.rglob("*"):
        if not path.is_file():
            continue

        if any(
            part in IGNORE_DIRS
            for part in path.parts
        ):
            continue

        if (
            path.suffix.lower()
            in SOURCE_EXTENSIONS
        ):
            yield path


def safe_read(path):
    try:
        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )
    except Exception:
        return ""


def line_matches(text, patterns):
    matches = []

    lines = text.splitlines()

    for index, line in enumerate(
        lines,
        start=1,
    ):
        for pattern in patterns:
            if re.search(
                pattern,
                line,
                re.IGNORECASE,
            ):
                matches.append(
                    {
                        "line": index,
                        "text": line[:500],
                        "pattern": pattern,
                    }
                )

    return matches


def main():
    discovery_file = (
        EXECUTION
        / "application-discovery.json"
    )

    discovery = {}

    if discovery_file.exists():
        try:
            discovery = json.loads(
                discovery_file.read_text(
                    encoding="utf-8"
                )
            )
        except Exception:
            discovery = {}

    evidence = {
        "generatedAt":
            datetime.utcnow().isoformat() + "Z",

        "sourceReadOnly": True,

        "applicationRoot":
            str(APPLICATION_ROOT),

        "files": [],

        "signals": {
            "security": [],
            "errorHandling": [],
            "logging": [],
            "retry": [],
            "transactions": [],
            "database": [],
            "messaging": [],
            "api": [],
        },
    }

    patterns = {
        "security": [
            r"password",
            r"client.?secret",
            r"api.?key",
            r"access.?token",
            r"private.?key",
            r"authorization",
        ],

        "errorHandling": [
            r"on-error-continue",
            r"on-error-propagate",
            r"<try",
            r"error-handler",
        ],

        "logging": [
            r"<logger",
            r"log\(",
        ],

        "retry": [
            r"until-successful",
            r"retry",
            r"reconnection",
        ],

        "transactions": [
            r"transaction",
            r"transactional",
        ],

        "database": [
            r"<db:",
            r"db:",
            r"select\s+",
            r"insert\s+",
            r"update\s+",
            r"delete\s+",
        ],

        "messaging": [
            r"jms:",
            r"amqp:",
            r"kafka:",
            r"anypoint-mq:",
            r"vm:",
        ],

        "api": [
            r"http:listener",
            r"http:request",
            r"raml",
            r"openapi",
        ],
    }

    for path in iter_source_files():
        text = safe_read(path)

        relative = str(
            path.relative_to(
                APPLICATION_ROOT
            )
        )

        try:
            size = path.stat().st_size
        except OSError:
            size = 0

        evidence["files"].append(
            {
                "path": relative,
                "extension":
                    path.suffix.lower(),
                "size": size,
                "lineCount":
                    len(text.splitlines()),
            }
        )

        for category, category_patterns in (
            patterns.items()
        ):
            matches = line_matches(
                text,
                category_patterns,
            )

            if matches:
                evidence["signals"][
                    category
                ].append(
                    {
                        "file": relative,
                        "matches": matches[:100],
                    }
                )

    output = (
        EXECUTION
        / "review-evidence.json"
    )

    output.write_text(
        json.dumps(
            evidence,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"Evidence written to {output}"
    )


if __name__ == "__main__":
    main()