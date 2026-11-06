#!/usr/bin/env python3
"""Engine ve tay so do sach: boxes + orthogonal routing, xuat PNG (supersampled) + SVG.
Quy uoc: trang-den, font DejaVu Sans, khong title trong anh, tieng Viet day du dau.
Dat trong tools/ theo ky luat Dedicated Tools Directory.
"""
from PIL import Image, ImageDraw, ImageFont

FONT = "C:/Windows/Fonts/DejaVuSans.ttf"
FONT_B = "C:/Windows/Fonts/DejaVuSans-Bold.ttf"
INK = (0, 0, 0)
PAPER = (255, 255, 255)


def _font(bold, size, ss):
    return ImageFont.truetype(FONT_B if bold else FONT, size * ss)


class Diagram:
    def __init__(self, w, h, ss=2):
        self.w, self.h, self.ss = w, h, ss
        self.img = Image.new("RGB", (w * ss, h * ss), PAPER)
        self.d = ImageDraw.Draw(self.img)
        self.svg = []
        self.boxes = {}

    # ---- text metrics (1x units) ----
    def tw(self, s, bold, size):
        f = _font(bold, size, 1)
        b = f.getbbox(s)
        return b[2] - b[0]

    # ---- primitives (coords in 1x) ----
    def _L(self, x1, y1, x2, y2, w=2):
        s = self.ss
        self.d.line([x1 * s, y1 * s, x2 * s, y2 * s], fill=INK, width=max(1, w * s))

    def _C(self, x, y, r, fill=None, w=2):
        s = self.ss
        self.d.ellipse([x * s - r * s, y * s - r * s, x * s + r * s, y * s + r * s],
                       outline=INK, width=max(1, w * s), fill=fill)

    def _R(self, x, y, w, h, fill=None, wline=2):
        s = self.ss
        self.d.rectangle([x * s, y * s, (x + w) * s, (y + h) * s],
                         outline=INK, width=max(1, wline * s), fill=fill)

    def _T(self, x, y, s_, bold=False, size=18, anchor_left=True, halo=True):
        f = _font(bold, size, self.ss)
        xx, yy = x * self.ss, y * self.ss
        if halo:
            b = f.getbbox(s_)
            pad = 3 * self.ss
            self.d.rectangle([xx - pad, yy - pad, xx + (b[2] - b[0]) + pad, yy + (b[3] - b[1]) + pad],
                             fill=PAPER)
        self.d.text((xx, yy), s_, font=f, fill=INK, anchor="la" if anchor_left else "ma")
        self.svg.append(
            '<text x="%d" y="%d" font-family="DejaVu Sans" font-size="%d" font-weight="%s" fill="black">%s</text>'
            % (x, y + size, size, "bold" if bold else "normal", _esc(s_)))

    # ---- entity/class box ----
    def box(self, bid, x, y, w, badge, name, sections, hsize=20, rsize=18):
        """sections: list of list-of-rows. Tra ve dict(x,y,w,h)."""
        pad, lpad = 10, 12
        lh_h, lh_r = hsize + 12, rsize + 8
        inner = w - lpad * 2
        h = pad + lh_h + 6
        for sec in sections:
            h += 4
            for row in sec:
                h += lh_r
            h += 6
        h += pad - 4
        self.boxes[bid] = {"x": x, "y": y, "w": w, "h": h}
        self._R(x, y, w, h, fill=PAPER)
        self.svg.append('<rect x="%d" y="%d" width="%d" height="%d" fill="white" stroke="black" stroke-width="2"/>' % (x, y, w, h))
        # badge + name
        cx, cy, br = x + 22, y + pad + lh_h // 2 - 2, 11
        self._C(cx, cy, br, fill=(210, 210, 210))
        self.svg.append('<circle cx="%d" cy="%d" r="%d" fill="#D2D2D2" stroke="black" stroke-width="2"/>' % (cx, cy, br))
        self._T(cx - 6, cy - 11, badge, bold=True, size=15)
        self._T(x + 40, y + pad, name, bold=True, size=hsize)
        yy = y + pad + lh_h
        self._L(x, yy, x + w, yy)
        self.svg.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="black" stroke-width="2"/>' % (x, yy, x + w, yy))
        yy += 4
        for si, sec in enumerate(sections):
            for row in sec:
                self._T(x + lpad, yy, row, size=rsize)
                yy += lh_r
            if si < len(sections) - 1:
                self._L(x, yy + 2, x + w, yy + 2)
                self.svg.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="black" stroke-width="1"/>' % (x, yy + 2, x + w, yy + 2))
                yy += 6
        return self.boxes[bid]

    # ---- orthogonal edge ----
    def edge(self, pts, end_mark="none", start_mark="none", label=None,
             label_pos=0.5, m_start=None, m_end=None):
        """pts: [(x,y)...] orthogonal. marks: none|one|many|zeroone."""
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            self._L(x1, y1, x2, y2)
            self.svg.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="black" stroke-width="2"/>' % (x1, y1, x2, y2))
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self._C(mx, my, 1, fill=INK)
            self.svg.append('<circle cx="%d" cy="%d" r="1" fill="black"/>' % (mx, my))
        self._mark(pts[0], pts[1], start_mark, at_start=True)
        self._mark(pts[-1], pts[-2], end_mark, at_start=False)
        if label:
            i = int(label_pos * (len(pts) - 1))
            (x1, y1), (x2, y2) = pts[i], pts[i + 1]
            self._T((x1 + x2) / 2 + 4, (y1 + y2) / 2 - 20, label, size=17)
        if m_start:
            (x1, y1), (x2, y2) = pts[0], pts[1]
            self._mult(x1, y1, x2, y2, m_start, near_start=True)
        if m_end:
            (x1, y1), (x2, y2) = pts[-2], pts[-1]
            self._mult(x1, y1, x2, y2, m_end, near_start=False)

    def _mark(self, tip, nxt, kind, at_start):
        if kind in ("none", None):
            return
        x, y = tip
        dx = 1 if nxt[0] > x else (-1 if nxt[0] < x else 0)
        dy = 1 if nxt[1] > y else (-1 if nxt[1] < y else 0)
        if kind == "one":  # tee tick
            if dx:
                self._L(x, y - 7, x, y + 7); self._svg_line(x, y - 7, x, y + 7)
            else:
                self._L(x - 7, y, x + 7, y); self._svg_line(x - 7, y, x + 7, y)
        elif kind == "many":  # crow foot
            L = 13
            if dx:
                bx = x + dx * L
                for oy in (-6, 0, 6):
                    self._L(x, y, bx, y + oy); self._svg_line(x, y, bx, y + oy)
            else:
                by = y + dy * L
                for ox in (-6, 0, 6):
                    self._L(x, y, x + ox, by); self._svg_line(x, y, x + ox, by)
        elif kind == "zeroone":  # open circle
            self._C(x + dx * 7 if dx else x, y + dy * 7 if dy else y, 6, fill=PAPER)

    def _svg_line(self, x1, y1, x2, y2):
        self.svg.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="black" stroke-width="2"/>' % (x1, y1, x2, y2))

    def _mult(self, x1, y1, x2, y2, txt, near_start):
        d = 26
        if x2 > x1: mx, my = x1 + d, y1 - 20
        elif x2 < x1: mx, my = x1 - d - 30, y1 - 20
        elif y2 > y1: mx, my = x1 + 6, y1 + d - 14
        else: mx, my = x1 + 6, y1 - d - 14
        self._T(mx, my, txt, size=16)

    def save(self, base):
        small = self.img.resize((self.w, self.h), Image.LANCZOS)
        small.save(base + ".png")
        with open(base + ".svg", "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" '
                    'width="%d" height="%d" viewBox="0 0 %d %d">\n<rect width="100%%" height="100%%" fill="white"/>\n'
                    % (self.w, self.h, self.w, self.h))
            f.write("\n".join(self.svg))
            f.write("\n</svg>\n")
        print("saved", base, "%dx%d" % (self.w, self.h))


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
