# Diagram Design Principles — Nguyên Tắc Thiết Kế Sơ Đồ Chuyên Nghiệp

Tài liệu hướng dẫn tư duy thẩm mỹ thị giác và kỹ thuật bố cục hình học cho sơ đồ kỹ thuật trong báo cáo học thuật, slide thuyết trình và tài liệu kiến trúc phần mềm.

---

## 1. Phân Cấp Thị Giác & Trọng Tâm (Visual Hierarchy & Focus)

Mỗi sơ đồ phải có một **điểm vào tự nhiên (Entry Point)** cho mắt người đọc:
1. **Luồng đọc tự nhiên:** Từ Trái sang Phải (Left-to-Right) cho luồng thời gian/nghiệp vụ; Từ Trên xuống Dưới (Top-to-Bottom) cho kiến trúc phân tầng/cấu trúc cây.
2. **Kích thước phản ánh tầm quan trọng:**
   * Khối trung tâm (Core Domain / Gateway): Kích thước lớn hơn hoặc đặt tại trung tâm hình học.
   * Khối phụ / Chi tiết giá trị (Value Objects / Helpers): Kích thước nhỏ hơn hoặc gộp vào bên trong khối cha.
3. **Màu sắc có chủ đích (Academic Monochrome):**
   * Nền trắng `#FFFFFF` tinh khiết.
   * Viền và chữ đen `#000000` (độ tương phản 21:1 tối đa).
   * **CẤM** dùng màu sắc tùy tiện để trang trí. Chỉ dùng màu khi có quy ước ngữ nghĩa cụ thể (ví dụ: viền nét đứt cho External Service, double-circle cho trạng thái kết thúc).

---

## 2. Ngân Sách Khoảng Trắng & Khổ Trang In A4 (Whitespace & Aspect Ratio)

Khoảng trắng (Negative Space) không phải là khoảng trống vô nghĩa, mà là ranh giới phân tách thông tin:
1. **Tỷ lệ khung hình chuẩn (Aspect Ratio):**
   * Báo cáo Word khổ A4: Tỷ lệ vàng từ **4:3 đến 16:9** (ngang), chiều rộng từ 14.0cm đến 15.5cm.
   * Chiếu slide thuyết trình: Tỷ lệ **16:9** chuẩn widescreen.
   * **Bẫy cần tránh:** Tuyệt đối không để sơ đồ dài ngoằng theo chiều dọc (Aspect Ratio < 0.3) hoặc dẹt lép theo chiều ngang (Aspect Ratio > 3.5).
2. **Khoảng cách thở (Breathing Room):**
   * Khoảng cách giữa các node (`nodesep`): Tối thiểu 50px - 70px.
   * Khoảng cách giữa các tầng (`ranksep`): Tối thiểu 60px - 80px.
   * Phân nhánh cây tỏa đều: Không dồn cục các node sang một phía làm trống nửa hình còn lại.

---

## 3. Quản Lý Đường Nối & Chống Cắt Nét (Routing & Collision Avoidance)

Đường nối (Edges/Connectors) là nguồn gốc lớn nhất gây ra cảm giác "rác mắt" và "chằng chịt":
1. **Đường nối vuông góc 90° (`ortho` / `polyline`):**
   * Luôn ưu tiên đường nối bẻ góc vuông dứt khoát. Tránh nét cong tự do uốn lượn làm mất tính trang nghiêm của báo cáo kỹ thuật.
2. **Quy tắc Zero-Crossing (Hạn chế tối đa đường cắt chéo nhau):**
   * Sắp xếp lại thứ tự khai báo các khối hoặc dùng liên kết ẩn (`-[hidden]->`) để hoán đổi vị trí các node, đưa các node có quan hệ gần nhau về cùng một phía.
   * **CẤM** đường nối xuyên thẳng qua mặt một node khác.
3. **Quản lý nhãn trên đường nối (Edge Labels):**
   * Nhãn quan hệ phải ngắn gọn (1–3 từ, ví dụ: `gọi API >`, `sở hữu >`).
   * Khi đường nối cắt qua ranh giới package/cluster trong Graphviz: Chuyển nhãn thành `xlabel` hoặc rút ngắn tên nhãn để tránh bị đường viền cluster chém ngang mặt chữ.

---

## 4. Hệ Thống Cỡ Chữ & Bảo Toàn Dấu Tiếng Việt (Typography)

1. **Thang kích thước chữ chuẩn mực (Type Scale):**
   * Tên Package / Tầng kiến trúc: `13pt - 14pt` (In hoa, đậm).
   * Tên Class / Thực thể / Khối: `12pt` (Chữ đậm).
   * Thuộc tính / Phương thức / Trường dữ liệu: `10pt - 11pt` (Chữ thường).
   * Nhãn đường nối & Bội số (`0..*`, `1`): `9pt - 10pt`.
2. **Font chữ chuẩn in ấn:**
   * Dùng font chuẩn hệ thống có hỗ trợ đầy đủ Unicode tiếng Việt: `Segoe UI`, `Arial`, `Roboto`.
   * Tuyệt đối không để lỗi bể font hoặc mất dấu tiếng Việt trên ảnh render.

---

## 5. Quy Chuẩn Lưới Bố Cục (Grid & Grouping)

1. **Bố cục 3 cột chuẩn (3-Column Architecture):**
   * **Cột trái:** Tác nhân / Client / Khách truy cập / Module đầu vào.
   * **Cột giữa:** Tầng xử lý nghiệp vụ / API Gateway / Core Services.
   * **Cột phải:** Cở sở dữ liệu / Dịch vụ thanh toán ngoài / Hạ tầng lưu trữ.
2. **Nguyên tắc phân rã khi quá tải (Decomposition Threshold):**
   * Một sơ đồ trình chiếu/báo cáo không nên chứa quá **7 ± 2 thành phần trung tâm**.
   * Nếu hệ thống có trên 15 bảng hoặc nhiều luồng phức tạp: **Bắt buộc phân rã** thành 1 sơ đồ khái niệm tổng quan và 4–5 sơ đồ ca sử dụng/tuần tự chuyên sâu.
