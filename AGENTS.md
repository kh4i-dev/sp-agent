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
2. **Chọn skill**: tra bảng **Routing** (ý định → skill) bên dưới. Nhiều việc → nạp nhiều skill, phối hợp. **Việc lớn** (đồ án/báo cáo, slide, sơ đồ, nghiên cứu, tài liệu) → nạp `skill-coordinator` **trước tiên** để có bản đồ + giao thức phối hợp (tránh dùng lẻ 1 skill).
3. **Nạp**: gọi công cụ `skill` với đúng `name` (trùng tên thư mục). Nếu không có công cụ đó → `Read` thẳng `.claude/skills/<name>/SKILL.md`.
4. **Đọc ĐẦY ĐỦ**: đọc trọn `SKILL.md`; cần chi tiết thì mở tiếp `reference/` rồi `scripts/` (progressive disclosure). **Không đoán**, không bỏ qua phần "bất biến / IRON RULE / GATE".
5. **Thực thi theo skill** + tuân thủ "Nguyên tắc bất biến" (cuối file này). Trong khi thực thi, nếu gặp lỗi/biến chứng mà skill CHƯA nói đến → đóng góp bài học ngược lại vào skill theo `skill-feedback` (xác minh trước khi ghi).
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

## Block coordinators (điều phối theo khối — nạp NHANH)

Khi việc thuộc một khối rõ ràng, **nạp coordinator của khối đó** thay vì quét cả bộ skill:

| Khối | Coordinator | Thành viên chính |
|---|---|---|
| Báo cáo/đồ án Word (.docx) | `coord-report` | docx-report, human-report-writing, safe-docx-modifier, docx, human-md-audit |
| Tài liệu dự án & viết/sửa docs | `coord-docs` | doc-architect, living-docs, okf-knowledge-format, documentation, documentation-and-adrs, doc-coauthoring, writing-guidelines |
| Sơ đồ kỹ thuật | `coord-diagrams` | handdrawn-diagrams, diagram-orchestrator, plantuml-diagrams, tldraw-diagrams, simplified-diagrams, use-case-layout, diagram-design, diagram-auditor, diagram-pack |
| Slide / thuyết trình | `coord-slides` | pptx-deck, pptx, ppt-master, pptx-phan-tich-bai-toan, theme-factory, anti-slop |
| Dữ liệu (Excel/PDF/biểu đồ) | `coord-data` | xlsx-sheet, xlsx, pdf-toolkit, pdf, data-visualization |
| Nghiên cứu | `coord-research` | research-report, research, research-artifacts |

## Skill index

| Skill | Dùng khi | Đầu ra chính |
|---|---|---|
| `skill-coordinator` | **Nạp ĐẦU TIÊN cho việc lớn** (đồ án/báo cáo, slide, sơ đồ, nghiên cứu, tài liệu): bản đồ toàn bộ skill + giao thức phối hợp, tránh dùng lẻ 1 skill (như chỉ `docx-report`) | Chuỗi skill phối hợp đúng + cổng kiểm (gate) |
| `docx-report` | Viết/sửa/audit file Word, báo cáo, đồ án, luận văn | `.docx` đúng cấu trúc, đã render kiểm tra |
| `safe-docx-modifier` | Chỉnh sửa an toàn file Word khi đã hoàn thiện (Zero Regeneration), thay ảnh in-place, sửa text bảo toàn Runs | `.docx` giữ 100% định dạng, ảnh và nội dung cập nhật |
| `human-report-writing` | Biên tập văn phong báo cáo cho tự nhiên như người, bỏ dấu hiệu văn AI | Văn xuôi tự nhiên, có Tóm tắt chương |
| `human-md-audit` | Vòng lặp nhanh: humanize văn xuôi, xuất Markdown review, audit cấu trúc Word bằng XML/text | Markdown review + FAST-CHECK PASS/FAIL, render ảnh chỉ ở gate cuối |
| `pptx-deck` | Làm slide, thuyết trình, PowerPoint cơ bản | `.pptx` biên tập được, chart native |
| `pptx-phan-tich-bai-toan` | Slide **chương phân tích bài toán** (đặt vấn đề → mục tiêu → phạm vi → phân tích → so sánh ưu/nhược): ít sơ đồ (chỉ sơ đồ chính), ảnh chụp THẬT, chữ vừa phải, **layer biên tập được**, chống "mùi AI", học thuật | `.pptx` native (shape đặt tên) + spec JSON + render QA |
| `ppt-master` | Chuyển tài liệu (PDF, Word, Markdown) thành slide PowerPoint native đẳng cấp, tái tạo slide từ ảnh, làm đẹp (beautify) deck, animation/transition native, audio narration TTS | `.pptx` native shapes/connectors, slide masters, audio narration |
| `diagram-orchestrator` | Điều phối sơ đồ theo giao thức tư duy thông minh (Intelligent Problem-Solving Protocol), chọn đúng công cụ theo ngữ nghĩa | Sơ đồ chuẩn xác theo công cụ tối ưu, có bằng chứng nghiệm thu |

| `handdrawn-diagrams` | **MẶC ĐỊNH CHO MỌI SƠ ĐỒ**: vẽ tay SVG bằng Python với toạ độ cứng (không PlantUML/Mermaid/Graphviz/drawio cho bản nộp), tách `vectors/*.svg` khỏi `images/*.png`, kiểm định tất định E1..E6 + selftest chống False PASS | `gen_*.py` + `vectors/*.svg` + `images/*.png` + audit PASS |
| `plantuml-diagrams` | **CHỈ LÀM NHÁP** (draft) để nghĩ bố cục + bộ luật UML/zero-color/state-playbook đáng giữ. Không dùng làm file cuối — render cuối phải qua `handdrawn-diagrams` | `.puml` nháp + luật UML/zero-color |
| `use-case-layout` | Use Case UML đúng nghiệp vụ + bố cục lane GỌN-ĐẸP-DỄ NHÌN, **cấm connector vòng xa**, **cấm đường nối xuyên qua tên actor**; **vẽ tay (draw.io/SVG) là mặc định bắt buộc**; **duyệt bố cục = MẮT SOI ẢNH Ở ĐỘ PHÓNG ĐẠI**: chạy `scripts/eye_audit.py --overlay --dump` (sinh ứng viên + **zoom crop 4×** + **overlay lưới 10×10**) rồi **MỞ** ảnh và phán thật/báo oan; **cấm gen hàng loạt** | `.drawio`/`.puml` + PNG/SVG + `*-audit.md` + `*-audit/overlay.png` + `*-audit/crops/F*.png` |
| `simplified-diagrams` | Sơ đồ tinh gọn / Khái niệm (Conceptual) cho thuyết trình & bảo vệ đồ án, 5-8 thực thể cốt lõi | `.puml`, SVG/PNG nét thẳng chuẩn + Kịch bản phát biểu 60s |
| `diagram-auditor` | Audit và kiểm định chất lượng sơ đồ (chống banner cảnh báo, chống méo lệch, chống đè nhãn, đủ SVG/PNG, hiển thị ảnh + tiêu đề Hình X.X, cấm xả code nguồn) | Báo cáo kiểm định PASS/FAIL + Ảnh sơ đồ & Tiêu đề Hình X.X |
| `diagram-pack` | Đóng gói toàn bộ vòng đời sơ đồ vào MỘT thư mục đích: code nguồn → `diagrams/`, ảnh render `.svg`+`.png` 1:1 → `images/diagrams/`, dấu vết soi mắt → `audit/soi-so-do/`, Bước 0 → `domain/`; quy tắc chống đè/chồng/vòng xa; vòng sửa = sửa nguồn → render lại chỉ hình ảnh hưởng → soi lại | Pack đạt contract + `check_pack.py` PASS (cặp 1:1, audit đủ overlay+crops) |
| `tldraw-diagrams` | Sơ đồ kiến trúc, flowchart, luồng dữ liệu thẩm mỹ cao, đường cong mềm mại | `.tldr`, `.svg`, `.png` (2x) hiện đại, chỉnh sửa được |
| `research-report` | Nghiên cứu, tổng hợp, fact-check, dẫn nguồn | Báo cáo có citation đã xác minh |
| `pdf-toolkit` | Đọc/trích/tạo/OCR/ghép PDF | Text/bảng/ảnh, PDF mới |
| `xlsx-sheet` | Bảng tính Excel, số liệu, biểu đồ | `.xlsx` đã recalc công thức |
| `anti-slop` | Thiết kế/làm lại UI, audit giao diện, chống "AI slop", bố cục slide/dashboard | Giao diện có chủ đích, qua anti-slop gate |
| `doc-architect` | Lập/audit/đồng bộ bộ tài liệu dự án (README, AGENTS.md, docs/, CONTEXT), chống drift tài liệu | Tài liệu đầy đủ, qua Fresh Session Test |
| `living-docs` | ADR/MADR, PRD, ghi vết quyết định (supersede, never delete), sơ đồ kiến trúc Mermaid sống | Nhật ký quyết định + sơ đồ sống |
| `okf-knowledge-format` | Đóng gói/chuẩn hóa tri thức theo OKF (bundle markdown + frontmatter `type`) | Bundle tri thức chuẩn OKF |
| `project-handbook` | Viết **SỔ TAY DỰ ÁN** cho người khác hiểu trọn dự án (bài toán, thuật ngữ, máy trạng thái, đường đi của tiền, **đặc tả từng trường hợp theo bảng Đầu vào–Xử lý hệ thống–Đầu ra–Nhánh lỗi**, kịch bản chạy suốt, bảng mã lỗi, hạn chế đã biết, bảng kiểm phủ) từ **mã nguồn thật**, rồi **xuất PDF** A4 có bìa/mục lục/số trang | `.md` + `.pdf` + `-nguon.md` (bảng truy vết `file:dòng`) + ảnh render bìa/trang bảng |
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
| `skill-feedback` | Agent chạy theo skill gặp lỗi/biến chứng mà skill CHƯA nói đến → xác minh, chống trùng, đóng góp bài học ngược lại vào skill đó | Entry bài học trong skill + dòng mới ở lessons-learned + mirror đã sync |

## Routing — ý định người dùng → skill

```text
"điều phối skill / chọn skill / nạp skill / phối hợp skill / bắt đầu việc lớn / không biết dùng skill nào / quy trình đồ án" → skill-coordinator
"viết báo cáo / sửa báo cáo / đồ án / luận văn Word (.docx)" → coord-report
"viết docs / sửa docs / README / AGENTS.md / ADR / PRD / tài liệu dự án / OKF" → coord-docs
"sơ đồ / UML / ERD / use case / kiến trúc / flowchart (khối sơ đồ)" → coord-diagrams
"vẽ tay hết / không dùng PlantUML / không dùng công cụ ngoài / sơ đồ vẽ xấu / cần toạ độ cứng / eye audit không cần mắt" → handdrawn-diagrams
"slide / thuyết trình / PowerPoint / deck / bảo vệ (khối slide)" → coord-slides
"Excel / bảng tính / PDF / biểu đồ / số liệu (khối dữ liệu)" → coord-data
"nghiên cứu / tổng hợp / literature review / fact-check (khối nghiên cứu)" → coord-research
"điều phối sơ đồ / chọn công cụ vẽ sơ đồ / diagram orchestrator / sơ đồ cây / trie / bk-tree" → diagram-orchestrator
"viết báo cáo / sửa file Word / đồ án / luận văn"        → docx-report
"sửa docx an toàn / thay ảnh docx / sửa chữ docx ko gen lại / sửa file word hoàn thiện" → safe-docx-modifier
"viết như người / tự nhiên hơn / đỡ giống AI / đổi văn phong" → human-report-writing
"sửa văn giống người / xuất markdown review / audit word nhanh / kiểm docx nhanh không ảnh / fast audit" → human-md-audit
"làm slide / thuyết trình / PowerPoint / bảo vệ"          → pptx-deck
"slide phân tích bài toán / slide đặt vấn đề / slide bảo vệ phần phân tích / slide đồ án ít chữ / slide đừng giống AI / bảng ưu nhược điểm / kịch bản slide đồ án" → pptx-phan-tich-bai-toan
"tạo slide từ tài liệu / PDF sang PPT / làm đẹp slide / beautify PPTX / tái tạo slide từ ảnh / ppt-master" → ppt-master
"sơ đồ đẹp / kiến trúc hiện đại / tldraw / đường cong mượt" → tldraw-diagrams
"vẽ sơ đồ / UML / ERD / use case / sequence / chuẩn kỹ thuật / plantuml" → plantuml-diagrams
"bố cục use case / use case gọn đẹp / đường nối use case sạch / không vẽ vòng xa / use case layout / actor 2 bên / vẽ use case bằng tay / line đè lên chữ / sơ đồ bị lệch / cần soi kỹ sơ đồ bằng mắt / zoom soi sơ đồ" → use-case-layout
"sơ đồ tối giản / đơn giản hơn / ít bảng hơn / sơ đồ khái niệm / sơ đồ bảo vệ / conceptual" → simplified-diagrams
"audit sơ đồ / kiểm tra sơ đồ / soi ảnh diagram / sơ đồ bị méo / sửa ảnh sơ đồ" → diagram-auditor
"gen sơ đồ dự án / pack sơ đồ / gói sơ đồ / ảnh ra ảnh code ra code / thư mục sơ đồ / sửa sơ đồ rồi render lại / sơ đồ chồng nhau đè nhãn / check pack" → diagram-pack
"nghiên cứu / tìm hiểu / tổng hợp / so sánh công nghệ"   → research-report
"đọc PDF / trích PDF / OCR / chuyển sang PDF"            → pdf-toolkit
"Excel / bảng tính / số liệu / biểu đồ Excel"            → xlsx-sheet
"thiết kế UI / làm lại giao diện / đừng giống AI / anti-slop / unslop" → anti-slop
"viết tài liệu hướng dẫn dự án / sổ tay dự án / tài liệu cho người mới hiểu dự án / tài liệu bàn giao / giải thích toàn bộ quy trình nghiệp vụ / liệt kê đầy đủ các trường hợp đầu vào–xử lý–đầu ra / xuất tài liệu md ra PDF" → project-handbook
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
"gặp lỗi khi dùng skill / skill chưa nói lỗi này / tìm ra cách làm khác tài liệu / đóng góp bài học vào skill / ghi pitfall / skill feedback" → skill-feedback
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
   - `docs/screenshots/` (hoặc `screenshots/` nếu repo không dùng `docs/`): 100% CHỈ chứa ảnh chụp màn hình UI thực tế của phần mềm (`01_*.png` ...). Tuyệt đối CẤM để sơ đồ hoặc file `.puml`/`.dot` vào đây.
   - `docs/diagrams/` (hoặc `diagrams/`): Chứa toàn bộ mã nguồn sơ đồ (`.puml`, `.dot`, `.tldr`) và file xuất vector/raster (`.svg`, `.png`). Đây là **path canonical** cho mọi skill sơ đồ.
   - CẤM xả mã nguồn sơ đồ (`.puml`, `.dot`) ra chat làm tràn màn hình; chỉ lưu file trên đĩa, nhúng ảnh render và dẫn link.
8. **Kỷ luật thư mục công cụ (Dedicated Tools Directory — Không giải rác)**:
   - Mọi script bổ trợ kiểm tra, sửa docx, hoán đổi ảnh, inspect hay render BẮT BUỘC phải nằm trong thư mục `tools/` (hoặc `docs/tools/`) của dự án.
   - Tuyệt đối CẤM tạo các script lẻ tẻ (`replace_docx_*.py`, `inspect_*.py`, `apply_*.py`) rải rác ở thư mục gốc (`root`) của dự án.
9. **Phân tách 2 không gian tài liệu (Dual Docs Architecture)**:
   - Tách biệt rõ ràng 2 mục đích tài liệu:
     - **Tài liệu Báo cáo học thuật / BTL (`reports/` hoặc `docs/report/`)**: Phục vụ in ấn, nộp bài, chấm điểm đồ án (file `.docx`, slide bảo vệ, rubric).
     - **Tài liệu Dự án Mã nguồn mở (`docs/`)**: Phục vụ phát hành open-source lâu dài (Architecture, Developer Guide, API Reference, User Manual, Contributing Guide, Screenshots). Không để file nháp/báo cáo học thuật làm ô nhiễm tài liệu mã nguồn mở.
10. **Verify trước khi báo xong (Evidence-before-Done)** — không tuyên bố hoàn thành chỉ vì "trông đã xong": phải **chạy thật + có bằng chứng** (build PASS, log, ảnh chụp thật). Khi nghi lỗi code, **kiểm tra server + DB đang chạy trước khi kết luận** (500 / `ERR_CONNECTION_REFUSED` thường do backend/DB tắt, không phải bug logic).
    - **CỔNG PASS HAI ĐIỀU KIỆN (áp cho CẢ `.docx`, ảnh sơ đồ `.png/.svg`, và file python sinh sơ đồ `.py`) — THIẾU MỘT = FAIL:**
      1. **MÁY (Automated):** chạy/render thật — audit script **0 lỗi đỏ**; **file nguồn (`.py` generator / `.puml` / `.dot` / `.tldr`) TỒN TẠI**; **file ảnh (`.png` + `.svg`) TỒN TẠI > 500 bytes**; DOCX render ra **PDF + PNG từng trang**, field TOC/TOF/TOT/PAGE tự cập nhật.
      2. **VISION AUDIT (Agent Visual QA):** agent **có VISION (multimodal) SOI ẢNH THẬT** bằng công cụ đưa pixel vào ngữ cảnh model (không phải read text), ghi **Proof-of-View: ≥3 nhãn nguyên văn + vị trí + kết luận rõ "sắp xếp đã hợp lý chưa" + "Vision audit by: <model-id>"**. Model text-only **không được tính**.
    - **Ba luật chặn:** chỉ chạy script → `FAIL — visual QA missing`; chỉ nhìn ảnh mà script còn lỗi/thiếu file → `FAIL — automated gate not met`; **ảnh có mà thiếu file nguồn `.py`/`.puml`/`.dot` = FAIL** (không tái lập được); **audit bằng model text-only (không vision) = FAIL** (không có chứng kiến thực tế). Chi tiết: `diagram-auditor` §1.5–§2 và `docx-report` mục RENDER & VISUAL QA.
    - **Riêng SƠ ĐỒ — bắt buộc SOI ẢNH (anti-rush):** trước mọi `PASS`/`xong`, phải **nạp file `.png` vào ngữ cảnh model** (đọc chính file ảnh) và dán Proof-of-View (≥3 nhãn nguyên văn + vị trí + đè?/đều?/dễ nhìn?). Không trích được 3 nhãn = **chưa xem ảnh = cấm PASS**; "render exit 0"/"script 0 đỏ" không thay được mắt soi. **Phải là VISION AUDIT — model text-only không tính**; nếu model hiện tại không đọc được ảnh → giao cho vision subagent/model, không có vision nào → `BLOCKED — Vision Audit unavailable`. Thiếu công cụ xem ảnh → `BLOCKED — Visual QA unavailable`.
    - **Và phải soi Ở ĐỘ PHÓNG ĐẠI, không chỉ một cái liếc 100%:** ở tỉ lệ chèn A4 (~15 cm) một đoạn nét xuyên qua chữ chỉ dày 1–2 px nên **mắt thường bỏ sót** (đã xảy ra thật: đường association cắt ngang tên actor mà liếc ảnh 100% không thấy). Quy trình bắt buộc 3 nhịp: (1) chạy `use-case-layout/scripts/eye_audit.py --overlay --dump` để sinh **ứng viên** + **crop zoom 4×** + **overlay lưới 10×10**; (2) **mở** `overlay.png` và **mọi** `crops/F*.png` rồi phán `THAT`/`BAO-OAN`/`CHAP-NHAN-DUOC` cho từng ứng viên; (3) điền bảng bằng chứng vào `*-audit.md`. **CẤM gen hàng loạt**: mỗi hình một vòng nghiệm thu riêng với dấu vết riêng; cấm tuyên bố "N hình đều đạt" khi thiếu dấu vết soi cho từng hình. Chỉ chạy script rồi PASS = **vi phạm** (script báo oan được); chỉ liếc 100% = **vi phạm** (đã chứng minh là bỏ sót). SSOT: `use-case-layout/reference/visual-audit-protocol.md`.
11. **Không placeholder / không bịa số liệu** — không ship UI trống rỗng hay ảnh placeholder vô nghĩa; empty state phải là lời mời hành động; ảnh đưa vào báo cáo/slide phải là **ảnh thật**, khung **16:9** (không full-page dài). Với tài liệu đang soạn, scaffold tạm (`TBD`, `[To be written]`) **được phép trong phiên** nhưng KHÔNG được ship; `living-docs check` chặn riêng cú pháp `{{PLACEHOLDER}}`.
12. **An toàn khôi phục & hỏi trước khi phá** — tạo git tag/nhánh trước khi xoá/đổi lớn; **stash** thay vì xoá WIP; **hỏi trước** khi đổi schema/phá cấu trúc; **chỉ commit khi được yêu cầu**. Sau thay đổi lớn → **đồng bộ tài liệu** (CONTEXT / CHANGELOG / DOMAIN_INVARIANTS) để chống drift.
13. **Sơ đồ — VẼ TAY 100%, toạ độ cứng, kiểm định tất định** (quyết định 2026-11-01, thay thế cách chọn công cụ cũ):
    - **MỌI sơ đồ kỹ thuật đều VẼ TAY bằng SVG sinh từ Python với toạ độ hằng số** (`handdrawn-diagrams`). Lý do người dùng nêu: PlantUML/Mermaid/công cụ ngoài **vẽ xấu và khó kiểm soát**. → PlantUML/Mermaid/Graphviz/drawio **chỉ được dùng làm NHÁP**, không bao giờ là file cuối chèn vào Word/Slide.
    - **Báo cáo/đồ án/luận văn học thuật → TRẮNG-ĐEN (zero-color)**. **Cấm sơ đồ màu** trong báo cáo học thuật. Bản branded/marketing → `diagram-design`, `theme-factory` (được màu).
    - **Hợp đồng thư mục (bắt buộc, mỗi định dạng MỘT thư mục riêng):** `docs/diagrams/` = nguồn (`gen_*.py`) · `docs/diagrams/spec/` = **`.json` duy nhất** · `docs/diagrams/vectors/` = **`.svg` duy nhất** · `docs/diagrams/drawio/` = **`.drawio` duy nhất** · `docs/images/diagrams/` = **`.png` duy nhất**. **Cấm** để `.svg`/`.drawio` trong thư mục PNG, cấm `.png` trong `vectors/`.
    - **Use Case — LUẬT "1 ĐIỂM XUẤT PHÁT + ĐƯỜNG THẲNG"** (sửa 2026-11-01, thay luật "bụng + vòng cung"): mọi association của một actor xuất phát từ **đúng một điểm ở khuỷu tay** (junction thân–tay `(ax, ay−4)`), mỗi cạnh là **đoạn thẳng** `<line>` tới mép ellipse — **cấm cung Bezier cho dây nối**. Lý do: *"vòng cung" là hình ELLIPSE (chức năng), không phải dây nối*; và tia đi lên từ bụng **cắt ngang cánh tay** (đo được 1 cạnh vi phạm). `include`/`extend`: nét đứt + mũi tên hở theo dây cung. `CURVE = 0.0` (bật `>0` chỉ khi được yêu cầu rõ).
    - **Toạ độ phải là hằng số trong code** (không random, không auto-layout ngẫu nhiên). Cùng input → cùng ra đúng từng pixel. Mẫu: `handdrawn-diagrams/reference/coordinate-workflow.md`.
    - **Cổng kiểm định bắt buộc trước khi chèn:** `audit_svg.py` (E1..E6: ngoài khung, nhãn đè, dây cắt nhãn, chữ tràn hình, id trùng, text rỗng) + `verify_box_layout.py` cho sơ đồ hộp (E1..E4 hình học) → **phải 0 lỗi**. Kèm `selftest_audit_svg.py` để chứng minh bộ kiểm **không phải đồ giả** (chống False PASS).
    - **Visual QA phải trung thực:** script chỉ đo được hình học. Nhịp cuối (thẩm mỹ/ngữ nghĩa) cần **người** hoặc **model có vision**. Nếu không xem được ảnh → ghi `Visual QA unavailable`, **CẤM bịa Proof-of-View** ("tôi thấy nhãn X ở …").
    - **Use Case / State Machine / Activity** vẫn giữ luật riêng trong `use-case-layout` và `plantuml-diagrams/reference/state-playbook.md` (nhãn sự kiện trên cạnh, không note/legend/footer trên canvas, final không có cạnh ra) — nhưng cách **render** giờ là vẽ tay SVG, không PlantUML.

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

Kiểm tra nhanh: `powershell -File tools/check-tools.ps1`. Kiểm định toàn bộ skill (frontmatter + audit tự động theo khối): `powershell -ExecutionPolicy Bypass -File tools/check-all.ps1` (chi tiết: `docs/workflow-audit-skills.md`).

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

## Bố cục Use Case theo ảnh mẫu (2026-11-01)

Khi vẽ Use Case, đọc SSOT `.claude/skills/use-case-layout/reference/actor-function-composition.md`: phân actor theo vai trò đã xác minh, chọn trái/phải theo cụm chức năng (bên phải không chỉ dành cho dịch vụ ngoài), giữ người que tỷ lệ bình thường; association ưu tiên tia thẳng chung gốc ở junction thân–tay `(ax, ay−4)`, ellipse lệch theo cụm như ảnh mẫu. Không kéo actor cao theo cột UC, không bắt buộc rải neo/bus/cong dây, không ép toàn bộ chức năng vào một cột dài. Quạt chung gốc không tự động là lỗi C-FAN; vẫn soi ảnh phóng đại để kiểm từng cạnh và nhãn.

## State Machine: cổng chống mô hình sai và chú thích (2026-11-01)

Trước khi vẽ/audit State, đọc `.claude/skills/plantuml-diagrams/reference/state-playbook.md`. Chọn rõ declared/as-is/to-be; đối chiếu ma trận với service ghi trạng thái, không đếm đủ cạnh rồi nhận là đã triển khai. Canvas chỉ chứa phần tử/nhãn UML, cấm note/legend/footer/chữ thuyết minh dù không có hộp. State có tên Hoàn tất còn cạnh ra vẫn là state thường; final bullseye không cạnh ra, không dùng chữ nhật viền đôi. Composite chỉ gom exit chung có bằng chứng và phải mở rộng kiểm đủ cạnh. Không áp máy móc guard đối nhau cho event khác nhau, không ép mọi cạnh initial/completion có nhãn. Chạy bộ kiểm model và render + soi phóng đại trước kết luận.
