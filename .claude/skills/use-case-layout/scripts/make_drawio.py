#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_drawio.py (v2) — sinh file .drawio WEB-EDITABLE cho Use Case (SKILL use-case-layout §3.4).

Muc dich: AI sinh ra file ma NGUOI DUNG mo bang web editor de tu keo-sua line:
  - app.diagrams.net (mien phi, cung paradigm Lucid: Straight/Elbow/Bendy line), hoac
  - Lucidchart: File -> Import documents -> chon file .drawio.
Edge sinh o che do GLUED (source/target id) + co dinh diem ra/vao (exitX/exitY, entryX/entryY)
=> keo hinh thi line di theo, diem neo giu nguyen (khong tut khoi shape).

BO CUC (v2 — thay bo cuc "cung tron" cu da bi loai):
  * CAM dat toan bo use case tren mot cung tron quanh actor: moi duong la mot ban kinh
    => chum day hoi tu dung 1 diem tren nguc actor = "con nhen/duoi cong". Khong ai ve vay.
  * Dung: use case cua MOI actor xep thanh COT doc theo CUM nghiep vu (cluster), cac cum
    lech nhau vai chuc px (bac thang nhe) de silhouette khong thanh mot duong keo dai.
    Cot doc la dieu kien de cac duong association KHONG BAO GIO cat nhau (thu tu y don dieu).
  * Duong association xuat phat tu DUNG MOT DIEM tai BUNG actor — junction (w/2, 2h/3) cua
    shape umlActor drawio (40x60 => exitX=0.5, exitY=0.667), tung day la 1 ban kinh rieng
    => "quat ga" goc chung kinh dien cua UML (yeu cau nguoi dung 2026-11-01). Goc giua 2 day
    ke phai >= ~12 deg (xep UC thanh cot doc theo cum de dam bao) thi eye_audit khong flag.
    Muon quay lai kieu rai neo doc canh tay (v2): dat "fan": "spread" trong spec.
  * Use case phu (include/extend) dat lech sang ben canh partner, day ngan (< 250px).
  * Ten actor dat DUOI chan (chuan UML); duong noi di ra tu canh tay nen khong bao gio xuyen ten.

Cach dung:
  python make_drawio.py --spec <model>.json --out docs/diagrams/<ten>.drawio [--svg-out <render>/<ten>.svg]
  -> ghi <ten>.drawio + SVG preview (CUNG toa do, cung diem neo) de chay eye_audit.py.
  Mac dinh SVG ghi CANH file .drawio (<ten>-preview.svg). Truyen --svg-out de dat SVG o
  thu muc render rieng (vd docs/images/diagrams/) — tranh nhan ban 2 ban SVG
  (yeu cau nguoi dung 2026-11-01: 1 diagram = 1 ban SVG duy nhat o thu muc render).

Spec JSON:
{
  "name": "san-tmbt-nguoi-ban",
  "title": "San TMBT", "subtitle": "Phan he nguoi ban",
  "actors": [{"id": "seller", "label": "Nguoi ban", "side": "L"}],
  "usecases": [
    {"id": "uc1", "label": "Dang ky mo gian hang", "cluster": "Tai khoan"},
    {"id": "qr", "label": "Dong goi va in tem QR", "secondary": true}
  ],
  "associations": [["seller", "uc1"]],
  "includes": [["uc_order", "qr"]],
  "extends": [["fb", "rating"]]
}
Ghi chu:
  - "x","y" tren usecase/actor = GHIM toa do (bo qua auto-layout).
  - "cluster" = ten cum nghiep vu; auto-layout chen khoang trong giua cac cum.
  - "secondary": true = use case phu (chi la dich cua include/extend, khong noi voi actor).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape

UC_W, UC_H = 170, 68
COL_X0 = 460.0          # x tam cot dau tien cua use case
ROW_PITCH = 132.0       # buoc doc trong 1 cum
CLUSTER_GAP = 42.0      # khoang trong them giua 2 cum (>= 1/3 buoc: mat thay ro nhom)
COL_DRIFT = 16.0        # moi cum lui sang phai 1 chut -> silhouette bac thang, khong thang thuoc
ACTOR_GAP = 210.0       # khoang cach actor -> cot use case gan nhat
NAME_DY = 54.0          # ten actor nam duoi chan (chi dung khi khong co nhan ben canh)
EXIT_BASE = 6.0         # (fan=spread) day neo lech xuong duoi tam actor 1 chut (tranh dau/co)
FAN_SPAN = 32.0         # (fan=spread) do rai diem neo doc THAN actor (px) — khong duoc cham vao dau
CHEST_DY = -4.0         # (fan=belly) gốc quạt tại KHUỶU TAY, tính từ TÂM actor (tay ở ay-4, đầu ở ay-22)
BELLY_DY = 10.0         # junction thân/chân của hình người que (dùng để VẼ actor, không dùng làm gốc quạt)
CURVE = 0.0             # mặc định = đường THẲNG (yêu cầu 2026-11-01: "vòng cung" = hình ellipse, dây nối thẳng)


def die(msg: str, code: int = 1) -> None:
    print(f"FAIL  {msg}", file=sys.stderr)
    raise SystemExit(code)


def wrap_label(text: str, width: int = 18, max_lines: int = 3) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if len(cand) <= width or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        head, tail = lines[: max_lines - 1], " ".join(lines[max_lines - 1:])
        lines = head + [tail]
    return lines


def ellipse_edge(cx, cy, rx, ry, outside):
    """Giao diem cua tia (tam -> outside) voi vien ellipse."""
    dx, dy = outside[0] - cx, outside[1] - cy
    if dx == 0 and dy == 0:
        return (cx + rx, cy)
    t = 1.0 / (math.sqrt((dx / rx) ** 2 + (dy / ry) ** 2) or 1.0)
    return (cx + dx * t, cy + dy * t)


def arc_control(p0, p1, amount: float = CURVE):
    """Diem trung gian cua quadratic Bezier -> day la VONG CUNG, khong phai duong thang.

    Chon phap tuyen sao cho cung bulge RA XA actor (cung dau voi dx): day roi khoi BUNG
    theo huong ra ngoai, khong chui nguoc vao than/dau actor.
    amount = 0 -> trung diem (duong thang).
    """
    if amount == 0:
        return ((p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0)
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    ln = math.hypot(dx, dy) or 1.0
    ux, uy = dx / ln, dy / ln
    nx, ny = -uy, ux
    if (dx >= 0 and nx < 0) or (dx < 0 and nx > 0):
        nx, ny = -nx, -ny
    mx, my = (p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0
    return (mx + nx * amount * ln, my + ny * amount * ln)


def bezier_point(p0, c, p1, t: float):
    u = 1.0 - t
    return (u * u * p0[0] + 2 * u * t * c[0] + t * t * p1[0],
            u * u * p0[1] + 2 * u * t * c[1] + t * t * p1[1])


def bezier_polyline(p0, c, p1, n: int = 20):
    if c is None:
        c = ((p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0)
    return [bezier_point(p0, c, p1, i / n) for i in range(n + 1)]


def seg_intersects_ellipse(p, q, cx, cy, rx, ry, shrink=0.92):
    """True neu doan p-q cat vao long ellipse (da thu nho de bo qua vet sat vien)."""
    rx, ry = rx * shrink, ry * shrink
    # dua ve he toa do don vi roi giai phuong trinh bac 2
    ax, ay = (p[0] - cx) / rx, (p[1] - cy) / ry
    bx, by = (q[0] - cx) / rx, (q[1] - cy) / ry
    dx, dy = bx - ax, by - ay
    a = dx * dx + dy * dy
    if a < 1e-9:
        return (ax * ax + ay * ay) < 1.0
    b = 2 * (ax * dx + ay * dy)
    c = ax * ax + ay * ay - 1.0
    disc = b * b - 4 * a * c
    if disc < 0:
        return False
    r = math.sqrt(disc)
    t1, t2 = (-b - r) / (2 * a), (-b + r) / (2 * a)
    return (0.02 < t1 < 0.98) or (0.02 < t2 < 0.98) or (t1 <= 0.02 and t2 >= 0.98)


def seg_cross(a, b, c, d):
    def orient(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

    def on(p, q, r):
        return min(p[0], r[0]) - 0.5 <= q[0] <= max(p[0], r[0]) + 0.5 and \
               min(p[1], r[1]) - 0.5 <= q[1] <= max(p[1], r[1]) + 0.5

    o1, o2 = orient(a, b, c), orient(a, b, d)
    o3, o4 = orient(c, d, a), orient(c, d, b)
    if ((o1 > 0) != (o2 > 0)) and ((o3 > 0) != (o4 > 0)):
        return True
    if abs(o1) < 1e-9 and on(a, c, b):
        return True
    if abs(o2) < 1e-9 and on(a, d, b):
        return True
    if abs(o3) < 1e-9 and on(c, a, d):
        return True
    if abs(o4) < 0.5 and on(c, b, d):
        return True
    return False


def layout(spec: dict):
    """Tra ve pos, edges(list dict), boundary, size. Khong dung cung tron."""
    actors = spec["actors"]
    ucs = spec["usecases"]
    assocs = [tuple(e) for e in spec.get("associations", [])]
    includes = [tuple(e) for e in spec.get("includes", [])]
    extends = [tuple(e) for e in spec.get("extends", [])]

    ids = [a["id"] for a in actors] + [u["id"] for u in ucs]
    if len(ids) != len(set(ids)):
        die("element_id trung lap trong spec")
    idset = set(ids)
    for e in assocs + includes + extends:
        for x in e:
            if x not in idset:
                die(f"edge tham chieu id khong ton tai: {x}")
    if not actors:
        die("spec thieu actors")

    sec_ids = {u["id"] for u in ucs if u.get("secondary")}
    pos: dict[str, tuple[float, float]] = {}

    # ---------- 1. GHIM toa do (neu co) ----------
    for u in ucs:
        if "x" in u and "y" in u:
            pos[u["id"]] = (float(u["x"]), float(u["y"]))
    for a in actors:
        if "x" in a and "y" in a:
            pos[a["id"]] = (float(a["x"]), float(a["y"]))

    # ---------- 2. AUTO: cot doc theo cum, bac thang nhe ----------
    auto = [u for u in ucs if u["id"] not in pos]
    cluster_order: list[str] = []
    for u in auto:
        c = u.get("cluster", "")
        if c not in cluster_order:
            cluster_order.append(c)
    y_cursor = 170.0
    for ci, cl in enumerate(cluster_order):
        members = [u for u in auto if u.get("cluster", "") == cl]
        x = COL_X0 + ci * COL_DRIFT
        for u in members:
            pos[u["id"]] = (x, y_cursor)
            y_cursor += ROW_PITCH
        y_cursor += CLUSTER_GAP - (ROW_PITCH - ROW_PITCH)  # giu nhip deu trong cum
    if cluster_order:
        y_cursor -= CLUSTER_GAP

    # actor auto: dat sat cot use case cua chinh no
    for a in actors:
        if a["id"] in pos:
            continue
        mine = [pos[t] for s, t in assocs if s == a["id"] and t in pos]
        if mine:
            cy = (min(p[1] for p in mine) + max(p[1] for p in mine)) / 2
            left = min(p[0] for p in mine) - UC_W / 2
            right = max(p[0] for p in mine) + UC_W / 2
        else:
            cy = 400.0
            left, right = COL_X0 - UC_W / 2, COL_X0 + UC_W / 2
        if a.get("side", "L") == "R":
            pos[a["id"]] = (right + ACTOR_GAP, cy)
        else:
            pos[a["id"]] = (max(90.0, left - ACTOR_GAP), cy)

    # ---------- 3. Neo day: hoi tu DUNG 1 DIEM tai BUNG actor (mac dinh "fan": "belly") ----------
    edges: list[dict] = []
    for s, t in assocs:
        edges.append({"kind": "assoc", "src": s, "dst": t, "label": ""})
    for s, t in includes:
        edges.append({"kind": "include", "src": s, "dst": t, "label": "«include»"})
    for s, t in extends:
        edges.append({"kind": "extend", "src": s, "dst": t, "label": "«extend»"})

    fan_mode = spec.get("fan", "belly")
    for a in actors:
        mine = [e for e in edges if e["kind"] == "assoc" and e["src"] == a["id"]]
        mine.sort(key=lambda e: pos[e["dst"]][1])
        n = len(mine)
        ax, ay = pos[a["id"]]
        right_side = a.get("side", "L") == "R"
        for k, e in enumerate(mine):
            if fan_mode == "spread":
                # kieu v2: rai neo doc canh tay, khong hoi tu 1 diem
                frac = (k + 0.5) / n - 0.5          # -0.5 .. +0.5
                oy = ay + EXIT_BASE + frac * FAN_SPAN
                ox = ax + (-22.0 if right_side else 22.0)
                e["exit"] = (0.0 if right_side else 1.0,
                             0.5 + (oy - ay) / 60.0)
            else:
                # kieu "quat ga" goc chung: hoi tu DUNG 1 DIEM o KHUYU TAY actor (junction than–tay).
                # Ly do: tia di LEN tu bung se cat ngang canh tay (do that: 1 canh vi pham F4).
                ox, oy = ax, ay + CHEST_DY
                e["exit"] = (0.5, 2.0 / 3.0)
            e["p0"] = (ox, oy)
            dx, dy = pos[e["dst"]]
            e["p1"] = ellipse_edge(dx, dy, UC_W / 2, UC_H / 2, (ox, oy))
            # Arc control: quadratic Bezier -> VONG CUNG (bulge ra xa actor)
            e["p2"] = arc_control(e["p0"], e["p1"], amount=CURVE)
            e["entry"] = (1.0 if right_side else 0.0,
                          0.5 + max(-0.38, min(0.38, (oy - dy) / UC_H)))

    for e in edges:
        if "p0" in e:
            continue
        s, t = e["src"], e["dst"]
        ps, pt = pos[s], pos[t]
        e["p0"] = ellipse_edge(ps[0], ps[1], UC_W / 2, UC_H / 2, pt)
        e["p1"] = ellipse_edge(pt[0], pt[1], UC_W / 2, UC_H / 2, ps)
        e["p2"] = arc_control(e["p0"], e["p1"], amount=CURVE)
        e["exit"] = (0.5, 0.5)
        e["entry"] = (0.5, 0.5)

    # ---------- 4. boundary + canvas ----------
    # day toan bo sang phai neu ten actor ben trai bi tran mep canvas
    shift = 0.0
    for a in actors:
        ax = pos[a["id"]][0]
        need = ax - (170.0 if a.get("side", "L") != "R" else 0.0)
        if need < 20.0:
            shift = max(shift, 20.0 - need)
    if shift:
        pos = {k: (p[0] + shift, p[1]) for k, p in pos.items()}
        for e in edges:
            e["p0"] = (e["p0"][0] + shift, e["p0"][1])
            e["p1"] = (e["p1"][0] + shift, e["p1"][1])
            e["p2"] = (e["p2"][0] + shift, e["p2"][1])

    xs = [p[0] for k, p in pos.items() if k not in {a["id"] for a in actors}]
    ys = [p[1] for k, p in pos.items() if k not in {a["id"] for a in actors}]
    bx0, bx1 = min(xs) - UC_W / 2 - 34, max(xs) + UC_W / 2 + 34
    by0, by1 = min(ys) - UC_H / 2 - 74, max(ys) + UC_H / 2 + 34
    W = bx1 + 40
    H = max(by1 + 40, max(p[1] for p in pos.values()) + 90)
    for a in actors:                      # chua cho ten actor dat BEN CANH (khong bi cat chu)
        ax, ay = pos[a["id"]]
        tw = 7.4 * len(a["label"]) + 34    # uoc luong be rong nhan
        if a.get("side", "L") == "R":
            W = max(W, ax + 28 + tw)
        H = max(H, ay + 60)
    return pos, edges, (bx0, by0, bx1, by1), (W, H)


def check_geometry(pos, edges, ucs):
    """Canh bao (khong chan) neu day CONG xuyen ellipse la hoac 2 day cat nhau.

    Kiem tren duong cong thuc te (sample quadratic Bezier), khong phai day cung.
    """
    warns = []
    polys = {id(e): bezier_polyline(e["p0"], e.get("p2"), e["p1"], n=16) for e in edges}
    for e in edges:
        pl = polys[id(e)]
        for u in ucs:
            if u["id"] in (e["src"], e["dst"]):
                continue
            cx, cy = pos[u["id"]]
            if any(seg_intersects_ellipse(pl[i], pl[i + 1], cx, cy, UC_W / 2, UC_H / 2)
                   for i in range(len(pl) - 1)):
                warns.append(f"day {e['src']}->{e['dst']} XUYEN ellipse '{u['label']}'")
    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            a, b = edges[i], edges[j]
            if {a["src"], a["dst"]} & {b["src"], b["dst"]}:
                continue
            if any(seg_cross(pa, pb, pc, pd)
                   for pa, pb in zip(polys[id(a)], polys[id(a)][1:])
                   for pc, pd in zip(polys[id(b)], polys[id(b)][1:])):
                warns.append(f"day {a['src']}->{a['dst']} CAT day {b['src']}->{b['dst']}")
    return warns


def build(spec: dict):
    name = spec.get("name", "usecase")
    title = spec.get("title", name)
    subtitle = spec.get("subtitle", "")
    actors = spec["actors"]
    ucs = spec["usecases"]
    pos, edges, boundary, (W, H) = layout(spec)
    bx0, by0, bx1, by1 = boundary

    warns = check_geometry(pos, edges, ucs)
    for w in warns:
        print(f"[CANH BAO] {w}", file=sys.stderr)

    cells = []

    def vertex(cid, value, style, cx, cy, w, h):
        cells.append(
            f'        <mxCell id="{escape(cid)}" value="{escape(value)}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{cx - w / 2:.0f}" y="{cy - h / 2:.0f}" width="{w:.0f}" height="{h:.0f}" as="geometry"/></mxCell>'
        )

    vertex("boundary", title,
           "rounded=1;whiteSpace=wrap;html=1;verticalAlign=top;fontSize=16;fontStyle=1;"
           "fillColor=none;strokeColor=#000000;arcSize=2;", (bx0 + bx1) / 2, (by0 + by1) / 2,
           bx1 - bx0, by1 - by0)
    if subtitle:
        vertex("subtitle", subtitle, "text;html=1;align=center;verticalAlign=middle;fontSize=12;",
               (bx0 + bx1) / 2, by0 + 46, 340, 24)
    for u in ucs:
        cx, cy = pos[u["id"]]
        vertex(u["id"], u["label"],
               "ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontSize=12;",
               cx, cy, UC_W, UC_H)
    for a in actors:
        cx, cy = pos[a["id"]]
        # Ten actor dat BEN CANH (trai cho Lane L / phai cho Lane R), canh giua theo chieu doc.
        # Ly do: khi actor co >=5 use case thi chum day toa rong > 45 deg; ten dat duoi chan
        # se bi chinh cac day do cat ngang (ca that L-ACTORNAME). Dat ben canh => vung toa sach.
        if a.get("side", "L") == "R":
            a_style = ("shape=umlActor;html=1;outlineConnect=0;labelPosition=right;"
                       "verticalLabelPosition=middle;align=left;spacingLeft=6;"
                       "fillColor=#FFFFFF;strokeColor=#000000;fontSize=12;")
        else:
            a_style = ("shape=umlActor;html=1;outlineConnect=0;labelPosition=left;"
                       "verticalLabelPosition=middle;align=right;spacingRight=6;"
                       "fillColor=#FFFFFF;strokeColor=#000000;fontSize=12;")
        vertex(a["id"], a["label"], a_style, cx, cy, 40, 60)

    def edge(cell_id, style, src, dst, label=""):
        lab = f' value="{escape(label)}"' if label else ""
        cells.append(
            f'        <mxCell id="{escape(cell_id)}"{lab} style="{style}" edge="1" parent="1" '
            f'source="{escape(src)}" target="{escape(dst)}"><mxGeometry relative="1" as="geometry"/></mxCell>'
        )

    for i, e in enumerate(edges):
        ex, ey = e["exit"]
        nx, ny = e["entry"]
        pin = f"exitX={ex:.3f};exitY={ey:.3f};exitDx=0;exitDy=0;entryX={nx:.3f};entryY={ny:.3f};entryDx=0;entryDy=0;"
        if e["kind"] == "assoc":
            edge(f"as{i}", "endArrow=none;html=1;rounded=0;curved=1;strokeColor=#000000;" + pin,
                 e["src"], e["dst"])
        else:
            style = ("endArrow=open;endFill=0;dashed=1;html=1;rounded=0;curved=1;fontSize=11;"
                     "labelBackgroundColor=#FFFFFF;strokeColor=#000000;" + pin)
            edge(f"r{i}", style, e["src"], e["dst"], e["label"])

    page_w = int(math.ceil(W / 50) * 50)
    page_h = int(math.ceil(H / 50) * 50)
    xml = "\n".join([
        '<mxfile host="app.diagrams.net" agent="sp-agent-use-case-layout" version="24.7.17">',
        f'  <diagram id="{hashlib.md5(name.encode()).hexdigest()[:12]}" name="Page-1">',
        f'    <mxGraphModel dx="1000" dy="640" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
        f'arrows="1" fold="1" page="1" pageScale="1" pageWidth="{page_w}" pageHeight="{page_h}" math="0" shadow="0">',
        '      <root>',
        '        <mxCell id="0"/>',
        '        <mxCell id="1" parent="0"/>',
        *cells,
        '      </root>',
        '    </mxGraphModel>',
        '  </diagram>',
        '</mxfile>',
        "",
    ])
    return xml, (W, H), boundary, pos, edges


def build_preview_svg(spec: dict, W, H, boundary, pos, edges) -> str:
    bx0, by0, bx1, by1 = boundary
    title = spec.get("title", "")
    subtitle = spec.get("subtitle", "")

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" '
         f'viewBox="0 0 {W:.0f} {H:.0f}">',
         f'<rect width="{W:.0f}" height="{H:.0f}" fill="white"/>',
         f'<rect x="{bx0:.0f}" y="{by0:.0f}" width="{bx1 - bx0:.0f}" height="{by1 - by0:.0f}" '
         f'fill="none" stroke="black" stroke-width="1.5" rx="8"/>',
         f'<text x="{(bx0 + bx1) / 2:.0f}" y="{by0 + 30:.0f}" font-size="16" font-weight="bold" '
         f'text-anchor="middle" font-family="Arial">{escape(title)}</text>']
    if subtitle:
        s.append(f'<text x="{(bx0 + bx1) / 2:.0f}" y="{by0 + 52:.0f}" font-size="12" '
                 f'text-anchor="middle" font-family="Arial">{escape(subtitle)}</text>')

    for u in spec["usecases"]:
        cx, cy = pos[u["id"]]
        s.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{UC_W / 2:.0f}" ry="{UC_H / 2:.0f}" '
                 f'fill="white" stroke="black" stroke-width="1.5"/>')
        lines = wrap_label(u["label"])
        n = len(lines)
        for i, ln in enumerate(lines):
            ty = cy + (i - (n - 1) / 2) * 15 + 4.3   # canh giua khoi chu theo chieu doc
            s.append(f'<text x="{cx:.0f}" y="{ty:.0f}" font-size="12" text-anchor="middle" '
                     f'font-family="Arial">{escape(ln)}</text>')

    for a in spec["actors"]:
        ax, ay = pos[a["id"]]
        s += [f'<circle cx="{ax:.0f}" cy="{ay - 22:.0f}" r="10" fill="white" stroke="black" stroke-width="1.6"/>',
              f'<line x1="{ax:.0f}" y1="{ay - 12:.0f}" x2="{ax:.0f}" y2="{ay + BELLY_DY:.0f}" stroke="black" stroke-width="1.8"/>',
              f'<line x1="{ax - 13:.0f}" y1="{ay - 4:.0f}" x2="{ax + 13:.0f}" y2="{ay - 4:.0f}" stroke="black" stroke-width="1.8"/>',
              f'<line x1="{ax:.0f}" y1="{ay + BELLY_DY:.0f}" x2="{ax - 13:.0f}" y2="{ay + 30:.0f}" stroke="black" stroke-width="1.8"/>',
              f'<line x1="{ax:.0f}" y1="{ay + BELLY_DY:.0f}" x2="{ax + 13:.0f}" y2="{ay + 30:.0f}" stroke="black" stroke-width="1.8"/>']
        if a.get("side", "L") == "R":
            s.append(f'<text x="{ax + 28:.0f}" y="{ay + 4:.0f}" font-size="12" text-anchor="start" '
                     f'font-family="Arial">{escape(a["label"])}</text>')
        else:
            s.append(f'<text x="{ax - 28:.0f}" y="{ay + 4:.0f}" font-size="12" text-anchor="end" '
                     f'font-family="Arial">{escape(a["label"])}</text>')

    for e in edges:
        p0, p1 = e["p0"], e["p1"]
        c = e.get("p2") or ((p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0)
        if CURVE == 0.0:
            # THANG (mặc định 2026-11-01)
            if e["kind"] == "assoc":
                s.append(f'<line x1="{p0[0]:.1f}" y1="{p0[1]:.1f}" x2="{p1[0]:.1f}" y2="{p1[1]:.1f}" '
                         f'stroke="black" stroke-width="1.2"/>')
                continue
            s.append(f'<line x1="{p0[0]:.1f}" y1="{p0[1]:.1f}" x2="{p1[0]:.1f}" y2="{p1[1]:.1f}" '
                     f'stroke="black" stroke-width="1.1" stroke-dasharray="5,4"/>')
            vx, vy = p0[0] - p1[0], p0[1] - p1[1]
        else:
            # VONG CUNG (chỉ bật khi người dùng yêu cầu rõ)
            arc = f'M {p0[0]:.1f} {p0[1]:.1f} Q {c[0]:.1f} {c[1]:.1f} {p1[0]:.1f} {p1[1]:.1f}'
            if e["kind"] == "assoc":
                s.append(f'<path d="{arc}" stroke="black" stroke-width="1.2" fill="none"/>')
                continue
            s.append(f'<path d="{arc}" stroke="black" stroke-width="1.1" '
                     f'stroke-dasharray="5,4" fill="none"/>')
            vx, vy = p1[0] - c[0], p1[1] - c[1]
        # dau mui ten HO tai p1 — tiep tuyen theo p0→p1 (straight) hoac p1−control (curved)
        vl = math.hypot(vx, vy) or 1.0
        vx, vy = vx / vl, vy / vl
        alen, acos, asin = 11.0, math.cos(math.radians(22)), math.sin(math.radians(22))
        for sgn in (1, -1):
            rx = vx * acos - sgn * vy * asin
            ry = vy * acos + sgn * vx * asin
            s.append(f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" '
                     f'x2="{p1[0] + rx * alen:.1f}" y2="{p1[1] + ry * alen:.1f}" '
                     f'stroke="black" stroke-width="1.1"/>')
        mx, my = bezier_point(p0, c, p1, 0.5)
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        ln = math.hypot(dx, dy) or 1.0
        px, py = -dy / ln, dx / ln
        if py > 0:
            px, py = -px, -py
        lx, ly = mx + px * 22, my + py * 22
        s.append(f'<rect x="{lx - 34:.0f}" y="{ly - 9:.0f}" width="68" height="16" fill="white"/>')
        s.append(f'<text x="{lx:.0f}" y="{ly + 3:.0f}" font-size="11" text-anchor="middle" '
                 f'font-family="Arial">{escape(e["label"])}</text>')
    s.append("</svg>")
    return "\n".join(s) + "\n"


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description="Sinh .drawio web-editable + SVG preview cho Use Case (SKILL §3.4).")
    ap.add_argument("--spec", required=True, help="file JSON model")
    ap.add_argument("--out", required=True, help="file .drawio dau ra")
    ap.add_argument("--svg-out", dest="svg_out", default=None,
                    help="duong dan SVG preview (vd docs/images/diagrams/<ten>.svg). "
                         "Bo qua = ghi <ten>-preview.svg canh file .drawio")
    args = ap.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.is_file():
        die(f"khong thay spec: {spec_path}")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    xml, (W, H), boundary, pos, edges = build(spec)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(xml, encoding="utf-8")

    try:
        root = ET.fromstring(xml)
    except ET.ParseError as e:
        die(f"XML sinh ra khong well-formed: {e}")
    vids = {c.get("id") for c in root.iter("mxCell") if c.get("vertex") == "1"}
    for c in root.iter("mxCell"):
        if c.get("edge") == "1":
            for ref in (c.get("source"), c.get("target")):
                if ref not in vids:
                    die(f"edge '{c.get('id')}' tham chieu id khong ton tai: {ref}")

    prev = Path(args.svg_out) if args.svg_out else out.with_name(out.stem + "-preview.svg")
    prev.parent.mkdir(parents=True, exist_ok=True)
    prev.write_text(build_preview_svg(spec, W, H, boundary, pos, edges), encoding="utf-8")

    print(f"OK    .drawio : {out}  ({len(vids)} node, WxH={W:.0f}x{H:.0f})")
    print(f"OK    preview : {prev}")
    print("      Buoc tiep theo (bat buoc):")
    print(f"      1. python .claude/skills/use-case-layout/scripts/eye_audit.py \"{prev}\" --overlay --dump")
    print("      2. Mo overlay.png + crops/ bang mat (3 nhip Buoc 4) — PASS thi moi ban giao")
    print("      3. Nguoi dung mo .drawio tai https://app.diagrams.net hoac Lucidchart (Import documents)")


if __name__ == "__main__":
    main()
