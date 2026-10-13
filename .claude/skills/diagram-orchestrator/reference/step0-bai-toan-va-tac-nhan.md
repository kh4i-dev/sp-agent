# Bước 0 — Xác định bài toán, quy mô và tác nhân
> Trạng thái: `DRAFT | VERIFIED | INCOMPLETE`
>
> Không vẽ sơ đồ cho đến khi tài liệu này được điền và các điểm cốt lõi được xác minh.
> **Mỗi trách nhiệm tác nhân BẮT BUỘC có nguồn xác nhận; chỗ chưa rõ ghi `UNKNOWN`, cấm tự suy diễn** (xem Phụ lục A).

## 1. Thông tin tài liệu

- Tên hệ thống:
- Tên sơ đồ:
- Ngày cập nhật:
- Người/tài liệu xác minh:
- Tài liệu nguồn đã đọc:

## 2. Bài toán

- Vấn đề hiện tại là gì?
- Ai gặp vấn đề?
- Quy trình hiện tại đang dùng cách nào?
- Hạn chế/rủi ro của cách hiện tại:
- Hệ thống mới hỗ trợ/thay thế phần nào?
- Ngoài phạm vi hệ thống:

## 3. Quy mô vận hành

| Hạng mục | Giá trị đã xác minh | Nguồn/bằng chứng | Trạng thái |
|---|---|---|---|
| Nhóm người dùng | UNKNOWN | | UNKNOWN |
| Số actor nghiệp vụ | UNKNOWN | | UNKNOWN |
| Số người vận hành/quản trị | UNKNOWN | | UNKNOWN |
| Tần suất sử dụng | UNKNOWN | | UNKNOWN |
| Khối lượng dự kiến | UNKNOWN | | UNKNOWN |
| Quy mô triển khai | UNKNOWN | | UNKNOWN |

Không tự chuyển `UNKNOWN` thành con số ước đoán mà không ghi rõ đó là giả định.

## 4. Danh sách actor và trách nhiệm

| ID | Actor | Mục tiêu | Trách nhiệm được phép | Không chịu trách nhiệm | Bằng chứng | Trạng thái |
|---|---|---|---|---|---|---|
| A1 | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | INCOMPLETE |

Cần xem xét rõ, khi phù hợp:

- Ai là người dùng/khách chính?
- Ai tiếp nhận và xử lý nghiệp vụ?
- Ai thực sự sửa lỗi kỹ thuật/IT?
- Ai kiểm duyệt hoặc đối soát? Họ kiểm duyệt nội dung/nghiệp vụ hay vận hành kỹ thuật?
- Quản trị viên quản lý tài khoản, cấu hình và phân quyền đến mức nào?
- Có actor chuyên biệt như gia sư, nhà cung cấp, kiểm toán viên hoặc khách vãng lai không?
- Dịch vụ ngoài nào tương tác trực tiếp với hệ thống?

## 5. Ranh giới hệ thống

### Bên trong

- UNKNOWN

### Bên ngoài / hệ thống phụ

| Hệ thống/actor ngoài | Tương tác với hệ thống | Có phải actor của sơ đồ này? | Bằng chứng |
|---|---|---|---|
| UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

Chỉ đưa một dịch vụ ngoài thành actor nếu nó tương tác với hệ thống đang mô hình hóa; không đưa thành phần nội bộ như module hoặc database thành actor chỉ vì có tên kỹ thuật.

## 6. Phạm vi và mức trừu tượng

- Mục đích sơ đồ: `Tổng quan | Phân rã chức năng | Khác`
- Đối tượng đọc: UNKNOWN
- Nơi sử dụng: `Báo cáo A4 | Tài liệu kỹ thuật | Khác`
- Danh sách nhóm chức năng dự kiến: UNKNOWN
- Tổng số use case sơ bộ: UNKNOWN
- Nếu hơn 15 use case, lý do chưa phân rã (nếu có): N/A

## 7. Quan hệ UML có căn cứ

| Quan hệ dự kiến | Phần tử nguồn | Phần tử đích | Lý do nghiệp vụ | Bằng chứng | Trạng thái |
|---|---|---|---|---|---|
| UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | INCOMPLETE |

Không cần phải có đủ `include`, `extend` và generalization. Để trống nếu không có quan hệ phù hợp.

## 8. Điểm chưa rõ và giả định

| ID | Câu hỏi/giả định | Ảnh hưởng tới mô hình | Người/tài liệu cần xác minh | Trạng thái |
|---|---|---|---|---|
| U-01 | UNKNOWN | UNKNOWN | UNKNOWN | OPEN |

## 9. Kết luận cổng Bước 0

- [ ] Bài toán và cách làm hiện tại đã rõ.
- [ ] Phạm vi trong/ngoài hệ thống đã rõ.
- [ ] Actor và trách nhiệm đã có căn cứ.
- [ ] Vai trò nghiệp vụ đã phân biệt với IT/quản trị kỹ thuật.
- [ ] Quy mô được ghi bằng dữ kiện hoặc đánh dấu `UNKNOWN`.
- [ ] Mức trừu tượng và chiến lược phân rã đã chọn.
- [ ] Quan hệ đặc biệt chỉ được đề xuất khi có lý do.
- [ ] Các UNKNOWN trọng yếu đã được giải quyết hoặc được nêu rõ là blocker.

**Kết quả:** `PASS | FAIL | BLOCKED`

**Lý do:**

**Được phép chuyển sang Bước 1?** `YES | NO`

---

## Phụ lục A — Kỷ luật bằng chứng (Evidence Discipline)

> [!CAUTION]
> File Bước 0 **KHÔNG** phải thủ tục hình thức. Nó chỉ hợp lệ khi **mỗi trách nhiệm tác nhân có nguồn xác nhận truy vết được**.

1. **Định dạng nguồn hợp lệ:** `[REQ-xx]`, `[BRD §x.y]`, `[SRS §x.y]`, `[user story #xx]`, `[code: <file>:<line>]`, `[db: <table>]`, `[user-confirmed YYYY-MM-DD]`.
2. **Không được suy diễn:** nếu tài liệu/yêu cầu/người dùng KHÔNG nói rõ → ghi **`UNKNOWN`**, tuyệt đối không tự đoán rồi ghi như sự thật.
3. **Xử lý `UNKNOWN`:**
   - Ghi rõ `UNKNOWN` và **mức ảnh hưởng**: `[ảnh hưởng: cao/trung bình/thấp]` tới sơ đồ.
   - Nếu `UNKNOWN` **ảnh hưởng cao** (làm thay đổi tác nhân, ranh giới hoặc quan hệ) → **DỪNG, hỏi người dùng**; KHÔNG được vẽ mặc định.
   - Nếu ảnh hưởng thấp → được vẽ nhưng phải chú thích `(giả định: UNKNOWN)` và nêu rõ trong báo cáo nghiệm thu.
4. **Tỷ lệ bằng chứng tối thiểu:** ≥ 80% ô trách nhiệm có nguồn thực; phần còn lại là `UNKNOWN` được khai báo. Không đạt → Bước 0 **chưa hoàn thành**, cấm vẽ.

## Phụ lục B — Luồng lỗi & kiểm duyệt (nếu có)

Nếu dự án có luồng báo lỗi/kiểm duyệt: mô tả phát hiện → báo cáo → phân loại → **ai duyệt** → **ai xử lý** → đóng. Ghi rõ ranh giới: tác nhân nào **chỉ báo cáo/duyệt mà KHÔNG sửa lỗi IT**, tác nhân nào **sửa lỗi IT**. Nếu dự án không có luồng này → ghi `N/A`.

## Phụ lục C — Ví dụ điền mẫu (tác nhân TRUNG TÍNH — thay bằng vai trò thực của dự án)

> Đây chỉ minh hoạ **độ sâu tối thiểu** và **cách ghi nguồn**; KHÔNG phải tác nhân của dự án nào cụ thể.

**1. Bài toán:** `<Hệ thống X>` giải quyết `<vấn đề Y>` cho `<đối tượng Z>`, thay cho `<cách làm hiện tại>`.

**2. Quy mô:** ~`<N>` người vận hành (`<số quản trị>` + `<số vận hành/kiểm duyệt>`); `<số>` người dùng; `<tần suất / khối lượng>`.

**3. Tác nhân & trách nhiệm:**

| Tác nhân | Loại | Trách nhiệm | Sửa lỗi IT? | Nguồn (evidence) |
| :--- | :--- | :--- | :---: | :--- |
| Khách (chưa đăng nhập) | Chính | Xem nội dung công khai, đăng ký, đăng nhập | Không | `[user-confirmed 2026-01-01]` |
| Người dùng | Chính | `<tác vụ nghiệp vụ chính>` | Không | `[BRD §x.y]` |
| Nhân viên vận hành | Nội bộ | `<nghiệp vụ + báo cáo/duyệt>`, **KHÔNG sửa lỗi IT** | **Không** | `[BRD §x.y]` |
| Quản trị viên | Nội bộ | Quản trị hệ thống/nội dung; **xử lý lỗi kỹ thuật** | **Có** | `[BRD §x.y]` |
| Dịch vụ ngoài | Phụ | `<chức năng bên thứ ba>` | – | `[SRS §x.y]` |
| (ví dụ UNKNOWN) | … | `<điểm chưa rõ>` | Không rõ | **`UNKNOWN`** `[ảnh hưởng: cao]` → **dừng, hỏi người dùng** |

**4. Luồng lỗi:** `<ai phát hiện>` → `<báo cáo>` → `<phân loại>` → `<ai duyệt>` → `<ai xử lý>`. Ghi rõ ai **không sửa IT**.

**5. Quan hệ thật sự cần:** `<UC A>` `..> <<include>>` `<UC B>` vì `<lý do>`; `<UC C>` `..> <<extend>>` `<UC D>` khi `<điều kiện>`.

**6. Mô hình hóa:** `<số hình>`; nhóm: `<package A / B / C>`; tác nhân chính bên trái, hệ thống ngoài bên phải; phân rã nếu > 15 use case.
