#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_frontmatter.py — đo description + số dòng SKILL.md (chặn WARN của audit-skills.ps1).

Ngưỡng (theo tools/audit-skills.ps1): description <= 1024 ký tự, SKILL.md <= 500 dòng,
description >= 40 ký tự.
Chạy: py -3 tools/check_frontmatter.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SK = ROOT / ".claude" / "skills"


def main() -> int:
    bad = 0
    rows = []
    for p in sorted(SK.glob("*/SKILL.md")):
        t = p.read_text(encoding="utf-8")
        m = re.search(r"^---\s*\n(.*?)\n---", t, re.S)
        if not m:
            rows.append((p.parent.name, "NO-FM", t.count("\n") + 1, ["thiếu frontmatter"]))
            bad += 1
            continue
        dm = re.search(r"^description:\s*(.*)$", m.group(1), re.S | re.M)
        desc = (dm.group(1) if dm else "").strip().strip('"').strip("'")
        n = len(desc)
        lines = t.count("\n") + 1
        issues = []
        if n > 1024:
            issues.append(f"description {n} > 1024")
        if n < 40:
            issues.append(f"description {n} < 40")
        if lines > 500:
            issues.append(f"{lines} dòng > 500")
        if issues:
            bad += 1
        rows.append((p.parent.name, n, lines, issues))

    for name, n, lines, issues in rows:
        mark = ("  <-- " + "; ".join(issues)) if issues else ""
        print(f"{name:34} desc={n!s:>6}  lines={lines:>4}{mark}")

    print(f"\n{len(rows)} skill · {bad} vượt ngưỡng")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
