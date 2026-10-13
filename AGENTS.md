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

## Giao thức nạp skill (BẮT BUỘC — làm đúng thứ tự)

1. **Mở / khám phá**: `AGENTS.md` này đã được tự nạp; liệt kê cây skill bằng `codegraph_files` hoặc glob `.claude/skills/*/SKILL.md`. Mỗi skill = 1 thư mục chứa `SKILL.md`.
2. **Chọn skill**: tra bảng **Routing** (ý định → skill) bên dưới. Nhiều việc → nạp nhiều skill, phối hợp.
3. **Nạp**: gọi công cụ `skill` với đúng `name` (trùng tên thư mục). Nếu không có công cụ đó → `Read` thẳng `.claude/skills/<name>/SKILL.md`.
4. **Đọc ĐẦY ĐỦ**: đọc trọn `SKILL.md`; cần chi tiết thì mở tiếp `reference/` rồi `scripts/` (progressive disclosure). **Không đoán**, không bỏ qua phần "bất biến / IRON RULE / GATE".
5. **Thực thi theo skill** + tuân thủ "Nguyên tắc bất biến" (cuối file này).
6. **Nhớ lâu dài**: chỉ `AGENTS.md` / `CLAUDE.md` được tự nạp mỗi phiên → **quy tắc bền vững phải ghi vào đây**; ghi chú trong phiên thì dùng bộ nhớ (`memory_save`).

**Bẫy khiến skill KHÔNG nạp / nạp sai (tránh tuyệt đối):**
- Frontmatter `name` **khác** tên thư mục (phải kebab-case và trùng khớp) → skill không thấy.
- `description` **thiếu từ khóa kích hoạt** → agent không chọn đúng skill.
- Sửa `.claude/skills/` mà **quên `tools/sync-skills.ps1`** → bản `.agents/skills/` lệch.
- `SKILL.md` quá dài (> ~500 dòng) → đẩy chi tiết sang `reference/`.
- Đọc skill nhưng **bỏ qua bước render / kiểm ảnh / QA** mà skill yêu cầu → coi như CHƯA xong.
- Tạo script lẻ ở thư mục gốc → phải để trong `tools/`/`docs/tools/` (xem Nguyên tắc bất biến).

**Definition of Done khi dùng skill:** đã nạp **đúng** skill · làm **đủ** bước skill yêu cầu · có **bằng chứng** (render/ảnh/log) · **không** vi phạm "Nguyên tắc bất biến".

## Tài liệu tham khảo bên thứ ba (`vendor/`)

Các repo agent-skill high-star đã clone về **để tra cứu — KHÔNG auto-load**: xem `vendor/README.md`.
- DOCX: `python-docx-editor`
- UI/anti-slop: `anti-slop`, `unslop-ui`, `no-slop-ui`
- Sơ đồ: `markdown-viewer-skills`, `plantuml-skill`, `spillwave-plantuml`
- Chuẩn Agent & Skill chính thức (OpenAI & Anthropic): `anthropics-skills`, `openai-plugins`, `openai-codex`, `anthropics-claude-code`


Muốn biến một repo trong `vendor/` thành skill thật: copy vào `.claude/skills/<name>/` rồi chạy `tools/sync-skills.ps1`.

## Skill index

| Skill | Dùng khi | Đầu ra chính |
|---|---|---|
| `docx-report` | Viết/sửa/audit file Word, báo cáo, đồ án, luận văn | `.docx` đúng cấu trúc, đã render kiểm tra |
| `safe-docx-modifier` | Chỉnh sửa an toàn file Word khi đã hoàn thiện (Zero Regeneration), thay ảnh in-place, sửa text bảo toàn Runs | `.docx` giữ 100% định dạng, ảnh và nội dung cập nhật |
| `human-report-writing` | Biên tập văn phong báo cáo cho tự nhiên như người, bỏ dấu hiệu văn AI | Văn xuôi tự nhiên, có Tóm tắt chương |
| `pptx-deck` | Làm slide, thuyết trình, PowerPoint cơ bản | `.pptx` biên tập được, chart native |
| `ppt-master` | Chuyển tài liệu (PDF, Word, Markdown) thành slide PowerPoint native đẳng cấp, tái tạo slide từ ảnh, làm đẹp (beautify) deck, animation/transition native, audio narration TTS | `.pptx` native shapes/connectors, slide masters, audio narration |
| `diagram-orchestrator` | Điều phối sơ đồ theo giao thức tư duy thông minh (Intelligent Problem-Solving Protocol), chọn đúng công cụ theo ngữ nghĩa | Sơ đồ chuẩn xác theo công cụ tối ưu, có bằng chứng nghiệm thu |

| `plantuml-diagrams` | Sơ đồ UML/ERD/Sequence/Activity/Class/Use Case chuẩn mực 100% (công cụ bất lực → vẽ tay/draw.io nhưng BẮT BUỘC theo chuẩn Use Case) | `.puml` → SVG/PNG, chuẩn học thuật Trắng-Đen |
| `use-case-layout` | Use Case UML đúng nghiệp vụ + bố cục lane GỌN-ĐẸP-DỄ NHÌN, **cấm connector vòng xa**, chuyển draw.io thủ công khi auto-layout không sạch | `.puml`/`.drawio` + PNG/SVG + báo cáo Semantic/Visual Review |
| `simplified-diagrams` | Sơ đồ tinh gọn / Khái niệm (Conceptual) cho thuyết trình & bảo vệ đồ án, 5-8 thực thể cốt lõi | `.puml`, SVG/PNG nét thẳng chuẩn + Kịch bản phát biểu 60s |
| `diagram-auditor` | Audit và kiểm định chất lượng sơ đồ (chống banner cảnh báo, chống méo lệch, chống đè nhãn, đủ SVG/PNG, hiển thị ảnh + tiêu đề Hình X.X, cấm xả code nguồn) | Báo cáo kiểm định PASS/FAIL + Ảnh sơ đồ & Tiêu đề Hình X.X |
| `tldraw-diagrams` | Sơ đồ kiến trúc, flowchart, luồng dữ liệu thẩm mỹ cao, đường cong mềm mại | `.tldr`, `.svg`, `.png` (2x) hiện đại, chỉnh sửa được |
| `research-report` | Nghiên cứu, tổng hợp, fact-check, dẫn nguồn | Báo cáo có citation đã xác minh |
| `pdf-toolkit` | Đọc/trích/tạo/OCR/ghép PDF | Text/bảng/ảnh, PDF mới |
| `xlsx-sheet` | Bảng tính Excel, số liệu, biểu đồ | `.xlsx` đã recalc công thức |
| `anti-slop` | Thiết kế/làm lại UI, audit giao diện, chống "AI slop", bố cục slide/dashboard | Giao diện có chủ đích, qua anti-slop gate |
| `doc-architect` | Lập/audit/đồng bộ bộ tài liệu dự án (README, AGENTS.md, docs/, CONTEXT), chống drift tài liệu | Tài liệu đầy đủ, qua Fresh Session Test |
| `living-docs` | ADR/MADR, PRD, ghi vết quyết định (supersede, never delete), sơ đồ kiến trúc Mermaid sống | Nhật ký quyết định + sơ đồ sống |
| `okf-knowledge-format` | Đóng gói/chuẩn hóa tri thức theo OKF (bundle markdown + frontmatter `type`) | Bundle tri thức chuẩn OKF |
| `documentation` | Viết tài liệu kỹ thuật: API docs, runbook, onboarding guide | Docs kỹ thuật hoàn chỉnh |
| `documentation-and-adrs` | Ghi ADR & lý do thiết kế khi đổi API/tính năng/hạ tầng | ADR + docs cập nhật |
| `doc-coauthoring` | Đồng soạn tài liệu/proposal/spec theo quy trình có kiểm chứng | Bản thảo đã kiểm cho người đọc |
| `research` | Nghiên cứu chủ đề, gom nguồn tin cậy, lưu thành file Markdown trong repo | Báo cáo nghiên cứu có dẫn nguồn |
| `research-artifacts` | Chuẩn hóa research thành bundle OKF (nguồn gốc, mức tin cậy, truy vết) | Artifact nghiên cứu có truy vết |
| `writing-guidelines` | Soát văn phong tài liệu/prose theo writing handbook | Danh sách chỉnh sửa theo chuẩn |
| `docx` | Tạo/đọc/sửa Word `.docx/.dotx` chuyên sâu OOXML (TOC, tracked changes, ảnh) | `.docx` hoàn chỉnh |
| `pptx` | Tạo/đọc/sửa PowerPoint `.pptx/.potx`, layout, speaker notes | `.pptx` hoàn chỉnh |
| `pdf` | Trích/ghép/tách/OCR/điền form/watermark PDF | PDF đã xử lý |
| `xlsx` | Tạo/đọc/sửa Excel/CSV/TSV, công thức, chart | `.xlsx`/`.csv` hoàn chỉnh |
| `diagram-design` | Vẽ đa dạng sơ đồ (kiến trúc, flowchart, ERD, Gantt, Sankey, UML...) xuất HTML/SVG/PNG, import drawio/Mermaid | Sơ đồ branded đa dạng |
| `data-visualization` | Biểu đồ matplotlib/seaborn/plotly đạt chất lượng công bố | Hình/biểu đồ in được |
| `theme-factory` | Áp theme màu/font cho artifact (slide, docs, report, landing) | Artifact đồng bộ theme |
| `engineering-discipline` | Kỷ luật kỹ thuật & bài học đã trả giá: verify trước khi báo xong, kiểm server/DB trước khi kết luận bug, an toàn migration, secrets từ env, UTF-8, dead code, doc-sync, rollback an toàn | Checklist kỷ luật + bảng lỗi→cách tránh |

## Routing — ý định người dùng → skill

```text
"điều phối sơ đồ / chọn công cụ vẽ sơ đồ / diagram orchestrator / sơ đồ cây / trie / bk-tree" → diagram-orchestrator
"viết báo cáo / sửa file Word / đồ án / luận văn"        → docx-report
"sửa docx an toàn / thay ảnh docx / sửa chữ docx ko gen lại / sửa file word hoàn thiện" → safe-docx-modifier
"viết như người / tự nhiên hơn / đỡ giống AI / đổi văn phong" → human-report-writing
"làm slide / thuyết trình / PowerPoint / bảo vệ"          → pptx-deck
"tạo slide từ tài liệu / PDF sang PPT / làm đẹp slide / beautify PPTX / tái tạo slide từ ảnh / ppt-master" → ppt-master
"sơ đồ đẹp / kiến trúc hiện đại / tldraw / đường cong mượt" → tldraw-diagrams
"vẽ sơ đồ / UML / ERD / use case / sequence / chuẩn kỹ thuật / plantuml" → plantuml-diagrams
"bố cục use case / use case gọn đẹp / đường nối use case sạch / không vẽ vòng xa / use case layout / actor 2 bên" → use-case-layout
"sơ đồ tối giản / đơn giản hơn / ít bảng hơn / sơ đồ khái niệm / sơ đồ bảo vệ / conceptual" → simplified-diagrams
"audit sơ đồ / kiểm tra sơ đồ / soi ảnh diagram / sơ đồ bị méo / sửa ảnh sơ đồ" → diagram-auditor
"nghiên cứu / tìm hiểu / tổng hợp / so sánh công nghệ"   → research-report
"đọc PDF / trích PDF / OCR / chuyển sang PDF"            → pdf-toolkit
"Excel / bảng tính / số liệu / biểu đồ Excel"            → xlsx-sheet
"thiết kế UI / làm lại giao diện / đừng giống AI / anti-slop / unslop" → anti-slop
"lập/audit tài liệu dự án / README / CONTEXT / AGENTS.md / tài liệu lệch / doc-architect" → doc-architect
"ADR / ghi vết quyết định / living docs / PRD / supersede"  → living-docs
"tri thức OKF / knowledge bundle / frontmatter type"        → okf-knowledge-format
"tài liệu kỹ thuật / API docs / runbook / developer guide"  → documentation
"đồng soạn tài liệu / proposal / spec / co-author"          → doc-coauthoring
"nghiên cứu chủ đề / gom nguồn / lưu báo cáo nghiên cứu"    → research / research-report / research-artifacts
"soát văn phong tài liệu / writing guidelines / prose"      → writing-guidelines
"file Word .docx / template Word .dotx"                     → docx (hoặc docx-report)
"file PowerPoint .pptx / template .potx"                    → pptx (hoặc pptx-deck)
"file PDF / OCR / điền form PDF / ghép PDF"                 → pdf (hoặc pdf-toolkit)
"Excel / CSV / TSV / .xlsx"                                 → xlsx (hoặc xlsx-sheet)
"vẽ đa dạng sơ đồ / diagram design / gantt / sankey / kiến trúc" → diagram-design
"biểu đồ số liệu / chart công bố / matplotlib / plotly"     → data-visualization
"đổi theme màu/font cho slide/tài liệu/báo cáo"             → theme-factory
"debug lỗi khó / trước khi báo xong / đổi schema-migration / 500 / mojibake / checklist trước commit" → engineering-discipline
```

Kết hợp nhiều skill khi cần. Ví dụ điển hình cho đồ án:

```text
research-report    → thu thập & xác minh nguồn
plantuml-diagrams  → vẽ Use Case / ERD / Sequence / Class chuẩn mực UML 100%
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
7. **Phân định rạch ròi Ảnh chụp (Screenshots) vs. Sơ đồ (Diagrams)**:
   - `screenshots/`: 100% CHỈ chứa ảnh chụp màn hình UI thực tế của phần mềm (`01_*.png` ...). Tuyệt đối CẤM để sơ đồ hoặc file `.puml`/`.dot` vào đây.
   - `diagrams/`: Chứa toàn bộ mã nguồn sơ đồ (`.puml`, `.dot`, `.tldr`) và file xuất vector/raster (`.svg`, `.png`).
   - CẤM xả mã nguồn sơ đồ (`.puml`, `.dot`) ra chat làm tràn màn hình; chỉ lưu file trên đĩa, nhúng ảnh render và dẫn link.
8. **Kỷ luật thư mục công cụ (Dedicated Tools Directory — Không giải rác)**:
   - Mọi script bổ trợ kiểm tra, sửa docx, hoán đổi ảnh, inspect hay render BẮT BUỘC phải nằm trong thư mục `tools/` (hoặc `docs/tools/`) của dự án.
   - Tuyệt đối CẤM tạo các script lẻ tẻ (`replace_docx_*.py`, `inspect_*.py`, `apply_*.py`) rải rác ở thư mục gốc (`root`) của dự án.
9. **Phân tách 2 không gian tài liệu (Dual Docs Architecture)**:
   - Tách biệt rõ ràng 2 mục đích tài liệu:
     - **Tài liệu Báo cáo học thuật / BTL (`reports/` hoặc `docs/report/`)**: Phục vụ in ấn, nộp bài, chấm điểm đồ án (file `.docx`, slide bảo vệ, rubric).
     - **Tài liệu Dự án Mã nguồn mở (`docs/`)**: Phục vụ phát hành open-source lâu dài (Architecture, Developer Guide, API Reference, User Manual, Contributing Guide, Screenshots). Không để file nháp/báo cáo học thuật làm ô nhiễm tài liệu mã nguồn mở.
10. **Verify trước khi báo xong (Evidence-before-Done)** — không tuyên bố hoàn thành chỉ vì "trông đã xong": phải **chạy thật + có bằng chứng** (build PASS, log, ảnh chụp thật). Khi nghi lỗi code, **kiểm tra server + DB đang chạy trước khi kết luận** (500 / `ERR_CONNECTION_REFUSED` thường do backend/DB tắt, không phải bug logic).
11. **Không placeholder / không bịa số liệu** — không ship UI trống rỗng hay ảnh placeholder vô nghĩa; empty state phải là lời mời hành động; ảnh đưa vào báo cáo/slide phải là **ảnh thật**, khung **16:9** (không full-page dài).
12. **An toàn khôi phục & hỏi trước khi phá** — tạo git tag/nhánh trước khi xoá/đổi lớn; **stash** thay vì xoá WIP; **hỏi trước** khi đổi schema/phá cấu trúc; **chỉ commit khi được yêu cầu**. Sau thay đổi lớn → **đồng bộ tài liệu** (CONTEXT / CHANGELOG / DOMAIN_INVARIANTS) để chống drift.

## Toolchain & cài đặt

Đã có sẵn: `python`, `node`, `npm`, `npx`, `git`.
Cần cài thêm tùy nhu cầu:

```bash
pip install python-docx python-pptx openpyxl xlsxwriter pandas pymupdf pdfplumber pypdf reportlab

# LibreOffice — bắt buộc cho render QA (docx/pptx/xlsx recalc)
winget install TheDocumentFoundation.LibreOffice

# PlantUML CLI / Kroki (dùng scripts/render-puml.mjs có sẵn, không cần cài Java)
# Hoac cai Graphviz + Java neu muon render local offline
winget install Graphviz.Graphviz

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
