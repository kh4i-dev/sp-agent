#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_pdf_monochrome.py — soi PDF xem co CHU MAU khong.

LUAT CUA KHOI TAI LIEU (dong bo voi `docx-report`):
    * KHONG dung CHU MAU (mau xanh theme, mau nhan manh, v.v.).
    * Chi duoc dung HIGHLIGHT (nen sang) de nhan manh.
    => Van ban trong PDF phai la DEN / XAM (grayscale). Nen (highlight) thi duoc phep.

Script doc tung span chu trong PDF, tinh mau chu (fill color) va bao moi span KHONG
thuoc thang xam. Dung de CHAN truoc khi giao tai lieu.

CACH DUNG:
    python check_pdf_monochrome.py <file.pdf> [more.pdf] [--tol 8] [--max-print 20]

    --tol N        sai so cho phep giua 3 kenh R,G,B (mac dinh 8/255)
    --max-print N  in toi da N vi du (mac dinh 20)

EXIT: 0 = sach (khong chu mau) · 1 = CO chu mau · 2 = loi doc file.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter

try:
    import pymupdf
except ImportError:  # pragma: no cover
    try:
        import fitz as pymupdf  # type: ignore
    except ImportError:
        print("[check_pdf_monochrome] Thieu PyMuPDF. Cai: pip install pymupdf", file=sys.stderr)
        sys.exit(2)


def to_rgb(col):
    """Chuan hoa mau chu ve (R, G, B) 0-255.

    PyMuPDF tra `span['color']` theo NHIEU dang:
      - int DONG GOI 0xRRGGBB (dang gap nhat voi PDF cua Chrome)  -> phai tach kenh!
      - float 0..1 (xam) hoac (r,g,b) float 0..1
      - int 0..1
    Bay da tung mac: coi moi int la "xam 0..1" -> mau xanh 0x1F4E79 bi doc thanh TRANG
    => script bao SACH oan. Xem `_self_test()`.
    """
    if col is None:
        return (0, 0, 0)
    if isinstance(col, bool):
        return (0, 0, 0)
    if isinstance(col, int):
        if 0 <= col <= 1:
            v = int(round(col * 255))
            return (v, v, v)
        return ((col >> 16) & 0xFF, (col >> 8) & 0xFF, col & 0xFF)
    if isinstance(col, float):
        v = int(round(max(0.0, min(1.0, col)) * 255))
        return (v, v, v)
    if isinstance(col, (tuple, list)) and len(col) >= 3:
        out = []
        for c in col[:3]:
            c = float(c)
            out.append(int(round(c * 255)) if c <= 1.0 else int(round(c)))
        return tuple(out)  # type: ignore[return-value]
    return (0, 0, 0)


def hexs(rgb):
    return '#%02X%02X%02X' % rgb


def is_gray(rgb, tol):
    r, g, b = rgb
    return max(r, g, b) - min(r, g, b) <= tol


def check(path, tol, max_print):
    try:
        doc = pymupdf.open(path)
    except Exception as e:  # noqa: BLE001
        print(f"[check] Khong mo duoc '{path}': {e}", file=sys.stderr)
        return 2

    bad = []
    total = 0
    for pno in range(doc.page_count):
        for blk in doc[pno].get_text("dict")["blocks"]:
            if blk.get("type") != 0:
                continue
            for ln in blk.get("lines", []):
                for sp in ln.get("spans", []):
                    txt = (sp.get("text") or "").strip()
                    if not txt:
                        continue
                    total += 1
                    rgb = to_rgb(sp.get("color"))
                    if not is_gray(rgb, tol):
                        bad.append((pno + 1, hexs(rgb), txt[:70]))

    name = path.split('\\')[-1].split('/')[-1]
    if not bad:
        print(f"[check] {name}: SACH — {total} span chu, tat ca deu DEN/XAM (khong chu mau).")
        return 0

    cnt = Counter(c for _, c, _ in bad)
    print(f"[check] {name}: CO CHU MAU — {len(bad)}/{total} span khong phai xam.")
    print("        Bang mau vi pham (so span):")
    for c, n in cnt.most_common():
        print(f"          {c}   x{n}")
    print("        Vi du:")
    for pno, c, t in bad[:max_print]:
        print(f"          tr.{pno:<4} {c}   {t!r}")
    if len(bad) > max_print:
        print(f"          ... (+{len(bad) - max_print} nua)")
    print("        => Sua CSS/bo codehilite cho toi khi script nay bao SACH.")
    return 1


def _self_test():
    """Chot chan FALSE-NEGATIVE: neu khong tach duoc kenh mau thi script vo dung."""
    cases = [
        (0x1F4E79, (0x1F, 0x4E, 0x79)),   # xanh dam (accent cu) -> phai la MAU
        (0x22303F, (0x22, 0x30, 0x3F)),   # xanh xam (header bang cu) -> MAU
        (0x1A1A1A, (0x1A, 0x1A, 0x1A)),   # ink -> xam
        (0x000000, (0, 0, 0)),
        (0.0, (0, 0, 0)),
        (1.0, (255, 255, 255)),
        ((0.1, 0.1, 0.1), (26, 26, 26)),
    ]
    for raw, want in cases:
        got = to_rgb(raw)
        assert got == want, f"to_rgb({raw!r}) = {got}, mong doi {want}"
    assert not is_gray((0x1F, 0x4E, 0x79), 8), 'xanh dam bi coi la xam -> FALSE NEGATIVE!'
    assert is_gray((0x1A, 0x1A, 0x1A), 8)


def main(argv=None):
    _self_test()
    ap = argparse.ArgumentParser(description="Soi PDF xem co chu mau khong (luat: chi den/xam + highlight).")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--tol", type=int, default=8, help="sai so R/G/B cho phep (mac dinh 8)")
    ap.add_argument("--max-print", type=int, default=20)
    a = ap.parse_args(argv)
    worst = 0
    for f in a.files:
        worst = max(worst, check(f, a.tol, a.max_print))
    return worst


if __name__ == "__main__":
    sys.exit(main())
