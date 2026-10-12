---
name: diagram-orchestrator
description: Điều phối thông minh toàn bộ hệ thống sơ đồ kỹ thuật cho báo cáo Word (docx-report), slide (pptx-deck), đồ án tốt nghiệp và tài liệu kiến trúc. Tự động phân tích ngữ nghĩa và nguồn dữ liệu để chọn chính xác công cụ tối ưu cho từng sơ đồ riêng biệt (PlantUML cho UML/ERD chuẩn mực; Graphviz DOT cho cấu trúc cây Prefix Trie, BK-Tree, đồ thị thuật toán; tldraw/draw.io cho kiến trúc tổng thể trực quan tự do); áp dụng chuẩn thẩm mỹ Academic Monochrome (Trắng - Đen học thuật 300 DPI, không title nhúng trong ảnh) và bắt buộc đi qua cổng kiểm định diagram-auditor trước khi xuất bản. Dùng khi cần vẽ sơ đồ, chọn công cụ vẽ sơ đồ, diagram orchestrator, sơ đồ cây, trie, bk-tree, kiến trúc hệ thống, phối hợp sơ đồ.
---

# Diagram Orchestrator Skill — Điều Phối Sơ Đồ Kỹ Thuật Thích Ứng

Mục tiêu: Đóng vai trò **nhạc trưởng điều phối (Orchestrator)** cho toàn bộ quy trình vẽ sơ đồ kỹ thuật. Skill phân tích ngữ nghĩa, cấu trúc dữ liệu, và yêu cầu trình bày để **tự chọn công cụ phù hợp nhất cho từng sơ đồ riêng biệt**, không mặc định dùng PlantUML cho mọi trường hợp, không tạo renderer mới khi repo đã có sẵn, và kiểm định chất lượng nghiêm ngặt trước khi bàn giao.

Sơ đồ đẹp không cứu được mô hình sai; sơ đồ đúng nhưng khó đọc cũng chưa hoàn thành nhiệm vụ. Phải kiểm tra cả ba: **đúng nội dung, đúng cách biểu diễn và đúng chất lượng hình ảnh**.

---

## 1. BẢY NGUYÊN TẮC XƯƠNG MÁU (CORE BATTLE-TESTED PRINCIPLES)

1. **Tìm nguồn sự thật trước khi vẽ:** Use Case dựa trên yêu cầu nghiệp vụ; ERD dựa trên schema/migration thật; Sequence dựa trên luồng xử lý mã nguồn; Class Diagram dựa trên class/interface thật. Tuyệt đối không tự bịa thêm `AdminService`, bảng `Logs`, lớp `Repository` hay Actor mới chỉ vì chúng hay gặp ở dự án khác.
2. **Một sơ đồ chỉ trả lời một câu hỏi chính:** Use Case trả lời ai dùng hệ thống để đạt mục tiêu gì; ERD trả lời dữ liệu lưu trữ thế nào; Sequence trả lời thành phần tương tác theo trình tự nào. Không nhét chung bảng dữ liệu, hàm xử lý, luồng nghiệp vụ và cấu trúc RAM vào cùng một hình.
3. **Không đánh đồng mọi loại quan hệ:** Quan hệ UML không mặc nhiên là Foreign Key trong CSDL; Lời gọi hàm trong Sequence không phải quan hệ kế thừa; Đường nối trong flowchart không phải lúc nào cũng là luồng dữ liệu. Ký hiệu phải mang đúng ngữ nghĩa của loại sơ đồ đó.
4. **Phân biệt mô hình thiết kế với hiện trạng triển khai:** Nếu thiết kế trước khi code, gọi là mô hình thiết kế đề xuất. Nếu mô tả hệ thống đang chạy, phải đối chiếu 100% với mã nguồn hiện hành.
5. **Không ép mọi sơ đồ vừa một trang bằng cách thu nhỏ chữ:** Nếu sơ đồ quá rộng hoặc nhiều chi tiết, phân rã thành sơ đồ tổng quan và các sơ đồ chi tiết. Kích thước chữ phải đọc rõ ở kích thước in thực tế trên trang A4.
6. **Mỗi sơ đồ phải có tệp nguồn để sửa lại:** Giữ nguyên `.puml`, `.dot` hoặc `.tldr`. PNG và SVG chỉ là đầu ra. Khi nghiệp vụ đổi, sửa từ file nguồn, render lại và kiểm tra.
7. **Không tuyên bố PASS chỉ vì công cụ render thành công:** Compiler xuất được ảnh không có nghĩa nội dung đúng. Bắt buộc có hai lượt đánh giá độc lập: một lượt kiểm tra ngữ nghĩa/tính nhất quán; một lượt kiểm tra hình ảnh, đường nối và bố cục.

---

## 2. BẢNG ĐỊNH TUYẾN: LOẠI SƠ ĐỒ NÀO CHO CÂU HỎI NÀO?

| Khi cần trả lời câu hỏi... | Loại sơ đồ | Công cụ tối ưu | Định dạng & Renderer |
|---|---|---|---|
| Ai sử dụng hệ thống, muốn đạt mục tiêu nghiệp vụ gì? | **Use Case** | **PlantUML** | `.puml` → `render-puml.mjs` |
| Quy trình xử lý nghiệp vụ đi qua những bước và điều kiện nào? | **Activity** | **PlantUML** | `.puml` → `render-puml.mjs` |
| Những đối tượng/lớp nào tồn tại, trách nhiệm và quan hệ ra sao? | **Class** | **PlantUML** | `.puml` → `render-puml.mjs` |
| Dữ liệu lưu trữ thế nào, khóa chính/ngoại và quan hệ ra sao? | **ERD** | **PlantUML** | `.puml` → `render-puml.mjs` |
| Thành phần nào gửi thông điệp cho thành phần nào, theo thứ tự gì? | **Sequence** | **PlantUML** | `.puml` → `render-puml.mjs` |
| Một đối tượng trải qua những trạng thái nào trong vòng đời? | **State Machine**| **PlantUML** | `.puml` → `render-puml.mjs` |
| Hệ thống gồm những khối phần mềm lớn nào và phụ thuộc nhau ra sao? | **Component** | **PlantUML / tldraw** | `.puml` hoặc `.tldr` |
| Phần mềm chạy ở máy/môi trường nào, kết nối mạng ra sao? | **Deployment**| **PlantUML / tldraw** | `.puml` hoặc `.tldr` |
| Cấu trúc cây tiền tố Prefix Trie, BK-Tree, đồ thị thuật toán? | **Data Structure**| **Graphviz (DOT)** | `.dot` → `render-graphviz.mjs` |
| Kiến trúc tổng quan cần bố trí tự do, bo góc mềm mại, theo vùng? | **High-Level Arch**| **tldraw / draw.io** | `.tldr` → `render.mjs` |
| Luồng dữ liệu đi giữa tiến trình, kho dữ liệu và thực thể ngoài? | **DFD** | **draw.io / tldraw** | `.tldr` / vector |

### Bẫy kinh điển: Class Diagram không thay thế ERD & Cấu trúc RAM

| Tiêu chí | Class Diagram (Thiết kế lớp) | ERD (Cơ sở dữ liệu) | Cấu trúc dữ liệu RAM (Trie/Tree) |
|---|---|---|---|
| **Trọng tâm** | Cấu trúc đối tượng OOP | Mô hình dữ liệu lưu trữ bền vững | Tổ chức bộ nhớ tạm thuật toán |
| **Thể hiện** | Field, method, kế thừa, visibility | Bảng, cột, PK, FK, quan hệ 1-N, N-N | Nút, cạnh, ký tự, khoảng cách |
| **Phương thức** | Có (`login()`, `search()`) | **CẤM** đưa phương thức vào ERD | Không áp dụng |
| **Công cụ** | PlantUML | PlantUML Crow's foot | **Bắt buộc dùng Graphviz DOT** |

---

## 3. UNIVERSAL DIAGRAM ENGINEERING RULES

### A. Semantic Integrity (Tính toàn vẹn ngữ nghĩa)
- Xác định rõ: mục tiêu của hình, người đọc, nguồn sự thật và mức độ trừu tượng.
- Chọn công cụ dựa trên thông tin cần truyền tải, không chọn chỉ vì renderer đó tiện nhất.
- Tuyệt đối không tự vẽ quan hệ Foreign Key dựa trên tên cột giống nhau mà chưa kiểm tra schema/migration thật.
- Khi minh họa BK-Tree, nhãn cạnh bắt buộc phải là khoảng cách Levenshtein chính xác 100% về mặt toán học. Không tự dựng cây sai để đối xứng hình.
- Phân biệt rõ: hệ thống đã chạy thực tế vs thiết kế đề xuất tương lai vs ví dụ minh họa nhỏ.

### B. Visual Quality, Density Control & Academic Monochrome
- Mặc định **Academic Monochrome**: Nền trắng `#FFFFFF`, viền và chữ đen `#000000`, 300 DPI, tương phản cao.
- **Zero-Title in Canvas:** Tiêu đề sơ đồ luôn nằm ở Caption tài liệu (*Hình X.Y: ...*), cấm dùng từ khóa `title` trong mã nguồn làm lặp chữ.
- **Kiểm soát mật độ liên tầng (Inter-tier Anti-Crowding):**
  - Trong sơ đồ kiến trúc (Layers / Packages / Components), **tuyệt đối không nhồi nhét dày đặc nhãn hành động CRUD, tìm kiếm, import/export** lên các đường nối giữa 2 tầng.
  - Sơ đồ kiến trúc chỉ thể hiện khối cấu trúc và quan hệ phụ thuộc cấp cao (`Phụ thuộc / Gọi API` hoặc `Yêu cầu nghiệp vụ`).
  - Chi tiết từng luồng tương tác, tham số và kết quả trả về **bắt buộc phân rã sang Sơ đồ Tuần tự (Sequence) hoặc Sơ đồ Hoạt động (Activity)** tương ứng.
- **Cân đối khoảng trắng & Cấu trúc RAM (RAM Data Structure Balance):**
  - Khi minh họa cây tiền tố Prefix Trie hoặc BK-Tree trong bộ nhớ: Phải chọn tập từ mẫu đại diện vừa phải (5–8 từ), phân nhánh tỏa đều từ gốc, **cấm dồn cục các node sang một bên làm trống nửa hình còn lại**.
  - Tỷ lệ khung hình chuẩn từ 4:3 đến 16:9 (ngang) hoặc 1:1, không được dẹt lép (> 3.8) hoặc dài ngoằng (< 0.28).
  - Khoảng cách thở tiêu chuẩn: `nodesep 70`, `ranksep 70`, đường nối vuông góc `linetype ortho`.
- Chữ tiếng Việt giữ nguyên dấu, font chuẩn hệ thống (`Segoe UI`, `Arial`).

### C. Source & Toolchain Execution
Mỗi sơ đồ phải lưu file nguồn và xuất đồng thời SVG (vector) + PNG (raster 300 DPI):
- **PlantUML:** `node .claude/skills/plantuml-diagrams/scripts/render-puml.mjs --in <path.puml>`
- **Graphviz DOT:** `node .claude/skills/diagram-orchestrator/scripts/render-graphviz.mjs --in <path.dot>`
- **tldraw:** `node .claude/skills/tldraw-diagrams/scripts/render.mjs --in <path.json> --png --scale 2`
- **Auditor:** `node .claude/skills/diagram-auditor/scripts/audit-diagrams.mjs <targetDir>`

---

## 4. QUY TRÌNH 4 CỔNG KIỂM ĐỊNH (THE 4-GATE VERIFICATION)

> [!CAUTION]
> **HỌC THUYẾT CHỐNG BÁO ẢO (ANTI-FALSE-PASS):**
> Script tự động báo 0 lỗi **KHÔNG ĐỒNG NGHĨA** với việc sơ đồ đạt chuẩn. Agent **BẮT BUỘC** phải tự mở ảnh soi mắt và đối chiếu mã nguồn thực tế trước khi xác nhận hoàn thành!

Mọi sơ đồ phải đi qua 4 cổng nghiệm thu độc lập trước khi bàn giao:

```text
[Nguồn sự thật / Yêu cầu]
           │
┌──────────▼──────────┐
│ Gate A — Correctness│ ➔ Đối chiếu schema, code, thuật toán. Đúng tên, PK/FK, hướng mũi tên, thứ tự message.
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ Gate B — Rendering  │ ➔ Cú pháp nguồn hợp lệ. Xuất đủ SVG + PNG > 500 bytes. Giữ nguyên dấu tiếng Việt.
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ Gate C — Visual QA  │ ➔ Chạy audit script + Soi mắt: Không chen chúc nhãn giữa các tầng, không dồn cục khoảng trắng.
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ Gate D — Document QA│ ➔ Đặt vào DOCX: Khớp 100% ảnh với Caption, có đoạn văn dẫn dắt, keep_with_next, chiều rộng 14-15.5cm.
└──────────┬──────────┘
           │
       [BÀN GIAO]
```

### Các trạng thái nghiệm thu:
- **`PASS`:** Tất cả 4 cổng bắt buộc đã qua với bằng chứng cụ thể, không còn bất kỳ điểm nghẽn thị giác nào.
- **`PASS WITH CONDITIONS`:** Kết quả sử dụng được nhưng có giới hạn mô hình hóa được nêu rõ trong báo cáo.
- **`BLOCKED`:** Thiếu nguồn sự thật hoặc công cụ lỗi, dừng lại báo cáo nguyên nhân.
- **`FAIL`:** Phát hiện lỗi nội dung, đè nhãn, dồn cục bố cục hoặc nhầm ảnh tài liệu; bắt buộc sửa và render lại.

---

## 5. BÀN GIAO TRỰC QUAN SẠCH (ZERO CODE DUMPS)

Khi báo cáo kết quả hoàn thành hoặc audit cho người dùng, Agent **TUYỆT ĐỐI KHÔNG** xả toàn bộ code block `.puml`, `.dot`, hay `.json` ra khung chat làm rối mắt. Báo cáo bàn giao chuẩn mực bắt buộc gồm:
1. **Ảnh sơ đồ trực quan (Rendered Preview):** `![Hình X.Y: Tên sơ đồ](path/to/diagram.png)`
2. **Tiêu đề hình chuẩn mực:** `*Hình X.Y: Tên sơ đồ*`
3. **Bảng tóm tắt kiểm định 4 Cổng:** Trạng thái Gate A, Gate B, Gate C, Gate D.
4. **Đường dẫn tệp nguồn:** Link markdown tới file trên đĩa `[ten_so_do.puml](file:///path/to/ten_so_do.puml)`.

---

## 6. CHECKLIST 12 MỤC NGHIỆM THU TRƯỚC KHI ĐƯA VÀO BÁO CÁO

- [ ] 1. Đã xác định đúng loại sơ đồ và câu hỏi duy nhất mà hình cần trả lời (1 sơ đồ = 1 câu hỏi).
- [ ] 2. Đã kiểm tra nguồn dữ liệu, schema hoặc mã nguồn làm căn cứ (không bịa thông tin).
- [ ] 3. Không nhầm lẫn giữa UML Class, ERD CSDL và Cấu trúc dữ liệu RAM (Trie/Tree).
- [ ] 4. Tên gọi, khóa, quan hệ, điều kiện và hướng mũi tên đều có căn cứ xác minh.
- [ ] 5. Sơ đồ kiến trúc không nhồi nhét chi tiết CRUD lên đường nối liên tầng (đã đưa sang Sequence).
- [ ] 6. Cấu trúc dữ liệu RAM (Trie / BK-Tree) cân đối, không lệch dồn cục, khoảng cách Levenshtein chính xác.
- [ ] 7. Đã chọn công cụ phù hợp nhất cho chính sơ đồ này (PlantUML / Graphviz / tldraw).
- [ ] 8. Đã lưu file nguồn có thể chỉnh sửa (`.puml`, `.dot`, `.tldr`) và xuất cả SVG + PNG 300 DPI.
- [ ] 9. Đã kiểm tra qua `audit-diagrams.mjs` và tự soi mắt trực quan (Anti-False-PASS).
- [ ] 10. Chữ, cạnh, dấu tiếng Việt và chú giải hiển thị rõ ràng ở kích thước in thực tế trên trang A4.
- [ ] 11. Caption và số thứ tự hình (*Hình X.Y*) đúng với bố cục báo cáo; không nhúng title trong canvas.
- [ ] 12. Khớp chính xác 100% file ảnh với Caption trong tài liệu DOCX, có văn bản dẫn nhập và `keep_with_next`.
