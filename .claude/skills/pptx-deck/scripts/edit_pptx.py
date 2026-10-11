#!/usr/bin/env python3
"""Chỉnh sửa và thay thế nội dung nhanh trong file PowerPoint (.pptx).

Cách dùng:
    python edit_pptx.py deck.pptx --replace "GVHD cũ" "TS. Nguyễn Thị Hương"
    python edit_pptx.py deck.pptx --replace-many pairs.json
    python edit_pptx.py deck.pptx --slide 1 --add-image bg.png --bg
    python edit_pptx.py deck.pptx -o output.pptx --replace "K58" "K59"
"""
import argparse
import json
import sys
from pathlib import Path

# Đảm bảo in tiếng Việt không bị lỗi charmap trên Windows terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def replace_text_in_shape(shape, old_text, new_text):
    replaced = 0
    if shape.has_text_frame:
        for p in shape.text_frame.paragraphs:
            for r in p.runs:
                if old_text in r.text:
                    r.text = r.text.replace(old_text, new_text)
                    replaced += 1
    if shape.has_table:
        for row in shape.table.rows:
            for cell in row.cells:
                for p in cell.text_frame.paragraphs:
                    for r in p.runs:
                        if old_text in r.text:
                            r.text = r.text.replace(old_text, new_text)
                            replaced += 1
    return replaced


def replace_text_in_deck(pptx_path: Path, replacements: dict[str, str], out_path: Path):
    from pptx import Presentation

    prs = Presentation(str(pptx_path))
    total_replaced = 0

    for slide_idx, slide in enumerate(prs.slides, start=1):
        for shape in slide.shapes:
            for old_text, new_text in replacements.items():
                c = replace_text_in_shape(shape, old_text, new_text)
                total_replaced += c

        # Thay cả trong speaker notes nếu có
        if slide.has_notes_slide:
            tf = slide.notes_slide.notes_text_frame
            for old_text, new_text in replacements.items():
                if old_text in tf.text:
                    tf.text = tf.text.replace(old_text, new_text)
                    total_replaced += 1

    prs.save(str(out_path))
    return total_replaced


def add_image_to_slide(pptx_path: Path, slide_idx: int, img_path: Path, out_path: Path, is_bg: bool = False):
    from pptx import Presentation
    from pptx.util import Inches

    prs = Presentation(str(pptx_path))
    if slide_idx < 1 or slide_idx > len(prs.slides):
        sys.exit(f"Lỗi: Slide {slide_idx} không hợp lệ (tổng số slide: {len(prs.slides)})")

    slide = prs.slides[slide_idx - 1]
    if is_bg:
        # Chèn làm nền full màn hình 16:9 (13.33 x 7.5 inches)
        left = top = Inches(0)
        width = prs.slide_width
        height = prs.slide_height
        pic = slide.shapes.add_picture(str(img_path), left, top, width, height)
        # Đưa hình xuống dưới cùng (z-order)
        slide.shapes._spTree.remove(pic._element)
        slide.shapes._spTree.insert(2, pic._element)
    else:
        # Chèn vào giữa slide
        left = Inches(4.0)
        top = Inches(2.0)
        width = Inches(5.0)
        slide.shapes.add_picture(str(img_path), left, top, width=width)

    prs.save(str(out_path))
    print(f">> Đã chèn ảnh {img_path.name} vào Slide {slide_idx} -> Lưu tại: {out_path}")


def main():
    ap = argparse.ArgumentParser(description="Chỉnh sửa văn bản và hình ảnh trong file PPTX.")
    ap.add_argument("pptx", help="Đường dẫn file .pptx nguồn")
    ap.add_argument("-o", "--output", help="File xuất ra (mặc định ghi đè hoặc tạo bản mới)")
    ap.add_argument("--replace", nargs=2, metavar=("OLD", "NEW"), help="Tìm và thay thế văn bản")
    ap.add_argument("--replace-many", help="File JSON chứa các cặp { 'OLD': 'NEW' }")
    ap.add_argument("--slide", type=int, help="Chỉ định số thứ tự slide (bắt đầu từ 1)")
    ap.add_argument("--add-image", help="Chèn ảnh vào slide")
    ap.add_argument("--bg", action="store_true", help="Đặt ảnh làm background toàn slide")
    args = ap.parse_args()

    pptx_path = Path(args.pptx)
    if not pptx_path.exists():
        sys.exit(f"Lỗi: Không tìm thấy {pptx_path}")

    out_path = Path(args.output) if args.output else pptx_path

    if args.add_image and args.slide:
        img_path = Path(args.add_image)
        if not img_path.exists():
            sys.exit(f"Lỗi: Không tìm thấy ảnh {img_path}")
        add_image_to_slide(pptx_path, args.slide, img_path, out_path, is_bg=args.bg)
        return

    replacements = {}
    if args.replace:
        replacements[args.replace[0]] = args.replace[1]
    if args.replace_many:
        j_path = Path(args.replace_many)
        if j_path.exists():
            replacements.update(json.loads(j_path.read_text(encoding="utf-8")))

    if replacements:
        print(f">> Đang tìm và thay thế {len(replacements)} cặp từ khóa trong {pptx_path.name}...")
        count = replace_text_in_deck(pptx_path, replacements, out_path)
        print(f">> Hoàn thành! Đã thay thế {count} vị trí. Lưu tại: {out_path}")
    else:
        print("Không có thao tác nào được chỉ định. Dùng --help để xem hướng dẫn.")


if __name__ == "__main__":
    main()
