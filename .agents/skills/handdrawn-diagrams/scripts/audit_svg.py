#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit_svg.py — kiểm định hình học TẤT ĐỊNH cho mọi sơ đồ SVG (không cần mắt người).

Vì sao cần: "render exit 0" và "script không đỏ" KHÔNG chứng minh sơ đồ đẹp.
Bộ này đọc chính file SVG đã render và bắt các lỗi đo được:

  E1 CANVAS   — phần tử nằm ngoài khung vẽ (bị cắt khi in)
  E2 TEXTOVL  — hai nhãn chồng lên nhau (đè chữ)
  E3 LINEOVL  — đường nối cắt xuyên qua nhãn (không có halo/nền trắng che)
  E4 OUTSHAPE — chữ tràn ra ngoài hình bao của nó (ellipse/hộp)
  E5 DUPLICATE— id trùng / phần tử trùng khít
  E6 EMPTY    — text rỗng hoặc toạ độ NaN

Nguyên tắc tránh báo oan:
  - Chữ có `paint-order=stroke` + stroke trắng (halo) => bỏ qua E3 (dây bị halo che).
  - Chữ có hình chữ nhật trắng phủ phía sau => bỏ qua E3.
  - Bề rộng chữ ước lượng theo font-size (Arial ~0.55em/ký tự).

Chạy:
  py -3 docs/tools/audit_svg.py                     # quét docs/diagrams/vectors/*.svg
  py -3 docs/tools/audit_svg.py --json out.json     # kèm xuất JSON
  py -3 docs/tools/audit_svg.py path1.svg path2.svg # chỉ định file

Mã thoát: 0 = PASS (0 lỗi), 1 = có lỗi mức E, 2 = chỉ có cảnh báo.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VEC = ROOT / "docs" / "diagrams" / "vectors"


def _resolve_vec(explicit_root: str | None) -> Path:
    """Tìm thư mục chứa SVG: --root/docs/diagrams/vectors, hoặc leo lên từ cwd."""
    if explicit_root:
        return Path(explicit_root) / "docs" / "diagrams" / "vectors"
    cur = Path.cwd().resolve()
    for d in (cur, *cur.parents):
        cand = d / "docs" / "diagrams" / "vectors"
        if cand.is_dir():
            return cand
    return VEC
NS = "{http://www.w3.org/2000/svg}"
CHAR_W = 0.55          # bề rộng trung bình 1 ký tự theo em (Arial)
PAD = 1.5              # nới hộp chữ khi xét chồng lấn


class Box:
    __slots__ = ("x1", "y1", "x2", "y2")

    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def overlap(self, o: "Box") -> float:
        w = min(self.x2, o.x2) - max(self.x1, o.x1)
        h = min(self.y2, o.y2) - max(self.y1, o.y1)
        return w * h if w > 0 and h > 0 else 0.0

    def area(self) -> float:
        return max(0.0, self.x2 - self.x1) * max(0.0, self.y2 - self.y1)

    def inside(self, o: "Box", tol=0.0) -> bool:
        return (self.x1 >= o.x1 - tol and self.x2 <= o.x2 + tol
                and self.y1 >= o.y1 - tol and self.y2 <= o.y2 + tol)


def fnum(el, name, default=0.0) -> float:
    v = el.get(name)
    if v is None:
        return default
    m = re.fullmatch(r"\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)(?:px)?\s*", v)
    return float(m.group(1)) if m else default


def text_width(s: str, fs: float) -> float:
    # ký tự hẹp/rộng khác nhau; ước lượng đủ tốt để phát hiện tràn/đè
    narrow = sum(1 for c in s if c in "iljI.,:;'|!()[]{}")
    wide = sum(1 for c in s if c in "mwMWĐÔƠƯÀÁẢÃẠ")
    return fs * (CHAR_W * (len(s) - narrow - wide) + 0.30 * narrow + 0.85 * wide)


def text_box(t) -> tuple[Box, str]:
    s = "".join(t.itertext())
    fs = fnum(t, "font-size", 12.0)
    x, y = fnum(t, "x"), fnum(t, "y")
    anchor = t.get("text-anchor", "start")
    w = text_width(s, fs)
    if anchor == "middle":
        x1 = x - w / 2
    elif anchor == "end":
        x1 = x - w
    else:
        x1 = x
    return Box(x1, y - 0.78 * fs, x1 + w, y + 0.24 * fs), s


def parse_path_segments(d: str) -> list[tuple[float, float, float, float]]:
    """Bóc mọi đoạn thẳng khỏi path: M/L/H/V/Z + mẫu hoá Q (bậc 2) và C (bậc 3).

    Sơ đồ vẽ tay dùng `M ... Q ...` cho vòng cung → nếu bỏ qua Q thì lỗi E3
    (dây cắt nhãn) sẽ lọt qua. Vì vậy phải mẫu hoá đường cong thành đoạn thẳng.
    """
    toks = re.findall(r"([MLHVZQCSmlhvzqcs])|(-?[\d.]+(?:e-?\d+)?)", d)
    cmds: list[tuple[str, list[float]]] = []
    cur = None
    for c, n in toks:
        if c:
            cur = [c, []]
            cmds.append(cur)
        elif cur is not None:
            cur[1].append(float(n))
    segs: list[tuple[float, float, float, float]] = []
    x = y = 0.0
    sx = sy = 0.0
    N = 10          # số đoạn thẳng xấp xỉ cho mỗi đường cong

    def quad(p0, cp, p1):
        prev = p0
        for i in range(1, N + 1):
            t = i / N
            u = 1 - t
            pt = (u * u * p0[0] + 2 * u * t * cp[0] + t * t * p1[0],
                  u * u * p0[1] + 2 * u * t * cp[1] + t * t * p1[1])
            segs.append((prev[0], prev[1], pt[0], pt[1]))
            prev = pt

    def cubic(p0, c0, c1, p1):
        prev = p0
        for i in range(1, N + 1):
            t = i / N
            u = 1 - t
            pt = (u**3 * p0[0] + 3 * u * u * t * c0[0] + 3 * u * t * t * c1[0] + t**3 * p1[0],
                  u**3 * p0[1] + 3 * u * u * t * c0[1] + 3 * u * t * t * c1[1] + t**3 * p1[1])
            segs.append((prev[0], prev[1], pt[0], pt[1]))
            prev = pt

    for c, vals in cmds:
        u = c.upper()
        if u == "M":
            for i in range(0, len(vals) - 1, 2):
                x, y = vals[i], vals[i + 1]
                if i == 0:
                    sx, sy = x, y
        elif u == "L":
            for i in range(0, len(vals) - 1, 2):
                nx, ny = vals[i], vals[i + 1]
                segs.append((x, y, nx, ny))
                x, y = nx, ny
        elif u == "H":
            for v in vals:
                segs.append((x, y, v, y))
                x = v
        elif u == "V":
            for v in vals:
                segs.append((x, y, x, v))
                y = v
        elif u == "Q":
            i = 0
            p0 = (x, y)
            while i + 3 < len(vals):
                cp = (vals[i], vals[i + 1])
                p1 = (vals[i + 2], vals[i + 3])
                quad(p0, cp, p1)
                p0 = p1
                i += 4
            x, y = p0
        elif u == "C":
            i = 0
            p0 = (x, y)
            while i + 5 < len(vals):
                c0 = (vals[i], vals[i + 1])
                c1 = (vals[i + 2], vals[i + 3])
                p1 = (vals[i + 4], vals[i + 5])
                cubic(p0, c0, c1, p1)
                p0 = p1
                i += 6
            x, y = p0
        elif u == "Z":
            segs.append((x, y, sx, sy))
            x, y = sx, sy
    return segs


def seg_hits_box(sx, sy, ex, ey, b: Box, pad=0.0) -> bool:
    """Đoạn thẳng có đi vào LÒNG hộp (đã nới pad) không — dùng Liang-Barsky."""
    x1, y1, x2, y2 = b.x1 - pad, b.y1 - pad, b.x2 + pad, b.y2 + pad
    dx, dy = ex - sx, ey - sy
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, sx - x1), (dx, x2 - sx), (-dy, sy - y1), (dy, y2 - sy)):
        if abs(p) < 1e-12:
            if q < 0:
                return False
        else:
            t = q / p
            if p < 0:
                if t > t1:
                    return False
                t0 = max(t0, t)
            else:
                if t < t0:
                    return False
                t1 = min(t1, t)
    return t0 < t1


def has_halo(t) -> bool:
    return (t.get("paint-order") or "").startswith("stroke") and \
           t.get("stroke", "").lower() in ("white", "#fff", "#ffffff") and \
           fnum(t, "stroke-width", 1) > 0 and fnum(t, "opacity", 1) == 1 and fnum(t, "stroke-opacity", 1) == 1


def svg_elements(root, errors):
    """Resolve inherited presentation and translate/scale; reject other transforms.

    This is a deliberately bounded SVG dialect, not a full browser renderer.
    Unsupported geometry must fail closed instead of being silently skipped.
    """
    inherited_keys = {'font-size', 'font-family', 'text-anchor', 'fill', 'stroke',
                      'stroke-width', 'paint-order', 'opacity', 'stroke-opacity'}
    def walk(el, inherited, matrix):
        tag = el.tag.replace(NS, '')
        if tag in ('defs', 'marker', 'metadata', 'title', 'desc'):
            return
        attrs = dict(inherited)
        attrs.update(el.attrib)
        for item in el.get('style', '').split(';'):
            if ':' in item:
                key, value = item.split(':', 1); attrs[key.strip()] = value.strip()
        if attrs.get('display') == 'none' or attrs.get('visibility') == 'hidden':
            return
        sx, sy, tx, ty = matrix
        transform = el.get('transform', '')
        matches = list(re.finditer(r'(translate|scale)\s*\(([^)]*)\)', transform))
        rest = re.sub(r'(translate|scale)\s*\([^)]*\)', '', transform).strip(' ,\t\r\n')
        if rest:
            errors.append({'code': 'E7', 'msg': f'unsupported transform: {transform}'})
        for match in matches:
            try:
                values = [float(x) for x in re.split(r'[ ,]+', match.group(2).strip())]
                if len(values) not in (1, 2) or not all(math.isfinite(v) for v in values):
                    raise ValueError()
                if match.group(1) == 'translate':
                    tx += sx*values[0]; ty += sy*(values[1] if len(values)>1 else 0)
                else:
                    sx *= values[0]; sy *= values[1] if len(values)>1 else values[0]
            except ValueError:
                errors.append({'code': 'E6', 'msg': f'invalid transform: {transform}'})
        if tag in ('style', 'use', 'image', 'foreignObject') or (tag == 'tspan' and any(k in el.attrib for k in ('x','y','dx','dy','transform'))):
            errors.append({'code':'E7','msg':f'unsupported geometry/style element: {tag}; flatten to explicit coordinates'})
        numeric = {'x','y','x1','x2','y1','y2','cx','cy','r','rx','ry','width','height','font-size','stroke-width'}
        for key,value in attrs.items():
            if key in numeric:
                if re.search(r'(?i)nan|inf', value):
                    errors.append({'code':'E6','msg':f'non-finite {key}: {value}'})
                elif not re.fullmatch(r'\s*[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?(?:px|%)?\s*',value):
                    errors.append({'code':'E7','msg':f'unsupported numeric {key}: {value}'})
            if key in ('d','points') and re.search(r'(?i)nan|\binf',value):
                errors.append({'code':'E6','msg':f'non-finite {key}'})
        effective = ET.Element(el.tag, attrs)
        effective.text = ''.join(el.itertext()) if tag == 'text' else el.text
        yield effective, (sx,sy,tx,ty)
        child_attrs = {k:v for k,v in attrs.items() if k in inherited_keys}
        for child in el:
            if tag != 'text':
                yield from walk(child, child_attrs, (sx,sy,tx,ty))
            elif child.tag.replace(NS,'') == 'tspan' and any(k in child.attrib for k in ('x','y','dx','dy','transform')):
                errors.append({'code':'E7','msg':'positioned tspan unsupported; use separate text elements'})
    yield from walk(root, {}, (1,1,0,0))


def audit(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    errs: list[dict] = []
    warns: list[dict] = []

    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        return {"file": path.name, "errors": [{"code": "E0", "msg": f"XML hỏng: {e}"}], "warnings": []}

    W, H = fnum(root, "width", 0), fnum(root, "height", 0)
    if not W or not H:
        vb = (root.get("viewBox") or "").split()
        if len(vb) == 4:
            W, H = float(vb[2]), float(vb[3])
    if not all(math.isfinite(v) and v>0 for v in (W,H)):
        return {'file':path.name,'errors':[{'code':'E6','msg':'invalid canvas dimensions'}],'warnings':[]}
    vb=(root.get('viewBox') or '').split()
    if len(vb)==4 and (float(vb[0])!=0 or float(vb[1])!=0 or float(vb[2])!=W or float(vb[3])!=H):
        errs.append({'code':'E7','msg':'normalize viewBox to 0 0 width height before audit'})
    canvas = Box(0, 0, W, H)

    texts: list[tuple[Box, str, object]] = []
    white_rects = []
    shapes: list[Box] = []
    all_segs: list[tuple[float, float, float, float]] = []
    seg_orders = []
    text_orders = {}
    drawn_bounds = []
    ids: dict[str, int] = {}

    for original in root.iter():
        if original.get('id'):
            key=original.get('id');ids[key]=ids.get(key,0)+1
    for order, (el, matrix) in enumerate(svg_elements(root, errs)):
        sx,sy,tx,ty=matrix
        def point(x,y): return sx*x+tx,sy*y+ty
        def box(b):
            a=point(b.x1,b.y1);z=point(b.x2,b.y2)
            return Box(min(a[0],z[0]),min(a[1],z[1]),max(a[0],z[0]),max(a[1],z[1]))
        before=len(all_segs)
        tag = el.tag.replace(NS, "")

        if tag == "text":
            b, s = text_box(el)
            b=box(b)
            texts.append((b, s, el))
            text_orders[id(el)]=order
            if not s.strip():
                errs.append({"code": "E6", "msg": "text rỗng", "at": [b.x1, b.y1]})
            for v in ("x", "y"):
                if "nan" in (el.get(v) or "").lower():
                    errs.append({"code": "E6", "msg": f"toạ độ {v}=NaN", "text": s[:30]})

        elif tag == "rect":
            x, y = fnum(el, "x"), fnum(el, "y")
            w, h = fnum(el, "width"), fnum(el, "height")
            if (el.get('width') or '').endswith('%'): w=W*float(el.get('width')[:-1])/100
            if (el.get('height') or '').endswith('%'): h=H*float(el.get('height')[:-1])/100
            b = box(Box(x, y, x + w, y + h))
            drawn_bounds.append(b)
            fill = (el.get("fill") or "").lower()
            # chỉ coi là "nền che nhãn" khi hộp nhỏ (nền toàn khung không che nhãn nào)
            if fill in ("#fff", "#ffffff", "white") and not el.get("stroke") \
                    and b.area() < 0.20 * max(1.0, W * H):
                white_rects.append((b, order))
            if el.get("stroke") and el.get("stroke").lower() not in ("none",):
                shapes.append(b)

        elif tag in ("ellipse", "circle"):
            cx, cy = fnum(el, "cx"), fnum(el, "cy")
            if tag == "ellipse":
                rx, ry = fnum(el, "rx"), fnum(el, "ry")
            else:
                rx = ry = fnum(el, "r")
            drawn_bounds.append(box(Box(cx-rx,cy-ry,cx+rx,cy+ry)))
            if el.get("stroke") and el.get("stroke").lower() not in ("none",):
                shapes.append(box(Box(cx - rx, cy - ry, cx + rx, cy + ry)))

        elif tag == "line":
            all_segs.append((fnum(el, "x1"), fnum(el, "y1"), fnum(el, "x2"), fnum(el, "y2")))

        elif tag == "polyline" or tag == "polygon":
            pts = [float(v) for v in re.findall(r"-?[\d.]+", el.get("points") or "")]
            for i in range(0, len(pts) - 3, 2):
                all_segs.append((pts[i], pts[i + 1], pts[i + 2], pts[i + 3]))

        elif tag == "path":
            d = el.get("d") or ""
            if any(c not in 'MLHVQCZ' for c in re.findall(r'[A-Za-z]',re.sub(r'[eE][+-]?\d+', '', d))):
                errs.append({'code':'E7','msg':'unsupported path command; use absolute M/L/H/V/Q/C/Z'})
            if "stroke" in el.attrib and el.get("stroke", "").lower() not in ("none",):
                all_segs.extend(parse_path_segments(d))
        for i in range(before,len(all_segs)):
            a,b,c,d=all_segs[i];x1,y1=point(a,b);x2,y2=point(c,d)
            all_segs[i]=(x1,y1,x2,y2);seg_orders.append(order)
            drawn_bounds.append(Box(min(x1,x2),min(y1,y2),max(x1,x2),max(y1,y2)))

    # E1: ra ngoài khung vẽ
    for b, s, _el in texts:
        if not b.inside(canvas, tol=1.0):
            errs.append({"code": "E1", "msg": f"nhãn ra ngoài khung: {s[:40]!r}", "at": [round(b.x1), round(b.y1)]})
    for b in drawn_bounds:
        if not b.inside(canvas, tol=1.0):
            errs.append({"code": "E1", "msg": "hình/đường vượt mép khung",
                          "at": [round(b.x1), round(b.y1)]})

    # E2: hai nhãn chồng nhau
    for i in range(len(texts)):
        bi, si, ei = texts[i]
        for j in range(i + 1, len(texts)):
            bj, sj, ej = texts[j]
            ov = bi.overlap(bj)
            if ov <= 0:
                continue
            ratio = ov / min(bi.area() or 1, bj.area() or 1)
            if ratio > 0.42:
                errs.append({"code": "E2", "msg": f"nhãn đè nhau: {si[:26]!r} × {sj[:26]!r}",
                             "at": [round(bi.x1), round(bi.y1)], "ratio": round(ratio, 2)})

    # E3: dây cắt xuyên nhãn
    for b, s, el in texts:
        if b.area() <= 0:
            continue
        for (sx, sy, ex, ey), edge_order in zip(all_segs,seg_orders):
            text_order=text_orders[id(el)]
            if edge_order < text_order and (has_halo(el) or any(edge_order < rect_order < text_order and b.inside(r,tol=2.0) for r,rect_order in white_rects)):
                continue
            # bỏ qua đoạn chỉ chạm mép hộp
            if seg_hits_box(sx, sy, ex, ey, b, pad=PAD):
                errs.append({"code": "E3", "msg": f"dây cắt qua nhãn: {s[:34]!r}",
                             "at": [round(b.x1), round(b.y1)],
                             "seg": [round(sx), round(sy), round(ex), round(ey)]})
                break

    # E4: chữ tràn khỏi hình bao gần nhất chứa nó
    for b, s, el in texts:
        host = None
        for sh in shapes:
            if b.inside(sh, tol=6.0) and (host is None or sh.area() < host.area()):
                host = sh
        if host is None:
            for sh in shapes:
                # chữ nằm giữa hình nhưng tràn ngang
                cy = (b.y1 + b.y2) / 2
                if sh.y1 <= cy <= sh.y2 and (b.x1 < sh.x1 - 1 or b.x2 > sh.x2 + 1) \
                        and b.x1 < sh.x2 and b.x2 > sh.x1:
                    host = sh
                    errs.append({"code": "E4", "msg": f"chữ tràn ngang khỏi hình: {s[:34]!r}",
                                 "at": [round(b.x1), round(b.y1)]})
                    break

    # E5: id trùng
    for k, n in ids.items():
        if n > 1:
            errs.append({"code": "E5", "msg": f"id trùng {n} lần: {k}"})

    return {
        "file": path.name,
        "canvas": [round(W), round(H)],
        "counts": {"text": len(texts), "shape": len(shapes), "segment": len(all_segs)},
        "errors": errs,
        "warnings": warns,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*", help="file SVG (mặc định: docs/diagrams/vectors/*.svg)")
    ap.add_argument("--root", default=None, help="thư mục project (mặc định: tự dò từ cwd)")
    ap.add_argument("--json", dest="json_out", default=None)
    args = ap.parse_args()

    vec = _resolve_vec(args.root)
    files = [Path(f) for f in args.files] if args.files else sorted(vec.glob("*.svg"))
    if not files:
        print("FAIL: không tìm thấy SVG nào", file=sys.stderr)
        return 1

    results = [audit(f) for f in files]
    total_e = sum(len(r["errors"]) for r in results)
    total_w = sum(len(r["warnings"]) for r in results)

    for r in results:
        e, w = len(r["errors"]), len(r["warnings"])
        mark = "PASS" if e == 0 else "FAIL"
        print(f"\n[{mark}] {r['file']}  canvas={r.get('canvas')}  "
              f"text={r.get('counts', {}).get('text')} seg={r.get('counts', {}).get('segment')}")
        for it in r["errors"][:12]:
            print(f"   E {it['code']}: {it['msg']} @ {it.get('at')}")
        if e > 12:
            print(f"   ... còn {e - 12} lỗi")
        for it in r["warnings"][:4]:
            print(f"   W {it['code']}: {it['msg']}")

    print(f"\n=== TỔNG: {len(results)} sơ đồ · {total_e} lỗi · {total_w} cảnh báo ===")
    if args.json_out:
        Path(args.json_out).write_text(
            json.dumps({"results": results, "errors": total_e, "warnings": total_w},
                       indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"JSON: {args.json_out}")

    if total_e:
        return 1
    return 2 if total_w else 0


if __name__ == "__main__":
    sys.exit(main())
