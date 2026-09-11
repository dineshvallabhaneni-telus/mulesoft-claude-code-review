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


def files_with_extensions(extensions):
    results = []

    for path in APPLICATION_ROOT.rglob("*"):
        if not path.is_file():
            continue

        if any(
            part in IGNORE_DIRS
            for part in path.parts
        ):
            continue

        if path.suffix.lower() in extensions:
            results.append(
                str(
                    path.relative_to(
                        APPLICATION_ROOT
                    )
                )
            )

    return sorted(results)


def read_text(path):
    try:
        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )
    except Exception:
        return ""


def find_first(pattern, text):
    match = re.search(
        pattern,
        text,
        re.MULTILINE,
    )

    return (
        match.group(1).strip()
        if match
        else None
    )


def inspect_pom():
    pom = APPLICATION_ROOT / "pom.xml"

    if not pom.exists():
        return {
            "exists": False,
            "runtime": None,
            "javaVersion": None,
            "muleMavenPlugin": False,
        }

    text = read_text(pom)

    return {
        "exists": True,
        "runtime": find_first(
            r"<(?:mule\.runtime|muleRuntimeVersion)[^>]*>\s*([^<]+)",
            text,
        ),
        "javaVersion": find_first(
            r"<(?:java\.version|maven.compiler.source)[^>]*>\s*([^<]+)",
            text,
        ),
        "muleMavenPlugin": bool(
            re.search(
                r"mule-maven-plugin",
                text,
                re.IGNORECASE,
            )
        ),
    }


def detect_features():
    xml_files = files_with_extensions(
        {".xml"}
    )

    dw_files = files_with_extensions(
        {".dwl"}
    )

    raml_files = files_with_extensions(
        {".raml"}
    )

    api_spec_files = files_with_extensions(
        {".yaml", ".yml", ".json"}
    )

    property_files = files_with_extensions(
        {".properties"}
    )

    test_files = [
        path
        for path in xml_files
        if (
            "test" in path.lower()
            or "munit" in path.lower()
        )
    ]

    combined = "\n".join(
        read_text(
            APPLICATION_ROOT / path
        )
        for path in xml_files[:500]
    )

    return {
        "muleXmlFiles": xml_files,
        "dataWeaveFiles": dw_files,
        "ramlFiles": raml_files,
        "apiSpecificationCandidates":
            api_spec_files,
        "propertyFiles": property_files,
        "munitCandidates": test_files,
        "features": {
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
                    r"db:",
                    combined,
                    re.IGNORECASE,
                )
            ),
            "messaging": bool(
                re.search(
                    r"(jms:|amqp:|vm:|kafka:|anypoint-mq:)",
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
                    r"objectstore",
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
        },
    }


def main():
    pom = inspect_pom()
    features = detect_features()

    application_name = (
        APPLICATION_ROOT.name
    )

    result = {
        "generatedAt":
            datetime.utcnow().isoformat() + "Z",

        "application": {
            "name": application_name,
            "repositoryPath":
                str(APPLICATION_ROOT),
        },

        "build": pom,

        "files": features,

        "reviewType": os.environ.get(
            "REVIEW_TYPE",
            "FULL_APPLICATION",
        ),
    }

    output = (
        EXECUTION
        / "application-discovery.json"
    )

    output.write_text(
        json.dumps(
            result,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"Discovery written to {output}"
    )


if __name__ == "__main__":
    main()