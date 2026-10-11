#!/usr/bin/env python3
"""Recalculate formulas in an .xlsx via LibreOffice headless (OOXMLRecalcMode=0).

Cach dung:
    python recalc_xlsx.py report.xlsx
    python recalc_xlsx.py report.xlsx --output report_recalc.xlsx

Yeu cau: LibreOffice (soffice).
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xlsx")
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    src = Path(args.xlsx)
    if not src.exists():
        sys.exit(f"Khong thay file: {src}")

    soffice = find_soffice()
    if not soffice:
        sys.exit(
            "Khong tim thay LibreOffice (soffice).\n"
            "Windows: winget install TheDocumentFoundation.LibreOffice"
        )

    out_dir = tempfile.mkdtemp(prefix="recalc_out_")
    profile = tempfile.mkdtemp(prefix="soffice_profile_")

    filter_name = "xlsx:Calc MS Excel 2007 XML:OOXMLRecalcMode=0"
    cmd = [
        soffice,
        "--headless",
        "--norestore",
        f"-env:UserInstallation=file:///{profile}",
        "--convert-to",
        filter_name,
        "--outdir",
        out_dir,
        str(src),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    produced = Path(out_dir) / src.name
    if not produced.exists():
        sys.exit("Recalc that bai: khong thay file ket qua.")

    if args.output:
        dest = Path(args.output)
    else:
        dest = src
    shutil.copyfile(produced, dest)
    print(f"Recalculated: {dest}")


if __name__ == "__main__":
    main()
