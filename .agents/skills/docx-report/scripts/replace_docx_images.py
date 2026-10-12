#!/usr/bin/env python3
"""
replace_docx_images.py — Công cụ thay thế ảnh siêu tốc và an toàn cho file Word (.docx)

Tính năng:
1. --list: Liệt kê toàn bộ hình ảnh trong file .docx (kèm rId, tên media trong zip, và Caption tương ứng).
2. --replace: Thay thế ảnh bằng phương pháp In-place ZIP Binary Swap:
   - Thay theo Caption (VD: --figure "Hình 3.2" --new "path/to/new.png")
   - Thay theo tên media (VD: --target "image4.png" --new "path/to/new.png")
   - Thay hàng loạt theo file JSON mapping (--mapping "map.json")
3. Bảo toàn 100% định dạng, style, bảng biểu, ngắt trang của file Word người dùng (KHÔNG regenerate).
4. Tự động cập nhật tỉ lệ khung hình (Aspect Ratio / wp:extent) tránh làm méo hình mới.
"""

import argparse
import json
import os
import shutil
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
}


def get_image_info_list(docx_path: str):
    """Quét và trích xuất danh sách tất cả hình ảnh cùng Caption tương ứng trong DOCX."""
    with zipfile.ZipFile(docx_path, 'r') as z:
        rels_xml = z.read('word/_rels/document.xml.rels')
        doc_xml = z.read('word/document.xml')

    rels_root = ET.fromstring(rels_xml)
    rid_to_target = {}
    for rel in rels_root:
        rid = rel.attrib.get('Id')
        target = rel.attrib.get('Target')
        if target and target.startswith('media/'):
            rid_to_target[rid] = target

    doc_root = ET.fromstring(doc_xml)
    paragraphs = doc_root.findall('.//w:p', NS)

    images = []
    seen_embeds = set()

    for idx, p in enumerate(paragraphs):
        blips = p.findall('.//a:blip', NS)
        for b in blips:
            embed = b.attrib.get(f"{{{NS['r']}}}embed")
            if not embed or embed in seen_embeds:
                continue
            seen_embeds.add(embed)

            target = rid_to_target.get(embed, 'Unknown')
            media_name = os.path.basename(target)

            # Lấy kích thước khung hình wp:extent (nếu có)
            extent = p.find('.//wp:extent', NS)
            cx = int(extent.attrib.get('cx', 0)) if extent is not None else 0
            cy = int(extent.attrib.get('cy', 0)) if extent is not None else 0

            # Tìm Caption ở đoạn kế tiếp hoặc chính đoạn này
            p_text = ''.join(p.itertext()).strip()
            caption = ''
            for offset in [1, 2, 0]:
                check_idx = idx + offset
                if 0 <= check_idx < len(paragraphs):
                    t = ''.join(paragraphs[check_idx].itertext()).strip()
                    if t.startswith(("Hình ", "Hình:", "HÌNH ", "Figure ")):
                        caption = t
                        break
            if not caption and idx + 1 < len(paragraphs):
                caption = ''.join(paragraphs[idx + 1].itertext()).strip()

            images.append({
                "rid": embed,
                "media_path": f"word/{target}",
                "media_name": media_name,
                "caption": caption,
                "cx": cx,
                "cy": cy
            })

    return images


def list_images(docx_path: str):
    images = get_image_info_list(docx_path)
    print(f"\n📂 Danh sách {len(images)} hình ảnh trong file: {os.path.basename(docx_path)}")
    print("=" * 80)
    for idx, img in enumerate(images, start=1):
        cap_preview = img['caption'][:65] + "..." if len(img['caption']) > 65 else img['caption']
        print(f"[{idx:2d}] Tệp: {img['media_name']:<15} | rId: {img['rid']:<6} | Caption: {cap_preview}")
    print("=" * 80)


def replace_images_in_docx(
    docx_path: str,
    replacements: dict,
    out_docx_path: str = None,
    update_aspect_ratio: bool = True
):
    """
    Thay thế ảnh an toàn trong docx.
    replacements: dict mapping giữa:
      - Media name (ví dụ 'image4.png') -> đường dẫn file ảnh mới
      - HOẶC Figure caption / số hiệu (ví dụ 'Hình 3.2' hoặc '3.2') -> đường dẫn file ảnh mới
    """
    docx_path = Path(docx_path).resolve()
    if not docx_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {docx_path}")

    if out_docx_path is None:
        out_docx_path = docx_path
    else:
        out_docx_path = Path(out_docx_path).resolve()

    images_info = get_image_info_list(str(docx_path))

    # Chuẩn hóa bảng mapping sang media_path đích
    resolved_map = {}  # "word/media/imageX.png" -> Path(new_img)

    for key, new_img in replacements.items():
        new_img_path = Path(new_img).resolve()
        if not new_img_path.exists():
            print(f"⚠️ Cảnh báo: File ảnh mới không tồn tại: {new_img_path}", flush=True)
            continue

        matched = False
        key_clean = key.strip()

        # 1. So khớp theo media_name
        for info in images_info:
            if key_clean.lower() in [info['media_name'].lower(), info['media_path'].lower()]:
                resolved_map[info['media_path']] = (new_img_path, info)
                matched = True
                break

        # 2. So khớp theo Caption hoặc số hiệu Hình (ví dụ 'Hình 3.2', '3.2')
        if not matched:
            for info in images_info:
                cap = info['caption']
                if key_clean.lower() in cap.lower() or f"hình {key_clean.lower()}" in cap.lower():
                    resolved_map[info['media_path']] = (new_img_path, info)
                    matched = True
                    break

        if not matched:
            print(f"⚠️ Không tìm thấy ảnh nào khớp với khóa: '{key}'", flush=True)

    if not resolved_map:
        print("❌ Không có ảnh nào được ánh xạ để thay thế.")
        return 0

    print(f"\n🔄 Bắt đầu thay thế {len(resolved_map)} hình ảnh...")
    for target_media, (new_path, info) in resolved_map.items():
        print(f"  • {info['media_name']} ({info['caption'][:40]}...) ➔ {new_path.name}")

    # Đọc và sửa file qua temp directory
    temp_dir = tempfile.mkdtemp(prefix="docx_img_replace_")
    try:
        with zipfile.ZipFile(str(docx_path), 'r') as z:
            z.extractall(temp_dir)

        # 1. Ghi đè file binary vào word/media/
        for target_media, (new_path, info) in resolved_map.items():
            dest_file = Path(temp_dir) / target_media
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(new_path), str(dest_file))

        # 2. Cập nhật tỷ lệ khung hình trong document.xml nếu cần
        if update_aspect_ratio:
            doc_xml_path = Path(temp_dir) / 'word' / 'document.xml'
            if doc_xml_path.exists():
                tree = ET.parse(str(doc_xml_path))
                root = tree.getroot()
                modified_xml = False

                for target_media, (new_path, info) in resolved_map.items():
                    rid = info['rid']
                    try:
                        with Image.open(str(new_path)) as im:
                            img_w, img_h = im.size
                            new_aspect = img_h / img_w
                    except Exception:
                        continue

                    # Tìm blip chứa rid này và cập nhật wp:extent
                    for p in root.findall('.//w:p', NS):
                        blip = p.find(f".//a:blip[@r:embed='{rid}']", NS)
                        if blip is not None:
                            extent = p.find('.//wp:extent', NS)
                            if extent is not None:
                                old_cx = int(extent.attrib.get('cx', 0))
                                if old_cx > 0:
                                    new_cy = int(old_cx * new_aspect)
                                    extent.set('cy', str(new_cy))
                                    modified_xml = True

                if modified_xml:
                    tree.write(str(doc_xml_path), encoding='utf-8', xml_declaration=True)

        # 3. Đóng gói lại file docx an toàn
        backup_path = str(docx_path) + ".bak"
        if not os.path.exists(backup_path):
            shutil.copyfile(str(docx_path), backup_path)

        with zipfile.ZipFile(str(out_docx_path), 'w', zipfile.ZIP_DEFLATED) as z_out:
            for foldername, subfolders, filenames in os.walk(temp_dir):
                for filename in filenames:
                    filepath = os.path.join(foldername, filename)
                    arcname = os.path.relpath(filepath, temp_dir)
                    z_out.write(filepath, arcname)

        print(f" Đã lưu thành công: {out_docx_path}")
        return len(resolved_map)

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="Thay thế ảnh nhanh và an toàn trong file Word (.docx)")
    parser.add_argument("docx", help="Đường dẫn file Word (.docx)")
    parser.add_argument("--list", action="store_true", help="Liệt kê danh sách ảnh và Caption hiện có")
    parser.add_argument("--figure", help="Số hiệu/tên hình cần thay (VD: 'Hình 3.2' hoặc '3.2')")
    parser.add_argument("--target", help="Tên media trong file Word (VD: 'image4.png')")
    parser.add_argument("--new", help="Đường dẫn file ảnh mới thay vào")
    parser.add_argument("--mapping", help="File JSON chứa ánh xạ thay thế hàng loạt")
    parser.add_argument("-o", "--output", help="Đường dẫn file xuất ra (mặc định ghi đè file gốc)")
    parser.add_argument("--no-aspect", action="store_true", help="Không tự động tính lại tỷ lệ khung hình")

    args = parser.parse_args()

    if args.list:
        list_images(args.docx)
        return

    replacements = {}
    if args.mapping:
        with open(args.mapping, 'r', encoding='utf-8') as f:
            replacements = json.load(f)
    elif args.figure and args.new:
        replacements[args.figure] = args.new
    elif args.target and args.new:
        replacements[args.target] = args.new
    else:
        print("❌ Vui lòng chọn --list để xem ảnh, hoặc chỉ định --figure/--target và --new để thay thế.")
        sys.exit(1)

    replace_images_in_docx(
        args.docx,
        replacements,
        out_docx_path=args.output,
        update_aspect_ratio=not args.no_aspect
    )


if __name__ == "__main__":
    main()
