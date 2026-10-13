#!/usr/bin/env python3
"""Liệt kê / chấp nhận / từ chối tracked changes (revisions) một cách AN TOÀN.

- `--list`   : chỉ ĐỌC XML, KHÔNG sửa file (an toàn tuyệt đối với python-docx).
- `--accept` / `--reject` : thao tác bằng Microsoft Word (COM) trên BẢN SAO, KHÔNG đụng file gốc
  (python-docx nuốt/ hỏng `w:ins`/`w:del` khi lưu — xem reference/rules.md §12, nên không dùng nó).

Cách dùng:
    python revisions.py report.docx --list
    python revisions.py report.docx --accept -o clean.docx
    python revisions.py report.docx --reject -o clean.docx
"""
import argparse
import re
import shutil
import sys
import zipfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

TAGS = {
    "w:ins": "chèn (insert)",
    "w:del": "xóa (delete)",
    "w:rPrChange": "đổi định dạng run",
    "w:pPrChange": "đổi định dạng đoạn",
    "w:moveFrom": "di chuyển đi (moveFrom)",
    "w:moveTo": "di chuyển đến (moveTo)",
}


def list_revisions(path):
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if re.match(r"word/(document|header\d*|footer\d*)\.xml$", n)]
        xml = "".join(z.read(n).decode("utf-8", "ignore") for n in names)
    counts = {}
    for tag, label in TAGS.items():
        counts[label] = len(re.findall(rf"<{tag}[ >/]", xml))
    comments = len(re.findall(r"<w:commentReference[ >/]", xml))
    return counts, comments


def word_com_action(path, out, action):
    """action = 'accept' | 'reject' — Word COM, lưu sang `out` (bản sao)."""
    method = "AcceptAll" if action == "accept" else "RejectAll"
    cmd = [
        "powershell", "-NoProfile", "-Command",
        f"""
        $word = New-Object -ComObject Word.Application;
        try {{
            $doc = $word.Documents.Open('{Path(path).resolve()}', $false, $false);
            $doc.Revisions.{method}();
            $doc.SaveAs2([ref]'{Path(out).resolve()}', [ref]16);
            $doc.Close($false);
        }} finally {{
            $word.Quit();
            [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null;
        }}
        """,
    ]
    import subprocess
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0 or not Path(out).exists():
        raise RuntimeError(f"Word COM thất bại: {res.stderr}")
    return Path(out)


def main():
    ap = argparse.ArgumentParser(description="Quản lý tracked changes (.docx): list / accept / reject (an toàn).")
    ap.add_argument("docx", help="Đường dẫn file .docx")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--list", action="store_true", help="Chỉ liệt kê (read-only, không sửa file)")
    g.add_argument("--accept", action="store_true", help="Chấp nhận mọi thay đổi (lưu bản sao)")
    g.add_argument("--reject", action="store_true", help="Từ chối mọi thay đổi (lưu bản sao)")
    ap.add_argument("-o", "--output", help="File xuất ra cho --accept/--reject (mặc định: <tên>_clean.docx)")
    args = ap.parse_args()

    path = Path(args.docx)
    if not path.exists():
        sys.exit(f"Không tìm thấy file: {path}")

    if args.list:
        counts, comments = list_revisions(path)
        total = sum(counts.values())
        print(f"=== TRACKED CHANGES: {path.name} ===")
        for label, n in counts.items():
            if n:
                print(f"  - {label}: {n}")
        print(f"  - bình luận (comment): {comments}")
        print(f"  TỔNG revision: {total}")
        if total == 0:
            print("  (Không có tracked change.)")
        else:
            print("  → Để chốt bản sạch: chạy --accept hoặc --reject (thao tác trên bản sao).")
        return

    action = "accept" if args.accept else "reject"
    out = args.output or str(Path(path).stem + "_clean.docx")
    word_com_action(path, out, action)
    verb = "chấp nhận" if action == "accept" else "từ chối"
    print(f">> Đã {verb} mọi tracked change. File sạch: {out}")
    print("   (File gốc KHÔNG bị thay đổi.)")


if __name__ == "__main__":
    main()
