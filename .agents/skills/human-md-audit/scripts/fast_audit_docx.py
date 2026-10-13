#!/usr/bin/env python3
"""Audit nhanh .docx bang XML/text trong vai giay, khong render anh.

Dung de lap nhanh. FAST-CHECK PASS khong phai VISUAL PASS: khong ket luan
layout/tran trang/vo bang neu chua render + soi anh.
"""
import argparse
import re
import sys
import zipfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
CAPTION_RE = re.compile(r"^(Hinh|Hình|Bang|Bảng)\s+(\d+(?:\.\d+)*)\s*[:.\-–]\s*(.+)$")


def caption_kind(raw_kind: str) -> str:
    return "Hình" if raw_kind.startswith("H") else "Bảng"
HEADING_RE = re.compile(r"heading\s*(\d+)", re.IGNORECASE)


def heading_level(style_name: str) -> int:
    name = (style_name or "").strip().lower()
    m = HEADING_RE.search(name)
    if m:
        return int(m.group(1))
    if name.startswith("ti\u00eau \u0111\u1ec1"):
        tail = name.rsplit(" ", 1)[-1]
        return int(tail) if tail.isdigit() else 1
    return 0


def is_body_style(style_name: str) -> bool:
    name = (style_name or "").strip().lower()
    return name in {"normal", "default", "body text", "n\u1ed9i dung"} or (
        "heading" not in name and "ti\u00eau \u0111\u1ec1" not in name and "caption" not in name
    )


def raw_xml_tokens(docx_path: Path) -> str:
    content_xml = re.compile(r"word/(?:document|header\d*|footer\d*)\.xml$")
    instr_text = re.compile(r"<w:instrText[^>]*>(.*?)</w:instrText>", re.S)
    fld_simple = re.compile(r"<w:fldSimple[^>]*\sw:instr=\"([^\"]+)\"", re.S)
    parts = []
    with zipfile.ZipFile(docx_path) as z:
        for item in z.namelist():
            if content_xml.match(item):
                try:
                    xml = z.read(item).decode("utf-8", "ignore")
                except KeyError:
                    continue
                parts.extend(instr_text.findall(xml))
                parts.extend(fld_simple.findall(xml))
    return "\n".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit nhanh .docx, khong render anh.")
    ap.add_argument("docx", help="Duong dan file .docx")
    ap.add_argument("--md", help="Ghi ket qua dang Markdown")
    ap.add_argument("--strict", action="store_true", help="WARN ve keep/cantSplit/tblHeader thanh FAIL")
    args = ap.parse_args()

    docx_path = Path(args.docx)
    if not docx_path.exists():
        print(f"Loi: Khong tim thay file {docx_path}", file=sys.stderr)
        return 2
    try:
        from docx import Document
        from docx.oxml.ns import qn
        from docx.table import Table
        from docx.text.paragraph import Paragraph
    except ImportError:
        print("Can cai dat: pip install python-docx", file=sys.stderr)
        return 2

    doc = Document(str(docx_path))
    fails: list[str] = []
    warns: list[str] = []
    blocks: list[dict] = []
    headings: list[tuple[int, str]] = []
    labels: list[tuple[str, str]] = []

    for child in doc.element.body.iterchildren():
        if child.tag.endswith("}p"):
            p = Paragraph(child, doc)
            text = p.text.strip()
            blocks.append({"kind": "p", "text": text, "p": p})
            level = heading_level(p.style.name if p.style else "")
            if level and text:
                headings.append((level, text))
            m = CAPTION_RE.match(text) if text else None
            if m:
                labels.append((caption_kind(m.group(1)), m.group(2)))
        elif child.tag.endswith("}tbl"):
            blocks.append({"kind": "tbl", "table": Table(child, doc)})

    prev_level = 0
    for level, text in headings:
        if not text:
            fails.append("HEADING_EMPTY: co Heading rong.")
        if prev_level and level > prev_level + 1:
            fails.append(f"HIERARCHY_SKIP: nhay tu H{prev_level} sang H{level}: {text[:100]}")
        prev_level = level or prev_level

    seen = set()
    for kind, num in labels:
        key = f"{kind} {num}"
        if key in seen:
            fails.append(f"CAPTION_DUP: trung {key}.")
        seen.add(key)

    xml = raw_xml_tokens(docx_path)
    if labels and "SEQ" not in xml:
        fails.append("CAPTION_PLAIN_NUMBER: caption dang so tay, chua co field SEQ.")
    if headings and "TOC" not in xml:
        warns.append("TOC_MISSING: chua thay field TOC.")

    for i, b in enumerate(blocks):
        if b["kind"] != "p" or not b["text"]:
            continue
        p = b["p"]
        style = p.style.name if p.style else ""
        if heading_level(style) or CAPTION_RE.match(b["text"]):
            continue
        if not is_body_style(style):
            continue
        for r in p.runs:
            if not (r.text or "").strip():
                continue
            if (r.font.name or "").strip().lower() in {"calibri", "arial"}:
                fails.append(f"FONT_DIRECT: '{r.text.strip()[:60]}' dang dung {r.font.name} thay vi Times New Roman.")
            elif (r.font.name or "").strip() and (r.font.name or "").strip().lower() != "times new roman":
                warns.append(f"FONT_OVERRIDE: '{r.text.strip()[:60]}' dang dung {r.font.name}.")
            if r.bold:
                fails.append(f"BOLD_BODY: than bai co chu in dam: '{r.text.strip()[:80]}'.")
        if "\u2014" in b["text"]:
            fails.append("EM_DASH: than bai chua dau gach dai —.")

    for i, b in enumerate(blocks):
        if b["kind"] == "tbl":
            table = b["table"]
            header_ok = False
            for r_idx, row in enumerate(table.rows):
                trpr = row._tr.find(qn("w:trPr"))
                if trpr is None or trpr.find(qn("w:cantSplit")) is None:
                    msg = f"TABLE_SPLITABLE: bang {i} hang {r_idx + 1} thieu cantSplit."
                    (fails if args.strict else warns).append(msg)
                if r_idx == 0 and trpr is not None and trpr.find(qn("w:tblHeader")) is not None:
                    header_ok = True
            if not header_ok:
                warns.append(f"TABLE_HEADER_REPEAT: bang {i} chua co tblHeader.")
            near = " ".join(x.get("text", "") for x in blocks[max(0, i - 2):i + 3] if x["kind"] == "p")
            if not re.search(r"^B\u1ea3ng\s+\d+", near, re.MULTILINE) and "B\u1ea3ng" not in near:
                warns.append(f"TABLE_CAPTION_FAR: bang {i} khong thay caption Bang ke ben.")
        elif b["kind"] == "p" and b["p"]._p.findall(f".//{W_NS}drawing"):
            if b["p"].paragraph_format.keep_with_next is not True:
                msg = f"IMAGE_KEEP_NEXT: doan anh thieu keep_with_next: '{b['text'][:80]}'."
                (fails if args.strict else warns).append(msg)
            near = " ".join(x.get("text", "") for x in blocks[i + 1:i + 3] if x["kind"] == "p")
            if "H\u00ecnh" not in near:
                warns.append("IMAGE_CAPTION_FAR: doan anh khong thay caption Hinh ngay ben duoi.")

    print(f"FAST-AUDIT {docx_path.name}: {len(fails)} FAIL, {len(warns)} WARN")
    for x in fails:
        print(f"FAIL {x}")
    for x in warns:
        print(f"WARN {x}")

    if args.md:
        out = Path(args.md)
        md = [
            f"# Fast audit: {docx_path.name}",
            "",
            f"- FAIL: {len(fails)}",
            f"- WARN: {len(warns)}",
            "",
            "## FAIL",
        ]
        md.extend(f"- [ ] {x}" for x in fails)
        if not fails:
            md.append("- Khong co.")
        md.extend(["", "## WARN"])
        md.extend(f"- [ ] {x}" for x in warns)
        if not warns:
            md.append("- Khong co.")
        md.extend(["", "> FAST-CHECK PASS khong phai VISUAL PASS."])
        out.write_text("\n".join(md) + "\n", encoding="utf-8")
        print(f"Da ghi: {out}")

    return 2 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
