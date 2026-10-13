# Ngôn từ caption / tên hình — MỀM HÓA (tránh cụm kỹ thuật cứng)

Caption/hình/bảng và tiêu đề mục nên đọc như **ngôn ngữ nghiệp vụ / trải nghiệm**, không phải
tên loại sơ đồ thuần kỹ thuật. Ưu tiên góc nhìn **vòng đời – hành trình – sự chuyển dịch**.

## 1. Tránh → Ưu tiên (ví dụ)

| Tránh (cứng, kỹ thuật) | Nên dùng (mềm, nghiệp vụ) |
|---|---|
| Biểu đồ máy trạng thái tài khoản / State Machine Diagram | **Vòng đời tài khoản người dùng** |
| (như trên) | Hành trình trạng thái tài khoản · Các giai đoạn của một tài khoản · Dòng chảy trạng thái tài khoản người dùng |
| (như trên) | Sơ đồ luân chuyển trạng thái tài khoản · Tiến trình quản lý tài khoản · Quy trình chuyển đổi trạng thái tài khoản |
| (như trên – bản ngắn cho slide) | Trạng thái tài khoản & Sự chuyển dịch · Sơ đồ vòng đời tài khoản |
| Activity Diagram X | Luồng xử lý X · Tiến trình X · Các bước thực hiện X |
| Sequence Diagram X | Trình tự trao đổi X · Luồng tương tác X |
| ERD / Class Diagram X | Mô hình dữ liệu X · Cấu trúc dữ liệu X |

> Gợi ý chuẩn nhất (ngắn, quen thuộc, bớt cảm giác kỹ thuật): **"Vòng đời tài khoản người dùng"**.

## 2. Chọn câu theo ngữ cảnh

- **Sản phẩm / UX** (mềm, hướng người dùng): *Vòng đời…*, *Hành trình trạng thái…*, *Các giai đoạn của…*, *Dòng chảy trạng thái…*
- **Nghiệp vụ / tài liệu hệ thống** (chuyên nghiệp nhưng nhẹ): *Sơ đồ luân chuyển trạng thái…*, *Tiến trình quản lý…*, *Quy trình chuyển đổi trạng thái…*
- **Ngắn gọn cho slide/báo cáo trực quan**: *Trạng thái … & Sự chuyển dịch*, *Sơ đồ vòng đời …*

## 3. Subtitle (chú thích dưới tiêu đề) — làm mềm tổng thể

Thêm một dòng nhẹ dưới tiêu đề (đặt ở caption hình, không nhồi trong ảnh):

> *"Mô tả cách tài khoản chuyển đổi qua các giai đoạn: Hoạt động, Tạm khóa và Đã đóng."*

## 4. Mềm hóa từ ngữ trạng thái (rất quan trọng)

| Từ cứng | Thay bằng |
|---|---|
| Bị khóa | **Tạm khóa / Gián đoạn** |
| Đã xóa | **Đã đóng / Ngừng kích hoạt** |
| Bị cấm | Hạn chế truy cập |
| Lỗi / Sai | Cần xử lý · Chưa hợp lệ |
| Hủy | Đã hủy · Ngừng |

## 5. Nguyên tắc

- Caption **đọc được cho người ngoài chuyên môn**; tên loại sơ đồ chuẩn (State Machine, Activity…) chỉ nêu khi thật cần (phụ lục/tài liệu kỹ thuật).
- Nhất quán: đã chọn "Tạm khóa" thì dùng thống nhất toàn bài (không lúc "Bị khóa" lúc "Tạm khóa").
- Áp dụng cho: **caption Hình/Bảng**, **tiêu đề mục**, **nhãn trong sơ đồ** (khi vẽ bằng `plantuml-diagrams`/`diagram-orchestrator`), **tiêu đề slide**.
- Không dùng từ hoa mỹ rỗng: mềm nhưng vẫn đúng bản chất nghiệp vụ (nguồn chân lý).
