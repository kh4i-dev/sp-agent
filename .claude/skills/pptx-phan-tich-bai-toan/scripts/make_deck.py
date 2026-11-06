#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
make_deck.py — sinh deck .pptx cho CHUONG PHAN TICH BAI TOAN (bao cao do an / BTL).

Moi phan tu deu la shape / textbox NATIVE cua PowerPoint => bien tap duoc tung layer,
khong flatten, khong anh hoa chu. Noi dung lay tu file spec JSON.

    python make_deck.py --spec assets/spec.example.json --out deck.pptx
    python make_deck.py --blank --out template.pptx      # khung rong de tu dien

Yeu cau: python-pptx (>=1.0), Pillow.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN, MSO_AUTO_SIZE
from pptx.util import Emu, Inches, Pt

try:
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None

# ----------------------------------------------------------------------------
# Bang mau hoc thuat: nen sang, 1 mau chu dao (navy/cyan) + 1 accent, khong gradient.
# ----------------------------------------------------------------------------
C = {
    "ink":       "122F38",
    "body":      "2E4A54",
    "muted":     "6C848E",
    "brand":     "0E7490",
    "brand_dk":  "0A4E60",
    "brand_soft": "E9F3F6",
    "line":      "D7E4EA",
    "surface":   "F5F9FA",
    "white":     "FFFFFF",
    "good":      "1B7F4B",
    "good_soft": "EAF6EE",
    "bad":       "B42318",
    "bad_soft":  "FBECEA",
    "warn":      "A45A03",
    "warn_soft": "FBF1E4",
    "ghost":     "C2DBE4",   # so thu tu mo lon (khong dung cho chu can doc)
}
FONT_H = "Arial"            # tieu de
FONT_B = "Times New Roman"  # than bai  (deu an toan khi render + dau tieng Viet)

SW, SH = 13.333, 7.5       # inch, 16:9
M = 0.62                   # margin ngang
CW = SW - 2 * M            # be rong vung noi dung


def _rgb(hx: str) -> RGBColor:
    return RGBColor.from_string(hx)


# ----------------------------------------------------------------------------
# Primitive
# ----------------------------------------------------------------------------
def _tx(slide, x, y, w, h, name="text"):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    return tb, tf


def _para(tf, first=False):
    return tf.paragraphs[0] if first else tf.add_paragraph()


def write(tf, blocks, first=True):
    """blocks: list of dict(text, size, color, bold, font, align, space_before, line, italic)."""
    for i, b in enumerate(blocks):
        p = _para(tf, first and i == 0)
        p.alignment = b.get("align", PP_ALIGN.LEFT)
        if b.get("space_before"):
            p.space_before = Pt(b["space_before"])
        if b.get("line"):
            p.line_spacing = b["line"]
        r = p.add_run()
        r.text = b["text"]
        f = r.font
        f.name = b.get("font", FONT_B)
        f.size = Pt(b.get("size", 15))
        f.bold = bool(b.get("bold"))
        f.italic = bool(b.get("italic"))
        f.color.rgb = _rgb(b.get("color", C["body"]))
    return tf


def box(slide, x, y, w, h, fill=None, line=None, radius=0.06, name="panel",
        line_w=0.75, shadow=False):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                 Inches(x), Inches(y), Inches(w), Inches(h))
    shp.name = name
    shp.adjustments[0] = radius
    if fill:
        shp.fill.solid()
        shp.fill.fore_color.rgb = _rgb(fill)
    else:
        shp.fill.background()
    if line:
        shp.line.color.rgb = _rgb(line)
        shp.line.width = Pt(line_w)
    else:
        shp.line.fill.background()
    shp.shadow.inherit = False
    tf = shp.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = Inches(0.14)
    tf.margin_top = tf.margin_bottom = Inches(0.08)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    return shp, tf


def hline(slide, x, y, w, color=None, name="rule", width=0.9):
    ln = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y),
                                Inches(w), Pt(width))
    ln.name = name
    ln.fill.solid()
    ln.fill.fore_color.rgb = _rgb(color or C["line"])
    ln.line.fill.background()
    ln.shadow.inherit = False
    return ln


def sq(slide, x, y, size=0.085, color=None, name="marker"):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y),
                               Inches(size), Inches(size))
    s.name = name
    s.fill.solid()
    s.fill.fore_color.rgb = _rgb(color or C["brand"])
    s.line.fill.background()
    s.shadow.inherit = False
    return s


def _img_size(path, bw, bh):
    if Image is None:
        return bw, bh
    with Image.open(path) as im:
        iw, ih = im.size
    r = min(bw / iw, bh / ih)
    return iw * r, ih * r


def picture(slide, path, x, y, w, h, name=None, frame=True, mode="contain"):
    """Chen anh THAT vao khung (x,y,w,h). mode='contain' giu ti le, 'cover' phu kin."""
    if not os.path.exists(path):
        sys.stderr.write(f"[warn] thieu anh: {path}\n")
        ph, tf = box(slide, x, y, w, h, fill=C["surface"], line=C["line"],
                     name=(name or "image") + "_missing")
        write(tf, [{"text": "[Thiếu ảnh: " + os.path.basename(path) + "]",
                    "size": 11, "color": C["muted"], "align": PP_ALIGN.CENTER}])
        return None
    if mode == "cover":
        iw, ih = _img_size(path, w, h)
        scale = max(w / iw, h / ih)
        # cat bang crop: dat lon hon khung roi can giua (giu don gian: dat theo contain)
        pic = slide.shapes.add_picture(path, Inches(x), Inches(y),
                                       Inches(w), Inches(h))
    else:
        iw, ih = _img_size(path, w, h)
        px = x + (w - iw) / 2
        py = y + (h - ih) / 2
        pic = slide.shapes.add_picture(path, Inches(px), Inches(py),
                                       Inches(iw), Inches(ih))
    pic.name = name or ("image_" + os.path.splitext(os.path.basename(path))[0])
    if frame:
        fr = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x - 0.06),
                                    Inches(y - 0.06), Inches(w + 0.12), Inches(h + 0.12))
        fr.name = (name or "image") + "_frame"
        fr.fill.background()
        fr.line.color.rgb = _rgb(C["line"])
        fr.line.width = Pt(0.75)
        fr.shadow.inherit = False
        # day frame xuong duoi anh ve z-order
        sp = fr._element
        sp.getparent().remove(sp)
        slide.shapes._spTree.insert(2, sp)
    return pic


# ----------------------------------------------------------------------------
# Chrome (header / footer) dung chung
# ----------------------------------------------------------------------------
def head(slide, title, kicker=None, y=0.44):
    if kicker:
        _, tf = _tx(slide, M, y - 0.02, CW, 0.24, "kicker")
        write(tf, [{"text": kicker, "size": 11.5, "color": C["brand"],
                    "font": FONT_H, "bold": False}])
        y += 0.26
    _, tf = _tx(slide, M, y, CW, 0.62, "title")
    write(tf, [{"text": title, "size": 25, "color": C["ink"], "font": FONT_H,
                "bold": True, "line": 1.0}])
    return y + 0.66


def foot(slide, meta, n, total=None):
    txt = meta.get("footer", "")
    if txt:
        _, tf = _tx(slide, M, SH - 0.42, CW * 0.75, 0.24, "footer")
        write(tf, [{"text": txt, "size": 9.5, "color": C["muted"], "font": FONT_H}])
    _, tf = _tx(slide, SW - M - 1.4, SH - 0.42, 1.4, 0.24, "pageno")
    write(tf, [{"text": f"{n}", "size": 9.5, "color": C["muted"],
                "font": FONT_H, "align": PP_ALIGN.RIGHT}])


def _bullet_rows(slide, x, y, w, items, size=15, gap=0.06, line_color=None,
                 text_color=None, marker_color=None):
    """Moi bullet = 1 textbox + 1 o vuong nho: de sua tung dong, khong dung ky tu bullet."""
    cy = y
    for it in items:
        txt = it["text"] if isinstance(it, dict) else it
        bold = it.get("bold") if isinstance(it, dict) else None
        sq(slide, x, cy + 0.075, 0.085, marker_color or C["brand"], "bullet_dot")
        _, tf = _tx(slide, x + 0.24, cy, w - 0.24, 0.28, "bullet_text")
        write(tf, [{"text": txt, "size": size, "color": text_color or C["body"],
                    "bold": bold, "line": 1.18}])
        cy += 0.30 + gap
    return cy


# ----------------------------------------------------------------------------
# Layouts
# ----------------------------------------------------------------------------
def lay_cover(prs, meta, d, n):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = box(s, 0, 0, SW, SH, fill=C["white"], line=None, radius=0.0, name="bg")
    # dai nen nhat ben phai
    box(s, 7.35, 0, SW - 7.35, SH, fill=C["brand_soft"], line=None,
        radius=0.0, name="cover_side")
    img = d.get("image")
    if img:
        picture(s, img, 7.75, 1.25, 5.1, 3.5, name="cover_image")

    _, tf = _tx(s, M, 1.05, 6.45, 0.3, "cover_kicker")
    write(tf, [{"text": meta.get("course_line", ""), "size": 12.5,
                "color": C["brand"], "font": FONT_H, "bold": True}])

    _, tf = _tx(s, M, 1.5, 6.45, 2.2, "cover_title")
    write(tf, [{"text": d.get("title", ""), "size": 28, "color": C["ink"],
                "font": FONT_H, "bold": True, "line": 1.06}])
    _, tf = _tx(s, M, 3.62, 6.45, 0.6, "cover_subtitle")
    write(tf, [{"text": d.get("subtitle", ""), "size": 13.5, "color": C["muted"],
                "line": 1.25}])

    hline(s, M, 4.4, 3.0, C["line"], "cover_rule")

    _, tf = _tx(s, M, 4.62, 6.45, 1.5, "cover_meta")
    rows = d.get("meta_lines", [])
    write(tf, [{"text": r, "size": 13.5, "color": C["body"], "line": 1.45,
                "space_before": 0 if i == 0 else 3} for i, r in enumerate(rows)])

    _, tf = _tx(s, M, SH - 0.62, 8.0, 0.3, "cover_note")
    write(tf, [{"text": d.get("note", ""), "size": 10, "color": C["muted"]}])
    return s


def lay_agenda(prs, meta, d, n):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    y = head(s, d["title"], d.get("kicker"))
    items = d["items"]
    cols = 2
    cw = (CW - 0.4) / cols
    ch = 0.95
    for i, it in enumerate(items):
        r, c = divmod(i, cols)
        x = M + c * (cw + 0.4)
        yy = y + 0.15 + r * (ch + 0.28)
        box(s, x, yy, cw, ch, fill=C["surface"], line=C["line"], radius=0.12,
            name=f"agenda_{i+1}")
        _, tf = _tx(s, x + 0.28, yy + 0.16, 0.7, 0.6, f"agenda_num_{i+1}")
        write(tf, [{"text": f"{i+1:02d}", "size": 26, "color": C["ghost"],
                    "font": FONT_H, "bold": True}])
        _, tf = _tx(s, x + 1.05, yy + 0.16, cw - 1.25, ch - 0.32, f"agenda_txt_{i+1}")
        write(tf, [{"text": it["text"], "size": 15.5, "color": C["ink"],
                    "font": FONT_H, "bold": True, "line": 1.05},
                   {"text": it.get("sub", ""), "size": 12, "color": C["muted"],
                    "space_before": 2}])
    foot(s, meta, n)
    return s


def lay_kpi(prs, meta, d, n):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    y = head(s, d["title"], d.get("kicker"))
    if d.get("lead"):
        _, tf = _tx(s, M, y - 0.04, CW, 0.5, "lead")
        write(tf, [{"text": d["lead"], "size": 14.5, "color": C["body"], "line": 1.25}])
        y += 0.62
    items = d["items"]
    cw = (CW - (len(items) - 1) * 0.35) / len(items)
    for i, it in enumerate(items):
        x = M + i * (cw + 0.35)
        box(s, x, y, cw, 2.5, fill=C["white"], line=C["line"], radius=0.10,
            name=f"kpi_{i+1}")
        _, tf = _tx(s, x + 0.32, y + 0.28, cw - 0.64, 0.9, f"kpi_num_{i+1}")
        write(tf, [{"text": it["value"], "size": 38, "color": C["brand"],
                    "font": FONT_H, "bold": True}])
        hline(s, x + 0.32, y + 1.24, cw - 0.64, C["line"], f"kpi_rule_{i+1}")
        _, tf = _tx(s, x + 0.32, y + 1.42, cw - 0.64, 1.0, f"kpi_lbl_{i+1}")
        write(tf, [{"text": it["label"], "size": 13, "color": C["ink"],
                    "line": 1.2}])
    if d.get("source"):
        _, tf = _tx(s, M, y + 2.72, CW, 0.3, "source")
        write(tf, [{"text": d["source"], "size": 10, "color": C["muted"],
                    "italic": True}])
    foot(s, meta, n)
    return s


def lay_cards(prs, meta, d, n):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    y = head(s, d["title"], d.get("kicker"))
    if d.get("lead"):
        _, tf = _tx(s, M, y - 0.04, CW, 0.5, "lead")
        write(tf, [{"text": d["lead"], "size": 14.5, "color": C["body"], "line": 1.25}])
        y += 0.6
    items = d["items"]
    cw = (CW - (len(items) - 1) * 0.4) / len(items)
    for i, it in enumerate(items):
        x = M + i * (cw + 0.4)
        box(s, x, y, cw, 3.5, fill=C["surface"], line=C["line"], radius=0.10,
            name=f"card_{i+1}")
        _, tf = _tx(s, x + 0.3, y + 0.22, cw - 0.6, 0.7, f"card_num_{i+1}")
        write(tf, [{"text": f"{i+1:02d}", "size": 30, "color": C["ghost"],
                    "font": FONT_H, "bold": True}])
        _, tf = _tx(s, x + 0.3, y + 0.95, cw - 0.6, 0.7, f"card_head_{i+1}")
        write(tf, [{"text": it["title"], "size": 16, "color": C["ink"],
                    "font": FONT_H, "bold": True, "line": 1.08}])
        _, tf = _tx(s, x + 0.3, y + 1.72, cw - 0.6, 1.6, f"card_body_{i+1}")
        write(tf, [{"text": it["body"], "size": 13.5, "color": C["body"],
                    "line": 1.32}])
    foot(s, meta, n)
    return s


def lay_flow(prs, meta, d, n):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    y = head(s, d["title"], d.get("kicker"))
    if d.get("lead"):
        _, tf = _tx(s, M, y - 0.04, CW, 0.5, "lead")
        write(tf, [{"text": d["lead"], "size": 14.5, "color": C["body"], "line": 1.25}])
        y += 0.6
    steps = d["steps"]
    k = len(steps)
    gap = 0.3
    cw = (CW - (k - 1) * gap) / k
    tints = [C["brand_soft"], C["brand_soft"], C["surface"], C["surface"]]
    for i, st in enumerate(steps):
        x = M + i * (cw + gap)
        box(s, x, y + 0.35, cw, 2.3, fill=tints[i % len(tints)], line=C["line"],
            radius=0.12, name=f"flow_{i+1}")
        _, tf = _tx(s, x + 0.2, y + 0.5, cw - 0.4, 0.35, f"flow_num_{i+1}")
        write(tf, [{"text": f"Bước {i+1}", "size": 11, "color": C["brand"],
                    "font": FONT_H, "bold": True}])
        _, tf = _tx(s, x + 0.2, y + 0.88, cw - 0.4, 1.5, f"flow_txt_{i+1}")
        write(tf, [{"text": st["text"], "size": 13.5, "color": C["ink"],
                    "bold": True, "line": 1.15},
                   {"text": st.get("sub", ""), "size": 11.5, "color": C["muted"],
                    "space_before": 3, "line": 1.2}])
        if i < k - 1:
            ar = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + cw + 0.03),
                                    Inches(y + 1.32), Inches(gap - 0.06), Inches(0.22))
            ar.name = f"flow_arrow_{i+1}"
            ar.fill.solid()
            ar.fill.fore_color.rgb = _rgb(C["line"])
            ar.line.fill.background()
            ar.shadow.inherit = False
    foot(s, meta, n)
    return s


def lay_bullets(prs, meta, d, n):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    y = head(s, d["title"], d.get("kicker"))
    if d.get("lead"):
        _, tf = _tx(s, M, y - 0.04, CW, 0.5, "lead")
        write(tf, [{"text": d["lead"], "size": 14.5, "color": C["body"], "line": 1.25}])
        y += 0.6
    items = d["items"]
    _bullet_rows(s, M + 0.1, y + 0.1, CW - 0.2, items, size=15.5, gap=0.12)
    foot(s, meta, n)
    return s


def lay_split(prs, meta, d, n):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    y = head(s, d["title"], d.get("kicker"))
    lw = CW * 0.44
    rw = CW - lw - 0.45
    if d.get("lead"):
        _, tf = _tx(s, M, y - 0.04, lw, 0.7, "lead")
        write(tf, [{"text": d["lead"], "size": 14, "color": C["body"], "line": 1.25}])
        y += 0.72
    _bullet_rows(s, M + 0.1, y + 0.05, lw - 0.1, d["items"], size=14, gap=0.10)
    picture(s, d["image"], M + lw + 0.45, y - 0.05, rw, 3.9, name="split_img")
    if d.get("caption"):
        _, tf = _tx(s, M + lw + 0.45, y + 3.95, rw, 0.3, "caption")
        write(tf, [{"text": d["caption"], "size": 10.5, "color": C["muted"],
                    "italic": True, "align": PP_ALIGN.CENTER}])
    foot(s, meta, n)
    return s


def lay_table(prs, meta, d, n):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    y = head(s, d["title"], d.get("kicker"))
    if d.get("lead"):
        _, tf = _tx(s, M, y - 0.04, CW, 0.5, "lead")
        write(tf, [{"text": d["lead"], "size": 14.5, "color": C["body"], "line": 1.25}])
        y += 0.56
    cols = d["columns"]
    rows = d["rows"]
    ncol = len(cols)
    nrow = len(rows) + 1
    avail_h = SH - 0.75 - y
    tbl_h = min(avail_h, 0.42 + 0.46 * len(rows))
    shp = s.shapes.add_table(nrow, ncol, Inches(M), Inches(y), Inches(CW),
                             Inches(tbl_h))
    tbl = shp.table
    tbl.first_row = False
    tbl.horz_banding = False
    shp.name = "table_main"
    widths = d.get("widths")
    if widths:
        tot = sum(widths)
        for i, wv in enumerate(widths):
            tbl.columns[i].width = Emu(int(Inches(CW) * wv / tot))
    fs = d.get("font_size", 12.5)
    for j, ctitle in enumerate(cols):
        cell = tbl.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = _rgb(C["brand_soft"])
        cell.margin_left = cell.margin_right = Inches(0.09)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        write(cell.text_frame, [{"text": ctitle, "size": fs, "color": C["ink"],
                                 "font": FONT_H, "bold": True}])
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = tbl.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = _rgb(C["white"] if i % 2 == 0 else C["surface"])
            cell.margin_left = cell.margin_right = Inches(0.09)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            write(cell.text_frame, [{"text": str(val), "size": fs,
                                     "color": C["body"],
                                     "bold": (j == 0 and d.get("bold_first", True))}])
    if d.get("caption"):
        _, tf = _tx(s, M, y + tbl_h + 0.12, CW, 0.3, "caption")
        write(tf, [{"text": d["caption"], "size": 10.5, "color": C["muted"],
                    "italic": True}])
    foot(s, meta, n)
    return s


def lay_compare(prs, meta, d, n):
    """Trang nhieu chu: 2 phuong an, moi phuong an co khoi Uu diem / Nhuoc diem mau nhat."""
    s = prs.slides.add_slide(prs.slide_layouts[6])
    y = head(s, d["title"], d.get("kicker"))
    if d.get("lead"):
        _, tf = _tx(s, M, y - 0.04, CW, 0.5, "lead")
        write(tf, [{"text": d["lead"], "size": 14, "color": C["body"], "line": 1.25}])
        y += 0.58
    plans = d["plans"]
    gap = 0.45
    cw = (CW - gap) / len(plans)
    for i, pl in enumerate(plans):
        x = M + i * (cw + gap)
        box(s, x, y, cw, 0.52, fill=C["brand_dk"], line=None, radius=0.14,
            name=f"cmp_head_{i+1}", shadow=False)
        _, tf = _tx(s, x + 0.2, y + 0.1, cw - 0.4, 0.34, f"cmp_head_txt_{i+1}")
        write(tf, [{"text": pl["name"], "size": 15, "color": C["white"],
                    "font": FONT_H, "bold": True}])
        yy = y + 0.66
        for tag, key, tone, soft in (("Ưu điểm", "pros", C["good"], C["good_soft"]),
                                     ("Nhược điểm", "cons", C["bad"], C["bad_soft"])):
            items = pl.get(key, [])
            bh = 0.34 + 0.30 * len(items) + 0.1
            box(s, x, yy, cw, bh, fill=soft, line=None, radius=0.10,
                name=f"cmp_{key}_{i+1}")
            _, tf = _tx(s, x + 0.18, yy + 0.1, cw - 0.36, 0.26, f"cmp_{key}_lbl_{i+1}")
            write(tf, [{"text": tag, "size": 12.5, "color": tone, "font": FONT_H,
                        "bold": True}])
            _bullet_rows(s, x + 0.2, yy + 0.4, cw - 0.4, items, size=12,
                         gap=0.0, text_color=C["body"], marker_color=tone)
            yy += bh + 0.18
    foot(s, meta, n)
    return s


def lay_chips(prs, meta, d, n):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    y = head(s, d["title"], d.get("kicker"))
    if d.get("lead"):
        _, tf = _tx(s, M, y - 0.04, CW, 0.5, "lead")
        write(tf, [{"text": d["lead"], "size": 14.5, "color": C["body"], "line": 1.25}])
        y += 0.6
    items = d["items"]
    cols = d.get("cols", 7)
    gap = 0.16
    cw = (CW - (cols - 1) * gap) / cols
    ch = d.get("chip_height", 0.78)
    for i, it in enumerate(items):
        r, c = divmod(i, cols)
        x = M + c * (cw + gap)
        yy = y + 0.1 + r * (ch + 0.18)
        new = it.get("new")
        box(s, x, yy, cw, ch, fill=(C["brand_soft"] if new else C["surface"]),
            line=C["line"], radius=0.16, name=f"chip_{i+1}")
        _, tf = _tx(s, x + 0.08, yy + 0.08, cw - 0.16, 0.3, f"chip_code_{i+1}")
        write(tf, [{"text": it["code"], "size": 13, "color": C["brand"],
                    "font": FONT_H, "bold": True, "align": PP_ALIGN.CENTER}])
        _, tf = _tx(s, x + 0.08, yy + 0.36, cw - 0.16, ch - 0.42, f"chip_txt_{i+1}")
        write(tf, [{"text": it["text"], "size": 9.5, "color": C["body"],
                    "line": 1.1, "align": PP_ALIGN.CENTER}])
    if d.get("legend"):
        _, tf = _tx(s, M, SH - 0.95, CW, 0.3, "legend")
        write(tf, [{"text": d["legend"], "size": 10.5, "color": C["muted"],
                    "italic": True}])
    foot(s, meta, n)
    return s


def lay_diagram(prs, meta, d, n):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    y = head(s, d["title"], d.get("kicker"))
    if d.get("lead"):
        _, tf = _tx(s, M, y - 0.04, CW, 0.5, "lead")
        write(tf, [{"text": d["lead"], "size": 14, "color": C["body"], "line": 1.25}])
        y += 0.5
    cap_h = 0.34 if d.get("caption") else 0.0
    picture(s, d["image"], M, y, CW, SH - 0.75 - y - cap_h, name="diagram",
            frame=False)
    if d.get("caption"):
        _, tf = _tx(s, M, SH - 0.78, CW, 0.3, "caption")
        write(tf, [{"text": d["caption"], "size": 10.5, "color": C["muted"],
                    "italic": True, "align": PP_ALIGN.CENTER}])
    foot(s, meta, n)
    return s


def lay_section(prs, meta, d, n):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    box(s, 0, 0, SW, SH, fill=C["brand_dk"], line=None, radius=0.0, name="section_bg")
    box(s, M, 2.4, 0.11, 2.0, fill=C["brand_soft"], line=None, radius=0.4,
        name="section_mark")
    _, tf = _tx(s, M + 0.5, 2.35, CW - 1.0, 0.5, "section_kicker")
    write(tf, [{"text": d.get("kicker", ""), "size": 14, "color": C["brand_soft"],
                "font": FONT_H, "bold": True}])
    _, tf = _tx(s, M + 0.5, 2.85, CW - 1.0, 1.1, "section_title")
    write(tf, [{"text": d["title"], "size": 30, "color": C["white"], "font": FONT_H,
                "bold": True, "line": 1.1}])
    if d.get("lead"):
        _, tf = _tx(s, M + 0.5, 4.0, CW - 2.5, 0.8, "section_lead")
        write(tf, [{"text": d["lead"], "size": 14, "color": C["brand_soft"],
                    "line": 1.3}])
    return s


def lay_closing(prs, meta, d, n):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    box(s, 0, 0, SW, SH, fill=C["white"], line=None, radius=0.0, name="bg")
    box(s, 0, 0, SW, 0.22, fill=C["brand"], line=None, radius=0.0, name="top_band")
    _, tf = _tx(s, M, 2.35, CW, 1.0, "close_title")
    write(tf, [{"text": d["title"], "size": 30, "color": C["ink"], "font": FONT_H,
                "bold": True, "align": PP_ALIGN.CENTER}])
    if d.get("lead"):
        _, tf = _tx(s, M + 1.5, 3.5, CW - 3.0, 0.7, "close_lead")
        write(tf, [{"text": d["lead"], "size": 14.5, "color": C["body"],
                    "align": PP_ALIGN.CENTER, "line": 1.3}])
    if d.get("meta_lines"):
        _, tf = _tx(s, M, 4.5, CW, 1.0, "close_meta")
        write(tf, [{"text": r, "size": 12.5, "color": C["muted"],
                    "align": PP_ALIGN.CENTER, "space_before": 0 if i == 0 else 3}
                   for i, r in enumerate(d["meta_lines"])])
    foot(s, meta, n)
    return s


LAYOUTS = {
    "cover": lay_cover, "agenda": lay_agenda, "kpi": lay_kpi, "cards": lay_cards,
    "flow": lay_flow, "bullets": lay_bullets, "split": lay_split,
    "table": lay_table, "compare": lay_compare, "chips": lay_chips,
    "diagram": lay_diagram, "section": lay_section, "closing": lay_closing,
}

BLANK = {
    "meta": {"footer": "Đồ án · Phân tích bài toán", "course_line": "Môn học"},
    "slides": [
        {"layout": "cover", "title": "[Tên đề tài]", "subtitle": "[Mô tả một dòng]",
         "meta_lines": ["Giảng viên hướng dẫn: [điền]", "Sinh viên: [điền]"]},
        {"layout": "section", "kicker": "Chương X", "title": "[Tên chương]",
         "lead": "[Một câu dẫn]"},
        {"layout": "bullets", "title": "[Tiêu đề khẳng định]", "items": ["[Ý 1]", "[Ý 2]"]},
    ],
}


def build(spec, out):
    meta = spec.get("meta", {})
    prs = Presentation()
    prs.slide_width = Inches(SW)
    prs.slide_height = Inches(SH)
    for i, d in enumerate(spec["slides"], start=1):
        lay = LAYOUTS.get(d["layout"])
        if not lay:
            raise SystemExit(f"Layout khong ho tro: {d['layout']}")
        slide = lay(prs, meta, d, i)
        if d.get("notes"):
            tf = slide.notes_slide.notes_text_frame
            tf.text = d["notes"]
    prs.save(out)
    return len(spec["slides"])


def main():
    ap = argparse.ArgumentParser(description="Sinh deck .pptx phan tich bai toan")
    ap.add_argument("--spec", help="file JSON noi dung")
    ap.add_argument("--out", required=True, help="file .pptx dau ra")
    ap.add_argument("--blank", action="store_true", help="khung rong 3 slide mau")
    a = ap.parse_args()
    if a.blank:
        spec = BLANK
    else:
        if not a.spec:
            raise SystemExit("Can --spec hoac --blank")
        with open(a.spec, encoding="utf-8") as f:
            spec = json.load(f)
    n = build(spec, a.out)
    print(f"OK  {a.out}  ({n} slide)")


if __name__ == "__main__":
    main()
