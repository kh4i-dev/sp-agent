---
name: diagram-auditor
description: Audit và kiểm định chất lượng sơ đồ kỹ thuật (PlantUML, Graphviz DOT, tldraw, SVG, PNG) trước khi gửi cho người dùng hoặc chèn vào báo cáo Word (docx-report). Ngăn chặn dứt điểm hội chứng False PASS (script chạy 0 lỗi nhưng nhìn bằng mắt vẫn méo mó, đè nhãn, dồn cục). Kiểm soát 4 cổng độc lập (Gate A Ngữ nghĩa, Gate B Biên dịch, Gate C Soi mắt Visual QA, Gate D Tích hợp DOCX). Kích hoạt khi người dùng yêu cầu "audit ảnh", "kiểm tra sơ đồ", "soi ảnh trước khi gửi", "diagram bị méo", "sơ đồ xấu", hoặc tự động chạy như một Quality Gate bắt buộc trước khi bàn giao bất kỳ sơ đồ nào.
---

# Diagram Auditor Skill — Cổng Kiểm Định Chất Lượng Sơ Đồ & Chống Báo Ảo (Anti-False-PASS)

Mục tiêu: Đảm bảo **100% sơ đồ xuất bản** đạt chuẩn kỹ thuật và thẩm mỹ in ấn học thuật cao cấp. Chặn đứng tận gốc tình trạng **"Script báo PASS nhưng mắt nhìn thấy FAIL"** — tức là file render được không lỗi cú pháp nhưng bố cục chật chội, nhãn đè nhau, khoảng trắng mất cân đối, hoặc nhầm lẫn hình ảnh trong tài liệu.

---

## 1. NGUYÊN TẮC CỐT LÕI: HỘI CHỨNG BÁO ẢO & THE ANTI-FALSE-PASS DOCTRINE

> [!CAUTION]
> **HỘI CHỨNG BÁO ẢO (FALSE PASS SYNDROME):**
> Script tự động (`audit-diagrams.mjs`) trả về exit code `0` chỉ là **ĐIỀU KIỆN CẦN (Gate B & một phần Gate C sơ bộ)**, **TUYỆT ĐỐI KHÔNG PHẢI ĐIỀU KIỆN ĐỦ**.
> Một sơ đồ vượt qua script vẫn có thể hoàn toàn **FAIL** về mặt thị giác và ngữ nghĩa:
> - **Hình 3.1 (Kiến trúc 3 lớp):** Nhiều mũi tên từ UI về Business Logic chen chúc nhau; các nhãn "Thao tác CRUD", "Yêu cầu xuất / nhập file", "Tìm kiếm" bị dồn ứ sát sạt giữa 2 tầng.
> - **Hình 3.4 (Cấu trúc RAM):** Nửa bên trái dồn cục các node, nửa bên phải để trống hoác; chữ lọt thỏm giữa khoảng không gian thừa mứa.
> - **Nhầm lẫn tài liệu:** File ảnh trong Word (`image3.png`) bị tráo lộn sang hình khác; caption một đằng nhưng hình vẽ một nẻo.

### Quy tắc bất biến:
1. **CẤM tuyên bố hoàn thành / `[PASS]`** nếu Agent chưa thực hiện cả 4 Gate độc lập (A, B, C, D).
2. **Soi trực quan bằng mắt (Visual Inspection):** Sau khi render, Agent phải thực sự mở ảnh để đánh giá bố cục tổng thể, khoảng cách thở và độ thông thoáng của nét chữ.
3. **Nếu có bất kỳ điểm nghẽn thị giác hoặc sai lệch ngữ nghĩa nào**, trạng thái phải là **`FAIL`** hoặc **`PASS WITH CONDITIONS`**, tuyệt đối không được báo `PASS` hoàn hảo!

---

## 2. BẢNG PHÂN ĐỊNH RANH GIỚI KIỂM ĐỊNH (AUDIT SCOPE & LIMITATIONS)

| Tiêu chí kiểm tra | Script tự động `audit-diagrams.mjs` | Agent soi mắt & đối chiếu thực tế |
| :--- | :---: | :---: |
| Banner cảnh báo compiler (`Please use...`, `Warning`, `Syntax`) | **Kiểm tra được 100%** | Xác nhận lại |
| Cú pháp thẻ SVG hợp lệ, kích thước file > 500B | **Kiểm tra được 100%** | Không cần |
| Tồn tại đồng thời cặp SVG vector và PNG raster 300DPI | **Kiểm tra được 100%** | Xác nhận kích thước in ấn |
| Chống nhúng từ khóa `title` bên trong canvas ảnh | **Kiểm tra được 100%** | Kiểm tra caption bên ngoài |
| Chữ đè chữ toạ độ thô & Đường nối xẻ ngang chữ ngắn | **Kiểm tra được 100%** | Soi các cụm chữ phức tạp |
| Cấm viết text label lên đường Crow's foot trong ERD | **Kiểm tra được 100%** | Kiểm tra đúng thực thể |
| **Mật độ nhãn chen chúc giữa các tầng kiến trúc** | Cảnh báo dải Y hẹp | **BẮT BUỘC Agent đánh giá** |
| **Sự cân đối khoảng trắng (Whitespace balance)** | Cảnh báo aspect ratio cực đoan | **BẮT BUỘC Agent đánh giá** |
| **Tính đúng đắn ngữ nghĩa (Đúng code, đúng schema DB)** | *Không kiểm tra được* | **BẮT BUỘC Agent đối chiếu** |
| **Khớp hình ảnh với Caption trong Word DOCX** | *Không kiểm tra được* | **BẮT BUỘC Agent đối chiếu** |
| **Bố cục in ấn trang Word A4 (Chống rớt trang, rớt caption)** | *Không kiểm tra được* | **BẮT BUỘC Agent đối chiếu** |

---

## 3. QUY TRÌNH 4 CỔNG KIỂM ĐỊNH (THE 4-GATE VERIFICATION)

Mọi sơ đồ kỹ thuật phải vượt qua 4 cổng độc lập trước khi nghiệm thu:

### Gate A: Semantic Correctness (Đúng đắn ngữ nghĩa & Nguồn sự thật)
- Đối chiếu 100% với schema CSDL, mã nguồn thật hoặc thuật toán thực tế.
- Đúng tên bảng/class, đúng khóa PK/FK, đúng quan hệ 1-N / N-N, đúng chiều mũi tên phụ thuộc.
- Không tự bịa thêm service ảo, bảng ảo, hoặc quan hệ không có trong codebase.
- Với BK-Tree: Nhãn cạnh **bắt buộc là khoảng cách Levenshtein toán học chính xác**, không tự bịa số để làm đẹp hình.

### Gate B: Toolchain & Rendering (Biên dịch sạch sẽ & Đủ định dạng)
- Mã nguồn cú pháp sạch: `@startuml...@enduml` hoặc `digraph {...}`.
- Không chứa banner cảnh báo compiler (`handwritten`, `deprecation`, `please use`).
- Xuất đồng thời cả `.svg` (vector nét vô hạn) và `.png` (raster 300 DPI siêu nét).
- Giữ nguyên vẹn 100% dấu tiếng Việt Unicode (Segoe UI / Arial).

### Gate C: Visual QA (Soi mắt bố cục & Chống chen chúc)
- **Zero-Title in Canvas:** Không nhúng `title` vào ảnh; tiêu đề chỉ nằm ở Caption tài liệu.
- **Quy tắc liên tầng (Inter-tier Anti-Crowding):**
  - Trong sơ đồ kiến trúc 3 lớp / phân tầng: **CẤM vẽ hàng loạt mũi tên kèm danh sách thao tác CRUD, Tìm kiếm, Import/Export** chen chúc nhau giữa 2 tầng.
  - Sơ đồ kiến trúc chỉ thể hiện khối thành phần và mũi tên phụ thuộc tổng quan (`Yêu cầu nghiệp vụ` hoặc `Dependency call`).
  - Chi tiết từng thao tác CRUD / Search / Export **BẮT BUỘC chuyển sang Sơ đồ Tuần tự (Sequence) hoặc Hoạt động (Activity) riêng**.
- **Cân đối khoảng trắng (Whitespace Balance):**
  - Tỷ lệ khung hình chuẩn từ 4:3 đến 16:9 (hoặc 1:1), không dẹt lép (> 3.8) hoặc dài ngoằng (< 0.28).
  - Không để các nút dồn cục về một góc trong khi góc đối diện trống trơn.
  - Khoảng cách phân tách tối thiểu: `nodesep 70`, `ranksep 70`, đường nối vuông góc `linetype ortho`.

### Gate D: Document QA (Tích hợp tài liệu Word DOCX an toàn)
- **Caption - Image Exact Match:** File ảnh chèn vào vị trí `Hình X.Y` phải khớp chính xác với nội dung Caption và mô tả trong văn bản. Tuyệt đối không swap nhầm `imageX.png`!
- **Đoạn văn dẫn dắt (Leading Paragraph):** Ngay trước hình phải có văn bản dẫn nhập (*"Như được mô tả tại Hình X.Y..."*). Không để sơ đồ đứng trơ trọi giữa 2 tiêu đề mục.
- **Khóa trang chống rớt Caption (`keep_with_next`):** Đoạn văn chứa ảnh hoặc caption phải được bật cờ `keep_with_next` trong Word OpenXML để hình và chú thích không bao giờ bị tách rời sang 2 trang khác nhau.
- **Kích thước chuẩn in ấn A4:** Chiều rộng ảnh trong Word căn giữa từ 14.0 cm đến 15.5 cm (vừa vặn lề trang 2.0 - 2.5 cm).

---

## 4. BỐN TRẠNG THÁI NGHIỆM THU (VERDICT STATES)

Mỗi lần báo cáo kết quả audit sơ đồ, Agent chỉ được sử dụng 1 trong 4 trạng thái sau:

1. **`[PASS]`**: Đạt hoàn hảo cả 4 cổng (Gate A, B, C, D) với đầy đủ bằng chứng cụ thể.
2. **`[PASS WITH CONDITIONS]`**: Về mặt kỹ thuật và thị giác đạt yêu cầu, nhưng có ghi chú về phạm vi mô hình hóa (được nêu rõ trong báo cáo).
3. **`[BLOCKED]`**: Thiếu schema/mã nguồn gốc, hoặc thiếu công cụ render môi trường (Graphviz/Java/Node), phải dừng lại báo cáo lý do.
4. **`[FAIL]`**: Phát hiện lỗi bố cục (đè chữ, dồn cục, mất cân đối, banner compiler) hoặc sai lệch ngữ nghĩa (bịa class/bảng), bắt buộc phải sửa mã nguồn và render lại!

---

## 5. BÀN GIAO TRỰC QUAN SẠCH — CẤM XẢ MÃ NGUỒN (ZERO CODE DUMPS)

> [!IMPORTANT]
> **QUY TẮC BÀN GIAO BẤT BIẾN:**
> - File mã nguồn (`.puml`, `.dot`, `.tldr`) **chỉ được lưu trên ổ đĩa**, tuyệt đối **KHÔNG in khối code nguồn** ra câu trả lời chat làm tràn màn hình.
> - Phản hồi bàn giao **BẮT BUỘC CHỈ GỒM**:
>   1. **Ảnh sơ đồ trực quan (Rendered Preview):** `![Hình X.Y: Tên sơ đồ](path/to/diagram.png)`
>   2. **Tiêu đề sơ đồ chuẩn:** `*Hình X.Y: Tên sơ đồ*`
>   3. **Bảng tóm tắt kiểm định 4 Gate:** Báo cáo chi tiết trạng thái Gate A, B, C, D.
>   4. **Đường dẫn tệp nguồn (Link Markdown ngắn gọn):** `[Mã nguồn .puml](file:///path/to/diagram.puml)`.

### Mẫu trình bày bàn giao chuẩn:

```markdown
### Kết quả kiểm định sơ đồ: [PASS]

![Hình 3.1: Kiến trúc phân tầng hệ thống](assets/diagrams/01_architecture.png)
*Hình 3.1: Kiến trúc phân tầng hệ thống (3-Tier Architecture)*

- **Gate A (Ngữ nghĩa):** [PASS] Khớp 100% các Controller, Service và Repository trong mã nguồn backend.
- **Gate B (Render & Toolchain):** [PASS] Xuất đủ SVG vector và PNG 300 DPI, không có banner cảnh báo compiler.
- **Gate C (Visual QA):** [PASS] Bố cục 3 tầng thông thoáng, chỉ giữ mũi tên phụ thuộc chính, chi tiết CRUD đã đưa sang Sơ đồ Tuần tự Hình 3.2.
- **Gate D (Tích hợp DOCX):** [PASS] Chiều rộng 15.0cm căn giữa, đã gán `keep_with_next` chống rớt caption, có đoạn văn dẫn nhập.
- **Tệp nguồn:** [01_architecture.puml](file:///E:/HOC%20TAP/my-project/sp-agent/assets/diagrams/01_architecture.puml) (đã lưu an toàn trên đĩa).
```

---

## 6. TOOLCHAIN KIỂM ĐỊNH TỰ ĐỘNG

Chạy script kiểm định tích hợp:

```bash
# Kiểm tra toàn bộ thư mục export sơ đồ
node .claude/skills/diagram-auditor/scripts/audit-diagrams.mjs <duong-dan-thu-muc>
```

Script sẽ tự động quét:
1. Phát hiện chuỗi cảnh báo ngầm (`Please use`, `Warning`, `handwritten`, `Syntax`).
2. Kiểm tra tính hợp lệ của thẻ SVG và kích thước file (> 500B).
3. Kiểm tra sự tồn tại đồng thời của file PNG 300 DPI tương ứng.
4. Kiểm tra từ khóa `title` nhúng trong file mã nguồn.
5. Cảnh báo nhãn đè lên đường Crow's foot trong ERD.
6. Kiểm tra va chạm tọa độ chữ thô (dx < 25, dy < 12).
7. Cảnh báo mật độ nhãn dày đặc theo dải ngang giữa các tầng.
8. Kiểm tra đường kẻ cắt ngang mặt chữ.
9. Cảnh báo tỷ lệ khung hình bất thường (quá dẹt hoặc quá dài).
