#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_docx_monochrome.py — soi DOCX xem co CHU MAU / TO NEN khong (luat den-trang).

LUAT (xem `docx-report/reference/rules.md`):
    * Chu trong than bai: DEN (auto / 000000). Khong mau xanh theme, khong mau nhan manh.
    * Bang: nen 100% TRANG TINH. Khong to nen xam/xanh o hang tieu de.
    * Nhan manh: chi bang DAM / NGHIENG (va highlight neu nguoi dung cho phep).

Vi sao can script nay thay vi mo mat do:
    1. **Bay `Hyperlink`**: Word dinh nghia san char style `Hyperlink` mau `0000FF`. MUC LUC /
       DANH MUC BANG la cac truong TOC co hyperlink -> tu dong mang style nay -> **in ra mau xanh**
       du than bai khong he dat mau. Mo Word nhin qua se khong thay.
    2. **Rac mau trong styles.xml**: Word nhet san hang chuc style dung-mau (Heading 2 = #4F81BD,
       Title, Quote, Intense Quote, cac "Grid"/"List"...) - phan lon KHONG duoc dung. Script tach
       rieng "mau dang dung" (nguy hiem) voi "style thua" (chi de biet).

CACH DUNG:
    python check_docx_monochrome.py <file.docx> [more.docx] [--allow-shading] [--quiet]

    --allow-shading  bo qua canh bao TO NEN bang (khi nguoi dung cho phep highlight)
    --quiet          chi in ket luan

EXIT: 0 = sach · 1 = co vi pham · 2 = loi doc file.
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from collections import Counter

OK_COLORS = {"auto", "000000", "000", "ffffff", "fff"}   # den / auto / trang
OK_FILLS = {"auto", "ffffff", "fff"}

PART_RE = re.compile(r"^word/(document|styles|numbering|header\d*|footer\d*|footnotes|endnotes)\.xml$")
COLOR_RE = re.compile(r'<w:color\s+w:val="([^"]+)"')
SHD_RE = re.compile(r'<w:shd\b[^>]*w:fill="([^"]+)"')
PSTYLE_RE = re.compile(r'<w:pStyle\s+w:val="([^"]+)"')
RSTYLE_RE = re.compile(r'<w:rStyle\s+w:val="([^"]+)"')
STYLE_RE = re.compile(r'<w:style\b(?P<attr>[^>]*)>(?P<body>.*?)</w:style>', re.S)
ID_RE = re.compile(r'w:styleId="([^"]+)"')
NAME_RE = re.compile(r'<w:name\s+w:val="([^"]+)"')

BODY_PARTS = ("word/document.xml",)


def xml_of(z, name):
    try:
        return z.read(name).decode("utf-8", "ignore")
    except KeyError:
        return ""


def used_style_ids(z, names):
    used = set()
    for n in names:
        if n.startswith("word/") and n.endswith(".xml") and (
                "document" in n or "header" in n or "footer" in n):
            x = xml_of(z, n)
            used |= set(PSTYLE_RE.findall(x))
            used |= set(RSTYLE_RE.findall(x))
    return used


def check(path, allow_shading, quiet):
    name = path.replace("/", "\\").split("\\")[-1]
    try:
        with zipfile.ZipFile(path) as z:
            names = z.namelist()
            styles_xml = xml_of(z, "word/styles.xml")
            doc_xml = xml_of(z, "word/document.xml")
            used = used_style_ids(z, names)

            # --- 1) mau chu dat TRUC TIEP trong than bai ---
            direct = Counter()
            for val in COLOR_RE.findall(doc_xml):
                if val.lower() not in OK_COLORS:
                    direct[val.lower()] += 1

            # --- 2) mau chu trong STYLE, tach "dang dung" vs "thua" ---
            style_colors = {}      # styleId -> (color, name)
            for m in STYLE_RE.finditer(styles_xml):
                sid = ID_RE.search(m.group("attr"))
                if not sid:
                    continue
                sid = sid.group(1)
                body = m.group("body")
                cols = [v.lower() for v in COLOR_RE.findall(body) if v.lower() not in OK_COLORS]
                if not cols:
                    continue
                nm = NAME_RE.search(body)
                style_colors[sid] = (cols[0], nm.group(1) if nm else sid)

            used_bad = {s: v for s, v in style_colors.items() if s in used}
            unused_bad = {s: v for s, v in style_colors.items() if s not in used}

            # --- 3) to nen (shading) ---
            shading = Counter()
            for val in SHD_RE.findall(doc_xml):
                if val.lower() not in OK_FILLS:
                    shading[val.lower()] += 1
    except Exception as e:  # noqa: BLE001
        print(f"[check] Khong doc duoc '{path}': {e}", file=sys.stderr)
        return 2

    problems = []
    if direct:
        problems.append(("CHU MAU dat truc tiep trong than bai",
                         ", ".join(f"#{c.upper()} x{n}" for c, n in direct.most_common())))
    if used_bad:
        problems.append(("CHU MAU trong STYLE DANG DUOC DUNG",
                         "; ".join(f"{s} (#{v[0].upper()})" for s, v in sorted(used_bad.items()))))
    if shading and not allow_shading:
        problems.append(("TO NEN (bang/o) — luat: nen 100% trang tinh",
                         ", ".join(f"#{c.upper()} x{n}" for c, n in shading.most_common())))

    # Canh bao rieng cho bay Hyperlink (hay gap nhat)
    hyperlink_warn = ""
    if "Hyperlink" in style_colors and "0" + "000ff" in style_colors["Hyperlink"][0]:
        hyperlink_warn = ("Style 'Hyperlink' con mau #0000FF. MUC LUC / DANH MUC BANG la cac truong TOC "
                          "(hyperlink) nen se IN RA MAU XANH du than bai khong dat mau. "
                          "Sua: doi <w:color> cua style Hyperlink thanh 000000 (giu <w:u>).")

    if not problems and not hyperlink_warn:
        print(f"[check] {name}: SACH — khong chu mau, khong to nen. ({len(used)} style dang dung da kiem.)")
        return 0

    print(f"[check] {name}: CO VI PHAM")
    for title, detail in problems:
        print(f"        - {title}: {detail}")
    if hyperlink_warn and "Hyperlink" not in {s for s, _ in
                                              [(s, v) for s, v in used_bad.items()]}:
        print(f"        ! BAY HYPERLINK: {hyperlink_warn}")
    if not quiet and unused_bad:
        shown = ", ".join(f"{s} (#{v[0].upper()})" for s, v in sorted(unused_bad.items())[:12])
        print(f"        (thong tin) {len(unused_bad)} style THUA cua Word con dinh mau, KHONG anh huong ban in:")
        print(f"          {shown}{' ...' if len(unused_bad) > 12 else ''}")
    print("        => Sua roi xuat lai PDF, va kiem lai PDF bang check_pdf_monochrome.py.")
    return 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="Soi DOCX xem co chu mau / to nen khong.")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--allow-shading", action="store_true", help="bo qua canh bao to nen")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    worst = 0
    for f in a.files:
        worst = max(worst, check(f, a.allow_shading, a.quiet))
    return worst


if __name__ == "__main__":
    sys.exit(main())
