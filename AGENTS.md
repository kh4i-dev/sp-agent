# AGENTS.md — sp-agent

Bộ **skill** cho agent: viết tài liệu, làm slide, vẽ sơ đồ, nghiên cứu.
Khi người dùng ra lệnh, agent tự chọn skill phù hợp dưới đây và nạp `SKILL.md` tương ứng.

## Cách skill được nạp

Skills nằm ở **hai nơi giống hệt nhau** (mirror):

- `.claude/skills/<name>/SKILL.md`
- `.agents/skills/<name>/SKILL.md`

opencode và Claude Code đều đọc `.claude/skills/` và `.agents/skills/`, nên agent sẽ tự thấy.
Sửa skill ở `.claude/skills/` rồi chạy `tools/sync-skills.ps1` để đồng bộ sang `.agents/skills/`.

Skill `ppt-master` (hugohe3/ppt-master, MIT) đã được cài sẵn như một skill thật trong `.claude/skills/ppt-master/`.

## Tài liệu tham khảo bên thứ ba (`vendor/`)

Các repo agent-skill high-star đã clone về **để tra cứu — KHÔNG auto-load**: xem `vendor/README.md`.
- DOCX: `python-docx-editor`
- UI/anti-slop: `anti-slop`, `unslop-ui`, `no-slop-ui`
- Sơ đồ: `markdown-viewer-skills`, `plantuml-skill`, `spillwave-plantuml`

Muốn biến một repo trong `vendor/` thành skill thật: copy vào `.claude/skills/<name>/` rồi chạy `tools/sync-skills.ps1`.

## Skill index

| Skill | Dùng khi | Đầu ra chính |
|---|---|---|
| `docx-report` | Viết/sửa/audit file Word, báo cáo, đồ án, luận văn | `.docx` đúng cấu trúc, đã render kiểm tra |
| `human-report-writing` | Biên tập văn phong báo cáo cho tự nhiên như người, bỏ dấu hiệu văn AI | Văn xuôi tự nhiên, có Tóm tắt chương |
| `pptx-deck` | Làm slide, thuyết trình, PowerPoint cơ bản | `.pptx` biên tập được, chart native |
| `ppt-master` | Chuyển tài liệu (PDF, Word, Markdown) thành slide PowerPoint native đẳng cấp, tái tạo slide từ ảnh, làm đẹp (beautify) deck, animation/transition native, audio narration TTS | `.pptx` native shapes/connectors, slide masters, audio narration |
| `mermaid-diagrams` | Sơ đồ UML/ERD/kiến trúc/flowchart | `.mmd` → SVG/PNG, nhúng vào tài liệu |
| `research-report` | Nghiên cứu, tổng hợp, fact-check, dẫn nguồn | Báo cáo có citation đã xác minh |
| `pdf-toolkit` | Đọc/trích/tạo/OCR/ghép PDF | Text/bảng/ảnh, PDF mới |
| `xlsx-sheet` | Bảng tính Excel, số liệu, biểu đồ | `.xlsx` đã recalc công thức |
| `anti-slop` | Thiết kế/làm lại UI, audit giao diện, chống "AI slop", bố cục slide/dashboard | Giao diện có chủ đích, qua anti-slop gate |

## Routing — ý định người dùng → skill

```text
"viết báo cáo / sửa file Word / đồ án / luận văn"        → docx-report
"viết như người / tự nhiên hơn / đỡ giống AI / đổi văn phong" → human-report-writing
"làm slide / thuyết trình / PowerPoint / bảo vệ"          → pptx-deck
"tạo slide từ tài liệu / PDF sang PPT / làm đẹp slide / beautify PPTX / tái tạo slide từ ảnh / ppt-master" → ppt-master
"vẽ sơ đồ / UML / ERD / use case / kiến trúc"            → mermaid-diagrams
"nghiên cứu / tìm hiểu / tổng hợp / so sánh công nghệ"   → research-report
"đọc PDF / trích PDF / OCR / chuyển sang PDF"            → pdf-toolkit
"Excel / bảng tính / số liệu / biểu đồ Excel"            → xlsx-sheet
"thiết kế UI / làm lại giao diện / đừng giống AI / anti-slop / unslop" → anti-slop
```

Kết hợp nhiều skill khi cần. Ví dụ điển hình cho đồ án:

```text
research-report  → thu thập & xác minh nguồn
mermaid-diagrams → vẽ Use Case / ERD / Sequence / kiến trúc
human-report-writing → biên tập văn phong cho tự nhiên
docx-report      → ghép thành báo cáo .docx, render & QA
pptx-deck        → làm slide bảo vệ từ nội dung báo cáo
```

## Nguyên tắc bất biến (mọi skill)

1. **Source truth** — không bịa dữ liệu, không bịa kết quả test/khảo sát; `PARTIAL`/`NOT_FOUND` không được nâng thành `IMPLEMENTED`.
2. **Render gate** — không kết luận file Word/Slide/PDF hoàn thiện nếu chưa render và soi từng trang.
3. **No fake sources** — chỉ trích dẫn URL đã thực sự truy cập; nghi ngờ thì đánh dấu `UNVERIFIED`.
4. **No secrets** — không đưa API key/mật khẩu/credential vào tài liệu; kiểm tra metadata trước khi phát hành.
5. **Minimal patch** — sửa tối thiểu, giữ nội dung & cấu trúc, có thể rollback.
6. **Vietnamese output** — giữ thuật ngữ kỹ thuật tiếng Anh khi cần; kiểm tra hiển thị dấu tiếng Việt khi render.

## Toolchain & cài đặt

Đã có sẵn: `python`, `node`, `npm`, `npx`, `git`.
Cần cài thêm tùy nhu cầu:

```bash
pip install python-docx python-pptx openpyxl xlsxwriter pandas pymupdf pdfplumber pypdf reportlab

# LibreOffice — bắt buộc cho render QA (docx/pptx/xlsx recalc)
winget install TheDocumentFoundation.LibreOffice

# Mermaid CLI (không cần cài global)
npx -p @mermaid-js/mermaid-cli mmdc --help

# pandoc (tùy chọn, để convert Markdown)
winget install JohnMacFarlane.Pandoc
```

Kiểm tra nhanh: `powershell -File tools/check-tools.ps1`.

## Thêm skill mới

1. Tạo `.claude/skills/<ten-kebab-case>/SKILL.md`.
2. Frontmatter bắt buộc:

```yaml
---
name: <ten-kebab-case>      # trùng tên thư mục, chữ thường + gạch nối, <= 64 ký tự
description: <what + when + từ khóa kích hoạt, <= 1024 ký tự>
---
```

3. Chi tiết sâu để ở `reference/`, script ở `scripts/`, tài nguyên ở `assets/` (progressive disclosure).
4. Giữ `SKILL.md` dưới ~500 dòng.
5. Chạy `tools/sync-skills.ps1`.
