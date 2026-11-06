#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_fan_arc.py — cổng kiểm TẤT ĐỊNH cho luật Use Case (straight mode, 2026-11-01).

YÊU CẦU MỚI (thay thế luật cũ "vòng cung"):
  "các line thẳng" = đường nối actor → use case PHẢI là đoạn thẳng (không Q/C).
  "vòng cung" = hình ellipse (chức năng), KHÔNG phải dây nối.

Luật kiểm (đọc thẳng file SVG đã render, không cần mắt):
  F1 MOT-DIEM  mọi association của một actor xuất phát từ ĐÚNG 1 điểm
               (khuỷu tay = giao giữa thân và tay, y = hy+18; hy là tâm đầu).
  F2 THANG     association phải là ĐOẠN THẲNG — thẻ <line> hoặc <path d="M.. L..">;
               cấm <path> có lệnh Q hoặc C (cung Bezier).
  F3 CLEAR-HEAD cung/đường không được đi vào đầu actor (vòng tròn r=10).
  F4 CLEAR-ARM cung/đường không được cắt qua cánh tay actor (đoạn ngang y=hy+18).
  F5 HAS-EDGE  actor có association (không có thì không kết luận gì).

Cách nhận diện (không cần đọc spec):
  - actor = các <circle r="10">; origin = (cx, cy + 18)  [đầu ở cy, chân ở cy+32,
    khuỷu tay ở cy+18 = junction thân–tay].
  - association = line/path có điểm ĐẦU trùng origin (sai số 2 px).
  - include/extend = line/path bắt đầu ở mép ellipse (không tính vào F1/F2).
  - để bỏ qua, các dòng <line> nối hai điểm đầu cuối cách origin > MATCH:
      + chân actor (xuất phát tại cy+32, đi chéo)
      + tay actor (ngang tại cy+18, nhưng 2 điểm đều nằm cách origin 13–16 px)
      + chân/nhãn tên dưới chân

Chạy:
  py -3 docs/tools/check_fan_arc.py                       # quét vectors/*.svg
  py -3 docs/tools/check_fan_arc.py path1.svg             # kiểm 1 file
Mã thoát: 0 = PASS hết · 1 = có lỗi · 2 = không có file use case nào.
"""
from __future__ import annotations

import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VEC = ROOT / "docs" / "diagrams" / "vectors"
NS = "{http://www.w3.org/2000/svg}"

HEAD_R = 10.0
ORIGIN_DY = 18.0          # khuỷu tay = junction than–tay (hy + 18)
ARM_HALF = 16.0           # nửa sải tay trong hình người que
MATCH = 2.0               # sai số nhận diện điểm đầu = origin
SAMPLE = 40               # số điểm lấy mẫu trên path
LEG_HALF = 13.0           # nửa sải chân (dùng để lọc chân actor)
LEG_DY_START = 32.0       # chân xuất phát tại hy + 32
LEG_LEN = 20.0            # chân dài 20 px

# Các phần tử đồ họa của actor (chỉ dùng để BỎ QUA khi kiểm định)
def _actor_glyph_segments(circles):
    """Trả về danh sách các đoạn tay/chân của từng actor (dùng để kiểm F4)."""
    skips = []
    for cx, cy, r in circles:
        if abs(r - HEAD_R) > 0.6:
            continue
        # tay: đoạn ngang tại cy+18
        tx = cx - ARM_HALF - 2
        ty = cy + ORIGIN_DY
        skips.append(((tx, ty), (tx + 2 * ARM_HALF + 4, ty)))
        # 2 chân chéo từ (cx, cy+32)
        skips.append(((cx, cy + LEG_DY_START), (cx - LEG_HALF, cy + LEG_DY_START + LEG_LEN)))
        skips.append(((cx, cy + LEG_DY_START), (cx + LEG_HALF, cy + LEG_DY_START + LEG_LEN)))
    return skips


def _seg_intersect_skip(seg, skip, t_min: float = 0.03) -> bool:
    """True nếu seg cắt skip Ở GIỮA (bỏ qua giao ngay tại điểm xuất phát, t < t_min)."""
    p, q = seg
    a, b = skip
    rx, ry = q[0] - p[0], q[1] - p[1]
    sx, sy = b[0] - a[0], b[1] - a[1]
    den = rx * sy - ry * sx
    if abs(den) < 1e-9:
        return False
    t = ((a[0] - p[0]) * sy - (a[1] - p[1]) * sx) / den
    u = ((a[0] - p[0]) * ry - (a[1] - p[1]) * rx) / den
    return t_min <= t <= 1.0 and 0.0 <= u <= 1.0


def fnum(el, name: str, default: float = 0.0) -> float:
    v = el.get(name)
    if v is None:
        return default
    m = re.match(r"^\s*(-?[\d.]+)", v)
    return float(m.group(1)) if m else default


def parse_d(d: str):
    """Trả về (start, kind, pts). kind in {'L','Q','C'}."""
    toks = re.findall(r"([MLHVZQCSmlhvzqcs])|(-?[\d.]+(?:e-?\d+)?)", d)
    cmds: list[tuple[str, list[float]]] = []
    cur = None
    for c, n in toks:
        if c:
            cur = (c, [])
            cmds.append(cur)
        elif cur is not None:
            cur[1].append(float(n))

    start = None
    kind = "L"
    pts: list[tuple[float, float]] = []
    x = y = 0.0
    for c, v in cmds:
        u = c.upper()
        if u == "M":
            for i in range(0, len(v) - 1, 2):
                x, y = v[i], v[i + 1]
                if start is None:
                    start = (x, y)
                    pts.append((x, y))
        elif u == "L":
            for i in range(0, len(v) - 1, 2):
                x, y = v[i], v[i + 1]
                pts.append((x, y))
        elif u in ("Q", "C"):
            kind = u
            if u == "Q":
                cp = (v[0], v[1]); p1 = (v[2], v[3]) if len(v) >= 4 else (x, y)
            else:
                cp = (v[0], v[1]); cp2 = (v[2], v[3]); p1 = (v[4], v[5]) if len(v) >= 6 else (x, y)
            for i in range(1, SAMPLE + 1):
                t = i / SAMPLE
                if u == "Q":
                    a, b, cc = (1 - t) ** 2, 2 * (1 - t) * t, t * t
                    px = a * x + b * cp[0] + cc * p1[0]
                    py = a * y + b * cp[1] + cc * p1[1]
                else:
                    a, b, cc, dd = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
                    px = a * x + b * cp[0] + cc * cp2[0] + dd * p1[0]
                    py = a * y + b * cp[1] + cc * cp2[1] + dd * p1[1]
                pts.append((px, py))
            x, y = p1
    return start, kind, pts


def dist(a, b) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def seg_cross(p, q, a, b) -> bool:
    def orient(o, s, t):
        return (s[0] - o[0]) * (t[1] - o[1]) - (s[1] - o[1]) * (t[0] - o[0])
    o1, o2 = orient(p, q, a), orient(p, q, b)
    o3, o4 = orient(a, b, p), orient(a, b, q)
    return ((o1 > 0) != (o2 > 0)) and ((o3 > 0) != (o4 > 0))


def check(path: Path) -> tuple[list[str], dict]:
    root = ET.fromstring(path.read_text(encoding="utf-8"))
    circles = []
    for el in root.iter():
        if el.tag == NS + "circle":
            circles.append((fnum(el, "cx"), fnum(el, "cy"), fnum(el, "r")))
    heads = [(cx, cy) for cx, cy, r in circles if abs(r - HEAD_R) < 0.6]
    origins = [(cx, cy + ORIGIN_DY) for cx, cy in heads]
    skips = _actor_glyph_segments(circles)

    paths_raw = [el.get("d") or "" for el in root.iter() if el.tag == NS + "path"]
    lines_raw = [el for el in root.iter() if el.tag == NS + "line"]

    # gộp thành danh sách đoạn/dây với điểm đầu
    segments: list[tuple[tuple[float, float], str, list[tuple[float,float]], str]] = []
    for d in paths_raw:
        start, kind, pts = parse_d(d)
        if start is not None:
            segments.append((start, kind, pts, d))
    for el in lines_raw:
        p0 = (fnum(el, "x1"), fnum(el, "y1"))
        p1 = (fnum(el, "x2"), fnum(el, "y2"))
        # bỏ qua chân/tay actor (đã xác định qua skips) — nhưng detect đơn giản hơn:
        # bỏ qua đoạn mà cả 2 đầu đều nằm trong ±(ARM_HALF+2) quanh gốc actor và |dy|<2
        # (tay) hoặc bắt đầu tại LEG_DY_START (chân).
        # Thực tế ta dựa vào _seg_intersect_skip để lọc F4, còn F2 kiểm kind.
        segments.append((p0, "L", [p0, p1], ""))

    errs: list[str] = []
    stat = {"actors": len(heads), "paths": len(paths_raw), "assoc": 0, "arcs": 0, "straight": 0}

    by_origin: list[list[tuple]] = [[] for _ in origins]
    for seg_start, kind, pts, d in segments:
        idx = next((i for i, o in enumerate(origins) if dist(seg_start, o) <= MATCH), None)
        if idx is None:
            continue
        by_origin[idx].append((seg_start, kind, pts, d))
        stat["assoc"] += 1
        if kind in ("Q", "C"):
            stat["arcs"] += 1
        else:
            stat["straight"] += 1

    for i, items in enumerate(by_origin):
        if not items:
            errs.append(f"[F5] {path.name}: actor #{i} has no recognized association")
            continue
        starts = {(round(s[0], 1), round(s[1], 1)) for s, _, _, _ in items}
        if len(starts) > 1:
            errs.append(f"[F1] {path.name}: actor #{i} có {len(starts)} điểm xuất phát khác nhau "
                        f"(phải ĐÚNG 1 điểm khuỷu tay): {sorted(starts)}")
        hx, hy = heads[i]
        # F2: cấm Q/C
        for _, kind, _, d in items:
            if kind in ("Q", "C"):
                errs.append(f"[F2] {path.name}: association là CUNG (Q/C) ở actor #{i} "
                            f"({items[0][0][0]:.0f},{items[0][0][1]:.0f})")
        # F3: cắt đầu actor
        for _, _, pts, _ in items:
            for p in pts[1:]:            # bỏ qua điểm đầu (đã là origin)
                if dist(p, (hx, hy)) < HEAD_R + 0.5:
                    errs.append(f"[F3] {path.name}: association đi vào ĐẦU actor #{i} tại "
                                f"({p[0]:.0f},{p[1]:.0f})")
                    break
        # F4: cắt cánh tay hoặc chân actor
        # Tìm chính xác cánh tay và chân từ SVG để check giao điểm
        arm_seg = None
        leg_segs = []
        for a, b in skips:
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            # cánh tay: đoạn ngắn ngang gần origin (dy ≈ 0, |dx| ≤ 32)
            if abs(b[1] - a[1]) < 0.6 and abs(b[0] - a[0]) <= ARM_HALF * 2 + 6 and abs(mx-hx)<1 and abs(my-hy-ORIGIN_DY)<1:
                arm_seg = (a, b)
            elif abs(a[0] - hx) <= LEG_HALF + 2 and abs(b[0] - hx) <= LEG_HALF + 2:
                # chân: gần trục actor
                leg_segs.append((a, b))
        for _, _, pts, _ in items:
            for j in range(len(pts) - 1):
                p, q = pts[j], pts[j + 1]
                if arm_seg and _seg_intersect_skip((p, q), arm_seg):
                    errs.append(f"[F4] {path.name}: association CẮT CÁNH TAY actor #{i}")
                    break
                for ls in leg_segs:
                    if _seg_intersect_skip((p, q), ls):
                        errs.append(f"[F4] {path.name}: association CẮT CHÂN actor #{i}")
                        break
                else:
                    continue
                break

    if heads and stat["assoc"] == 0:
        errs.append(f"[F5] {path.name}: có {len(heads)} actor nhưng 0 association nhận diện được")

    return errs, stat


def main() -> int:
    files = [Path(f) for f in sys.argv[1:]] or sorted(VEC.glob("*.svg"))
    tot_e = 0
    touched = 0
    for f in files:
        errs, stat = check(f)
        if stat["actors"] == 0:
            continue
        touched += 1
        tot_e += len(errs)
        mark = "PASS" if not errs else "FAIL"
        print(f"[{mark}] {f.name}  actor={stat['actors']} assoc={stat['assoc']} "
              f"arc={stat['arcs']} straight={stat['straight']}")
        for e in errs:
            print("   " + e)

    if touched == 0:
        print("Không có sơ đồ use case nào (không có <circle r=10>) — không kết luận.")
        return 2
    print(f"\n=== {touched} sơ đồ use case · {tot_e} lỗi (F1..F5) ===")
    return 1 if tot_e else 0


if __name__ == "__main__":
    sys.exit(main())
