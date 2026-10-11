#!/usr/bin/env python3
"""Render .pptx -> PDF -> PNG (mỗi slide 1 ảnh) để kiểm tra trực quan.

Cách dùng:
    python render_pptx.py deck.pptx --output_dir render
    python render_pptx.py deck.pptx --dpi 150
    python render_pptx.py deck.pptx --pdf-only

Hỗ trợ tự động:
  - Windows: Microsoft PowerPoint qua COM (ưu tiên, xuất siêu nét và giữ nguyên 100% layout)
  - Linux/macOS/Windows fallback: LibreOffice (soffice)
  - PDF -> PNG: PyMuPDF (fitz), pdftoppm, hoặc native PowerPoint export trên Windows.
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


def pptx_to_pdf_powerpoint_com(pptx_path, out_pdf_path):
    """Chuyển đổi PPTX sang PDF bằng Microsoft PowerPoint COM trên Windows."""
    try:
        import win32com.client  # type: ignore
        ppt = win32com.client.DispatchEx("PowerPoint.Application")
    except Exception:
        # Fallback dùng PowerShell nếu không có pywin32
        cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            f"""
            $ppt = New-Object -ComObject PowerPoint.Application;
            try {{
                $pres = $ppt.Presentations.Open('{Path(pptx_path).resolve()}', [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse);
                $pres.SaveAs('{Path(out_pdf_path).resolve()}', 32);
                $pres.Close();
            }} finally {{
                $ppt.Quit();
                [System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null;
            }}
            """
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0 or not Path(out_pdf_path).exists():
            raise RuntimeError(f"PowerPoint PowerShell export thất bại: {res.stderr}")
        return Path(out_pdf_path)

    try:
        pres = ppt.Presentations.Open(str(Path(pptx_path).resolve()), True, False, False)
        # 32 = ppSaveAsPDF
        pres.SaveAs(str(Path(out_pdf_path).resolve()), 32)
        pres.Close()
        return Path(out_pdf_path)
    finally:
        try:
            ppt.Quit()
        except Exception:
            pass


def pptx_to_pdf_soffice(pptx_path, out_dir):
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
        str(pptx_path),
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    pdf_path = Path(out_dir) / (Path(pptx_path).stem + ".pdf")
    if pdf_path.exists():
        return pdf_path
    return None


def pptx_to_pdf(pptx_path, out_dir):
    out_pdf_path = Path(out_dir) / (Path(pptx_path).stem + ".pdf")
    
    # 1. Thử PowerPoint COM nếu trên Windows
    if is_windows():
        try:
            return pptx_to_pdf_powerpoint_com(pptx_path, out_pdf_path)
        except Exception as e:
            print(f"[Cảnh báo] PowerPoint COM lỗi ({e}), chuyển sang soffice fallback...", file=sys.stderr)

    # 2. Thử LibreOffice soffice
    pdf_path = pptx_to_pdf_soffice(pptx_path, out_dir)
    if pdf_path and pdf_path.exists():
        return pdf_path

    sys.exit(
        "Lỗi: Không tìm thấy Microsoft PowerPoint (COM) hoặc LibreOffice (soffice) để render PDF.\n"
        "Vui lòng cài đặt Microsoft Office hoặc LibreOffice (winget install TheDocumentFoundation.LibreOffice)."
    )


def export_slides_com(pptx_path, out_dir, width=1920, height=1080):
    """Xuất trực tiếp slide sang PNG bằng PowerPoint COM trên Windows."""
    cmd = [
        "powershell",
        "-NoProfile",
        "-Command",
        f"""
        $ppt = New-Object -ComObject PowerPoint.Application;
        try {{
            $pres = $ppt.Presentations.Open('{Path(pptx_path).resolve()}', [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse);
            for ($i = 1; $i -le $pres.Slides.Count; $i++) {{
                $imgPath = Join-Path '{Path(out_dir).resolve()}' ('slide-{{0:D2}}.png' -f $i);
                $pres.Slides.Item($i).Export($imgPath, 'PNG', {width}, {height});
            }}
            $pres.Close();
        }} finally {{
            $ppt.Quit();
            [System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null;
        }}
        """
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        pngs = sorted(Path(out_dir).glob("slide-*.png"))
        if pngs:
            return pngs
    return None


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
        out = Path(out_dir) / f"slide-{i:02d}.png"
        pix.save(str(out))
        pages.append(out)
    doc.close()
    return pages


def pdf_to_png_poppler(pdf_path, out_dir, dpi):
    pdftoppm = shutil.which("pdftoppm")
    if not pdftoppm:
        return None
    prefix = Path(out_dir) / "slide"
    subprocess.run([pdftoppm, "-png", "-r", str(dpi), str(pdf_path), str(prefix)], check=True)
    return sorted(Path(out_dir).glob("slide-*.png"))


def main():
    ap = argparse.ArgumentParser(description="Render .pptx sang PDF và ảnh PNG từng slide.")
    ap.add_argument("pptx", help="Đường dẫn file .pptx")
    ap.add_argument("--output_dir", default="render", help="Thư mục xuất kết quả (mặc định: render)")
    ap.add_argument("--dpi", type=int, default=150, help="Độ phân giải DPI khi xuất ảnh (mặc định: 150)")
    ap.add_argument("--pdf-only", action="store_true", help="Chỉ xuất PDF, không render ra PNG")
    args = ap.parse_args()

    pptx_path = Path(args.pptx)
    if not pptx_path.exists():
        sys.exit(f"Không tìm thấy file: {pptx_path}")

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f">> Đang chuyển đổi: {pptx_path} -> PDF...")
    pdf_path = pptx_to_pdf(pptx_path, out_dir)
    print(f"   Đã tạo PDF: {pdf_path}")

    if args.pdf_only:
        print(">> Hoàn thành (chế độ --pdf-only).")
        return

    print(">> Đang render ảnh PNG từng slide...")
    pages = None

    # Thử PyMuPDF trước nếu có
    pages = pdf_to_png_pymupdf(pdf_path, out_dir, args.dpi)
    if pages:
        print(f"   Render thành công {len(pages)} slide bằng PyMuPDF.")
    else:
        # Thử native PowerPoint export nếu trên Windows
        if is_windows():
            pages = export_slides_com(pptx_path, out_dir)
            if pages:
                print(f"   Render thành công {len(pages)} slide bằng PowerPoint COM.")
        
        # Thử poppler
        if not pages:
            pages = pdf_to_png_poppler(pdf_path, out_dir, args.dpi)
            if pages:
                print(f"   Render thành công {len(pages)} slide bằng pdftoppm.")

    if not pages:
        print("   [Lưu ý] Không có PyMuPDF / pdftoppm. File PDF đã sẵn sàng tại:", pdf_path)
    else:
        print(f">> Thành công! Toàn bộ slide đã được lưu tại: {out_dir}")


if __name__ == "__main__":
    main()
