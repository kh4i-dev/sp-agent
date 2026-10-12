#!/usr/bin/env python3
"""Chỉnh sửa, định dạng style và chuẩn hóa học thuật cho file Word (.docx).

Cách dùng:
    python edit_docx.py report.docx --academic-format -o report_chuan_hoc_thuat.docx
    python edit_docx.py report.docx --style-tables
    python edit_docx.py report.docx --add-toc --add-tof --add-tot
    python edit_docx.py report.docx --replace "K58" "K59"
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


def apply_academic_page_setup(doc, top_cm=3.0, bottom_cm=3.0, left_cm=3.5, right_cm=2.0):
    """Căn lề chuẩn luận văn / đồ án theo quy định học thuật:
    - Trái (Left): 3.5 cm (để chừa gáy đóng bìa/dập ghim).
    - Phải (Right): 2.0 cm.
    - Trên (Top): 3.0 cm.
    - Dưới (Bottom): 3.0 cm.
    """
    from docx.shared import Cm

    for section in doc.sections:
        section.top_margin = Cm(top_cm)
        section.bottom_margin = Cm(bottom_cm)
        section.left_margin = Cm(left_cm)
        section.right_margin = Cm(right_cm)


def apply_academic_paragraph_format(doc, font_name="Times New Roman", font_size_pt=13,
                                     indent_cm=1.27, line_spacing=1.35):
    """Chuẩn hóa toàn bộ văn xuôi báo cáo/luận văn:
    - Thụt lề đầu dòng: 1.0 cm - 1.27 cm (tương đương 1 Tab / 0.5 inch).
    - Căn đều hai bên (Justify).
    - Giãn dòng: 1.3 - 1.5 lines (mặc định 1.35).
    - Giãn đoạn: Spacing Before: 2pt, Spacing After: 4pt.
    - Chống dòng mồ côi (Widow/Orphan control).
    - Giữ nguyên các đoạn đặc biệt: Tiêu đề (Headings), Caption hình/bảng, Bìa.
    """
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Cm, Pt

    for p in doc.paragraphs:
        txt = p.text.strip()
        if not txt:
            continue

        style_name = p.style.name.lower() if p.style else ""
        is_heading = "heading" in style_name or "tiêu đề" in style_name
        is_caption = "caption" in style_name or txt.startswith("Hình ") or txt.startswith("Bảng ")

        # Nếu là Heading
        if is_heading:
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.keep_with_next = True
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(6)
            continue

        # Nếu là Caption
        if is_caption:
            p.paragraph_format.first_line_indent = Cm(0)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(12)
            for r in p.runs:
                r.font.name = font_name
                r.font.size = Pt(12)
                r.font.italic = True
                r.font.bold = False
            continue

        # Đoạn văn xuôi thông thường (Normal body text)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.first_line_indent = Cm(indent_cm)
        p.paragraph_format.line_spacing = line_spacing
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.widow_control = True

        for r in p.runs:
            if font_name:
                r.font.name = font_name
            if font_size_pt:
                r.font.size = Pt(font_size_pt)


def style_table(table, font_name="Times New Roman", font_size_pt=11):
    """Định dạng chuẩn học thuật cho bảng biểu:
    - Nền bảng: 100% TRẮNG TINH (xóa mọi shading w:shd, không tô màu).
    - Header: In đậm (Bold), không nghiêng (Italic=False), căn trái (LEFT, không căn giữa).
    - Header lặp lại khi sang trang mới (w:tblHeader).
    - Body: Times New Roman, chống gãy hàng giữa trang (w:cantSplit).
    - Căn giữa toàn bộ bảng theo chiều ngang trang.
    """
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import parse_xml
    from docx.oxml.ns import nsdecls, qn
    from docx.shared import Pt

    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Tùy biến viền bảng tinh gọn chuẩn báo cáo khoa học
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="333333"/>'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="333333"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="D0D5DD"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

    # Định dạng hàng Header (hàng 0)
    if len(table.rows) > 0:
        header_row = table.rows[0]
        trPr = header_row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        for cell in header_row.cells:
            tcPr = cell._tc.get_or_add_tcPr()
            # Xóa bỏ mọi nền màu (shading) -> Nền trắng tinh
            for old_shd in tcPr.findall(qn('w:shd')):
                tcPr.remove(old_shd)

            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT  # TIÊU ĐỀ CỘT: KHÔNG CĂN GIỮA (CĂN TRÁI)
                p.paragraph_format.first_line_indent = Pt(0)
                for r in p.runs:
                    r.font.name = font_name
                    r.font.size = Pt(font_size_pt)
                    r.font.italic = False              # KHÔNG IN NGHIÊNG
                    r.font.bold = True                 # IN ĐẬM

    # Định dạng hàng Body (từ hàng 1 trở đi)
    for row in table.rows[1:]:
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        for cell in row.cells:
            tcPr = cell._tc.get_or_add_tcPr()
            for old_shd in tcPr.findall(qn('w:shd')):
                tcPr.remove(old_shd)

            for p in cell.paragraphs:
                p.paragraph_format.first_line_indent = Pt(0)
                for r in p.runs:
                    r.font.name = font_name
                    r.font.size = Pt(font_size_pt)


def style_all_tables_in_doc(doc, font_name="Times New Roman", font_size_pt=13):
    """Áp dụng style chuẩn cho tất cả bảng biểu trong tài liệu."""
    for table in doc.tables:
        style_table(table, font_name, font_size_pt)


def relocate_and_format_table_captions(doc, font_name="Times New Roman"):
    """Đảm bảo Caption của bảng luôn được đặt ở CUỐI BẢNG (ngay dưới bảng).
    Định dạng: Chữ nghiêng (italic), cỡ 12-13pt, căn giữa hoặc căn trái, không bold.
    """
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Cm, Pt

    for p in doc.paragraphs:
        txt = p.text.strip()
        if txt.startswith("Bảng ") and (":" in txt or "." in txt):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(12)
            for r in p.runs:
                r.font.name = font_name
                r.font.size = Pt(12)
                r.font.italic = True
                r.font.bold = False


def format_images_and_captions(doc, font_name="Times New Roman"):
    """Căn giữa hình ảnh và khóa chặt hình với caption bên dưới để không bị tách trang."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Cm, Pt

    for p in doc.paragraphs:
        if "graphic" in p._p.xml or "drawing" in p._p.xml:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.keep_with_next = True

        txt = p.text.strip()
        if txt.startswith("Hình ") and (":" in txt or "." in txt):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(12)
            for r in p.runs:
                r.font.name = font_name
                r.font.size = Pt(12)
                r.font.italic = True
                r.font.bold = False


def insert_field_code(doc, field_instr: str, title: str = None):
    """Chèn trường tự động Word (Field Codes như TOC, TOF, TOT)."""
    from docx.oxml import parse_xml
    from docx.oxml.ns import nsdecls

    if title:
        doc.add_paragraph(title, style="Heading 1")

    p = doc.add_paragraph()
    fldSimple = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="{field_instr}"/>')
    p._p.append(fldSimple)


def add_table_of_contents(doc, title="MỤC LỤC"):
    insert_field_code(doc, r'TOC \o "1-3" \h \z \u', title)


def add_table_of_figures(doc, title="DANH MỤC HÌNH VẼ"):
    insert_field_code(doc, r'TOC \c "Hình" \h \z', title)


def add_table_of_tables(doc, title="DANH MỤC BẢNG BIỂU"):
    insert_field_code(doc, r'TOC \c "Bảng" \h \z', title)


def main():
    ap = argparse.ArgumentParser(description="Chỉnh sửa nội dung, style bảng và chuẩn hóa học thuật cho file Word .docx.")
    ap.add_argument("docx", help="Đường dẫn file .docx")
    ap.add_argument("-o", "--output", help="Đường dẫn file xuất ra")
    ap.add_argument("--academic-format", action="store_true",
                    help="Áp dụng toàn bộ quy chuẩn học thuật: Thụt lề 1 tab (1.27cm), căn đều 2 bên (Justify), lề giấy 3.5/2.0/3.0/3.0 cm, giãn dòng 1.35, giãn đoạn, style bảng & caption")
    ap.add_argument("--set-font", default="Times New Roman", help="Đặt tên font (mặc định: 'Times New Roman')")
    ap.add_argument("--font-size", type=float, default=13.0, help="Đặt cỡ chữ pt (mặc định: 13.0)")
    ap.add_argument("--indent-cm", type=float, default=1.27, help="Khoảng cách thụt đầu dòng cm (mặc định: 1.27 cm / 1 tab)")
    ap.add_argument("--line-spacing", type=float, default=1.35, help="Hệ số giãn dòng (mặc định: 1.35 lines)")
    ap.add_argument("--style-tables", action="store_true", help="Chuẩn hóa style bảng (Header nghiêng, căn giữa, 13pt; body 13pt; cantSplit; tblHeader)")
    ap.add_argument("--style-captions", action="store_true", help="Chuẩn hóa caption bảng đặt ở cuối bảng và caption hình")
    ap.add_argument("--add-toc", action="store_true", help="Chèn Mục lục tự động (TOC 1-3)")
    ap.add_argument("--add-tof", action="store_true", help="Chèn Danh mục hình vẽ (TOF)")
    ap.add_argument("--add-tot", action="store_true", help="Chèn Danh mục bảng biểu (TOT)")
    ap.add_argument("--replace", nargs=2, metavar=("OLD", "NEW"), help="Tìm và thay thế văn bản")
    ap.add_argument("--replace-many", help="File JSON chứa các cặp { 'từ cũ': 'từ mới' }")
    args = ap.parse_args()

    doc_path = Path(args.docx)
    if not doc_path.exists():
        sys.exit(f"Lỗi: Không tìm thấy file {doc_path}")

    out_path = Path(args.output) if args.output else doc_path

    try:
        from docx import Document
    except ImportError:
        sys.exit("Cần cài đặt: pip install python-docx")

    # Xử lý thay thế từ nếu có
    if args.replace or args.replace_many:
        replacements = {}
        if args.replace:
            replacements[args.replace[0]] = args.replace[1]
        if args.replace_many:
            j_path = Path(args.replace_many)
            if j_path.exists():
                replacements.update(json.loads(j_path.read_text(encoding="utf-8")))
        count = replace_text_in_docx(doc_path, replacements, out_path)
        print(f">> Đã thay thế {count} vị trí văn bản.")
        doc_path = out_path

    doc = Document(str(doc_path))
    modified = False

    if args.academic_format:
        print(">> Đang áp dụng quy chuẩn luận văn / đồ án học thuật:")
        apply_academic_page_setup(doc)
        print("   1. Căn lề giấy: Trái 3.5cm, Phải 2.0cm, Trên 3.0cm, Dưới 3.0cm.")
        apply_academic_paragraph_format(doc, args.set_font, args.font_size, args.indent_cm, args.line_spacing)
        print(f"   2. Văn xuôi: Thụt lề đầu dòng {args.indent_cm}cm (1 tab), Căn đều hai bên (Justify), Giãn dòng {args.line_spacing}x, Giãn đoạn 2pt/4pt.")
        style_all_tables_in_doc(doc, args.set_font, args.font_size)
        print("   3. Bảng biểu: Header chữ thường in nghiêng căn giữa 13pt, lặp header & chống gãy hàng, viền ngang thanh mảnh.")
        relocate_and_format_table_captions(doc, args.set_font)
        print("   4. Caption bảng: Đặt ở cuối bảng, chữ nghiêng 12pt, căn giữa.")
        format_images_and_captions(doc, args.set_font)
        print("   5. Hình ảnh: Căn giữa, khóa chặt với chú thích bên dưới (keep-with-next).")
        modified = True

    if not args.academic_format and args.style_tables:
        style_all_tables_in_doc(doc, args.set_font, args.font_size)
        print(">> Đã chuẩn hóa style bảng.")
        modified = True

    if not args.academic_format and args.style_captions:
        relocate_and_format_table_captions(doc, args.set_font)
        format_images_and_captions(doc, args.set_font)
        print(">> Đã chuẩn hóa caption bảng & hình.")
        modified = True

    if args.add_toc:
        add_table_of_contents(doc)
        print(">> Đã chèn trường Mục lục tự động (TOC 1-3).")
        modified = True

    if args.add_tof:
        add_table_of_figures(doc)
        print(">> Đã chèn trường Danh mục hình vẽ (TOF).")
        modified = True

    if args.add_tot:
        add_table_of_tables(doc)
        print(">> Đã chèn trường Danh mục bảng biểu (TOT).")
        modified = True

    if modified:
        doc.save(str(out_path))
        print(f">> Thành công! File đã lưu tại: {out_path}")
    else:
        print("Không có tùy chọn định dạng nào được chọn. Dùng --help để xem cú pháp.")


if __name__ == "__main__":
    main()
