#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit_tables_docx.py — GATE BẢNG trước khi in.

Rà mọi bảng trong .docx và báo cảnh báo cấu trúc/căn lề:
  - header không căn giữa (T1)
  - ô thiếu căn giữa dọc vAlign (T2)
  - cột số/ngắn đang căn trái (T3, cần --center-cols hoặc tự phát hiện cột số)
  - ô rỗng trong bảng nội dung (T4)
  - bảng thiếu caption dưới (T5)
  - header không lặp khi sang trang (thiếu w:tblHeader) (T6)

Dùng:
  python audit_tables_docx.py file.docx             # audit, exit 1 nếu có cảnh báo
  python audit_tables_docx.py file.docx --json out.json
"""
import argparse
import json
import re
import sys
import zipfile
from lxml import etree as ET

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def q(t):
    return f"{{{W}}}{t}"


def cell_text(tc):
    return " ".join("".join(x.text or "" for x in tc.findall(".//w:t", NS)).split())


def pjc(p):
    pPr = p.find("w:pPr", NS)
    if pPr is not None:
        j = pPr.find("w:jc", NS)
        if j is not None:
            return j.get(q("val"))
    return "left"


def is_numeric_cell(s):
    return bool(re.fullmatch(r"[0-9.,\s%×xN=()ms–\-]*", s or "")) and any(c.isdigit() for c in s or "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docx")
    ap.add_argument("--json")
    args = ap.parse_args()

    root = ET.fromstring(zipfile.ZipFile(args.docx).read("word/document.xml"))
    kids = list(root.find("w:body", NS))
    tbl_positions = [i for i, el in enumerate(kids) if el.tag == q("tbl")]

    warn = []
    tables = []
    layout_skipped = []
    for k, pos in enumerate(tbl_positions, 1):
        tbl = kids[pos]
        rows = tbl.findall("w:tr", NS)
        ncol = len(rows[0].findall("w:tc", NS)) if rows else 0
        cap = ""
        for j in range(pos, min(pos + 4, len(kids))):
            t = " ".join("".join(x.text or "" for x in kids[j].findall(".//w:t", NS)).split())
            if re.match(r"^(Bảng|Hình)\s", t):
                cap = t[:70]
                break
        info = {"#": k, "caption": cap, "rows": len(rows), "cols": ncol}

        # Bảng LAYOUT (bìa/nhiệm vụ/khối chữ ký): không caption, ít cột → bỏ qua luật nội dung
        if not cap and ncol <= 3 and len(rows) <= 4:
            layout_skipped.append(k)
            tables.append(info)
            continue

        # header jc
        if rows:
            hdr = [pjc(p) for tc in rows[0].findall("w:tc", NS) for p in tc.findall("w:p", NS)]
            bad_hdr = [j for j in hdr if j != "center"]
            if bad_hdr:
                warn.append(f"T1 bảng #{k} ({cap or 'không caption'}): header chưa căn giữa ({len(bad_hdr)} ô)")
            info["header_jc"] = sorted(set(hdr))

        # vAlign + ô rỗng
        no_valign = 0
        empty = 0
        for tr in rows:
            for tc in tr.findall("w:tc", NS):
                tcPr = tc.find("w:tcPr", NS)
                va = tcPr.find("w:vAlign", NS) if tcPr is not None else None
                if va is None or va.get(q("val")) not in ("center", "both"):
                    no_valign += 1
                if not cell_text(tc):
                    empty += 1
        if no_valign:
            warn.append(f"T2 bảng #{k} ({cap or 'không caption'}): {no_valign} ô thiếu vAlign=center")
        if empty and cap:
            warn.append(f"T4 bảng #{k} ({cap}): {empty} ô rỗng")

        # cột số đang căn trái
        if rows and ncol:
            for ci in range(ncol):
                vals = [cell_text(tr.findall("w:tc", NS)[ci]) for tr in rows[1:] if len(tr.findall("w:tc", NS)) > ci]
                if not vals:
                    continue
                if all(is_numeric_cell(v) for v in vals if v):
                    jcs = [pjc(p) for tr in rows[1:] if len(tr.findall("w:tc", NS)) > ci
                           for p in tr.findall("w:tc", NS)[ci].findall("w:p", NS)]
                    if any(j != "center" for j in jcs):
                        warn.append(f"T3 bảng #{k} ({cap or 'không caption'}): cột {ci} là cột số nhưng chưa căn giữa")

        # header lặp khi sang trang
        if len(rows) > 6 and rows:
            tcPr0 = rows[0].find("w:trPr", NS)
            if tcPr0 is None or tcPr0.find("w:tblHeader", NS) is None:
                warn.append(f"T6 bảng #{k} ({cap or 'không caption'}): nhiều dòng nhưng header chưa đặt tblHeader")

        tables.append(info)

    # bảng nội dung thiếu caption
    for info in tables:
        if info["#"] in layout_skipped:
            continue
        if info["rows"] > 3 and not info["caption"]:
            warn.append(f"T5 bảng #{info['#']} ({info['rows']} dòng) không thấy caption 'Bảng x.y'")

    print(f"AUDIT TABLES — {args.docx}")
    print(f"  số bảng: {len(tables)} (bỏ qua {len(layout_skipped)} bảng layout: {layout_skipped})")
    for info in tables:
        print(f"   #{info['#']:2d} rows={info['rows']:2d} cols={info['cols']} {info['caption'][:64]}")
    if warn:
        print(f"\nCẢNH BÁO ({len(warn)}):")
        for w in warn:
            print("  -", w)
    else:
        print("\nPASS: cấu trúc + căn lề bảng đạt.")

    if args.json:
        json.dump({"tables": tables, "warnings": warn}, open(args.json, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
    sys.exit(1 if warn else 0)


if __name__ == "__main__":
    main()
