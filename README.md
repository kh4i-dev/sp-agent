# sp-agent

Bộ **agent skills** cho công việc học tập/đồ án: viết tài liệu Word, làm slide PowerPoint,
vẽ sơ đồ (Mermaid/PlantUML), nghiên cứu có dẫn nguồn, xử lý PDF và Excel.

Mục tiêu: bạn bảo agent "viết báo cáo", "làm slide", "vẽ use case", "nghiên cứu chủ đề X" —
agent tự nhận diện và nạp đúng skill để làm đúng chuẩn.

## Cấu trúc

```text
sp-agent/
├── AGENTS.md                 # master routing: agent đọc cái này trước
├── CLAUDE.md                 # trỏ về AGENTS.md
├── README.md                 # file này
├── .claude/skills/           # NGUỒN CHÍNH — sửa ở đây
│   ├── docx-report/          #   SKILL.md + reference/ + scripts/
│   ├── human-report-writing/ #   văn phong tự nhiên như người
│   ├── pptx-deck/
│   ├── ppt-master/           #   Chuyển tài liệu/ảnh thành slide native, beautify, animation, narration
│   ├── plantuml-diagrams/    #   UML, Use Case, Sequence, ERD chuẩn 100% ISO Trắng-Đen
│   ├── use-case-layout/      #   Use Case gọn-đẹp-dễ nhìn, cấm đường nối vòng xa
│   ├── tldraw-diagrams/      #   Sơ đồ thẩm mỹ cao, đường cong mượt, xuất SVG/PNG 2x, tldr
│   ├── research-report/
│   ├── pdf-toolkit/
│   └── xlsx-sheet/
├── .agents/skills/           # BẢN MIRROR (đừng sửa tay)
├── reference/                # Tài liệu tham khảo & guide ppt-master
└── tools/
    ├── sync-skills.ps1       # .claude/skills -> .agents/skills
    ├── check-tools.ps1       # kiểm tra toolchain đã cài
    └── verify-skills.ps1     # kiểm tra frontmatter SKILL.md
```

## Skill có gì

| Skill | Việc |
|---|---|
| `docx-report` | Word/báo cáo/đồ án: heading, bảng, hình, caption, TOC, render QA |
| `human-report-writing` | Biên tập văn phong báo cáo cho tự nhiên, bỏ dấu hiệu văn AI |
| `pptx-deck` | Slide thuyết trình cơ bản: template, chart native, render QA |
| `ppt-master` | Đỉnh cao AI Slide: Biến PDF/Doc/MD thành slide native, tái tạo slide từ ảnh, làm đẹp deck, hiệu ứng & âm thanh |
| `plantuml-diagrams` | Use Case, Class, Activity, Sequence, State, ERD chuẩn 100% UML Trắng-Đen |
| `use-case-layout` | Use Case UML bố cục lane gọn-đẹp-dễ nhìn, đường nối ngắn trực tiếp, **không vẽ vòng xa** |
| `simplified-diagrams` | Sơ đồ tinh gọn / Khái niệm (5-8 thực thể cốt lõi) bảo vệ đồ án, vẽ tay tự nhiên + Kịch bản phát biểu |
| `tldraw-diagrams` | Sơ đồ kiến trúc, flowchart thẩm mỹ cao, đường cong mềm mại (bezier arc), xuất SVG/PNG 2x |
| `research-report` | Deep research, xác minh trích dẫn, chống bịa nguồn |
| `pdf-toolkit` | Đọc/trích/tạo/OCR/ghép PDF |
| `xlsx-sheet` | Excel: công thức, recalc, biểu đồ |

## Cài đặt

```powershell
# Python packages
pip install python-docx python-pptx openpyxl xlsxwriter pandas pymupdf pdfplumber pypdf reportlab

# LibreOffice — bắt buộc cho render QA (Word/Slide) và recalc Excel
winget install TheDocumentFoundation.LibreOffice

# pandoc (tùy chọn)
winget install JohnMacFarlane.Pandoc
```

Mermaid không cần cài: dùng `npx -p @mermaid-js/mermaid-cli mmdc ...`.

Kiểm tra môi trường:

```powershell
powershell -File tools/check-tools.ps1
```

## Cách dùng

Đặt project này cạnh (hoặc trong) workspace bạn đang làm, rồi chỉ cần ra lệnh tự nhiên:

- "Viết chương 3 báo cáo PTTKHT, có ERD và bảng use case, render kiểm tra giúp tôi."
- "Làm 12 slide bảo vệ đồ án từ báo cáo này, tông màu xanh navy."
- "Vẽ sơ đồ tuần tự cho luồng đăng nhập và chèn vào tài liệu."
- "Nghiên cứu so sánh PostgreSQL vs MongoDB cho đồ án, có dẫn nguồn."

## Đồng bộ skill

Sửa skill trong `.claude/skills/`, sau đó:

```powershell
powershell -File tools/sync-skills.ps1
```

## Thêm skill mới

Xem mục "Thêm skill mới" trong `AGENTS.md`. Nhớ: `name` trong frontmatter phải trùng tên thư mục.
