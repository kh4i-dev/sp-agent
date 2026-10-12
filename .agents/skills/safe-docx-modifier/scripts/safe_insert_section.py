#!/usr/bin/env python3
"""
safe_insert_section.py — Chèn đoạn văn/bảng mới tại mốc neo (Anchor) in-place trong file Word (.docx)
Không tái tạo (Zero Regeneration): Định vị chính xác phần tử XML của đoạn neo (anchor paragraph)
và chèn phần tử mới vào ngay sau đó mà không làm ảnh hưởng đến 99% còn lại của tài liệu.
"""
import argparse
import os
import shutil
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'xml': 'http://www.w3.org/XML/1998/namespace'
}


def create_paragraph_element(text: str, style: str = None, bold: bool = False, italic: bool = False):
    """Tạo một phần tử w:p XML hợp lệ theo chuẩn OpenXML."""
    p = ET.Element(f"{{{NS['w']}}}p")
    pPr = ET.SubElement(p, f"{{{NS['w']}}}pPr")
    if style:
        pStyle = ET.SubElement(pPr, f"{{{NS['w']}}}pStyle")
        pStyle.set(f"{{{NS['w']}}}val", style)

    r = ET.SubElement(p, f"{{{NS['w']}}}r")
    rPr = ET.SubElement(r, f"{{{NS['w']}}}rPr")
    if bold:
        ET.SubElement(rPr, f"{{{NS['w']}}}b")
    if italic:
        ET.SubElement(rPr, f"{{{NS['w']}}}i")

    t = ET.SubElement(r, f"{{{NS['w']}}}t")
    t.text = text
    if text.startswith(" ") or text.endswith(" "):
        t.set(f"{{{NS['xml']}}}space", "preserve")

    return p


def insert_after_anchor(
    docx_path: str,
    anchor_text: str,
    content_text: str,
    style: str = None,
    bold: bool = False,
    italic: bool = False,
    out_docx_path: str = None
):
    docx_path = Path(docx_path).resolve()
    if not docx_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {docx_path}")

    if out_docx_path is None:
        out_docx_path = docx_path
    else:
        out_docx_path = Path(out_docx_path).resolve()

    temp_dir = tempfile.mkdtemp(prefix="docx_insert_")
    try:
        with zipfile.ZipFile(str(docx_path), 'r') as z:
            z.extractall(temp_dir)

        doc_xml_path = Path(temp_dir) / 'word' / 'document.xml'
        tree = ET.parse(str(doc_xml_path))
        root = tree.getroot()
        body = root.find('.//w:body', NS)
        if body is None:
            raise ValueError("Không tìm thấy w:body trong document.xml")

        # Tìm vị trí anchor trong body
        anchor_idx = -1
        for idx, child in enumerate(body):
            if child.tag == f"{{{NS['w']}}}p":
                full_text = "".join(child.itertext()).strip()
                if anchor_text in full_text:
                    anchor_idx = idx
                    print(f"🎯 Đã tìm thấy mốc neo tại phần tử [{idx}]: '{full_text[:50]}...'")
                    break

        if anchor_idx == -1:
            print(f"❌ Không tìm thấy mốc neo chứa: '{anchor_text}'")
            return False

        # Tạo phần tử paragraph mới và chèn ngay sau anchor_idx
        new_p = create_paragraph_element(content_text, style=style, bold=bold, italic=italic)
        body.insert(anchor_idx + 1, new_p)

        # Lưu lại XML
        tree.write(str(doc_xml_path), encoding='utf-8', xml_declaration=True)

        # Tạo backup an toàn
        backup_path = str(docx_path) + ".bak_safe"
        if not os.path.exists(backup_path):
            shutil.copyfile(str(docx_path), backup_path)

        # Đóng gói DOCX
        with zipfile.ZipFile(str(out_docx_path), 'w', zipfile.ZIP_DEFLATED) as z_out:
            for foldername, subfolders, filenames in os.walk(temp_dir):
                for filename in filenames:
                    filepath = os.path.join(foldername, filename)
                    arcname = os.path.relpath(filepath, temp_dir)
                    z_out.write(filepath, arcname)

        print(f"✅ Đã chèn thành công nội dung mới vào sau mốc neo: {out_docx_path}")
        return True

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="Chèn nội dung mới an toàn sau mốc neo trong file Word (.docx)")
    parser.add_argument("docx", help="Đường dẫn file Word (.docx)")
    parser.add_argument("--anchor", required=True, help="Chuỗi văn bản của đoạn mốc cần chèn ngay sau nó")
    parser.add_argument("--content", required=True, help="Nội dung văn bản cần chèn")
    parser.add_argument("--style", help="Tên Style Word (VD: Normal, Heading1)")
    parser.add_argument("--bold", action="store_true", help="In đậm nội dung chèn")
    parser.add_argument("--italic", action="store_true", help="In nghiêng nội dung chèn")
    parser.add_argument("-o", "--output", help="Đường dẫn file xuất ra")

    args = parser.parse_args()

    insert_after_anchor(
        args.docx,
        args.anchor,
        args.content,
        style=args.style,
        bold=args.bold,
        italic=args.italic,
        out_docx_path=args.output
    )


if __name__ == "__main__":
    main()
