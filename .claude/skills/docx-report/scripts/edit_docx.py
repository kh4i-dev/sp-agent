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
import re
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
    from docx.shared import Cm, Pt, RGBColor

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
            # KHÓA HEADING 1: luôn bắt đầu ở đầu trang mới (page-break-before)
            if _heading_level(p) == 1:
                p.paragraph_format.page_break_before = True
            # HEADING CŨNG PHẢI LÀ TIMES NEW ROMAN, MÀU ĐEN, KHÔNG NGHIÊNG
            for r in p.runs:
                r.font.name = font_name
                r.font.italic = False
                r.font.color.rgb = RGBColor(0, 0, 0)
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


def _heading_level(p) -> int:
    """Trả về cấp Heading (1-5) của paragraph; 0 nếu không phải Heading."""
    name = (p.style.name or "").lower()
    if "heading" not in name and "tiêu đề" not in name:
        return 0
    for ch in name:
        if ch.isdigit():
            return int(ch)
    return 1


def _paragraph_has_image(p) -> bool:
    """True nếu paragraph chứa ảnh (DrawingML `w:drawing` hoặc VML `w:pict`).

    CẢNH BÁO: TUYỆT ĐỐI KHÔNG dùng `'drawing' in p._p.xml` — chuỗi namespace
    `.../drawingml/...` xuất hiện trong XML của MỌI paragraph nên điều kiện
    luôn đúng, khiến toàn bộ tài liệu bị căn giữa oan.
    """
    from docx.oxml.ns import qn

    return bool(p._p.findall(".//" + qn("w:drawing"))) or bool(p._p.findall(".//" + qn("w:pict")))


def format_heading_styles(doc, font_name="Times New Roman", sizes_pt=(16, 14, 13, 12, 12)):
    """Chuẩn hóa style Heading 1..5 theo chuẩn học thuật:
    - Font Times New Roman, MÀU ĐEN (0,0,0), KHÔNG in nghiêng.
    - Heading 1: BẮT BUỘC page_break_before=True (khóa luôn nằm đầu trang mới).
    - Heading 2/3/4/5: keep_with_next=True (không mồ côi), KHÔNG ép ngắt trang.
    """
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor

    for level in range(1, 6):
        try:
            st = doc.styles[f"Heading {level}"]
        except KeyError:
            continue

        # 1. Font + màu + không nghiêng ở cấp STYLE (Styles Gallery)
        st.font.name = font_name
        st.font.italic = False
        st.font.bold = True
        st.font.color.rgb = RGBColor(0, 0, 0)
        if level - 1 < len(sizes_pt):
            st.font.size = Pt(sizes_pt[level - 1])

        # 2. Ép cả w:rFonts (ascii/hAnsi/eastAsia/cs) để Word không fallback font
        rpr = st.element.get_or_add_rPr()
        rfonts = rpr.find(qn("w:rFonts"))
        if rfonts is None:
            rfonts = OxmlElement("w:rFonts")
            rpr.insert(0, rfonts)
        for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
            rfonts.set(qn(attr), font_name)

        pf = st.paragraph_format
        if level == 1:
            pf.page_break_before = True   # KHÓA HEADING 1 LUÔN ĐẦU TRANG MỚI
        pf.keep_with_next = True

    # 3. Chuẩn hóa mọi paragraph Heading thực tế đang dùng trong tài liệu
    for p in doc.paragraphs:
        lvl = _heading_level(p)
        if lvl == 0:
            continue
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.keep_with_next = True
        if lvl == 1:
            p.paragraph_format.page_break_before = True
        for r in p.runs:
            r.font.name = font_name
            r.font.italic = False
            r.font.color.rgb = RGBColor(0, 0, 0)


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


def style_all_tables_in_doc(doc, font_name="Times New Roman", font_size_pt=11):
    """Áp dụng style chuẩn cho tất cả bảng biểu trong tài liệu (mặc định 11pt theo chuẩn 10.5–12)."""
    for table in doc.tables:
        style_table(table, font_name, font_size_pt)


def _is_caption_text(text: str, kind: str) -> bool:
    """Nhận diện caption bảng/hình dạng 'Bảng 3.1: ...' / 'Hình 2.4: ...'."""
    t = text.strip()
    return t.startswith(kind + " ") and (":" in t or "." in t)


def relocate_captions_below(doc):
    """Di chuyển caption về ĐÚNG VỊ TRÍ chuẩn của skill:
    - Caption bảng ('Bảng X.Y: ...') phải nằm NGAY DƯỚI bảng.
    - Caption hình ('Hình X.Y: ...') phải nằm NGAY DƯỚI hình.
    Nếu caption đang nằm TRÊN bảng/hình, hàm di chuyển xuống dưới.
    An toàn: chỉ di chuyển paragraph (không tạo/xóa nội dung), bỏ qua dòng trống chen giữa.
    """
    # 1. Bảng: caption nằm ngay trước bảng -> chuyển xuống sau bảng
    for table in list(doc.tables):
        tbl = table._tbl
        prev = tbl.getprevious()
        while prev is not None and prev.tag.endswith("}p") and not "".join(prev.itertext()).strip():
            prev = prev.getprevious()
        if prev is not None and prev.tag.endswith("}p") and _is_caption_text("".join(prev.itertext()), "Bảng"):
            tbl.addnext(prev)

    # 2. Hình: caption nằm ngay trước paragraph chứa ảnh -> chuyển xuống sau ảnh
    for p in list(doc.paragraphs):
        if not _paragraph_has_image(p):
            continue
        prev = p._p.getprevious()
        while prev is not None and prev.tag.endswith("}p") and not "".join(prev.itertext()).strip():
            prev = prev.getprevious()
        if prev is not None and prev.tag.endswith("}p") and _is_caption_text("".join(prev.itertext()), "Hình"):
            p._p.addnext(prev)


def format_table_captions(doc, font_name="Times New Roman"):
    """Định dạng caption bảng: chữ thường in nghiêng, căn giữa, không bold, cỡ 12pt.
    (Vị trí đã được đảm bảo bởi relocate_captions_below)."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Cm, Pt

    for p in doc.paragraphs:
        if _is_caption_text(p.text, "Bảng"):
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
        if _paragraph_has_image(p):
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


def insert_field_code(doc, field_instr: str, title: str = None, font_name="Times New Roman"):
    """Chèn trường tự động Word (Field Codes như TOC, TOF, TOT).

    Dùng OxmlElement + set attribute (KHÔNG nối chuỗi XML) để tránh lỗi
    XMLSyntaxError khi instr chứa dấu ngoặc kép, ví dụ: TOC \\o "1-3".
    Tiêu đề tự động (nếu có) được tạo bằng Heading 1 + Times New Roman + ngắt trang.
    """
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import RGBColor

    if title:
        h = doc.add_paragraph(title, style="Heading 1")
        h.paragraph_format.page_break_before = True   # Mục lục/danh mục bắt đầu trang mới
        h.paragraph_format.keep_with_next = True
        for r in h.runs:
            r.font.name = font_name
            r.font.italic = False
            r.font.color.rgb = RGBColor(0, 0, 0)

    p = doc.add_paragraph()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), field_instr)
    p._p.append(fld)


def add_table_of_contents(doc, title="MỤC LỤC", font_name="Times New Roman"):
    insert_field_code(doc, r'TOC \o "1-3" \h \z \u', title, font_name)


def add_table_of_figures(doc, title="DANH MỤC HÌNH VẼ", font_name="Times New Roman"):
    insert_field_code(doc, r'TOC \c "Hình" \h \z', title, font_name)


def add_table_of_tables(doc, title="DANH MỤC BẢNG BIỂU", font_name="Times New Roman"):
    insert_field_code(doc, r'TOC \c "Bảng" \h \z', title, font_name)


def _build_page_field_run(run):
    """Gắn field PAGE { begin | instrText | separate | '1' | end } vào một run."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    fld_begin = OxmlElement("w:fldChar"); fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText"); instr.set(qn("xml:space"), "preserve"); instr.text = " PAGE "
    fld_sep = OxmlElement("w:fldChar"); fld_sep.set(qn("w:fldCharType"), "separate")
    fld_txt = OxmlElement("w:t"); fld_txt.text = "1"
    fld_end = OxmlElement("w:fldChar"); fld_end.set(qn("w:fldCharType"), "end")
    for node in (fld_begin, instr, fld_sep, fld_txt, fld_end):
        run._r.append(node)


def _clear_footer(section):
    """Gỡ nội dung footer của section (dùng cho trang bìa KHÔNG đánh số)."""
    footer = section.footer
    footer.is_linked_to_previous = False
    for p in footer.paragraphs:
        for r in list(p.runs):
            r._r.getparent().remove(r._r)


def _write_page_field(section, font_name="Times New Roman", position="center"):
    """Ghi field PAGE vào footer của 1 section, căn giữa/phải, TNR 12pt."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt

    align = WD_ALIGN_PARAGRAPH.RIGHT if position == "right" else WD_ALIGN_PARAGRAPH.CENTER
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    for r in list(p.runs):
        r._r.getparent().remove(r._r)
    p.alignment = align
    run = p.add_run()
    run.font.name = font_name
    run.font.size = Pt(12)
    _build_page_field_run(run)


def _set_pgnumtype(section, fmt=None, start=None):
    """Đặt <w:pgNumType w:fmt=... w:start=.../> cho section (La Mã / Ả Rập / reset số trang)."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    sectPr = section._sectPr
    for old in sectPr.findall(qn("w:pgNumType")):
        sectPr.remove(old)
    el = OxmlElement("w:pgNumType")
    if fmt:
        el.set(qn("w:fmt"), fmt)
    if start is not None:
        el.set(qn("w:start"), str(start))
    cols = sectPr.find(qn("w:cols"))
    if cols is not None:
        cols.addprevious(el)          # đúng thứ tự schema: pgNumType đứng trước cols
    else:
        sectPr.append(el)


def _find_paragraph(doc, marker: str):
    """Tìm paragraph đầu tiên khớp marker (ưu tiên startswith, không phân biệt hoa thường)."""
    m = marker.strip().lower()
    for p in doc.paragraphs:
        if p.text.strip().lower().startswith(m):
            return p
    for p in doc.paragraphs:
        if m in p.text.strip().lower():
            return p
    return None


def _insert_section_break_before(doc, target_p):
    """Chèn Section Break (Next Page) ngay TRƯỚC paragraph target_p.

    OOXML: section break nằm trong <w:pPr><w:sectPr> của paragraph CUỐI section
    trước đó. Vì vậy ta sao bản sao sectPr hiện hành vào pPr của paragraph liền
    trước target_p. Giả định tài liệu đang ở 1 section (đúng cho văn bản mới);
    với tài liệu đã nhiều section phức tạp nên tách tay trong Word.
    """
    from copy import deepcopy
    from docx.oxml.ns import qn

    prev = target_p._p.getprevious()
    while prev is not None and not prev.tag.endswith("}p"):
        prev = prev.getprevious()
    if prev is None:
        raise ValueError("Không tìm được đoạn liền trước mốc để chèn Section Break.")
    if not prev.tag.endswith("}p"):
        raise ValueError("Phần tử liền trước mốc không phải paragraph.")

    body_sectPr = doc.element.body.find(qn("w:sectPr"))
    if body_sectPr is None:
        raise ValueError("Không tìm thấy <w:sectPr> gốc của tài liệu.")

    new_sectPr = deepcopy(body_sectPr)
    for old in new_sectPr.findall(qn("w:pgNumType")):
        new_sectPr.remove(old)

    pPr = prev.get_or_add_pPr()
    for old in pPr.findall(qn("w:sectPr")):
        pPr.remove(old)
    pPr.append(new_sectPr)


def setup_academic_page_numbering(doc, cover_end_text=None, body_start_text=None,
                                  font_name="Times New Roman"):
    """Đánh số trang chuẩn đồ án với 2 mốc tách Section:
      - `cover_end_text`: mốc BẮT ĐẦU phần đầu (VD 'LỜI CAM ĐOAN'). Trước mốc = BÌA (không đánh số).
      - `body_start_text`: mốc BẮT ĐẦU thân bài (VD 'MỞ ĐẦU' / 'CHƯƠNG 1'). Từ mốc = Ả Rập, bắt đầu lại từ 1.

    Kết quả:
      - Chỉ body_start  → 2 section: front-matter (La Mã i,ii) | thân bài (Ả Rập từ 1).
      - Chỉ cover_end   → 2 section: bìa (không số)        | phần sau (Ả Rập từ 1).
      - Cả hai mốc      → 3 section: bìa (không số) | front-matter (La Mã) | thân bài (Ả Rập từ 1).
    """
    break_points = []
    for marker in (cover_end_text, body_start_text):
        if not marker:
            continue
        p = _find_paragraph(doc, marker)
        if p is None:
            raise ValueError(f"Không tìm thấy mốc để tách section: {marker!r}")
        break_points.append(p)

    break_points.sort(key=lambda p: list(doc.element.body).index(p._p))  # theo thứ tự tài liệu
    for p in break_points:
        _insert_section_break_before(doc, p)

    sections = list(doc.sections)
    n = len(sections)

    if cover_end_text and body_start_text and n >= 3:
        cover, front, body = sections[0], sections[1], sections[-1]
        _clear_footer(cover)
        _set_pgnumtype(front, fmt="lowerRoman", start=1); _write_page_field(front, font_name)
        _set_pgnumtype(body, fmt="decimal", start=1);    _write_page_field(body, font_name)
    elif body_start_text and n >= 2:
        front, body = sections[0], sections[-1]
        _set_pgnumtype(front, fmt="lowerRoman", start=1); _write_page_field(front, font_name)
        _set_pgnumtype(body, fmt="decimal", start=1);    _write_page_field(body, font_name)
    elif cover_end_text and n >= 2:
        cover, body = sections[0], sections[-1]
        _clear_footer(cover)
        _set_pgnumtype(body, fmt="decimal", start=1);    _write_page_field(body, font_name)
    else:
        add_page_numbers(doc, font_name)


def add_page_numbers(doc, font_name="Times New Roman", position="center"):
    """Đánh số trang LIÊN TỤC (Ả Rập) cho MỌI section, ghi vào footer.
    Muốn La Mã cho front-matter + reset Ả Rập từ Chương 1, dùng
    setup_academic_page_numbering() qua cờ --cover-end / --body-start."""
    for section in doc.sections:
        _write_page_field(section, font_name, position)


CAPTION_RE = re.compile(r"^(Hình|Bảng)\s+(\d+(?:\.\d+)?)\s*[:.]\s*(.+)$")
REF_RE = re.compile(r"(Hình|Bảng)\s+(\d+(?:\.\d+)?)")


def _append_field(run, instr, placeholder="1"):
    """Gắn 1 field Word (begin|instrText|separate|'placeholder'|end) vào run hiện có."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    seq = [
        ("w:fldChar", qn("w:fldCharType"), "begin"),
        ("w:instrText", qn("xml:space"), "preserve"),
        ("w:fldChar", qn("w:fldCharType"), "separate"),
        ("w:t", None, None),
        ("w:fldChar", qn("w:fldCharType"), "end"),
    ]
    for tag, attr, val in seq:
        e = OxmlElement(tag)
        if attr is not None:
            e.set(attr, val)
        if tag == "w:instrText":
            e.text = instr
        elif tag == "w:t":
            e.text = placeholder
        run._r.append(e)


def _clear_runs(p):
    from docx.oxml.ns import qn

    for r in list(p.runs):
        r._r.getparent().remove(r._r)
    for f in p._p.findall(qn("w:fldSimple")):
        p._p.remove(f)


def number_captions(doc, chapter_based=True, link_refs=True, font_name="Times New Roman"):
    """Tự đánh số caption bằng field (SEQ + STYLEREF) + bookmark, và biến các tham chiếu
    dạng text ("Hình 3.2" / "Bảng 3.2") trong thân bài thành field REF (cross-reference).

    - Figure caption: 'Hình <chương>.<SEQ Hình>'  → tự cập nhật khi chèn/xóa.
    - Table caption : 'Bảng <chương>.<SEQ Bảng>'.
      Số chương lấy từ tiêu đề Heading 1 dạng 'CHƯƠNG N'; SEQ tự tăng và reset theo chương.
    - chapter_based=False → chỉ dùng SEQ (Hình 1, 2, 3...).
    Chỉ chạy trên caption dạng text 'Hình X.Y: Tên' / 'Bảng X.Y: Tên' (số đang gõ tay).
    Numbering chỉ hiển thị đúng sau khi Word cập nhật field (render_docx dùng Word COM tự update).
    """
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Pt

    def _run(p, text=None):
        r = p.add_run(text or "")
        r.font.name = font_name
        r.font.size = Pt(12)
        r.font.italic = True
        r.font.bold = False
        return r

    chap_re = re.compile(r"CHƯƠNG\s+(\d+)", re.IGNORECASE)
    captions = []
    current_chapter = None
    for p in doc.paragraphs:
        if (p.style.name or "").startswith("Heading 1"):
            mc = chap_re.search(p.text)
            if mc:
                current_chapter = int(mc.group(1))
        m = CAPTION_RE.match(p.text.strip())
        if m:
            captions.append((p, m.group(1), m.group(2), m.group(3).strip(), current_chapter))

    label_to_bm = {}
    bid = 7000
    for idx, (p, kind, number, title, chapter) in enumerate(captions, start=1):
        seq_name = kind  # 'Hình' / 'Bảng' — trùng với TOC \c "Hình"/"Bảng"
        bm = f"_Ref_{'Hinh' if kind == 'Hình' else 'Bang'}_{idx}"
        label_to_bm[f"{kind} {number}"] = bm

        _clear_runs(p)
        _run(p, f"{kind} ")
        bms = OxmlElement("w:bookmarkStart")
        bms.set(qn("w:id"), str(bid)); bms.set(qn("w:name"), bm)
        p._p.append(bms)
        if chapter_based and chapter is not None:
            _run(p, f"{chapter}.")  # số chương (lấy từ Heading 1 'CHƯƠNG N')
        if chapter_based:
            _append_field(_run(p), rf"SEQ {seq_name} \* ARABIC \s 1", "1")   # tự tăng, reset theo chương
        else:
            _append_field(_run(p), rf"SEQ {seq_name} \* ARABIC", "1")
        bme = OxmlElement("w:bookmarkEnd")
        bme.set(qn("w:id"), str(bid))
        p._p.append(bme)
        _run(p, f": {title}")
        bid += 1

        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = 0

    # Cross-reference: thay 'Hình 3.2'/'Bảng 3.2' trong thân bài bằng field REF
    if link_refs:
        for p in doc.paragraphs:
            if CAPTION_RE.match(p.text.strip()):
                continue
            text = p.text
            matches = [m for m in REF_RE.finditer(text) if f"{m.group(1)} {m.group(2)}" in label_to_bm]
            if not matches:
                continue
            tokens, last = [], 0
            for m in matches:
                label = f"{m.group(1)} {m.group(2)}"
                tokens.append(("t", text[last:m.start()]))
                tokens.append(("ref", m.group(1), label_to_bm[label], m.group(2)))
                last = m.end()
            tokens.append(("t", text[last:]))

            _clear_runs(p)
            for tok in tokens:
                if tok[0] == "t":
                    if tok[1]:
                        r = p.add_run(tok[1]); r.font.name = font_name; r.font.size = Pt(13)
                else:
                    r = p.add_run(tok[1] + " "); r.font.name = font_name; r.font.size = Pt(13)
                    rf = p.add_run(); rf.font.name = font_name; rf.font.size = Pt(13)
                    _append_field(rf, rf"REF {tok[2]} \h", tok[3])

    return len(captions)


def main():
    ap = argparse.ArgumentParser(description="Chỉnh sửa nội dung, style bảng và chuẩn hóa học thuật cho file Word .docx.")
    ap.add_argument("docx", help="Đường dẫn file .docx")
    ap.add_argument("-o", "--output", help="Đường dẫn file xuất ra")
    ap.add_argument("--academic-format", action="store_true",
                    help="Áp dụng toàn bộ quy chuẩn học thuật: Thụt lề 1 tab (1.27cm), căn đều 2 bên (Justify), lề giấy 3.5/2.0/3.0/3.0 cm, giãn dòng 1.35, giãn đoạn, style bảng & caption")
    ap.add_argument("--set-font", default="Times New Roman", help="Đặt tên font (mặc định: 'Times New Roman')")
    ap.add_argument("--font-size", type=float, default=13.0, help="Đặt cỡ chữ thân bài pt (mặc định: 13.0)")
    ap.add_argument("--table-font-size", type=float, default=11.0, help="Cỡ chữ trong bảng pt (mặc định: 11.0, chuẩn 10.5–12)")
    ap.add_argument("--indent-cm", type=float, default=1.27, help="Khoảng cách thụt đầu dòng cm (mặc định: 1.27 cm / 1 tab)")
    ap.add_argument("--line-spacing", type=float, default=1.35, help="Hệ số giãn dòng (mặc định: 1.35 lines)")
    ap.add_argument("--style-tables", action="store_true", help="Chuẩn hóa style bảng (Header in đậm căn trái, nền trắng, cantSplit; tblHeader)")
    ap.add_argument("--style-headings", action="store_true", help="Chuẩn hóa heading: Times New Roman màu đen; Heading 1 khóa đầu trang mới (page-break-before); Heading 2-5 keep-with-next")
    ap.add_argument("--style-captions", action="store_true", help="Chuẩn hóa caption bảng đặt ở cuối bảng và caption hình")
    ap.add_argument("--add-toc", action="store_true", help="Chèn Mục lục tự động (TOC 1-3)")
    ap.add_argument("--add-tof", action="store_true", help="Chèn Danh mục hình vẽ (TOF)")
    ap.add_argument("--add-tot", action="store_true", help="Chèn Danh mục bảng biểu (TOT)")
    ap.add_argument("--add-page-numbers", action="store_true", help="Chèn số trang tự động (field PAGE) vào footer các section (đánh liên tục)")
    ap.add_argument("--cover-end", metavar="TEXT", help="Mốc bắt đầu front-matter (VD 'LỜI CAM ĐOAN'); trước mốc = BÌA không đánh số. Kích hoạt tách Section")
    ap.add_argument("--body-start", metavar="TEXT", help="Mốc bắt đầu thân bài (VD 'MỞ ĐẦU' / 'CHƯƠNG 1'); từ mốc = số Ả Rập bắt đầu lại từ 1")
    ap.add_argument("--number-captions", action="store_true",
                    help="Tự đánh số caption bằng field (SEQ+STYLEREF) + bookmark; biến tham chiếu 'Hình 3.2'/'Bảng 3.2' trong bài thành REF (cross-reference)")
    ap.add_argument("--caption-plain", action="store_true",
                    help="Khi --number-captions: đánh số đơn giản (Hình 1,2,3...) thay vì theo chương (Hình 2.1)")
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
        format_heading_styles(doc, args.set_font)
        print("   3. Heading: Times New Roman màu đen không nghiêng; Heading 1 KHÓA đầu trang mới (page-break-before); Heading 2-5 keep-with-next.")
        style_all_tables_in_doc(doc, args.set_font, args.table_font_size)
        print(f"   4. Bảng biểu: Header in đậm căn trái, nền trắng 100%, cỡ {args.table_font_size}pt, lặp header & chống gãy hàng.")
        n = relocate_captions_below(doc)
        format_table_captions(doc, args.set_font)
        print("   5. Caption bảng: đưa về NGAY DƯỚI bảng, chữ nghiêng 12pt, căn giữa.")
        format_images_and_captions(doc, args.set_font)
        print("   6. Hình ảnh: Căn giữa, khóa chặt với chú thích bên dưới (keep-with-next).")
        modified = True

    if not args.academic_format and args.style_headings:
        format_heading_styles(doc, args.set_font)
        print(">> Đã chuẩn hóa heading: Times New Roman màu đen; Heading 1 khóa đầu trang mới; Heading 2-5 keep-with-next.")
        modified = True

    if not args.academic_format and args.style_tables:
        style_all_tables_in_doc(doc, args.set_font, args.table_font_size)
        print(">> Đã chuẩn hóa style bảng.")
        modified = True

    if not args.academic_format and args.style_captions:
        relocate_captions_below(doc)
        format_table_captions(doc, args.set_font)
        format_images_and_captions(doc, args.set_font)
        print(">> Đã chuẩn hóa caption bảng (về dưới bảng) & hình.")
        modified = True

    if args.add_toc:
        add_table_of_contents(doc, font_name=args.set_font)
        print(">> Đã chèn trường Mục lục tự động (TOC 1-3).")
        modified = True

    if args.add_tof:
        add_table_of_figures(doc, font_name=args.set_font)
        print(">> Đã chèn trường Danh mục hình vẽ (TOF).")
        modified = True

    if args.add_tot:
        add_table_of_tables(doc, font_name=args.set_font)
        print(">> Đã chèn trường Danh mục bảng biểu (TOT).")
        modified = True

    if args.cover_end or args.body_start:
        setup_academic_page_numbering(doc, args.cover_end, args.body_start, args.set_font)
        print(">> Đã tách Section & đánh số trang: BÌA (không số) | FRONT-MATTER (La Mã i,ii) | THÂN BÀI (Ả Rập từ 1).")
        modified = True
    elif args.add_page_numbers:
        add_page_numbers(doc, args.set_font)
        print(">> Đã chèn số trang tự động (field PAGE, liên tục) vào footer các section.")
        modified = True

    if args.number_captions:
        n = number_captions(doc, chapter_based=not args.caption_plain, font_name=args.set_font)
        print(f">> Đã đánh số {n} caption bằng field (SEQ+STYLEREF) + bookmark, và liên kết tham chiếu (REF).")
        modified = True

    if modified:
        doc.save(str(out_path))
        print(f">> Thành công! File đã lưu tại: {out_path}")
    else:
        print("Không có tùy chọn định dạng nào được chọn. Dùng --help để xem cú pháp.")


if __name__ == "__main__":
    main()
