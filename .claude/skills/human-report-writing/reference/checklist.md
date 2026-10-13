# Human Report Writing — Reference Checklist & Guidelines

Chi tiết hỗ trợ cho skill `human-report-writing`. Đọc khi cần checklist đầy đủ, nguyên tắc nhịp điệu và ví dụ đối chiếu.

---

## 1. Checklist "Đọc tự nhiên như Kỹ sư thực chiến" (Đầy đủ)

### A. Nội dung, Lập luận & Chiều sâu Kỹ thuật
- [ ] **Có lý do đánh đổi (Trade-offs):** Giải thích tại sao chọn công nghệ/kiến trúc này thay vì phương án khác.
- [ ] **Có trở ngại thực tế (Friction):** Nêu lỗi phát sinh, nút thắt cổ chai hoặc bài toán kiểm thử cụ thể thay vì chỉ vẽ bức tranh hoàn hảo.
- [ ] **Cơ chế thay vì tính từ:** Dùng thông số, cấu hình, giải thuật, tên bảng thay vì tính từ "an toàn", "nhanh chóng", "tối ưu".
- [ ] **Không chép rác giáo trình:** Bỏ các định nghĩa vỡ lòng (Docker là gì, React là gì); tập trung vào việc áp dụng trong dự án.
- [ ] **Lập luận có chuỗi nhân quả:** Vấn đề nghiệp vụ → Giải pháp kỹ thuật → Dữ liệu thực nghiệm chứng minh.
- [ ] **Mỗi chương kết thúc bằng "Tóm tắt chương" 2–3 câu** nêu đọng lại các kết luận kỹ thuật chính; đầu chương có thể có câu dẫn.

### B. Nhịp điệu câu & Cấu trúc đoạn (Cadence & Burstiness)
- [ ] **Độ dài câu biến thiên linh hoạt:** Đan xen câu ngắn (4–8 từ), câu trung bình (12–20 từ), câu phân tích phức (25–35 từ). Tuyệt đối không để câu nào cũng ~20 từ.
- [ ] **Chủ động và có chủ thể:** Hạn chế bị động vô căn cứ ("được thực hiện bởi"); nêu rõ chủ thể hành động hoặc thực thể hệ thống.
- [ ] **Móc xích tự nhiên:** Không mở đầu hàng loạt câu bằng "Bên cạnh đó", "Ngoài ra", "Hơn nữa", "Đồng thời".
- [ ] **Phá bỏ khuôn mẫu 3 thì:** Không viết mọi tiểu mục theo công thức cơ học: [Giới thiệu] → [Liệt kê] → [Tự khen].

### C. Từ vựng & Dấu hiệu máy móc
- [ ] **Không từ sáo rỗng trong Fluff Blacklist:** Loại bỏ "đóng vai trò quan trọng", "tối ưu hóa quy trình", "mang tính toàn diện", "hệ sinh thái", "nâng cao trải nghiệm"...
- [ ] **Bỏ câu rào đón:** "có thể nói rằng", "nhìn chung", "cần được lưu ý rằng"...
- [ ] **Bỏ câu hướng dẫn nội bộ:** "trước khi nộp...", "khi nộp bài cần...", "số liệu mô phỏng cần ghi rõ...". Chuyển thành câu khẳng định hoặc xóa bỏ.
- [ ] **Không khuôn câu nào lặp quá ~3 lần:** "điều này cho thấy", "cần được", "không chỉ... mà còn...".

### D. Định dạng bất biến
- [ ] **Không có chữ in đậm (bold) trong thân bài.** Chỉ dùng Heading style cho tiêu đề.
- [ ] **Không có dấu gạch dài em dash (—).**
- [ ] **Không có highlight màu hay nền vàng.**
- [ ] **Hạn chế gạch đầu dòng:** Ưu tiên văn xuôi; chỉ dùng bullet khi liệt kê thật sự.

---

## 2. Các ví dụ Before → After theo chuyên đề kỹ thuật

### Ví dụ 1: Kiến trúc Caching & Database
- **Before (AI sáo rỗng):**
  > "Hệ thống áp dụng công nghệ caching tiên tiến với Redis nhằm tối ưu hóa hiệu năng truy vấn và đem lại trải nghiệm liền mạch cho người dùng. Bên cạnh đó, cơ sở dữ liệu PostgreSQL cũng đóng vai trò quan trọng trong việc đảm bảo tính toàn vẹn dữ liệu."
- **AI sửa vội (Cứng đơ hành chính):**
  > "Hệ thống dùng Redis để lưu dữ liệu tạm và dùng PostgreSQL để lưu dữ liệu chính. Việc này được thực hiện nhằm mục đích giúp hệ thống chạy nhanh hơn và dữ liệu không bị mất."
- **After (Kỹ sư thực chiến):**
  > "Nhóm đặt một lớp đệm Redis phía trước PostgreSQL với thời gian sống (TTL) 5 phút cho danh mục sản phẩm. Cơ chế này đạt tỷ lệ cache hit 88%, giúp giảm lượng truy vấn đọc trực tiếp vào cơ sở dữ liệu từ 1.200 xuống còn 140 query mỗi phút trong giờ cao điểm."

---

### Ví dụ 2: Cơ chế Xác thực & Phân quyền
- **Before (AI sáo rỗng):**
  > "Module xác thực không chỉ đảm bảo an toàn tuyệt đối cho thông tin tài khoản mà còn cung cấp khả năng phân quyền mạnh mẽ, linh hoạt, đáp ứng toàn diện nhu cầu của hệ thống."
- **AI sửa vội (Cứng đơ hành chính):**
  > "Module xác thực thực hiện việc kiểm tra thông tin đăng nhập và phân quyền người dùng theo quy định. Các quyền được chia thành các nhóm khác nhau."
- **After (Kỹ sư thực chiến):**
  > "Module xác thực chia người dùng thành ba vai trò: Quản trị viên, Nhân viên kho và Khách hàng. Token JWT gắn kèm danh sách quyền tương ứng, cho phép API gateway chặn truy cập trái phép ngay tại cửa vào mà không cần gọi lại cơ sở dữ liệu."

---

### Ví dụ 3: Xử lý Bất đồng bộ & Hàng đợi
- **Before (AI sáo rỗng):**
  > "Hệ thống tích hợp hàng đợi thông điệp để xử lý các tác vụ ngầm một cách hiệu quả, giúp nâng cao tính ổn định và khả năng mở rộng của toàn bộ nền tảng."
- **AI sửa vội (Cứng đơ hành chính):**
  > "Các tác vụ nặng được gửi vào hàng đợi RabbitMQ. Quá trình xử lý sau đó được thực hiện bởi các worker chạy ngầm."
- **After (Kỹ sư thực chiến):**
  > "Xử lý đồng bộ gửi email kích hoạt trực tiếp trong luồng đăng ký khiến thời gian phản hồi API kéo dài hơn 2,5 giây mỗi khi máy chủ SMTP chậm. Nhóm chuyển toàn bộ việc gửi email sang hàng đợi RabbitMQ. Máy chủ xác thực trả kết quả thành công cho người dùng trong 85 mili-giây, trong khi worker chạy ngầm xử lý hàng đợi với cơ chế tự động thử lại tối đa 3 lần."

---

## 3. Cấu trúc & Hình thức báo cáo chuẩn (Tham chiếu các trường ĐH)

- **Bố cục:** Trang bìa → Lời cảm ơn → Tóm tắt (100–300 từ) → Mục lục → Danh mục bảng/hình → Nội dung chính (Mở đầu, Tổng quan, Phân tích/Thiết kế, Triển khai & Đánh giá, Kết luận) → Tài liệu tham khảo → Phụ lục.
- **Quy chuẩn hiển thị:** Times New Roman cỡ 13, giãn dòng 1.3–1.5; lề trái 3–3.5 cm, lề phải 2 cm, trên/dưới 2–2.5 cm.
- **Tiêu đề & Đánh số:** Tối đa 4 cấp (Chương 1, 1.1, 1.1.1, 1.1.1.1); mỗi nhóm tiểu mục phải có từ 2 mục trở lên.
- **Bảng & Hình:** Tên bảng đặt phía trên (`Bảng X.Y`), tên hình đặt phía dưới (`Hình X.Y`). Phải có câu tham chiếu rõ ràng trong bài ("xem Hình 3.2"), không dùng "hình dưới đây".

---

## 4. Phân công vai trò giữa các Skill

- **`human-report-writing`:** Văn phong, nhịp điệu, tư duy kỹ sư thực tế, loại bỏ AI slop và tính khô cứng hành chính.
- **`docx-report`:** Dựng cấu trúc OOXML/python-docx, heading styles, captions, cross-references, TOC, visual render QA.
- **`plantuml-diagrams`:** Vẽ sơ đồ UML, ERD, Sequence, Flowchart, Use Case chuẩn kỹ thuật (trắng-đen học thuật).
- **`research-report`:** Thu thập, kiểm chứng số liệu và nguồn trích dẫn đáng tin cậy.
