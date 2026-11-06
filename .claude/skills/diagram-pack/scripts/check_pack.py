#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_pack.py — Kiểm tra hợp đồng thư mục của một diagram pack.

Dùng:
    py -3 check_pack.py <TARGET>          # vd: E:\\HOC TAP\\my-project\\btl-cnpm\\private-docs
    py -3 check_pack.py <TARGET> --strict # WARN cũng tính là FAIL

Kiểm tra (theo hợp đồng trong reference/dir-contract.md):
  1. Thư mục bắt buộc: diagrams/, images/diagrams/      -> thiếu = ERROR
     domain/step0*.md, audit/soi-so-do/                  -> thiếu = WARN
  2. Cặp 1:1 .svg <-> .png trong images/diagrams/       -> lệch = ERROR
     (bỏ qua thư mục bắt đầu bằng _ và __pycache__)
  3. Nguồn trong diagrams/: *.py *.puml *.dot *.drawio *.tldr
     -> không có nguồn nào = WARN (pack chỉ còn ảnh = mất truy vết)
  4. Mỗi thư mục audit chứa eye-audit.md phải có overlay.png + crops/
     -> thiếu = WARN

Exit code: 0 = PASS, 1 = có ERROR (hoặc WARN khi --strict).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SKIP_DIRS = {"__pycache__", ".git"}
SOURCE_EXTS = {".py", ".puml", ".dot", ".drawio", ".tldr"}


def is_skipped(name: str) -> bool:
    return name in SKIP_DIRS or name.startswith("_")


def walk_top(path: Path):
    """Duyệt đệ quy nhưng bỏ qua thư mục _legacy/__pycache__."""
    if not path.exists():
        return
    for entry in sorted(path.iterdir()):
        if entry.is_dir():
            if is_skipped(entry.name):
                continue
            yield from walk_top(entry)
        else:
            yield entry


def main() -> int:
    ap = argparse.ArgumentParser(description="Kiểm tra hợp đồng thư mục diagram pack")
    ap.add_argument("target", help="root của pack (vd .../private-docs)")
    ap.add_argument("--strict", action="store_true", help="WARN cũng tính là FAIL")
    args = ap.parse_args()

    root = Path(args.target)
    errors: list[str] = []
    warns: list[str] = []
    oks: list[str] = []

    if not root.is_dir():
        print(f"[ERROR] Không tìm thấy thư mục: {root}")
        return 1

    # ---- 1. Thư mục bắt buộc ----
    diagrams_dir = root / "diagrams"
    images_dir = root / "images" / "diagrams"
    domain_dir = root / "domain"
    audit_dir = root / "audit" / "soi-so-do"

    if diagrams_dir.is_dir():
        oks.append(f"diagrams/ tồn tại")
    else:
        errors.append("thiếu diagrams/ (code nguồn)")

    if images_dir.is_dir():
        oks.append("images/diagrams/ tồn tại")
    else:
        errors.append("thiếu images/diagrams/ (ảnh render)")

    step0 = sorted(domain_dir.glob("step0*.md")) if domain_dir.is_dir() else []
    if step0:
        oks.append(f"domain/step0: {step0[0].name}")
    else:
        warns.append("thiếu domain/step0-*.md (Bước 0 — bắt buộc trước khi vẽ Use Case)")

    if audit_dir.is_dir():
        oks.append("audit/soi-so-do/ tồn tại")
    else:
        warns.append("thiếu audit/soi-so-do/ (dấu vết soi mắt)")

    # ---- 2. Cặp 1:1 svg <-> png ----
    svgs: dict[str, Path] = {}
    pngs: dict[str, Path] = {}
    if images_dir.is_dir():
        for f in walk_top(images_dir):
            if f.suffix.lower() == ".svg":
                svgs[f.stem] = f
            elif f.suffix.lower() == ".png":
                pngs[f.stem] = f
        for stem in sorted(set(svgs) - set(pngs)):
            errors.append(f"cặp 1:1 lệch: {svgs[stem].relative_to(root)} thiếu .png")
        for stem in sorted(set(pngs) - set(svgs)):
            errors.append(f"cặp 1:1 lệch: {pngs[stem].relative_to(root)} thiếu .svg")
        if svgs and not (set(svgs) - set(pngs)) and not (set(pngs) - set(svgs)):
            oks.append(f"cặp 1:1: {len(svgs)} cặp .svg+.png khớp hết")

    # ---- 3. Nguồn trong diagrams/ ----
    sources: list[Path] = []
    if diagrams_dir.is_dir():
        for f in walk_top(diagrams_dir):
            if f.suffix.lower() in SOURCE_EXTS:
                sources.append(f)
        if sources:
            kinds = sorted({f.suffix.lower() for f in sources})
            oks.append(f"nguồn diagrams/: {len(sources)} file ({', '.join(kinds)})")
        else:
            warns.append("diagrams/ không có file nguồn nào (*.py/*.puml/*.dot/*.drawio/*.tldr)")

    # ---- 4. Audit folders ----
    audit_dirs = 0
    if audit_dir.is_dir():
        for f in walk_top(audit_dir):
            if f.name.lower() == "eye-audit.md":
                audit_dirs += 1
                parent = f.parent
                if not (parent / "overlay.png").exists():
                    warns.append(f"audit/{parent.relative_to(audit_dir)}: thiếu overlay.png")
                if not (parent / "crops").is_dir():
                    warns.append(f"audit/{parent.relative_to(audit_dir)}: thiếu crops/")
        if audit_dirs:
            oks.append(f"audit folders: {audit_dirs} thư mục có eye-audit.md")

    # ---- Báo cáo ----
    print(f"Diagram pack: {root}\n")
    for msg in oks:
        print(f"[OK]    {msg}")
    for msg in warns:
        print(f"[WARN]  {msg}")
    for msg in errors:
        print(f"[ERROR] {msg}")

    print()
    if errors or (args.strict and warns):
        print("Status: FAIL")
        return 1
    print("Status: PASS" + (" (có WARN — xem lại)" if warns else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
