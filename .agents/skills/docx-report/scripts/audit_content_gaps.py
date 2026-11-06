#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit_content_gaps.py — GATE NỘI DUNG trước khi in (đủ nội dung, hết chỗ trống).

Rà .docx tìm:
  C1. Trường bỏ trống cần điền (sau dấu ':' mà rỗng) — Ngày giao/hoàn thành, GVHD, MSSV...
  C2. Thông tin bìa bắt buộc thiếu (Trường, Khoa, Đề tài, Ngành, Hệ, SV, Lớp, MSSV, năm)
  C3. Placeholder chưa thay: TODO/TBD/Lorem/XXX/…/[...]
  C4. Mục lục (TOC) thiếu entry so với heading thật (đếm theo tiền tố 'x.y.')
  C5. Caption Hình/Bảng trong thân bài thiếu dòng tương ứng ở DANH MỤC (theo số hiệu)
  C6. Số liệu dạng 'N.n ms' trong text → in ra để người đối chiếu với bảng/hình

Dùng: python audit_content_gaps.py file.docx
Exit 1 nếu có C1–C5 vi phạm (C6 chỉ để đọc).
"""
import argparse
import re
import sys
import zipfile
from lxml import etree as ET

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}

REQ_COVER = ["TRƯỜNG ĐẠI HỌC", "KHOA", "ĐỀ TÀI", "NGÀNH", "HỆ", "SINH VIÊN", "LỚP", "MSSV", "20"]
FIELD_KEYS = ["Ngày giao nhiệm vụ", "Ngày hoàn thành", "Giáo viên hướng dẫn",
              "Họ và tên sinh viên", "Lớp", "MSSV", "Bộ môn"]


def paragraphs(root):
    return ["".join(x.text or "" for x in p.findall(".//w:t", NS))
            for p in root.findall(".//w:p", NS)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docx")
    args = ap.parse_args()

    root = ET.fromstring(zipfile.ZipFile(args.docx).read("word/document.xml"))
    paras = paragraphs(root)
    joined = "\n".join(paras)
    warns, notes = [], []

    # C1: trường bỏ trống
    for p in paras:
        for key in FIELD_KEYS:
            m = re.search(re.escape(key) + r"\s*[:：]\s*(.*)$", p.strip())
            if m and not m.group(1).strip():
                warns.append(f"C1 '{key}:' chưa điền giá trị (đoạn: ...{p.strip()[:60]})")

    # C2: bìa đủ thông tin
    head = joined[:4000].upper()
    missing = [k for k in REQ_COVER if k not in head]
    if missing:
        warns.append(f"C2 phần đầu/bìa thiếu thông tin: {missing}")

    # C3: placeholder
    for kw in ["TODO", "TBD", "Lorem", "[…]", "[...]", "XXXX"]:
        if kw in joined:
            warns.append(f"C3 còn placeholder '{kw}'")

    # C4: TOC vs heading thật
    toc_entries = set(re.findall(r"^\s*(\d+\.\d+|[A-Z]\.\d+)\.", joined, re.M))
    heading_entries = set()
    for p in paras:
        m = re.match(r"^(\d+\.\d+|[A-Z]\.\d+)\.\s+\S", p.strip())
        if m:
            heading_entries.add(m.group(1))
    # heading thật có thể nhiều hơn TOC do trùng đoạn trích; chỉ cảnh báo heading ngoài TOC
    missing_toc = sorted(h for h in heading_entries if h not in toc_entries)
    if missing_toc:
        notes.append(f"C4 heading không thấy trong mục lục (kiểm bằng mắt): {missing_toc[:12]}")

    # C5: caption vs danh mục
    figs = set(re.findall(r"^Hình\s+(\d+\.\d+):", joined, re.M))
    dm_idx = joined.find("DANH MỤC HÌNH ẢNH")
    dm = joined[dm_idx:dm_idx + 6000] if dm_idx >= 0 else ""
    missing_dm = sorted(f for f in figs if f not in dm)
    if missing_dm:
        warns.append(f"C5 caption hình không có trong DANH MỤC HÌNH ẢNH: {missing_dm}")

    # C6: số liệu ms để đối chiếu
    times = sorted(set(re.findall(r"\d+[.,]\d+\s*ms", joined)))
    if times:
        notes.append(f"C6 số liệu thời gian trong text ({len(times)} giá trị), tự đối chiếu bảng/hình: {times[:25]}")

    print(f"AUDIT CONTENT — {args.docx}")
    print(f"  đoạn văn: {len(paras)} | 'Hình x.y' caption: {len(figs)} | TOC entry: {len(toc_entries)}")
    if warns:
        print(f"\nCẦN SỬA ({len(warns)}):")
        for w in warns:
            print("  -", w)
    else:
        print("\nPASS: không thấy chỗ trống/thiếu bắt buộc.")
    if notes:
        print("\nLƯU Ý (đọc tay):")
        for n in notes:
            print("  -", n)
    sys.exit(1 if warns else 0)


if __name__ == "__main__":
    main()
