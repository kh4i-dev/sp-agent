# Lessons Learned — Chi tiết & Ví dụ Stack (minh hoạ)

Bổ trợ cho [`SKILL.md`](file:///E:/HOC%20TAP/my-project/sp-agent/.claude/skills/engineering-discipline/SKILL.md). Các ví dụ dưới đây minh hoạ **mẫu lỗi lặp lại**, không gắn với một dự án cụ thể — thay tên bảng/module bằng thứ tự của bạn.

---

## L1. UI placeholder che nội dung thật
- **Triệu chứng:** bìa/khung trống vô nghĩa đè lên avatar/nội dung; nhìn "đã xong" nhưng thực chất rỗng.
- **Nguyên nhân:** ship ảnh/khối placeholder thay vì trạng thái thật.
- **Sửa:** bỏ placeholder; avatar/nội dung luôn hiển thị; empty state phải là **lời mời hành động**.
- **Phòng:** kiểm UI bằng **dữ liệu thật**, không chỉ bằng "không lỗi build".

## L2. "Lỗi code" hoá ra do hạ tầng tắt
- **Triệu chứng:** `500`, `ERR_CONNECTION_REFUSED`, request treo.
- **Nguyên nhân:** backend/DB chưa chạy, sai port, sai connection string.
- **Sửa:** khởi động lại đúng service; xác nhận port & env.
- **Phòng:** luôn **kiểm tra server + DB trước** khi kết luận bug logic (nguyên tắc 1.2).

## L3. Migration drift
- **Triệu chứng:** `migrate deploy` fail vì cột/bảng (ví dụ `Grade.slug`) **đã tồn tại** trong DB nhưng không có migration tương ứng.
- **Nguyên nhân:** DB bị chỉnh tay/ngoài migration ⇒ lịch sử migration lệch trạng thái thật.
- **Sửa:** tạo bảng/cột bằng **SQL trực tiếp**, rồi đánh dấu migration đã áp dụng (`prisma migrate resolve --applied <name>`), hoặc baseline lại.
- **Phòng:** **backup DB trước**; không sửa schema ngoài migration; đối soát `migrate status` định kỳ.

## L4. Validation whitelist loại bỏ field
- **Triệu chứng:** request hợp lệ nhưng field bị mất ⇒ `500`/dữ liệu sai.
- **Nguyên nhân:** `ValidationPipe({ whitelist: true })` **strip mọi field không có decorator validate**.
- **Sửa:** thêm decorator (`@IsString()`, `@IsOptional()`, `@Allow()`, …) cho **mọi** field DTO.
- **Phòng:** rà toàn bộ DTO sau khi bật `whitelist`; viết test gửi payload đầy đủ.

## L5. Encoding body ⇒ mojibake tiếng Việt
- **Triệu chứng:** tiếng Việt gửi đi biến thành `?` hoặc ký tự lạ.
- **Nguyên nhân:** client (ví dụ PowerShell `Invoke-RestMethod`) mã hoá body sai.
- **Sửa:** gửi **UTF-8 bytes** + header `Content-Type: application/json; charset=utf-8`.
- **Phòng:** sau mỗi lần gửi bằng script, **kiểm lại dấu tiếng Việt** ở phía nhận.

## L6. Secret hardcode trong seed
- **Triệu chứng:** mật khẩu/khóa xuất hiện trong mã hoặc log.
- **Nguyên nhân:** tiện tay hardcode khi viết seed/demo.
- **Sửa:** đọc từ env (`SEED_DEMO_PASSWORD`, …); không commit secrets.
- **Phòng:** quét secret trước khi commit/phát hành (nguyên tắc 1.5).

## L7. Sót bộ lọc sau khi đổi mô hình dữ liệu
- **Triệu chứng:** bug nghiệp vụ thật — ví dụ khi hợp nhất gói, một nhóm người dùng bị giới hạn sai số bài.
- **Nguyên nhân:** đổi mô hình nhưng chỉ sửa một chỗ, quên các nơi khác dùng cùng dữ liệu.
- **Sửa:** rà **MỌI nơi** đọc/ghi field đó (API, service, UI, seed, test, doc).
- **Phòng:** đổi mô hình ⇒ **grep toàn bộ** (nguyên tắc 1.4).

## L8. Dead code gọi endpoint không tồn tại
- **Triệu chứng:** hàm client (ví dụ `conversationsApi.create`) gọi endpoint backend không có ⇒ lỗi runtime/khó hiểu.
- **Nguyên nhân:** endpoint bị xoá/đổi nhưng client không cập nhật.
- **Sửa:** rà & xoá lời gọi chết; hoặc khôi phục endpoint nếu thực sự cần.
- **Phòng:** sau khi đổi/xoá API, grep client; dead code không được giữ.

## L9. Docs lệch code
- **Triệu chứng:** CONTEXT/CHANGELOG mô tả hành vi cũ.
- **Nguyên nhân:** thay đổi lớn nhưng quên đồng bộ tài liệu.
- **Sửa:** Doc-Sync ngay trong cùng thay đổi.
- **Phòng:** đưa Doc-Sync vào **checklist trước commit** (Mục 3 của SKILL.md).

---

## Ghi chú
Khi gặp lỗi **mới** không có trong danh sách: thêm một mục `L<n>` theo cấu trúc **Triệu chứng → Nguyên nhân → Sửa → Phòng**. Không xoá bài học cũ (supersede, never delete).
