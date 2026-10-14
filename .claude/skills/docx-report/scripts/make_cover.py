#!/usr/bin/env python3
"""Sinh phần đầu tài liệu TNUT theo MẪU CHUẨN — hỗ trợ 2 định dạng:
  --kind doan : ĐỒ ÁN PHÂN TÍCH THIẾT KẾ HỆ THỐNG (Bìa chính + Bìa lót + Nhiệm vụ thiết kế)
  --kind btl  : BÁO CÁO BÀI TẬP LỚN          (Bìa + Bìa lót + Đề bài/Nhiệm vụ BTL)

Cách dùng:
    # Đồ án PTTKHT (mặc định)
    python make_cover.py --kind doan --out bia.docx --data data.json
    # Báo cáo bài tập lớn
    python make_cover.py --kind btl --out bia.docx --mon-hoc "CÔNG NGHỆ PHẦN MỀM" \
        --topic "..." --gvhd "..." --sv "..." --lop "K59KMT" --mssv "..." --nam-hoc "2025-2026" --year 2026
    # Ghép phần đầu lên ĐẦU một báo cáo có sẵn
    python make_cover.py --kind btl --prepend-to report.docx --data data.json -o report_full.docx

data.json (mọi trường tùy chọn):
{
  "kind": "doan" | "btl",
  "tieu_de": "<tự suy theo kind nếu bỏ trống>",
  "truong": "TRƯỜNG ĐẠI HỌC KỸ THUẬT CÔNG NGHIỆP",
  "khoa": "KHOA ĐIỆN TỬ", "bo_mon": "CÔNG NGHỆ THÔNG TIN",
  "mon_hoc": "<tên môn học — dùng cho BTL>",
  "nganh": "KỸ THUẬT MÁY TÍNH", "he": "ĐẠI HỌC CHÍNH QUY",
  "de_tai": "...", "gvhd": "...", "sinh_vien": "...", "lop": "...", "mssv": "...",
  "khoa_dao_tao": "2019-2024", "nam_hoc": "2025-2026", "nam": 2024,
  "ngay_giao": "08/09/2024", "ngay_hoan_thanh": "25/10/2024",
  "logo": "<đường dẫn logo>", "border_phu_bia": true
}
"""
import argparse
import json
import sys
from copy import deepcopy
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

FONT = "Times New Roman"
DEFAULT_LOGO = str(Path(__file__).resolve().parent.parent / "assets" / "tnut-logo.png")

TIEU_DE = {
    "doan": "ĐỒ ÁN PHÂN TÍCH THIẾT KẾ HỆ THỐNG",
    "btl": "BÁO CÁO BÀI TẬP LỚN",
}
NHIEM_VU_TITLE = {
    "doan": "NHIỆM VỤ THIẾT KẾ ĐỒ ÁN PTTKHT HỆ THỐNG",
    "btl": "NHIỆM VỤ BÀI TẬP LỚN",
}

DEFAULTS = {
    "kind": "doan",
    "tieu_de": "",                       # để trống -> suy theo kind
    "truong": "TRƯỜNG ĐẠI HỌC KỸ THUẬT CÔNG NGHIỆP",
    "khoa": "KHOA ĐIỆN TỬ",
    "bo_mon": "CÔNG NGHỆ THÔNG TIN",
    "mon_hoc": "",                       # tên môn học (BTL)
    "nganh": "KỸ THUẬT MÁY TÍNH",
    "he": "ĐẠI HỌC CHÍNH QUY",
    # --- Thông tin CÁ NHÂN: KHÔNG hardcode — BẮT BUỘC hỏi người dùng trước khi sinh bìa ---
    "de_tai": "",
    "gvhd": "",
    "sinh_vien": "",
    "lop": "",
    "mssv": "",
    "khoa_dao_tao": "",
    "nam_hoc": "",
    "nam": None,
    "ngay_giao": "",
    "ngay_hoan_thanh": "",
    "logo": DEFAULT_LOGO,
    "border_phu_bia": True,
    "full": False,
    "abbreviations": {},     # {"CSDL": "Cơ sở dữ liệu", "API": "Application Programming Interface"}
}

# Trường bắt buộc phải có (nếu thiếu → script BÁO LỖI, buộc agent hỏi người dùng).
REQUIRED = ("de_tai", "gvhd", "sinh_vien", "lop", "mssv")


def _set_page_border(section):
    """Gắn khung viền trang hoa văn (double-line) cho một section.

    Dùng offsetFrom="text" để khung bám theo LỀ VĂN BẢN (3.5cm trái) — chừa gáy đóng quyển.
    KHÔNG dùng offsetFrom="page" (khung sẽ dính sát mép giấy, không đúng khi đóng quyển).
    """
    from docx.oxml import parse_xml
    from docx.oxml.ns import nsdecls, qn

    sectPr = section._sectPr
    for old in sectPr.findall(qn("w:pgBorders")):
        sectPr.remove(old)
    el = parse_xml(
        f'<w:pgBorders {nsdecls("w")} w:offsetFrom="text">'
        '<w:top w:val="thinThickSmallGap" w:sz="24" w:space="8" w:color="auto"/>'
        '<w:left w:val="thinThickSmallGap" w:sz="24" w:space="8" w:color="auto"/>'
        '<w:bottom w:val="thickThinSmallGap" w:sz="24" w:space="8" w:color="auto"/>'
        '<w:right w:val="thickThinSmallGap" w:sz="24" w:space="8" w:color="auto"/>'
        "</w:pgBorders>"
    )
    cols = sectPr.find(qn("w:cols"))
    if cols is not None:
        cols.addprevious(el)
    else:
        sectPr.append(el)


def _line(doc, text="", size=13, bold=False, italic=False, align=None, before=0, after=0, underline=None):
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_UNDERLINE
    from docx.shared import Pt

    p = doc.add_paragraph()
    if align == "center":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == "justify":
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    elif align == "right":
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    if text:
        r = p.add_run(text)
        r.font.name = FONT
        r.font.size = Pt(size)
        r.bold = bold
        r.italic = italic
        if underline == "double":
            r.underline = WD_UNDERLINE.DOUBLE
        elif underline == "single":
            r.underline = True
    return p


def _logo(doc, logo_path, width_in=1.3):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Inches, Pt

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(6)
    if logo_path and Path(logo_path).exists():
        p.add_run().add_picture(str(logo_path), width=Inches(width_in))
    return p


def _header_block(doc, d):
    _line(doc, d["truong"], 13, bold=True, align="center")
    _line(doc, d["khoa"], 13, bold=True, align="center", underline="double")
    _logo(doc, d.get("logo"))


def _fix_table_widths(table, col_cm):
    """Khóa cứng độ rộng cột (tái tạo tblGrid + tcW) để Word không chia đều cột."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm

    tbl = table._tbl
    tblPr = tbl.tblPr
    for old in tbl.findall(qn("w:tblGrid")):
        tbl.remove(old)
    grid = OxmlElement("w:tblGrid")
    for w in col_cm:
        gc = OxmlElement("w:gridCol")
        gc.set(qn("w:w"), str(int(Cm(w).twips)))
        grid.append(gc)
    tblPr.addnext(grid)
    for row in table.rows:
        for i, cell in enumerate(row.cells):
            if i < len(col_cm):
                cell.width = Cm(col_cm[i])


def _set_table_indent(table, indent_cm):
    """Thụt cả bảng vào trong (giữ khối nhãn/giá trị giống mẫu bìa)."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm

    tblPr = table._tbl.tblPr
    for old in tblPr.findall(qn("w:tblInd")):
        tblPr.remove(old)
    ind = OxmlElement("w:tblInd")
    ind.set(qn("w:w"), str(int(Cm(indent_cm).twips)))
    ind.set(qn("w:type"), "dxa")
    tblW = tblPr.find(qn("w:tblW"))
    if tblW is not None:
        tblW.addnext(ind)
    else:
        tblPr.insert(0, ind)


def _label_value_block(doc, rows, col_cm=(2.7, 0.6, 9.0), font_size=16, indent_cm=1.0):
    """Khối nhãn : giá trị (NGÀNH/HỆ) dạng bảng ẩn viền, cố định độ rộng thay cho tab."""
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt

    t = doc.add_table(rows=0, cols=3)
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False
    t.allow_autofit = False
    for label, value in rows:
        cells = t.add_row().cells
        for i, txt in enumerate((label, ":", value)):
            p = cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(txt)
            r.font.name = FONT
            r.font.size = Pt(font_size)
            r.bold = True
    _fix_table_widths(t, col_cm)
    _set_table_indent(t, indent_cm)
    return t


def _info_table(doc, rows, col_cm=(6.4, 0.5, 6.0), font_size=14):
    """Bảng thông tin SV/GV: nhãn | ':' | giá trị, bề rộng cố định, căn trái."""
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt

    t = doc.add_table(rows=0, cols=3)
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False
    t.allow_autofit = False
    for label, value in rows:
        cells = t.add_row().cells
        for i, txt in enumerate((label, ":", value)):
            p = cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run(txt)
            r.font.name = FONT
            r.font.size = Pt(font_size)
            r.bold = True
    _fix_table_widths(t, col_cm)
    return t


def _two_col_header(doc, left_lines, right_lines, col_cm=(7.6, 8.4), font_size=12):
    """Header 2 cột (trường/khoa | quốc hiệu/tiêu ngữ)."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt

    t = doc.add_table(rows=len(left_lines), cols=2)
    t.autofit = False
    t.allow_autofit = False
    for i in range(len(left_lines)):
        for col, txt in ((0, left_lines[i]), (1, right_lines[i])):
            cell = t.cell(i, col)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(txt)
            r.font.name = FONT
            r.font.size = Pt(font_size)
            r.bold = True
    _fix_table_widths(t, col_cm)
    return t


def _set_table_borders(table, sz=6, color="333333"):
    """Kẻ viền lưới cho bảng (dùng cho Phiếu thông qua)."""
    from docx.oxml import parse_xml
    from docx.oxml.ns import nsdecls

    tblPr = table._tbl.tblPr
    tblPr.append(parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        "</w:tblBorders>"
    ))


def _phieu_thong_qua(doc, d):
    """PHIẾU THÔNG QUA ĐỒ ÁN — bảng theo dõi tiến độ từng tuần (Ngày | Nội dung | GVHD ký)."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    _two_col_header(
        doc, [d["truong"], d["khoa"]],
        ["CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc"],
    )
    _line(doc)
    _line(doc, "PHIẾU THÔNG QUA ĐỒ ÁN", 16, bold=True, align="center")
    _line(doc, "(Từng lần thông qua của giáo viên hướng dẫn)", 12, italic=True, align="center")
    _line(doc)
    t = doc.add_table(rows=6, cols=3)
    t.autofit = False
    t.allow_autofit = False
    headers = ("Ngày", "Nội dung cần chuẩn bị cho lần thông qua tiếp theo", "GVHD ký")
    for j, h in enumerate(headers):
        c = t.cell(0, j); c.text = h
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in c.paragraphs[0].runs:
            r.font.name = FONT; r.bold = True
    _fix_table_widths(t, (3.5, 9.5, 3.0))
    _set_table_borders(t)


def _phieu_ghi_diem(doc, d):
    """PHIẾU GHI ĐIỂM / nhận xét của GVHD."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt

    _two_col_header(
        doc, [d["truong"], d["khoa"]],
        ["CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc"],
    )
    _line(doc)
    _line(doc, "PHIẾU GHI ĐIỂM", 16, bold=True, align="center")
    _line(doc, f"Sinh viên: {d['sinh_vien']}          Lớp: {d['lop']}")
    _line(doc, f"Giáo viên hướng dẫn: {d['gvhd']}")
    _line(doc, f"Đề tài: {d['de_tai']}")
    _line(doc)
    _line(doc, "NHẬN XÉT CỦA GIÁO VIÊN HƯỚNG DẪN", 13, bold=True, align="center")
    for _ in range(4):
        _line(doc, "." * 90, 13)
    _line(doc, "Xếp loại: ..............................        Điểm: ....................")
    _line(doc)
    _line(doc, f"Thái Nguyên, ngày ..... tháng ..... năm {d['nam']}", align="right")
    _line(doc, "GIÁO VIÊN HƯỚNG DẪN", bold=True, align="right")
    _line(doc, "(Ký và ghi rõ họ tên)", italic=True, align="right")


def _danh_muc_viet_tat(doc, d):
    """DANH MỤC CÁC TỪ VIẾT TẮT — bảng ẩn viền: STT | Từ viết tắt | Diễn giải (xếp A–Z)."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt

    abbr = d.get("abbreviations") or {}
    items = sorted(abbr.items(), key=lambda kv: str(kv[0]).upper())
    _line(doc, "DANH MỤC CÁC TỪ VIẾT TẮT", 16, bold=True, align="center")
    _line(doc)
    t = doc.add_table(rows=1, cols=3)
    t.autofit = False
    t.allow_autofit = False
    for j, h in enumerate(("STT", "Từ viết tắt", "Diễn giải")):
        c = t.cell(0, j)
        c.text = ""
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = c.paragraphs[0].add_run(h)
        r.font.name = FONT; r.bold = True; r.font.size = Pt(13)
    rows = items if items else [("...", "...")]
    for i, (k, v) in enumerate(rows, start=1):
        cells = t.add_row().cells
        cells[0].text = str(i); cells[1].text = str(k); cells[2].text = str(v)
        for c in cells:
            for r in c.paragraphs[0].runs:
                r.font.name = FONT; r.font.size = Pt(13)
    _fix_table_widths(t, (1.5, 4.0, 10.5))   # bảng ẩn viền: KHÔNG kẻ border


def _loi_cam_doan(doc, d):
    """LỜI CAM ĐOAN."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Cm, Pt

    _line(doc, "LỜI CAM ĐOAN", 16, bold=True, align="center")
    _line(doc)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(1.27)
    r = p.add_run(
        f'Tôi xin cam đoan đồ án “{d["de_tai"]}” này là công trình nghiên cứu của riêng tôi. '
        "Các số liệu sử dụng trong báo cáo là trung thực. Các kết quả nghiên cứu được trình bày "
        "trong đồ án chưa từng được công bố tại bất kỳ công trình nào khác."
    )
    r.font.name = FONT
    r.font.size = Pt(13)
    _line(doc)
    _line(doc, "Sinh viên thực hiện", bold=True, align="right")
    _line(doc, "(Ký và ghi rõ họ tên)", italic=True, align="right")


def build_front_matter(d):
    """Tạo Document: [Bìa chính] + [Bìa lót] + [Nhiệm vụ / Đề bài] theo kind (doan|btl)."""
    from docx import Document
    from docx.enum.section import WD_SECTION
    from docx.shared import Cm

    kind = d.get("kind", "doan")
    if kind not in TIEU_DE:
        kind = "doan"
    tieu_de = d.get("tieu_de") or TIEU_DE[kind]
    is_btl = (kind == "btl")

    doc = Document()
    for s in doc.sections:
        s.top_margin = Cm(2.0); s.bottom_margin = Cm(2.0)
        s.left_margin = Cm(3.0); s.right_margin = Cm(2.0)

    def subject_lines():
        # Dòng "MÔN HỌC: ..." chỉ hiện cho BTL khi có tên môn
        out = []
        if is_btl and d.get("mon_hoc"):
            out.append(f"MÔN HỌC: {d['mon_hoc']}")
        if is_btl and d.get("nam_hoc"):
            out.append(f"NĂM HỌC: {d['nam_hoc']}")
        return out

    # ---------- [1] BÌA CHÍNH ----------
    _header_block(doc, d)
    for _ in range(2):
        _line(doc)
    _line(doc, tieu_de, 28, bold=True, align="center", after=6)
    for sl in subject_lines():
        _line(doc, sl, 14, bold=True, align="center")
    for _ in range(3):
        _line(doc)
    _label_value_block(doc, [("NGÀNH", d["nganh"]), ("HỆ", d["he"])])
    for _ in range(4):
        _line(doc)
    _line(doc, f"ĐỀ TÀI:  {d['de_tai']}", 16, bold=True, align="center")
    for _ in range(4):
        _line(doc)
    _line(doc, f"THÁI NGUYÊN - {d['nam']}", 14, bold=True, align="center")

    # ---------- [2] BÌA LÓT (phụ bìa) ----------
    doc.add_section(WD_SECTION.NEW_PAGE)
    _header_block(doc, d)
    for _ in range(2):
        _line(doc)
    _line(doc, tieu_de, 28, bold=True, align="center", after=6)
    for sl in subject_lines():
        _line(doc, sl, 14, bold=True, align="center")
    _line(doc, f"BỘ MÔN : {d['bo_mon']}", 16, bold=True, align="center")
    _line(doc, f"ĐỀ TÀI: {d['de_tai']}", 16, bold=True, align="center")
    for _ in range(2):
        _line(doc)
    _info_table(doc, [
        ("GIÁO VIÊN HƯỚNG DẪN", d["gvhd"]),
        ("HỌ VÀ TÊN SINH VIÊN", d["sinh_vien"]),
        ("LỚP", d["lop"]),
        ("MSSV", d["mssv"]),
    ])
    for _ in range(3):
        _line(doc)
    _line(doc, f"THÁI NGUYÊN - {d['nam']}", 14, bold=True, align="center")

    # ---------- [3] NHIỆM VỤ / ĐỀ BÀI ----------
    doc.add_section(WD_SECTION.NEW_PAGE)
    _two_col_header(
        doc,
        [d["truong"], d["khoa"]],
        ["CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Độc lập - Tự do - Hạnh phúc"],
    )
    _line(doc)
    _line(doc, NHIEM_VU_TITLE[kind], 16, bold=True, align="center")
    _line(doc, f"Sinh viên: {d['sinh_vien']}", bold=True)
    _line(doc, f"Lớp: {d['lop']}                Khoá: {d['khoa_dao_tao']}", bold=True)
    _line(doc, f"Bộ môn: {d['bo_mon']}", bold=True)
    _line(doc, f"Giáo viên hướng dẫn: {d['gvhd']}", bold=True)
    if is_btl and d.get("mon_hoc"):
        _line(doc, f"Môn học: {d['mon_hoc']}", bold=True)
    _line(doc, "1. Tên đề tài")
    _line(doc, d["de_tai"], italic=True)
    _line(doc, "2. Các số liệu ban đầu (nếu có)")
    _line(doc, "3. Nội dung các phần thuyết minh và tính toán")
    _line(doc, "- Khảo sát, phân tích hiện trạng của hệ thống")
    _line(doc, "- Phân tích hệ thống thông tin")
    _line(doc, "- Thiết kế hệ thống")
    _line(doc, "- Xây dựng các tệp cơ sở dữ liệu.")
    _line(doc, "- Thiết kế chương trình")
    _line(doc, "4. Các sản phẩm, kết quả:")
    _line(doc, "- Thuyết minh báo cáo")
    _line(doc, "- Demo phần mềm")
    _line(doc, "- Đĩa CD chứa các sơ đồ thiết kế gốc, báo cáo. Nhãn đĩa ghi rõ: Họ tên + lớp + "
              "tên đề tài (tóm tắt) + GV hướng dẫn + Ngày tháng.")
    _line(doc, f"5. Ngày giao nhiệm vụ: {d['ngay_giao']}")
    _line(doc, f"6. Ngày hoàn thành nhiệm vụ: {d['ngay_hoan_thanh']}")
    for _ in range(2):
        _line(doc)
    t = doc.add_table(rows=2, cols=3)
    for i, h in enumerate(("BCN KHOA", "TRƯỞNG BỘ MÔN", "GIÁO VIÊN HƯỚNG DẪN")):
        c = t.cell(0, i); c.text = h
        c.paragraphs[0].alignment = 1
        c2 = t.cell(1, i); c2.text = "(Ký và ghi rõ họ tên)"
        c2.paragraphs[0].alignment = 1

    # ---------- [4..6] CÁC TRANG PHẦN ĐẦU BỔ SUNG (tùy chọn --full) ----------
    if d.get("full"):
        doc.add_section(WD_SECTION.NEW_PAGE)
        _phieu_thong_qua(doc, d)
        doc.add_section(WD_SECTION.NEW_PAGE)
        _phieu_ghi_diem(doc, d)
        doc.add_section(WD_SECTION.NEW_PAGE)
        _loi_cam_doan(doc, d)

    # ---------- [7] DANH MỤC TỪ VIẾT TẮT ----------
    if d.get("full") or d.get("abbreviations"):
        doc.add_section(WD_SECTION.NEW_PAGE)
        _danh_muc_viet_tat(doc, d)

    # ---------- Viền trang cho bìa chính + bìa lót ----------
    secs = list(doc.sections)
    if len(secs) >= 1:
        _set_page_border(secs[0])
    if len(secs) >= 2 and d.get("border_phu_bia", True):
        _set_page_border(secs[1])

    return doc


def build_and_save(d, out_path):
    doc = build_front_matter(d)
    doc.save(str(out_path))
    return out_path


def prepend_to(target_path, d, out_path):
    """Ghép BÌA + BÌA LÓT + NHIỆM VỤ lên ĐẦU file báo cáo có sẵn (giữ nguyên nội dung báo cáo)."""
    from docx import Document
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    cover = build_front_matter(d)
    report = Document(str(target_path))

    cover_body = cover.element.body
    report_body = report.element.body

    cover_children = list(cover_body)
    cover_final_sectPr = cover_body.find(qn("w:sectPr"))
    if cover_final_sectPr is not None:
        cover_children.remove(cover_final_sectPr)

    for offset, el in enumerate(cover_children):
        report_body.insert(offset, deepcopy(el))

    # Đoạn ranh mang sectPr đóng section cuối của bìa (đặt SAU nội dung bìa, TRƯỚC báo cáo)
    brk = OxmlElement("w:p")
    report_body.insert(len(cover_children), brk)
    if cover_final_sectPr is not None:
        pPr = brk.get_or_add_pPr()
        pPr.append(deepcopy(cover_final_sectPr))

    report.save(str(out_path))
    return out_path


def main():
    ap = argparse.ArgumentParser(description="Sinh bìa đồ án PTTKHT / báo cáo bài tập lớn (mẫu TNUT).")
    ap.add_argument("--kind", choices=["doan", "btl"], default=None,
                    help="Định dạng: 'doan' = Đồ án PTTKHT, 'btl' = Báo cáo bài tập lớn (mặc định: doan)")
    ap.add_argument("--out", help="File .docx xuất ra (chế độ tạo bìa riêng)")
    ap.add_argument("--prepend-to", help="File báo cáo .docx để ghép bìa lên đầu")
    ap.add_argument("-o", "--output", help="File xuất ra khi dùng --prepend-to")
    ap.add_argument("--data", help="File JSON chứa các trường thông tin")
    ap.add_argument("--full", action="store_true",
                    help="Thêm các trang phần đầu: Phiếu thông qua đồ án, Phiếu ghi điểm, Lời cam đoan, Danh mục từ viết tắt")
    ap.add_argument("--abbr", help="Danh mục từ viết tắt: 'CSDL:Cơ sở dữ liệu;API:Application Programming Interface'")
    for k in ("tieu-de", "truong", "khoa-donvi", "mon-hoc", "bo-mon", "nganh", "he",
              "topic", "gvhd", "sv", "lop", "mssv", "khoa-dao-tao", "nam-hoc",
              "ngay-giao", "ngay-ht", "logo"):
        ap.add_argument(f"--{k}")
    ap.add_argument("--year", type=int)
    args = ap.parse_args()

    d = dict(DEFAULTS)
    if args.data:
        d.update(json.loads(Path(args.data).read_text(encoding="utf-8")))

    mapping = {
        "kind": args.kind, "tieu_de": args.tieu_de, "truong": args.truong,
        "khoa": args.khoa_donvi, "mon_hoc": args.mon_hoc, "bo_mon": args.bo_mon,
        "nganh": args.nganh, "he": args.he, "de_tai": args.topic, "gvhd": args.gvhd,
        "sinh_vien": args.sv, "lop": args.lop, "mssv": args.mssv,
        "khoa_dao_tao": args.khoa_dao_tao, "nam_hoc": args.nam_hoc,
        "ngay_giao": args.ngay_giao, "ngay_hoan_thanh": args.ngay_ht, "logo": args.logo,
        "nam": args.year,
    }
    for k, v in mapping.items():
        if v is not None:
            d[k] = v
    if args.full:
        d["full"] = True
    if args.abbr:
        d["abbreviations"] = dict(d.get("abbreviations") or {})
        for pair in args.abbr.split(";"):
            if ":" in pair:
                k, v = pair.split(":", 1)
                d["abbreviations"][k.strip()] = v.strip()

    # Năm mặc định = năm hiện tại (không hardcode)
    if not d.get("nam"):
        import datetime
        d["nam"] = datetime.date.today().year

    # BẮT BUỘC: đủ thông tin cá nhân. Thiếu → LỖI, buộc agent HỎI người dùng.
    missing = [k for k in REQUIRED if not d.get(k)]
    if d.get("kind") == "btl" and not d.get("mon_hoc"):
        missing.append("mon_hoc")
    if missing:
        sys.exit(
            "LỖI: Thiếu thông tin bắt buộc: " + ", ".join(missing) + ".\n"
            "→ PHẢI HỎI NGƯỜI DÙNG (từng câu một, kèm gợi ý trả lời) trước khi sinh bìa.\n"
            "   Trường cần: --topic --gvhd --sv --lop --mssv "
            "(+ --mon-hoc --nam-hoc nếu --kind btl)."
        )

    if args.prepend_to:
        out = args.output or (Path(args.prepend_to).stem + "_full.docx")
        prepend_to(args.prepend_to, d, out)
        print(f">> Đã ghép bìa ({d['kind']}) lên đầu báo cáo: {out}")
    elif args.out:
        build_and_save(d, args.out)
        print(f">> Đã tạo phần bìa ({d['kind']}): {args.out}")
    else:
        ap.error("Cần --out hoặc --prepend-to")


if __name__ == "__main__":
    main()
