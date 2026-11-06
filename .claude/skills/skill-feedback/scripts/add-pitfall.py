#!/usr/bin/env python3
"""add-pitfall.py — ghi nhanh một bài học/pitfall vào một skill của sp-agent.

Vòng lặp đầy đủ do skill `skill-feedback` định nghĩa; script này chỉ làm bước
"GHI" (tạo file chuẩn + append entry + chống trùng). Sau khi chạy, agent VẪN PHẢI:
  1. Thêm 1 dòng vào bảng docs/lessons-learned.md
  2. Chạy tools/verify-skills.ps1 và tools/sync-skills.ps1
  3. Nếu severity = iron: chuyển quy tắc lên SKILL.md của skill đó

Ví dụ:
  python .claude/skills/skill-feedback/scripts/add-pitfall.py \
    --skill docx-report --severity warn --title "COM render quên Fields.Update" \
    --symptom "TOC hien gia tri cu trong PDF" \
    --cause "COM khong tu update field khi SaveAs" \
    --fix "Goi Fields.Update() truoc SaveAs" \
    --evidence "python render_docx.py a.docx -> PDF dung"
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
import unicodedata
from pathlib import Path

HEADER = """# Pitfalls — {skill}

> Bài học do agent đóng góp khi gặp lỗi/biến chứng mà SKILL.md chưa nói đến.
> Quy trình đóng góp: skill `skill-feedback` (xác minh → chống trùng → ghi → cập nhật
> bản đồ lessons-learned → verify + sync). Bài học mức IRON phải được chuyển lên SKILL.md.

## Bẫy đã đóng góp

| Ngày | Mức | Bẫy |
|---|---|---|
"""


def die(msg: str, code: int = 1) -> None:
    print(f"FAIL  {msg}", file=sys.stderr)
    raise SystemExit(code)


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", text.lower()).strip()


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / ".claude" / "skills").is_dir():
            return parent
    die("không tìm thấy repo root (thư mục chứa .claude/skills)")


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass

    ap = argparse.ArgumentParser(description="Ghi pitfall vào một skill (vòng lặp skill-feedback).")
    ap.add_argument("--skill", required=True, help="tên thư mục skill, VD: docx-report")
    ap.add_argument("--severity", default="warn", choices=["iron", "warn", "info"], help="mức độ bài học")
    ap.add_argument("--title", required=True, help="tên ngắn của bẫy")
    ap.add_argument("--symptom", default="—", help="triệu chứng")
    ap.add_argument("--cause", default="—", help="nguyên nhân")
    ap.add_argument("--fix", required=True, help="cách sửa/phòng")
    ap.add_argument("--evidence", default="—", help="lệnh + output chứng minh")
    ap.add_argument("--repro", default="—", help="điều kiện tái lập")
    ap.add_argument("--file", default="reference/pitfalls.md",
                    help="đường dẫn file đích, tính từ thư mục skill (mặc định: reference/pitfalls.md)")
    ap.add_argument("--unverified", action="store_true",
                    help="chưa xác minh — gắn nhãn [UNVERIFIED] (cấm bỏ nhãn khi chưa chạy thật)")
    ap.add_argument("--force", action="store_true", help="ghi dù tiêu đề có vẻ trùng")
    args = ap.parse_args()

    root = find_repo_root()
    skill_dir = root / ".claude" / "skills" / args.skill
    if not (skill_dir / "SKILL.md").is_file():
        die(f"skill '{args.skill}' không tồn tại trong .claude/skills")

    target = skill_dir / args.file
    if not str(target.resolve()).startswith(str(skill_dir.resolve())):
        die("--file phải nằm trong thư mục skill")

    # --- Chống trùng: tìm tiêu đề đã có trong skill + bản đồ lessons-learned ---
    needle = norm(args.title)
    hay_files = [skill_dir / "SKILL.md", *sorted((skill_dir / "reference").glob("*.md"))] \
        if (skill_dir / "reference").is_dir() else [skill_dir / "SKILL.md"]
    lessons_map = root / "docs" / "lessons-learned.md"
    if lessons_map.is_file():
        hay_files.append(lessons_map)

    hits: list[str] = []
    for f in [h for h in hay_files if h.is_file()]:
        text = f.read_text(encoding="utf-8", errors="replace")
        if needle in norm(text):
            hits.append(str(f.relative_to(root)))
    if hits and not args.force:
        print("CHẶN  tiêu đề trông đã có ở:")
        for h in hits:
            print(f"      - {h}")
        print("      → Đọc lại: đã có thì CẬP NHẬT bản cũ (không thêm bản sao);")
        print("        thật sự khác thì đổi tiêu đề hoặc dùng --force.")
        raise SystemExit(2)

    # --- Ghi entry (giữ nguyên kiểu xuống dòng của file nếu đã tồn tại) ---
    if target.exists():
        raw = target.read_bytes()
        eol = "\r\n" if b"\r\n" in raw else "\n"
        text = raw.decode("utf-8", errors="replace")
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        eol = "\n"
        text = HEADER.format(skill=args.skill)

    today = _dt.date.today().isoformat()
    sev = args.severity.upper()
    head = f"### [{sev}] {args.title}" + (" [UNVERIFIED]" if args.unverified else "") + f" ({today})"
    entry = eol.join([
        head,
        f"- **Triệu chứng:** {args.symptom}",
        f"- **Nguyên nhân:** {args.cause}",
        f"- **Sửa/phòng:** {args.fix} (bằng chứng: `{args.evidence}`)",
        f"- **Điều kiện tái lập:** {args.repro}",
    ])
    if args.unverified:
        entry += eol + "- **Cần kiểm:** [UNVERIFIED] — chưa tái lập/fix PASS; xác minh rồi bỏ nhãn này."
    if not text.endswith(eol):
        text += eol
    text += entry + eol
    target.write_text(text, encoding="utf-8", newline="")

    print(f"OK    đã ghi entry vào {target.relative_to(root)}")
    print("      Việc còn lại (bắt buộc, script KHÔNG làm thay):")
    print("      1. Thêm 1 dòng vào bảng docs/lessons-learned.md")
    print("      2. Chạy tools/verify-skills.ps1 rồi tools/sync-skills.ps1")
    if args.severity == "iron":
        print("      3. Mức IRON → chuyển quy tắc lên SKILL.md của skill này")


if __name__ == "__main__":
    main()
