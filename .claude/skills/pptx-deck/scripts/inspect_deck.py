#!/usr/bin/env python3
"""Kiểm tra và audit chất lượng slide deck (.pptx).

Cách dùng:
    python inspect_deck.py deck.pptx
    python inspect_deck.py deck.pptx --verbose

Công dụng:
  - Thống kê tổng số slide, số shape, số ảnh, số bảng
  - Phát hiện slide nào thiếu Speaker Notes
  - Cảnh báo slide quá nhiều chữ (> 40 từ) vi phạm nguyên tắc trình bày
  - Liệt kê tiêu đề và nội dung chính của từng slide
"""
import argparse
import sys
from pathlib import Path

# Đảm bảo in tiếng Việt không bị lỗi charmap trên Windows terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def inspect_presentation(pptx_path: Path, verbose: bool = False):
    from pptx import Presentation
    from pptx.enum.shapes import MSO_SHAPE_TYPE

    prs = Presentation(str(pptx_path))
    slides = prs.slides
    total_slides = len(slides)

    print("=" * 60)
    print(f"BÁO CÁO KIỂM TRA SLIDE DECK: {pptx_path.name}")
    print(f"Tổng số slide: {total_slides}")
    print("=" * 60)

    missing_notes = []
    wordy_slides = []

    for i, slide in enumerate(slides, start=1):
        # Lấy tiêu đề slide
        title = "(Không tiêu đề)"
        text_content = []
        shape_count = len(slide.shapes)
        image_count = 0
        table_count = 0

        for shape in slide.shapes:
            if shape.has_text_frame:
                txt = shape.text.strip()
                if txt:
                    text_content.append(txt)
            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                image_count += 1
            if shape.has_table:
                table_count += 1

        if text_content:
            title = text_content[0].split("\n")[0][:60]

        # Đếm tổng số từ trên slide
        total_words = sum(len(txt.split()) for txt in text_content)

        # Kiểm tra notes
        has_note = False
        note_length = 0
        if slide.has_notes_slide:
            note_txt = slide.notes_slide.notes_text_frame.text.strip()
            if note_txt:
                has_note = True
                note_length = len(note_txt)

        if not has_note:
            missing_notes.append(i)
        if total_words > 45:
            wordy_slides.append((i, total_words))

        status_flag = "OK"
        if not has_note and total_words > 45:
            status_flag = "CẢNH BÁO: Quá nhiều chữ & Thiếu Notes"
        elif not has_note:
            status_flag = "Thiếu Notes"
        elif total_words > 45:
            status_flag = f"Nhiều chữ ({total_words} từ)"

        if verbose or status_flag != "OK":
            print(f"Slide {i:02d} | [{status_flag}] | {title}")
            print(f"         Shapes: {shape_count} | Ảnh: {image_count} | Bảng: {table_count} | Từ: {total_words} | Note: {note_length} ký tự")

    print("-" * 60)
    print("TỔNG KẾT CHẤT LƯỢNG:")
    if missing_notes:
        print(f"  ❌ {len(missing_notes)} slide chưa có Speaker Notes: Slide {missing_notes}")
    else:
        print("  ✅ 100% slide đã có Speaker Notes.")

    if wordy_slides:
        print(f"  ⚠️  {len(wordy_slides)} slide có nguy cơ quá tải chữ (>45 từ):")
        for s_idx, w_count in wordy_slides:
            print(f"     - Slide {s_idx:02d}: {w_count} từ (Cân nhắc chuyển bớt sang hình vẽ hoặc chuyển vào Speaker Notes)")
    else:
        print("  ✅ Mật độ chữ trên các slide hợp lý, không bị quá tải.")
    print("=" * 60)


def main():
    ap = argparse.ArgumentParser(description="Kiểm tra chất lượng slide PPTX.")
    ap.add_argument("pptx", help="Đường dẫn file .pptx")
    ap.add_argument("-v", "--verbose", action="store_true", help="Hiển thị chi tiết từng slide")
    args = ap.parse_args()

    pptx_path = Path(args.pptx)
    if not pptx_path.exists():
        sys.exit(f"Lỗi: Không tìm thấy file {pptx_path}")

    try:
        inspect_presentation(pptx_path, args.verbose)
    except ImportError:
        sys.exit("Cần cài đặt: pip install python-pptx (hoặc dùng uv run --with python-pptx ...)")


if __name__ == "__main__":
    main()
