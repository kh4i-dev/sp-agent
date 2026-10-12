---
name: diagram-auditor
description: Audit và kiểm định chất lượng sơ đồ kỹ thuật (PlantUML, Graphviz DOT, tldraw, SVG, PNG) trước khi gửi cho người dùng hoặc chèn vào báo cáo Word (docx-report). Ngăn chặn dứt điểm hội chứng False PASS (script chạy 0 lỗi nhưng nhìn bằng mắt vẫn méo mó, đè nhãn, dồn cục). Bắt buộc thực hiện Visual QA bằng cách đưa ảnh PNG trực tiếp vào ngữ cảnh model để soi mắt thực tế. Báo cáo độc lập 5 kết quả kiểm chứng (Render validation, Automated audit, Actual visual inspection, Semantic correctness, DOCX rendered-page inspection), cấm gộp thành một chữ PASS chung chung.
---

# Diagram Auditor Skill — Cổng Kiểm Định Chất Lượng Sơ Đồ & Visual QA Thực Tế

Mục tiêu: Đảm bảo **100% sơ đồ xuất bản** đạt chuẩn kỹ thuật và thẩm mỹ in ấn học thuật cao cấp. Chặn đứng tận gốc tình trạng **"Script báo PASS nhưng mắt nhìn thấy FAIL"** — tức là file render được không lỗi cú pháp nhưng bố cục chật chội, nhãn đè nhau, khoảng trắng bất hợp lý, hoặc nhầm lẫn hình ảnh trong tài liệu.

---

## 1. HỌC THUYẾT KIỂM ĐỊNH ĐỘC LẬP: HARD ACCEPTANCE GATE — NO SELF-CERTIFIED PASS

> [!CAUTION]
> **5 NGUYÊN NHÂN GỐC KHIẾN AGENT BỊ "FALSE PASS" (BÁO ẢO):**
> 1. **Nhầm lệnh chạy thành công với sản phẩm đạt yêu cầu:** Tạo `.puml` chạy renderer thành công và auditor báo 0 lỗi, nhưng kết quả ấy không chứng minh sơ đồ đúng kiến trúc hay dễ đọc khi in.
> 2. **Sửa hình nhưng chưa kiểm tra mô hình bên dưới:** Ví dụ trong sơ đồ kiến trúc 3 lớp, file có đường `UI_Main --> Store` nhảy cóc qua `Engine` (Tầng nghiệp vụ). Đây là mâu thuẫn kiến trúc nghiêm trọng nhưng agent chỉ lo vẽ đẹp mũi tên mà không sửa mô hình logic! Chưa làm rõ đang mô tả kiến trúc hiện tại (As-Is) hay mục tiêu (To-Be).
> 3. **"Mở ảnh" chưa chắc là "đã xem ảnh":** Chạy `Start-Process`, `os.startfile()` hay đọc metadata chỉ mở file trên máy tính hoặc lấy kích thước bytes. Chúng không đưa pixel vào thị giác của model.
> 4. **Công cụ audit tự động kiểm tra thiếu tiêu chí:** Script chỉ phát hiện toạ độ thô hoặc SVG hợp lệ, bỏ sót mật độ nhãn dày đặc, mũi tên gây hiểu nhầm, hoặc sai lệch quan hệ.
> 5. **Agent tự sinh rồi tự tuyên bố đạt:** Cùng một agent vừa vẽ, vừa quyết định thế nào là đẹp, vừa khen mình làm tốt. Cần cơ chế kiểm định độc lập (Adversarial Review) với quyền bác bỏ (`REJECT`).

### Nguyên tắc chỉ thị cốt lõi (Hard Acceptance Gate):
- Mục tiêu của nhiệm vụ là **chất lượng đã được kiểm chứng của sản phẩm cuối cùng**, KHÔNG PHẢI là việc thực thi thành công các lệnh render hay exit code 0 của script.
- Bắt buộc kiểm tra 5 cổng độc lập có bằng chứng. Một lệnh thành công, một file SVG hợp lệ hay lời tự nhận của agent tạo sơ đồ **KHÔNG PHẢI là bằng chứng hoàn thành**.
- **Quyền Bác Bỏ (Right to Reject):** Lượt kiểm định (Reviewer) phải chủ động tìm lỗi để bác bỏ sản phẩm chưa đạt. Không tối ưu hóa số lượng kết quả PASS; tối ưu hóa tính đúng đắn và độ tin cậy của sản phẩm bàn giao!
- **4 Trạng thái nghiệm thu bắt buộc:**
  - `PASS`: Tất cả các cổng bắt buộc đều có bằng chứng hỗ trợ rõ ràng.
  - `PASS WITH CONDITIONS`: Còn một số giới hạn nhưng được ghi nhận rõ ràng và được dự án chấp thuận.
  - `FAIL`: Còn tồn tại lỗi cụ thể chưa được khắc phục.
  - `BLOCKED`: Một kiểm tra bắt buộc không thể thực hiện được (ví dụ thiếu tool xem ảnh, thiếu schema).

---

## 2. QUY CHUẨN BẮT BUỘC: VISUAL QA — IMAGE MUST ACTUALLY BE VIEWED

Sau khi render mỗi sơ đồ, Agent **BẮT BUỘC** thực hiện quy trình kiểm tra thị giác nghiêm ngặt sau:

1. **Xác minh file vật lý:** File PNG tồn tại trên đĩa, dung lượng > 0 bytes và mở được bình thường.
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
4. **Semantic correctness:** Đối chiếu 100% với schema CSDL, mã nguồn thật hoặc kiến trúc quy chuẩn (không vi phạm nhảy cóc tầng như `UI -> Store`, đúng tên bảng/class, đúng khóa PK/FK, đúng khoảng cách Levenshtein toán học trên cạnh BK-Tree).
5. **DOCX rendered-page inspection:** Đã kiểm tra trực quan trang văn bản sau khi chèn hình (chiều rộng 14–15.5 cm căn giữa, khớp 100% hình với Caption `Hình X.Y`, có câu văn dẫn dắt, có thuộc tính `keep_with_next` chống rớt caption sang trang sau).

---

## 5. CỔNG NGƯỜI DÙNG NGHIỆM THU — HỎI TRƯỚC KHI THAY VÀO DOCX

> [!IMPORTANT]
> **QUY TẮC CHỜ NGƯỜI DÙNG DUYỆT (USER ACCEPTANCE CHECKPOINT):**
> Sau khi tạo ảnh và báo cáo kiểm định 5 cổng, Agent **DỪNG LẠI**, tuyệt đối **KHÔNG TỰ Ý GHI ĐÈ/SWAP ẢNH VÀO FILE WORD** nếu chưa có sự xác nhận của người dùng!
> 
> Agent phải hiển thị ảnh trực quan và hỏi người dùng câu hỏi nghiệm thu chuẩn:
> *"Tôi đã hoàn thành bản vẽ và kiểm định 5 cổng phía trên. Bạn kiểm tra trực quan giúp tôi: Ảnh đã đạt yêu cầu để thay thế luôn vào tài liệu Word chưa, hay cần sửa đổi/tinh chỉnh ảnh nào? Vui lòng phản hồi để tôi tiến hành bước tiếp theo!"*

---

## 6. BÀN GIAO TRỰC QUAN SẠCH — CẤM XẢ MÃ NGUỒN (ZERO CODE DUMPS)

- File mã nguồn (`.puml`, `.dot`, `.tldr`) **chỉ được lưu trên ổ đĩa**, tuyệt đối **KHÔNG in khối code nguồn** ra câu trả lời chat làm tràn màn hình.
- Phản hồi bàn giao **BẮT BUỘC CHỈ GỒM**:
  1. **Ảnh sơ đồ trực quan (Rendered Preview):** `![Hình X.Y: Tên sơ đồ](path/to/diagram.png)`.
  2. **Tiêu đề sơ đồ chuẩn:** `*Hình X.Y: Tên sơ đồ*`.
  3. **Báo cáo chi tiết 5 kết quả kiểm chứng độc lập** (không gộp tắt).
  4. **Câu hỏi xin ý kiến nghiệm thu người dùng** (theo Mục 5).
  5. **Đường dẫn tệp nguồn (Link Markdown ngắn gọn):** `[Mã nguồn .puml](file:///path/to/diagram.puml)`.

---

## 7. TOOLCHAIN KIỂM ĐỊNH TỰ ĐỘNG

Chạy script kiểm định tích hợp:

```bash
# Kiểm tra toàn bộ thư mục export sơ đồ
node .claude/skills/diagram-auditor/scripts/audit-diagrams.mjs <duong-dan-thu-muc>
```
