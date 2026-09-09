#!/usr/bin/env python3
"""PHASE 20 - Consolidated Microsoft Word code review report.

Consumes the structured review evidence authored by Claude in PHASE 19 and
renders a single professional .docx:

    <findings JSON>   (written by Claude, see references/review-report-schema.md)

Report structure follows .claude/skills/mule-code-review/references/
review-report-schema.md.

Usage:
    python3 scripts/generate_report.py \
        --input  review-findings.json \
        --app    "order-experience-api" \
        --repo   "org/order-experience-api" \
        --branch "main" \
        --commit "0b058e7"

That writes one document per run:

    reports/CODE_REVIEW_REPORT_20260909-084530.docx

Use `--output-dir` to change the directory, `--name-prefix` to change the
filename prefix, or `--output` to set an explicit path (which bypasses the
timestamped naming). `--input -` reads the JSON from stdin.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime


def _ensure_python_docx() -> None:
    """Import python-docx, installing it on first use if necessary."""
    try:
        import docx  # noqa: F401
        return
    except ImportError:
        pass

    for extra in ([], ["--user"], ["--break-system-packages"]):
        cmd = [sys.executable, "-m", "pip", "install", "--quiet",
               "--disable-pip-version-check", *extra, "python-docx"]
        if subprocess.call(cmd) == 0:
            break

    try:
        import docx  # noqa: F401
    except ImportError:
        sys.exit("ERROR: python-docx is required. Install it with: "
                 "python3 -m pip install python-docx")


_ensure_python_docx()

from docx import Document  # noqa: E402
from docx.enum.table import WD_TABLE_ALIGNMENT  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Inches, Pt, RGBColor  # noqa: E402

# --------------------------------------------------------------------------
# Palette
# --------------------------------------------------------------------------

STATUS_COLOURS = {
    # Finding severity and overall risk.
    "CRITICAL": "FFC7CE", "HIGH": "FFC7CE", "MEDIUM": "FFE0B2",
    "LOW": "FFF2CC", "NIT": "E7E6E6", "NONE": "C6EFCE",
    # Overall recommendation.
    "APPROVE": "C6EFCE", "APPROVE WITH MINOR CHANGES": "C6EFCE",
    "CHANGES REQUIRED": "FFE0B2", "HIGH RISK": "FFC7CE",
    # Assessment ratings and production-readiness dimensions.
    "STRONG": "C6EFCE", "ADEQUATE": "FFF2CC", "WEAK": "FFE0B2",
    "INADEQUATE": "FFC7CE", "NOT ASSESSED": "E7E6E6",
    "READY": "C6EFCE", "PARTIAL": "FFE0B2", "NOT READY": "FFC7CE",
    "NOT APPLICABLE": "E7E6E6",
}

# Confidence deliberately does not share the severity map: a HIGH-confidence
# finding is well evidenced, not dangerous, and must not be shaded red.
CONFIDENCE_COLOURS = {
    "HIGH": "C6EFCE", "MEDIUM": "FFF2CC", "LOW": "FFE0B2",
}

HEADER_FILL = "1F3864"
ACCENT = RGBColor(0x1F, 0x38, 0x64)
MUTED = RGBColor(0x59, 0x59, 0x59)
DANGER = RGBColor(0xC0, 0x00, 0x00)
GOOD = RGBColor(0x1E, 0x71, 0x45)
WARN = RGBColor(0xB2, 0x6B, 0x00)

SEVERITIES = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "NIT"]
RISKS = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
RECOMMENDATIONS = ["APPROVE", "APPROVE WITH MINOR CHANGES",
                   "CHANGES REQUIRED", "HIGH RISK"]

# Section 4 renders one numbered subsection per area, in this order, whether
# or not the JSON supplies it. A missing area is reported as NOT ASSESSED
# rather than silently dropped.
ASSESSMENT_AREAS = [
    ("security", "Security"),
    ("architecture", "Mule Architecture"),
    ("muleXml", "Mule XML"),
    ("errorHandling", "Error Handling"),
    ("dataweave", "DataWeave"),
    ("api", "API"),
    ("connectors", "Connectors"),
    ("database", "Database"),
    ("messaging", "Messaging"),
    ("performance", "Performance"),
    ("logging", "Logging and Observability"),
    ("munit", "MUnit"),
    ("maven", "Maven and Dependencies"),
    ("configuration", "Configuration"),
    ("maintainability", "Maintainability"),
]

READINESS_DIMENSIONS = [
    ("security", "Security"),
    ("reliability", "Reliability"),
    ("errorRecovery", "Error Recovery"),
    ("idempotency", "Idempotency"),
    ("observability", "Observability"),
    ("performance", "Performance"),
    ("scalability", "Scalability"),
    ("configuration", "Configuration"),
    ("testing", "Testing"),
    ("operationalSupport", "Operational Support"),
]

DEFAULT_OUTPUT_DIR = "reports"
DEFAULT_NAME_PREFIX = "CODE_REVIEW_REPORT"
FILENAME_STAMP_FORMAT = "%Y%m%d-%H%M%S"


# --------------------------------------------------------------------------
# docx helpers
# --------------------------------------------------------------------------

def shade(cell, hex_fill: str) -> None:
    element = OxmlElement("w:shd")
    element.set(qn("w:val"), "clear")
    element.set(qn("w:fill"), hex_fill)
    cell._tc.get_or_add_tcPr().append(element)


def add_runs(paragraph, text: str, *, size: int = 10, bold: bool = False,
             colour: RGBColor | None = None) -> None:
    """Add text, honouring `**bold**` and `` `code` `` inline markup.

    Review prose routinely names files, flows and XML elements in backticks,
    so rendering that markup keeps the narrative readable in Word.
    """
    import re

    pattern = re.compile(r"(\*\*[^*]+\*\*)|(`[^`]+`)")
    cursor = 0
    for match in pattern.finditer(text):
        if match.start() > cursor:
            run = paragraph.add_run(text[cursor:match.start()])
            run.bold = bold
            run.font.size = Pt(size)
            run.font.name = "Calibri"
            if colour is not None:
                run.font.color.rgb = colour
        if match.group(1):
            run = paragraph.add_run(match.group(1)[2:-2])
            run.bold = True
            run.font.size = Pt(size)
            run.font.name = "Calibri"
            if colour is not None:
                run.font.color.rgb = colour
        else:
            run = paragraph.add_run(match.group(2)[1:-1])
            run.bold = bold
            run.font.size = Pt(size - 0.5)
            run.font.name = "Consolas"
            if colour is not None:
                run.font.color.rgb = colour
        cursor = match.end()
    if cursor < len(text):
        run = paragraph.add_run(text[cursor:])
        run.bold = bold
        run.font.size = Pt(size)
        run.font.name = "Calibri"
        if colour is not None:
            run.font.color.rgb = colour


def style_cell(cell, text, *, bold: bool = False, size: int = 9,
               colour: RGBColor | None = None, mono: bool = False,
               markup: bool = False) -> None:
    cell.text = ""
    paragraph = cell.paragraphs[0]
    paragraph.paragraph_format.space_before = Pt(1)
    paragraph.paragraph_format.space_after = Pt(1)
    value = str(text) if text not in (None, "") else "-"
    if markup and not mono:
        add_runs(paragraph, value, size=size, bold=bold, colour=colour)
        return
    run = paragraph.add_run(value)
    run.bold = bold
    run.font.size = Pt(size)
    run.font.name = "Consolas" if mono else "Calibri"
    if colour is not None:
        run.font.color.rgb = colour


def add_table(document, headers: list[str], widths: list[float] | None = None):
    table = document.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    for index, header in enumerate(headers):
        cell = table.rows[0].cells[index]
        style_cell(cell, header, bold=True, size=9,
                   colour=RGBColor(0xFF, 0xFF, 0xFF))
        shade(cell, HEADER_FILL)
    _repeat_header(table.rows[0])
    if widths:
        for row in table.rows:
            for index, width in enumerate(widths):
                row.cells[index].width = Inches(width)
    return table


def add_row(table, values: list, widths: list[float] | None = None,
            status_column: int | None = None, mono_columns: tuple[int, ...] = (),
            markup_columns: tuple[int, ...] = (),
            fill_map: dict[str, str] | None = None):
    cells = table.add_row().cells
    for index, value in enumerate(values):
        style_cell(cells[index], value, size=9, mono=index in mono_columns,
                   markup=index in markup_columns)
        if status_column is not None and index == status_column:
            fill = (fill_map or STATUS_COLOURS).get(str(value).upper())
            if fill:
                shade(cells[index], fill)
                cells[index].paragraphs[0].runs[0].bold = True
    if widths:
        for index, width in enumerate(widths):
            cells[index].width = Inches(width)
    return cells


def _repeat_header(row) -> None:
    """Repeat the header row when a table spans a page break."""
    tr_pr = row._tr.get_or_add_trPr()
    element = OxmlElement("w:tblHeader")
    element.set(qn("w:val"), "true")
    tr_pr.append(element)


def kv_table(document, pairs: list[tuple[str, object]],
             widths: tuple[float, float] = (2.1, 4.4),
             status_keys: tuple[str, ...] = ()):
    table = add_table(document, ["Attribute", "Value"], list(widths))
    for key, value in pairs:
        cells = add_row(table, [key, value], list(widths),
                        status_column=1 if key in status_keys else None)
        cells[0].paragraphs[0].runs[0].bold = True
    document.add_paragraph()
    return table


def bullets(document, items: list, empty: str = "None identified.") -> None:
    if not items:
        para = document.add_paragraph(empty)
        para.runs[0].italic = True
        para.runs[0].font.color.rgb = MUTED
        return
    for item in items:
        para = document.add_paragraph(style="List Bullet")
        add_runs(para, str(item), size=10)


def code_block(document, text: str, max_lines: int = 40) -> None:
    lines = str(text).splitlines()
    truncated = len(lines) > max_lines
    body = "\n".join(lines[:max_lines])
    if truncated:
        body += f"\n... {len(lines) - max_lines} further lines omitted ..."
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.left_indent = Inches(0.25)
    paragraph.paragraph_format.space_after = Pt(6)
    run = paragraph.add_run(body)
    run.font.name = "Consolas"
    run.font.size = Pt(7.5)


def heading(document, text: str, level: int = 1):
    head = document.add_heading(text, level=level)
    for run in head.runs:
        run.font.color.rgb = ACCENT
    return head


def narrative(document, text: str, empty: str = "") -> None:
    if not text:
        if empty:
            para = document.add_paragraph(empty)
            para.runs[0].italic = True
            para.runs[0].font.color.rgb = MUTED
        return
    for block in str(text).split("\n\n"):
        if block.strip():
            add_runs(document.add_paragraph(), block.strip(), size=10)


def status_paragraph(document, label: str, value: str) -> None:
    paragraph = document.add_paragraph()
    run = paragraph.add_run(f"{label}: ")
    run.bold = True
    run.font.size = Pt(12)
    value_run = paragraph.add_run(str(value))
    value_run.bold = True
    value_run.font.size = Pt(12)
    upper = str(value).upper()
    if upper in ("CRITICAL", "HIGH", "HIGH RISK", "INADEQUATE", "NOT READY"):
        value_run.font.color.rgb = DANGER
    elif upper in ("LOW", "NONE", "APPROVE", "APPROVE WITH MINOR CHANGES",
                   "STRONG", "READY"):
        value_run.font.color.rgb = GOOD
    else:
        value_run.font.color.rgb = WARN


# --------------------------------------------------------------------------
# Data loading and reconciliation
# --------------------------------------------------------------------------

def load_findings(raw: str) -> dict:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        sys.exit(f"ERROR: review evidence is not valid JSON: {exc}")
    if not isinstance(data, dict):
        sys.exit("ERROR: review evidence must be a JSON object.")
    return data


def severity_counts(findings: list[dict]) -> dict[str, int]:
    counts = {severity: 0 for severity in SEVERITIES}
    for finding in findings:
        severity = str(finding.get("severity", "")).upper().strip()
        if severity in counts:
            counts[severity] += 1
    return counts


def category_counts(findings: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for finding in findings:
        category = str(finding.get("category", "UNCATEGORISED")).upper().strip()
        counts[category] = counts.get(category, 0) + 1
    return dict(sorted(counts.items()))


def derive_overall_risk(counts: dict[str, int], stated: str) -> str:
    """Overall risk, preferring Claude's judgement but never understating it."""
    if counts["CRITICAL"]:
        floor = "CRITICAL"
    elif counts["HIGH"]:
        floor = "HIGH"
    elif counts["MEDIUM"]:
        floor = "MEDIUM"
    else:
        floor = "LOW"
    stated = str(stated).upper().strip()
    if stated in RISKS and RISKS.index(stated) < RISKS.index(floor):
        return stated
    return floor


def derive_recommendation(counts: dict[str, int], stated: str) -> str:
    """Overall recommendation, floored by the evidence in the findings."""
    if counts["CRITICAL"]:
        floor = "HIGH RISK"
    elif counts["HIGH"] or counts["MEDIUM"]:
        floor = "CHANGES REQUIRED"
    elif counts["LOW"] or counts["NIT"]:
        floor = "APPROVE WITH MINOR CHANGES"
    else:
        floor = "APPROVE"
    stated = str(stated).upper().strip()
    if stated in RECOMMENDATIONS and \
            RECOMMENDATIONS.index(stated) > RECOMMENDATIONS.index(floor):
        return stated
    return floor


def sort_findings(findings: list[dict]) -> list[dict]:
    def key(finding):
        severity = str(finding.get("severity", "")).upper().strip()
        rank = SEVERITIES.index(severity) if severity in SEVERITIES else len(SEVERITIES)
        return (rank, str(finding.get("id", "")))
    return sorted(findings, key=key)


# --------------------------------------------------------------------------
# Sections
# --------------------------------------------------------------------------

def cover_page(document, meta, data, counts, risk, recommendation) -> None:
    for _ in range(4):
        document.add_paragraph()

    title = document.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run(meta["app"] or "MuleSoft Application")
    run.bold = True
    run.font.size = Pt(26)
    run.font.color.rgb = ACCENT

    subtitle = document.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run("MuleSoft Full Application Code Review Report")
    run.font.size = Pt(15)
    run.font.color.rgb = MUTED

    document.add_paragraph()
    application = data.get("application", {})
    table = add_table(document, ["Attribute", "Value"], [2.3, 4.0])
    rows = [
        ("Application", meta["app"] or "(not identified)"),
        ("Repository", meta["repo"] or "(not supplied)"),
        ("Branch", meta["branch"] or "(not supplied)"),
        ("Commit", meta["commit"] or "(not supplied)"),
        ("Mule Runtime", application.get("muleRuntime") or "Not identified"),
        ("Java Version", application.get("javaVersion") or "Not identified"),
        ("Review Type", meta["review_type"]),
        ("Report Generated", meta["generated"]),
        ("Total Findings", sum(counts.values())),
        ("Overall Risk", risk),
        ("Overall Recommendation", recommendation),
    ]
    for key, value in rows:
        cells = add_row(table, [key, value], [2.3, 4.0],
                        status_column=1 if key in ("Overall Risk",
                                                   "Overall Recommendation") else None)
        cells[0].paragraphs[0].runs[0].bold = True

    document.add_paragraph()
    note = document.add_paragraph()
    note.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = note.add_run(meta["footnote"])
    run.italic = True
    run.font.size = Pt(9)
    run.font.color.rgb = MUTED
    document.add_page_break()


def add_toc(document) -> None:
    head = document.add_paragraph()
    run = head.add_run("Contents")
    run.bold = True
    run.font.size = Pt(16)
    run.font.color.rgb = ACCENT

    paragraph = document.add_paragraph()
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    begin.set(qn("w:dirty"), "true")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = r'TOC \o "1-2" \h \z \u'
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = "Open in Word and press F9 (or Update Table) to build the contents."
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for element in (begin, instr, separate, text, end):
        run._r.append(element)
    for existing in paragraph.runs:
        existing.font.size = Pt(10)
        existing.font.color.rgb = MUTED
    document.add_page_break()


def section_summary(document, data, counts, risk, recommendation) -> None:
    heading(document, "1. Executive Summary", 1)

    status_paragraph(document, "Overall Risk", risk)
    status_paragraph(document, "Overall Recommendation", recommendation)
    document.add_paragraph()

    narrative(document, data.get("executiveSummary"),
              "No executive summary was recorded by the review.")
    document.add_paragraph()

    heading(document, "1.1 Review Scope", 2)
    scope = data.get("scope", {}) or {}
    narrative(document, scope.get("statement"))
    if scope.get("included"):
        para = document.add_paragraph()
        run = para.add_run("In scope")
        run.bold = True
        run.font.size = Pt(10)
        bullets(document, scope["included"])
    if scope.get("excluded"):
        para = document.add_paragraph()
        run = para.add_run("Out of scope")
        run.bold = True
        run.font.size = Pt(10)
        bullets(document, scope["excluded"])
    if not (scope.get("statement") or scope.get("included") or scope.get("excluded")):
        bullets(document, [], "No review scope was recorded.")
    document.add_paragraph()

    heading(document, "1.2 Review Methodology", 2)
    bullets(document, data.get("methodology", []),
            "No review methodology was recorded.")
    document.add_paragraph()

    heading(document, "1.3 Findings by Severity", 2)
    table = add_table(document, ["Severity", "Count"], [3.6, 1.6])
    for severity in SEVERITIES:
        cells = add_row(table, [severity, counts[severity]], [3.6, 1.6],
                        status_column=0)
        cells[1].paragraphs[0].runs[0].bold = True
    cells = add_row(table, ["TOTAL", sum(counts.values())], [3.6, 1.6])
    cells[0].paragraphs[0].runs[0].bold = True
    cells[1].paragraphs[0].runs[0].bold = True
    document.add_paragraph()

    heading(document, "1.4 Findings by Category", 2)
    by_category = category_counts(data.get("findings", []))
    if by_category:
        table = add_table(document, ["Category", "Findings"], [3.6, 1.6])
        for category, count in by_category.items():
            add_row(table, [category, count], [3.6, 1.6])
    else:
        bullets(document, [], "No findings were recorded, so no categories apply.")
    document.add_page_break()


def section_inventory(document, data) -> None:
    heading(document, "2. Application Inventory", 1)

    inventory = data.get("inventory", [])
    if inventory:
        table = add_table(document, ["Area", "Inventory"], [1.9, 4.6])
        for entry in inventory:
            cells = add_row(table, [entry.get("area", "-"),
                                    entry.get("inventory", "Not identified")],
                            [1.9, 4.6], markup_columns=(1,))
            cells[0].paragraphs[0].runs[0].bold = True
    else:
        bullets(document, [], "No application inventory was recorded.")
    document.add_paragraph()

    heading(document, "2.1 Technology Stack", 2)
    stack = data.get("technologyStack", [])
    if stack:
        table = add_table(document, ["Component", "Version", "Evidence", "Notes"],
                          [1.7, 1.0, 1.9, 1.9])
        for item in stack:
            add_row(table, [item.get("component", "-"), item.get("version", "-"),
                            item.get("source", "-"), item.get("notes", "-")],
                    [1.7, 1.0, 1.9, 1.9], mono_columns=(2,))
    else:
        bullets(document, [], "No technology stack detail was recorded.")
    document.add_paragraph()

    heading(document, "2.2 Architecture Summary", 2)
    narrative(document, data.get("architectureSummary"),
              "No architecture summary was recorded.")
    document.add_paragraph()

    heading(document, "2.3 Integration Inventory", 2)
    integrations = data.get("integrations", [])
    if integrations:
        table = add_table(document,
                          ["Source", "Target", "Mechanism", "Mode", "Retry",
                           "Transaction", "Risk"],
                          [1.0, 1.0, 1.2, 0.7, 0.7, 1.0, 0.9])
        for row in integrations:
            add_row(table, [row.get("source", "-"), row.get("target", "-"),
                            row.get("mechanism", "-"), row.get("mode", "-"),
                            row.get("retry", "-"), row.get("transaction", "-"),
                            str(row.get("risk", "-")).upper()],
                    [1.0, 1.0, 1.2, 0.7, 0.7, 1.0, 0.9], status_column=6)
    else:
        bullets(document, [], "No integration boundaries were identified.")
    document.add_page_break()


def render_finding(document, finding) -> None:
    severity = str(finding.get("severity", "")).upper().strip() or "UNSPECIFIED"
    head = document.add_heading(
        f"{finding.get('id', 'UNKNOWN')} - {finding.get('title', 'Untitled finding')}",
        level=3)
    for run in head.runs:
        run.font.size = Pt(11)
        run.font.color.rgb = DANGER if severity in ("CRITICAL", "HIGH") else ACCENT

    table = add_table(document, ["Attribute", "Value"], [1.5, 5.0])
    for key, value in [
        ("Finding ID", finding.get("id", "-")),
        ("Severity", severity),
        ("Category", str(finding.get("category", "-")).upper()),
        ("File", finding.get("file", "-")),
        ("Location", finding.get("location", "-")),
        ("Confidence", str(finding.get("confidence", "-")).upper()),
    ]:
        cells = add_row(
            table, [key, value], [1.5, 5.0],
            status_column=1 if key in ("Severity", "Confidence") else None,
            mono_columns=(1,) if key == "File" else (),
            fill_map=CONFIDENCE_COLOURS if key == "Confidence" else None)
        cells[0].paragraphs[0].runs[0].bold = True
    document.add_paragraph()

    for label, key in [("Problem", "problem"), ("Evidence", "evidence"),
                       ("Impact", "impact"), ("Recommendation", "recommendation")]:
        caption = document.add_paragraph()
        run = caption.add_run(label)
        run.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = ACCENT
        narrative(document, finding.get(key), f"No {label.lower()} was recorded.")
        if label == "Evidence" and finding.get("evidenceSnippet"):
            code_block(document, finding["evidenceSnippet"])
    document.add_paragraph()


def section_findings(document, data) -> None:
    heading(document, "3. Findings", 1)

    findings = data.get("findings", [])
    if not findings:
        para = document.add_paragraph(
            "No material findings were identified based on the repository "
            "evidence reviewed. Review coverage, positive observations, risk "
            "assessment and limitations are reported in the sections that follow."
        )
        para.runs[0].bold = True

    for index, severity in enumerate(SEVERITIES, start=1):
        bucket = [f for f in findings
                  if str(f.get("severity", "")).upper().strip() == severity]
        heading(document, f"3.{index} {severity.title()} Findings", 2)
        if not bucket:
            bullets(document, [], f"No {severity} findings were identified.")
            document.add_paragraph()
            continue
        for finding in sorted(bucket, key=lambda f: str(f.get("id", ""))):
            render_finding(document, finding)

    unknown = [f for f in findings
               if str(f.get("severity", "")).upper().strip() not in SEVERITIES]
    if unknown:
        heading(document, "3.6 Findings with an Unrecognised Severity", 2)
        para = document.add_paragraph(
            "These findings did not declare a severity from CRITICAL, HIGH, "
            "MEDIUM, LOW or NIT and are excluded from the severity counts."
        )
        para.runs[0].italic = True
        para.runs[0].font.color.rgb = MUTED
        for finding in unknown:
            render_finding(document, finding)
    document.add_page_break()


def section_assessments(document, data) -> None:
    heading(document, "4. Category Assessments", 1)

    assessments = data.get("assessments", {}) or {}
    for index, (key, label) in enumerate(ASSESSMENT_AREAS, start=1):
        entry = assessments.get(key) or {}
        heading(document, f"4.{index} {label} Assessment", 2)
        rating = str(entry.get("rating", "NOT ASSESSED")).upper().strip() or "NOT ASSESSED"
        kv_table(document, [("Rating", rating)], (1.5, 5.0),
                 status_keys=("Rating",))
        narrative(document, entry.get("summary"),
                  f"No {label} assessment narrative was recorded.")
        if entry.get("observations"):
            para = document.add_paragraph()
            run = para.add_run("Observations")
            run.bold = True
            run.font.size = Pt(10)
            bullets(document, entry["observations"])
        if entry.get("gaps"):
            para = document.add_paragraph()
            run = para.add_run("Gaps")
            run.bold = True
            run.font.size = Pt(10)
            bullets(document, entry["gaps"])
        document.add_paragraph()
    document.add_page_break()


def section_readiness(document, data) -> None:
    heading(document, "5. Production Readiness Assessment", 1)

    readiness = data.get("productionReadiness", {}) or {}
    narrative(document, readiness.get("summary"))

    heading(document, "5.1 Readiness Dimensions", 2)
    dimensions = readiness.get("dimensions", {}) or {}
    table = add_table(document, ["Dimension", "Status", "Notes"], [1.6, 1.1, 3.8])
    for key, label in READINESS_DIMENSIONS:
        entry = dimensions.get(key) or {}
        if isinstance(entry, str):
            entry = {"status": entry}
        cells = add_row(table,
                        [label,
                         str(entry.get("status", "NOT ASSESSED")).upper().strip()
                         or "NOT ASSESSED",
                         entry.get("notes", "-")],
                        [1.6, 1.1, 3.8], status_column=1, markup_columns=(2,))
        cells[0].paragraphs[0].runs[0].bold = True
    document.add_paragraph()

    heading(document, "5.2 Positive Observations", 2)
    positives = data.get("positiveObservations", [])
    if positives:
        table = add_table(document, ["Strength", "Supporting Evidence"], [2.6, 3.9])
        for item in positives:
            if isinstance(item, str):
                item = {"observation": item}
            add_row(table, [item.get("observation", "-"),
                            item.get("evidence", "-")],
                    [2.6, 3.9], markup_columns=(0, 1))
    else:
        bullets(document, [],
                "No evidence-supported strengths were recorded by the review.")
    document.add_page_break()


def section_risk(document, data, counts, risk, recommendation) -> None:
    heading(document, "6. Risk and Recommendation", 1)

    heading(document, "6.1 Risk Summary", 2)
    risks = data.get("riskSummary", [])
    if risks:
        table = add_table(document, ["Risk Area", "Risk", "Severity", "Explanation"],
                          [1.3, 1.6, 0.9, 2.7])
        ordered = sorted(risks, key=lambda r: SEVERITIES.index(
            str(r.get("severity", "")).upper())
            if str(r.get("severity", "")).upper() in SEVERITIES else len(SEVERITIES))
        for item in ordered:
            add_row(table, [item.get("area", "-"), item.get("risk", "-"),
                            str(item.get("severity", "-")).upper(),
                            item.get("explanation", "-")],
                    [1.3, 1.6, 0.9, 2.7], status_column=2, markup_columns=(3,))
    else:
        bullets(document, [], "No risk areas were recorded by the review.")
    document.add_paragraph()

    heading(document, "6.2 Top 10 Remediation Priorities", 2)
    priorities = data.get("remediationPriorities", [])
    if priorities:
        table = add_table(document,
                          ["Priority", "Finding", "Severity", "Recommended Action"],
                          [0.8, 1.0, 0.9, 3.8])
        for item in sorted(priorities, key=lambda p: p.get("priority", 99))[:10]:
            add_row(table, [item.get("priority", "-"), item.get("finding", "-"),
                            str(item.get("severity", "-")).upper(),
                            item.get("action", "-")],
                    [0.8, 1.0, 0.9, 3.8], status_column=2, markup_columns=(3,))
    else:
        bullets(document, [], "No remediation priorities were recorded.")
    document.add_paragraph()

    heading(document, "6.3 Review Limitations", 2)
    bullets(document, data.get("limitations", []),
            "No review limitations were recorded.")
    document.add_paragraph()

    heading(document, "6.4 Overall Risk and Recommendation", 2)
    status_paragraph(document, "Overall Risk", risk)
    status_paragraph(document, "Overall Recommendation", recommendation)
    document.add_paragraph()
    narrative(document, data.get("recommendationRationale"),
              "No recommendation rationale was recorded.")

    stated_risk = str(data.get("overallRisk", "")).upper().strip()
    stated_rec = str(data.get("overallRecommendation", "")).upper().strip()
    if (stated_risk and stated_risk != risk) or (stated_rec and stated_rec != recommendation):
        para = document.add_paragraph()
        run = para.add_run(
            f"Reconciliation: the review stated an overall risk of "
            f"{stated_risk or 'none'} and a recommendation of "
            f"{stated_rec or 'none'}. The finding evidence "
            f"({counts['CRITICAL']} CRITICAL, {counts['HIGH']} HIGH, "
            f"{counts['MEDIUM']} MEDIUM) does not support that, so the report "
            f"records {risk} / {recommendation}."
        )
        run.italic = True
        run.font.size = Pt(9)
        run.font.color.rgb = DANGER
    document.add_page_break()


def appendix_inventory(document, data, counts) -> None:
    heading(document, "Appendix A - Complete Findings Inventory", 1)
    document.add_paragraph(
        "Every finding reported by this review appears below. No finding is "
        "omitted, and these counts reconcile with section 1.3."
    )
    findings = data.get("findings", [])
    if not findings:
        bullets(document, [], "The review reported no findings.")
        document.add_page_break()
        return
    table = add_table(document,
                      ["ID", "Severity", "Category", "Confidence", "Title", "Location"],
                      [0.8, 0.8, 1.0, 0.9, 1.9, 1.9])
    for finding in sort_findings(findings):
        add_row(table, [finding.get("id", "-"),
                        str(finding.get("severity", "-")).upper(),
                        str(finding.get("category", "-")).upper(),
                        str(finding.get("confidence", "-")).upper(),
                        finding.get("title", "-"),
                        finding.get("file", "-")],
                [0.8, 0.8, 1.0, 0.9, 1.9, 1.9], status_column=1,
                mono_columns=(5,))
    document.add_paragraph()

    para = document.add_paragraph()
    run = para.add_run(
        f"Reconciliation: {len(findings)} findings listed; "
        + ", ".join(f"{counts[s]} {s}" for s in SEVERITIES) + "."
    )
    run.italic = True
    run.font.size = Pt(9)
    run.font.color.rgb = MUTED
    document.add_page_break()


def appendix_evidence(document, data) -> None:
    heading(document, "Appendix B - Finding Evidence Detail", 1)
    findings = [f for f in data.get("findings", []) if f.get("evidenceSnippet")]
    if not findings:
        bullets(document, [],
                "No finding supplied a verbatim repository evidence excerpt.")
        document.add_page_break()
        return
    document.add_paragraph(
        "Verbatim repository excerpts supporting the findings, reproduced so a "
        "reader can confirm each finding without opening the repository."
    )
    for finding in sort_findings(findings):
        head = document.add_heading(
            f"{finding.get('id', 'UNKNOWN')} - {finding.get('file', 'unknown location')}",
            level=2)
        for run in head.runs:
            run.font.size = Pt(10.5)
            run.font.color.rgb = ACCENT
        code_block(document, finding["evidenceSnippet"], max_lines=60)
    document.add_page_break()


def appendix_coverage(document, data, meta) -> None:
    heading(document, "Appendix C - Review Coverage and Boundaries", 1)

    coverage = data.get("coverage", []) or []
    if coverage:
        table = add_table(document, ["Review Phase", "Status", "Notes"],
                          [2.2, 1.0, 3.3])
        for item in coverage:
            cells = add_row(table, [item.get("phase", "-"),
                                    str(item.get("status", "-")).upper(),
                                    item.get("notes", "-")],
                            [2.2, 1.0, 3.3], markup_columns=(2,))
            cells[0].paragraphs[0].runs[0].bold = True
        document.add_paragraph()

    table = add_table(document, ["Control", "Confirmation"], [2.2, 4.3])
    for control, confirmation in [
        ("Review mode", meta["review_type"]),
        ("Source modification",
         "The MuleSoft source was read only and was not modified."),
        ("Git write operations", "None performed by this review."),
        ("Dependency changes", "No dependency was added, removed or upgraded."),
        ("Remediation", "No defect was fixed. This review reports only."),
        ("Files created",
         "One timestamped Word report under the reports directory. Nothing else."),
        ("Generated artifacts",
         "target, .git, IDE metadata and build output were excluded from analysis."),
        ("Evidence basis",
         "Every finding cites a repository file and structural location."),
        ("Unverifiable areas",
         "Recorded as review limitations in section 6.3, never as defects."),
        ("Severity reconciliation",
         "Overall risk and recommendation are floored by the finding evidence."),
    ]:
        cells = add_row(table, [control, confirmation], [2.2, 4.3])
        cells[0].paragraphs[0].runs[0].bold = True
    document.add_paragraph()

    para = document.add_paragraph()
    run = para.add_run(
        "All findings in this report are derived from repository evidence "
        "inspected during the review. Areas that could not be verified are "
        "reported as limitations with the reason recorded, never as defects."
    )
    run.italic = True
    run.font.size = Pt(9)
    run.font.color.rgb = MUTED


# --------------------------------------------------------------------------
# Document assembly
# --------------------------------------------------------------------------

def page_footer(document, text: str) -> None:
    for section in document.sections:
        paragraph = section.footer.paragraphs[0]
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = paragraph.add_run(text)
        run.font.size = Pt(8)
        run.font.color.rgb = MUTED


REQUIRED_SECTIONS = [
    "1. Executive Summary",
    "2. Application Inventory",
    "3. Findings",
    "4. Category Assessments",
    "5. Production Readiness Assessment",
    "6. Risk and Recommendation",
    "Appendix A - Complete Findings Inventory",
    "Appendix B - Finding Evidence Detail",
    "Appendix C - Review Coverage and Boundaries",
]


def parse_args(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(
        description="Generate the consolidated Word code review report.")
    parser.add_argument("--input", "-i", required=True,
                        help="Review findings JSON file, or '-' for stdin.")
    parser.add_argument("--output", "-o", default="",
                        help="Explicit output .docx path. By default the document is named "
                             f"{DEFAULT_NAME_PREFIX}_<YYYYMMDD-HHMMSS>.docx inside --output-dir.")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, dest="output_dir",
                        help=f"Directory for the generated document (default: {DEFAULT_OUTPUT_DIR}). "
                             "Created if it does not exist.")
    parser.add_argument("--name-prefix", default=DEFAULT_NAME_PREFIX, dest="name_prefix",
                        help=f"Filename prefix before the timestamp (default: {DEFAULT_NAME_PREFIX}).")
    parser.add_argument("--app", default="",
                        help="Application name (defaults to application.name in the JSON).")
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", ""),
                        help="Repository name (defaults to $GITHUB_REPOSITORY).")
    parser.add_argument("--branch", default="", help="Branch or ref reviewed.")
    parser.add_argument("--commit", default="", help="Commit SHA reviewed.")
    parser.add_argument("--review-type", default="Full application review (read-only)",
                        dest="review_type", help="Review type shown on the cover.")
    parser.add_argument("--footnote",
                        default="Generated by Claude Code. Findings are evidence-based and "
                                "require engineering validation before remediation.",
                        help="Italic note at the bottom of the cover page.")
    parser.add_argument("--date", default="", help="Override the generated-on timestamp.")
    parser.add_argument("--no-toc", action="store_true",
                        help="Omit the table of contents.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.input == "-":
        raw = sys.stdin.read()
    else:
        if not os.path.isfile(args.input):
            sys.exit(f"ERROR: input file not found: {args.input}")
        with open(args.input, encoding="utf-8") as handle:
            raw = handle.read()

    if not raw.strip():
        sys.exit("ERROR: the review evidence is empty; refusing to write an empty document.")

    data = load_findings(raw)
    findings = data.get("findings", [])
    if not isinstance(findings, list):
        sys.exit("ERROR: 'findings' must be a JSON array.")

    counts = severity_counts(findings)
    risk = derive_overall_risk(counts, data.get("overallRisk", ""))
    recommendation = derive_recommendation(counts, data.get("overallRecommendation", ""))

    now = datetime.now()
    review = data.get("review", {}) or {}
    application = data.get("application", {}) or {}
    meta = {
        "app": args.app or application.get("name", ""),
        "repo": args.repo or review.get("repository", ""),
        "branch": args.branch or review.get("branch", ""),
        "commit": args.commit or review.get("commit", ""),
        "review_type": args.review_type,
        "generated": args.date or now.strftime("%d %b %Y %H:%M:%S"),
        "footnote": args.footnote,
    }

    document = Document()
    normal = document.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(10)
    normal.paragraph_format.space_after = Pt(6)
    for section in document.sections:
        section.left_margin = section.right_margin = Inches(0.9)
        section.top_margin = section.bottom_margin = Inches(0.8)

    cover_page(document, meta, data, counts, risk, recommendation)
    if not args.no_toc:
        add_toc(document)
    section_summary(document, data, counts, risk, recommendation)
    section_inventory(document, data)
    section_findings(document, data)
    section_assessments(document, data)
    section_readiness(document, data)
    section_risk(document, data, counts, risk, recommendation)
    appendix_inventory(document, data, counts)
    appendix_evidence(document, data)
    appendix_coverage(document, data, meta)

    app = meta["app"] or "mulesoft-application"
    page_footer(document, f"{app} - code review report - generated {meta['generated']}")

    stamp = now.strftime(FILENAME_STAMP_FORMAT)
    if args.output:
        out_path = os.path.abspath(args.output)
    else:
        out_path = os.path.abspath(
            os.path.join(args.output_dir, f"{args.name_prefix}_{stamp}.docx"))

    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    document.save(out_path)

    # Validate the written document before declaring success.
    reopened = Document(out_path)
    headings = [p.text for p in reopened.paragraphs
                if p.style.name.startswith("Heading 1")]
    missing = [s for s in REQUIRED_SECTIONS if s not in headings]
    if missing:
        print(f"ERROR: generated report is missing sections: {missing}", file=sys.stderr)
        return 2

    print(f"Report generated: {out_path}")
    print(f"  overall risk         : {risk}")
    print(f"  overall recommendation: {recommendation}")
    print(f"  findings documented  : {len(findings)} "
          f"({', '.join(f'{counts[s]} {s}' for s in SEVERITIES)})")
    print(f"  sections             : {len(headings)} top-level")
    print(f"  size                 : {os.path.getsize(out_path):,} bytes")

    stated_risk = str(data.get("overallRisk", "")).upper().strip()
    stated_rec = str(data.get("overallRecommendation", "")).upper().strip()
    if stated_risk and stated_risk != risk:
        print(f"  NOTE: stated risk {stated_risk} raised to {risk} by the finding evidence.")
    if stated_rec and stated_rec != recommendation:
        print(f"  NOTE: stated recommendation {stated_rec} raised to {recommendation} "
              f"by the finding evidence.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
