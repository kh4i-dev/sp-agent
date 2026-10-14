#!/usr/bin/env python3
"""
safe_replace_text.py — Thay thế văn bản an toàn in-place trong file Word (.docx)
Không tái tạo (Zero Regeneration): Bảo toàn 100% định dạng, style, margins, tables, runs.
Giải quyết triệt để vấn đề Word ngắt text qua nhiều thẻ <w:r> (Run-splitting problem).
"""
import argparse
import json
import os
import re
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


def _preserve_namespaces(xml_path):
    """Đăng ký lại toàn bộ prefix namespace đúng như file gốc.

    BẮT BUỘC trước mọi tree.write(): nếu không, ElementTree sẽ đổi prefix
    (w: -> ns0:, mc: -> ns1:, ...) và Word báo "file appears to be corrupted"
    vì các giá trị như mc:Ignorable="w14 w15" không còn khớp prefix nào.
    """
    raw = Path(xml_path).read_bytes()
    for m in re.finditer(rb'\bxmlns:([A-Za-z_][\w.\-]*)\s*=\s*"([^"]+)"', raw):
        prefix = m.group(1).decode('ascii', 'ignore')
        uri = m.group(2).decode('utf-8', 'ignore')
        if prefix.lower() == 'xml':
            continue
        try:
            ET.register_namespace(prefix, uri)
        except ValueError:
            pass


def replace_in_element_runs(root, old_text, new_text, use_regex=False):
    """
    Tìm và thay thế old_text bằng new_text trong các đoạn w:p,
    bảo toàn Run formatting và xử lý run-splitting.
    """
    count = 0
    paragraphs = root.findall('.//w:p', NS)

    for p in paragraphs:
        runs = []
        for r in p.findall('.//w:r', NS):
            t_elems = r.findall('./w:t', NS)
            if t_elems:
                run_str = "".join([te.text or "" for te in t_elems])
                runs.append((r, t_elems, run_str))

        if not runs:
            continue

        full_text = "".join([r[2] for r in runs])

        # Tìm các vị trí xuất hiện
        matches = []
        if use_regex:
            for m in re.finditer(old_text, full_text):
                matches.append((m.start(), m.end(), m.group(0)))
        else:
            idx = 0
            while True:
                pos = full_text.find(old_text, idx)
                if pos == -1:
                    break
                matches.append((pos, pos + len(old_text), old_text))
                idx = pos + len(old_text)

        if not matches:
            continue

        # Duyệt từ cuối lên đầu để không làm lệch chỉ số chuỗi
        for m_start, m_end, orig_match in reversed(matches):
            count += 1
            replacement_str = new_text

            curr_pos = 0
            affected_runs = []
            for r_idx, (r, t_elems, r_text) in enumerate(runs):
                r_len = len(r_text)
                r_start = curr_pos
                r_end = curr_pos + r_len

                if max(m_start, r_start) < min(m_end, r_end):
                    loc_start = max(0, m_start - r_start)
                    loc_end = min(r_len, m_end - r_start)
                    affected_runs.append((r_idx, loc_start, loc_end))
                curr_pos += r_len

            if not affected_runs:
                continue

            # Run đầu tiên nhận text thay thế
            first_idx, first_loc_s, first_loc_e = affected_runs[0]
            r, t_elems, r_text = runs[first_idx]

            new_r_text = r_text[:first_loc_s] + replacement_str + (r_text[first_loc_e:] if len(affected_runs) == 1 else "")
            t_elems[0].text = new_r_text
            if new_r_text.startswith(" ") or new_r_text.endswith(" "):
                t_elems[0].set(f"{{{NS['xml']}}}space", "preserve")
            for te in t_elems[1:]:
                te.text = ""
            runs[first_idx] = (r, t_elems, new_r_text)

            # Các run ở giữa (nếu match trải dài nhiều run)
            for aff_idx, loc_s, loc_e in affected_runs[1:-1]:
                r_mid, t_elems_mid, r_text_mid = runs[aff_idx]
                t_elems_mid[0].text = ""
                for te in t_elems_mid[1:]:
                    te.text = ""
                runs[aff_idx] = (r_mid, t_elems_mid, "")

            # Run cuối cùng
            if len(affected_runs) > 1:
                last_idx, last_loc_s, last_loc_e = affected_runs[-1]
                r_last, t_elems_last, r_text_last = runs[last_idx]
                rem_text = r_text_last[last_loc_e:]
                t_elems_last[0].text = rem_text
                if rem_text.startswith(" ") or rem_text.endswith(" "):
                    t_elems_last[0].set(f"{{{NS['xml']}}}space", "preserve")
                for te in t_elems_last[1:]:
                    te.text = ""
                runs[last_idx] = (r_last, t_elems_last, rem_text)

    return count


def safe_replace_text_in_docx(
    docx_path: str,
    replacements: list,
    out_docx_path: str = None,
    dry_run: bool = False,
    include_headers_footers: bool = True
):
    docx_path = Path(docx_path).resolve()
    if not docx_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {docx_path}")

    if out_docx_path is None:
        out_docx_path = docx_path
    else:
        out_docx_path = Path(out_docx_path).resolve()

    temp_dir = tempfile.mkdtemp(prefix="docx_txt_replace_")
    try:
        with zipfile.ZipFile(str(docx_path), 'r') as z:
            z.extractall(temp_dir)

        # Danh sách các XML cần quét
        target_xmls = ['word/document.xml']
        if include_headers_footers:
            for fname in os.listdir(os.path.join(temp_dir, 'word')):
                if fname.startswith(('header', 'footer', 'footnotes', 'endnotes')) and fname.endswith('.xml'):
                    target_xmls.append(f"word/{fname}")

        total_changes = 0
        report = []

        for xml_rel in target_xmls:
            xml_full_path = Path(temp_dir) / xml_rel
            if not xml_full_path.exists():
                continue

            tree = ET.parse(str(xml_full_path))
            root = tree.getroot()
            file_changed = False

            for old_str, new_str in replacements:
                cnt = replace_in_element_runs(root, old_str, new_str)
                if cnt > 0:
                    report.append((xml_rel, old_str, new_str, cnt))
                    total_changes += cnt
                    file_changed = True

            if file_changed and not dry_run:
                _preserve_namespaces(xml_full_path)
                tree.write(str(xml_full_path), encoding='utf-8', xml_declaration=True)

        print(f"\n📊 Báo cáo thay thế văn bản an toàn ({len(report)} mục khớp, tổng {total_changes} lượt):")
        print("=" * 80)
        for xml_rel, old_s, new_s, cnt in report:
            old_preview = old_s[:30] + "..." if len(old_s) > 30 else old_s
            new_preview = new_s[:30] + "..." if len(new_s) > 30 else new_s
            print(f"[{xml_rel}] '{old_preview}' ➔ '{new_preview}' ({cnt} lần)")
        print("=" * 80)

        if dry_run:
            print("🔍 Chế độ Dry-Run: Không ghi vào file.")
            return total_changes

        if total_changes == 0:
            print("ℹ️ Không có thay đổi nào cần thực hiện.")
            return 0

        # Tạo bản sao lưu an toàn
        backup_path = str(docx_path) + ".bak_safe"
        if not os.path.exists(backup_path):
            shutil.copyfile(str(docx_path), backup_path)
            print(f"🔒 Đã tạo backup: {os.path.basename(backup_path)}")

        # Đóng gói DOCX
        with zipfile.ZipFile(str(out_docx_path), 'w', zipfile.ZIP_DEFLATED) as z_out:
            for foldername, subfolders, filenames in os.walk(temp_dir):
                for filename in filenames:
                    filepath = os.path.join(foldername, filename)
                    arcname = os.path.relpath(filepath, temp_dir)
                    z_out.write(filepath, arcname)

        print(f"✅ Đã ghi thành công file DOCX an toàn: {out_docx_path}")
        return total_changes

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="Thay thế văn bản in-place an toàn cho file Word (.docx)")
    parser.add_argument("docx", help="Đường dẫn file Word (.docx)")
    parser.add_argument("--old", help="Chuỗi văn bản cần tìm")
    parser.add_argument("--new", help="Chuỗi văn bản thay thế")
    parser.add_argument("--batch", help="File JSON chứa danh sách cặp [old, new] hoặc dict {old: new}")
    parser.add_argument("-o", "--output", help="Đường dẫn file xuất ra (mặc định ghi đè)")
    parser.add_argument("--dry-run", action="store_true", help="Chỉ kiểm tra số lượng khớp, không ghi file")

    args = parser.parse_args()

    replacements = []
    if args.batch:
        with open(args.batch, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                replacements = data
            elif isinstance(data, dict):
                replacements = list(data.items())
    elif args.old is not None and args.new is not None:
        replacements.append((args.old, args.new))
    else:
        print("❌ Vui lòng cung cấp cặp --old và --new, hoặc chỉ định file --batch.")
        sys.exit(1)

    safe_replace_text_in_docx(
        args.docx,
        replacements,
        out_docx_path=args.output,
        dry_run=args.dry_run
    )


if __name__ == "__main__":
    main()
