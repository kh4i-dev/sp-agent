#!/usr/bin/env python3
"""Che SDT trong anh dau (minh chung lua dao) - giu nguyen kich thuoc de swap in-place."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SRC = Path(r"C:\Users\My PC\AppData\Local\Temp\opencode\docxzip\word\media\image2.png")
DST = Path(r"C:\Users\My PC\AppData\Local\Temp\opencode\anh-dau-che.png")

im = Image.open(SRC).convert("RGB")
W, H = im.size
d = ImageDraw.Draw(im)
# Vung chua SDT "zalo 0396248644" nam giua cot noi dung (uoc luong rong, se hien preview de duyet)
x0, y0, x1, y1 = int(W*0.375), int(H*0.432), int(W*0.55), int(H*0.46)
d.rectangle([x0, y0, x1, y1], fill=(30, 30, 30))
try:
    fnt = ImageFont.truetype("arial.ttf", size=max(14, int(H*0.018)))
except Exception:
    fnt = ImageFont.load_default()
d.text((x0+8, y0+4), "[Da che SDT]", fill=(255, 255, 255), font=fnt)
im.save(DST)
print(f"saved {DST} size={im.size} box={[x0,y0,x1,y1]}")
