#!/usr/bin/env python3
"""Render a MuleSoft code review report (Markdown) as a styled Word document.

Used by `prompts/mule-full-review.md`: the review report is written to a
temporary Markdown file outside the repository, converted here, and only the
resulting .docx is left behind as the review deliverable.

Usage:
    python3 scripts/md_to_docx.py \
        --input  /tmp/mule-review/report.md \
        --output CODE_REVIEW_REPORT.docx \
        --title  "MuleSoft Code Review Report" \
        --app    "order-experience-api" \
        --repo   "org/order-experience-api" \
        --branch "main" \
        --commit "0b058e7"

`--input -` reads Markdown from stdin.

Supported Markdown: ATX headings, paragraphs, bullet/numbered lists (nested),
pipe tables, fenced and indented code blocks, block quotes, horizontal rules,
and inline bold/italic/code/links. Severity keywords (CRITICAL, HIGH, MEDIUM,
LOW, NIT) are colour-coded wherever they appear.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import re
import subprocess
import sys


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
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Inches, Pt, RGBColor  # noqa: E402

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------

INK = RGBColor(0x1A, 0x1A, 0x1A)
MUTED = RGBColor(0x5A, 0x63, 0x6E)
ACCENT = RGBColor(0x1F, 0x4E, 0x79)
ACCENT_LIGHT = RGBColor(0x2E, 0x74, 0xB5)
CODE_INK = RGBColor(0x2B, 0x2B, 0x2B)
RULE = "D5DBE1"
CODE_BG = "F4F6F8"
TABLE_HDR_BG = "1F4E79"
QUOTE_BG = "F7F9FA"

SEVERITY_COLORS = {
    "CRITICAL": RGBColor(0xB3, 0x0C, 0x0C),
    "HIGH": RGBColor(0xC5, 0x50, 0x0C),
    "MEDIUM": RGBColor(0xA0, 0x76, 0x00),
    "LOW": RGBColor(0x1F, 0x6F, 0x8B),
    "NIT": RGBColor(0x6B, 0x72, 0x7B),
}
SEVERITY_RE = re.compile(r"\b(CRITICAL|HIGH|MEDIUM|LOW|NIT)\b")

MONO = "Consolas"
BODY_FONT = "Calibri"

# ---------------------------------------------------------------------------
# Low-level OOXML helpers
# ---------------------------------------------------------------------------


# WordprocessingML requires strict child ordering inside pPr/tcPr/trPr; Word
# reports the document as corrupt otherwise. python-docx deletes its own
# `_tag_seq` after class definition, so the orderings are repeated here.
PPR_SEQ = (
    "w:pStyle", "w:keepNext", "w:keepLines", "w:pageBreakBefore", "w:framePr",
    "w:widowControl", "w:numPr", "w:suppressLineNumbers", "w:pBdr", "w:shd",
    "w:tabs", "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap",
    "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN",
    "w:bidi", "w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind",
    "w:contextualSpacing", "w:mirrorIndents", "w:suppressOverlap", "w:jc",
    "w:textDirection", "w:textAlignment", "w:textboxTightWrap", "w:outlineLvl",
    "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr", "w:pPrChange",
)
TCPR_SEQ = (
    "w:cnfStyle", "w:tcW", "w:gridSpan", "w:hMerge", "w:vMerge", "w:tcBorders",
    "w:shd", "w:noWrap", "w:tcMar", "w:textDirection", "w:tcFitText",
    "w:vAlign", "w:hideMark", "w:headers", "w:cellIns", "w:cellDel",
    "w:cellMerge", "w:tcPrChange",
)
TRPR_SEQ = (
    "w:cnfStyle", "w:divId", "w:gridBefore", "w:gridAfter", "w:wBefore",
    "w:wAfter", "w:cantSplit", "w:trHeight", "w:tblHeader", "w:tblCellSpacing",
    "w:jc", "w:hidden", "w:ins", "w:del", "w:trPrChange",
)
PBDR_SEQ = ("w:top", "w:left", "w:bottom", "w:right", "w:between", "w:bar")


def _insert_ordered(parent, tag: str, sequence: tuple[str, ...], *, reuse=False):
    """Insert (or fetch) `tag` under `parent` at its schema-mandated position."""
    if reuse:
        existing = parent.find(qn(tag))
        if existing is not None:
            return existing
    element = OxmlElement(tag)
    successors = {qn(name) for name in sequence[sequence.index(tag) + 1:]}
    for position, child in enumerate(parent):
        if child.tag in successors:
            parent.insert(position, element)
            return element
    parent.append(element)
    return element


def _shade(element, fill: str) -> None:
    """Apply a solid background fill to a paragraph or table cell."""
    if element.tag == qn("w:p"):
        pr, sequence = element.get_or_add_pPr(), PPR_SEQ
    else:
        pr, sequence = element.get_or_add_tcPr(), TCPR_SEQ
    shd = _insert_ordered(pr, "w:shd", sequence, reuse=True)
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)


def _border(paragraph, edge: str, color: str, size: int = 6) -> None:
    pr = paragraph._p.get_or_add_pPr()
    borders = _insert_ordered(pr, "w:pBdr", PPR_SEQ, reuse=True)
    el = _insert_ordered(borders, f"w:{edge}", PBDR_SEQ, reuse=True)
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), str(size))
    el.set(qn("w:space"), "4")
    el.set(qn("w:color"), color)


def _field(paragraph, instruction: str, placeholder: str = "") -> None:
    """Insert a Word field code (used for the TOC and page numbers)."""
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    begin.set(qn("w:dirty"), "true")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = instruction
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = placeholder
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for el in (begin, instr, separate, text, end):
        run._r.append(el)


def _hyperlink(paragraph, url: str, text: str):
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), r_id)
    run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "2E74B5")
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    rpr.append(color)
    rpr.append(underline)
    run.append(rpr)
    t = OxmlElement("w:t")
    t.set(qn("xml:space"), "preserve")
    t.text = text
    run.append(t)
    link.append(run)
    paragraph._p.append(link)


def _prevent_row_split(row) -> None:
    _insert_ordered(row._tr.get_or_add_trPr(), "w:cantSplit", TRPR_SEQ, reuse=True)


def _repeat_header(row) -> None:
    el = _insert_ordered(row._tr.get_or_add_trPr(), "w:tblHeader", TRPR_SEQ, reuse=True)
    el.set(qn("w:val"), "true")


# ---------------------------------------------------------------------------
# Inline Markdown
# ---------------------------------------------------------------------------

_INLINE_RE = re.compile(
    r"(?P<code>`{1,2}[^`]+?`{1,2})"
    r"|(?P<link>\[[^\]]+\]\([^)\s]+\))"
    r"|(?P<bold>\*\*[^*]+\*\*|__[^_]+__)"
    r"|(?P<italic>\*[^*\n]+\*|(?<![A-Za-z0-9_])_[^_\n]+_(?![A-Za-z0-9_]))"
)


def add_inline(paragraph, text: str, *, base_bold=False, base_italic=False,
               color: RGBColor | None = None, size: Pt | None = None,
               font: str | None = None) -> None:
    """Add `text` to `paragraph`, honouring inline Markdown markup."""

    def style(run, *, bold=False, italic=False, mono=False):
        run.font.name = MONO if mono else (font or BODY_FONT)
        if size is not None:
            run.font.size = size
        run.bold = base_bold or bold
        run.italic = base_italic or italic
        run.font.color.rgb = CODE_INK if mono else (color if color is not None else INK)

    def add_plain(chunk: str) -> None:
        """Emit plain text, colour-coding severity keywords."""
        pos = 0
        for match in SEVERITY_RE.finditer(chunk):
            if match.start() > pos:
                style(paragraph.add_run(chunk[pos:match.start()]))
            run = paragraph.add_run(match.group(0))
            style(run, bold=True)
            run.font.color.rgb = SEVERITY_COLORS[match.group(0)]
            pos = match.end()
        if pos < len(chunk):
            style(paragraph.add_run(chunk[pos:]))

    cursor = 0
    for match in _INLINE_RE.finditer(text):
        if match.start() > cursor:
            add_plain(text[cursor:match.start()])
        cursor = match.end()

        if match.group("code"):
            inner = match.group("code").strip("`")
            run = paragraph.add_run(inner)
            style(run, mono=True)
        elif match.group("link"):
            label, url = re.match(r"\[([^\]]+)\]\(([^)\s]+)\)", match.group("link")).groups()
            if url.startswith(("http://", "https://", "mailto:")):
                _hyperlink(paragraph, url, label)
            else:
                run = paragraph.add_run(label)
                style(run, mono=True)
        elif match.group("bold"):
            run = paragraph.add_run(match.group("bold").strip("*_"))
            style(run, bold=True)
        elif match.group("italic"):
            run = paragraph.add_run(match.group("italic").strip("*_"))
            style(run, italic=True)

    if cursor < len(text):
        add_plain(text[cursor:])


def strip_inline(text: str) -> str:
    """Plain-text form of an inline Markdown string."""
    text = re.sub(r"\[([^\]]+)\]\([^)\s]+\)", r"\1", text)
    text = re.sub(r"`{1,2}([^`]+?)`{1,2}", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*|__([^_]+)__", lambda m: m.group(1) or m.group(2), text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    return text.strip()


# ---------------------------------------------------------------------------
# Block tokenizer
# ---------------------------------------------------------------------------

FENCE_RE = re.compile(r"^\s*(```+|~~~+)\s*([A-Za-z0-9_+-]*)\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
BULLET_RE = re.compile(r"^(\s*)[-*+]\s+(.*)$")
ORDERED_RE = re.compile(r"^(\s*)(\d+)[.)]\s+(.*)$")
RULE_RE = re.compile(r"^\s*([-*_])(\s*\1){2,}\s*$")
QUOTE_RE = re.compile(r"^\s*>\s?(.*)$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{1,}:?\s*(\|\s*:?-{1,}:?\s*)+\|?\s*$")


def tokenize(markdown: str) -> list[dict]:
    lines = markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    tokens: list[dict] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        fence = FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)[0] * 3
            body: list[str] = []
            i += 1
            while i < n and not lines[i].strip().startswith(marker):
                body.append(lines[i])
                i += 1
            i += 1  # closing fence
            tokens.append({"type": "code", "lines": body, "lang": fence.group(2)})
            continue

        heading = HEADING_RE.match(line)
        if heading:
            tokens.append({"type": "heading",
                           "level": len(heading.group(1)),
                           "text": heading.group(2)})
            i += 1
            continue

        if RULE_RE.match(line):
            tokens.append({"type": "rule"})
            i += 1
            continue

        # Pipe table: a header row followed by a separator row.
        if "|" in line and i + 1 < n and TABLE_SEP_RE.match(lines[i + 1]):
            rows = [split_row(line)]
            i += 2
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append(split_row(lines[i]))
                i += 1
            tokens.append({"type": "table", "rows": rows})
            continue

        quote = QUOTE_RE.match(line)
        if quote:
            body = [quote.group(1)]
            i += 1
            while i < n and (m := QUOTE_RE.match(lines[i])):
                body.append(m.group(1))
                i += 1
            tokens.append({"type": "quote", "text": " ".join(p for p in body if p.strip())})
            continue

        bullet = BULLET_RE.match(line)
        ordered = ORDERED_RE.match(line)
        if bullet or ordered:
            indent = len((bullet or ordered).group(1).replace("\t", "    "))
            text = bullet.group(2) if bullet else ordered.group(3)
            i += 1
            # Fold lazy continuation lines into the item.
            while (i < n and lines[i].strip()
                   and not BULLET_RE.match(lines[i]) and not ORDERED_RE.match(lines[i])
                   and not HEADING_RE.match(lines[i]) and not FENCE_RE.match(lines[i])
                   and not RULE_RE.match(lines[i])
                   and len(lines[i]) - len(lines[i].lstrip()) > indent):
                text += " " + lines[i].strip()
                i += 1
            tokens.append({"type": "list_item",
                           "ordered": bool(ordered),
                           "marker": f"{ordered.group(2)}." if ordered else "",
                           "level": min(indent // 2, 4),
                           "text": text})
            continue

        # Indented code block (4+ spaces, not part of a list).
        if line.startswith("    ") and (not tokens or tokens[-1]["type"] != "list_item"):
            body = []
            while i < n and (lines[i].startswith("    ") or not lines[i].strip()):
                body.append(lines[i][4:])
                i += 1
            while body and not body[-1].strip():
                body.pop()
            tokens.append({"type": "code", "lines": body, "lang": ""})
            continue

        para = [line.strip()]
        i += 1
        while (i < n and lines[i].strip()
               and not HEADING_RE.match(lines[i]) and not FENCE_RE.match(lines[i])
               and not BULLET_RE.match(lines[i]) and not ORDERED_RE.match(lines[i])
               and not RULE_RE.match(lines[i]) and not QUOTE_RE.match(lines[i])
               and not ("|" in lines[i] and i + 1 < n and TABLE_SEP_RE.match(lines[i + 1]))):
            para.append(lines[i].strip())
            i += 1
        tokens.append({"type": "paragraph", "text": " ".join(para)})

    return tokens


def split_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


# ---------------------------------------------------------------------------
# Document construction
# ---------------------------------------------------------------------------


def configure_styles(document) -> None:
    normal = document.styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = INK
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.15

    heading_specs = {
        1: (17, ACCENT, True),
        2: (14, ACCENT, False),
        3: (12, ACCENT_LIGHT, False),
        4: (11, INK, False),
        5: (10.5, MUTED, False),
        6: (10.5, MUTED, False),
    }
    for level, (size, color, keep_page) in heading_specs.items():
        style = document.styles[f"Heading {level}"]
        style.font.name = BODY_FONT
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.italic = False
        style.font.color.rgb = color
        pf = style.paragraph_format
        pf.space_before = Pt(16 if level <= 2 else 10)
        pf.space_after = Pt(5)
        pf.keep_with_next = True
        pf.page_break_before = False
        if keep_page:
            pf.space_before = Pt(18)


def add_footer(document, label: str) -> None:
    for section in document.sections:
        footer = section.footer
        paragraph = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        paragraph.text = ""
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = paragraph.add_run(f"{label}    |    Page ")
        run.font.size = Pt(8)
        run.font.color.rgb = MUTED
        _field(paragraph, "PAGE", "1")
        run = paragraph.add_run(" of ")
        run.font.size = Pt(8)
        run.font.color.rgb = MUTED
        _field(paragraph, "NUMPAGES", "1")
        for r in paragraph.runs:
            r.font.size = Pt(8)
            r.font.color.rgb = MUTED


def add_cover(document, meta: dict) -> None:
    for _ in range(4):
        document.add_paragraph()

    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run(meta["eyebrow"].upper())
    run.font.size = Pt(10)
    run.bold = True
    run.font.color.rgb = ACCENT_LIGHT
    run.font.name = BODY_FONT

    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_after = Pt(4)
    run = paragraph.add_run(meta["title"])
    run.font.size = Pt(28)
    run.bold = True
    run.font.color.rgb = ACCENT
    run.font.name = BODY_FONT

    if meta.get("app"):
        paragraph = document.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = paragraph.add_run(meta["app"])
        run.font.size = Pt(14)
        run.font.color.rgb = MUTED
        run.font.name = BODY_FONT

    divider = document.add_paragraph()
    divider.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _border(divider, "bottom", RULE, size=8)

    rows = [("Repository", meta.get("repo")),
            ("Branch", meta.get("branch")),
            ("Commit", meta.get("commit")),
            ("Review type", meta.get("review_type")),
            ("Generated", meta.get("generated"))]
    rows = [(k, v) for k, v in rows if v]

    table = document.add_table(rows=0, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for key, value in rows:
        cells = table.add_row().cells
        p = cells[0].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run = p.add_run(key)
        run.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = MUTED
        run.font.name = BODY_FONT
        p = cells[1].paragraphs[0]
        run = p.add_run(value)
        run.font.size = Pt(10)
        run.font.color.rgb = INK
        run.font.name = BODY_FONT
    for row in table.rows:
        row.cells[0].width = Inches(1.6)
        row.cells[1].width = Inches(3.4)

    document.add_paragraph()
    note = document.add_paragraph()
    note.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = note.add_run(meta.get("footnote", ""))
    run.font.size = Pt(9)
    run.italic = True
    run.font.color.rgb = MUTED
    run.font.name = BODY_FONT

    document.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def add_toc(document) -> None:
    heading = document.add_paragraph()
    heading.paragraph_format.space_after = Pt(8)
    run = heading.add_run("Contents")
    run.font.size = Pt(16)
    run.bold = True
    run.font.color.rgb = ACCENT
    run.font.name = BODY_FONT
    _border(heading, "bottom", RULE)

    paragraph = document.add_paragraph()
    _field(paragraph, r'TOC \o "1-3" \h \z \u',
           "Open in Word and press F9 (or Update Table) to build the contents.")
    for r in paragraph.runs:
        r.font.size = Pt(10)
        r.font.color.rgb = MUTED
    document.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def add_code_block(document, lines: list[str]) -> None:
    if not lines:
        return
    for index, text in enumerate(lines):
        paragraph = document.add_paragraph()
        pf = paragraph.paragraph_format
        pf.space_before = Pt(6 if index == 0 else 0)
        pf.space_after = Pt(6 if index == len(lines) - 1 else 0)
        pf.left_indent = Inches(0.15)
        pf.line_spacing = 1.0
        run = paragraph.add_run(text if text.strip() else " ")
        run.font.name = MONO
        run.font.size = Pt(8.5)
        run.font.color.rgb = CODE_INK
        _shade(paragraph._p, CODE_BG)
        _border(paragraph, "left", "C6CFD8", size=12)


def add_table(document, rows: list[list[str]]) -> None:
    if not rows:
        return
    width = max(len(row) for row in rows)
    table = document.add_table(rows=1, cols=width)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True

    header = table.rows[0]
    _repeat_header(header)
    for index in range(width):
        cell = header.cells[index]
        _shade(cell._tc, TABLE_HDR_BG)
        paragraph = cell.paragraphs[0]
        paragraph.paragraph_format.space_after = Pt(2)
        paragraph.paragraph_format.space_before = Pt(2)
        text = rows[0][index] if index < len(rows[0]) else ""
        run = paragraph.add_run(strip_inline(text))
        run.bold = True
        run.font.size = Pt(9.5)
        run.font.name = BODY_FONT
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for source in rows[1:]:
        cells = table.add_row().cells
        _prevent_row_split(table.rows[-1])
        for index in range(width):
            paragraph = cells[index].paragraphs[0]
            paragraph.paragraph_format.space_after = Pt(2)
            paragraph.paragraph_format.space_before = Pt(2)
            value = source[index] if index < len(source) else ""
            add_inline(paragraph, value, size=Pt(9.5))

    document.add_paragraph().paragraph_format.space_after = Pt(4)


def add_quote(document, text: str) -> None:
    paragraph = document.add_paragraph()
    pf = paragraph.paragraph_format
    pf.left_indent = Inches(0.2)
    pf.space_before = Pt(6)
    pf.space_after = Pt(6)
    add_inline(paragraph, text, base_italic=True, color=MUTED)
    _shade(paragraph._p, QUOTE_BG)
    _border(paragraph, "left", "9FB3C8", size=14)


def add_rule(document) -> None:
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.space_before = Pt(2)
    paragraph.paragraph_format.space_after = Pt(8)
    _border(paragraph, "bottom", RULE)


BULLET_CHARS = ["•", "◦", "▪", "–"]


def add_list_item(document, token: dict) -> None:
    """Render a list item with an explicit marker and a hanging indent.

    Markers come from the Markdown source rather than Word's list styles: all
    `List Number` paragraphs share one numbering definition, so consecutive
    lists in a long report would keep counting up instead of restarting at 1.
    """
    level = token["level"]
    marker = token["marker"] if token["ordered"] else BULLET_CHARS[min(level, len(BULLET_CHARS) - 1)]

    indent = 0.22 + 0.28 * level
    paragraph = document.add_paragraph()
    pf = paragraph.paragraph_format
    pf.left_indent = Inches(indent + 0.26)
    pf.first_line_indent = Inches(-0.26)
    pf.space_after = Pt(3)
    pf.tab_stops.add_tab_stop(Inches(indent + 0.26))

    run = paragraph.add_run(marker)
    run.font.name = BODY_FONT
    run.font.size = Pt(10.5)
    run.font.color.rgb = MUTED if not token["ordered"] else ACCENT_LIGHT
    run.bold = token["ordered"]
    paragraph.add_run("\t")

    add_inline(paragraph, token["text"])


def render(document, tokens: list[dict], *, demote_headings: bool) -> None:
    for token in tokens:
        kind = token["type"]
        if kind == "heading":
            level = token["level"] + (1 if demote_headings else 0)
            level = max(1, min(level, 6))
            paragraph = document.add_heading(level=level)
            add_inline(paragraph, token["text"], base_bold=True,
                       color=paragraph.style.font.color.rgb or ACCENT)
            if level <= 2:
                _border(paragraph, "bottom", RULE)
        elif kind == "paragraph":
            paragraph = document.add_paragraph()
            add_inline(paragraph, token["text"])
        elif kind == "list_item":
            add_list_item(document, token)
        elif kind == "code":
            add_code_block(document, token["lines"])
        elif kind == "table":
            add_table(document, token["rows"])
        elif kind == "quote":
            add_quote(document, token["text"])
        elif kind == "rule":
            add_rule(document)


def build(markdown: str, args) -> "Document":
    document = Document()
    configure_styles(document)

    section = document.sections[0]
    section.top_margin = Inches(0.9)
    section.bottom_margin = Inches(0.9)
    section.left_margin = Inches(0.9)
    section.right_margin = Inches(0.9)

    tokens = tokenize(markdown)

    # If the Markdown opens with a single H1, use it as the cover title and
    # demote the remaining headings so Word's outline stays consistent.
    title = args.title
    demote = False
    if tokens and tokens[0]["type"] == "heading" and tokens[0]["level"] == 1:
        h1_count = sum(1 for t in tokens if t["type"] == "heading" and t["level"] == 1)
        if not args.title:
            title = strip_inline(tokens[0]["text"])
        if h1_count == 1:
            tokens = tokens[1:]
        demote = h1_count > 1

    title = title or "MuleSoft Code Review Report"

    add_cover(document, {
        "eyebrow": args.eyebrow,
        "title": title,
        "app": args.app,
        "repo": args.repo,
        "branch": args.branch,
        "commit": args.commit,
        "review_type": args.review_type,
        "generated": args.date or _dt.datetime.now().strftime("%d %b %Y, %H:%M %Z").strip(),
        "footnote": args.footnote,
    })

    if not args.no_toc:
        add_toc(document)

    render(document, tokens, demote_headings=demote)
    add_footer(document, args.app or title)
    return document


def parse_args(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(
        description="Convert a Markdown code review report into a styled Word document.")
    parser.add_argument("--input", "-i", required=True,
                        help="Markdown input file, or '-' for stdin.")
    parser.add_argument("--output", "-o", default="CODE_REVIEW_REPORT.docx",
                        help="Output .docx path (default: CODE_REVIEW_REPORT.docx).")
    parser.add_argument("--title", default="", help="Cover title (default: first H1).")
    parser.add_argument("--app", default="", help="Application name shown on the cover.")
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", ""),
                        help="Repository name (defaults to $GITHUB_REPOSITORY).")
    parser.add_argument("--branch", default="", help="Branch or ref reviewed.")
    parser.add_argument("--commit", default="", help="Commit SHA reviewed.")
    parser.add_argument("--review-type", default="Full application review (read-only)",
                        dest="review_type", help="Review type shown on the cover.")
    parser.add_argument("--eyebrow", default="MuleSoft Integration Architecture",
                        help="Small label above the cover title.")
    parser.add_argument("--footnote",
                        default="Generated by Claude Code. Findings are evidence-based and "
                                "require engineering validation before remediation.",
                        help="Italic note at the bottom of the cover page.")
    parser.add_argument("--date", default="", help="Override the generated-on timestamp.")
    parser.add_argument("--no-toc", action="store_true", help="Omit the table of contents.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.input == "-":
        markdown = sys.stdin.read()
    else:
        if not os.path.isfile(args.input):
            sys.exit(f"ERROR: input file not found: {args.input}")
        with open(args.input, encoding="utf-8") as handle:
            markdown = handle.read()

    if not markdown.strip():
        sys.exit("ERROR: the review report is empty; refusing to write an empty document.")

    document = build(markdown, args)

    output = os.path.abspath(args.output)
    parent = os.path.dirname(output)
    if parent:
        os.makedirs(parent, exist_ok=True)
    document.save(output)

    size = os.path.getsize(output)
    print(f"Wrote {output} ({size:,} bytes)")
    if size < 8_000:
        print("WARNING: the generated document is unusually small; verify the report content.",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
