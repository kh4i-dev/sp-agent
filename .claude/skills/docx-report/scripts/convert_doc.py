#!/usr/bin/env python3
"""Chuyển file Word cũ (.doc, Word 97-2003) sang .docx để xử lý bằng python-docx.

python-docx KHÔNG đọc được .doc — phải convert trước. Script ưu tiên Microsoft Word
(COM, Windows), fallback LibreOffice (soffice).

Cách dùng:
    python convert_doc.py old.doc                 # -> old.docx (cùng thư mục)
    python convert_doc.py old.doc -o out.docx
    python convert_doc.py "C:\\path\\folder"         # chuyển mọi .doc trong thư mục
"""
import argparse
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def _find_soffice():
    for c in (shutil.which("soffice"), shutil.which("libreoffice"),
              r"C:\Program Files\LibreOffice\program\soffice.exe",
              r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
              "/Applications/LibreOffice.app/Contents/MacOS/soffice",
              "/usr/bin/soffice"):
        if c and Path(c).exists():
            return c
    return None


def _convert_word_com(src, dst):
    """Convert 1 file bằng Microsoft Word COM (PowerShell). 16 = wdFormatDocumentDefault (.docx)."""
    cmd = [
        "powershell", "-NoProfile", "-Command",
        f"""
        $word = New-Object -ComObject Word.Application;
        try {{
            $doc = $word.Documents.Open('{Path(src).resolve()}', $false, $true);
            $doc.SaveAs2([ref]'{Path(dst).resolve()}', [ref]16);
            $doc.Close($false);
        }} finally {{
            $word.Quit();
            [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null;
        }}
        """,
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0 or not Path(dst).exists():
        raise RuntimeError(f"Word COM thất bại: {res.stderr}")
    return Path(dst)


def _convert_soffice(src, dst):
    soffice = _find_soffice()
    if not soffice:
        return None
    out_dir = Path(dst).parent
    profile = tempfile.mkdtemp(prefix="soffice_profile_")
    subprocess.run(
        [soffice, "--headless", "--norestore",
         f"-env:UserInstallation=file:///{profile}",
         "--convert-to", "docx", "--outdir", str(out_dir), str(src)],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    produced = Path(out_dir) / (Path(src).stem + ".docx")
    if produced.exists():
        if produced != Path(dst):
            shutil.move(str(produced), str(dst))
        return Path(dst)
    return None


def convert_one(src, dst=None):
    src = Path(src)
    dst = Path(dst) if dst else src.with_suffix(".docx")
    if src.suffix.lower() == ".docx":
        print(f">> Đã là .docx, bỏ qua: {src}")
        return src
    if platform.system() == "Windows":
        try:
            return _convert_word_com(src, dst)
        except Exception as e:
            print(f"[Cảnh báo] Word COM lỗi ({e}), thử LibreOffice...", file=sys.stderr)
    if _convert_soffice(src, dst):
        return dst
    sys.exit("Lỗi: Không có Microsoft Word hoặc LibreOffice (soffice) để chuyển đổi.")


def main():
    ap = argparse.ArgumentParser(description="Chuyển .doc -> .docx (Word COM / LibreOffice).")
    ap.add_argument("src", help="File .doc hoặc thư mục chứa .doc")
    ap.add_argument("-o", "--output", help="File .docx xuất ra (chỉ khi src là 1 file)")
    args = ap.parse_args()

    src = Path(args.src)
    if src.is_dir():
        docs = sorted(src.glob("*.doc"))
        if not docs:
            sys.exit(f"Không tìm thấy .doc trong {src}")
        for d in docs:
            out = convert_one(d)
            print(f">> {d.name} -> {out.name}")
        return
    if not src.exists():
        sys.exit(f"Không tìm thấy file: {src}")
    out = convert_one(src, args.output)
    print(f">> Đã chuyển: {out}")


if __name__ == "__main__":
    main()
