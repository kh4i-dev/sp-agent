#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
inspect_deck.py — kiem tra nhanh deck .pptx truoc khi render:
  - dem slide, so tu moi slide (canh bao "qua nhieu chu" > 45 tu)
  - con sot placeholder ([dien] / TODO / xxx / lorem / ...)
  - font khong an toan khi render
  - uoc luong TRAN CHU (heuristic: chieu cao chu > chieu cao khung)
  - slide khong co anh/so do (canh bao slide "chi co chu")
  - thieu speaker notes

    python inspect_deck.py deck.pptx
Tra ve exit code 1 neu co loi (placeholder / tran chu / sai font).
"""
from __future__ import annotations

import argparse
import math
import sys

from pptx import Presentation
from pptx.util import Emu

SAFE_FONTS = {"Arial", "Calibri", "Cambria", "Times New Roman",
              "Segoe UI", "Verdana", "Tahoma", "Georgia"}
BAD = ["[điền]", "[dien]", "todo", "tbd", "lorem", "xxx", "placeholder",
       "{{", "}}", "<điền>"]

# Gioi han tu theo layout (slide van xuoi giu chat 45; bang/so sanh duoc noi).
WORD_CAP = {"cover": 55, "agenda": 65, "kpi": 65, "cards": 78, "flow": 85,
            "bullets": 55, "split": 60, "table": 130, "compare": 140,
            "chips": 105, "diagram": 55, "section": 35, "closing": 40}
CHROME = {"footer", "pageno"}  # khong tinh vao so tu noi dung


def walk(shapes):
    for sh in shapes:
        if sh.shape_type == 6:  # GROUP
            yield from walk(sh.shapes)
        else:
            yield sh


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx")
    ap.add_argument("--spec", help="spec JSON -> lay gioi han tu theo tung layout")
    ap.add_argument("--max-words", type=int, default=None,
                    help="ghi de gioi han tu cho moi slide")
    a = ap.parse_args()

    layouts = []
    if a.spec:
        import json
        with open(a.spec, encoding="utf-8") as f:
            layouts = [s["layout"] for s in json.load(f)["slides"]]

    prs = Presentation(a.pptx)
    errors, warns = [], []
    for i, slide in enumerate(prs.slides, start=1):
        words = 0
        pics = 0
        for sh in walk(slide.shapes):
            if sh.shape_type == 13 or sh.__class__.__name__ == "Picture":
                pics += 1
            if not sh.has_text_frame:
                continue
            if sh.name in CHROME:
                continue
            for p in sh.text_frame.paragraphs:
                txt = "".join(r.text for r in p.runs)
                words += len(txt.split())
                low = txt.lower()
                for b in BAD:
                    if b in low:
                        errors.append(f"slide {i}: con placeholder '{b}' -> '{txt[:50]}'")
                for r in p.runs:
                    fn = r.font.name
                    if fn and fn not in SAFE_FONTS:
                        warns.append(f"slide {i}: font '{fn}' khong an toan khi render")
                    size = (r.font.size or 0)
                    if size and size.pt < 9:
                        warns.append(f"slide {i}: co chu {size.pt:.0f}pt qua nho")
            # uoc luong tran chu
            tf = sh.text_frame
            box_h = Emu(sh.height).inches
            box_w = Emu(sh.width).inches
            needed = 0.0
            for p in tf.paragraphs:
                t = "".join(r.text for r in p.runs)
                if not t.strip():
                    continue
                size = next((r.font.size.pt for r in p.runs if r.font.size), 15)
                cpl = max(6, int(box_w / (size * 0.0072)))  # ky tu / dong (uoc luong)
                lines = max(1, math.ceil(len(t) / cpl))
                needed += lines * size * 1.28 / 72
            if box_h > 0.1 and needed > box_h + 0.22:
                warns.append(f"slide {i}: nghi TRAN CHU o '{sh.name}' "
                             f"(can ~{needed:.1f}\" / khung {box_h:.1f}\")")
        notes = slide.notes_slide.notes_text_frame.text.strip() if slide.has_notes_slide else ""
        if not notes:
            warns.append(f"slide {i}: thieu speaker notes")
        cap = a.max_words
        if cap is None:
            lay = layouts[i - 1] if i - 1 < len(layouts) else "bullets"
            cap = WORD_CAP.get(lay, 45)
        if words > cap:
            warns.append(f"slide {i}: {words} tu (> {cap}) — cat bot")
        if pics == 0:
            warns.append(f"slide {i}: khong co anh/so do (slide chi toan chu)")

    print(f"Slides: {len(prs.slides._sldIdLst)}")
    print(f"Loi : {len(errors)}   Canh bao: {len(warns)}")
    for e in errors:
        print("  [LOI ]", e)
    for w in warns:
        print("  [CANH]", w)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
