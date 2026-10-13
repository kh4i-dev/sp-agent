#!/usr/bin/env python3
"""Xuat Markdown review tu .docx de doc noi dung nhanh, khong can mo Word.

Khong thay the render anh. Markdown chi dung de doc/kiểm noi dung + cau truc text.
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


def has_image(paragraph_element) -> bool:
    return bool(
        paragraph_element.findall(f".//{W_NS}drawing")
        or paragraph_element.findall(f".//{W_NS}pict")
    )


def field_tokens(docx_path: Path) -> set[str]:
    tokens = set()
    content_xml = re.compile(r"word/(?:document|header\d*|footer\d*)\.xml$")
    instr_text = re.compile(r"<w:instrText[^>]*>(.*?)</w:instrText>", re.S)
    fld_simple = re.compile(r"<w:fldSimple[^>]*\sw:instr=\"([^\"]+)\"", re.S)
    with zipfile.ZipFile(docx_path) as z:
        for item in z.namelist():
            if not content_xml.match(item):
                continue
            try:
                xml = z.read(item).decode("utf-8", "ignore")
            except KeyError:
                continue
            field_code = " ".join(instr_text.findall(xml) + fld_simple.findall(xml))
            for token in ("TOC", "SEQ", "PAGE", "REF", "STYLEREF"):
                if token in field_code:
                    tokens.add(token)
    return tokens


def iter_body(doc):
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    for child in doc.element.body.iterchildren():
        tag = child.tag
        if tag.endswith("}p"):
            yield ("p", Paragraph(child, doc))
        elif tag.endswith("}tbl"):
            yield ("tbl", Table(child, doc))


def main() -> int:
    ap = argparse.ArgumentParser(description="Xuat Markdown review tu .docx.")
    ap.add_argument("docx", help="Duong dan file .docx")
    ap.add_argument("--out", help="File Markdown dau ra")
    ap.add_argument("--max-chars", type=int, default=60000, help="Gioi han ky tu noi dung trong Markdown")
    args = ap.parse_args()

    docx_path = Path(args.docx)
    if not docx_path.exists():
        print(f"Loi: Khong tim thay file {docx_path}", file=sys.stderr)
        return 2

    try:
        from docx import Document
    except ImportError:
        print("Can cai dat: pip install python-docx", file=sys.stderr)
        return 2

    out_path = Path(args.out) if args.out else docx_path.with_suffix(".review.md")
    doc = Document(str(docx_path))

    stats = {"words": 0, "paragraphs": 0, "empty": 0, "tables": 0, "images": 0, "captions": []}
    headings: list[tuple[int, str, int]] = []
    sections: list[dict] = []
    current = {"title": "(Chua co Heading 1)", "words": 0}
    body_chars = 0
    lines: list[str] = []

    for kind, node in iter_body(doc):
        if kind == "tbl":
            stats["tables"] += 1
            rows = len(node.rows)
            cols = len(node.columns) if rows else 0
            head = " / ".join(c.text.strip().replace("\n", " ") for c in node.rows[0].cells) if rows and cols else ""
            lines.append(f"\n[BANG {stats['tables']}: {rows}x{cols} | {head[:160]}]\n")
            continue

        text = node.text.strip()
        stats["paragraphs"] += 1
        if not text and not has_image(node._p):
            stats["empty"] += 1
            continue

        level = heading_level(node.style.name if node.style else "")
        words = len(text.split()) if text else 0
        stats["words"] += words

        if level:
            headings.append((level, text, words))
            if level == 1:
                if current["words"] or sections:
                    sections.append(current)
                current = {"title": text, "words": 0}
            lines.append(f"\n{'#' * min(level + 1, 6)} {text}\n")
            continue

        current["words"] += words
        m = CAPTION_RE.match(text)
        if m:
            stats["captions"].append((caption_kind(m.group(1)), m.group(2), m.group(3)))
            lines.append(f"\n*{text}*\n")
            continue
        if has_image(node._p):
            stats["images"] += 1
            lines.append(f"\n[ANH {stats['images']}]{(' ' + text) if text else ''}\n")
            continue
        if body_chars < args.max_chars and text:
            take = min(len(text), args.max_chars - body_chars)
            lines.append(text[:take] + "\n")
            body_chars += take

    sections.append(current)
    fields = field_tokens(docx_path)

    md = []
    md.append(f"# Review: {docx_path.name}\n")
    md.append("## Tom tat\n")
    md.append(f"- Tong tu: ~{stats['words']:,}")
    md.append(f"- Doan van: {stats['paragraphs']} ({stats['empty']} doan trong)")
    md.append(f"- Heading: {len(headings)} | Bang: {stats['tables']} | Anh: {stats['images']} | Caption: {len(stats['captions'])}")
    md.append(f"- Field phat hien: {', '.join(sorted(fields)) if fields else 'khong co TOC/SEQ/PAGE/REF/STYLEREF'}")
    if body_chars >= args.max_chars:
        md.append(f"- Noi dung da cat ngan o {args.max_chars:,} ky tu de review nhanh.")
    md.append("\n## Cay Heading + tu theo muc\n")
    for level, text, words in headings:
        md.append(f"{'  ' * (level - 1)}- H{level} ({words} tu tieu de): {text}")
    md.append("\n## Tu theo chuong (H1)\n")
    for sec in sections:
        md.append(f"- {sec['title']}: ~{sec['words']:,} tu")
    if stats["captions"]:
        md.append("\n## Caption\n")
        for kind, num, title in stats["captions"]:
            md.append(f"- {kind} {num}: {title[:180]}")
    md.append("\n## Noi dung trich\n")
    md.extend(lines)
    md.append("\n## Checklist doc bang mat (dien tay)\n")
    md.append("- [ ] Van giong nguoi, khong dau hieu AI theo human-report-writing")
    md.append("- [ ] Caption dung vi tri/kieu, so thu tu khop cross-reference")
    md.append("- [ ] Bang/hinh khong vo, khong mo côi caption o muc text")
    md.append("- [ ] TOC/số trang/field dung loai tai lieu")

    out_path.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Da xuat: {out_path} (~{stats['words']:,} tu, {len(headings)} heading)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
