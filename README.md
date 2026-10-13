# sp-agent

Bộ **agent skills** cho học tập/đồ án: viết tài liệu Word, làm slide PowerPoint, vẽ sơ đồ,
nghiên cứu có dẫn nguồn, xử lý PDF/Excel, viết tài liệu dự án.

Mục tiêu: bạn ra lệnh tự nhiên ("viết báo cáo", "làm slide", "vẽ use case", "nghiên cứu X") —
agent **tự nhận diện và nạp đúng skill** để làm đúng chuẩn. Hiện có **32 skill**.

## Cách agent nạp skill (quan trọng)

`AGENTS.md` là file agent đọc trước (được tự nạp mỗi phiên). Giao thức đầy đủ nằm ở
mục **"Giao thức nạp skill (BẮT BUỘC)"** trong `AGENTS.md`. Tóm tắt:

1. Khám phá cây skill (`.claude/skills/*/SKILL.md`).
2. Chọn skill theo bảng **Routing** trong `AGENTS.md`.
3. Nạp bằng công cụ `skill` (hoặc đọc thẳng `SKILL.md`).
4. Đọc trọn `SKILL.md` → mở tiếp `reference/` → `scripts/` khi cần.
5. Quy tắc bền vững phải ghi vào `AGENTS.md`/`CLAUDE.md` (file tự nạp mỗi phiên).

**Bẫy:** `name` frontmatter phải **trùng tên thư mục**; sửa `.claude/skills/` xong phải chạy
`tools/sync-skills.ps1`; đừng bỏ qua bước render/QA mà skill yêu cầu.

## Cấu trúc

```text
sp-agent/
├── AGENTS.md                 # master routing + giao thức nạp skill (agent đọc trước)
├── CLAUDE.md                 # trỏ về AGENTS.md
├── README.md                 # file này
├── .gitignore                # bỏ vendor/ + __pycache__/
├── .claude/skills/           # NGUỒN CHÍNH — sửa ở đây (32 skill)
├── .agents/skills/           # BẢN MIRROR (đừng sửa tay)
├── vendor/                   # repo tham khảo (KHÔNG auto-load, KHÔNG commit)
├── reference/                # tài liệu tham khảo & guide ppt-master
└── tools/
    ├── sync-skills.ps1       # .claude/skills -> .agents/skills
    ├── check-tools.ps1       # kiểm tra toolchain đã cài
    └── verify-skills.ps1     # kiểm tra frontmatter SKILL.md
```

## Skill index (32)

### Tài liệu Word / báo cáo

| Skill | Việc |
|---|---|
| `docx-report` | Word/báo cáo/đồ án: heading (khóa đầu trang), bảng, hình, caption (+SEQ/REF tự đánh số), TOC, số trang La Mã/Ả Rập, **sinh bìa 2 định dạng (Đồ án/BTL)**, render QA |
| `safe-docx-modifier` | Sửa Word đã hoàn thiện **không sinh lại**: thay ảnh in-place, sửa text bảo toàn Runs |
| `docx` | Tạo/đọc/sửa `.docx` chuyên sâu OOXML (TOC, tracked changes, comment) |
| `human-report-writing` | Biên tập văn phong tự nhiên, bỏ dấu hiệu văn AI |

### Slide / thuyết trình

| Skill | Việc |
|---|---|
| `pptx-deck` | Slide thuyết trình: template, chart native, render QA |
| `ppt-master` | PDF/Doc/MD → slide native, tái tạo slide từ ảnh, beautify, animation/narration |
| `pptx` | Tạo/đọc/sửa `.pptx/.potx` (layout, speaker notes) |

### Sơ đồ

| Skill | Việc |
|---|---|
| `diagram-orchestrator` | Điều phối chọn công cụ vẽ theo ngữ nghĩa (Intelligent Problem-Solving Protocol) |
| `plantuml-diagrams` | UML/ERD/Sequence/Activity/Class/Use Case chuẩn 100%, Trắng-Đen |
| `use-case-layout` | Use Case UML bố cục lane gọn-đẹp, **cấm vòng xa** |
| `simplified-diagrams` | Sơ đồ tinh gọn/khái niệm (5-8 thực thể) cho bảo vệ đồ án |
| `tldraw-diagrams` | Sơ đồ kiến trúc/flowchart thẩm mỹ cao, đường cong mềm |
| `diagram-auditor` | Audit chất lượng sơ đồ (chống False-PASS, méo/đè nhãn) |
| `diagram-design` | Đa dạng sơ đồ (gantt, sankey, ERD, UML…) xuất HTML/SVG/PNG |

### Nghiên cứu

| Skill | Việc |
|---|---|
| `research-report` | Deep research, xác minh trích dẫn, chống bịa nguồn |
| `research` | Nghiên cứu chủ đề, gom nguồn, lưu báo cáo Markdown |
| `research-artifacts` | Chuẩn hóa research thành bundle OKF có truy vết |

### PDF / Excel

| Skill | Việc |
|---|---|
| `pdf-toolkit` / `pdf` | Đọc/trích/tạo/OCR/ghép/điền form PDF |
| `xlsx-sheet` / `xlsx` | Excel: công thức, recalc, biểu đồ |

### Tài liệu dự án / ADR / tri thức

| Skill | Việc |
|---|---|
| `doc-architect` | Lập/audit tài liệu dự án (README, AGENTS.md, docs/) |
| `living-docs` | ADR/MADR, PRD, sơ đồ kiến trúc Mermaid sống |
| `okf-knowledge-format` | Đóng gói tri thức theo OKF bundle |
| `documentation` / `documentation-and-adrs` / `doc-coauthoring` / `writing-guidelines` | API docs, ADR, đồng soạn, soát văn phong |

### Thiết kế / thẩm mỹ / kỷ luật

| Skill | Việc |
|---|---|
| `anti-slop` | Chống "AI slop" cho UI/bố cục |
| `theme-factory` | Áp theme màu/font cho artifact |
| `data-visualization` | Biểu đồ matplotlib/seaborn/plotly chất lượng công bố |
| `engineering-discipline` | Kỷ luật kỹ thuật: verify trước khi báo xong, an toàn migration… |

## docx-report — điểm mạnh

- Chuẩn hóa học thuật: lề 3.5cm, Justify, giãn dòng; **Heading Times New Roman + Heading 1 khóa đầu trang**.
- Bảng nền trắng, header đậm căn trái; caption tự chuyển về đúng vị trí.
- **Caption tự đánh số (SEQ) + cross-reference (REF)** theo chương.
- **Số trang theo phần**: bìa (không số) | front-matter (i, ii) | thân bài (1, 2, 3).
- **Sinh bìa 2 định dạng** `--kind doan|btl`: Bìa, Bìa lót, Nhiệm vụ, Phiếu thông qua, Phiếu ghi điểm, Lời cam đoan, Danh mục từ viết tắt — viền chừa gáy + logo TNUT. **Không hardcode tên → bắt buộc hỏi người dùng.**
- Công cụ kèm: `convert_doc.py` (`.doc`→`.docx`), `revisions.py` (tracked changes an toàn), `render_docx.py` (PDF/PNG + tự cập nhật field).
- Reference: `rules.md`, `cover-formats.md`, `report-scope.md` (chống báo cáo mỏng), `caption-wording.md` (mềm hóa ngôn từ).

## Cài đặt

```powershell
# Python packages
pip install python-docx python-pptx openpyxl xlsxwriter pandas pymupdf pdfplumber pypdf reportlab

# LibreOffice — bắt buộc cho render QA (Word/Slide) và recalc Excel
winget install TheDocumentFoundation.LibreOffice

# pandoc (tùy chọn)
winget install JohnMacFarlane.Pandoc
```

Kiểm tra môi trường:

```powershell
powershell -File tools/check-tools.ps1
```

## Cách dùng

Đặt project này cạnh (hoặc trong) workspace bạn đang làm, rồi ra lệnh tự nhiên:

- "Viết đồ án PTTKHT quản lý bán hàng, có bìa và mục lục, render kiểm tra giúp tôi."
- "Làm 12 slide bảo vệ đồ án từ báo cáo này, tông màu xanh navy."
- "Vẽ sơ đồ tuần tự cho luồng đăng nhập và chèn vào tài liệu."
- "Nghiên cứu so sánh PostgreSQL vs MongoDB cho đồ án, có dẫn nguồn."

## Đồng bộ skill & thêm skill mới

Sửa skill trong `.claude/skills/`, sau đó:

```powershell
powershell -File tools/sync-skills.ps1
```

Thêm skill mới: xem mục "Thêm skill mới" trong `AGENTS.md`. Nhớ: `name` trong frontmatter
phải trùng tên thư mục (kebab-case) và `description` phải chứa từ khóa kích hoạt.
