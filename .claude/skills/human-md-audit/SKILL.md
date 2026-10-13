---
name: human-md-audit
description: Vòng lặp nhanh báo cáo Word: biên tập văn xuôi giống người bằng human-report-writing, xuất Markdown review, audit cấu trúc XML/text trong vài giây; chỉ render ảnh ở gate cuối. Dùng khi cần sửa văn nhanh, kiểm docx nhanh, tránh đọc ảnh từng trang; từ khóa: human giống người, markdown review, audit nhanh, kiểm docx nhanh, fast audit.
---

# human-md-audit — Vòng lặp nhanh: humanize → Markdown → audit cấu trúc

Mục tiêu: sửa văn nhanh **mà vẫn giống người**, đọc nội dung qua **Markdown** thay vì mở `.docx`
lòng vòng, và audit cấu trúc Word bằng **XML/text trong vài giây**. Ảnh render chỉ dùng cho
**gate cuối**, không dùng để đọc nội dung.

## Không trùng skill khác

- Văn phong: **thuộc `human-report-writing`**. Skill này KHÔNG tự đặt luật văn mới.
- Cấu trúc Word: **thuộc `docx-report`**. Skill này KHÔNG tự đặt luật heading/caption/TOC.
- Sửa file đẹp: **thuộc `safe-docx-modifier`**. Skill này chỉ sửa nháp/chương đang làm.
- Điều phối khối: **thuộc `coord-report` / `skill-coordinator`**.

## Khi nào dùng

- Viết/sửa một chương rồi muốn kiểm nhanh trước khi render.
- Muốn đọc toàn bộ nội dung qua một file `.md` gọn thay vì mở Word.
- Muốn audit lặp đi lặp lại mà không tốn thời gian đọc ảnh từng trang.

## Khi nào KHÔNG dùng

- File đã căn chỉnh đẹp, chỉ cần thay ảnh/sửa chữ: dùng `safe-docx-modifier`.
- Kết luận layout/tràn trang/vỡ bảng: vẫn phải qua `render_docx.py` + soi ảnh.
- Viết mới toàn bộ báo cáo từ đầu: dùng `coord-report`.

## Chuỗi bắt buộc

```text
1. human-report-writing: sửa văn + đọc lại toàn bộ bản thảo
2. export_review_md.py: xuất review Markdown để đọc/kiểm nội dung
3. fast_audit_docx.py: audit cấu trúc XML/text, FAIL thì sửa ngay
4. Lặp 1–3 cho tới FAST-CHECK PASS
5. Chỉ khi đổi layout/trang/hình: render_docx.py + soi ảnh (gate cuối)
```

## Lệnh

```bash
# 1. Xuất Markdown review để đọc nội dung nhanh
py -V:3.14 .claude/skills/human-md-audit/scripts/export_review_md.py reports/chuong-3.docx --out reports/chuong-3.review.md

# 2. Audit nhanh cấu trúc, đồng thời ghi Markdown kết quả
py -V:3.14 .claude/skills/human-md-audit/scripts/fast_audit_docx.py reports/chuong-3.docx --md reports/chuong-3.fast.md --strict
```

## Hai cổng khác nhau (bất biến)

- `FAST-CHECK PASS` = cấu trúc/text ổn, **KHÔNG** chứng minh layout/tràn trang.
- `VISUAL PASS` = đã render + soi từng ảnh PNG.
- CẤM ghi “hoàn thiện” khi mới chỉ qua fast audit.

## Definition of Done

```text
[ ] Đã nạp human-report-writing và đọc lại toàn bộ bản thảo.
[ ] Đã xuất review Markdown và đọc nội dung qua Markdown.
[ ] fast_audit_docx.py: 0 FAIL (WARN phải có lý do).
[ ] Nếu đổi layout/trang/hình: render + soi ảnh từng trang.
[ ] Không vi phạm luật của skill chủ.
```
