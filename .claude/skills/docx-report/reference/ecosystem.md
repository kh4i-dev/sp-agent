# Hệ sinh thái DOCX — repo & skill tham khảo (high-star)

> Tổng hợp các nguồn hữu ích cho việc tạo/đọc/sửa `.docx`. Số ⭐ là ước lượng tại thời
> điểm khảo sát (2026-10), chỉ để xếp hạng tương đối. Luôn xác minh lại trước khi phụ thuộc.
> Với lỗi numbering/list, ưu tiên tài liệu chính thức Microsoft Learn (OOXML).

## Thư viện nền (bắt buộc biết)

| Repo | ⭐ | Vai trò |
|---|---|---|
| `python-openxml/python-docx` | ~5.7k | Thư viện chuẩn đọc/tạo/sửa `.docx`. sp-agent dùng trực tiếp. |
| `elapouya/python-docx-template` (docxtpl) | ~1.7k | Jinja2 template cho `.docx` — sinh báo cáo từ template + dữ liệu. |
| `pandoc` | — | Chuyển Markdown ↔ DOCX; dùng khi cần convert nhanh. |

## Skill / toolkit cho AI agent (định dạng Agent Skills)

| Repo | Vai trò |
|---|---|
| `martinderm/python-docx-editor` | **"DOCX editor for AI Agents"** — CLI an toàn, có `SKILL.md`. Trích `.docx` → JSON (`docx-structure.v2`), patch có guard (`expected_matches`, heading-protection), Markdown↔DOCX (standalone hoặc theo template), fill ô bảng từ JSON (`cell-map`), inspect comment/revision/highlight. Rất đáng tham chiếu cho nhánh *Sửa patch tối thiểu*. |
| `paper-instruments/paper-docx` | Fork "agent-safe" của python-docx: giữ API `import docx`, thêm inspection/editing có guard, **từ chối thao tác không hỗ trợ thay vì đoán** (chống hỏng file âm thầm). |
| `Poggi-Tang/DocxSpec` | Thư viện sinh báo cáo có cấu trúc trên python-docx: container nội dung, caption hình/bảng tự đánh số, field PAGE/NUMPAGES, refresh TOC/lists. Hữu ích cho đồ án cần caption + mục lục. |
| `cmhac/docx-report` | Wrapper python-docx: tiện chèn bảng/hình từ pandas, cú pháp viết gọn. |

## Ý tưởng nên mượn cho `docx-report`

- **Patch có guard** (từ `python-docx-editor`): khai báo `expected_matches` để tránh thay nhầm,
  bảo vệ heading khi replace range — khớp với "Quy tắc patch bất biến" của skill này.
- **Trích cấu trúc ra JSON** trước khi sửa: cho phép diff và audit khách quan.
- **Caption/sequence tự động** (từ `DocxSpec`): tránh tự gõ `Hình 3.1` gây lệch khi chèn/xoá.
- **Dùng template + dữ liệu** (docxtpl/DocxSpec) khi báo cáo có khuôn lặp lại.
- **Kiểm tra numbering bằng tài liệu Microsoft Learn** thay vì đoán khi list/heading lỗi.

## Bản clone trong project

- `vendor/python-docx-editor/` — repo `martinderm/python-docx-editor` (GPL-3.0, commit `e994b2b`).
  KHÔNG auto-load; copy vào `.claude/skills/` nếu muốn dùng như skill thật.

## Render & QA

- LibreOffice (`soffice --headless --convert-to pdf`) hoặc Word COM (Windows) để render.
- Xem `scripts/render_docx.py` của skill này; luôn soi từng trang trước khi giao.
