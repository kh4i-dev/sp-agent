#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_box_layout.py — kiểm định hình học cho sơ đồ HỘP từ layout spec JSON.

Dùng cho Class / ERD / BFD / kiến trúc: mọi sơ đồ mà phần tử là hộp đặt trên lưới cột.

Định dạng spec (giống docs/tools/layout_spec.json):
{
  "canvas": {"width": 2300, "height": 1100},
  "grid":   {"box_width": 300, "col_left": [20,500,980,1460,1940],
             "head_height": 40, "line_height": 21},
  "entities": [{"id": "user", "col": 0, "top": 70, "fields": ["id: int", ...]}, ...],
  "relationships": [{"id": "...", "a": "user", "b": "role",
                     "points": [[320,153],[362,153],[362,494],[320,494]]}, ...]
}

4 luật:
  E1 đầu mút quan hệ phải nằm TRÊN BIÊN hộp mà nó khai báo
  E2 đầu mút không được rơi vào LÒNG hộp khác
  E3 không có 2 hộp chồng nhau
  E4 không có đoạn dây nào xuyên qua lòng hộp trung gian

Chạy: py -3 verify_box_layout.py docs/tools/layout_spec.json
Mã thoát: 0 = PASS, 1 = FAIL.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

EPS = 1.0


def box_pos(spec: dict, eid: str) -> tuple[float, float, float, float]:
    ent = next(e for e in spec["entities"] if e["id"] == eid)
    g = spec["grid"]
    x1 = g["col_left"][ent["col"]]
    top = ent["top"]
    return (x1, top, x1 + g["box_width"],
            top + g["head_height"] + g["line_height"] * len(ent["fields"]))


def on_boundary(x, y, box) -> bool:
    x1, y1, x2, y2 = box
    ix = x1 - EPS <= x <= x2 + EPS
    iy = y1 - EPS <= y <= y2 + EPS
    return (iy and (abs(x - x1) <= EPS or abs(x - x2) <= EPS)) or \
           (ix and (abs(y - y1) <= EPS or abs(y - y2) <= EPS))


def inside(x, y, box) -> bool:
    x1, y1, x2, y2 = box
    return x1 + EPS < x < x2 - EPS and y1 + EPS < y < y2 - EPS


def seg_hits(xa, ya, xb, yb, box) -> bool:
    x1, y1, x2, y2 = box
    # Liang–Barsky works for diagonal segments as well as axis-aligned routes.
    x1+=EPS;y1+=EPS;x2-=EPS;y2-=EPS
    dx,dy=xb-xa,yb-ya;t0,t1=0.,1.
    for p,q in ((-dx,xa-x1),(dx,x2-xa),(-dy,ya-y1),(dy,y2-ya)):
        if abs(p)<1e-12:
            if q<0:return False
        else:
            t=q/p
            if p<0:t0=max(t0,t)
            else:t1=min(t1,t)
            if t0>t1:return False
    return t0<t1


def verify(spec: dict) -> list[str]:
    if not spec.get('entities'):
        return ['[E0] empty entities: no box layout was checked']
    if len({e['id'] for e in spec['entities']})!=len(spec['entities']):
        return ['[E0] duplicate entity IDs']
    boxes = {e["id"]: box_pos(spec, e["id"]) for e in spec["entities"]}
    errs: list[str] = []

    for rel in spec["relationships"]:
        a, b, pts = rel["a"], rel["b"], rel["points"]
        if a not in boxes or b not in boxes or len(pts)<2 or not all(len(p)==2 and all(isinstance(v,(int,float)) and math.isfinite(v) for v in p) for p in pts):
            return ['[E0] invalid relationship endpoints/coordinates']
        for eid, (px, py) in ((a, pts[0]), (b, pts[-1])):
            if not on_boundary(px, py, boxes[eid]):
                errs.append(f"[E1] {rel.get('id', a + '->' + b)}: đầu mút ({px},{py}) "
                            f"KHÔNG trên biên hộp '{eid}'")
            for other, ob in boxes.items():
                if other != eid and inside(px, py, ob):
                    errs.append(f"[E2] {rel.get('id', a + '->' + b)}: đầu mút ({px},{py}) "
                                f"rơi vào LÒNG hộp '{other}'")

    ids = list(boxes)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a1, b1, a2, b2 = boxes[ids[i]]
            c1, d1, c2, d2 = boxes[ids[j]]
            if a1 < c2 - EPS and c1 < a2 - EPS and b1 < d2 - EPS and d1 < b2 - EPS:
                errs.append(f"[E3] hộp '{ids[i]}' chồng hộp '{ids[j]}'")

    for rel in spec["relationships"]:
        a, b, pts = rel["a"], rel["b"], rel["points"]
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            for other, ob in boxes.items():
                if other not in (a, b) and seg_hits(xa, ya, xb, yb, ob):
                    errs.append(f"[E4] {rel.get('id', a + '->' + b)}: đoạn ({xa},{ya})→({xb},{yb}) "
                                f"xuyên hộp '{other}'")
    return errs


def main() -> int:
    if len(sys.argv) < 2:
        print("Dùng: py -3 verify_box_layout.py <layout_spec.json>", file=sys.stderr)
        return 1
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errs = verify(spec)
    if errs:
        print(f"FAIL — {len(errs)} lỗi hình học:\n")
        for e in errs:
            print("  " + e)
        return 1
    n_fields = sum(len(e["fields"]) for e in spec["entities"])
    print(f"PASS — {len(spec['entities'])} hộp / {n_fields} trường, "
          f"{len(spec['relationships'])} quan hệ, 0 lỗi (E1..E4)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
