# Đặc tả Use Case — bộ 9 thành phần, kỷ luật ID, template & lỗi thường gặp

Mục đích: khi viết **đặc tả use case** (bảng luồng chính/phụ) cho Chương 2, tài liệu phải
để Developer biết cần code gì và Tester biết cần test trường hợp nào — không để mỗi người
tự diễn giải nghiệp vụ. Nguồn: bài viết người dùng cung cấp (02/11/2026) + thực hành BA phổ biến.

## 1. Bộ 9 thành phần (không được thiếu)

| Thành phần | Nghĩa | Bẫy khi bỏ sót |
|---|---|---|
| Use Case Name | Tên mục tiêu người dùng muốn đạt | Tên biến thành hành động kỹ thuật ("Click button") |
| Objective | Chức năng tồn tại để làm gì | Người đọc đoán phạm vi sai |
| Actors | Người/hệ thống tương tác (có **actor phụ**: OAuth provider, email service…) | Quên actor phụ → luồng xác thực không ai "diễn" |
| Pre-condition | Điều kiện trước khi UC bắt đầu | Tester không biết dựng data gì để chạy test |
| Trigger | Sự kiện kích hoạt | Không rõ ranh giới bắt đầu |
| Basic Flow | Các bước thông thường tới đích | — |
| Alternative Flow | Cách khác vẫn tới được đích | Bị nhét vào Exceptional → tester bỏ sót ca kiểm thử |
| Exceptional Flow | Lỗi/ngoại lệ, KHÔNG tới được đích | Mới liệt kê điều kiện mà không nêu phản hồi hệ thống |
| Post-condition | Trạng thái sau khi hoàn tất (kể cả luồng lỗi) | Tester không biết verify bản ghi có được insert hay không |

## 2. Kỷ luật ID (bắt buộc khi đặc tả dài hơn 1 màn hình)

1. **Đánh số từng bước** trong Basic Flow (1, 2, 3…).
2. **ID cho luồng phụ/ngoại lệ**: `A1`, `A2`… (alternative), `E1`, `E2`… (exceptional).
3. **Business Rules có ID riêng** (`BR-01`, `BR-02`…): quy tắc dữ liệu/nghiệp vụ viết MỘT nơi,
   các luồng và bảng ca kiểm thử chỉ *tham chiếu* — tránh lặp mô tả ở 3 nơi rồi lệch nhau.
4. **Truy vết**: bước 3 của E1 trong đặc tả → ca kiểm thử TC-05 ở Chương 4 cùng ghi
   "theo E1". Không có ID thì không truy vết được.

## 3. Exceptional Flow phải đủ 4 thứ (luật)

Chỉ liệt kê "Email không đúng định dạng" là **CHƯA ĐỦ**. Mỗi E-Flow cần:

```text
E1 — Điều kiện: email sai định dạng
     → Phản hồi hệ thống: hiển thị lỗi tại trường email, KHÔNG tạo tài khoản
     → Thông báo: "Email không hợp lệ, vui lòng kiểm tra lại"
     → Điểm quay về (rejoin): trở lại bước 2, dữ liệu đã nhập được giữ nguyên
```

Và **post-condition cho luồng lỗi**: trạng thái hệ thống không đổi, không có bản ghi mới
được tạo — đây chính là điều Tester cần để viết test phủ định.

## 4. Template bảng đặc tả (khớp "bảng luồng chính/phụ" ở report-scope §2)

```markdown
### 2.x. Đặc tả Use Case UC-01: <Tên>
- Mã: UC-01 · Actor chính: … · Actor phụ: … (nếu có)
- Objective: …
- Pre-condition: … · Trigger: …

| ID | Bước | Actor | Hệ thống phản hồi |
|---|---|---|---|
| 1 | … | Người dùng | … |

**Luồng thay thế:**
A1 — <điều kiện/chọn cách khác>: <các bước, về điểm nào của luồng chính>

**Luồng ngoại lệ** (mỗi mục đủ 4 thứ theo §3):
E1 — <điều kiện> → <phản hồi> → <thông báo> → <quay về bước n>

**Business Rules:** BR-01: … · BR-02: …
**Post-condition:** thành công: … · thất bại (E1, E2): …
```

## 5. Lỗi thường gặp (checklist chặn)

- [ ] Exceptional flow chỉ liệt kê điều kiện, thiếu phản hồi hệ thống / điểm quay về.
- [ ] Quên post-condition cho luồng lỗi.
- [ ] Gộp alternative vào exceptional (chọn đăng ký bằng Google **vẫn tới đích** → là A, không phải E).
- [ ] Bỏ sót actor phụ (hệ thống gửi mail, cổng thanh toán, API bên thứ ba).
- [ ] Quy tắc nghiệp vụ lặp lại trong nhiều luồng thay vì đặt ID `BR-xx` một nơi.
- [ ] Không đánh số bước → không truy vết được sang bảng ca kiểm thử Chương 4.
- [ ] Chỉ mô tả luồng thành công ("happy path") — đặc tả thiếu chiều sâu, vi phạm report-scope.

## 6. Format linh hoạt — nhưng nhất quán trong CẢ tài liệu

Không bắt buộc tách Basic/Alternative/Exceptional thành 3 mục rời. Ba hướng thay thế
hợp lệ: **Activity Diagram** (biểu diễn luồng + nhánh bằng sơ đồ — vẽ qua
`diagram-orchestrator`/`handdrawn-diagrams`), **Business Rules riêng** (quy tắc & điều kiện
kiểm tra dữ liệu), **tách UC con** khi một phương thức là mục tiêu độc lập
(ví dụ "Đăng ký bằng Google" tách thành UC riêng).

Quy tắc: **chọn một cách trình bày và dùng nhất quán cho toàn bộ use case trong báo cáo**;
khi tham gia dự án có sẵn, theo cấu trúc tài liệu hiện có trước khi đề xuất đổi.
Điều quan trọng: yêu cầu rõ ràng, nhất quán, đủ chi tiết để người đọc hiểu đúng nghiệp vụ —
không phải format nào "chuẩn hơn".

## 7. Ví dụ mẫu tối giản — UC-01: Đăng ký tài khoản (Spotify)

- Objective: cho phép người dùng tạo tài khoản mới để dùng dịch vụ nghe nhạc.
- Actor chính: Người dùng. Actor phụ: Google/Facebook (OAuth), hệ thống gửi email xác thực.
- Pre-condition: người dùng chưa có tài khoản. Trigger: nhấn "Sign Up".

| ID | Bước | Actor | Hệ thống phản hồi |
|---|---|---|---|
| 1 | Truy cập trang đăng ký | Người dùng | Hiển thị form đăng ký |
| 2 | Nhập email, mật khẩu, ngày sinh, giới tính (BR-01, BR-02) | Người dùng | Kiểm tra hợp lệ realtime |
| 3 | Xác nhận đăng ký | Người dùng | Kiểm tra BR-01..03, tạo tài khoản |
| 4 | — | Hệ thống | Thông báo thành công, điều hướng tới trang tải ứng dụng |

- A1 — Người dùng chọn đăng ký bằng Google/Facebook: xác thực qua OAuth, hệ thống nhận
  thông tin từ tài khoản được chọn, tiếp tục từ bước 3.
- E1 — Email sai định dạng (BR-01): báo lỗi tại trường email, quay về bước 2, giữ dữ liệu đã nhập.
- E2 — Email đã tồn tại (BR-02): báo "Email đã được sử dụng", quay về bước 2, gợi ý đăng nhập.
- E3 — Ngày sinh không hợp lệ / thiếu giới tính (BR-03): báo lỗi tương ứng, quay về bước 2.
- Post-condition — thành công: tài khoản được tạo, thông tin lưu trong hệ thống, người dùng
  đăng nhập được. Thất bại (E1–E3): không tạo tài khoản, không có bản ghi mới.
