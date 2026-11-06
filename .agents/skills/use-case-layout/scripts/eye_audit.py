#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""eye_audit.py — "soi nhu mat nguoi" cho so do VE TAY (Use Case / flow / state / sequence).

TRIET LY (doc truoc khi dung — day la ly do ton tai cua script):
  Script nay KHONG phan quyet PASS/FAIL va KHONG duoc dung lam cong nghiem thu.
  No lam dung 2 viec:
    (1) CHI RA UNG VIEN loi hinh hoc: line xuyen vao long ellipse, line cat chu,
        nhan tran ellipse, node chong nhau, cot lech truc, khoang cach khong deu,
        duong di vong (far loop), neo lo lung, actor rai vao giua...
    (2) CAT PHONG TO (zoom crop) tung vung nghi van thanh anh rieng + xuat overlay
        co LUOI 10x10, de MAT NGUOI nhin o do phan giai cao.
  Cong quyet dinh bo cuc VAN LA: agent mo crops/ + overlay.png, tu tra loi
  "de? deu? de nhin?" va dien bang chung vao eye-audit.md.

  Vi sao can script: khi chen A4 ~15cm, 1 doan line xuyen qua chu chi ~1-2px tren anh
  -> mat THUONG bo sot. Script tim ung vien + zoom 4x => mat chi phai phan xuat
  "that hay bao oan", nhanh va khong bo sot.

CACH DUNG:
  python eye_audit.py <file.svg|file.pdf> [more...] [--out DIR] [--scale 4]
                      [--overlay] [--dump] [--strict] [--quiet]

  --out DIR     thu muc xuat (mac dinh: <thu_muc_file>/<ten>-audit/)
  --scale N     he so phong to crop (mac dinh 4)
  --overlay     xuat them overlay.png (luoi 10x10 + truc giua do) de soi lech/can chinh
  --dump        in mo hinh DA DOC DUOC (node/nhan/duong noi) — BAT BUOC chay khi lan dau
                dung tren 1 nguon moi, de biet parser doc dung truoc khi tin ket qua
  --strict      exit 1 neu co ung vien MUC DO CAO (chi de chan CI; KHONG phai nghiem thu)
  --quiet       chi in bang tom tat

XUAT RA:
  <out>/eye-audit.md            bang ung vien + cho trong BAT BUOC dien "bang chung mat thay"
  <out>/crops/F##-<MA>.png      anh phong to tung vung nghi van
  <out>/overlay.png             (neu --overlay) anh co luoi

MA FINDING:
  L-INSIDE    duong noi xuyen vao long 1 ellipse/khung node
  L-TEXT      duong noi cat ngang mat chu (chua duoc nen trang che)
  L-ACTORNAME duong noi cat ngang ten actor (luat: ten actor khong bi duong xuyen)
  T-OVERFLOW  nhan tran ra ngoai ellipse chua no        T-TIGHT   nhan sat vien (<95%)
  T-COLLIDE   hai KHOI nhan chong len nhau              N-OVERLAP hai node chong nhau
  N-UNALIGN   node cung cot lech truc (ung vien thiet ke, LOW)  G-GAP  buoc cot khong deu (thiet ke, LOW)
  C-FARLOOP   duong dai/vong nhieu lan khoang cach thang (dau hieu VONG XA)
  C-COINCIDE  hai duong trung khit                      C-DANGLE  neo lo lung
  C-MASKED    nen trang cua nhan CHE dau/canh duong noi (mat mui tam giac/mui ten)
  C-FAN       >=5 duong xuat phat gan dung mot diem nho — 'quat ga' (thiet ke, LOW)
  A-BAND      actor rai vao giua (khong theo dai trai/phai)   A-SKEW  actor cung dai lech cot (thiet ke, LOW)
  U-OCCUPY    bo cuc don cuc / rong                     S-FONT    nhieu font tron trong 1 nhan
  S-LADDER    >=8 node trong mot dai doc rong ~80px — 'thang may' (thiet ke, LOW)
  S-TINY      co chu qua nho khi in A4                  S-RATIO   ty le khung det/dai
  S-BOUNDARY  node tran ra ngoai khung system boundary  D-DUP     hai nhan y nguyen van
  I-MASKED    (thong tin) duong bi nen trang che — dung thiet ke, KHONG sua
"""

from __future__ import annotations

import argparse
import math
import os
import re
import statistics
import sys
from dataclasses import dataclass, field

try:
    import pymupdf  # PyMuPDF >= 1.24
except ImportError:  # pragma: no cover
    try:
        import fitz as pymupdf  # type: ignore
    except ImportError:
        print("[eye_audit] Thieu PyMuPDF. Cai: pip install pymupdf", file=sys.stderr)
        sys.exit(2)


# --------------------------------------------------------------------------------------
# NGUONG — ghi ro de bien luan duoc. Day la "kinh nghiem do luong", khong phai chan ly.
# --------------------------------------------------------------------------------------
TH = {
    "far_ratio": 2.2,          # path_len / euclid_len > nguong => nghi vong xa
    "coincide_tol": 3.0,       # px: 2 duong coi la trung khit trong sai so nay
    "coincide_frac": 0.6,      # ty le do dai trung nhau
    "unalign_std": 4.0,        # px: do lech chuan tam cot cho phep
    "gap_mult_tol": 0.22,      # buoc cot phai la boi so nguyen cua buoc nho nhat (sai so)
    "ellipse_inset": -2.0,     # co vao ellipse khi kiem "xuyen vao long"
    "ink_top": 0.17,           # inset tren cua line-box de ~bbox MUC (khong tinh ascender)
    "ink_bot": 0.19,           # inset duoi tuong tu
    "mask_cover": 0.85,        # rect trang phu >= 85% chieu ngang nhan => nhan duoc che
    "tight_ratio": 0.95,       # >= 95% ellipse => SAT VIA, canh bao (mat phan xu)
    "overflow_ratio": 1.05,    # > 105% => coi la TRAN that (theo bbox MUC chu)
    "tiny_font": 9.0,          # pt
    "ratio_max": 3.2,
    "ratio_min": 0.30,
    "occ_min": 0.30,
    "occ_worst": 0.45,
    "collide_frac": 0.18,      # dien tich chong / dien tich nho hon > nguong => coi la chong that
}

SEV = {
    "L-INSIDE": "HIGH", "L-TEXT": "HIGH", "L-ACTORNAME": "HIGH",
    "T-OVERFLOW": "HIGH", "N-OVERLAP": "HIGH", "T-COLLIDE": "HIGH", "C-FARLOOP": "HIGH",
    "C-COINCIDE": "MEDIUM", "C-DANGLE": "MEDIUM", "N-UNALIGN": "LOW", "G-GAP": "LOW",
    "C-MASKED": "MEDIUM",
    "A-BAND": "MEDIUM", "A-SKEW": "LOW", "S-BOUNDARY": "MEDIUM",
    "S-TINY": "MEDIUM", "S-RATIO": "MEDIUM", "T-TIGHT": "MEDIUM",
    "U-OCCUPY": "LOW", "S-FONT": "LOW", "D-DUP": "LOW", "S-LADDER": "LOW", "C-FAN": "LOW", "I-MASKED": "INFO",
}

REL_LABELS = {"«include»", "«extend»", "«include>>", "«extend>>", "include", "extend"}


# --------------------------------------------------------------------------------------
# Mo hinh
# --------------------------------------------------------------------------------------
@dataclass
class Ellipse:
    cx: float
    cy: float
    rx: float
    ry: float
    filled: bool = True

    @property
    def bbox(self):
        return (self.cx - self.rx, self.cy - self.ry, self.cx + self.rx, self.cy + self.ry)

    def contains_point(self, x, y, inflate=0.0):
        rx = max(0.1, self.rx + inflate)
        ry = max(0.1, self.ry + inflate)
        return ((x - self.cx) / rx) ** 2 + ((y - self.cy) / ry) ** 2 <= 1.0

    def radial_of(self, x, y):
        """Gia tri phuong trinh ellipse: <1 la trong long, =1 la tren vien."""
        return ((x - self.cx) / self.rx) ** 2 + ((y - self.cy) / self.ry) ** 2

    def box_overlaps(self, other, pad=0.0):
        a, b = self.bbox, other.bbox
        return not (a[2] + pad <= b[0] or b[2] + pad <= a[0] or a[3] + pad <= b[1] or b[3] + pad <= a[1])


@dataclass
class Box:
    """Node dang HINH CHU NHAT / thoi / bo goc (flowchart, activity, state, lifeline header).

    Cung giao dien voi Ellipse (bbox / contains_point / radial_of) de dung chung moi phep kiem.
    """
    x0: float
    y0: float
    x1: float
    y1: float

    @property
    def cx(self):
        return (self.x0 + self.x1) / 2

    @property
    def cy(self):
        return (self.y0 + self.y1) / 2

    @property
    def rx(self):
        return (self.x1 - self.x0) / 2

    @property
    def ry(self):
        return (self.y1 - self.y0) / 2

    @property
    def bbox(self):
        return (self.x0, self.y0, self.x1, self.y1)

    def contains_point(self, x, y, inflate=0.0):
        return (self.x0 - inflate <= x <= self.x1 + inflate
                and self.y0 - inflate <= y <= self.y1 + inflate)

    def radial_of(self, x, y):
        hw = max(0.1, self.rx)
        hh = max(0.1, self.ry)
        return max(abs(x - self.cx) / hw, abs(y - self.cy) / hh)

    def box_overlaps(self, other, pad=0.0):
        a, b = self.bbox, other.bbox
        return not (a[2] + pad <= b[0] or b[2] + pad <= a[0] or a[3] + pad <= b[1] or b[3] + pad <= a[1])


@dataclass
class Rect:
    x0: float
    y0: float
    x1: float
    y1: float
    kind: str = "labelbg"  # 'bg' | 'labelbg' | 'boundary'

    @property
    def bbox(self):
        return (self.x0, self.y0, self.x1, self.y1)


@dataclass
class TextLine:
    text: str
    x0: float
    y0: float
    x1: float
    y1: float
    size: float
    fonts: set = field(default_factory=set)

    @property
    def cx(self):
        return (self.x0 + self.x1) / 2

    @property
    def cy(self):
        return (self.y0 + self.y1) / 2

    @property
    def bbox(self):
        return (self.x0, self.y0, self.x1, self.y1)

    def ink_bbox(self):
        """Bbox 'muc chu' — bo phan ascender/descender trong line-box de khong bao tran oan."""
        return (self.x0, self.y0 + TH["ink_top"] * self.size,
                self.x1, self.y1 - TH["ink_bot"] * self.size)


@dataclass
class Label:
    """Mot nhan = 1..n TextLine thuoc cung 1 nhan (vd ten use case 2 dong)."""
    lines: list

    @property
    def text(self):
        return " ".join(l.text.strip() for l in self.lines if l.text.strip()).strip()

    @property
    def size(self):
        return max(l.size for l in self.lines)

    @property
    def fonts(self):
        out = set()
        for l in self.lines:
            out |= l.fonts
        return out

    @property
    def cx(self):
        return (self.bbox[0] + self.bbox[2]) / 2

    @property
    def cy(self):
        return (self.bbox[1] + self.bbox[3]) / 2

    @property
    def bbox(self):
        return (min(l.x0 for l in self.lines), min(l.y0 for l in self.lines),
                max(l.x1 for l in self.lines), max(l.y1 for l in self.lines))

    def ink_bbox(self):
        bbs = [l.ink_bbox() for l in self.lines]
        return (min(b[0] for b in bbs), min(b[1] for b in bbs),
                max(b[2] for b in bbs), max(b[3] for b in bbs))


@dataclass
class Conn:
    pts: list
    dashed: bool
    width: float

    @property
    def a(self):
        return self.pts[0]

    @property
    def b(self):
        return self.pts[-1]

    def length(self):
        return sum(math.dist(self.pts[i], self.pts[i + 1]) for i in range(len(self.pts) - 1))

    def euclid(self):
        return math.dist(self.a, self.b)

    def bbox(self):
        xs = [p[0] for p in self.pts]
        ys = [p[1] for p in self.pts]
        return (min(xs), min(ys), max(xs), max(ys))

    def sample(self, step=3.0):
        out = []
        for i in range(len(self.pts) - 1):
            (x0, y0), (x1, y1) = self.pts[i], self.pts[i + 1]
            d = math.dist((x0, y0), (x1, y1))
            n = max(1, int(d / step))
            for k in range(n + 1):
                t = k / n
                out.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
        return out


@dataclass
class Diagram:
    path: str
    width: float
    height: float
    ellipses: list = field(default_factory=list)
    boxes: list = field(default_factory=list)
    rects: list = field(default_factory=list)
    labels: list = field(default_factory=list)
    conns: list = field(default_factory=list)
    glyph_boxes: list = field(default_factory=list)

    @property
    def nodes(self):
        """Node = ellipse to (use case) HOAC hop chu nhat/thoi (flowchart/activity/state)."""
        return [e for e in self.ellipses if not (e.rx < 26 and e.ry < 26)] + list(self.boxes)

    @property
    def boundary(self):
        for r in self.rects:
            if r.kind == "boundary":
                return r
        return None

    @property
    def label_bgs(self):
        return [r for r in self.rects if r.kind == "labelbg"]

    def label_of(self, e: Ellipse):
        inside = [lb for lb in self.labels if e.contains_point(lb.cx, lb.cy, inflate=1.0)]
        if inside:
            return " ".join(lb.text for lb in sorted(inside, key=lambda l: l.bbox[1]))
        return f"ellipse@({e.cx:.0f},{e.cy:.0f})"

    def actor_labels(self):
        out = []
        for g in self.glyph_boxes:
            cand = [lb for lb in self.labels
                    if g[0] - 16 <= lb.cx <= g[2] + 16 and g[3] - 8 <= lb.cy <= g[3] + 46]
            out.extend(cand)
        return out


# --------------------------------------------------------------------------------------
# Doc file -> mo hinh
# --------------------------------------------------------------------------------------
def _dash_on(dashes) -> bool:
    if dashes is None:
        return False
    m = re.search(r"\[([^\]]*)\]", str(dashes))
    return bool(m.group(1).strip()) if m else False


def _polylines(d: dict):
    polys, cur = [], []

    def push():
        nonlocal cur
        if len(cur) >= 2:
            polys.append(cur)
        cur = []

    for it in d["items"]:
        k = it[0]
        if k == "l":
            p0, p1 = it[1], it[2]
            if not cur:
                cur.append((p0.x, p0.y))
            cur.append((p1.x, p1.y))
        elif k == "c":
            p0, p1, p2, p3 = it[1], it[2], it[3], it[4]
            if not cur:
                cur.append((p0.x, p0.y))
            for s in (0.2, 0.4, 0.6, 0.8, 1.0):
                mt = 1 - s
                cur.append((
                    (mt ** 3) * p0.x + 3 * (mt ** 2) * s * p1.x + 3 * mt * (s ** 2) * p2.x + (s ** 3) * p3.x,
                    (mt ** 3) * p0.y + 3 * (mt ** 2) * s * p1.y + 3 * mt * (s ** 2) * p2.y + (s ** 3) * p3.y,
                ))
        elif k == "re":
            push()
            r = it[1]
            polys.append([(r.x0, r.y0), (r.x1, r.y0), (r.x1, r.y1), (r.x0, r.y1), (r.x0, r.y0)])
        elif k == "qu":
            push()
            q = it[1]
            polys.append([(q.ul.x, q.ul.y), (q.ur.x, q.ur.y), (q.lr.x, q.lr.y), (q.ll.x, q.ll.y), (q.ul.x, q.ul.y)])
    push()
    return polys


def read_diagram(path: str) -> Diagram:
    doc = pymupdf.open(path)
    page = doc[0]
    W, H = page.rect.width, page.rect.height
    dia = Diagram(path=path, width=W, height=H)
    page_area = W * H

    ellipses, boxes, rects, conns = [], [], [], []
    for d in page.get_drawings():
        r = d["rect"]
        is_fill = "f" in d["type"]
        is_stroke = "s" in d["type"]
        dashed = _dash_on(d.get("dashes"))
        width = round(float(d.get("width") or 0.0), 2)
        items = d["items"]
        kinds = [i[0] for i in items]
        curve_cnt = kinds.count("c")
        polys = _polylines(d)

        # 1) Ellipse / tron: 4 cung bezier dong kin
        if curve_cnt == 4 and len(items) == 4 and kinds == ["c"] * 4:
            ellipses.append(Ellipse(cx=(r.x0 + r.x1) / 2, cy=(r.y0 + r.y1) / 2,
                                    rx=(r.x1 - r.x0) / 2, ry=(r.y1 - r.y0) / 2, filled=is_fill))
            continue

        # 2) Nen trang / nen nhan (fill + rect)
        if is_fill and not is_stroke and kinds and all(k == "re" for k in kinds):
            area = (r.x1 - r.x0) * (r.y1 - r.y0)
            rects.append(Rect(r.x0, r.y0, r.x1, r.y1, kind="bg" if area >= 0.9 * page_area else "labelbg"))
            continue

        # 3) Khung boundary: do lon + co stroke
        big = (r.x1 - r.x0) > 0.30 * W and (r.y1 - r.y0) > 0.30 * H
        if is_stroke and big and len(items) >= 4 and ("re" in kinds or len(polys) == 1):
            rects.append(Rect(r.x0, r.y0, r.x1, r.y1, kind="boundary"))
            continue

        # 4) Node dang HOP (rect/thoi/bo goc ve bang path): polyline KIN + nho + co stroke.
        #    CHI tieu thu khi that su la hop; neu khong thi de roi xuong buoc 5 (duong noi).
        area_frac = ((r.x1 - r.x0) * (r.y1 - r.y0)) / page_area
        looks_boxish = (is_stroke and not dashed and area_frac < 0.10
                        and (r.x1 - r.x0) > 14 and (r.y1 - r.y0) > 14)
        if looks_boxish:
            is_closed = any(len(pl) >= 5 and math.dist(pl[0], pl[-1]) < 2.5 for pl in polys)
            if is_closed:
                boxes.append(Box(r.x0, r.y0, r.x1, r.y1))
                continue

        # 5) Duong noi
        for pl in polys:
            if sum(math.dist(pl[i], pl[i + 1]) for i in range(len(pl) - 1)) >= 8.0:
                conns.append(Conn(pts=pl, dashed=dashed, width=width))

    # ---- Chu ----
    raw_lines = []
    for b in page.get_text("dict")["blocks"]:
        if b.get("type") != 0:
            continue
        for ln in b.get("lines", []):
            spans = ln.get("spans", [])
            if not spans:
                continue
            text = "".join(s["text"] for s in spans).strip()
            if not text:
                continue
            raw_lines.append([TextLine(
                text=text,
                x0=min(s["bbox"][0] for s in spans), y0=min(s["bbox"][1] for s in spans),
                x1=max(s["bbox"][2] for s in spans), y1=max(s["bbox"][3] for s in spans),
                size=max(float(s.get("size") or 0) for s in spans),
                fonts={str(s.get("font") or "") for s in spans},
            )])

    # ---- Gom cac dong cua CUNG 1 nhan (vd ten use case 2 dong) ----
    dia.labels = _merge_labels(raw_lines)

    # ---- Glyph actor = TRON DAU + it nhat 2 net than dinh vao (loai tru 'cham start/end') ----
    small = [e for e in ellipses if e.rx < 26 and e.ry < 26]
    glyph_boxes = []
    glyph_conn_idx = set()
    for c in small:
        pad = max(30.0, 2.4 * c.rx)
        box0 = (c.cx - pad, c.cy - pad, c.cx + pad, c.cy + 1.7 * pad)
        # Net than actor: NGAN, DAY (>=1.6), dinh vao vung dau. Actor can >=3 net (than + 2 chan).
        attached = [idx for idx, cn in enumerate(conns)
                    if (cn.width or 0) >= 1.6 and cn.length() <= 70
                    and any(box0[0] - 4 <= p[0] <= box0[2] + 4 and box0[1] - 4 <= p[1] <= box0[3] + 4
                            for p in cn.pts)]
        if len(attached) < 3:      # khong du net -> khong phai actor (vd cham start/end)
            continue
        box = box0
        for idx in attached:
            b2 = conns[idx].bbox()
            box = (min(box[0], b2[0]), min(box[1], b2[1]), max(box[2], b2[2]), max(box[3], b2[3]))
        glyph_conn_idx |= set(attached)
        glyph_boxes.append(box)

    # ---- Loai arrowhead + than actor khoi danh sach duong noi ----
    def _in_glyph(pt, pad=1.0):
        return any(g[0] - pad <= pt[0] <= g[2] + pad and g[1] - pad <= pt[1] <= g[3] + pad for g in glyph_boxes)

    keep = []
    n = len(conns)
    for i, c in enumerate(conns):
        if i in glyph_conn_idx:
            continue
        L = c.length()
        if L <= 26 and not c.dashed and (c.width or 0) >= 1.4:
            if _in_glyph(c.a, 2) or _in_glyph(c.b, 2):
                continue
            if any(j != i and (math.dist(c.a, conns[j].a) < 22 or math.dist(c.a, conns[j].b) < 22
                               or math.dist(c.b, conns[j].a) < 22) for j in range(n)):
                continue
        keep.append(c)

    dia.ellipses = ellipses
    dia.boxes = boxes
    dia.rects = rects
    dia.conns = keep
    dia.glyph_boxes = glyph_boxes
    return dia


def _merge_labels(raw_groups):
    """Gom cac dong chu thanh 1 nhan neu cung tam x va sat nhau theo truc y.

    raw_groups: list[list[TextLine]] — moi phan tu la 1 dong (Label 1 dong).
    Tra ve list[Label]; Label 2 dong = nhan bi wrap (vd ten use case dai).
    """
    out = []  # list[list[TextLine]]
    for grp in sorted(raw_groups, key=lambda g: (g[0].cy, g[0].cx)):
        line = grp[0]
        placed = False
        for cluster in out:
            last = cluster[-1]
            if abs(line.cx - last.cx) <= max(9.0, 0.42 * max(line.size, last.size)) \
               and abs(line.cy - last.cy) <= 1.75 * max(line.size, last.size) \
               and abs(line.size - last.size) <= 2.5 and line.cy > last.cy:
                cluster.append(line)
                placed = True
                break
        if not placed:
            out.append([line])
    return [Label(cluster) for cluster in out]


# --------------------------------------------------------------------------------------
# Helper hinh hoc
# --------------------------------------------------------------------------------------
def _union(*bbs):
    bbs = [b for b in bbs if b]
    if not bbs:
        return (0, 0, 0, 0)
    return (min(b[0] for b in bbs), min(b[1] for b in bbs),
            max(b[2] for b in bbs), max(b[3] for b in bbs))


def _inflate(bb, pad):
    return (bb[0] - pad, bb[1] - pad, bb[2] + pad, bb[3] + pad)


def _overlap(a, b):
    ox = min(a[2], b[2]) - max(a[0], b[0])
    oy = min(a[3], b[3]) - max(a[1], b[1])
    return (ox, oy) if ox > 0 and oy > 0 else None


def _in_box(x, y, bb, pad=0.0):
    return bb[0] - pad <= x <= bb[2] + pad and bb[1] - pad <= y <= bb[3] + pad


def _inside(inner, outer, pad=0.0):
    return (inner[0] >= outer[0] - pad and inner[1] >= outer[1] - pad
            and inner[2] <= outer[2] + pad and inner[3] <= outer[3] + pad)


def _short(s, n=44):
    s = re.sub(r"\s+", " ", str(s)).strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def _cluster_by_key(objs, key, tol=10.0):
    out = []
    for o in sorted(objs, key=key):
        if out and abs(key(o) - statistics.fmean(key(x) for x in out[-1])) <= tol:
            out[-1].append(o)
        else:
            out.append([o])
    return out


@dataclass
class Finding:
    code: str
    msg: str
    bbox: tuple
    fix: str = ""
    sev: str = ""

    def __post_init__(self):
        if not self.sev:
            self.sev = SEV.get(self.code, "LOW")


# --------------------------------------------------------------------------------------
# Kiem tra
# --------------------------------------------------------------------------------------
def check(dia: Diagram):
    F: list[Finding] = []
    nodes = dia.nodes
    boundary = dia.boundary
    actor_names = dia.actor_labels()

    # =============== L-INSIDE ===============
    for ci, c in enumerate(dia.conns):
        for e in nodes:
            pts = c.sample(3.0)
            deep = [p for p in pts
                    if e.contains_point(p[0], p[1], inflate=TH["ellipse_inset"])
                    and not c.a == p and not c.b == p]
            # loai diem nam gan vien (diem neo hop le)
            deep = [p for p in deep if not (e.contains_point(p[0], p[1], inflate=4.0)
                                            and not e.contains_point(p[0], p[1], inflate=TH["ellipse_inset"]))]
            if len(deep) >= 3:
                bb = _union((min(p[0] for p in deep), min(p[1] for p in deep),
                             max(p[0] for p in deep), max(p[1] for p in deep)))
                F.append(Finding(
                    "L-INSIDE",
                    f"Duong #{ci} ({'net dut' if c.dashed else 'lien'}) xuyen QUA LONG ellipse '{_short(dia.label_of(e))}'",
                    _inflate(bb, 14),
                    "DI CHUYEN node (doi row/lane) cho 2 dau gan nhau; KHONG be ngoat hay keo vong.",
                ))

    # =============== L-TEXT + I-MASKED ===============
    for ci, c in enumerate(dia.conns):
        pts = c.sample(3.0)
        for lb in dia.labels:
            t = lb.bbox
            tb = lb.ink_bbox()
            hit = [p for p in pts if _in_box(p[0], p[1], tb, 0.5)]
            if len(hit) < 2:
                continue
            covered = False
            for r in dia.label_bgs:
                ov = _overlap(r.bbox, t)
                if ov and (t[2] - t[0]) > 0 and ov[0] / (t[2] - t[0]) >= TH["mask_cover"]:
                    covered = True
                    break
            if covered:
                F.append(Finding("I-MASKED",
                                 f"Nhan '{_short(lb.text)}' co nen trang che duong — dung thiet ke.",
                                 _inflate(t, 10), "Khong can sua."))
                continue
            F.append(Finding(
                "L-TEXT",
                f"Duong #{ci} cat ngang chu '{_short(lb.text)}' (khong co nen che)",
                _inflate(_union(tb, (min(p[0] for p in hit), min(p[1] for p in hit),
                                     max(p[0] for p in hit), max(p[1] for p in hit))), 12),
                "Doi vi tri node/neo cho duong tranh chu, hoac them nen trang cho nhan.",
            ))

    # =============== L-ACTORNAME ===============
    # Luu y: ten actor thuong co NEN TRANG che duong. Neu moi diem cat deu nam trong
    # nen trang do thi day KHONG con la "xuyen qua chu" nua, chi la "sat mep tren nhan"
    # -> ha xuong MEDIUM va noi ro, de khong bao oan.
    for ci, c in enumerate(dia.conns):
        pts = c.sample(3.0)
        for lb in actor_names:
            hit = [p for p in pts if _in_box(p[0], p[1], lb.ink_bbox(), 0.5)]
            if len(hit) < 2:
                continue
            masks = [r for r in dia.label_bgs
                     if _overlap(r.bbox, lb.bbox)
                     and (lb.bbox[2] - lb.bbox[0]) > 0
                     and _overlap(r.bbox, lb.bbox)[0] / (lb.bbox[2] - lb.bbox[0]) >= TH["mask_cover"]]
            visible = [p for p in hit if not any(_in_box(p[0], p[1], r.bbox) for r in masks)]
            if len(visible) >= 2:
                F.append(Finding(
                    "L-ACTORNAME",
                    f"Duong #{ci} XUYEN QUA ten actor '{_short(lb.text)}' (khong bi nen che) — "
                    f"luat: ten actor khong bi duong noi xuyen",
                    _inflate(lb.bbox, 12),
                    "Doi diem neo (neo vao vai/dinh dau) hoac DAY TEN ACTOR ra khoi huong dai duong "
                    "(vd dat ten ben trai hinh nguoi, hoac qua 1 'truc' phan phoi).",
                ))
            else:
                F.append(Finding(
                    "L-ACTORNAME",
                    f"Duong #{ci} SAT/CAT qua mep tren ten actor '{_short(lb.text)}' — "
                    f"phan giao nam trong nen trang cua nhan nen bi che mot phan, nhung MAT thay ro vet cat",
                    _inflate(lb.bbox, 14),
                    "Doi diem neo hoac day ten actor ra khoi huong dai duong.",
                    "MEDIUM",
                ))

    # =============== T-OVERFLOW + T-TIGHT ===============
    for e in nodes:
        owners = [lb for lb in dia.labels if e.contains_point(lb.cx, lb.cy, inflate=1.0)]
        if not owners:
            continue
        ub = _union(*[lb.ink_bbox() for lb in owners])
        pts = [(ub[0], ub[1]), (ub[2], ub[1]), (ub[0], ub[3]), (ub[2], ub[3]),
               ((ub[0] + ub[2]) / 2, ub[1]), ((ub[0] + ub[2]) / 2, ub[3]),
               (ub[0], (ub[1] + ub[3]) / 2), (ub[2], (ub[1] + ub[3]) / 2)]
        vals = [e.radial_of(x, y) for x, y in pts]
        mx = max(vals)
        txt = _short(" ".join(lb.text for lb in owners))
        if mx > TH["overflow_ratio"]:
            F.append(Finding(
                "T-OVERFLOW",
                f"Nhan '{txt}' TRAN ra ngoai ellipse (do tran {mx*100:.0f}% > {TH['overflow_ratio']*100:.0f}%; "
                f"rx={e.rx:.0f}, ry={e.ry:.0f})",
                _inflate(ub, 14),
                "Rut gon nhan <= 25 ky tu, TANG ry ellipse, hoac tach dong deu hon.",
            ))
        elif mx >= TH["tight_ratio"]:
            F.append(Finding(
                "T-TIGHT",
                f"Nhan '{txt}' SAT VIA ellipse ({mx*100:.0f}% — vung {TH['tight_ratio']*100:.0f}–"
                f"{TH['overflow_ratio']*100:.0f}%). MAT phan xu: sat nhung chua tran thi chi nen tang ry ~15% cho an toan.",
                _inflate(ub, 12),
                "Tang ry ellipse ~15% (an toan khi doi font/thiet bi khac) hoac rut gon nhan.",
            ))

    # =============== T-COLLIDE (theo NHAN, khong theo dong) ===============
    lbs = [lb for lb in dia.labels if len(lb.text.strip()) >= 2]
    for i in range(len(lbs)):
        for j in range(i + 1, len(lbs)):
            a, b = lbs[i], lbs[j]
            ov = _overlap(a.bbox, b.bbox)
            if not ov:
                continue
            area = ov[0] * ov[1]
            amin = min((a.bbox[2] - a.bbox[0]) * (a.bbox[3] - a.bbox[1]),
                       (b.bbox[2] - b.bbox[0]) * (b.bbox[3] - b.bbox[1]))
            if amin > 0 and area / amin >= TH["collide_frac"]:
                F.append(Finding(
                    "T-COLLIDE",
                    f"Chu '{_short(a.text)}' va '{_short(b.text)}' chong nhau ({area/amin*100:.0f}% dien tich nho hon)",
                    _inflate(_union(a.bbox, b.bbox), 12),
                    "Day 2 nhan ra xa; kiem lai toa do dat nhan.",
                ))

    # =============== N-OVERLAP ===============
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if nodes[i].box_overlaps(nodes[j], pad=-1.0):
                F.append(Finding(
                    "N-OVERLAP",
                    f"Hai ellipse chong nhau: '{_short(dia.label_of(nodes[i]))}' vs '{_short(dia.label_of(nodes[j]))}'",
                    _inflate(_union(nodes[i].bbox, nodes[j].bbox), 12),
                    "Tang khoang cach hang/cot.",
                ))

    # =============== N-UNALIGN + G-GAP ===============
    for col in _cluster_by_key(nodes, key=lambda e: e.cx, tol=10.0):
        if len(col) < 3:
            continue
        spread = statistics.pstdev([e.cx for e in col])
        if spread > TH["unalign_std"]:
            F.append(Finding(
                "N-UNALIGN",
                f"Mot cot {len(col)} ellipse LECH TRUC: do lech chuan tam cot = {spread:.1f}px (nguong {TH['unalign_std']})",
                _inflate(_union(*[e.bbox for e in col]), 16),
                "Can lai truc NEU LECH VO Y trong cung cum; lech co chu dich giua cac cum (stagger, SKILL §3.2b) thi ghi BAO-OAN voi ly do nhom.",
            ))
        ordered = sorted(col, key=lambda e: e.cy)
        gaps = [ordered[k + 1].cy - ordered[k].cy for k in range(len(ordered) - 1)]
        if len(gaps) >= 2:
            unit = min(g for g in gaps if g > 0.5) if any(g > 0.5 for g in gaps) else 0
            if unit > 0:
                bad = []
                for g in gaps:
                    k = round(g / unit)
                    if k < 1 or abs(g / unit - k) > TH["gap_mult_tol"] * max(1, k):
                        bad.append(round(g))
                if bad:
                    F.append(Finding(
                        "G-GAP",
                        f"Buoc cot khong deu: {[round(g) for g in gaps]} (buoc nho nhat {unit:.0f}px, "
                        f"{bad} khong la boi so) — phan xu: khoang rong GIUA CAC CUM co chu dich thi bao oan, "
                        f"lech vo y trong cung cum thi sua",
                        _inflate(_union(*[e.bbox for e in col]), 16),
                        f"Nhip TRONG cum = {unit:.0f}px cho cac node cung cum (giua cac cum duoc rong hon ~2x — SKILL §3.2b); "
                        f"kiem tra chu dich nhom truoc khi sua.",
                    ))

    # =============== S-LADDER (thang may — SKILL §3.2b rule 3) ===============
    # >= 8 node tam nam trong mot dai doc rong ~80px => mot cot don dieu.
    # Luu y: ladder HOAN HAO se PASS ca N-UNALIGN lan G-GAP (no dung la "deu"),
    # nen can phat rieng. LOW — ung vien thiet ke, mat phan xu.
    if len(nodes) >= 8:
        band = 80.0
        best_grp = []
        for a in nodes:
            grp = [b for b in nodes if abs(b.cx - a.cx) <= band / 2]
            if len(grp) > len(best_grp):
                best_grp = grp
        if len(best_grp) >= 8:
            F.append(Finding(
                "S-LADDER",
                f"{len(best_grp)}/{len(nodes)} node nam trong mot dai doc rong ~{band:.0f}px — "
                f"dau hieu 'THANG MAY' (mot cot don dieu, SKILL §3.2b)",
                _inflate(_union(*[e.bbox for e in best_grp]), 16),
                "Tach thanh 2-3 cot theo nhom chuc nang va dan cum theo luong; "
                "giua cac cum rong hon nhip trong cum.",
            ))

    # =============== C-FARLOOP ===============
    for ci, c in enumerate(dia.conns):
        L, E = c.length(), c.euclid()
        if E > 1 and L > 120 and L / E > TH["far_ratio"]:
            F.append(Finding(
                "C-FARLOOP",
                f"Duong #{ci} dai {L:.0f}px / khoang cach thang {E:.0f}px = {L/E:.1f}x — dau hieu VONG XA",
                _inflate(c.bbox(), 14),
                "DI CHUYEN NODE cho gan nhau. CAM keo duong vong qua mep canvas.",
            ))

    # =============== C-MASKED: nen trang cua nhan CHE dau/canh cua mot duong noi ===============
    # Phan biet voi I-MASKED (duong di XUYEN QUA nhan — dung thiet ke, duoc che):
    #   o day la duong CO DINH (vertex) NAM TRONG nen trang -> bi cat cut, mat mui tam giac,
    #   hoac doan cuoi bien mat. Ca that da gap: doi nhan actor sang trai roi de nguyen nen trang
    #   -> nen trang che mat mui tam giac generalization (chi con 1 manh).
    for ci, c in enumerate(dia.conns):
        for r in dia.label_bgs:
            inside = [p for p in c.pts if _in_box(p[0], p[1], r.bbox, -1.0)]
            outside = [p for p in c.pts if not _in_box(p[0], p[1], r.bbox, 1.0)]
            if inside and outside:
                owner = ""
                for lb in dia.labels:
                    ov = _overlap(r.bbox, lb.bbox)
                    if ov and ov[0] > 0.6 * max(1.0, (lb.bbox[2] - lb.bbox[0])):
                        owner = _short(lb.text)
                        break
                F.append(Finding(
                    "C-MASKED",
                    f"Nen trang cua nhan '{owner or '?'}' dang CHE mot phan duong #{ci} "
                    f"({len(inside)} diem neo nam trong nen) — mat mui tam giac/dau doan",
                    _inflate(r.bbox, 10),
                    "BO nen trang cua nhan (nhan nen dat o cho khong co duong di qua), "
                    "hoac doi vi tri nhan/duong. Kiem lai bang cach zoom dung vung nay.",
                ))

    # =============== C-COINCIDE ===============
    for i in range(len(dia.conns)):
        for j in range(i + 1, len(dia.conns)):
            a, b = dia.conns[i], dia.conns[j]
            fr = _coincide(a, b)
            if fr >= TH["coincide_frac"]:
                F.append(Finding(
                    "C-COINCIDE",
                    f"Duong #{i} va #{j} TRUNG KHIT ({fr*100:.0f}%) — khong phan biet duoc canh nao toi dau",
                    _inflate(_union(a.bbox(), b.bbox()), 12),
                    "Tach neo hoac doi vi tri node.",
                ))

    # =============== C-FAN (quat ga — SKILL §3.2b rule 4, v2) ===============
    # >= 4 duong co mot dau hut gan dung mot diem nho (R_HUB) VA CAC DUONG KE NHAU
    # gan-song-song (goc lech giua 2 duong ke lien tiep < ANG_MIN deg).
    # Phan biet: fan VONG CUNG tot (muc tieu dan deu theo arc -> goc ke nhau ~15-25 deg,
    # PASS) vs fan "tuong day" xau (muc tieu xep cot doc -> cac duong gan song song ~1-8 deg,
    # FAIL). Khong trung khit nen C-COINCIDE khong bat duoc. LOW — ung vien thiet ke.
    R_HUB = 28.0
    FAN_MIN = 4
    ANG_MIN = 8.0
    end_list = []
    for ci, c in enumerate(dia.conns):
        if c.length() >= 60:
            end_list.append((ci, c.a))
            end_list.append((ci, c.b))
    used_conn = set()
    scored = []
    for ci, p in end_list:
        near = {cj for cj, q in end_list if math.dist(p, q) <= R_HUB}
        near.add(ci)
        scored.append((len(near), p, near))
    scored.sort(key=lambda t: -t[0])
    for cnt, p, near in scored:
        if cnt < FAN_MIN:
            break
        fresh = {cj for cj in near if cj not in used_conn}
        if len(fresh) < FAN_MIN:
            continue
        if any(e.contains_point(p[0], p[1], inflate=6.0) for e in nodes):
            continue  # hoi tu hop le vao cung mot ellipse/node
        # huong cua moi duong tinh tu dau hub
        dirs = []
        for cj in fresh:
            c = dia.conns[cj]
            q = c.a if math.dist(c.a, p) <= math.dist(c.b, p) else c.b
            r = c.b if q is c.a else c.a
            dirs.append((math.degrees(math.atan2(r[1] - q[1], r[0] - q[0])), cj, q))
        dirs.sort()
        angs = [d[0] for d in dirs]
        diffs = [abs(angs[k + 1] - angs[k]) for k in range(len(angs) - 1)]
        med_len = statistics.median(dia.conns[cj].length() for _, cj, _ in dirs)
        if diffs and min(diffs) < ANG_MIN and med_len >= 120.0:
            pts = [q for _, _, q in dirs]
            bb = (min(q[0] for q in pts), min(q[1] for q in pts),
                  max(q[0] for q in pts), max(q[1] for q in pts))
            F.append(Finding(
                "C-FAN",
                f"{len(fresh)} duong xuat phat gan mot diem (ban kinh {R_HUB:.0f}px tai "
                f"({p[0]:.0f},{p[1]:.0f})) va gan SONG SONG (goc lech nho nhat giua 2 duong ke = "
                f"{min(diffs):.1f} deg < {ANG_MIN:.0f}) — 'QUAT GA/TUONG DAY' (SKILL §3.2b)",
                _inflate(bb, 24),
                "Dan deu muc tieu tren CUNG quanh actor (goc giua 2 duong ke >= ~15 deg, dung "
                "make_drawio.py) hoac xep theo cum; xep muc tieu thanh cot doc se sinh tuong day. "
                "Neu la 'goc chung' co chu dich thi ghi BAO-OAN voi ly do.",
            ))
            used_conn |= fresh
            break  # chi bao hub to nhat de bang audit gon

    # =============== C-DANGLE ===============
    # Neo hop le = cham node / nhan / glyph actor, HOAC nam GIUA THAN mot duong khac
    # (chu T / diem noi vao lifeline cua sequence diagram).
    anchor = [e.bbox for e in nodes] + [lb.bbox for lb in dia.labels] + [g for g in dia.glyph_boxes]
    for ci, c in enumerate(dia.conns):
        for endname, p in (("dau", c.a), ("cuoi", c.b)):
            ok = any(_in_box(p[0], p[1], bb, 6) for bb in anchor)
            if not ok:
                ok = _on_other_interior(p, dia.conns, ci)
            if not ok:
                # Ngoai le: BARB CUA MUI TEN HO (open arrow «include»/«extend»).
                # Doan RAT NGAN (<=18px) ma dau kia da neo vao node/nhan => day la 1 nua
                # mui ten, khong phai duong noi bi lo lung. Duong noi that su bi lo lung
                # thi dai hon nhieu, nen nguong ngan nay khong che duoc loi that.
                other = c.b if endname == "dau" else c.a
                if c.length() <= 18.0 and any(_in_box(other[0], other[1], bb, 6) for bb in anchor):
                    ok = True
            if not ok:
                F.append(Finding(
                    "C-DANGLE",
                    f"Duong #{ci} co {endname} LO LUNG tai ({p[0]:.0f},{p[1]:.0f}) — khong cham node/actor/nhan nao",
                    (p[0] - 34, p[1] - 34, p[0] + 34, p[1] + 34),
                    "Keo neo dung vao bien node/actor; kiem lai toa do.",
                ))

    # =============== A-BAND / A-SKEW ===============
    if boundary and dia.glyph_boxes:
        left, right, mid = [], [], []
        for g in dia.glyph_boxes:
            cx = (g[0] + g[2]) / 2
            if cx <= boundary.x0 - 2:
                left.append(cx)
            elif cx >= boundary.x1 + 2:
                right.append(cx)
            else:
                mid.append(cx)
        if mid:
            F.append(Finding(
                "A-BAND",
                f"{len(mid)} actor KHONG theo dai trai/phai (x={[round(m) for m in mid]}) — luat: actor chi duoc o Lane L hoac Lane R",
                (min(mid) - 40, 0, max(mid) + 40, dia.height),
                "Day actor ra ngoai khung boundary, gon vao 1 cot trai hoac phai.",
            ))
        for name, side in (("trai", left), ("phai", right)):
            if len(side) >= 3 and statistics.pstdev(side) > 12.0:
                F.append(Finding(
                    "A-SKEW",
                    f"Cac actor dai {name} KHONG thang cot (do lech chuan x = {statistics.pstdev(side):.1f}px)",
                    (min(side) - 40, 0, max(side) + 40, dia.height),
                    "Can cot actor neu lech vo y; actor cao/thap hon de bam tam cum lien quan co chu dich thi ghi BAO-OAN (van phai o dai L/R).",
                ))

    # =============== U-OCCUPY ===============
    F.extend(_occupancy(dia))

    # =============== S-TINY / S-FONT ===============
    for lb in dia.labels:
        if lb.size < TH["tiny_font"] and len(lb.text) >= 3:
            F.append(Finding(
                "S-TINY",
                f"Co chu {lb.size:.1f}pt < {TH['tiny_font']}pt: '{_short(lb.text)}'",
                _inflate(lb.bbox, 8),
                "Tang co chu hoac phan ra so do nho hon de in A4 doc duoc.",
            ))
    mixed = [lb for lb in dia.labels
             if len({f.split("-")[0].strip() for f in lb.fonts}) > 1 and len(lb.text) >= 2]
    if mixed:
        F.append(Finding(
            "S-FONT",
            f"{len(mixed)}/{len(dia.labels)} nhan co >1 ho font tron lan trong 1 nhan "
            f"(vd '{_short(mixed[0].text)}': {sorted({f.split('-')[0].strip() for f in mixed[0].fonts})}). "
            f"Thuong do dau tieng Viet roi sang font du phong cua trinh render.",
            _inflate(_union(*[lb.bbox for lb in mixed[:12]]), 10),
            "Nhung font phu day du dau tieng Viet (Arial Unicode / DejaVu Sans) de 1 font duy nhat; "
            "kiem lai bang Chrome/LibreOffice chu khong chi viewer nay.",
        ))

    # =============== S-RATIO ===============
    if dia.height > 0:
        ratio = dia.width / dia.height
        if ratio > TH["ratio_max"] or ratio < TH["ratio_min"]:
            F.append(Finding(
                "S-RATIO",
                f"Ty le khung {ratio:.2f}:1 ngoai [{TH['ratio_min']}, {TH['ratio_max']}] — chen A4 ~15cm se bi bep chu",
                (0, 0, dia.width, dia.height),
                "Chia nhieu hang/cot lai, hoac tach thanh 2 so do.",
            ))

    # =============== S-BOUNDARY ===============
    if boundary:
        for e in nodes:
            if not _inside(e.bbox, boundary.bbox, pad=-1):
                F.append(Finding(
                    "S-BOUNDARY",
                    f"Ellipse '{_short(dia.label_of(e))}' TRAN ra ngoai khung system boundary",
                    _inflate(_union(e.bbox, boundary.bbox), 0),
                    "Thu nho ban kinh ellipse hoac nong khung boundary.",
                ))

    # =============== D-DUP ===============
    seen = {}
    for lb in dia.labels:
        key = re.sub(r"\s+", " ", lb.text.strip().lower())
        if len(key) < 5 or key in REL_LABELS or key.strip("«»") in REL_LABELS:
            continue
        seen.setdefault(key, []).append(lb)
    for key, grp in seen.items():
        if len(grp) >= 2:
            F.append(Finding(
                "D-DUP",
                f"Nhan '{_short(key)}' xuat hien {len(grp)} lan Y NGUYEN VAN — kiem copy-paste",
                _inflate(_union(*[lb.bbox for lb in grp]), 12),
                "Xac nhan co phai 2 use case that su khac nhau; neu khong thi gop lai.",
            ))

    return F


def _on_other_interior(pt, conns, exclude_idx, tol=3.5, edge_skip=9.0):
    """True neu pt nam tren THAN (khong phai 2 dau) cua mot duong noi khac => chu T hop le."""
    for j, c in enumerate(conns):
        if j == exclude_idx:
            continue
        pts = c.sample(3.0)
        if len(pts) < 4:
            continue
        # bo 2 dau: uoc luong bang khoang cach tich luy
        inner = []
        acc = 0.0
        for k in range(len(pts) - 1):
            acc += math.dist(pts[k], pts[k + 1])
            if acc > edge_skip:
                inner.append(pts[k])
        if len(inner) > 2:
            inner = inner[:-2]
        for q in inner:
            if math.dist(pt, q) <= tol:
                return True
    return False


def _coincide(a: Conn, b: Conn):
    pa, pb = a.sample(6.0), b.sample(6.0)
    if len(pa) < 3 or len(pb) < 3:
        return 0.0
    near = sum(1 for p in pa if any(math.dist(p, q) <= TH["coincide_tol"] for q in pb))
    return near / len(pa)


def _occupancy(dia: Diagram):
    out = []
    items = [e.bbox for e in dia.nodes] + [lb.bbox for lb in dia.labels if lb.size >= TH["tiny_font"]]
    if len(items) < 5:
        return out
    ub = _union(*items)
    gw, gh = max(1.0, ub[2] - ub[0]), max(1.0, ub[3] - ub[1])
    gx = gy = 3
    cells = [[0.0] * gx for _ in range(gy)]
    for bb in items:
        cx = min(gx - 1, max(0, int((((bb[0] + bb[2]) / 2) - ub[0]) / gw * gx)))
        cy = min(gy - 1, max(0, int((((bb[1] + bb[3]) / 2) - ub[1]) / gh * gy)))
        cells[cy][cx] += (bb[2] - bb[0]) * (bb[3] - bb[1])
    total = sum(sum(r) for r in cells) or 1.0
    frac = [[c / total for c in row] for row in cells]
    occupied = sum(1 for row in frac for c in row if c > 0.02)
    share = occupied / (gx * gy)
    worst = max(c for row in frac for c in row)
    if share < TH["occ_min"]:
        out.append(Finding("U-OCCUPY",
                           f"Chi {occupied}/{gx*gy} o luoi co noi dung ({share:.0%}) — so do RONG / don cuc mot phia",
                           ub, "Can doi: dan trai / dan cot cho het khung."))
    elif worst > TH["occ_worst"]:
        out.append(Finding("U-OCCUPY",
                           f"Mot o luoi chiem {worst:.0%} noi dung — mat thay la 'DON CUC'",
                           ub, "Dan cac cum cho khong cum nao chiem qua nua hinh; 'deu' = tuong dong giua cac cum, khong phai luoi mot buoc (SKILL §3.2b)."))
    return out


# --------------------------------------------------------------------------------------
# Xuat
# --------------------------------------------------------------------------------------
def make_crops(path, dia, findings, outdir, scale):
    os.makedirs(outdir, exist_ok=True)
    page = pymupdf.open(path)[0]
    made = []
    for f in findings:
        if f.sev == "INFO":
            continue
        pad = max(12.0, 0.03 * max(dia.width, dia.height))
        clip = pymupdf.Rect(*_inflate(f.bbox, pad)) & page.rect
        if clip.is_empty:
            continue
        try:
            pm = page.get_pixmap(clip=clip, dpi=int(round(72 * scale)))
        except Exception:
            continue
        idx = len(made) + 1
        name = f"F{idx:02d}-{f.code.replace('-', '_')}.png"
        pm.save(os.path.join(outdir, name))
        made.append((idx, f, name))
    return made


def make_overlay(path, dia, outdir, scale=2.0):
    try:
        from io import BytesIO

        from PIL import Image, ImageDraw
    except ImportError:
        return None
    os.makedirs(outdir, exist_ok=True)
    page = pymupdf.open(path)[0]
    pm = page.get_pixmap(dpi=int(round(72 * scale)))
    im = Image.open(BytesIO(pm.tobytes("png"))).convert("RGB")
    W, H = im.size
    dr = ImageDraw.Draw(im)
    step = 10
    for k in range(1, step):
        x, y = int(W * k / step), int(H * k / step)
        col = (255, 0, 0) if k == step // 2 else (0, 160, 255)
        dr.line([(x, 0), (x, H)], fill=col, width=1)
        dr.line([(0, y), (W, y)], fill=col, width=1)
    dr.rectangle([0, 0, W - 1, H - 1], outline=(0, 0, 0), width=2)
    out = os.path.join(outdir, "overlay.png")
    im.save(out)
    return out


def write_report(dia, findings, made, outdir, overlay):
    os.makedirs(outdir, exist_ok=True)
    by = {"HIGH": [], "MEDIUM": [], "LOW": [], "INFO": []}
    for f in findings:
        by.setdefault(f.sev, []).append(f)

    name = os.path.splitext(os.path.basename(dia.path))[0]
    L = []
    L.append(f"# Soi bang mat — {name}\n")
    L.append("> Sinh boi `eye_audit.py`. **Script KHONG phan quyet PASS/FAIL** — no chi liet ke UNG VIEN\n"
             "> va cat anh phong to. Cong nghiem thu van la: **mo anh, tu nhin, tu tra loi**.\n")
    L.append(f"- Nguon: `{dia.path}`")
    L.append(f"- Khung: {dia.width:.0f} x {dia.height:.0f} (ty le {dia.width/max(dia.height,1):.2f}:1)")
    L.append(f"- Do luong: {len(dia.nodes)} node ellipse · {len(dia.labels)} nhan · "
             f"{len(dia.conns)} duong noi · {len(dia.glyph_boxes)} actor · "
             f"{1 if dia.boundary else 0} khung boundary")
    L.append(f"- Ung vien: **HIGH={len(by['HIGH'])}** · MEDIUM={len(by['MEDIUM'])} · "
             f"LOW={len(by['LOW'])} · INFO={len(by['INFO'])}\n")
    L.append("## 0. BAT BUOC DIEN SAU KHI NHIN ANH\n")
    L.append("Mo `overlay.png` (co luoi) va tung file trong `crops/`, roi dien bang duoi.\n")
    L.append("| # | Ma | Zoom can xem | Mat thay gi (nguyen van) | That / Bao oan | Da sua? |")
    L.append("|---|---|---|---|---|---|")
    for i, f, fname in made:
        L.append(f"| {i} | {f.code} | `crops/{fname}` | _(dien)_ | _(That/Bao oan)_ | _(co/khong)_ |")
    if not made:
        L.append("| — | — | — | _(khong co ung vien — VAN phai mo overlay.png nhan xac nhan)_ | | |")
    L.append("")
    L.append("Bang chung toi thieu de duoc coi la **DA SOI**: doc nguyen van >= 3 nhan + vi tri\n"
             "(vd \"ellipse 'Rút tiền' o cot giua, hang 8\"), va tra loi du 3 cau "
             "**de? deu? de nhin?**\n")
    for title, key in (("1. Ung vien MUC DO CAO — uu tien soi truoc", "HIGH"),
                       ("2. Ung vien MUC DO TRUNG BINH", "MEDIUM"),
                       ("3. Ung vien MUC DO THAP", "LOW"),
                       ("4. Ghi chu thiet ke (KHONG phai loi)", "INFO")):
        L.append(f"## {title}\n")
        if not by[key]:
            L.append("_(khong co)_\n")
        for f in by[key]:
            L.append(f"- **{f.code}** — {f.msg}")
            if f.fix and key != "INFO":
                L.append(f"  - Goi y sua: {f.fix}")
        L.append("")
    L.append("## 5. Ket luan\n")
    L.append("```text")
    L.append("Da mo overlay.png?            YES/NO")
    L.append("Da mo TAT CA crops/?          YES/NO   (neu NO thi moi ket luan deu KHONG hop le)")
    L.append("De?        <doc nguyen van >=3 nhan + vi tri>")
    L.append("Deu?       <khoang cach / can chinh / do lech>")
    L.append("De nhin?   <lan theo duoc duong khong? co vong xa khong?>")
    L.append("Ket luan:  PASS / BLOCKED-Visual   (CAM ghi PASS khi chua dien muc 0)")
    L.append("```")
    L.append("")
    if overlay:
        L.append(f"Overlay luoi: `{os.path.relpath(overlay, outdir)}`\n")
    out = os.path.join(outdir, "eye-audit.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
    return out


def dump_model(dia: Diagram):
    print("  -- MO HINH DA DOC (kiem parser truoc khi tin ket qua) --")
    b = dia.boundary
    print(f"  boundary: {('x %.0f..%.0f, y %.0f..%.0f' % (b.x0, b.x1, b.y0, b.y1)) if b else 'KHONG THAY'}")
    for i, g in enumerate(dia.glyph_boxes):
        print(f"  actor#{i}: x {g[0]:.0f}..{g[2]:.0f}, y {g[1]:.0f}..{g[3]:.0f}")
    for i, e in enumerate(dia.nodes):
        owners = [lb for lb in dia.labels if e.contains_point(lb.cx, lb.cy, inflate=1.0)]
        tight = 0.0
        if owners:
            ub = _union(*[lb.ink_bbox() for lb in owners])
            tight = max(e.radial_of(x, y) for x, y in
                        [(ub[0], ub[1]), (ub[2], ub[1]), (ub[0], ub[3]), (ub[2], ub[3]),
                         ((ub[0] + ub[2]) / 2, ub[1]), ((ub[0] + ub[2]) / 2, ub[3])])
        print(f"  node#{i:02d}: ({e.cx:6.0f},{e.cy:6.0f}) rx={e.rx:3.0f} ry={e.ry:3.0f} "
              f"day={tight*100:3.0f}%  '{_short(dia.label_of(e), 34)}'")
    for i, c in enumerate(dia.conns):
        kinds = "net-dut" if c.dashed else "lien   "
        print(f"  conn#{i:02d}: {kinds} w={c.width:<4} dai={c.length():6.0f} "
              f"({c.a[0]:.0f},{c.a[1]:.0f}) -> ({c.b[0]:.0f},{c.b[1]:.0f})")
    print()


# --------------------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(description="Soi so do ve tay nhu mat nguoi (ung vien + zoom crop + overlay).")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--out", default=None)
    ap.add_argument("--scale", type=float, default=4.0)
    ap.add_argument("--overlay", action="store_true")
    ap.add_argument("--dump", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    worst = 0
    for path in args.files:
        if not os.path.isfile(path):
            print(f"[eye_audit] Khong thay file: {path}", file=sys.stderr)
            worst = max(worst, 2)
            continue
        try:
            dia = read_diagram(path)
        except Exception as e:  # noqa: BLE001
            print(f"[eye_audit] Khong doc duoc '{path}': {e}", file=sys.stderr)
            worst = max(worst, 2)
            continue

        findings = check(dia)
        base = os.path.splitext(os.path.basename(path))[0]
        outdir = args.out or os.path.join(os.path.dirname(os.path.abspath(path)), f"{base}-audit")
        made = make_crops(path, dia, findings, os.path.join(outdir, "crops"), args.scale)
        ov = make_overlay(path, dia, outdir) if args.overlay else None
        report = write_report(dia, findings, made, outdir, ov)

        n = {k: sum(1 for f in findings if f.sev == k) for k in ("HIGH", "MEDIUM", "LOW", "INFO")}
        print(f"== {base} ==")
        print(f"   node={len(dia.nodes)} nhan={len(dia.labels)} conn={len(dia.conns)} actor={len(dia.glyph_boxes)}")
        if args.dump:
            dump_model(dia)
        if not args.quiet:
            for f in findings:
                if f.sev == "INFO":
                    continue
                print(f"   [{f.sev:6}] {f.code:12} {f.msg}")
        print(f"   -> HIGH={n['HIGH']} MEDIUM={n['MEDIUM']} LOW={n['LOW']} "
              f"INFO={n['INFO']} | crop={len(made)}")
        print(f"   bao cao: {report}")
        if args.strict and n["HIGH"]:
            worst = max(worst, 1)

    print("\n[NHAC LAI] Script chi tim UNG VIEN. Chua mo crops/ va overlay.png = CHUA audit.")

    return worst


if __name__ == "__main__":
    sys.exit(main())
