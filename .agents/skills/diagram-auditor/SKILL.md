---
name: diagram-auditor
description: Audit và kiểm tra chất lượng sơ đồ (PlantUML, SVG, PNG) trước khi gửi cho người dùng. Phát hiện và chặn đứng các lỗi: banner cảnh báo ngầm ("Please use...", syntax warning), nét vẽ méo lệch méo mó, đường nối chéo nhau, đè nhãn (label overlap), thiếu file PNG/SVG, mất cân đối bố cục. Kích hoạt khi người dùng yêu cầu "audit ảnh", "kiểm tra sơ đồ", "soi ảnh trước khi gửi", "diagram bị méo", hoặc tự động chạy như một Quality Gate bắt buộc trước khi bàn giao bất kỳ sơ đồ nào.
---

# Diagram Auditor Skill — Cổng Kiểm Định Chất Lượng Sơ Đồ (Quality Gate)

Mục tiêu: Đảm bảo **100% sơ đồ xuất bản** đạt chuẩn thẩm mỹ cao cấp, chuẩn học thuật in ấn, tuyệt đối **không có banner lỗi ngầm, không méo lệch, không đè nhãn, không chéo đường rác mắt**.

---

## 1. 5 TIÊU CHÍ KIỂM ĐỊNH BẮT BUỘC (THE 5-POINT AUDIT GATE)

Mọi sơ đồ trước khi bàn giao cho người dùng **BẮT BUỘC** phải vượt qua 5 cổng kiểm tra sau:

### Cổng 1: Không có Banner Thông báo / Cảnh báo (Zero-Banner Gate)
- **Lỗi thường gặp:** Sử dụng các tính năng thử nghiệm hoặc cú pháp cũ (như `skinparam handwritten true`) khiến PlantUML in đè banner cảnh báo lên ảnh:
  `Please use '!option handwritten true' to enable handwritten`
- **Quy tắc:** Tuyệt đối không dùng `handwritten` trong các sơ đồ học thuật/bảo vệ. Bất kỳ sơ đồ nào chứa text thông báo từ compiler đều bị đánh **FAIL ngay lập tức**.

### Cổng 2: Nét vẽ Ngay ngắn, Không Méo Lệch (Orthogonal / Clean Geometry Gate)
- **Lỗi thường gặp:** Nét vẽ uốn lượn cong queo khiến sơ đồ trông cẩu thả, các hộp class bị méo cạnh, không chuẩn mực cho đồ án tốt nghiệp TNUT hay sách giáo trình.
- **Quy tắc:**
  - Dùng đường nối vuông góc chuẩn mực: `skinparam linetype ortho` hoặc `polyline`.
  - Bo góc nhẹ nhàng hiện đại: `skinparam roundCorner 4` hoặc `6`.
  - Cắt bỏ hoàn toàn nét sketch run rẩy gây cảm giác "méo lệch".

### Cổng 3: Chống Chồng chéo Đường & Đè Nhãn (Zero-Crossing & Label Overlap Gate)
- **Lỗi thường gặp:**
  - Đường nối từ Actor/Class bên trái cắt ngang mặt Class ở giữa để nối tới Class bên phải.
  - Số lượng quan hệ (`0..*`, `1`) đè thẳng lên tên quan hệ (`gửi yêu cầu`, `sở hữu`).
- **Quy tắc:**
  - Thiết kế bố cục **phân tầng rõ ràng (Tiered Layout)** từ Trái sang Phải hoặc Trên xuống Dưới.
  - Các khối liên quan trực tiếp phải đặt cạnh nhau.
  - Tách nhãn quan hệ và nhãn số lượng: nếu chật chội, dùng chú thích ghi chú bên cạnh hoặc chia layout nhiều hàng với liên kết ẩn `-[hidden]->`.

### Cổng 4: Chuẩn mực Đen - Trắng Học thuật (Monochrome Contrast Gate)
- **Quy tắc:**
  - Nền: Trắng tinh khiết `#FFFFFF`.
  - Viền & Chữ: Đen thuần `#000000`.
  - Không bóng đổ lỗi thời (`skinparam shadowing false`).
  - Độ phân giải: 300 DPI (`skinparam dpi 300`), xuất đồng thời cả `.svg` (vector) và `.png` (raster sắc nét).

### Cổng 5: Không Nhúng Tiêu Đề Vào Trong Ảnh (Zero-Title Gate)
- **Lỗi thường gặp:** Viết dòng `title SƠ ĐỒ...` to đùng ở đầu file PlantUML khiến ảnh bị thừa khoảng trống trên cùng và lặp lại tiêu đề khi chèn vào văn bản.
- **Quy tắc:**
  - **TUYỆT ĐỐI KHÔNG** dùng từ khóa `title` trong mã `.puml`.
  - Tiêu đề sơ đồ luôn được quản lý bằng caption văn bản trong tài liệu báo cáo: `Hình 3.1: Sơ đồ thực thể liên kết (ERD)`.
  - Ảnh chỉ chứa các bảng, thực thể và đường nối nghiệp vụ.

### Cổng 6: Tự Soi Ảnh Trước Khi Gửi (Self-Inspection Gate)
- **Quy định bất biến cho Agent:** Sau khi render, Agent **phải tự chạy script audit** và kiểm tra file trước khi báo cáo cho người dùng. Không bao giờ bàn giao sơ đồ mà chưa qua bước kiểm định này!

### Cổng 7: Bàn Giao Trực Quan Sạch — Cấm Xả Mã Nguồn (Clean Visual Delivery Gate)
- **Lỗi gây rối mắt nhất:** Agent in toàn bộ khối mã nguồn (`@startuml ... @enduml` hay mã Graphviz dài cả trang) ra khung chat, khiến màn hình bị rối và người dùng không nhìn thấy được hình ảnh trực quan.
- **Quy tắc bất biến:**
  - File mã nguồn (`.puml`, `.dot`, `.tldr`) **chỉ được lưu trên ổ đĩa**, tuyệt đối **KHÔNG in khối code nguồn** ra câu trả lời chat.
  - Phản hồi bàn giao **BẮT BUỘC CHỈ GỒM**:
    1. **Ảnh sơ đồ trực quan (Rendered Image Preview):** `![Hình X.X: Tên sơ đồ](path/to/diagram.png)`.
    2. **Tiêu đề sơ đồ chuẩn:** `*Hình X.X: Tên sơ đồ*`.
    3. **Bảng tóm tắt kiểm định:** Trạng thái `[PASS]` 100% (không đè chữ, không méo nét, đủ SVG/PNG 300 DPI).
    4. **Đường dẫn tệp nguồn (chỉ dẫn link Markdown, KHÔNG xổ code):** `[Mã nguồn .puml](file:///path/to/diagram.puml)`.

---

## 2. TOOLCHAIN KIỂM ĐỊNH TỰ ĐỘNG

Chạy script kiểm định tích hợp:

```bash
# Kiểm tra toàn bộ thư mục export sơ đồ
node .claude/skills/diagram-auditor/scripts/audit-diagrams.mjs <duong-dan-thu-muc>
```

Script sẽ tự động quét:
1. Phát hiện chuỗi cảnh báo ngầm (`Please use`, `Warning`, `handwritten`, `Syntax`).
2. Kiểm tra tính hợp lệ của thẻ SVG.
3. Kiểm tra sự tồn tại đồng thời của file PNG tương ứng.
4. Báo cáo chi tiết từng file `[PASS]` hoặc `[FAIL]`.

---

## 3. CÔNG THỨC KHẮC PHỤC LỖI KHI BỊ FAIL

| Lỗi phát hiện | Nguyên nhân | Cách khắc phục triệt để |
| :--- | :--- | :--- |
| Banner `Please use '!option...'` | Dùng `skinparam handwritten true` | Bỏ hoàn toàn dòng `handwritten`. Dùng nét thẳng tinh tế chuẩn mực. |
| Đường nối cong vẹo, cắt chéo mặt class | Layout tự do thiếu định hướng | Thêm `skinparam linetype ortho`. Dùng `left to right direction` kết hợp các liên kết ẩn `-[hidden]->` để ép thứ tự. |
| Nhãn đè lên số lượng `0..*` | Tên quan hệ quá dài | Rút ngắn tên quan hệ hoặc đặt tên nhãn ở giữa mũi tên: `A "1" --> "0..*" B : action >`. |
| Thiếu file PNG | Chỉ mới xuất SVG | Chạy `render-puml.mjs` xuất đủ cả SVG và PNG. |

---

## 4. QUY CHUẨN ĐỊNH DẠNG BÀN GIAO CHO NGƯỜI DÙNG (CLEAN PRESENTATION)

Khi bàn giao kết quả tạo sơ đồ hoặc audit sơ đồ, Agent trình bày theo mẫu chuẩn sau:

```markdown
### Kết quả kiểm định sơ đồ: [PASS]

![Hình 3.1: Sơ đồ thực thể liên kết ERD](assets/diagrams/03_erd.png)
*Hình 3.1: Sơ đồ thực thể liên kết (ERD)*

- **Trạng thái Audit:** Đạt 100% tiêu chuẩn Academic Monochrome (không đè nhãn, không cắt nét, đủ SVG & PNG 300 DPI).
- **Tệp nguồn:** [03_erd.puml](file:///E:/HOC%20TAP/my-project/sp-agent/assets/diagrams/03_erd.puml) (đã lưu an toàn trên đĩa).
```

*(Tuyệt đối KHÔNG kèm theo bất kỳ code block PlantUML/DOT nào trong phản hồi bàn giao)*

