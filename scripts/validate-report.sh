#!/usr/bin/env bash

set -Eeuo pipefail

echo "============================================================"
echo " MuleSoft Report Validation"
echo "============================================================"

WORKSPACE="${GITHUB_WORKSPACE:-$(pwd)}"
REPORT_DIR="${WORKSPACE}/reports"

echo "Workspace: ${WORKSPACE}"
echo "Reports  : ${REPORT_DIR}"

if [[ ! -d "${REPORT_DIR}" ]]; then
    echo "ERROR: Report directory does not exist:"
    echo "${REPORT_DIR}"
    exit 1
fi

mapfile -t REPORTS < <(
    find "${REPORT_DIR}" \
        -maxdepth 1 \
        -type f \
        -name 'mulesoft-standards-review_*.docx' \
        -print \
        | sort
)

if [[ "${#REPORTS[@]}" -eq 0 ]]; then
    echo "ERROR: No MuleSoft review DOCX was found."
    exit 1
fi

if [[ "${#REPORTS[@]}" -gt 1 ]]; then
    echo "WARNING: Multiple review reports found:"
    printf '%s\n' "${REPORTS[@]}"

    REPORT_FILE="${REPORTS[-1]}"
else
    REPORT_FILE="${REPORTS[0]}"
fi

echo ""
echo "Validating:"
echo "${REPORT_FILE}"

if [[ ! -f "${REPORT_FILE}" ]]; then
    echo "ERROR: Report does not exist."
    exit 1
fi

if [[ ! -s "${REPORT_FILE}" ]]; then
    echo "ERROR: Report is empty."
    exit 1
fi

echo ""
echo "Checking DOCX file signature..."

FILE_SIGNATURE="$(xxd -p -l 4 "${REPORT_FILE}")"

if [[ "${FILE_SIGNATURE}" != "504b0304" ]]; then
    echo "ERROR: File does not appear to be a valid DOCX/ZIP package."
    echo "Signature: ${FILE_SIGNATURE}"
    exit 1
fi

echo "DOCX signature: OK"

echo ""
echo "Checking DOCX package..."

TEMP_DIR="$(mktemp -d)"

cleanup() {
    rm -rf "${TEMP_DIR}"
}

trap cleanup EXIT

if ! unzip -t "${REPORT_FILE}" > "${TEMP_DIR}/unzip-test.log" 2>&1; then
    echo "ERROR: DOCX package is corrupted."
    cat "${TEMP_DIR}/unzip-test.log"
    exit 1
fi

echo "DOCX package: OK"

echo ""
echo "Extracting document text..."

unzip -q "${REPORT_FILE}" -d "${TEMP_DIR}/docx"

DOCUMENT_XML="${TEMP_DIR}/docx/word/document.xml"

if [[ ! -f "${DOCUMENT_XML}" ]]; then
    echo "ERROR: Word document.xml is missing."
    exit 1
fi

TEXT_FILE="${TEMP_DIR}/document-text.txt"

sed \
    -e 's/<[^>]*>/ /g' \
    -e 's/&amp;/\&/g' \
    -e 's/&lt;/</g' \
    -e 's/&gt;/>/g' \
    "${DOCUMENT_XML}" \
    > "${TEXT_FILE}"

echo ""
echo "Checking required report content..."

REQUIRED_CONTENT=(
    "Executive Summary"
    "Architecture"
    "Finding"
    "Recommendation"
    "Solution"
)

for required in "${REQUIRED_CONTENT[@]}"; do
    if ! grep -qi "${required}" "${TEXT_FILE}"; then
        echo "ERROR: Required content was not found:"
        echo "${required}"
        exit 1
    fi

    echo "OK: ${required}"
done

echo ""
echo "Checking for obvious secret exposure..."

SECRET_PATTERNS=(
    'password[[:space:]]*[:=][[:space:]]*[^[:space:]]+'
    'client_secret[[:space:]]*[:=][[:space:]]*[^[:space:]]+'
    'access_token[[:space:]]*[:=][[:space:]]*[^[:space:]]+'
    'refresh_token[[:space:]]*[:=][[:space:]]*[^[:space:]]+'
    'api[_-]?key[[:space:]]*[:=][[:space:]]*[^[:space:]]+'
)

for pattern in "${SECRET_PATTERNS[@]}"; do
    if grep -Eqi "${pattern}" "${TEXT_FILE}"; then
        echo "ERROR: Potential secret exposure detected in report."
        exit 1
    fi
done

echo "Secret exposure scan: OK"

echo ""
echo "Checking filename..."

BASENAME="$(basename "${REPORT_FILE}")"

if [[ ! "${BASENAME}" =~ ^mulesoft-standards-review_[0-9]{8}_[0-9]{6}\.docx$ ]]; then
    echo "ERROR: Invalid report filename:"
    echo "${BASENAME}"
    exit 1
fi

echo "Filename: OK"

echo ""
echo "Checking file size..."

FILE_SIZE="$(stat -c '%s' "${REPORT_FILE}")"

if [[ "${FILE_SIZE}" -lt 1000 ]]; then
    echo "ERROR: Report is suspiciously small:"
    echo "${FILE_SIZE} bytes"
    exit 1
fi

echo "Report size: ${FILE_SIZE} bytes"

echo ""
echo "============================================================"
echo " Report validation successful"
echo "============================================================"

echo ""
echo "Validated report:"
echo "${REPORT_FILE}"

echo ""
echo "Download full report: ${REPORT_FILE}"