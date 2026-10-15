# Step 0 fixture — Multi-actor Use Case layout regression

## Mục đích
Đây là fixture tổng hợp để kiểm tra khả năng phát hiện sơ đồ có nhiều actor/use case và nhiều hidden-layout constraints. Đây không phải mô hình nghiệp vụ triển khai của dự án thật.

## Bài toán
Kiểm tra liệu pipeline có cảnh báo trước khi người dùng nộp một Use Case Diagram đông tác nhân, nhiều use case, và bị ép bố cục bằng nhiều hidden links hay không.

## Actor được mô phỏng
- Phụ huynh/Học sinh: tài khoản, tìm kiếm, hồ sơ, kết nối, tương tác.
- Gia sư: hồ sơ gia sư, minh chứng, bài viết, phản hồi kết nối, tương tác.
- Kiểm duyệt viên: duyệt minh chứng và xử lý báo cáo.
- Quản trị viên: quản lý tài khoản và audit log.

## Ranh giới / mức trừu tượng
Hệ thống là nền tảng kết nối gia sư; 18 use case được cố ý đặt vào ba nhóm. Các quan hệ chỉ dùng để tạo fixture kiểm thử bố cục, cần kiểm tra UML trước khi dùng ngoài benchmark.

## Expected static signals
- Cảnh báo Use Case nhiều actor / nhiều use case.
- Cảnh báo có nhiều hidden-layout constraints.
- Không coi warning này là kết luận giao cắt; vẫn cần mở PNG và kiểm tra thủ công.
