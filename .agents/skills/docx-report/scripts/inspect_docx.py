#!/usr/bin/env python3
"""Audit và phân tích cấu trúc tài liệu Word (.docx).

Cách dùng:
    python inspect_docx.py report.docx
    python inspect_docx.py report.docx --verbose

Công dụng:
  - Thống kê tổng số từ, đoạn văn, số bảng biểu, số ảnh
  - Liệt kê cây tiêu đề (Heading hierarchy H1, H2, H3, H4)
  - Phát hiện các đoạn rỗng hoặc bảng bị lỗi
"""
import argparse
import sys
from pathlib import Path

# Đảm bảo in tiếng Việt không bị lỗi charmap trên Windows terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def inspect_docx(doc_path: Path, verbose: bool = False):
    from docx import Document

    doc = Document(str(doc_path))

    total_words = 0
    headings = []
    empty_paragraphs = 0
    tables_count = len(doc.tables)

    for p in doc.paragraphs:
        txt = p.text.strip()
        if not txt:
            empty_paragraphs += 1
            continue

        words = len(txt.split())
        total_words += words

        style_name = p.style.name.lower()
        if "heading" in style_name or "tiêu đề" in style_name:
            headings.append((p.style.name, txt))

    # Đếm số ảnh bằng cách duyệt các XML elements
    image_count = 0
    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:
            image_count += 1

    print("=" * 65)
    print(f"BÁO CÁO CẤU TRÚC TÀI LIỆU WORD: {doc_path.name}")
    print(f"  - Tổng số từ:        ~{total_words:,} từ")
    print(f"  - Tổng số đoạn văn:  {len(doc.paragraphs)} đoạn ({empty_paragraphs} đoạn trống)")
    print(f"  - Tổng số bảng biểu: {tables_count} bảng")
    print(f"  - Tổng số hình ảnh:  {image_count} hình")
    print(f"  - Tổng số Heading:   {len(headings)} mục")
    print("=" * 65)

    if headings:
        print("\nCÂY TIÊU ĐỀ NỘI DUNG (HEADING HIERARCHY):")
        for style, h_text in headings:
            indent = "  "
            if "2" in style:
                indent = "    "
            elif "3" in style:
                indent = "      "
            elif "4" in style:
                indent = "        "
            print(f"{indent}• [{style}] {h_text}")

    if verbose and tables_count > 0:
        print("\nDANH SÁCH BẢNG BIỂU:")
        for t_idx, table in enumerate(doc.tables, start=1):
            rows = len(table.rows)
            cols = len(table.columns) if rows > 0 else 0
            first_cell = table.rows[0].cells[0].text.strip() if rows > 0 and cols > 0 else ""
            print(f"  Bảng {t_idx:02d}: {rows} hàng x {cols} cột | Ô đầu: '{first_cell[:40]}'")

    print("\n" + "=" * 65)


def main():
    ap = argparse.ArgumentParser(description="Audit cấu trúc tài liệu Word (.docx).")
    ap.add_argument("docx", help="Đường dẫn file .docx")
    ap.add_argument("-v", "--verbose", action="store_true", help="Hiển thị chi tiết bảng biểu")
    args = ap.parse_args()

    doc_path = Path(args.docx)
    if not doc_path.exists():
        sys.exit(f"Lỗi: Không tìm thấy file {doc_path}")

    try:
        from docx import Document
    except ImportError:
        sys.exit("Cần cài đặt: pip install python-docx")

    inspect_docx(doc_path, args.verbose)


if __name__ == "__main__":
    main()
