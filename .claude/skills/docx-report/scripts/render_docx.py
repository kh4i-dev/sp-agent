#!/usr/bin/env python3
"""Render .docx -> PDF -> PNG để kiểm tra trực quan (visual QA).

Cách dùng:
    python render_docx.py report.docx --output_dir render --emit_pdf
    python render_docx.py report.docx --dpi 150

Hỗ trợ tự động:
  - Windows: Microsoft Word qua COM (ưu tiên, giữ nguyên 100% định dạng, TOC, mục lục, bảng biểu)
  - Linux/macOS/Windows fallback: LibreOffice (soffice)
  - PDF -> PNG: PyMuPDF (fitz) hoặc pdftoppm (Poppler).
"""
import argparse
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def is_windows():
    return platform.system() == "Windows"


def find_soffice():
    candidates = [
        os.environ.get("SOFFICE_PATH"),
        shutil.which("soffice"),
        shutil.which("libreoffice"),
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        "/usr/bin/soffice",
        "/usr/bin/libreoffice",
    ]
    for c in candidates:
        if c and Path(c).exists():
            return c
    return None


def docx_to_pdf_word_com(docx_path, out_pdf_path):
    """Chuyển đổi DOCX sang PDF bằng Microsoft Word COM trên Windows."""
    try:
        import win32com.client  # type: ignore
        word = win32com.client.DispatchEx("Word.Application")
    except Exception:
        # Fallback PowerShell nếu chưa cài pywin32
        cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            f"""
            $word = New-Object -ComObject Word.Application;
            try {{
                $doc = $word.Documents.Open('{Path(docx_path).resolve()}', $false, $true);
                $doc.SaveAs([ref]'{Path(out_pdf_path).resolve()}', [ref]17);
                $doc.Close();
            }} finally {{
                $word.Quit();
                [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null;
            }}
            """
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0 or not Path(out_pdf_path).exists():
            raise RuntimeError(f"Word PowerShell export thất bại: {res.stderr}")
        return Path(out_pdf_path)

    try:
        doc = word.Documents.Open(str(Path(docx_path).resolve()), False, True)
        # 17 = wdFormatPDF
        doc.SaveAs(str(Path(out_pdf_path).resolve()), FileFormat=17)
        doc.Close()
        return Path(out_pdf_path)
    finally:
        try:
            word.Quit()
        except Exception:
            pass


def docx_to_pdf_soffice(docx_path, out_dir):
    soffice = find_soffice()
    if not soffice:
        return None
    profile = tempfile.mkdtemp(prefix="soffice_profile_")
    cmd = [
        soffice,
        "--headless",
        "--norestore",
        f"-env:UserInstallation=file:///{profile}",
        "--convert-to",
        "pdf",
        "--outdir",
        str(out_dir),
        str(docx_path),
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    pdf_path = Path(out_dir) / (Path(docx_path).stem + ".pdf")
    if pdf_path.exists():
        return pdf_path
    return None


def docx_to_pdf(docx_path, out_dir):
    out_pdf_path = Path(out_dir) / (Path(docx_path).stem + ".pdf")
    
    # 1. Thử Microsoft Word COM nếu trên Windows
    if is_windows():
        try:
            return docx_to_pdf_word_com(docx_path, out_pdf_path)
        except Exception as e:
            print(f"[Cảnh báo] Word COM lỗi ({e}), chuyển sang soffice fallback...", file=sys.stderr)

    # 2. Thử LibreOffice soffice
    pdf_path = docx_to_pdf_soffice(docx_path, out_dir)
    if pdf_path and pdf_path.exists():
        return pdf_path

    sys.exit(
        "Lỗi: Không tìm thấy Microsoft Word hoặc LibreOffice (soffice) để xuất PDF.\n"
        "Vui lòng cài đặt Microsoft Office hoặc LibreOffice."
    )


def pdf_to_png_pymupdf(pdf_path, out_dir, dpi):
    try:
        import fitz  # type: ignore
    except ImportError:
        return None
    doc = fitz.open(str(pdf_path))
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)
    pages = []
    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=matrix)
        out = Path(out_dir) / f"page-{i:02d}.png"
        pix.save(str(out))
        pages.append(out)
    doc.close()
    return pages


def pdf_to_png_poppler(pdf_path, out_dir, dpi):
    pdftoppm = shutil.which("pdftoppm")
    if not pdftoppm:
        return None
    prefix = Path(out_dir) / "page"
    subprocess.run([pdftoppm, "-png", "-r", str(dpi), str(pdf_path), str(prefix)], check=True)
    return sorted(Path(out_dir).glob("page-*.png"))


def main():
    ap = argparse.ArgumentParser(description="Render DOCX sang PDF và ảnh PNG từng trang.")
    ap.add_argument("docx", help="Đường dẫn file .docx")
    ap.add_argument("--output_dir", default="render", help="Thư mục xuất ảnh (mặc định: render)")
    ap.add_argument("--dpi", type=int, default=150, help="DPI xuất ảnh (mặc định: 150)")
    ap.add_argument("--emit_pdf", action="store_true", help="Chỉ xuất file PDF")
    args = ap.parse_args()

    docx_path = Path(args.docx)
    if not docx_path.exists():
        sys.exit(f"Không tìm thấy file: {docx_path}")

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f">> Đang chuyển đổi: {docx_path.name} -> PDF...")
    pdf_path = docx_to_pdf(docx_path, out_dir)
    print(f"   Đã xuất PDF: {pdf_path}")

    if args.emit_pdf:
        print(">> Hoàn thành (chế độ --emit_pdf).")
        return

    print(">> Đang render từng trang ra PNG...")
    pages = pdf_to_png_pymupdf(pdf_path, out_dir, args.dpi)
    if not pages:
        pages = pdf_to_png_poppler(pdf_path, out_dir, args.dpi)

    if not pages:
        print("   [Lưu ý] Không có PyMuPDF / pdftoppm để trích ảnh. File PDF đã sẵn sàng tại:", pdf_path)
    else:
        print(f">> Thành công! Đã lưu {len(pages)} trang tại: {out_dir}")


if __name__ == "__main__":
    main()
