#!/usr/bin/env python3

"""
MuleSoft application discovery.

Execution model:
    framework_root/
        CLAUDE.md
        agents/
        skills/
        references/
        scripts/
        reports/
        workspace/
        <MuleSoft application source>

The script is intentionally read-only against the application source.

It discovers:
- application identity
- Git metadata
- Maven/runtime metadata
- Mule XML
- DataWeave
- API specifications
- properties
- MUnit
- deployment configuration
- integration technologies
- framework/application boundaries

Generated file:
    <framework_root>/workspace/execution/application-discovery.json
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SCRIPT_PATH = Path(__file__).resolve()
FRAMEWORK_ROOT = SCRIPT_PATH.parent.parent.resolve()

# The framework root is also the execution root for this review framework.
ROOT = FRAMEWORK_ROOT

EXECUTION_DIR = ROOT / "workspace" / "execution"
OUTPUT_FILE = EXECUTION_DIR / "application-discovery.json"

EXECUTION_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Directory boundaries
# ---------------------------------------------------------------------------

IGNORED_DIR_NAMES = {
    ".git",
    ".idea",
    ".vscode",
    ".github",
    "target",
    "node_modules",
    "reports",
    "workspace",
    "__pycache__",
}

# Framework-owned directories are not application source.
FRAMEWORK_DIR_NAMES = {
    "agents",
    "skills",
    "references",
    "scripts",
}


# ---------------------------------------------------------------------------
# File extensions
# ---------------------------------------------------------------------------

MULE_XML_EXTENSIONS = {".xml"}
DATAWEAVE_EXTENSIONS = {".dwl"}
RAML_EXTENSIONS = {".raml"}
PROPERTY_EXTENSIONS = {".properties"}
JAVA_EXTENSIONS = {".java"}

API_CANDIDATE_EXTENSIONS = {
    ".yaml",
    ".yml",
    ".json",
}

DEPLOYMENT_FILE_NAMES = {
    "mule-artifact.json",
    "mule-deploy.json",
    "runtime.yaml",
    "runtime.yml",
    "deployment.yaml",
    "deployment.yml",
    "deployment.json",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def safe_read(path: Path) -> str:
    try:
        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )
    except (OSError, UnicodeError):
        return ""


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def should_ignore(path: Path) -> bool:
    """
    Ignore framework-generated/runtime directories.

    The check is component-based rather than string-based so that paths
    such as 'src/main/workspace-data' are not accidentally ignored.
    """
    return any(
        part in IGNORED_DIR_NAMES
        for part in path.parts
    )


def is_framework_file(path: Path) -> bool:
    """
    Identify files belonging to the review framework itself.

    This prevents framework source from being mistaken for Mule
    application source.
    """
    parts = set(path.parts)

    if parts.intersection(FRAMEWORK_DIR_NAMES):
        return True

    if path.name == "CLAUDE.md":
        return True

    return False


def iter_files() -> Iterable[Path]:
    """
    Recursively enumerate files while respecting framework boundaries.
    """
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue

        if should_ignore(path):
            continue

        if is_framework_file(path):
            continue

        yield path


def files_with_extensions(
    extensions: set[str],
) -> list[Path]:
    return sorted(
        path
        for path in iter_files()
        if path.suffix.lower() in extensions
    )


def find_first(
    patterns: list[str],
    text: str,
) -> Optional[str]:
    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.MULTILINE | re.IGNORECASE,
        )

        if match:
            value = match.group(1).strip()

            if value:
                return value

    return None


def find_all(
    patterns: list[str],
    text: str,
) -> list[str]:
    values: list[str] = []

    for pattern in patterns:
        for match in re.finditer(
            pattern,
            text,
            re.MULTILINE | re.IGNORECASE,
        ):
            value = match.group(1).strip()

            if value and value not in values:
                values.append(value)

    return values


def contains_any(
    text: str,
    patterns: list[str],
) -> bool:
    return any(
        re.search(
            pattern,
            text,
            re.IGNORECASE,
        )
        for pattern in patterns
    )


def run_git(
    *args: str,
) -> Optional[str]:
    """
    Read-only Git metadata.

    Any failure is represented as unavailable metadata rather than
    causing the discovery step to fail.
    """
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            return None

        value = result.stdout.strip()

        return value or None

    except (
        OSError,
        subprocess.SubprocessError,
    ):
        return None


def get_git_metadata() -> dict:
    return {
        "repository": run_git(
            "config",
            "--get",
            "remote.origin.url",
        ),
        "branch": (
            run_git(
                "rev-parse",
                "--abbrev-ref",
                "HEAD",
            )
            or os.environ.get("GITHUB_REF_NAME")
        ),
        "commit": (
            run_git(
                "rev-parse",
                "HEAD",
            )
            or os.environ.get("GITHUB_SHA")
        ),
        "isGitRepository": (
            run_git(
                "rev-parse",
                "--is-inside-work-tree",
            )
            == "true"
        ),
    }


# ---------------------------------------------------------------------------
# Application root discovery
# ---------------------------------------------------------------------------

def detect_application_root(
    pom_files: list[Path],
    mule_xml_files: list[Path],
) -> Optional[Path]:
    """
    Identify the most likely Mule application root.

    Priority:
    1. pom.xml containing Mule Maven Plugin
    2. pom.xml containing Mule runtime metadata
    3. directory containing mule-artifact.json
    4. common Mule source layout
    5. framework root if the repository itself is the application

    This function never changes directories or files.
    """

    candidates: list[tuple[int, Path]] = []

    for pom in pom_files:
        text = safe_read(pom)

        score = 0

        if re.search(
            r"mule-maven-plugin",
            text,
            re.IGNORECASE,
        ):
            score += 100

        if re.search(
            r"mule\.runtime|muleRuntimeVersion",
            text,
            re.IGNORECASE,
        ):
            score += 50

        if re.search(
            r"<groupId>\s*org\.mule",
            text,
            re.IGNORECASE,
        ):
            score += 20

        if score:
            candidates.append(
                (score, pom.parent)
            )

    artifact_files = [
        path
        for path in iter_files()
        if path.name == "mule-artifact.json"
    ]

    for artifact in artifact_files:
        candidates.append(
            (80, artifact.parent)
        )

    for directory in {
        path.parent
        for path in mule_xml_files
    }:
        score = 0

        if (directory / "src").exists():
            score += 20

        if (directory / "src" / "main").exists():
            score += 20

        if (
            directory
            / "src"
            / "main"
            / "mule"
        ).exists():
            score += 30

        if score:
            candidates.append(
                (score, directory)
            )

    if not candidates:
        return None

    candidates.sort(
        key=lambda item: (
            -item[0],
            len(item[1].parts),
            str(item[1]),
        )
    )

    return candidates[0][1]


# ---------------------------------------------------------------------------
# Maven / runtime discovery
# ---------------------------------------------------------------------------

def inspect_pom(
    application_root: Optional[Path],
) -> dict:
    if application_root is None:
        return {
            "exists": False,
            "path": None,
            "groupId": None,
            "artifactId": None,
            "version": None,
            "packaging": None,
            "runtime": None,
            "javaVersion": None,
            "muleMavenPlugin": False,
            "muleMavenPluginVersion": None,
        }

    pom = application_root / "pom.xml"

    if not pom.exists():
        return {
            "exists": False,
            "path": None,
            "groupId": None,
            "artifactId": None,
            "version": None,
            "packaging": None,
            "runtime": None,
            "javaVersion": None,
            "muleMavenPlugin": False,
            "muleMavenPluginVersion": None,
        }

    text = safe_read(pom)

    plugin_version = find_first(
        [
            r"<artifactId>\s*mule-maven-plugin\s*</artifactId>"
            r".{0,1500}?"
            r"<version>\s*([^<]+)\s*</version>",
        ],
        text,
    )

    return {
        "exists": True,
        "path": relative_path(pom),
        "groupId": find_first(
            [r"<groupId>\s*([^<]+)\s*</groupId>"],
            text,
        ),
        "artifactId": find_first(
            [r"<artifactId>\s*([^<]+)\s*</artifactId>"],
            text,
        ),
        "version": find_first(
            [
                r"<version>\s*([^<]+)\s*</version>"
            ],
            text,
        ),
        "packaging": find_first(
            [
                r"<packaging>\s*([^<]+)\s*</packaging>"
            ],
            text,
        ),
        "runtime": find_first(
            [
                r"<(?:mule\.runtime|muleRuntimeVersion)"
                r">\s*([^<]+)"
            ],
            text,
        ),
        "javaVersion": find_first(
            [
                r"<(?:java\.version|maven.compiler.source)"
                r">\s*([^<]+)",
                r"<maven.compiler.release>\s*([^<]+)",
            ],
            text,
        ),
        "muleMavenPlugin": bool(
            re.search(
                r"<artifactId>\s*mule-maven-plugin\s*</artifactId>",
                text,
                re.IGNORECASE,
            )
        ),
        "muleMavenPluginVersion": plugin_version,
    }


# ---------------------------------------------------------------------------
# Mule artifact metadata
# ---------------------------------------------------------------------------

def inspect_mule_artifact(
    application_root: Optional[Path],
) -> dict:
    if application_root is None:
        return {
            "exists": False,
            "path": None,
            "name": None,
            "minMuleVersion": None,
        }

    artifact = application_root / "mule-artifact.json"

    if not artifact.exists():
        return {
            "exists": False,
            "path": None,
            "name": None,
            "minMuleVersion": None,
        }

    try:
        data = json.loads(
            artifact.read_text(
                encoding="utf-8"
            )
        )
    except (
        OSError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ):
        return {
            "exists": True,
            "path": relative_path(artifact),
            "name": None,
            "minMuleVersion": None,
            "parseError": True,
        }

    return {
        "exists": True,
        "path": relative_path(artifact),
        "name": data.get("name"),
        "minMuleVersion": data.get(
            "minMuleVersion"
        ),
    }


# ---------------------------------------------------------------------------
# Mule XML discovery
# ---------------------------------------------------------------------------

def inspect_mule_xml(
    xml_files: list[Path],
) -> dict:
    all_text = "\n".join(
        safe_read(path)
        for path in xml_files
    )

    return {
        "count": len(xml_files),
        "files": [
            relative_path(path)
            for path in xml_files
        ],
        "features": {
            "httpListener": contains_any(
                all_text,
                [
                    r"<http:listener\b",
                    r"http:listener",
                ],
            ),
            "httpRequest": contains_any(
                all_text,
                [
                    r"<http:request\b",
                    r"http:request",
                ],
            ),
            "database": contains_any(
                all_text,
                [
                    r"<db:",
                    r"db:",
                ],
            ),
            "messaging": contains_any(
                all_text,
                [
                    r"<jms:",
                    r"<amqp:",
                    r"<kafka:",
                    r"<anypoint-mq:",
                    r"<vm:",
                ],
            ),
            "scheduler": contains_any(
                all_text,
                [
                    r"<scheduler:",
                    r"scheduler",
                ],
            ),
            "batch": contains_any(
                all_text,
                [
                    r"<batch:",
                    r"batch:",
                ],
            ),
            "objectStore": contains_any(
                all_text,
                [
                    r"objectstore",
                    r"object-store",
                ],
            ),
            "salesforce": contains_any(
                all_text,
                [
                    r"<salesforce:",
                    r"salesforce",
                ],
            ),
            "untilSuccessful": contains_any(
                all_text,
                [
                    r"until-successful",
                ],
            ),
            "tryScope": contains_any(
                all_text,
                [
                    r"<try\b",
                ],
            ),
            "errorHandlers": contains_any(
                all_text,
                [
                    r"on-error-continue",
                    r"on-error-propagate",
                    r"error-handler",
                ],
            ),
            "transactions": contains_any(
                all_text,
                [
                    r"transaction",
                    r"transactional",
                ],
            ),
            "flowReferences": contains_any(
                all_text,
                [
                    r"<flow-ref\b",
                ],
            ),
            "subflows": contains_any(
                all_text,
                [
                    r"<sub-flow\b",
                ],
            ),
            "privateFlows": contains_any(
                all_text,
                [
                    r"<flow\b",
                ],
            ),
            "async": contains_any(
                all_text,
                [
                    r"<async\b",
                ],
            ),
            "foreach": contains_any(
                all_text,
                [
                    r"<foreach\b",
                ],
            ),
            "parallelForeach": contains_any(
                all_text,
                [
                    r"<parallel-foreach\b",
                ],
            ),
            "choice": contains_any(
                all_text,
                [
                    r"<choice\b",
                ],
            ),
            "scatterGather": contains_any(
                all_text,
                [
                    r"<scatter-gather\b",
                ],
            ),
            "forEach": contains_any(
                all_text,
                [
                    r"<foreach\b",
                ],
            ),
        },
    }


# ---------------------------------------------------------------------------
# DataWeave / API / configuration discovery
# ---------------------------------------------------------------------------

def inspect_file_groups(
    dw_files: list[Path],
    raml_files: list[Path],
    api_candidates: list[Path],
    property_files: list[Path],
    java_files: list[Path],
) -> dict:
    return {
        "dataWeave": {
            "count": len(dw_files),
            "files": [
                relative_path(path)
                for path in dw_files
            ],
        },
        "raml": {
            "count": len(raml_files),
            "files": [
                relative_path(path)
                for path in raml_files
            ],
        },
        "apiSpecificationCandidates": {
            "count": len(api_candidates),
            "files": [
                relative_path(path)
                for path in api_candidates
            ],
        },
        "properties": {
            "count": len(property_files),
            "files": [
                relative_path(path)
                for path in property_files
            ],
        },
        "java": {
            "count": len(java_files),
            "files": [
                relative_path(path)
                for path in java_files
            ],
        },
    }


def inspect_deployment_files(
    application_root: Optional[Path],
) -> list[str]:
    if application_root is None:
        return []

    results: list[str] = []

    for path in application_root.rglob("*"):
        if not path.is_file():
            continue

        if should_ignore(path):
            continue

        if path.name.lower() in {
            name.lower()
            for name in DEPLOYMENT_FILE_NAMES
        }:
            results.append(
                relative_path(path)
            )

    return sorted(set(results))


# ---------------------------------------------------------------------------
# Dependency / connector discovery
# ---------------------------------------------------------------------------

def inspect_connectors(
    application_root: Optional[Path],
) -> list[str]:
    if application_root is None:
        return []

    pom = application_root / "pom.xml"

    if not pom.exists():
        return []

    text = safe_read(pom)

    connector_patterns = {
        "HTTP": r"(?:http-connector|mule-http-connector)",
        "Database": r"(?:mule-db-connector|database-connector)",
        "JMS": r"(?:mule-jms-connector|jms-connector)",
        "AMQP": r"(?:mule-amqp-connector|amqp-connector)",
        "Kafka": r"(?:mule-kafka-connector|kafka-connector)",
        "Salesforce": r"(?:mule-salesforce-connector|salesforce-connector)",
        "SFTP": r"(?:mule-sftp-connector|sftp-connector)",
        "FTP": r"(?:mule-ftp-connector|ftp-connector)",
        "VM": r"(?:mule-vm-connector|vm-connector)",
        "Object Store": r"(?:object-store|objectstore)",
        "MUnit": r"(?:munit-runner|munit-tools)",
    }

    found: list[str] = []

    for name, pattern in connector_patterns.items():
        if re.search(
            pattern,
            text,
            re.IGNORECASE,
        ):
            found.append(name)

    return sorted(found)


# ---------------------------------------------------------------------------
# Flow inventory
# ---------------------------------------------------------------------------

def inspect_flow_inventory(
    xml_files: list[Path],
) -> dict:
    flows: list[dict] = []

    flow_pattern = re.compile(
        r"<flow\b[^>]*\bname\s*=\s*['\"]([^'\"]+)['\"]",
        re.IGNORECASE,
    )

    subflow_pattern = re.compile(
        r"<sub-flow\b[^>]*\bname\s*=\s*['\"]([^'\"]+)['\"]",
        re.IGNORECASE,
    )

    for path in xml_files:
        text = safe_read(path)

        for match in flow_pattern.finditer(text):
            flows.append(
                {
                    "type": "flow",
                    "name": match.group(1),
                    "file": relative_path(path),
                }
            )

        for match in subflow_pattern.finditer(text):
            flows.append(
                {
                    "type": "sub-flow",
                    "name": match.group(1),
                    "file": relative_path(path),
                }
            )

    return {
        "count": len(flows),
        "flows": flows,
    }


# ---------------------------------------------------------------------------
# Application structure
# ---------------------------------------------------------------------------

def inspect_application_structure(
    application_root: Optional[Path],
) -> dict:
    if application_root is None:
        return {
            "root": None,
            "srcMain": False,
            "srcMainMule": False,
            "srcTest": False,
            "srcTestMunit": False,
        }

    src = application_root / "src"
    main = src / "main"
    mule = main / "mule"
    test = src / "test"
    munit = test / "munit"

    return {
        "root": relative_path(application_root),
        "srcMain": main.exists(),
        "srcMainMule": mule.exists(),
        "srcTest": test.exists(),
        "srcTestMunit": munit.exists(),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    all_pom_files = sorted(
        path
        for path in iter_files()
        if path.name == "pom.xml"
    )

    # First collect candidate source files from the framework root.
    xml_files = files_with_extensions(
        MULE_XML_EXTENSIONS
    )

    dw_files = files_with_extensions(
        DATAWEAVE_EXTENSIONS
    )

    raml_files = files_with_extensions(
        RAML_EXTENSIONS
    )

    api_candidates = files_with_extensions(
        API_CANDIDATE_EXTENSIONS
    )

    property_files = files_with_extensions(
        PROPERTY_EXTENSIONS
    )

    java_files = files_with_extensions(
        JAVA_EXTENSIONS
    )

    application_root = detect_application_root(
        all_pom_files,
        xml_files,
    )

    # Restrict application-level inventories to the detected application
    # root where possible. This prevents framework files from affecting
    # review conclusions.
    if application_root is not None:
        def under_application(
            path: Path,
        ) -> bool:
            try:
                path.relative_to(application_root)
                return True
            except ValueError:
                return False

        application_xml_files = [
            path
            for path in xml_files
            if under_application(path)
        ]

        application_dw_files = [
            path
            for path in dw_files
            if under_application(path)
        ]

        application_raml_files = [
            path
            for path in raml_files
            if under_application(path)
        ]

        application_api_candidates = [
            path
            for path in api_candidates
            if under_application(path)
        ]

        application_property_files = [
            path
            for path in property_files
            if under_application(path)
        ]

        application_java_files = [
            path
            for path in java_files
            if under_application(path)
        ]

    else:
        application_xml_files = xml_files
        application_dw_files = dw_files
        application_raml_files = raml_files
        application_api_candidates = api_candidates
        application_property_files = property_files
        application_java_files = java_files

    pom = inspect_pom(application_root)

    artifact = inspect_mule_artifact(
        application_root
    )

    mule_xml = inspect_mule_xml(
        application_xml_files
    )

    file_groups = inspect_file_groups(
        application_dw_files,
        application_raml_files,
        application_api_candidates,
        application_property_files,
        application_java_files,
    )

    git = get_git_metadata()

    application_name = (
        artifact.get("name")
        or pom.get("artifactId")
        or (
            application_root.name
            if application_root is not None
            else ROOT.name
        )
    )

    deployment_files = inspect_deployment_files(
        application_root
    )

    connectors = inspect_connectors(
        application_root
    )

    flow_inventory = inspect_flow_inventory(
        application_xml_files
    )

    structure = inspect_application_structure(
        application_root
    )

    features = mule_xml["features"]

    # Deployment model is intentionally conservative. We only classify
    # it when repository evidence exists.
    if deployment_files:
        deployment_model = "Repository deployment configuration identified"
    else:
        deployment_model = "Not Identified"

    # Test detection is based on actual application files, not framework
    # scripts.
    munit_present = bool(
        any(
            "munit" in path.as_posix().lower()
            or "test" in path.as_posix().lower()
            for path in application_xml_files
        )
    )

    result = {
        "generatedAt": utc_now(),
        "sourceReadOnly": True,

        "framework": {
            "root": str(ROOT),
            "executionDirectory": str(EXECUTION_DIR),
            "model": "APPLICATION_ROOT / FRAMEWORK_ROOT",
        },

        "application": {
            "name": application_name,
            "repositoryPath": str(ROOT),
            "applicationRoot": (
                str(application_root)
                if application_root is not None
                else None
            ),
            "relativeApplicationRoot": (
                relative_path(application_root)
                if application_root is not None
                else None
            ),
        },

        "git": git,

        "reviewType": os.environ.get(
            "REVIEW_TYPE",
            "FULL_APPLICATION",
        ),

        "build": pom,

        "muleArtifact": artifact,

        "structure": structure,

        "files": {
            "muleXmlFiles": [
                relative_path(path)
                for path in application_xml_files
            ],
            "dataWeaveFiles": [
                relative_path(path)
                for path in application_dw_files
            ],
            "ramlFiles": [
                relative_path(path)
                for path in application_raml_files
            ],
            "apiSpecificationCandidates": [
                relative_path(path)
                for path in application_api_candidates
            ],
            "propertyFiles": [
                relative_path(path)
                for path in application_property_files
            ],
            "javaFiles": [
                relative_path(path)
                for path in application_java_files
            ],
        },

        "inventory": {
            "muleXml": mule_xml,
            "fileGroups": file_groups,
            "flows": flow_inventory,
            "connectors": connectors,
            "deploymentFiles": deployment_files,
            "munitPresent": munit_present,
        },

        "features": features,

        "applicationSignals": {
            "httpListener": features["httpListener"],
            "httpRequest": features["httpRequest"],
            "database": features["database"],
            "messaging": features["messaging"],
            "scheduler": features["scheduler"],
            "batch": features["batch"],
            "objectStore": features["objectStore"],
            "salesforce": features["salesforce"],
            "dataWeave": bool(application_dw_files),
            "raml": bool(application_raml_files),
            "apiSpecification": bool(
                application_api_candidates
            ),
            "properties": bool(
                application_property_files
            ),
            "munit": munit_present,
            "deploymentConfiguration": bool(
                deployment_files
            ),
        },

        "counts": {
            "muleXml": len(application_xml_files),
            "dataWeave": len(application_dw_files),
            "raml": len(application_raml_files),
            "apiSpecificationCandidates": len(
                application_api_candidates
            ),
            "properties": len(application_property_files),
            "java": len(application_java_files),
            "flows": flow_inventory["count"],
            "connectors": len(connectors),
            "deploymentFiles": len(deployment_files),
        },
    }

    OUTPUT_FILE.write_text(
        json.dumps(
            result,
            indent=2,
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    print(
        f"Discovery written to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()