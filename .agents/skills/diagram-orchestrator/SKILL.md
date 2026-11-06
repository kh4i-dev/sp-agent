---
name: diagram-orchestrator
description: "Điều phối thông minh toàn bộ hệ thống sơ đồ kỹ thuật cho báo cáo Word (docx-report), slide (pptx-deck), đồ án tốt nghiệp và tài liệu kiến trúc. Tự động phân tích ngữ nghĩa và nguồn dữ liệu để chọn chính xác công cụ tối ưu cho từng sơ đồ riêng biệt (PlantUML cho UML/ERD chuẩn mực; Graphviz DOT cho cấu trúc cây Prefix Trie, BK-Tree, đồ thị thuật toán; tldraw/draw.io cho kiến trúc tổng thể trực quan tự do); áp dụng Giao thức Giải quyết Vấn đề Thông minh (Intelligent Problem-Solving Protocol), chuẩn thẩm mỹ Academic Monochrome (Trắng - Đen học thuật 300 DPI, không title nhúng trong ảnh) và bắt buộc đi qua cổng kiểm định diagram-auditor trước khi xuất bản. Dùng khi cần vẽ sơ đồ, chọn công cụ vẽ sơ đồ, diagram orchestrator, sơ đồ cây, trie, bk-tree, kiến trúc hệ thống, phối hợp sơ đồ."
---

> **Quy tắc hiện hành (02/11/2026):** bản cuối dùng `handdrawn-diagrams`: Python toạ độ cố định → `docs/diagrams/vectors/*.svg` + `docs/images/diagrams/*.png`, spec JSON riêng. PlantUML/Graphviz/Mermaid/drawio/tldraw trong các ví dụ bên dưới chỉ dùng nháp. Nguồn `.py` là bắt buộc. Duyệt ngữ nghĩa theo nguồn, chạy `run_diagrams.py` (cổng máy), rồi Vision QA từng hình; không suy PASS bố cục từ exit 0. Use Case chung gốc ở junction thân–tay `(ax, ay−4)` = tâm đầu +18 với mẫu hiện hành, không ở bụng. State đọc `plantuml-diagrams/reference/state-playbook.md`, không note/legend/footer trên canvas. Khi hướng dẫn cũ trái khối này, áp dụng khối này.


# Diagram Orchestrator Skill — Điều Phối Sơ Đồ Kỹ Thuật Thích Ứng

Mục tiêu: Đóng vai trò **nhạc trưởng điều phối (Orchestrator)** cho toàn bộ quy trình vẽ sơ đồ kỹ thuật. Skill vận hành theo **Giao thức Giải Quyết Vấn Đề Thông Minh (Intelligent Problem-Solving Protocol)**: không đơn thuần là người thực thi lệnh mù quáng (command executor), mà đóng vai trò như một Kiến trúc sư phần mềm, Chuyên gia phân tích miền và Người phản biện độc lập để tạo ra kết quả chính xác, rõ ràng, thẩm mỹ và có thể kiểm chứng bằng bằng chứng thực tế.

Sơ đồ đẹp không cứu được mô hình sai; sơ đồ đúng nhưng khó đọc cũng chưa hoàn thành nhiệm vụ. Phải bảo đảm cả ba: **đúng nội dung, đúng cách biểu diễn và đúng chất lượng hình ảnh**.

> **ĐỒNG BỘ QUY TẮC LIÊN SKILL (Single Source of Truth) — mọi skill sơ đồ defer về đây:**
> - **Màu:** báo cáo/đồ án/luận văn học thuật = **zero-color tuyệt đối** (kể cả khi ảnh mẫu có màu). Chỉ branded/presentational mới được dùng màu (`diagram-design`, `theme-factory`).
> - **Tiêu đề nhúng:** cấm banner tiêu đề trong `.puml/.dot/.svg/.png`; caption do `docx-report` sinh (`Hình X.Y: ...`).
> - **Bước 0 (path canonical):** `docs/domain/step0-<du-an>.md` — mọi skill dùng đúng path này.
> - **Tỷ lệ khung:** khuyến nghị **0.5–2.4**; **hard-fail** của `audit-diagrams.mjs` khi ratio `> 3.8` hoặc `< 0.28`.
> - **Số node:** sơ đồ chi tiết (PlantUML/Graphviz) ≤ 15; sơ đồ trình chiếu/khái niệm ≤ 9; lõi khái niệm 7 ± 2.
> - **Cỡ chữ:** ≥ 9pt khi in A4.
> - **Độ phân giải:** PlantUML/Graphviz = 300 DPI; tldraw/diagram-design = scale 2×.
> - **Xuất file:** pipeline học thuật xuất **đồng thời SVG (vector) + PNG (raster)**; `diagram-design` (branded HTML) là ngoại lệ thủ công.
> - **Nơi lưu:** `docs/diagrams/` (nguồn `.puml/.dot/.tldr` + `.svg/.png`); `docs/screenshots/` chỉ chứa ảnh UI thật.

---

## 1. GIAO THỨC TƯ DUY & GIẢI QUYẾT VẤN ĐỀ (INTELLIGENT PROBLEM-SOLVING PROTOCOL)

### Mission
Act as a software architect, domain analyst, visual designer, and critical reviewer — not merely a command executor.
The objective is not to produce an artifact quickly or maximize successful tool calls. The objective is to produce the most suitable, correct, understandable, maintainable, and verifiable result for the user's actual problem.

### 1.1. Understand before acting
Before implementation, establish:
- What problem must be solved?
- What is the authoritative source of truth?
- What does success look like to the user?
- Which constraints are mandatory?
- Which facts remain uncertain?
- Which existing parts are already good and must not be degraded?

Inspect the actual repository, source files, existing skills, available tools, and relevant examples. Do not assume a claimed capability exists until it has been verified. Separate verified facts, reasonable inferences, design proposals, and unknowns. Do not invent facts to fill gaps.

### 1.2. Explore before committing to a solution
For non-trivial tasks, consider at least three genuinely different approaches before selecting one:
- Different suitable diagram types.
- Different ways to group and arrange components.
- Different placements or routing strategies.
- Whether one diagram should be split into multiple focused diagrams.
- Whether an existing renderer or skill already provides a better solution.

Do not generate cosmetic variations of the same flawed design and call them independent alternatives. Assess each candidate: semantic correctness, readability, maintainability, implementation cost, and known risks. Select the best-supported option and explain the decision concisely with evidence and trade-offs.

### 1.3. Preserve what already works
Inspect the existing result before rewriting it. Identify:
- What is correct and should remain.
- What is demonstrably wrong.
- What is merely a preference.
- What is uncertain and requires a test.

Make the smallest change that adequately solves the demonstrated problem. Never apply a local fix by destroying correct semantics, useful structure, or established project conventions. Do not turn a successful workaround into an absolute rule unless its general validity is established.

### 1.4. Use evidence-driven experimentation
When the cause of a problem is uncertain:
1. State a testable hypothesis.
2. Establish a reproducible baseline.
3. Change one relevant variable at a time (Single-Variable Isolation).
4. Re-run the affected process.
5. Compare the new result with the baseline.
6. Accept, reject, or refine the hypothesis based on evidence.

Do not claim a root cause merely because a change happened to improve the output.

### 1.5. Choose tools intelligently
Select tools according to the problem's semantics and practical requirements. Do not force every task through a single default tool:
- **PlantUML:** Structured UML (Use Case, Sequence, Class, State, Activity).
- **Graphviz (DOT):** Algorithmic graphs, trees (Prefix Trie, BK-Tree, AST).
- **draw.io / tldraw:** Freeform high-level architecture with visual regions.

Inspect capabilities and limitations of each tool before relying on it. A tool producing valid output is not proof that the output is semantically correct or visually usable.

### 1.6. Build a real feedback loop
After producing a result:
- Inspect the actual artifact.
- Compare it against explicit acceptance criteria.
- Use an adversarial reviewer that actively searches for failure modes.
- Record concrete defects with evidence.
- Fix identified causes rather than applying random cosmetic changes.
- Re-run all checks affected by the changes.

When image inspection is required, use a tool that actually exposes the rendered image to visual analysis (`view_file`). Opening a file in an OS application is not proof that the model inspected it.

### 1.7. Apply the protocol to diagrams
For every diagram, complete these stages:
A0. **(Use Case / mô hình miền) BẮT BUỘC làm Bước 0 trước:** tạo file `docs/domain/step0-<du-an>.md` theo template [`reference/step0-bai-toan-va-tac-nhan.md`](reference/step0-bai-toan-va-tac-nhan.md) — xác định bài toán, quy mô, số người vận hành, **trách nhiệm từng tác nhân** (phân biệt ai sửa lỗi IT vs ai không sửa lỗi IT nhưng chịu trách nhiệm nghiệp vụ), ranh giới hệ thống, quan hệ thật sự cần. **Không có file Bước 0 → CẤM vẽ** (vi phạm kỷ luật, sản phẩm bị bác bỏ).  
A. Define purpose, notation, audience, abstraction level, and source of truth.  
A1. **NGHĨ TRƯỚC KHI VẼ (Think-Before-Draw) — bắt buộc ra giấy:** trước khi viết code, phải (1) chọn công cụ theo SSOT [`reference/tool-sweet-spot.md`](reference/tool-sweet-spot.md), (2) lập **bảng adjacency-first** (quan hệ → zone) theo [`reference/layout-thinking.md`](reference/layout-thinking.md) §1, (3) **dự đoán bố cục** và chỗ dễ vỡ (nhãn dài, hub, cặp include/extend, hành lang dây). Chưa có kế hoạch → **chưa được viết một dòng code**. Cấm "render rồi tính".  
B. Validate semantics before choosing layout.  
C. Select the appropriate rendering tool.  
D. Plan layout and identify potentially difficult relationships or long labels.  
E. Generate editable source and render the actual image.  
F. Inspect rendered image for semantic errors, clipping, overlapping labels, poor spacing, unreadable text, and visual imbalance.  
G. If embedded in DOCX, inspect final rendered pages.  
H. Record final validation evidence and unresolved limitations.  
*Do not collapse all these stages into a single automated PASS.*

### 1.8. Learn from repeated failures
Maintain a concise failure record when recurring issues appear:
- Original problem & observed symptoms.
- Confirmed cause & experiment used to investigate it.
- Change that resolved it and conditions under which the fix is valid.
- Any remaining limitations.

### 1.9. Completion criteria
Before declaring a task complete, report:
- **Changed:** What was actually modified.
- **Decision:** Why the selected approach fits the problem.
- **Evidence:** What was inspected, executed, tested, rendered, or independently reviewed.
- **Remaining uncertainty:** What could not be verified.
- **Status:** PASS, PASS WITH CONDITIONS, FAIL, or BLOCKED.

---

## 1.10. BỘ NÃO TƯ DUY & ĐIỀU PHỐI VẼ HÌNH CHUẨN ĐẸP NHƯ CON NGƯỜI KÉO THẢ (HUMAN-GRADE INTERACTIVE DIAGRAMMING MINDSET)

Khi con người sử dụng các công cụ vẽ sơ đồ có tương tác kéo thả trực quan (như Draw.io, Lucidchart, Figma, Microsoft Visio), họ luôn tuân theo các nguyên lý tâm lý học Gestalt và trực giác không gian thẩm mỹ mà các bộ sinh mã tự động (code generators) thường bỏ sót. Để tạo ra sơ đồ chuẩn đẹp như người vẽ tay, Agent **BẮT BUỘC** áp dụng 7 nguyên lý tư duy sau:

### 1. Bounding Box co dãn tự nhiên — Tuyệt đối không đè/cắt đứt nét viền
- **Tư duy con người**: Khi thấy chuỗi văn bản dài hơn ô hình chữ nhật, con người sẽ **kéo rộng chiều ngang (width)** hoặc **tăng chiều cao (height)** của hộp để chữ nằm trọn vẹn bên trong với khoảng đệm an toàn (padding >= 12-16px).
- **Hành vi máy móc cần cấm**: Tuyệt đối **CẤM** dùng các thủ thuật che mắt như vẽ một miếng trắng (`<rect fill="#ffffff">`) đè lên viền ô chữ nhật làm mất nét ô, đứt nét viền, hoặc để chữ tràn ra cắt đứt đường biên.
- **Quy chuẩn viền**: Viền hình chữ nhật kỹ thuật/UML phải vuông vức 100% 90 độ (`rx=0, ry=0`), nét đen đơn sắc liền mạch, không bị đứt khúc hay chắp vá.

### 2. Nhãn chuyển trạng thái / Mũi tên kết thúc — Nổi trên đường & Tách biệt mép hộp
- **Tư duy con người**: Nhãn hành động/sự kiện chuyển trạng thái luôn được đặt nổi phía trên đường kẻ (`y - 8` hoặc `x + 10`), giữ khoảng cách thở (breathing room) >= 35-40px với mép các hộp trạng thái.
- **Hành vi máy móc cần cấm**: Không để chữ dính sát sạt vào mép hộp (< 25px) hoặc đè lên viền hộp; nhãn không được che mất đầu mũi tên.

### 3. Sequence Diagram — Giãn dòng thông thoáng & Tab Frame độc lập
- **Khoảng cách dọc giữa các bước (Lifeline Spacing)**: Con người kéo dãn tối thiểu **45–50px mỗi bước** (thay vì ép chật 20-25px như máy) để mắt người đọc dễ lần theo số thứ tự (autonumber) và nội dung thông điệp mà không bị dính chùm.
- **Khung nhóm/Giao dịch (Frame Transaction, Alt, Opt, Loop)**:
  - Tab nhãn góc trên (ví dụ: `group [Prisma $transaction]` hay `alt [Thành công]`) là một khối định danh độc lập.
  - Thông điệp đầu tiên bên trong khung phải có **khoảng đệm an toàn (safe margin) >= 30-35px** tính từ đỉnh khung xuống mũi tên đầu tiên. Tuyệt đối không để mũi tên hay chữ đè lên tab frame.

### 4. Sơ đồ Hiện trạng / Luồng xử lý (As-Is / Flow Diagram) — Luồng ngang & Mũi tên chỉ thẳng 90 độ
- Các bước của quy trình xếp ngang tuần tự với khoảng cách >= 45-55px.
- Các khối bất cập / nguyên nhân (Pain Points) đặt thẳng hàng ở bên dưới bước bị ảnh hưởng, dùng **mũi tên đỏ chỉ thẳng góc 90 độ đi lên**. Không vẽ đường chéo hay bắt chéo luồng gây rối mắt.

### 5. Sơ đồ Use Case — Phân vùng Actor theo vòng đời & Hành lang thông gió (Air Corridors)
- **Lane L (Trái)**: Xếp toàn bộ người dùng cuối (Khách vãng lai, Phụ huynh, Gia sư) theo tiến trình vòng đời tương tác từ trên xuống dưới.
- **Lane R (Phải)**: Dành riêng cho Quản trị viên (Admin), Kiểm duyệt viên (Moderator), Hệ thống bên ngoài (OTP, Cổng thanh toán).
- **Hành lang thông gió (Air Corridors)**: Cột giữa để lại khoảng hở dọc rộng rãi để các Use Case tương tác hai chiều (Chat, Đánh giá, Báo cáo) đón các đường nối từ hai phía mà **không cắt ngang qua bất kỳ Use Case độc lập nào**.

### 6. Chuẩn Học thuật Tuyệt đối — Zero-Title & Zero-Legend trong Canvas
- **CẤM nhúng tiêu đề to trong ảnh**: Tiêu đề thuộc về Caption của Word (`Hình X.Y: Tên sơ đồ`). Nhúng tiêu đề trong ảnh là lỗi trùng lặp tiêu đề thô thiển.
- **CẤM nhúng hộp chú thích nét đứt / note box / legend trong ảnh**: Mọi giải thích ký hiệu, từ viết tắt hoặc quy ước phải viết thành văn xuôi dẫn nhập hoặc phân tích bên dưới hình trong bài viết Word.

### 7. Quy trình Visual Audit Loop bằng Mắt Thật (LibreOffice & PyMuPDF)
- Script chạy exit code 0 chỉ chứng minh cú pháp không lỗi, KHÔNG chứng minh sơ đồ đẹp.
- **Bắt buộc**: Render file ra PDF qua LibreOffice (`soffice --headless --convert-to pdf`), dùng PyMuPDF render trang sang ảnh PNG và dùng công cụ xem ảnh (`view_file`) soi trực quan từng chi tiết bằng mắt trước khi bàn giao.

## 2. BÀI KIỂM TRA NĂNG LỰC TƯ DUY (3 LITMUS TESTS)

| Tình huống thực tế | Agent phản xạ máy móc (Cần tránh) | Agent thông minh (Bắt buộc) |
|---|---|---|
| **Nhãn cạnh chồng lên viền/node** | Xóa nhãn, xóa package, đổi hướng mũi tên cùng lúc mà không biết cái nào có tác dụng. | Đặt giả thuyết (do `splines=ortho` hoặc thiếu không gian), thử 1 biến (rút gọn nhãn / `xlabel` / tăng khoảng cách), so sánh trước/sau. |
| **Sơ đồ kiến trúc có quan hệ sai (nhảy cóc tầng)** | Giữ nguyên quan hệ sai để tránh phải vẽ lại bố cục; cố căn lề cho "đẹp". | Ưu tiên tính đúng đắn kiến trúc: sửa quan hệ cho đúng tầng dù phải tổ chức lại layout. |
| **Sơ đồ quá phức tạp, chằng chịt 20-30 node** | Cố nhét tất cả vào 1 hình, thu nhỏ cỡ chữ đến mức không đọc được. | Chủ động đề xuất phân rã: 1 hình tổng quan (5-8 khối) + các hình phân đoạn chuyên sâu (Sequence/Use Case). |

---

## 3. BẢY NGUYÊN TẮC XƯƠNG MÁU & NGUYÊN TẮC KỸ THUẬT CÓ ĐIỀU KIỆN

1. **Tìm nguồn sự thật trước khi vẽ:** Use Case dựa trên yêu cầu nghiệp vụ; ERD dựa trên schema/migration thật; Sequence dựa trên luồng xử lý mã nguồn; Class Diagram dựa trên class/interface thật. Tuyệt đối không tự bịa thêm `AdminService`, bảng `Logs`, lớp `Repository` hay Actor mới.
2. **Một sơ đồ chỉ trả lời một câu hỏi chính:** Không nhét chung bảng dữ liệu, hàm xử lý, luồng nghiệp vụ và cấu trúc RAM vào cùng một hình.
3. **Không đánh đồng mọi loại quan hệ:** Quan hệ UML không mặc nhiên là FK trong CSDL; Lời gọi hàm trong Sequence không phải quan hệ kế thừa; Đường nối trong flowchart không phải lúc nào cũng là luồng dữ liệu.
4. **Phân biệt mô hình thiết kế với hiện trạng triển khai:** Nếu mô tả hệ thống đang chạy, phải đối chiếu 100% với mã nguồn hiện hành.
5. **Không ép mọi sơ đồ vừa một trang bằng cách thu nhỏ chữ:** Kích thước chữ phải đọc rõ ở kích thước in thực tế trên trang A4. Nếu quá tải, bắt buộc phân rã sơ đồ.
6. **Mỗi sơ đồ phải có tệp nguồn để sửa lại:** Giữ nguyên `.puml`, `.dot` hoặc `.tldr`. PNG và SVG chỉ là đầu ra.
7. **Không tuyên bố PASS chỉ vì công cụ render thành công:** Phải qua kiểm tra độc lập cả về ngữ nghĩa lẫn hình học.
8. **Chốt ngữ nghĩa trước khi bố cục:** Xác định rõ component diagram (tĩnh), data-flow diagram (dữ liệu) hay sequence diagram (thời gian).
9. **Chỉ dùng nhãn dài khi có đủ không gian hình học:** Không đặt nhãn dài lên ranh giới package hoặc vùng giao nhau chật hẹp.
10. **Layout là cấu hình phải được kiểm chứng thực nghiệm (Single-Variable Isolation):** Khi gặp lỗi bố cục, chỉ đổi 1 biến tại 1 thời điểm. Cấm xóa package và phá vỡ cấu trúc tổng thể một cách mù quáng.
11. **Phân định rạch ròi Ảnh chụp (Screenshots) vs. Sơ đồ (Diagrams):**
    - `docs/screenshots/`: 100% CHỈ chứa ảnh chụp màn hình UI thực tế (`01_*.png` -> `09_*.png`). CẤM để sơ đồ hoặc file `.puml`/`.dot` vào đây.
    - `docs/diagrams/`: Chứa mã nguồn sơ đồ (`.puml`, `.dot`) và file xuất vector/raster (`.svg`, `.png`).
    - Bàn giao trực quan sạch: CẤM xả mã nguồn sơ đồ ra chat gây tràn màn hình; chỉ lưu file đĩa và nhúng ảnh render preview kèm link.
12. **Kỷ luật thư mục công cụ (Dedicated Tools):** Toàn bộ script hỗ trợ (render, audit, convert) phải nằm trong `tools/` hoặc `docs/tools/`, tuyệt đối CẤM rải rác ở thư mục gốc dự án.
13. **Kỷ luật Bước 0 — Không hiểu bài toán thì cấm vẽ (Iron Discipline):** Sơ đồ Use Case/mô hình miền chỉ được bắt đầu sau khi có file Bước 0 **đã xác minh bằng bằng chứng** (mỗi trách nhiệm tác nhân trỏ nguồn; chỗ chưa rõ ghi `UNKNOWN`, cấm tự suy diễn). Nếu Agent vẽ khi chưa có file này, **BẮT BUỘC tự tố cáo vi phạm** (`⚠️ VI PHẠM KỶ LUẬT: thiếu Bước 0`), dừng lại, làm lại từ gốc. **Nghiệm thu gồm 2 cổng tách biệt:** Semantic Review (nghiệp vụ/UML) và Visual Review (hình học) — **thiếu Bước 0 = FAIL nghiệp vụ**, dù hình đẹp tới đâu; và **cấm căn chỉnh bố cục để che lỗi mô hình**. Không tự tha thứ, không nể nang.

---

### 3.6. CLASS DIAGRAM NHIỀU QUAN HỆ — HUB, DENSITY, PARALLEL ROLES

**SSOT bắt buộc:** đọc [reference/class-diagram-layout.md](reference/class-diagram-layout.md) trước khi tạo/sửa Class Diagram có từ 6 lớp trở lên, có lớp bậc cao, hoặc có nhiều association giữa cùng một cặp lớp.

Trước khi viết PlantUML, lập bảng lớp/nhóm/bậc (degree)/các association song song. Sau khi render, bắt buộc xem:
- Lớp hub (degree >= 5) có bị đẩy ra rìa khiến các cạnh kéo qua toàn hình không.
- Các association cùng cặp lớp có vai trò khác nhau (ví dụ Review–User reviewer/reviewee) có bị đè hoặc gây nhầm cạnh không.
- Số lớp/quan hệ trong source có khớp với comment, model và render không.
- Các hidden links có đang ép thứ tự khai báo thành bố cục xấu không.
- Vùng trắng có cân đối; không chỉ nhìn tỷ lệ khung tổng thể.
- Đường nối có giao cắt, chạy sát song song hoặc vòng xa dù syntax/render thành công hay không.

**Không coi cấu hình là nghiệm thu:** linetype ortho, nodesep, ranksep, package, together và hidden links không chứng minh không giao cắt. Thử một thay đổi mỗi vòng; nếu hai vòng hữu ích vẫn thất bại về hình học, dùng manual-fallback hoặc phân rã theo domain. Không tự động xóa/gộp association khác vai trò. Tách rõ Semantic Review và Visual Review.

## 4. BẢNG ĐỊNH TUYẾN: LOẠI SƠ ĐỒ NÀO CHO CÂU HỎI NÀO?

| Khi cần trả lời câu hỏi... | Loại sơ đồ | Công cụ tối ưu | Định dạng & Renderer |
|---|---|---|---|
| Ai sử dụng hệ thống, muốn đạt mục tiêu nghiệp vụ gì? | **Use Case** | **VẼ TAY: draw.io/SVG** (PlantUML chỉ nháp) | `.drawio`/`.svg` → exporter | 
| Quy trình xử lý nghiệp vụ đi qua những bước và điều kiện nào? | **Activity** | **VẼ TAY: draw.io/SVG** (PlantUML chỉ nháp) | `.drawio`/`.svg` → exporter |
| Những đối tượng/lớp nào tồn tại, trách nhiệm và quan hệ ra sao? | **Class** | **PlantUML auto** (nhỏ), **draw.io tay/phân rã** (≥6 lớp, hub) | `.puml` / `.drawio` |
| Dữ liệu lưu trữ thế nào, khóa chính/ngoại và quan hệ ra sao? | **ERD** | **PlantUML (auto)** | `.puml` → `render-puml.mjs` |
| Thành phần nào gửi thông điệp cho thành phần nào, theo thứ tự gì? | **Sequence** | **PlantUML** | `.puml` → `render-puml.mjs` |
| Một đối tượng trải qua những trạng thái nào trong vòng đời? | **State Machine**| **VẼ TAY: draw.io/SVG** (PlantUML chỉ nháp) | `.drawio`/`.svg` → exporter |
| Hệ thống gồm những khối phần mềm lớn nào và phụ thuộc nhau ra sao? | **Component** | **PlantUML / tldraw** | `.puml` hoặc `.tldr` |
| Phần mềm chạy ở máy/môi trường nào, kết nối mạng ra sao? | **Deployment**| **PlantUML / tldraw** | `.puml` hoặc `.tldr` |
| Cấu trúc cây tiền tố Prefix Trie, BK-Tree, đồ thị thuật toán? | **Data Structure**| **Graphviz (DOT)** | `.dot` → `render-graphviz.mjs` |
| Kiến trúc tổng quan cần bố trí tự do, bo góc mềm mại, theo vùng? | **High-Level Arch**| **tldraw / draw.io** | `.tldr` → `render.mjs` |
| Luồng dữ liệu đi giữa tiến trình, kho dữ liệu và thực thể ngoài? | **DFD** | **draw.io / tldraw** | `.tldr` / vector |

> [!IMPORTANT]
> **CHỌN VẼ TAY hay AUTO — đọc SSOT [`reference/tool-sweet-spot.md`](reference/tool-sweet-spot.md):**
> **AUTO đẹp** khi bố cục là hệ quả tất định của cấu trúc: **Sequence, Trie/BK-Tree/AST, ERD vừa, Class nhỏ**.
> **VẼ TAY (draw.io/SVG) chuẩn** khi bố cục cần vị trí tuyệt đối do người quyết: **Use Case (bắt buộc)**, **State Machine (bắt buộc)**, **Activity (bắt buộc)**, **Class ≥ 6 lớp/có hub**, **kiến trúc tổng quan, DFD, Deployment trực quan**.
> **Bẫy kiểm soát vị trí:** PlantUML/Graphviz **KHÔNG ghim được vị trí** từng phần tử (dễ dồn actor về một phía). Đừng ép PlantUML ghim vị trí bằng hack vô ích — chuyển **draw.io / SVG vẽ tay**.
> Ngưỡng + quy trình vẽ tay: [`reference/manual-fallback.md`](reference/manual-fallback.md).

### Bẫy kinh điển: Class Diagram không thay thế ERD & Cấu trúc RAM

| Tiêu chí | Class Diagram (Thiết kế lớp) | ERD (Cơ sở dữ liệu) | Cấu trúc dữ liệu RAM (Trie/Tree) |
|---|---|---|---|
| **Trọng tâm** | Cấu trúc đối tượng OOP | Mô hình dữ liệu lưu trữ bền vững | Tổ chức bộ nhớ tạm thuật toán |
| **Thể hiện** | Field, method, kế thừa, visibility | Bảng, cột, PK, FK, quan hệ 1-N, N-N | Nút, cạnh, ký tự, khoảng cách |
| **Phương thức** | Có (`login()`, `search()`) | **CẤM** đưa phương thức vào ERD | Không áp dụng |
| **Công cụ** | PlantUML | PlantUML Crow's foot | **Bắt buộc dùng Graphviz DOT** |

---

## 5. UNIVERSAL DIAGRAM ENGINEERING RULES

### A. Semantic Integrity (Tính toàn vẹn ngữ nghĩa)
- Xác định rõ: mục tiêu của hình, người đọc, nguồn sự thật và mức độ trừu tượng.
- Chọn công cụ dựa trên thông tin cần truyền tải, không chọn chỉ vì renderer đó tiện nhất.
- Tuyệt đối không tự vẽ quan hệ Foreign Key dựa trên tên cột giống nhau mà chưa kiểm tra schema/migration thật.
- Khi minh họa BK-Tree, nhãn cạnh bắt buộc phải là khoảng cách Levenshtein chính xác 100% về mặt toán học. Không tự dựng cây sai để đối xứng hình.

### B. Visual Quality, Density Control & Academic Monochrome
- Mặc định **Academic Monochrome**: Nền trắng `#FFFFFF`, viền và chữ đen `#000000`, 300 DPI, tương phản cao.
- **LUẬT ZERO-COLOR BẤT BIẾN (kể cả khi ảnh mẫu người dùng có màu):** Nếu người dùng gửi sơ đồ mẫu nhiều màu, Agent **chỉ sao chép cấu trúc/bố cục/nhóm/quan hệ**, tuyệt đối **KHÔNG sao chép màu**. Nhóm màu trong ảnh mẫu phải dịch sang `package`/`rectangle`, nét liền-đứt, `<<stereotype>>`. Mọi mã màu phi thang độ xám (`max(R,G,B) - min(R,G,B) > 12`) trong SVG render = **FAIL** (script `audit-diagrams.mjs` chặn cứng, trừ khi có ghi đè tường minh `override-monochrome: true`).
- **Cổng bố cục đẹp đo được (Layout Beauty Gate):** cỡ chữ nhỏ nhất ≥ 9pt; tỷ lệ khung 0.5–2.4; không node mồ côi/node trùng chồng; không cụm dồn cục (≥3 node < 30px); trọng tâm khối không lệch > 20%/trục; tổng node/hình ≤ 15 (vượt → bắt buộc phân rã).
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
- **Vẽ tay fallback (khi auto ≥ 2 vòng vẫn FAIL Visual):** theo [`reference/manual-fallback.md`](reference/manual-fallback.md) — freeze ngữ nghĩa, dựng `.drawio`/`.tldr`/`.svg` tay, xuất đủ SVG+PNG, qua auditor như bản auto.

---

## 6. QUY TRÌNH KIỂM ĐỊNH & BÁO CÁO 5 KẾT QUẢ ĐỘC LẬP

> [!CAUTION]
> **HỌC THUYẾT CHỐNG BÁO ẢO & HARD ACCEPTANCE GATE (NO SELF-CERTIFIED PASS):**
> 1. Xác minh file PNG tồn tại, không rỗng và mở được bình thường.
> 2. **Dùng công cụ xem ảnh đưa nội dung hình ảnh vào ngữ cảnh của model** (như `view_file` trên PNG) để kiểm tra PNG thực tế.
> 3. **CẤM coi `os.startfile()`, `Start-Process`, đọc kích thước ảnh, metadata hay đọc source code `.puml` là bằng chứng đã kiểm tra ảnh.**
> 4. **Tách biệt 2 vai trò (Generator vs Adversarial Reviewer):** Người kiểm định phải chủ động tìm lỗi để bác bỏ sản phẩm chưa đạt, không được tự động đồng ý hay tự cấp chứng chỉ hoàn thành cho chính mình.
> 5. **KHÔNG GỘP NĂM KẾT QUẢ DƯỚI ĐÂY THÀNH MỘT TRẠNG THÁI PASS DUY NHẤT NẾU CÒN BƯỚC CHƯA ĐƯỢC KIỂM CHỨNG.**
> 6. **LUẬT CHỐNG LÀM ẨU (ANTI-RUSH) — BẮT BUỘC SOI ẢNH TRƯỚC KHI NÓI "XONG":** Việc vẽ nhanh rồi báo xong mà **chưa thực sự đưa ảnh vào tầm nhìn của model** là **lỗi nặng nhất**. Trước mọi chữ `PASS`/`xong`/`hoàn thành`, Agent **BẮT BUỘC**:
>    - **Nạp PNG vào ngữ cảnh model** bằng công cụ đọc ảnh thật (ví dụ `read` trên file `.png`, hoặc trình xem ảnh của harness) — **không** chỉ mở bằng app hệ điều hành.
>    - **Dán khối Proof-of-View**: ≥ 3 nhãn đọc **nguyên văn từ ảnh** + vị trí + trả lời rõ **đè? đều? dễ nhìn?** + tên file/dung lượng/thời điểm.
>    - Tự hỏi: *"Tôi có thể trích 3 nhãn nguyên văn từ ảnh không?"* **Không trích được = CHƯA xem ảnh = CẤM PASS.**
>    - Không nạp được ảnh (thiếu công cụ) → báo `BLOCKED — Visual QA unavailable`, **tuyệt đối không PASS**. Thà nói chưa xong còn hơn bàn giao ảnh sai/chữ đè mà chưa nhìn.

Báo cáo nghiệm thu cuối cùng **BẮT BUỘC** trình bày tách bạch 5 mục:
1. **Render validation:** File PNG & SVG tồn tại, > 500B, biên dịch sạch không có banner compiler, SVG **không chứa mã màu phi thang độ xám**.
2. **Automated audit:** Script `audit-diagrams.mjs` báo **0 LỖI ĐỎ** (không đè toạ độ, tỷ lệ khung hình chuẩn, **đạt ZERO-COLOR**, **cỡ chữ ≥ 9pt**). Cảnh báo VÀNG phải được Agent soi mắt phân xử.
3. **Actual visual inspection:** Agent trực tiếp xem ảnh PNG trong model context: nét chữ thoáng, không chen chúc nhãn giữa các tầng, không lệch dồn cục khoảng trắng.
4. **Semantic correctness:** Đối chiếu 100% với schema DB, mã nguồn backend hoặc thuật toán (không vi phạm nhảy cóc tầng như `UI -> Store`, đúng PK/FK, đúng khoảng cách Levenshtein).
5. **DOCX rendered-page inspection:** Đã kiểm tra trang Word thực tế sau chèn hình (chiều rộng 14–15.5cm, khớp caption Hình X.Y, có `keep_with_next` chống rớt trang).

### Các trạng thái nghiệm thu:
- **`PASS`:** Tất cả 5 mục bắt buộc đều đạt với bằng chứng cụ thể.
- **`PASS WITH CONDITIONS`:** Kỹ thuật và thị giác đạt, nhưng có giới hạn mô hình hóa được nêu rõ.
- **`BLOCKED — Visual QA unavailable`:** Thiếu công cụ xem ảnh hoặc thiếu schema nguồn.
- **`FAIL`:** Phát hiện lỗi nội dung, đè nhãn, dồn cục khoảng trắng hoặc nhầm ảnh tài liệu; bắt buộc sửa và render lại.

---

## 7. CỔNG NGƯỜI DÙNG NGHIỆM THU — HỎI TRƯỚC KHI THAY VÀO DOCX

> [!IMPORTANT]
> **QUY TẮC CHỜ NGƯỜI DÙNG DUYỆT (USER ACCEPTANCE CHECKPOINT):**
> Sau khi tạo ảnh và báo cáo kiểm định 5 cổng, Agent **DỪNG LẠI**, tuyệt đối **KHÔNG TỰ Ý GHI ĐÈ/SWAP ẢNH VÀO FILE WORD** nếu chưa có sự xác nhận của người dùng!
> 
> Agent phải hiển thị ảnh trực quan và hỏi người dùng câu hỏi nghiệm thu chuẩn:
> *"Tôi đã hoàn thành bản vẽ và kiểm định 5 cổng phía trên. Bạn kiểm tra trực quan giúp tôi: Ảnh đã đạt yêu cầu để thay thế luôn vào tài liệu Word chưa, hay cần sửa đổi/tinh chỉnh ảnh nào? Vui lòng phản hồi để tôi tiến hành bước tiếp theo!"*

---

## 8. BÀN GIAO TRỰC QUAN SẠCH (ZERO CODE DUMPS)

Khi báo cáo kết quả hoàn thành hoặc audit cho người dùng, Agent **TUYỆT ĐỐI KHÔNG** xả toàn bộ code block `.puml`, `.dot`, hay `.json` ra khung chat làm rối mắt. Báo cáo bàn giao chuẩn mực bắt buộc gồm:
1. **Ảnh sơ đồ trực quan (Rendered Preview):** `![Hình X.Y: Tên sơ đồ](path/to/diagram.png)`
2. **Tiêu đề hình chuẩn mực:** `*Hình X.Y: Tên sơ đồ*`
3. **Báo cáo riêng biệt 5 kết quả kiểm chứng:** Trình bày độc lập (Render, Automated, Visual, Semantic, DOCX).
4. **Câu hỏi xin ý kiến nghiệm thu người dùng** (theo Mục 7).
5. **Đường dẫn tệp nguồn:** Link markdown tới file trên đĩa `[ten_so_do.puml](file:///path/to/ten_so_do.puml)`.

---

## 9. CHECKLIST 14 MỤC NGHIỆM THU TRƯỚC KHI ĐƯA VÀO BÁO CÁO

- [ ] 0. **Bước 0 (bắt buộc):** Đã có file `step0-<du-an>.md` xác định bài toán, quy mô, số người vận hành, trách nhiệm từng tác nhân (phân biệt ai sửa lỗi IT / ai không), ranh giới hệ thống — TRƯỚC khi vẽ.
- [ ] 1. Đã xác định đúng loại sơ đồ và câu hỏi duy nhất mà hình cần trả lời (1 sơ đồ = 1 câu hỏi).
- [ ] 2. Đã kiểm tra nguồn dữ liệu, schema hoặc mã nguồn làm căn cứ (Semantic correctness).
- [ ] 3. Kiểm tra mâu thuẫn kiến trúc (không có đường nhảy cóc tầng như `UI -> Store` trong kiến trúc 3 lớp).
- [ ] 4. Không nhầm lẫn giữa UML Class, ERD CSDL và Cấu trúc dữ liệu RAM (Trie/Tree).
- [ ] 5. Sơ đồ kiến trúc không nhồi nhét chi tiết CRUD lên đường nối liên tầng (đã đưa sang Sequence).
- [ ] 6. Cấu trúc dữ liệu RAM (Trie / BK-Tree) cân đối, không lệch dồn cục, khoảng cách Levenshtein chính xác.
- [ ] 7. Đã chọn công cụ phù hợp nhất cho chính sơ đồ này (PlantUML / Graphviz / tldraw).
- [ ] 8. Render validation: File nguồn hợp lệ, xuất đủ cả SVG + PNG 300 DPI > 500B.
- [ ] 9. Automated audit: Vượt qua `audit-diagrams.mjs` (không đè toạ độ, tỷ lệ khung hình chuẩn).
- [ ] 10. Actual visual inspection: Đã trực tiếp mở ảnh PNG bằng công cụ xem ảnh vào ngữ cảnh model để soi mắt.
- [ ] 11. DOCX rendered-page inspection: Khớp 100% file ảnh với Caption Hình X.Y, có câu dẫn nhập và `keep_with_next`.
- [ ] 12. Báo cáo độc lập 5 kết quả kiểm chứng, không gộp thành 1 chữ PASS duy nhất khi chưa kiểm chứng đủ.
- [ ] 13. Dừng lại hỏi người dùng nghiệm thu ảnh trước khi thực hiện hành động thay ảnh vào file Word.

---

## 10. TÀI NGUYÊN NÂNG CAO & BỘ KIỂM THỬ (EVALS & REFERENCES)

Theo chuẩn thiết kế Progressive Disclosure của OpenAI Codex và Anthropic Claude Code, các tài nguyên đào sâu được tổ chức độc lập để nạp khi cần:
- **Bước 0 — Xác định bài toán & vai trò tác nhân (BẮT BUỘC trước khi vẽ Use Case):** [`reference/step0-bai-toan-va-tac-nhan.md`](reference/step0-bai-toan-va-tac-nhan.md) (Problem statement, quy mô, ma trận trách nhiệm tác nhân **kèm nguồn bằng chứng / UNKNOWN**, ranh giới hệ thống, luồng lỗi–kiểm duyệt nếu có, ví dụ điền mẫu **trung tính**). Tác nhân của dự án cụ thể được điền ở bản copy theo dự án, KHÔNG hard-code vào skill.
- **Điểm ngọt công cụ — loại nào AUTO đẹp, loại nào phải VẼ TAY (SSOT):** [`reference/tool-sweet-spot.md`](reference/tool-sweet-spot.md) (bảng loại sơ đồ → công cụ → vẽ tay/auto → lý do + bằng chứng; luật chọn 1 câu).
- **Vẽ tay fallback — khi auto-layout vẫn xấu (SSOT):** [`reference/manual-fallback.md`](reference/manual-fallback.md) (ngưỡng, 3 đường draw.io/tldraw/SVG, quy trình 6 bước, checklist PASS).
- **Tư duy bố cục cho AI — NGHĨ trước khi vẽ (SSOT):** [`reference/layout-thinking.md`](reference/layout-thinking.md) (adjacency-first: bảng quan hệ→zone trước khi viết code; trục luồng deployment; ngân sách cạnh 2.5× + test 4 góc; nhãn đủ dấu tiếng Việt; sàn spacing; checklist 60 giây).
- **Nguyên tắc thiết kế thị giác & bố cục:** [`reference/design-principles.md`](reference/design-principles.md) (Visual hierarchy, whitespace budget, routing, typography, khổ in A4).
- **Thư viện tương phản Mẫu Tốt & Mẫu Lỗi (Gallery):** [`reference/diagram-gallery.md`](reference/diagram-gallery.md) (Đối chiếu mẫu đúng vs mẫu sai cho Use Case, Class, ERD, Sequence, Architecture, Trie/BK-Tree).
- **Chuẩn hệ sinh thái Agent chính thức:** [`reference/benchmark-ecosystem.md`](reference/benchmark-ecosystem.md) (Nghiên cứu kiến trúc từ `openai/codex`, `anthropics/claude-code`, `openai/plugins`, `anthropics/skills`).
- **Bộ bài kiểm thử đánh giá chất lượng (Evals Suite):** [`evals/README.md`](evals/README.md) — Chạy test runner: `node .claude/skills/diagram-orchestrator/scripts/run-evals.mjs`.

---

## ⚡ PROMPT BẮT BUỘC KHI GỌI SKILL NÀY (COPY VÀO PROMPT AGENT)

> **KHI BẠN ĐƯỢC YÊU CẦU VẼ/AUDIT/ĐIỀU PHỐI SƠ ĐỒ, BẮT BUỘC TUÂN THỦ GIAO THỨC 10 GIAI ĐOẠN (A0–H) — KHÔNG BƯỚC NÀO ĐƯỢC BỎ QUA:**
>
> **A0. BƯỚC 0 (Use Case/Domain): TẠO FILE `docs/domain/step0-<du-an>.md` TRƯỚC KHI VẼ**
> - Xác định: bài toán, quy mô, số người vận hành, **trách nhiệm từng tác nhân** (phân biệt ai sửa lỗi IT vs ai chịu trách nhiệm nghiệp vụ KHÔNG sửa lỗi IT), ranh giới hệ thống, quan hệ thật sự cần.
> - Mỗi trách nhiệm **phải có bằng chứng** (`[REQ-xx]`, `[BRD §x.y]`, `[code:file:line]`, `[user-confirmed YYYY-MM-DD]`). Chưa rõ ghi `UNKNOWN`. **Cấm tự suy diễn**.
> - **Thiếu file Bước 0 = DỪNG, KHÔNG VẼ**, báo: `⚠️ VI PHẠM KỶ LUẬT: thiếu Bước 0 — lỗi tư duy mô hình hóa.`
>
> **A. XÁC ĐỊNH MỤC ĐÍCH & NGUỒN SỰ THẬT:** 1 sơ đồ = 1 câu hỏi. Nguồn: schema DB / mã nguồn / yêu cầu nghiệp vụ.
> **B. VALIDATE SEMANTICS TRƯỚC KHI CHỌN LAYOUT:** Đối chiếu 100% với thực tế. Không nhảy tầng (UI→Store). Không nhầm UML Class ↔ ERD ↔ Trie.
> **C. CHỌN CÔNG CỤ THEO NGỮ NGHĨA (SSOT `tool-sweet-spot.md`):**
>    - **AUTO đẹp:** Sequence, ERD vừa, Class nhỏ, Trie/BK-Tree/AST → PlantUML/Graphviz
>    - **VẼ TAY (draw.io/SVG) chuẩn:** Use Case (**bắt buộc**), State Machine (**bắt buộc**), Activity (**bắt buộc**), Class ≥6 lớp/có hub, kiến trúc tổng quan, DFD, Deployment trực quan
> **D. NGHĨ TRƯỚC KHI VẼ (bắt buộc):** lập bảng adjacency-first + chọn zone + dự đoán bố cục **trước khi viết một dòng code** (`layout-thinking.md` §1–§2).
> **D1. LẬP BẢNG ADJACENCY-FIRST** (`docs/diagrams/<ten>-model.md`): Mỗi FK/association = 1 dòng, kèm zone + có-bắt-buộc-ngắn. Theo `layout-thinking.md` §1.
> **E. SINH NGUỒN + RENDER THỰC TẾ:** Chạy script render tương ứng, xuất **ĐỒNG THỜI SVG + PNG 300DPI**.
> **F. INSPECT RENDERED IMAGE — BẮT BUỘC SOI ẢNH (ANTI-RUSH):**
>    - Chạy `audit-diagrams.mjs` → 0 lỗi ĐỎ (chỉ là cổng phụ, KHÔNG thay mắt soi)
>    - **Nạp PNG vào ngữ cảnh model** (vd `read` file `.png`) — không phải mở bằng app hệ điều hành
>    - Ghi Proof-of-View: **≥3 nhãn nguyên văn từ ảnh** + vị trí + **đè? đều? dễ nhìn?** + tên file/dung lượng/hash
>    - **Không trích được 3 nhãn = chưa xem ảnh = CẤM PASS.** Thiếu công cụ → `BLOCKED — Visual QA unavailable`
> **G. NẾU CHÈN VÀO DOCX: KIỂM TRA TRANG WORD THỰC TẾ** (rộng 14–15.5cm, khớp caption, `keep_with_next`).
> **H. GHI NHẬN BẰNG CHỨNG & TRẠNG THÁI:** PASS / PASS WITH CONDITIONS / FAIL / BLOCKED — tách 5 cổng riêng.
>
> **QUY TẮC DỪNG VÁ THAM SỐ (STOP PARAMETER TWEAKING):** Chỉ 1 lần thử khóa rank/hidden link. Không giữ rank → dừng, chuyển vẽ tay/phân rã (`manual-fallback.md`). **Cấm vá vô hạn.**
>
> **NGƯỠNG CHUYỂN VẼ TAY:** ≥ 2 vòng render→soi→sửa-1-biến vẫn FAIL Visual → freeze ngữ nghĩa, dựng `.drawio`/`.tldr`/SVG tay, qua auditor như bản auto.
>
> **ADVERSARIAL REVIEWER:** Bạn là người **chủ động tìm lỗi để bác bỏ**. Hỏi: *"Đâu là 3 lỗi tôi có thể tìm ra để FAIL sơ đồ này?"*
>
> **ZERO CODE DUMPS:** Bàn giao chỉ gồm: ảnh `![Hình X.Y](path)`, caption `Hình X.Y: <tên>`, báo cáo 5 cổng, câu hỏi nghiệm thu user, link file nguồn. **CẤM xả code block ra chat.**
