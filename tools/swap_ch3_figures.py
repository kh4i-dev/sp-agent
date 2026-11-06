#!/usr/bin/env python3
"""Thay 8 anh chuong 3: swap deployment/RBAC + xoa ERD/Class cu + chen 6 hinh moi.
Giu field SEQ/REF/TOF con song (clone caption, bookmark id duy nhat).
Dat trong tools/ theo ky luat Dedicated Tools Directory.
"""
import copy
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

SRC = r"C:\Users\MYPC~1\AppData\Local\Temp\opencode\DA_SUA_swapped.docx"
DST = r"C:\Users\MYPC~1\AppData\Local\Temp\opencode\DA_SUA_fig.docx"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
QN = lambda t: "{%s}%s" % (W, t)

NEWFIGS = [
    ("erd_a_identity.png", "Sơ đồ quan hệ thực thể: định danh và hồ sơ gia sư"),
    ("erd_b_connection.png", "Sơ đồ quan hệ thực thể: kết nối và tin nhắn"),
    ("erd_c_trust.png", "Sơ đồ quan hệ thực thể: đánh giá và báo cáo"),
    ("class_a_identity.png", "Sơ đồ lớp: tài khoản và hồ sơ gia sư"),
    ("class_b_connection.png", "Sơ đồ lớp: kết nối và hội thoại"),
    ("class_c_trust.png", "Sơ đồ lớp: đánh giá và báo cáo"),
]
DP = "E:/HOC TAP/my-project/ecosystem_ketnoi_giasu/docs/diagrams/"

doc = Document(SRC)
rels = {r.rId: (r.target_ref or "") for r in doc.part.rels.values()}

def media_of(p):
    for d in p._p.findall(".//{%s}drawing" % W):
        for b in d.findall(".//{http://schemas.openxmlformats.org/drawingml/2006/main}blip"):
            rid = b.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")
            ref = rels.get(rid, "")
            if "media/" in ref:
                return ref.split("/")[-1]
    return None

def is_cap(p):
    return p.text.strip().startswith("Hình")

# 1. dinh vi fig image21/image22 + caption ke sau
paras = doc.paragraphs
targets = {}
for i, p in enumerate(paras):
    m = media_of(p)
    if m in ("image21.png", "image22.png"):
        # caption la doan ke tiep bat dau bang Hinh
        j = i + 1
        while j < len(paras) and not paras[j].text.strip():
            j += 1
        assert is_cap(paras[j]), (m, paras[j].text[:40])
        targets[m] = (i, j)
assert set(targets) == {"image21.png", "image22.png"}, targets
print("targets:", targets)

# 2. template caption = caption ERD cu (se copy)
tpl = paras[targets["image21.png"][1]]._p

# max bookmark id
maxid = 0
for el in doc.element.iter():
    if el.tag.endswith("}bookmarkStart"):
        try:
            maxid = max(maxid, int(el.get(QN("id"))))
        except (TypeError, ValueError):
            pass

def clone_caption(title, tag):
    global maxid
    el = copy.deepcopy(tpl)
    # rename bookmarks
    for b in el.iter():
        if b.tag.endswith("}bookmarkStart"):
            maxid += 1
            nm = b.get(QN("name"))
            if nm.startswith("_Ref"):
                b.set(QN("name"), "_Ref_Hinh3%s" % tag)
            elif nm.startswith("_Toc"):
                b.set(QN("name"), "_Toc3%s" % tag)
            b.set(QN("id"), str(maxid))
        elif b.tag.endswith("}bookmarkEnd"):
            maxid += 1
            b.set(QN("id"), str(maxid))
    # thay title: text runs o depth 0 sau field SEQ (bo qua STYLEREF dung truoc)
    depth = 0
    seen_seq = False
    seen_end = False
    done = False
    for r in el.findall(QN("r")):
        fc = r.find(QN("fldChar"))
        if fc is not None:
            t = fc.get(QN("fldCharType"))
            if t == "begin":
                depth += 1
            elif t == "end":
                depth -= 1
                if seen_seq and depth == 0:
                    seen_end = True
            continue
        it = r.find(QN("instrText"))
        if it is not None:
            if it.text and "SEQ" in it.text:
                seen_seq = True
            continue
        if seen_end and depth == 0 and not done:
            t = r.find(QN("t"))
            if t is not None:
                t.text = ": " + title
                done = True
        elif seen_end and depth == 0 and done:
            t = r.find(QN("t"))
            if t is not None:
                t.text = ""
    assert done, "khong thay duoc title"
    return el

# 3. tao fig paras (add cuoi roi move): can giu thu tu chen
anchor = paras[targets["image21.png"][0]]._p  # chen sau khi xoa? giu anchor truoc khi xoa
# luu anchor la previous sibling con song: doan text truoc fig ERD cu
prev = anchor.getprevious()
assert prev is not None

# 4. xoa 4 doan cu (fig+cap ERD, fig+cap Class) - xoa tu duoi len
for m in ("image22.png", "image21.png"):
    i, j = targets[m]
    for idx in sorted((i, j), reverse=True):
        paras[idx]._p.getparent().remove(paras[idx]._p)

# 5. chen 6 cap moi sau prev
from docx.oxml import OxmlElement
cur = prev
for k, (fn, title) in enumerate(NEWFIGS):
    # fig para
    fp = OxmlElement("w:p")
    pPr = OxmlElement("w:pPr")
    jc = OxmlElement("w:jc")
    jc.set(QN("val"), "center")
    pPr.append(jc)
    keep = OxmlElement("w:keepNext")
    pPr.append(keep)
    fp.append(pPr)
    cur.addnext(fp)
    # dung python-docx de chen anh vao fp thong qua Paragraph wrapper tam
    from docx.text.paragraph import Paragraph
    pw = Paragraph(fp, doc)
    pw.add_run().add_picture(DP + fn, width=Inches(6.0))
    cur = fp
    cap = clone_caption(title, "N%d" % k)
    cur.addnext(cap)
    cur = cap

doc.save(DST)
print("saved", DST)
