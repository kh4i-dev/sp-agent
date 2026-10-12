#!/usr/bin/env python3
"""
verify_docx.py — Kiểm định tính toàn vẹn và thẩm định từ khóa cho file Word (.docx)
Kiểm tra:
1. Tính hợp lệ của cấu trúc tệp nén ZIP và OpenXML.
2. Cú pháp XML của toàn bộ các tệp cấu trúc (document.xml, styles.xml, rels, headers, footers).
3. Tính toàn vẹn của liên kết hình ảnh (Relationship Media Integrity).
4. Kiểm toán sự hiện diện / vắng mặt của các từ khóa mục tiêu (Keyword Audit Gate).
"""
import argparse
import os
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def verify_docx(docx_path: str, must_have: list = None, must_not_have: list = None):
    docx_path = Path(docx_path).resolve()
    if not docx_path.exists():
        print(f"❌ Không tìm thấy file: {docx_path}")
        return False

    print(f"\n🔍 BẮT ĐẦU KIỂM ĐỊNH TÍNH TOÀN VẸN FILE WORD: {docx_path.name}")
    print("=" * 80)

    # 1. Kiểm tra ZIP
    if not zipfile.is_zipfile(str(docx_path)):
        print("❌ LỖI: Tệp không phải là định dạng ZIP/DOCX hợp lệ!")
        return False
    print("✅ 1. Cấu trúc đóng gói ZIP hợp lệ.")

    # 2. Kiểm tra XML syntax toàn bộ tệp bên trong
    xml_errors = []
    text_contents = []
    media_files = set()
    referenced_media = set()

    with zipfile.ZipFile(str(docx_path), 'r') as z:
        namelist = z.namelist()
        for name in namelist:
            if name.startswith('word/media/'):
                media_files.add(os.path.basename(name))

            if name.endswith('.xml') or name.endswith('.rels'):
                try:
                    content = z.read(name)
                    root = ET.fromstring(content)
                    if name == 'word/document.xml':
                        text_contents.append(''.join(root.itertext()))
                    if name == 'word/_rels/document.xml.rels':
                        for rel in root:
                            target = rel.attrib.get('Target', '')
                            if target.startswith('media/'):
                                referenced_media.add(os.path.basename(target))
                except Exception as e:
                    xml_errors.append((name, str(e)))

    if xml_errors:
        print(f"❌ 2. Phát hiện {len(xml_errors)} tệp XML bị lỗi cú pháp:")
        for name, err in xml_errors:
            print(f"   • {name}: {err}")
        return False
    print("✅ 2. Toàn bộ các tệp cấu trúc XML đều Well-formed (Cú pháp chuẩn 100%).")

    # 3. Kiểm tra liên kết Media
    missing_media = referenced_media - media_files
    if missing_media:
        print(f"⚠️ 3. Cảnh báo: Có {len(missing_media)} ảnh được tham chiếu nhưng thiếu tệp binary:")
        for m in missing_media:
            print(f"   • Thiếu: {m}")
    else:
        print(f"✅ 3. Toàn bộ {len(referenced_media)} liên kết hình ảnh Media đều nguyên vẹn.")

    # 4. Kiểm toán từ khóa (Keyword Audit Gate)
    doc_text = " ".join(text_contents)
    audit_passed = True

    if must_have:
        print("\n📋 4. Kiểm toán từ khóa BẮT BUỘC CÓ (Must-have):")
        for kw in must_have:
            cnt = doc_text.count(kw)
            if cnt > 0:
                print(f"   ✅ '{kw}': Xuất hiện {cnt} lần.")
            else:
                print(f"   ❌ '{kw}': KHÔNG TÌM THẤY TRONG VĂN BẢN!")
                audit_passed = False

    if must_not_have:
        print("\n📋 5. Kiểm toán từ khóa BỊ CẤM / CẦN LOẠI BỎ (Must-not-have):")
        for kw in must_not_have:
            cnt = doc_text.count(kw)
            if cnt == 0:
                print(f"   ✅ '{kw}': Đã loại bỏ sạch (0 lần).")
            else:
                print(f"   ⚠️ '{kw}': Vẫn còn tồn tại {cnt} lần!")
                audit_passed = False

    print("=" * 80)
    if audit_passed:
        print("🎉 TÀI LIỆU HOÀN TOÀN ĐẠT TIÊU CHUẨN KIỂM ĐỊNH (PASSED)!\n")
    else:
        print("⚠️ TÀI LIỆU CẦN CHÚ Ý CÁC MỤC KIỂM TOÁN CHƯA ĐẠT TRÊN.\n")

    return audit_passed


def main():
    parser = argparse.ArgumentParser(description="Kiểm định tính toàn vẹn và từ khóa cho file DOCX")
    parser.add_argument("docx", help="Đường dẫn file Word (.docx)")
    parser.add_argument("--must-have", nargs="*", help="Danh sách từ khóa bắt buộc phải có")
    parser.add_argument("--must-not-have", nargs="*", help="Danh sách từ khóa không được xuất hiện")

    args = parser.parse_args()
    success = verify_docx(
        args.docx,
        must_have=args.must_have,
        must_not_have=args.must_not_have
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
