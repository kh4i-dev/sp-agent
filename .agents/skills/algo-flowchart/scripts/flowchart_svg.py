# -*- coding: utf-8 -*-
"""flowchart_svg.py — thư viện vẽ SƠ ĐỒ KHỐI thuật toán chuẩn giáo trình.

Ký hiệu (theo môn Kỹ thuật lập trình):
  oval    : Bắt đầu / Kết thúc           <ellipse>
  rect    : Xử lý / tính toán / gán      <rect>
  diamond : Điều kiện (Đúng / Không)     <polygon>
  para    : Nhập / Xuất                  <polygon (hình bình hành)>
  seg_arrow / elbow: luồng + mũi tên tam giác đặc

Cách dùng (quick):
  from flowchart_svg import Canvas
  c = Canvas(431, 440)                     # theo pt; 431pt ~ bề ngang hình chuẩn
  c.oval (215, 22, 110, 22, "Bắt đầu")
  c.seg_arrow(215, 33, 215, 45)
  c.para  (215, 58, 184, 26, "Nhập truy vấn")
  ...
  c.note_box(14, 442, 403, 62, ["dòng 1", "dòng 2"])   # tùy chọn, net dut
  c.save("fig.svg"); c.render_png("fig.png")            # can ImageMagick
"""
import math

W_NS = 'font-family="Arial, Helvetica, sans-serif"'
STROKE = "#000"
SW = 1.1


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}pt" height="{h}pt" '
            f'viewBox="0 0 {w} {h}">',
            f'<rect width="{w}" height="{h}" fill="#ffffff"/>',
        ]

    # ---- text ----
    def text(self, x, y, s, size=8.5, bold=False, anchor="middle"):
        b = 'font-weight="bold" ' if bold else ""
        self.parts.append(
            f'<text x="{x}" y="{y}" {W_NS} font-size="{size}" {b}'
            f'text-anchor="{anchor}" fill="{STROKE}">{s}</text>')

    # ---- symbols ----
    def oval(self, cx, cy, w, h, s, size=8.5):
        self.parts.append(
            f'<ellipse cx="{cx}" cy="{cy}" rx="{w/2}" ry="{h/2}" fill="none" '
            f'stroke="{STROKE}" stroke-width="{SW}"/>')
        self.text(cx, cy + size * 0.35, s, size)

    def rect(self, cx, cy, w, h, lines, center=True, bold_last=False):
        self.parts.append(
            f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" '
            f'fill="none" stroke="{STROKE}" stroke-width="{SW}"/>')
        n = len(lines)
        for i, s in enumerate(lines):
            size = 8.5 if (n == 1 or i == 0) else (7.5 if len(s) > 34 else 8)
            if center:
                yy = cy + size * 0.35 + (i - (n - 1) / 2) * 11.5
            else:
                yy = cy - h / 2 + 11 + i * 11.5
            self.text(cx, yy, s, size, bold=bold_last and i == n - 1)

    def para(self, cx, cy, w, h, s, size=8.5, sk=13):
        x0, y0 = cx - w / 2, cy - h / 2
        pts = f"{x0+sk},{y0} {x0+w},{y0} {x0+w-sk},{y0+h} {x0},{y0+h}"
        self.parts.append(
            f'<polygon points="{pts}" fill="none" stroke="{STROKE}" '
            f'stroke-width="{SW}"/>')
        self.text(cx, cy + size * 0.35, s, size)

    def diamond(self, cx, cy, w, h, s, size=8.5):
        pts = f"{cx},{cy-h/2} {cx+w/2},{cy} {cx},{cy+h/2} {cx-w/2},{cy}"
        self.parts.append(
            f'<polygon points="{pts}" fill="none" stroke="{STROKE}" '
            f'stroke-width="{SW}"/>')
        self.text(cx, cy + size * 0.35, s, size)

    # ---- connectors ----
    def _head(self, x, y, dx, dy):
        n = math.hypot(dx, dy)
        dxn, dyn = dx / n, dy / n
        px, py = -dyn, dxn
        ax, ay = x - 3.4 * dxn, y - 3.4 * dyn
        return (f'<polygon points="{x},{y} {ax+2.6*px:.1f},{ay+2.6*py:.1f} '
                f'{ax-2.6*px:.1f},{ay-2.6*py:.1f}" fill="{STROKE}"/>')

    def line(self, x1, y1, x2, y2):
        self.parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{STROKE}" stroke-width="{SW}"/>')

    def seg_arrow(self, x1, y1, x2, y2):
        n = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / n, (y2 - y1) / n
        self.line(x1, y1, x2 - ux * 3, y2 - uy * 3)
        self.parts.append(self._head(x2, y2, ux, uy))

    def elbow_arrow(self, pts, head_dx, head_dy):
        """Đgấp khúc 90 độ: pts = [(x,y), ...]; head ở điểm cuối."""
        for a, b in zip(pts, pts[1:]):
            self.line(*a, *b)
        self.parts.append(self._head(pts[-1][0], pts[-1][1], head_dx, head_dy))

    def label(self, x, y, s, anchor="start", size=8):
        self.text(x, y, s, size, anchor=anchor)

    # ---- optional note box (net dut) ----
    def note_box(self, x, y, w, h, lines, size=8):
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" '
            f'stroke="{STROKE}" stroke-width="1.1" stroke-dasharray="5,3"/>')
        step = h / (len(lines) + 1)
        for i, s in enumerate(lines):
            self.text(x + w / 2, y + step * (i + 1) + size * 0.35, s, size)

    # ---- output ----
    def save(self, path):
        self.parts.append("</svg>")
        open(path, "w", encoding="utf-8").write("\n".join(self.parts))
        return path

    def render_png(self, svg_path=None, png_path=None, magick=None):
        import os, subprocess
        if svg_path is None:
            raise ValueError("phải save() trước hoặc truyền svg_path")
        if png_path is None:
            png_path = os.path.splitext(svg_path)[0] + ".png"
        magick = magick or r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
        subprocess.run([magick, "-density", "300", "-background", "white",
                        svg_path, "-flatten", png_path], capture_output=True, text=True)
        return png_path
