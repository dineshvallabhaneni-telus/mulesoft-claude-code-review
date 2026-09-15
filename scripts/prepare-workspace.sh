#!/usr/bin/env bash

set -Eeuo pipefail

echo "============================================================"
echo " MuleSoft Code Review - Workspace Preparation"
echo "============================================================"

WORKSPACE="${GITHUB_WORKSPACE:-$(pwd)}"
FRAMEWORK_DIR="${WORKSPACE}/code-review"
REPORT_DIR="${WORKSPACE}/reports"

echo "Workspace : ${WORKSPACE}"
echo "Framework : ${FRAMEWORK_DIR}"
echo "Reports   : ${REPORT_DIR}"

mkdir -p "${REPORT_DIR}"

echo ""
echo "Checking required application files..."

if [[ ! -f "${WORKSPACE}/pom.xml" ]]; then
    echo "WARNING: pom.xml was not found."
fi

if [[ ! -f "${WORKSPACE}/mule-artifact.json" ]]; then
    echo "WARNING: mule-artifact.json was not found."
fi

if [[ ! -d "${WORKSPACE}/src" ]]; then
    echo "WARNING: src directory was not found."
fi

echo ""
echo "Checking code-review framework..."

if [[ ! -d "${FRAMEWORK_DIR}" ]]; then
    echo "ERROR: code-review framework directory does not exist:"
    echo "${FRAMEWORK_DIR}"
    exit 1
fi

REQUIRED_FILES=(
    "${FRAMEWORK_DIR}/CLAUDE.md"
    "${FRAMEWORK_DIR}/prompts/mulesoft-review.md"
    "${FRAMEWORK_DIR}/config/review-config.yaml"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [[ ! -f "${file}" ]]; then
        echo "ERROR: Required framework file is missing:"
        echo "${file}"
        exit 1
    fi
done

echo ""
echo "Checking review directories..."

mkdir -p "${REPORT_DIR}"

echo ""
echo "Workspace preparation completed successfully."
echo ""

echo "Application root:"
find "${WORKSPACE}" \
    -maxdepth 2 \
    -type f \
    ! -path "${FRAMEWORK_DIR}/*" \
    ! -path "${REPORT_DIR}/*" \
    | sort \
    | head -100 || true

echo ""
echo "Framework root:"
find "${FRAMEWORK_DIR}" \
    -maxdepth 2 \
    -type f \
    | sort \
    | head -100 || true

echo ""
echo "Report directory:"
ls -la "${REPORT_DIR}" || true

echo ""
echo "Workspace is ready for Claude review."