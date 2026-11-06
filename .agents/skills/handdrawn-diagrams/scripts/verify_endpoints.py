#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_endpoints.py — KIỂM ĐỊNH HÌNH HỌC sơ đồ class/ERD trước khi công bố.

Không nhân bản logic: gọi thẳng `check_geometry()` của generator (một nguồn sự thật).
Bộ kiểm gồm 4 luật:
  E1. Mỗi đầu mút quan hệ phải nằm TRÊN BIÊN của hộp mà quan hệ khai báo.
  E2. Đầu mút không được rơi vào lòng bất kỳ hộp nào.
  E3. Không có 2 hộp nào chồng lên nhau.
  E4. Không có đoạn dây nào cắt qua lòng hộp trung gian.

Chạy: py -3 docs/tools/verify_endpoints.py
Mã thoát: 0 = PASS, 1 = FAIL (in danh sách lỗi).
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
GEN = HERE.parents[1] / "diagrams" / "gen_class_erd.py"


def load_gen():
    spec = importlib.util.spec_from_file_location("gen_class_erd", GEN)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    g = load_gen()
    errors = g.check_geometry()
    if errors:
        print(f"FAIL — {len(errors)} lỗi hình học:\n")
        for e in errors:
            print("  " + e)
        return 1
    total_fields = sum(len(e[4]) for e in g.ENT)
    print(f"PASS — {len(g.ENT)} hộp / {total_fields} trường, {len(g.REL)} quan hệ, 0 lỗi hình học")
    print("       (E1 đầu mút trên biên · E2 không trong lòng hộp · E3 không chồng · E4 không xuyên hộp)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
