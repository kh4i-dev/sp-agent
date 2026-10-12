---
name: diagram-auditor
description: Audit và kiểm định chất lượng sơ đồ kỹ thuật (PlantUML, Graphviz DOT, tldraw, SVG, PNG) trước khi gửi cho người dùng hoặc chèn vào báo cáo Word (docx-report). Ngăn chặn dứt điểm hội chứng False PASS (script chạy 0 lỗi nhưng nhìn bằng mắt vẫn méo mó, đè nhãn, dồn cục). Bắt buộc thực hiện Visual QA bằng cách đưa ảnh PNG trực tiếp vào ngữ cảnh model để soi mắt thực tế. Báo cáo độc lập 5 kết quả kiểm chứng (Render validation, Automated audit, Actual visual inspection, Semantic correctness, DOCX rendered-page inspection), cấm gộp thành một chữ PASS chung chung.
---

# Diagram Auditor Skill — Cổng Kiểm Định Chất Lượng Sơ Đồ & Visual QA Thực Tế

Mục tiêu: Đảm bảo **100% sơ đồ xuất bản** đạt chuẩn kỹ thuật và thẩm mỹ in ấn học thuật cao cấp. Chặn đứng tận gốc tình trạng **"Script báo PASS nhưng mắt nhìn thấy FAIL"** — tức là file render được không lỗi cú pháp nhưng bố cục chật chội, nhãn đè nhau, khoảng trắng bất hợp lý, hoặc nhầm lẫn hình ảnh trong tài liệu.

---

## 1. NGUYÊN TẮC CỐT LÕI: HỘI CHỨNG BÁO ẢO & THE ANTI-FALSE-PASS DOCTRINE

> [!CAUTION]
> **HỘI CHỨNG BÁO ẢO (FALSE PASS SYNDROME):**
> Script tự động (`audit-diagrams.mjs`) trả về exit code `0` chỉ là **ĐIỀU KIỆN CẦN (Kiểm tra hình học thô)**, **TUYỆT ĐỐI KHÔNG PHẢI ĐIỀU KIỆN ĐỦ**.
> Một sơ đồ vượt qua script vẫn có thể hoàn toàn **FAIL** về mặt thị giác và ngữ nghĩa:
> - **Hình 3.1 (Kiến trúc 3 lớp):** Nhiều mũi tên từ UI về Business Logic chen chúc nhau; các nhãn "Thao tác CRUD", "Yêu cầu xuất / nhập file", "Tìm kiếm" bị dồn ứ sát sạt giữa 2 tầng.
> - **Hình 3.4 (Cấu trúc RAM):** Nửa bên trái dồn cục các node, nửa bên phải để trống hoác; chữ lọt thỏm giữa khoảng không gian thừa mứa.
> - **Nhầm lẫn tài liệu:** File ảnh trong Word (`image3.png`) bị tráo lộn sang hình khác; caption một đằng nhưng hình vẽ một nẻo.

---

## 2. QUY CHUẨN BẮT BUỘC: VISUAL QA — IMAGE MUST ACTUALLY BE VIEWED

Sau khi render mỗi sơ đồ, Agent **BẮT BUỘC** thực hiện quy trình kiểm tra thị giác nghiêm ngặt sau:

1. **Xác minh tính hợp lệ vật lý:** File PNG tồn tại trên đĩa, dung lượng > 0 bytes và mở được bình thường.
2. **Đưa ảnh trực tiếp vào ngữ cảnh model:** Dùng công cụ xem ảnh có khả năng đưa nội dung hình ảnh vào ngữ cảnh của model (như `view_file` trên tệp `.png`) để trực tiếp kiểm tra hình ảnh thực tế.
3. **CẤM giả định việc xem ảnh:** Tuyệt đối **KHÔNG** được coi các thao tác sau là bằng chứng đã trực tiếp kiểm tra hình ảnh:
   - Chạy lệnh hệ thống `os.startfile()` hoặc `Start-Process`.
   - Đọc kích thước file trên đĩa (bytes / KB).
   - Phân tích metadata ảnh (width, height, DPI).
   - Đọc mã nguồn `.puml`, `.dot` hoặc tệp SVG dạng text.
4. **Kiểm tra riêng từng sơ đồ:** Mở riêng từng hình ở kích thước đủ lớn để soi chi tiết. Nếu có nhiều sơ đồ, có thể dùng contact sheet để có cái nhìn tổng quan, nhưng vẫn bắt buộc phải mở từng hình để kiểm tra chi tiết từng thành phần.
5. **Danh mục lỗi bắt buộc phải soi và ghi nhận cụ thể:**
   - Chữ đè lên chữ, text đè lên đường kẻ.
   - Nhãn không gắn đúng vào đường nối tương ứng (lơ lửng, lệch vị trí).
   - Mũi tên sai hướng logic hoặc đi chéo ngang mặt khối khác.
   - Đường nối cắt xuyên qua khung hoặc cắt qua nội dung của box.
   - Cỡ chữ quá nhỏ so với tỷ lệ chung, không đọc được khi in ra A4.
   - Khoảng trắng bất hợp lý (lệch dồn cục sang một bên, để trống hoác bên còn lại).
   - Luồng nghiệp vụ rối rắm, khó hiểu cho người đọc.
6. **Vòng lặp sửa lỗi có kiểm chứng:** Chỉ sửa sau khi đã xác định chính xác lỗi; sau khi sửa mã nguồn bắt buộc phải render lại và **mở xem ảnh mới** để xác nhận lỗi đã biến mất.
7. **Xử lý khi thiếu công cụ xem ảnh:** Nếu môi trường thiếu công cụ xem ảnh đưa được pixel vào ngữ cảnh model, Agent phải dừng lại và báo:
   `BLOCKED — Visual QA unavailable`. Tuyệt đối không được đoán mò kết quả dựa trên output của renderer hay script auditor!

---

## 3. BẢNG PHÂN ĐỊNH RANH GIỚI KIỂM ĐỊNH (AUDIT SCOPE & LIMITATIONS)

| Tiêu chí kiểm tra | Script tự động `audit-diagrams.mjs` | Agent soi mắt & đối chiếu thực tế |
| :--- | :---: | :---: |
| Banner cảnh báo compiler (`Please use...`, `Warning`, `Syntax`) | **Kiểm tra được 100%** | Xác nhận lại |
| Cú pháp thẻ SVG hợp lệ, kích thước file > 500B | **Kiểm tra được 100%** | Không cần |
| Tồn tại đồng thời cặp SVG vector và PNG raster 300DPI | **Kiểm tra được 100%** | Xác nhận kích thước in ấn |
| Chống nhúng từ khóa `title` bên trong canvas ảnh | **Kiểm tra được 100%** | Kiểm tra caption bên ngoài |
| Chữ đè chữ toạ độ thô & Đường nối xẻ ngang chữ ngắn | **Kiểm tra được 100%** | Soi các cụm chữ phức tạp |
| Cấm viết text label lên đường Crow's foot trong ERD | **Kiểm tra được 100%** | Kiểm tra đúng thực thể |
| **Mật độ nhãn chen chúc giữa các tầng kiến trúc** | Cảnh báo dải Y hẹp | **BẮT BUỘC Agent soi mắt** |
| **Sự cân đối khoảng trắng (Whitespace balance)** | Cảnh báo aspect ratio cực đoan | **BẮT BUỘC Agent soi mắt** |
| **Tính đúng đắn ngữ nghĩa (Đúng code, đúng schema DB)** | *Không kiểm tra được* | **BẮT BUỘC Agent đối chiếu** |
| **Khớp hình ảnh với Caption trong Word DOCX** | *Không kiểm tra được* | **BẮT BUỘC Agent đối chiếu** |
| **Bố cục in ấn trang Word A4 (Chống rớt trang, rớt caption)** | *Không kiểm tra được* | **BẮT BUỘC Agent đối chiếu** |

---

## 4. BÁO CÁO ĐỘC LẬP 5 KẾT QUẢ KIỂM CHỨNG (SEPARATE 5-POINT VERIFICATION)

> [!IMPORTANT]
> **QUY TẮC BẤT BIẾN:**
> **KHÔNG GỘP NĂM KẾT QUẢ DƯỚI ĐÂY THÀNH MỘT TRẠNG THÁI PASS DUY NHẤT NẾU CÒN BƯỚC CHƯA ĐƯỢC KIỂM CHỨNG.**
> Báo cáo nghiệm thu bắt buộc phải trình bày riêng rẽ từng mục:

1. **Render validation:** File PNG & SVG tồn tại trên đĩa, không rỗng (> 500 bytes), biên dịch sạch sẽ không có banner cảnh báo compiler (`Please use...`, `Warning`).
2. **Automated audit:** Kết quả từ script `audit-diagrams.mjs` (không có va chạm tọa độ chữ, không có đường cắt ngang chữ, không có nhãn trên Crow's foot ERD, tỷ lệ aspect ratio hợp lý).
3. **Actual visual inspection:** Kết quả từ việc Agent trực tiếp mở ảnh PNG bằng công cụ xem ảnh vào ngữ cảnh model (soi nét chữ thông thoáng, không chen chúc nhãn giữa các tầng, bố cục cân đối không lệch dồn cục, luồng rõ ràng).
4. **Semantic correctness:** Đối chiếu 100% với schema CSDL, mã nguồn thật hoặc thuật toán (đúng tên bảng/class, đúng khóa PK/FK, đúng quan hệ 1-N / N-N, đúng khoảng cách Levenshtein toán học trên cạnh BK-Tree).
5. **DOCX rendered-page inspection:** Đã kiểm tra trực quan trang văn bản sau khi chèn hình (chiều rộng 14–15.5 cm căn giữa, khớp 100% hình với Caption `Hình X.Y`, có câu văn dẫn dắt, có thuộc tính `keep_with_next` chống rớt caption sang trang sau).

---

## 5. BÀN GIAO TRỰC QUAN SẠCH — CẤM XẢ MÃ NGUỒN (ZERO CODE DUMPS)

- File mã nguồn (`.puml`, `.dot`, `.tldr`) **chỉ được lưu trên ổ đĩa**, tuyệt đối **KHÔNG in khối code nguồn** ra câu trả lời chat làm tràn màn hình.
- Phản hồi bàn giao **BẮT BUỘC CHỈ GỒM**:
  1. **Ảnh sơ đồ trực quan (Rendered Preview):** `![Hình X.Y: Tên sơ đồ](path/to/diagram.png)`.
  2. **Tiêu đề sơ đồ chuẩn:** `*Hình X.Y: Tên sơ đồ*`.
  3. **Báo cáo chi tiết 5 kết quả kiểm chứng độc lập** (không gộp tắt).
  4. **Đường dẫn tệp nguồn (Link Markdown ngắn gọn):** `[Mã nguồn .puml](file:///path/to/diagram.puml)`.

### Mẫu báo cáo nghiệm thu chuẩn:

```markdown
### Báo cáo kiểm định sơ đồ: Hình 3.1 — Kiến trúc phân tầng hệ thống

![Hình 3.1: Kiến trúc phân tầng hệ thống](assets/diagrams/01_architecture.png)
*Hình 3.1: Kiến trúc phân tầng hệ thống (3-Tier Architecture)*

- **1. Render validation:** [PASS] Đã tạo đủ `01_architecture.svg` và `01_architecture.png` (300 DPI, 185 KB), biên dịch sạch sẽ không banner.
- **2. Automated audit:** [PASS] `audit-diagrams.mjs` báo 0 lỗi, aspect ratio 1.4:1 đạt chuẩn in ấn, không đè toạ độ.
- **3. Actual visual inspection:** [PASS] Đã mở file PNG soi mắt thực tế qua view_file: Các tầng Presentation, Business Logic và Data Access phân cách rõ ràng; các nhãn CRUD chi tiết đã lược bỏ khỏi liên tầng để tránh chen chúc; nét chữ Segoe UI sắc nét, khoảng thở thoáng đãng.
- **4. Semantic correctness:** [PASS] Khớp 100% các Controller, Service và Repository trong mã nguồn backend thực tế của dự án.
- **5. DOCX rendered-page inspection:** [PASS] Ảnh rộng 15.0 cm căn giữa, khớp với caption "Hình 3.1", đoạn văn dẫn dắt nằm ngay trước hình, đã bật `keep_with_next` chống rớt trang.

*Tệp nguồn:* [01_architecture.puml](file:///E:/HOC%20TAP/my-project/sp-agent/assets/diagrams/01_architecture.puml)
```

---

## 6. TOOLCHAIN KIỂM ĐỊNH TỰ ĐỘNG

Chạy script kiểm định tích hợp:

```bash
# Kiểm tra toàn bộ thư mục export sơ đồ
node .claude/skills/diagram-auditor/scripts/audit-diagrams.mjs <duong-dan-thu-muc>
```
