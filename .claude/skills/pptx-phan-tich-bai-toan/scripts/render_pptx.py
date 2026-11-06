#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
render_pptx.py — render .pptx -> PDF (LibreOffice/PowerPoint) -> PNG tung slide.

    python render_pptx.py deck.pptx --outdir render --dpi 110

Dung cho CONG RENDER (bat buoc): phai soi tung anh slide truoc khi giao.
Yeu cau: LibreOffice (soffice) hoac PowerPoint (Windows), pymupdf (fitz).
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys

SOFFICE_CANDIDATES = [
    shutil.which("soffice"),
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    "/usr/bin/soffice",
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
]


def find_soffice():
    for c in SOFFICE_CANDIDATES:
        if c and os.path.exists(c):
            return c
    return None


def to_pdf(pptx, outdir):
    soffice = find_soffice()
    if not soffice:
        raise SystemExit("Khong tim thay LibreOffice (soffice). Cai: winget install "
                         "TheDocumentFoundation.LibreOffice")
    os.makedirs(outdir, exist_ok=True)
    subprocess.run([soffice, "--headless", "--norestore", "--convert-to", "pdf",
                    "--outdir", outdir, pptx], check=True,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    pdf = os.path.join(outdir, os.path.splitext(os.path.basename(pptx))[0] + ".pdf")
    if not os.path.exists(pdf):
        raise SystemExit("Render PDF that bai: " + pdf)
    return pdf


def pdf_to_png(pdf, outdir, dpi=110):
    try:
        import pymupdf as fitz  # type: ignore
    except Exception:
        try:
            import fitz  # type: ignore
        except Exception:
            raise SystemExit("Can pymupdf: pip install pymupdf")
    doc = fitz.open(pdf)
    out = []
    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(dpi=dpi)
        p = os.path.join(outdir, f"slide-{i:02d}.png")
        pix.save(p)
        out.append(p)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx")
    ap.add_argument("--outdir", default="render")
    ap.add_argument("--dpi", type=int, default=110)
    a = ap.parse_args()
    pdf = to_pdf(a.pptx, a.outdir)
    pngs = pdf_to_png(pdf, a.outdir, a.dpi)
    print(f"PDF : {pdf}")
    print(f"PNG : {len(pngs)} anh trong {a.outdir}")
    for p in pngs:
        print("  -", os.path.basename(p))


if __name__ == "__main__":
    main()
