---
name: skill-coordinator
description: Bản đồ + giao thức điều phối TOÀN BỘ bộ skill sp-agent để các skill phối hợp và tôn trọng lẫn nhau, tránh dùng lẻ một skill (như chỉ `docx-report`) hoặc làm trái quy ước chung. Nạp khi bắt đầu bất kỳ việc lớn: viết báo cáo/đồ án/luận văn, làm slide, vẽ sơ đồ, nghiên cứu, xử lý Word/PDF/Excel, lập tài liệu dự án. Từ khóa kích hoạt: điều phối skill, chọn skill, nạp skill, phối hợp skill, quy trình đồ án, bắt đầu dự án tài liệu, không biết dùng skill nào.
---

# Skill Coordinator — Nhạc trưởng của bộ skill sp-agent

Nạp skill này **một lần** khi bắt đầu việc lớn để nắm: (a) bản đồ toàn bộ skill, (b) chuỗi
điều phối theo tình huống, (c) quy ước chung buộc mọi skill tôn trọng nhau.

**Nguyên tắc gốc:** KHÔNG dùng lẻ một skill rồi coi đó là "đã làm cả việc". Một báo cáo/đồ án
thật cần **nhiều skill phối hợp** (nội dung → sơ đồ → văn phong → dựng file → render). Chỉ gọi
`docx-report` là **thiếu** — nó chỉ lo khâu dựng/hình thức file `.docx`.

---

## 1. Bản đồ skill (chọn theo việc)

| Việc | Skill chủ | Skill phụ (bắt buộc/khi cần) |
|---|---|---|
| Báo cáo/đồ án/luận văn (.docx) | `docx-report` | `human-report-writing`, `diagram-orchestrator`, `caption-wording` (trong docx-report) |
| Sửa Word đã hoàn thiện | `safe-docx-modifier` | `docx-report` (khi cần chuẩn hóa) |
| Văn phong / bỏ giọng AI | `human-report-writing` | `docx-report`, `caption-wording` |
| Slide / thuyết trình | `pptx-deck` / `ppt-master` | `theme-factory`, `anti-slop`, `diagram-orchestrator` |
| Sơ đồ (UML/ERD/kiến trúc/flowchart) | `diagram-orchestrator` | `plantuml-diagrams` / `tldraw-diagrams` / `simplified-diagrams` / `use-case-layout` → **`diagram-auditor` (gate)** |
| Nghiên cứu / tổng hợp / dẫn nguồn | `research-report` | `research`, `research-artifacts`, `deep-research` (nếu có) |
| PDF | `pdf-toolkit` / `pdf` | — |
| Excel | `xlsx-sheet` / `xlsx` | `data-visualization` (biểu đồ) |
| Tài liệu dự án / ADR | `doc-architect`, `living-docs` | `okf-knowledge-format`, `documentation`, `documentation-and-adrs` |
| Thiết kế/bố cục (chống slop) | `anti-slop` | `theme-factory`, `diagram-design` |
| Kỷ luật kỹ thuật / debug | `engineering-discipline` | — |

> **Nạp nhanh theo khối:** nếu việc thuộc một khối rõ ràng, nạp thẳng **coordinator của khối đó** thay vì tự ghép:
> `coord-report` (báo cáo/đồ án Word) · `coord-docs` (tài liệu dự án, viết/sửa docs) · `coord-diagrams` (sơ đồ) · `coord-slides` (slide) · `coord-data` (Excel/PDF/biểu đồ) · `coord-research` (nghiên cứu).
> Mỗi coordinator tự khai báo thành viên + thứ tự nạp + cổng của khối mình.

---

## 2. Giao thức 1 lần nạp (BẮT BUỘC, làm đúng thứ tự)

1. **Đọc `AGENTS.md`** (đã tự nạp) — bảng Routing + "Nguyên tắc bất biến" là luật cao nhất.
2. **Nạp skill này** để có bản đồ, rồi **nạp các skill chủ/phụ** bằng công cụ `skill` (đúng `name`).
3. **Đọc trọn `SKILL.md`** của từng skill liên quan (đừng đoán); mở `reference/` → `scripts/` khi cần.
   Khi **sửa skill hoặc debug lỗi khó**, đọc thêm `docs/lessons-learned.md` (kho bài học xương máu:
   bẫy ET/lxml, substring-XML, regex raw-string, quét field, cô lập từng bước, test khả năng thật).
4. **Chạy đủ chuỗi** theo mục 3–4 bên dưới; có **bằng chứng** (render/ảnh/log) trước khi báo xong.
5. **Nhớ & đồng bộ:** quy tắc bền vững ghi vào `AGENTS.md`; sửa skill xong chạy `tools/sync-skills.ps1`.

---

## 3. Chuỗi điều phối theo tình huống

### A. Báo cáo / Đồ án / Luận văn (chuỗi đầy đủ)
```text
grill-me (hỏi thông tin: loại bìa, đề tài, GVHD, SV, lớp, MSSV, mục tiêu số trang)
 → research-report/research (thu thập & xác minh nguồn, nếu cần)
 → diagram-orchestrator → plantuml-diagrams/tldraw-diagrams/simplified-diagrams (TRẮNG-ĐEN)
 → diagram-auditor (GATE: phải PASS trước khi chèn)
 → make_cover.py (bìa 2 định dạng) + edit_docx.py (format, TOC, số trang, caption SEQ/REF)
 → human-report-writing + caption-wording (văn phong tự nhiên, nghiêm túc, không jargon thừa; **có lượt đọc lại bản thảo**)
 → render_docx.py (PDF→PNG) → soi từng trang (Visual QA)
```
Chỉ `docx-report` mà bỏ các khâu còn lại ⇒ **đọc là thấy thiếu**.

### B. Slide
```text
pptx-deck/ppt-master (chủ) → diagram-orchestrator (sơ đồ) → theme-factory (màu/font) → anti-slop (bố cục) → render QA
```

### C. Sơ đồ
```text
diagram-orchestrator (chọn công cụ theo ngữ nghĩa) → <tool> → diagram-auditor (gate) → chèn vào docx/pptx
```

### D. Nghiên cứu / Tài liệu dự án / PDF / Excel → theo bảng mục 1.

---

## 4. Quy tắc "các skill tôn trọng nhau" (không mâu thuẫn)

1. **Thứ bậc thẩm quyền:** `AGENTS.md` (Nguyên tắc bất biến) **>** skill chủ **>** skill phụ. Xung đột → theo cấp cao hơn.
2. **Không tự chế khi skill có sẵn công cụ:** dùng `edit_docx.py`, `make_cover.py`, `replace_docx_images.py`,
   `convert_doc.py`, `revisions.py`, `render_docx.py` — **không** viết script thay thế (TOC/caption phải là
   **field OOXML**, ảnh thay bằng **binary swap**, số trang bằng `pgNumType`…).
3. **Quy ước chung bắt buộc (đã cố định trong các skill):**
   - Báo cáo học thuật → sơ đồ **TRẮNG-ĐEN** (zero-color). Branded/marketing mới được dùng màu.
   - **Không nhúng `title` trong ảnh** — tiêu đề để ở caption (`Hình X.Y: ...`).
   - Ảnh chụp = UI thật (`screenshots/`); sơ đồ = file có mã nguồn (`diagrams/`).
   - Văn xuôi: **không** em dash, **không** in đậm thân bài, **không** highlight, không bullet tràn lan.
4. **Khi hai skill chạm nhau:** xác định *skill chủ* cho artifact, coi các skill khác là *phụ*; nhường
   quyền cho skill chủ trong phạm vi của nó (VD: `docx-report` quyết định caption/TOC; `plantuml-diagrams`
   quyết định cú pháp `.puml`).
5. **Bàn giao có cổng (gate):** `diagram-auditor` là cổng cho mọi sơ đồ; `render_docx.py` + soi ảnh là cổng
   cho mọi file Word. Không qua cổng = **chưa xong**.

---

## 5. Chống lỗi phổ biến (Anti-patterns)

- ❌ Chỉ gọi `docx-report` cho cả đồ án (bỏ sơ đồ, văn phong, nghiên cứu, bìa).
- ❌ Viết số caption / mục lục bằng **tay** thay vì field (`SEQ`/`TOC`).
- ❌ Tự blob-swap ảnh thay vì `replace_docx_images.py`; tự sinh lại file thay vì `safe-docx-modifier`.
- ❌ Bỏ qua `diagram-auditor` rồi chèn sơ đồ lỗi vào báo cáo.
- ❌ Dùng **màu** cho sơ đồ đồ án học thuật; nhúng `title` trong ảnh.
- ❌ Sửa `.claude/skills/` mà quên `tools/sync-skills.ps1`.
- ❌ Nạp skill nhưng **bỏ bước render / kiểm ảnh** mà skill yêu cầu.

---

## 6. Definition of Done (khi dùng bộ skill)

```text
[ ] Đã nạp ĐÚNG các skill liên quan (không chỉ docx-report).
[ ] Làm ĐỦ chuỗi theo mục 3 (cho tình huống đang làm).
[ ] Sơ đồ qua diagram-auditor; file Word qua render + soi ảnh.
[ ] Tuân quy ước chung (trắng-đen học thuật, không title trong ảnh, không em dash/bold thân bài).
[ ] Có BẰNG CHỨNG (render/ảnh/log); không vi phạm "Nguyên tắc bất biến" trong AGENTS.md.
[ ] Đã sync .agents/skills nếu có sửa skill.
```
