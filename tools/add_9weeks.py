#!/usr/bin/env python3
"""Them du 9 tuan cho bang theo doi thong qua (TABLE 4) - o Ngay/GVHD de trong de ky tay."""
from docx import Document
from docx.shared import Pt

SRC = r"C:\Users\My PC\Documents\DOCX\BAO_CAO_PTTKHT_DA_SUA.docx"
DST = r"C:\Users\MYPC~1\AppData\Local\Temp\opencode\DA_SUA_w9.docx"

NOIDUNG = [
    "Nhận nhiệm vụ đồ án, chốt tên đề tài và đề cương các chương; lập kế hoạch khảo sát.",
    "Khảo sát thực tế tại Thái Nguyên, phân tích 5W1H, chốt quy trình hiện tại và các bất cập (Chương 1).",
    "Đặc tả yêu cầu chức năng/phi chức năng, quy tắc nghiệp vụ và ma trận truy vết (Chương 2).",
    "Vẽ Use Case tổng quan, sơ đồ hoạt động, tuần tự và vòng đời trạng thái (Chương 2).",
    "Thiết kế CSDL, ERD, sơ đồ lớp, kiến trúc hệ thống và danh mục API (Chương 3).",
    "Cài đặt các chức năng chính: OTP, gửi/chấp nhận kết nối, nhắn tin thời gian thực (Chương 4).",
    "Kiểm thử chức năng, rà soát OWASP Top 10 và bảo vệ dữ liệu cá nhân (Chương 4).",
    "Hoàn thiện báo cáo, danh mục hình/bảng, kiểm tra chính tả và định dạng.",
    "Thông qua toàn bộ đồ án với GVHD, chuẩn bị slide và demo bảo vệ.",
]

doc = Document(SRC)
tbl = doc.tables[4]
hdr = [c.text.strip() for c in tbl.rows[0].cells]
assert "GVHD" in hdr[2], hdr
assert "qua" in hdr[1].lower(), hdr
# Them dong cho du 9 dong noi dung (dang co len(tbl.rows)-1 dong)
while len(tbl.rows) < 10:
    tbl.add_row()
assert len(tbl.rows) == 10, len(tbl.rows)
for i, nd in enumerate(NOIDUNG, start=1):
    row = tbl.rows[i]
    # Cot Ngay + GVHD ky de trong; chi dien cot Noi dung
    for ci, txt in ((1, "Tuần %d: %s" % (i, nd)),):
        cell = row.cells[ci]
        cell.text = ""
        p = cell.paragraphs[0]
        r = p.add_run(txt)
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)
doc.save(DST)
d2 = Document(DST)
print("rows:", len(d2.tables[4].rows))
print("OK", DST)
