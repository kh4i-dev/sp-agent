---
name: coord-report
description: Điều phối khối BÁO CÁO / ĐỒ ÁN Word (.docx): nạp nhanh để viết, sửa, chuẩn hóa, biên tập báo cáo - đồ án - luận văn - bài tập lớn. Gom docx-report (chủ), human-report-writing, human-md-audit, safe-docx-modifier, docx và chỉ rõ thứ tự nạp + cổng render. Từ khóa kích hoạt: viết báo cáo, sửa báo cáo, đồ án, luận văn, bài tập lớn, file Word .docx, chỉnh định dạng báo cáo, biên tập văn phong báo cáo.
---

# coord-report — Điều phối khối Báo cáo / Đồ án Word

Nạp skill này để vào đúng khối **báo cáo/đồ án `.docx`** mà không phải quét toàn bộ bộ skill.

> Bản đồ toàn cục: `skill-coordinator`. Baseline chống mâu thuẫn: `docs/rule-conflicts.md`.

## Khi nào nạp

- Viết / bổ sung / rút gọn chương báo cáo, đồ án, luận văn, BTL.
- Sửa hình thức: heading, caption, bảng, TOC, lề, số trang.
- Biên tập văn phong báo cáo; sửa file Word đã hoàn thiện.

## Khối gồm

| Skill | Vai trò | Khi nào |
|---|---|---|
| `docx-report` | **CHỦ**: cấu trúc, heading, bảng, caption SEQ/REF, TOC, số trang, bìa, render QA | mọi việc báo cáo |
| `human-report-writing` | Văn xuôi tự nhiên + luật định dạng (cấm em dash, cấm in đậm thân bài, không bullet tràn lan) | khi viết/biên tập nội dung |
| `safe-docx-modifier` | Sửa file ĐÃ hoàn thiện, Zero Regeneration (thay ảnh in-place, sửa text bảo toàn runs) | file đã căn chỉnh đẹp |
| `docx` | OOXML chuyên sâu: tracked changes, comments, template | case nâng cao |
| `human-md-audit` | Vòng lặp nhanh: humanize → Markdown review → audit cấu trúc (không luật văn mới) | kiểm nhanh trước render |

## Thứ tự nạp & chuỗi

```text
(grill-me: hỏi bìa — đề tài, GVHD, SV, lớp, MSSV, mục tiêu số trang)
 → docx-report (dựng/sửa cấu trúc, format, TOC, caption)
 → human-report-writing (biên tập văn xuôi + **đọc lại TOÀN BỘ bản thảo** trước khi giao)
 → human-md-audit (xuất review Markdown + `fast_audit_docx.py`; FAIL thì sửa ngay, lặp tới FAST-CHECK PASS)
 → [cần sơ đồ] coord-diagrams → diagram-auditor (GATE)
 → [cần bìa] make_cover.py ; [file đẹp] safe-docx-modifier
 → render_docx.py → soi từng trang PNG (Visual QA, chỉ gate cuối cho layout/trang/hình)
```

## Cổng (gate)

- **Vòng nhanh:** `fast_audit_docx.py` phải 0 FAIL trước khi render.
- **Gate cuối:** **bắt buộc render + soi ảnh** khi đổi layout/trang/hình hoặc trước khi giao (AGENTS #2). FAST-CHECK PASS **không** thay VISUAL PASS.

## Quy ước chung (bất biến)

- Văn xuôi: **không em dash**, **không in đậm thân bài**, **không highlight**, không bullet tràn lan.
- Sơ đồ học thuật trong báo cáo: **trắng-đen**; caption dạng `Hình X.Y: ...`.
- Thay ảnh / sửa file đẹp → dùng script của skill, KHÔNG sinh lại từ đầu.

## Anti-patterns

- ❌ Chỉ gọi `docx-report` mà bỏ sơ đồ / văn phong / bìa.
- ❌ Viết số caption / mục lục bằng tay thay vì field (`SEQ`/`TOC`).
- ❌ Dùng em dash / in đậm trong thân bài.

## Definition of Done

```text
[ ] Nạp đúng khối (docx-report + human-report-writing + human-md-audit...).
[ ] human-report-writing đã **đọc lại toàn bộ** bản thảo (self-review), không chỉ viết.
[ ] human-md-audit: đã đọc Markdown review + `fast_audit_docx.py` 0 FAIL.
[ ] Sơ đồ (nếu có) qua diagram-auditor.
[ ] render + soi ảnh từng trang: PASS.
[ ] Không vi phạm quy ước chung.
```
