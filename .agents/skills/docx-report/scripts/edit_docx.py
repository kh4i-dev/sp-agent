#!/usr/bin/env python3
"""Chỉnh sửa và tìm kiếm/thay thế nội dung trong file Word (.docx).

Cách dùng:
    python edit_docx.py report.docx --replace "K58" "K59"
    python edit_docx.py report.docx --replace-many map.json -o report_updated.docx
    python edit_docx.py report.docx --set-font "Times New Roman" --font-size 13
"""
import argparse
import json
import sys
from pathlib import Path

# Đảm bảo in tiếng Việt không bị lỗi charmap trên Windows terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def replace_text_in_paragraph(p, old_text, new_text):
    count = 0
    if old_text in p.text:
        # Nếu cụm từ nằm trọn trong 1 run
        for r in p.runs:
            if old_text in r.text:
                r.text = r.text.replace(old_text, new_text)
                count += 1
        # Nếu bị ngắt giữa các runs
        if old_text in p.text:
            p.text = p.text.replace(old_text, new_text)
            count += 1
    return count


def replace_text_in_docx(doc_path: Path, replacements: dict[str, str], out_path: Path):
    from docx import Document

    doc = Document(str(doc_path))
    total_replaced = 0

    # 1. Đoạn văn trong thân văn bản
    for p in doc.paragraphs:
        for old, new in replacements.items():
            total_replaced += replace_text_in_paragraph(p, old, new)

    # 2. Bảng biểu
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for old, new in replacements.items():
                        total_replaced += replace_text_in_paragraph(p, old, new)

    # 3. Header và Footer
    for section in doc.sections:
        for p in section.header.paragraphs:
            for old, new in replacements.items():
                total_replaced += replace_text_in_paragraph(p, old, new)
        for p in section.footer.paragraphs:
            for old, new in replacements.items():
                total_replaced += replace_text_in_paragraph(p, old, new)

    doc.save(str(out_path))
    return total_replaced


def format_doc_typography(doc_path: Path, font_name: str, font_size_pt: float, out_path: Path):
    from docx import Document
    from docx.shared import Pt

    doc = Document(str(doc_path))
    for p in doc.paragraphs:
        for r in p.runs:
            if font_name:
                r.font.name = font_name
            if font_size_pt:
                r.font.size = Pt(font_size_pt)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for r in p.runs:
                        if font_name:
                            r.font.name = font_name
                        if font_size_pt:
                            r.font.size = Pt(font_size_pt)

    doc.save(str(out_path))
    print(f">> Đã chuẩn hóa font chữ thành '{font_name}' cỡ {font_size_pt}pt -> Lưu tại: {out_path}")


def main():
    ap = argparse.ArgumentParser(description="Chỉnh sửa nội dung file Word .docx.")
    ap.add_argument("docx", help="Đường dẫn file .docx")
    ap.add_argument("-o", "--output", help="Đường dẫn file xuất ra")
    ap.add_argument("--replace", nargs=2, metavar=("OLD", "NEW"), help="Tìm và thay thế văn bản")
    ap.add_argument("--replace-many", help="File JSON chứa các cặp { 'từ cũ': 'từ mới' }")
    ap.add_argument("--set-font", help="Đặt lại tên font (ví dụ: 'Times New Roman', 'Arial')")
    ap.add_argument("--font-size", type=float, help="Đặt lại cỡ chữ (pt)")
    args = ap.parse_args()

    doc_path = Path(args.docx)
    if not doc_path.exists():
        sys.exit(f"Lỗi: Không tìm thấy file {doc_path}")

    out_path = Path(args.output) if args.output else doc_path

    try:
        from docx import Document
    except ImportError:
        sys.exit("Cần cài đặt: pip install python-docx (hoặc dùng uv run --with python-docx ...)")

    if args.set_font or args.font_size:
        format_doc_typography(doc_path, args.set_font, args.font_size, out_path)
        return

    replacements = {}
    if args.replace:
        replacements[args.replace[0]] = args.replace[1]
    if args.replace_many:
        j_path = Path(args.replace_many)
        if j_path.exists():
            replacements.update(json.loads(j_path.read_text(encoding="utf-8")))

    if replacements:
        print(f">> Đang tìm và thay thế {len(replacements)} cụm từ trong {doc_path.name}...")
        count = replace_text_in_docx(doc_path, replacements, out_path)
        print(f">> Hoàn thành! Đã thay đổi {count} vị trí -> Lưu tại: {out_path}")
    else:
        print("Vui lòng chỉ định --replace hoặc --set-font. Dùng --help để xem cú pháp.")


if __name__ == "__main__":
    main()
