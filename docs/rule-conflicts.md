# Baseline chống mâu thuẫn quy tắc giữa các skill

Mục đích: ghi lại **bản đồ mâu thuẫn quy tắc liên skill** đã audit và **cách chốt** (scope/owner), để lần sau không tái phát và có cơ sở đối chiếu khi sửa skill.

- Ngày chốt baseline: **2026-10-14**
- Phạm vi audit: 33 skill trong `.claude/skills/` (mirror `.agents/skills/` chỉ đọc bản `.claude`).
- Cách chạy lại audit: dùng sub-agent đọc `AGENTS.md` (13 nguyên tắc bất biến) + `SKILL.md`/`reference/` của các skill cùng miền, đối chiếu **cặp quy tắc cùng chủ đề**, trích nguyên văn `file:line`.
- Sau mọi thay đổi skill: chạy `tools/sync-skills.ps1` rồi `tools/verify-skills.ps1`.

## A. Nguyên tắc chung đã áp dụng

1. **Khai báo phạm vi (scope) thay vì xoá luật gốc** — mỗi skill tự nói rõ nó áp cho ngữ cảnh nào; hai skill khác ngữ cảnh thì **loại trừ nhau**, không mâu thuẫn.
2. **Chỉ định bên sở hữu (owner)** cho chủ đề bị nhiều skill cùng định nghĩa; skill còn lại **defer/trỏ về** owner.
3. **SSOT cho hệ sơ đồ** = `diagram-orchestrator/SKILL.md` (khối "ĐỒNG BỘ QUY TẮC LIÊN SKILL").

## B. Sổ đăng ký mâu thuẫn & trạng thái

Trạng thái: **FIXED** = đã đồng bộ; **BY-DESIGN** = khác ngữ cảnh, không phải lỗi.

| ID | Chủ đề | Các bên | Mức | Trạng thái | Cách chốt |
|---|---|---|---|---|---|
| PROSE-1 | Dấu em dash `—` | `human-report-writing` ↔ `docx-report`, `ppt-master` | HIGH | FIXED | `docx-report` mang luật cấm + defer; `ppt-master` nêu rõ luật raw-Unicode chỉ là *hình thức ký tự SVG* |
| PROSE-2 | Bold / bullet / ngôi kể / heading | `writing-guidelines` (Vercel) ↔ `human-report-writing` | HIGH | FIXED | Scope: `writing-guidelines` = docs sản phẩm (EN); báo cáo học thuật dùng `human-report-writing` |
| PROSE-3 | Vị trí caption bảng (trên/dưới) | `docx-report` ↔ `human-report-writing/checklist.md` | HIGH | FIXED | Tuỳ quy định trường; mặc định `docx-report` = dưới bảng; hình luôn caption dưới |
| DIAG-1 | Ý nghĩa "chỉ dùng màu khi có quy ước" | `diagram-orchestrator/design-principles.md` ↔ zero-color hard-block | MED | FIXED | Bỏ ngoại lệ màu → zero-color tuyệt đối; phân biệt bằng nét đứt/`doublecircle`/stereotype |
| DIAG-2 | Ví dụ JSON có `color`/`title`; nhúng tiêu đề vào ảnh | `tldraw-diagrams` ↔ `plantuml`/`simplified`/`auditor` | HIGH | FIXED | Bỏ color+title khỏi ví dụ; thêm luật Zero-Title-in-Canvas; caption `Hình X.Y:` |
| DIAG-3 | Ngưỡng tỷ lệ khung doc vs script | `diagram-auditor` SKILL ↔ `audit-diagrams.mjs` | HIGH | FIXED | Khuyến nghị 0.5–2.4; **hard-fail** `>3.8` / `<0.28` — ghi rõ là cùng một luật |
| DIAG-4 | Bắt buộc cặp SVG+PNG | `diagram-auditor` ↔ `use-case-layout` | HIGH | FIXED | Pipeline học thuật luôn xuất cả SVG+PNG (`use-case-layout` đã sửa) |
| DIAG-5 | Path Bước 0 | `diagram-orchestrator`/`auditor` ↔ `use-case-layout` | HIGH | FIXED | Canonical `docs/domain/step0-<du-an>.md` (mọi skill dùng chung) |
| DIAG-6 | Nền trắng tinh vs warm-neutral | `plantuml`/`orchestrator` ↔ `diagram-design` | LOW-MED | BY-DESIGN | `diagram-design` là branded → ngoại lệ hợp lệ |
| DIAG-7 | Nơi lưu screenshots/diagrams | AGENTS #7 ↔ skills (`docs/...`) | MED | FIXED | Canonical `docs/screenshots/`, `docs/diagrams/` (hoặc không tiền tố nếu repo không dùng `docs/`) |
| DIAG-8 | Số node (≤15 / ≤9 / 7±2) | `plantuml`/`orchestrator`/`simplified`/`design-principles` | MED | FIXED | SSOT: chi tiết ≤15; trình chiếu ≤9; lõi khái niệm 7±2 |
| DIAG-9 | DPI 300 vs scale 2× | PlantUML/Graphviz ↔ tldraw/`diagram-design` | MED | FIXED | SSOT: 300 DPI cho PlantUML/Graphviz; 2× cho tldraw/diagram-design |
| DIAG-10 | Auto vs manual export; HTML self-contained | `orchestrator` ↔ `diagram-design` | LOW | BY-DESIGN | `diagram-design` = branded/HTML thủ công, ngoài pipeline `docs/diagrams/` |
| DIAG-11 | Ngưỡng chuyển công cụ / phân rã Use Case (≥3 actor/>12 UC vs >15) | `plantuml` ↔ `use-case-layout`/`orchestrator` | MED | FIXED | SSOT: >12 cân nhắc tách/vẽ tay; >15 bắt buộc phân rã |
| DIAG-12 | Accent tldraw (loopback/curve) vs cấm connector vòng xa | `tldraw` ↔ `use-case-layout` | MED | BY-DESIGN | tldraw không dùng cho Use Case; nếu dùng phải tránh vòng qua mép canvas |
| SLIDE-1 | Accent line / stripe dưới tiêu đề | `pptx`/`anti-slop` ↔ `ppt-master` templates | HIGH | FIXED | `ppt-master`: chỉ hợp lệ trong style/brand template tường minh, không cho deck học thuật |
| SLIDE-2 | Font "an toàn" (Georgia/Trebuchet/Palatino/Garamond/Consolas) | `pptx` ↔ `ppt-master` | HIGH | FIXED | "PPT-native safe" ≠ "LibreOffice-QA-safe"; nghi ngờ thì dùng Arial/Calibri/Cambria/TNR |
| SLIDE-3 | Render gate bắt buộc vs visual-review opt-in | AGENTS #2/`pptx`/`pptx-deck` ↔ `ppt-master` | HIGH | FIXED | Với đồ án/báo cáo trong repo này: **buộc bật visual-review** |
| SLIDE-4 | Scenario data | `anti-slop` Hard Gate ↔ `ppt-master` | MED | FIXED | Chỉ hợp lệ khi có nhãn hiển thị `Scenario data` |
| SLIDE-5 | Script nội bộ trong thư mục skill vs `tools/` | AGENTS #8 ↔ `ppt-master` | LOW | FIXED | Script đi kèm skill = package; script agent sinh thêm vẫn vào `tools/` |
| DOCS-1 | ADR location + Status (body vs frontmatter) | `documentation-and-adrs` ↔ `living-docs` | HIGH | FIXED | Khi dùng `living-docs` thì living-docs sở hữu (`docs/adr/NNNN-slug.md`, status frontmatter) |
| DOCS-2 | Placeholder `TBD`/`[To be written]` vs `{{PLACEHOLDER}}` | `doc-architect`/`doc-coauthoring` ↔ `living-docs check` | MED | FIXED | TBD tạm trong phiên, không ship; `check` chỉ chặn `{{PLACEHOLDER}}` (ghi ở AGENTS #11) |
| DOCS-3 | Template README (3 bản khác nhau) | `documentation`/`documentation-and-adrs`/`doc-architect` | MED | FIXED | `doc-architect` sở hữu template README; skill khác trỏ về |
| DOCS-4 | Hệ số xác minh nguồn (≥3 vs ≥2) + chuẩn trích dẫn (IEEE/APA vs NBR 6023) | `research-report` ↔ `research-artifacts` | MED | FIXED | Scope: research-report = báo cáo học thuật (≥3, IEEE/APA); research-artifacts = OKF bundle (≥2, NBR 6023) |
| DOCS-5 | Lề trên/dưới + Heading 3 in nghiêng (nội bộ `docx-report`) | `docx-report/reference/rules.md` ↔ `tnut-thesis-template-guide.md`; `human-report-writing/checklist.md` | MED | MỞ | Chốt theo mẫu trường (TNUT 2.5cm / H3 không nghiêng) — cân nhắc khi có mẫu trường cụ thể |
| SHEET-1 | Recalc Excel bắt buộc vs file Power Query/custom XML | `xlsx` ↔ `xlsx-sheet` | MED | FIXED | `xlsx`: thêm ngoại lệ chính thức — không recalc file Power Query/custom XML, hỏi người dùng |

## C. Bảo trì

- Trước khi thêm/sửa skill có chủ đề trùng với skill khác: kiểm tra bảng trên, chọn **scope** hoặc **owner**, không tạo luật đối nghịch.
- Chủ đề đã có SSOT (hệ sơ đồ): cập nhật tại `diagram-orchestrator` rồi để các skill khác defer, KHÔNG sửa rải rác.
- Mục còn **MỞ**: chốt khi có ngữ cảnh thực tế (mẫu trường/quy định cụ thể của người dùng).
