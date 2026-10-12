---
name: diagram-orchestrator
description: Điều phối thông minh toàn bộ hệ thống sơ đồ kỹ thuật cho báo cáo Word (docx-report), slide (pptx-deck), đồ án tốt nghiệp và tài liệu kiến trúc. Tự động phân tích ngữ nghĩa và nguồn dữ liệu để chọn chính xác công cụ tối ưu cho từng sơ đồ riêng biệt (PlantUML cho UML/ERD chuẩn mực; Graphviz DOT cho cấu trúc cây Prefix Trie, BK-Tree, đồ thị thuật toán; tldraw/draw.io cho kiến trúc tổng thể trực quan tự do); áp dụng chuẩn thẩm mỹ Academic Monochrome (Trắng - Đen học thuật 300 DPI, không title nhúng trong ảnh) và bắt buộc đi qua cổng kiểm định diagram-auditor trước khi xuất bản. Dùng khi cần vẽ sơ đồ, chọn công cụ vẽ sơ đồ, diagram orchestrator, sơ đồ cây, trie, bk-tree, kiến trúc hệ thống, phối hợp sơ đồ.
---

# Diagram Orchestrator Skill — Điều Phối Sơ Đồ Thông Minh & Thích Ứng

Mục tiêu: Đóng vai trò **nhạc trưởng điều phối (Orchestrator)** cho toàn bộ quy trình vẽ sơ đồ kỹ thuật. Skill phân tích ngữ nghĩa, cấu trúc dữ liệu, và yêu cầu trình bày để **tự chọn công cụ phù hợp nhất cho từng sơ đồ riêng biệt**, không mặc định dùng PlantUML cho mọi trường hợp, không tạo renderer mới khi repo đã có sẵn, và bắt buộc kiểm định chất lượng trước khi bàn giao.

---

## 1. NGUYÊN TẮC CỐT LÕI (CORE PRINCIPLES)

1. **Semantic-First (Ngữ nghĩa quyết định công cụ):** Mỗi dạng sơ đồ có một công cụ tối ưu tự nhiên. Sơ đồ UML thuộc về PlantUML; Cấu trúc cây/thuật toán thuộc về Graphviz; Kiến trúc tổng quan tự do thuộc về tldraw/draw.io.
2. **Reuse Verified Toolchain (Tái sử dụng công cụ đã kiểm chứng):** Tận dụng tối đa các skill và script đã được cài đặt và kiểm định trong repo (`plantuml-diagrams`, `simplified-diagrams`, `tldraw-diagrams`, `diagram-auditor`).
3. **Academic Monochrome by Default (Mặc định Trắng - Đen học thuật):** Nền trắng `#FFFFFF`, nét đen `#000000`, 300 DPI, độ tương phản cao, tối ưu cho in ấn A4 và nộp luận văn. Chỉ dùng màu có chủ đích khi người dùng yêu cầu rõ ràng.
4. **Zero-Title in Canvas:** Tiêu đề sơ đồ luôn nằm ở Caption tài liệu (*Hình X.Y: ...*), tuyệt đối không nhúng cứng từ khóa `title` vào ảnh làm lặp chữ và mất diện tích.
5. **Auditor Gate Mandatory (Bắt buộc kiểm định):** 100% sơ đồ xuất bản phải đi qua `diagram-auditor` để đảm bảo không đè chữ, không cắt nét, không banner cảnh báo ngầm, đủ cả SVG vector và PNG raster.
6. **Zero Code Dumps in Output (Cấm xả mã nguồn ra chat):** Khi hoàn thành vẽ và audit sơ đồ, phản hồi bàn giao **CHỈ chứa ảnh trực quan** (`![Hình X.Y](path)`), dòng tiêu đề `Hình X.Y: ...`, và tóm tắt audit. Mã nguồn (`.puml`, `.dot`) đã lưu an toàn trên đĩa; tuyệt đối KHÔNG in toàn bộ code block ra khung chat làm rối mắt người dùng.

---

## 2. BẢNG ĐỊNH TUYẾN CÔNG CỤ (ROUTING MATRIX)

| Loại sơ đồ cần vẽ | Công cụ chỉ định | Định dạng nguồn | Renderer trong repo | Tiêu chuẩn chất lượng |
|---|---|---|---|---|
| **Use Case, Activity, Sequence, Class, State, Component** | **PlantUML** | `.puml` | `plantuml-diagrams/scripts/render-puml.mjs` | Chuẩn ISO/UML 2.x, `roundCorner 0/4`, `nodesep 70`, `ranksep 70`, `linetype ortho`. |
| **ERD (Thực thể - Quan hệ cơ sở dữ liệu)** | **PlantUML** | `.puml` | `plantuml-diagrams/scripts/render-puml.mjs` | Crow's foot notation, cấm viết nhãn chữ trên dây nối, cấm quan hệ 2 chiều trùng lặp. |
| **Sơ đồ tinh gọn / Bảo vệ đồ án (5-8 thực thể)** | **PlantUML** | `.puml` | `simplified-diagrams/` | Bố cục 3 cột (Identity -> Core -> Payment), kèm kịch bản phát biểu 60s. |
| **Cây tiền tố (Prefix Trie), Cây tìm kiếm từ khóa** | **Graphviz (DOT)** | `.dot` | `diagram-orchestrator/scripts/render-graphviz.mjs` | `rankdir=TB`, node hình tròn/elip, ký tự phân cấp rõ ràng, đánh dấu node kết thúc từ. |
| **Cây BK-Tree (Fuzzy Matching / Levenshtein)** | **Graphviz (DOT)** | `.dot` | `diagram-orchestrator/scripts/render-graphviz.mjs` | Cạnh có nhãn khoảng cách Levenshtein chính xác (`d=1`, `d=2`), tính nhất quán thuật toán 100%. |
| **Abstract Syntax Tree (AST), Đồ thị thuật toán** | **Graphviz (DOT)** | `.dot` | `diagram-orchestrator/scripts/render-graphviz.mjs` | Phân cấp nút-cạnh tự nhiên, trọng số cạnh rõ ràng. |
| **Kiến trúc tổng thể hệ thống (High-Level Architecture)** | **tldraw** / draw.io | `.tldr` / `.json` | `tldraw-diagrams/scripts/render.mjs` | Phân vùng trực quan (Client, Gateway, Service, Database), bo góc mềm mại, icon hạ tầng. |
| **Sơ đồ triển khai hạ tầng nhiều vùng (Cloud/Edge)** | **tldraw** hoặc **PlantUML** | `.tldr` hoặc `.puml` | Linh hoạt theo ngữ cảnh | Dùng PlantUML nếu báo cáo chuẩn UML node/artifact; dùng tldraw nếu cần bố cục tự do trực quan. |

---

## 3. QUY TẮC RA QUYẾT ĐỊNH (DECISION HIERARCHY)

Khi nhận yêu cầu vẽ sơ đồ, áp dụng 5 bước lọc tuần tự:

1. **Ưu tiên 1 — Đúng ngữ nghĩa & nguồn dữ liệu:**
   - Dữ liệu là cấu trúc nút-cạnh thuật toán (Trie, BK-Tree, Graph, AST)? -> **Bắt buộc dùng Graphviz DOT**.
   - Dữ liệu là quy trình nghiệp vụ, ca sử dụng, quan hệ đối tượng UML, bảng DB? -> **Dùng PlantUML**.
   - Dữ liệu là bức tranh kiến trúc tổng thể cần bố trí tự do theo vùng? -> **Dùng tldraw / draw.io**.
2. **Ưu tiên 2 — Công cụ có sẵn và đã xác minh:**
   - Sử dụng các pipeline render nội bộ đã kiểm chứng: `render-puml.mjs`, `render-graphviz.mjs`, `render.mjs`.
3. **Ưu tiên 3 — Khả năng bảo trì & chỉnh sửa:**
   - File nguồn (`.puml`, `.dot`, `.tldr`) phải được lưu trữ song song với ảnh xuất để người dùng có thể mở ra tinh chỉnh.
4. **Ưu tiên 4 — Bố cục & Khả năng đọc:**
   - Không nhồi nhét quá nhiều thông tin vào một hình. Nếu sơ đồ quá lớn (như Sequence toàn hệ thống), phân rã thành 4-5 sơ đồ use case trọng điểm theo hướng dẫn của `simplified-diagrams`.
5. **Ưu tiên 5 — Thẩm mỹ & Phong cách học thuật:**
   - Luôn tuân thủ Academic Monochrome: không màu mè lòe loẹt, đường nét vuông vức, khoảng cách thoáng đãng.

---

## 4. QUY CHUẨN THỊ GIÁC: ACADEMIC MONOCHROME

Mọi sơ đồ (dù sinh bằng PlantUML, Graphviz hay tldraw) đều phải tuân thủ bảng phong cách học thuật:

```text
Nền (Background):        Trắng tinh khiết (#FFFFFF)
Đường viền & Nét vẽ:     Đen thuần (#000000), độ dày 1px - 1.5px
Chữ (Typography):        Font Segoe UI, Arial, sans-serif (giữ dấu tiếng Việt 100%)
Kích thước chữ:          Tiêu đề nhóm/khối 12-13pt, nội dung 10-11pt, nhãn cạnh 9-10pt
Bóng đổ (Shadow):        BANNED (Tắt hoàn toàn)
Hiệu ứng 3D/Gradient:    BANNED (Không sử dụng)
Tiêu đề nhúng (title):   BANNED (Không đặt dòng 'title ...' trong canvas)
Độ phân giải xuất:       Vector SVG + Raster PNG 300 DPI
```

*Lưu ý:* Chỉ chuyển sang bảng màu **Academic Navy** (nền trắng, viền xanh Navy `#1E3A8A`, điểm nhấn nhẹ `#2563EB`) khi người dùng yêu cầu rõ ràng cho mục đích trình chiếu slide hoặc bản PDF số.

---

## 5. QUY TRÌNH KIỂM ĐỊNH 9 BƯỚC BẮT BUỘC (9-STEP QUALITY PIPELINE)

Mọi sơ đồ do `diagram-orchestrator` xuất ra phải hoàn tất đủ 9 bước kiểm định:

```text
[1. Phân tích ngữ nghĩa & Chọn công cụ]
                  │
[2. Đối chiếu nguồn dữ liệu thật (schema/code/thuật toán)]
                  │
[3. Viết mã nguồn (.puml / .dot / .json)]
                  │
[4. Render song song SVG và PNG 300 DPI]
                  │
[5. Xác minh file tồn tại & dung lượng > 500 bytes]
                  │
[6. Chạy diagram-auditor kiểm tra tự động]
                  │
[7. Visual Inspection: Soi tọa độ cắt nét, đè chữ, dấu tiếng Việt]
                  │
[8. Đối chiếu tính chính xác dữ liệu (Levenshtein, PK/FK, Lifelines)]
                  │
[9. KẾT LUẬN: Đạt 100% PASS mới bàn giao hoặc chèn DOCX]
```

---

## 6. LỆNH THỰC THI (TOOLCHAIN EXECUTION)

### 6.1. Render PlantUML (.puml)
```bash
node .claude/skills/plantuml-diagrams/scripts/render-puml.mjs --in <path/to/diagram.puml>
```

### 6.2. Render Graphviz DOT (.dot)
```bash
node .claude/skills/diagram-orchestrator/scripts/render-graphviz.mjs --in <path/to/diagram.dot>
```

### 6.3. Render tldraw (.json -> .tldr, .svg, .png)
```bash
node .claude/skills/tldraw-diagrams/scripts/render.mjs --in <path/to/diagram.json> --png --scale 2
```

### 6.4. Audit kiểm định chất lượng (Bắt buộc)
```bash
node .claude/skills/diagram-auditor/scripts/audit-diagrams.mjs <duong-dan-thu-muc-export>
```

---

## 7. QUY CHUẨN CHÈN VÀO DOCX (WORD INTEGRATION)

Khi nhiệm vụ yêu cầu chèn sơ đồ vào file Word báo cáo:
1. **Khóa tỷ lệ & Canh giữa:** Chiều rộng chuẩn từ 5.8 đến 6.2 inches (vừa khít khổ trang A4 lề 2cm).
2. **Caption chuẩn học thuật:** Đặt ngay dưới ảnh, định dạng in nghiêng, cỡ chữ 10.5pt: `*Hình X.Y: Tên sơ đồ*`.
3. **Chống rớt trang:** Thiết lập `paragraph.paragraph_format.keep_with_next = True` trên ảnh để caption luôn đi liền với hình.
4. **Render QA:** Chuyển đổi DOCX sang PDF/ảnh trang bằng LibreOffice để soi lại trực quan bố cục thực tế.

---

## 8. QUY CHUẨN BÀN GIAO TRỰC QUAN SẠCH (CLEAN VISUAL PRESENTATION)

Khi báo cáo hoàn thành hoặc audit sơ đồ cho người dùng, Agent **TUYỆT ĐỐI KHÔNG** in code block `.puml`, `.dot`, hay `.json` ra khung chat làm rối mắt. Báo cáo bàn giao chuẩn mực bắt buộc gồm:

1. **Ảnh sơ đồ trực quan (Rendered Preview):** `![Hình X.Y: Tên sơ đồ](path/to/diagram.png)`
2. **Tiêu đề hình chuẩn mực:** `*Hình X.Y: Tên sơ đồ*`
3. **Tóm tắt kiểm định `diagram-auditor`:** Trạng thái `[PASS]` 100% (không đè nhãn, không cắt nét, đủ SVG + PNG 300 DPI).
4. **Đường dẫn tệp nguồn:** Link markdown tới file trên đĩa `[ten_so_do.puml](file:///path/to/ten_so_do.puml)`.

