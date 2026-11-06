#!/usr/bin/env python3
"""Chuyen field TOF/TOT tu cuoi tai lieu len sau cac Heading DANH MUC o dau (an toan, lxml)."""
import copy
from docx import Document

SRC = r"C:\Users\MYPC~1\AppData\Local\Temp\opencode\BAO_CAO_PTTKHT_fix3.docx"
DST = r"C:\Users\MYPC~1\AppData\Local\Temp\opencode\BAO_CAO_PTTKHT_fix4.docx"

doc = Document(SRC)
ps = doc.paragraphs
assert ps[184].text.strip().startswith("DANH M"), ps[184].text
assert ps[185].text.strip().startswith("DANH M"), ps[185].text
assert ps[612].text.strip().startswith("DANH M"), ps[612].text
assert ps[614].text.strip().startswith("DANH M"), ps[614].text
assert "TOC" in ps[613]._p.xml, "613 khong phai TOF"
assert "TOC" in ps[615]._p.xml, "615 khong phai TOT"

anchor_hinh = ps[184]._p
anchor_bang = ps[185]._p
tof = copy.deepcopy(ps[613]._p)
tot = copy.deepcopy(ps[615]._p)

anchor_hinh.addnext(tof)
anchor_bang.addnext(tot)
# Xoa ban goc o cuoi (nguoc tu duoi len)
for idx in (615, 614, 613, 612):
    el = ps[idx]._p
    el.getparent().remove(el)

doc.save(DST)
# verify
d2 = Document(DST)
texts = [p.text.strip() for p in d2.paragraphs if p.text.strip().startswith("DANH M")]
print("DANH MUC con lai:", len(texts))
for t in texts:
    print("-", t[:40])
n_tof = sum(1 for p in d2.paragraphs if "TOC \\c" in p._p.xml or "TOC" in p._p.xml and "H\xecnh" in p.text)
print("OK saved", DST)
