---
name: engineering-discipline
description: Kỷ luật kỹ thuật & bài học xương máu khi làm dự án phần mềm. Gồm: verify trước khi báo xong (Evidence-before-Done), kiểm tra server/DB trước khi kết luận bug, an toàn migration & dữ liệu, secrets đọc từ env, encoding UTF-8, chống dead code, chống drift tài liệu, và quy tắc rollback/hỏi-trước-khi-phá. Dùng khi debug lỗi khó, trước khi tuyên bố "đã xong", khi đổi schema/migration, khi gặp 500/ERR_CONNECTION_REFUSED, mojibake tiếng Việt, field bị strip, hoặc cần checklist kỷ luật trước commit/bàn giao.
---

# Engineering Discipline Skill — Kỷ luật Kỹ thuật & Bài học Đã Trả Giá

Mục tiêu: chuyển các **lỗi đã từng phạm** thành **quy tắc chặn trước**, để không lặp lại. Skill này là bộ "phản xạ an toàn" cho mọi phiên làm việc có chạm code / hạ tầng / dữ liệu.

> [!IMPORTANT]
> Nguyên tắc gốc: **HIỂU BÀI TOÁN & TRẠNG THÁI HỆ THỐNG TRƯỚC KHI SỬA/KẾT LUẬN.** Kết luận sớm từ triệu chứng bề mặt là nguồn gốc của phần lớn lỗi dưới đây.

---

## 1. SÁU NGUYÊN TẮC LÕI

### 1.1. Evidence-before-Done — chạy thật rồi hãy nói xong
Không tuyên bố hoàn thành chỉ vì "trông đã xong". Bắt buộc có **bằng chứng thực thi**: build PASS, log, test, hoặc ảnh chụp thật. `PARTIAL` không được nâng thành `IMPLEMENTED`.

### 1.2. Kiểm tra server + DB trước khi kết luận "lỗi code"
Trước khi đổ lỗi cho logic, xác nhận **hạ tầng đang chạy**: backend up? DB up? đúng port? `500` / `ERR_CONNECTION_REFUSED` / timeout **thường do service tắt hoặc cấu hình sai**, không phải bug thuật toán.

### 1.3. Phân biệt triệu chứng vs nguyên nhân gốc
Khi lỗi không rõ nguyên nhân: lập giả thuyết → tái lập baseline → **đổi một biến một lúc** (Single-Variable Isolation) → so sánh → mới kết luận. Không kết luận nguyên nhân chỉ vì một thay đổi "tình cờ" hết lỗi.

### 1.4. Đổi mô hình/dữ liệu → rà MỌI nơi sử dụng
Khi đổi hợp nhất/tách/đổi tên field hay bảng: **grep toàn bộ** nơi đọc/ghi nó (API, service, UI, seed, test, doc). Một chỗ bỏ sót bộ lọc sẽ thành bug nghiệp vụ thật.

### 1.5. Secrets & cấu hình qua biến môi trường
Không hardcode mật khẩu/token/API key — kể cả trong seed/demo. Đọc từ env (ví dụ `SEED_DEMO_PASSWORD`). Kiểm tra metadata/secrets trước khi phát hành.

### 1.6. An toàn khôi phục & hỏi trước khi phá
Tạo **git tag/nhánh** trước khi xoá/đổi lớn; **stash** thay vì xoá WIP; **hỏi trước** khi đổi schema/phá cấu trúc; **chỉ commit khi được yêu cầu**. Sau thay đổi lớn → **đồng bộ tài liệu** (CONTEXT / DOMAIN_INVARIANTS / CHANGELOG) để chống drift.

---

## 2. BẢNG LỖI THƯỜNG GẶP → CÁCH TRÁNH

| # | Lỗi đã gặp | Cách sửa / phòng |
| :-: | :--- | :--- |
| 1 | **Ship UI placeholder** (khung/bìa trống che mất nội dung thật) | Không ship placeholder vô nghĩa; kiểm UI với **dữ liệu thật**; empty state phải là lời mời hành động |
| 2 | Tưởng lỗi code nhưng **backend/DB tắt** (500 / `ERR_CONNECTION_REFUSED`) | Kiểm tra server + DB + port **trước** khi kết luận |
| 3 | **Migration drift**: cột/bảng đã tồn tại ⇒ `migrate deploy` fail | Đối soát trạng thái DB; tạo bằng **SQL trực tiếp** rồi đánh dấu applied (ví dụ `prisma migrate resolve --applied`); **backup trước** |
| 4 | **Validation whitelist strip field**: DTO thiếu decorator ⇒ field bị loại ⇒ 500 | Rà **mọi** DTO; thêm decorator validate/allow cho từng field |
| 5 | **Encoding body sai** ⇒ tiếng Việt thành `?` (mojibake) | Gửi **UTF-8 bytes** + `Content-Type: application/json; charset=utf-8`; kiểm dấu tiếng Việt sau khi gửi |
| 6 | **Mật khẩu hardcode** trong seed | Đọc từ **env**; không commit secrets |
| 7 | Sót bộ lọc sau khi đổi mô hình (ví dụ quên lọc theo `audience`) | Rà **MỌI nơi** dùng model sau khi đổi (nguyên tắc 1.4) |
| 8 | **Dead code**: gọi endpoint/API không tồn tại | Rà & xoá; không giữ lời gọi chết |
| 9 | **Docs lệch code** sau thay đổi lớn | **Doc-Sync**: cập nhật CONTEXT / DOMAIN_INVARIANTS / CHANGELOG |

---

## 3. CHECKLIST TRƯỚC KHI BÁO "XONG" / TRƯỚC KHI COMMIT

- [ ] Đã **chạy thật** luồng chính + luồng lỗi, có **bằng chứng** (log/ảnh/build).
- [ ] Đã xác nhận **server + DB + port** đúng trước khi kết luận bất kỳ lỗi nào.
- [ ] Không còn **placeholder/ảnh giả/số liệu bịa**.
- [ ] Không còn **dead code**; đã `grep` mọi nơi dùng field/model vừa đổi.
- [ ] Không có **secret hardcode**; cấu hình đọc từ env.
- [ ] Đã **đồng bộ tài liệu** (CONTEXT/CHANGELOG/DOMAIN_INVARIANTS) nếu có thay đổi lớn.
- [ ] Có **tag/nhánh/stash** để rollback; chỉ commit khi được yêu cầu.
- [ ] Báo cáo rõ: **Changed / Decision / Evidence / Uncertainty / Status**.

---

## 4. TÀI LIỆU THAM KHẢO

- **Bài học chi tiết kèm ví dụ stack (NestJS/Prisma/HTTP/encoding…)**: [`reference/lessons-learned.md`](file:///E:/HOC%20TAP/my-project/sp-agent/.claude/skills/engineering-discipline/reference/lessons-learned.md)
