#!/usr/bin/env python3
"""Render moi trang PDF -> PNG de kiem tra truc quan.

Cach dung:
    python pdf_to_images.py input.pdf --output_dir render --dpi 150

Uu tien PyMuPDF (fitz); neu khong co thi fallback pdftoppm (Poppler).
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def render_pymupdf(pdf_path, out_dir, dpi):
    import fitz
    doc = fitz.open(str(pdf_path))
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)
    pages = []
    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=matrix)
        out = Path(out_dir) / f"page-{i}.png"
        pix.save(str(out))
        pages.append(out)
    doc.close()
    return pages


def render_poppler(pdf_path, out_dir, dpi):
    pdftoppm = shutil.which("pdftoppm")
    if not pdftoppm:
        return None
    prefix = Path(out_dir) / "page"
    subprocess.run([pdftoppm, "-png", "-r", str(dpi), str(pdf_path), str(prefix)], check=True)
    return sorted(Path(out_dir).glob("page-*.png"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--output_dir", default="render")
    ap.add_argument("--dpi", type=int, default=150)
    args = ap.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        sys.exit(f"Khong thay file: {pdf_path}")

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        pages = render_pymupdf(pdf_path, out_dir, args.dpi)
        backend = "PyMuPDF"
    except Exception:
        pages = render_poppler(pdf_path, out_dir, args.dpi)
        backend = "pdftoppm"

    if not pages:
        sys.exit("Khong render duoc. Cai PyMuPDF (pip install pymupdf) hoac Poppler.")

    print(f"Backend: {backend}")
    print(f"Pages: {len(pages)}")
    for p in pages:
        print(f"  {p}")


if __name__ == "__main__":
    main()
