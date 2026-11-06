# Reference: Quyết định include / extend / kế thừa tác nhân (Use Case)

> Tài liệu tham chiếu cho skill `use-case-layout`. Dùng khi chốt mô hình UML (Bước 1) để tránh vẽ quan hệ "cho đủ bộ". Được cập nhật từ audit lỗi btl-cnpm (2026-11-01).

## 0. Tại sao cần protocol này

Nhầm include ↔ extend hoặc kế thừa sai actor là lỗi **mô hình**, không phải lỗi bố cục. Nó làm sơ đồ sai nghĩa mặc dù hình vẽ có thể trông đẹp. Bảng dưới đây giúp quyết định một lần dựa vào **test 1 câu**, không phải "trông giống UML mẫu".

## 1. Test 1 câu cho mỗi quan hệ (bắt buộc)

| Quan hệ | Test (trả lời YES/NO) | Nếu YES → dùng | Nếu NO → |
|---|---|---|---|
| `<<include>>` | **"Nếu không làm X thì Y không hoàn thành được?"** — X là use case gốc, Y là hành vi bắt buộc | YES → include | Bỏ quan hệ hoặc đổi thành extend |
| `<<extend>>` | **"Chỉ xảy ra khi điều kiện Z đúng?"** — Z là điều kiện rõ ràng, không phải "luôn" | YES (có điều kiện) → extend | Bỏ hoặc chuyển thành include |
| Generalization (actor) | **"Con có phải là cha không? (is-a)"** — con kế thừa **toàn bộ** quyền cha + thêm đặc thù | YES → generalization | Tách tác nhân riêng, dùng association |
| Generalization (use case) | **"Use case con là một loại của cha?"** | YES (hiếm) → generalization | Bỏ, dùng include/extend |

**Luật cứng:** Không trả lời được test → **bỏ quan hệ đó**. Không thêm quan hệ chỉ để sơ đồ trông nhiều dây hoặc "giống UML mẫu".

## 2. include vs extend (so sánh)

| Tiêu chí | include | extend |
|---|---|---|
| **Tần suất** | **Luôn** gọi — bắt buộc | **Có điều kiện** — tùy |
| **Hướng mũi tên** | Từ base **→** included | Từ extending **→** base được mở rộng |
| **Hành vi** | Dùng chung bắt buộc | Mở rộng được, không bắt buộc |
| **Ví dụ** | "Đặt hàng" include "Xác thực OTP" (luôn cần) | "Đặt hàng" extend "Tặng quà" (khi có khuyến mãi) |
| **Lỗi thường gặp** | Included use case có actor riêng khởi tạo độc lập → đó là **association, không include** | Điều kiện luôn đúng → đó là **include, không extend** |

**Quy tắc chỉnh sửa include:**
- Nếu included use case có **actor riêng khởi tạo độc lập** → **bỏ include, vẽ 2 association riêng** thay vì 1 association + 1 include. 
  Ví dụ sai: UC-A (actor Customer) include UC-B (actor Admin khởi tạo) → sai mô hình. 
  Sửa: UC-A ← Customer, UC-B ← Admin (2 association riêng).

## 3. Kế thừa tác nhân (Actor Generalization) — **kiểm is-a chặt**

### 3.1 Khi nào kế thừa đúng

- Con **kế thừa toàn bộ quyền** cha **+ thêm** đặc thù riêng.
- Con không "chỉ dùng một phần" quyền cha.
- Quan hệ là **is-a** (con là một loại của cha), không phải "có quan hệ".

Ví dụ đúng:
- `VIPCustomer --|> Customer` — VIP kế thừa toàn bộ quyền khách thường + thêm quyền ưu tiên. ✅
- `Guest --|> Customer` — Khách chưa đăng ký không kế thừa gì từ khách đã đăng ký → **SAI**, tách riêng. ❌

### 3.2 Anti-pattern — từng thấy trong bộ 4 Use Case btl-cnpm

| Anti-pattern | Sai ở đâu | Cách sửa |
|---|---|---|
| `Auditor --|> Viewer` | Auditor không chỉ "xem" — còn **thay đổi trạng thái** (duyệt/từ chối). Không kế thừa toàn bộ. | Tách tác nhân riêng; nếu cả hai cần xem chung → dùng **`<<include>>`** giữa use case "Xem chi tiết", không kế thừa actor |
| `Admin --|> Auditor` | Admin quản trị **tài khoản/hệ thống**; Auditor kiểm duyệt **nghiệp vụ** — khác trách nhiệm hoàn toàn | Tách riêng, không kế thừa |
| `Admin --|> Customer` | Admin quản trị; Customer mua hàng — không is-a | Tách riêng |
| Kế thừa để tránh vẽ đường nối | "Gom use case vào một cụm" bằng kế thừa actor | Dùng **`<<include>>`** hoặc **`<<extend>>`** giữa use case, không kế thừa actor |

**Quy tắc:** Nếu con "chỉ" dùng một phần quyền cha → **không kế thừa**, tách tác nhân riêng.

## 4. Actor là hệ thống ngoài — ranh giới rõ

- Hệ thống ngoài chỉ là actor nếu **tương tác qua ranh giới hệ thống** (ví dụ: "Hệ thống thanh toán" gửi lệnh, nhận response).
- Nếu chỉ là **cơ chế bên trong** (SePay, SMTP, VietQR, thư viện) → **gộp vào use case**, không vẽ thành actor.

Ví dụ:
- "Gửi email" — Mail server là hệ thống ngoài (tương tác qua SMTP) → **có thể là actor** nếu bạn muốn thể hiện ranh giới.
- "Xác thực OTP" — OTP là **cơ chế bên trong** → gộp vào use case "Xác thực", không vẽ OTP thành actor.

## 5. Bảng traceability mẫu (cổng Bước 1)

Tạo bảng này **trước khi vẽ**; dùng làm checklist:

| From | To | Loại quan hệ | Test / Lý do | Ghi chú |
|---|---|---|---|---|
| Customer | UC-03 Gửi yêu cầu | association | Customer khởi tạo | - |
| UC-03 Gửi yêu cầu | UC-05 Xác thực OTP | include | Nếu không OTP thì yêu cầu không gửi được → YES | Bắt buộc |
| UC-03 Gửi yêu cầu | UC-06 Gửi thông báo | include | Nếu không thông báo thì vấn đề chưa xong → YES | Bắt buộc |
| UC-03 Gửi yêu cầu | UC-04 Thanh toán | extend | Chỉ khi yêu cầu cần tiền → YES (có điều kiện) | Có điều kiện |
| Auditor | UC-07 Kiểm duyệt | association | Auditor khởi tạo | - |
| UC-07 Kiểm duyệt | UC-08 Ghi log | include | Mọi duyệt phải log → YES | Bắt buộc |
| Customer | Guest | generalization | Customer "là một" Guest đã đăng ký? → **KIỂM is-a** | Nếu có căn cứ từ BRD |
| Viewer | Auditor | generalization | Auditor "là một" Viewer + thêm quyền duyệt? → **KHÔNG, Auditor khác Viewer** | Tách riêng, không kế thừa |

**Cách dùng bảng:**
1. Lập mô hình từ Bước 0 (bài toán, actor, use case).
2. Với mỗi dòng, trả lời test 1 câu ở cột "Test / Lý do".
3. Nếu test trả lời được → giữ quan hệ; nếu không → xóa dòng.
4. **Không bịa** quan hệ để gom use case hoặc trang trí sơ đồ.

## 6. Checklist Bước 1 — Model (bắt buộc trước khi vẽ)

Lưu file `docs/diagrams/<name>-model.md` hoặc ghi trong Bước 0 audit:

- [ ] **Mỗi quan hệ trả lời được test 1 câu** (§1 bảng trên).
- [ ] **Mỗi kế thừa actor đã kiểm is-a** (§3.1 — con kế thừa **toàn bộ** quyền cha?).
- [ ] Không có actor là **phương thức/kênh** (SePay, SMTP, …) — gộp vào use case.
- [ ] Không vẽ quan hệ chỉ để sơ đồ **"trông giống UML mẫu"**.
- [ ] **Bảng traceability hoàn thiện** (§5) — mỗi dòng là một quan hệ đã kiểm.
- [ ] **Included use case không có actor riêng khởi tạo độc lập** (nếu có → bỏ include, dùng 2 association).
- [ ] **Extend phải có điều kiện rõ ràng bằng 1 câu** — nếu luôn đúng → đổi thành include (§2).