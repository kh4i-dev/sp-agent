# Phân tích bài toán Use Case: include / extend / kế thừa tác nhân (Customer · Viewer · Auditor)

> Tài liệu phân tích mô hình UML Use Case cho nhóm tác nhân **Khách hàng (Customer)**, **Người xem (Viewer)**, **Người audit/kiểm duyệt (Auditor)**.
> Mục tiêu: xác định rõ **cái gì cần `<<include>>`**, **cái gì cần `<<extend>>`**, **cái gì cần kế thừa tác nhân (generalization)**; và audit lại toàn skill `use-case-layout` để bổ sung suy nghĩ còn thiếu.

---

## 0. Giả định & nguồn bằng chứng (Bước 0 mini)

| # | Nội dung | Nguồn | Trạng thái |
|---|---|---|---|
| 1 | Hệ thống có 3 nhóm tác nhân người dùng: Customer, Viewer, Auditor | Giả định từ yêu cầu | `ASSUMPTION` (chưa có BRD/SRS) |
| 2 | Customer khởi tạo luồng chính (đặt hàng / gửi yêu cầu) | Giả định | `ASSUMPTION` |
| 3 | Viewer chỉ đọc/tra cứu, không thay đổi trạng thái | Giả định | `ASSUMPTION` |
| 4 | Auditor kiểm duyệt / duyệt / từ chối, không tạo dữ liệu gốc | Giả định | `ASSUMPTION` |
| 5 | Có hệ thống ngoài (mail/thông báo) là tác nhân phụ | Giả định | `ASSUMPTION` |

> [!CAUTION]
> Mọi giả định trên đều là `ASSUMPTION`. Trước khi vẽ thật, phải tạo `docs/domain/step0-<du-an>.md` với bằng chứng (`[REQ-xx]`, `[BRD §x.y]`, `[code: file:line]`, `[user-confirmed YYYY-MM-DD]`). Thiếu Bước 0 → `FAIL — lỗi tư duy mô hình hóa`.

---

## 1. Phân biệt 3 quan hệ (để không vẽ "cho đủ bộ")

| Quan hệ | Khi nào dùng | Hướng mũi tên (nét đứt) | Test 1 câu nghiệp vụ |
|---|---|---|---|
| `<<include>>` | Use case cơ sở **luôn** gọi hành vi dùng chung bắt buộc | Từ base → về use case được include | "Nếu không làm X thì Y không hoàn thành được?" → YES |
| `<<extend>>` | Hành vi mở rộng **có điều kiện** (tùy ngữ cảnh) | Từ extending → về base được mở rộng | "Chỉ xảy ra khi điều kiện Z đúng?" → YES |
| Generalization (kế thừa) | Actor/use case con **là một loại** của cha, kế thừa toàn bộ quyền + thêm đặc thù | Tam giác rỗng hướng về phần tử tổng quát | "Con có phải là cha không? (is-a)" → YES |

**Luật cứng:** Nếu không trả lời được test 1 câu → bỏ quan hệ đó. Không thêm quan hệ để sơ đồ "trông giống UML mẫu".

---

## 2. Mô hình tác nhân & kế thừa (Actor Generalization)

### 2.1. Phân tầng tác nhân đề xuất

```
Guest (Khách chưa đăng nhập)
   └── Customer (Khách hàng đã đăng ký)   [generalization]
        └── VIP Customer (Khách VIP)       [generalization, nếu có căn cứ]

Viewer (Người xem / tra cứu)
   └── Auditor (Người audit)              [generalization? xem §2.2]

Admin (Quản trị viên)                     [tác nhân riêng, không kế thừa Customer]
```

### 2.2. Kiểm tra is-a (bảng quyết định)

| Cặp (con → cha) | is-a? | Kết luận | Ghi chú |
|---|---|---|---|
| Customer → Guest | Customer "là một" Guest (đã đăng ký vẫn có quyền Guest) | ✅ Kế thừa | Guest giữ use case công khai; Customer thêm use case cần đăng nhập |
| VIP Customer → Customer | VIP "là một" Customer với thêm quyền | ✅ Kế thừa (nếu BRD có VIP) | Không bịa nếu không có yêu cầu |
| Auditor → Viewer | Auditor "là một" Viewer (xem) + thêm quyền duyệt | ⚠️ Có thể, nhưng nên tách | Auditor không chỉ "xem" — còn thay đổi trạng thái. Kế thừa dễ gây nhầm "Auditor chỉ đọc". Khuyến nghị: **tác nhân riêng**, không kế thừa Viewer, trừ khi BRD nói rõ Auditor kế thừa quyền xem |
| Admin → Auditor | Admin "là một" Auditor? | ❌ Không | Admin quản trị tài khoản/hệ thống, Auditor kiểm duyệt nghiệp vụ — khác trách nhiệm (xem plantuml skill: phân biệt quản trị tài khoản vs vận hành nghiệp vụ) |
| Viewer → Guest | Viewer "là một" Guest? | ❌ Không (trừ khi Viewer không cần đăng nhập) | Viewer thường đã đăng nhập → không is-a Guest |

**Nguyên tắc:** Kế thừa actor chỉ dùng khi **thật sự có quan hệ is-a** và **con kế thừa toàn bộ quyền cha + thêm đặc thù**. Nếu con "chỉ dùng một phần" quyền cha → không kế thừa, tách tác nhân riêng.

### 2.3. Anti-pattern kế thừa

- ❌ Kế thừa để "gom use case cho gọn": `Auditor --|> Viewer` chỉ vì cả hai đều "xem dữ liệu" → sai, vì Auditor còn hành động thay đổi trạng thái.
- ❌ Kế thừa chéo giữa vai trò nghiệp vụ và quản trị (`Admin --|> Customer`).
- ❌ Kế thừa để tránh vẽ association: nếu con cần dùng use case của cha nhưng không is-a → dùng `<<include>>` giữa use case, không kế thừa actor.

---

## 3. Phân tích include / extend cho nhóm Customer · Viewer · Auditor

### 3.1. Bảng use case đề xuất (ví dụ domain tổng quát)

| ID | Use case | Actor khởi tạo | Nhóm |
|---|---|---|---|
| UC-01 | Xem danh sách / chi tiết | Viewer, Customer, Auditor | Tra cứu |
| UC-02 | Đăng nhập | Customer, Viewer, Auditor | Tài khoản |
| UC-03 | Gửi yêu cầu / đặt hàng | Customer | Luồng chính |
| UC-04 | Thanh toán | Customer | Luồng chính |
| UC-05 | Xác thực OTP | (hệ thống) | Dùng chung |
| UC-06 | Gửi thông báo (mail) | (hệ thống ngoài) | Dùng chung |
| UC-07 | Kiểm duyệt / duyệt / từ chối | Auditor | Kiểm duyệt |
| UC-08 | Ghi log audit | (hệ thống) | Dùng chung |
| UC-09 | Xuất báo cáo | Auditor, Admin | Báo cáo |
| UC-10 | Tìm kiếm nâng cao | Viewer | Tra cứu |

### 3.2. Quyết định include (bắt buộc, dùng chung)

| Base (luôn gọi) | Included (bắt buộc) | Lý do (1 câu) | Test include |
|---|---|---|---|
| UC-03 Gửi yêu cầu | UC-05 Xác thực OTP | Không xác thực thì yêu cầu không được gửi | "Nếu không OTP thì gửi yêu cầu không hoàn thành?" → YES |
| UC-03 Gửi yêu cầu | UC-06 Gửi thông báo | Mỗi yêu cầu phải thông báo cho các bên | "Nếu không thông báo thì UC-03 chưa xong?" → YES |
| UC-04 Thanh toán | UC-05 Xác thực OTP | Thanh toán bắt buộc OTP | YES |
| UC-07 Kiểm duyệt | UC-08 Ghi log audit | Mọi quyết định kiểm duyệt phải được ghi log | YES |
| UC-09 Xuất báo cáo | UC-01 Xem danh sách | Báo cáo lấy dữ liệu từ danh sách | YES |

**Quy tắc include:** Included use case **không được** là use case có actor riêng khởi tạo độc lập nếu nó chỉ là bước con bắt buộc. Nếu included use case có actor riêng → xem lại, có thể là association chứ không phải include.

### 3.3. Quyết định extend (có điều kiện)

| Base (được mở rộng) | Extending (mở rộng) | Điều kiện | Test extend |
|---|---|---|---|
| UC-03 Gửi yêu cầu | UC-04 Thanh toán | Chỉ khi yêu cầu cần thanh toán (không phải mọi yêu cầu) | "Chỉ xảy ra khi cần thanh toán?" → YES |
| UC-07 Kiểm duyệt | UC-09 Xuất báo cáo | Chỉ khi Auditor chọn xuất báo cáo sau duyệt | YES |
| UC-01 Xem danh sách | UC-10 Tìm kiếm nâng cao | Chỉ khi Viewer dùng bộ lọc nâng cao | YES |
| UC-02 Đăng nhập | UC-05 Xác thực OTP | Chỉ khi bật 2FA | YES |

**Quy tắc extend:** Extending use case **phải** có điều kiện rõ ràng bằng 1 câu. Nếu điều kiện luôn đúng → đó là include, không phải extend.

### 3.4. Association (đường liền, không mũi tên)

| Actor | Use case | Ghi chú |
|---|---|---|
| Customer | UC-03, UC-04 | Khởi tạo luồng chính |
| Viewer | UC-01, UC-10 | Chỉ đọc/tra cứu |
| Auditor | UC-01, UC-07, UC-09 | Kiểm duyệt + báo cáo |
| Admin | UC-09 (nếu có) | Quản trị |

### 3.5. Bảng tổng hợp quan hệ (traceability)

| From | To | Loại | Điều kiện / lý do |
|---|---|---|---|
| Customer | UC-03 | association | khởi tạo |
| Customer | UC-04 | association | khởi tạo |
| Viewer | UC-01 | association | tra cứu |
| Auditor | UC-07 | association | kiểm duyệt |
| UC-03 | UC-05 | include | bắt buộc OTP |
| UC-03 | UC-06 | include | bắt buộc thông báo |
| UC-04 | UC-05 | include | bắt buộc OTP |
| UC-07 | UC-08 | include | bắt buộc log |
| UC-03 | UC-04 | extend | khi cần thanh toán |
| UC-07 | UC-09 | extend | khi xuất báo cáo |
| UC-01 | UC-10 | extend | khi dùng filter nâng cao |
| Customer | Guest | generalization | is-a |
| VIP Customer | Customer | generalization | is-a (nếu có) |

---

## 4. Audit toàn skill `use-case-layout` — bổ sung suy nghĩ

### 4.1. Điểm mạnh hiện có (giữ nguyên)

- Bước 0 bắt buộc, có bằng chứng → tốt.
- Khóa actor trái/phải → tốt.
- Cấm vòng xa → tốt.
- Visual Review bằng mắt → tốt.

### 4.2. Lỗ hổng / suy nghĩ còn thiếu (bổ sung)

1. **Thiếu quyết định include/extend/generalization có hệ thống.**
   - Skill nói "quan hệ nếu có căn cứ" nhưng không có bảng test is-a / test include / test extend.
   - → Bổ sung §1–§3 của tài liệu này vào skill (hoặc reference).

2. **Thiếu phân biệt "actor là người" vs "actor là hệ thống ngoài".**
   - Skill đã cảnh báo phương thức thanh toán không phải actor, nhưng chưa có quy tắc cho "hệ thống ngoài chỉ tương tác qua ranh giới" (vd SMTP, SePay).
   - → Thêm: hệ thống ngoài chỉ là actor nếu tương tác qua ranh giới hệ thống; nếu chỉ là cơ chế bên trong → gộp vào use case.

3. **Thiếu quy tắc anti-pattern kế thừa.**
   - Skill chỉ nói "generalization nếu thật cần" nhưng không có ví dụ sai (Auditor --|> Viewer).
   - → Thêm bảng §2.3.

4. **Thiếu quy tắc "include use case không được có actor riêng khởi tạo độc lập".**
   - Nếu included use case có actor riêng → có thể là association, không phải include.
   - → Thêm vào §1.

5. **Thiếu quy tắc "extend phải có điều kiện rõ ràng bằng 1 câu".**
   - Nếu điều kiện luôn đúng → đó là include.
   - → Thêm vào §1.

6. **Thiếu quy tắc "kế thừa actor chỉ khi con kế thừa toàn bộ quyền cha".**
   - Nếu con chỉ dùng một phần → tách actor riêng.
   - → Thêm vào §2.2.

7. **Thiếu traceability table bắt buộc.**
   - Skill yêu cầu `docs/diagrams/<name>-model.md` nhưng không mẫu bảng traceability.
   - → Thêm mẫu bảng §3.5.

8. **Thiếu quy tắc "không vẽ quan hệ để sơ đồ trông giống UML mẫu".**
   - Skill có câu này nhưng chưa có test 1 câu.
   - → Thêm test §1.

### 4.3. Đề xuất patch skill

- Thêm file `reference/include-extend-inheritance.md` vào skill `use-case-layout`.
- Thêm 1 đoạn trong SKILL.md §1 (Mục tiêu) hoặc §3 (Luồng) trỏ tới reference.
- Thêm checklist vào Bước 1: "Mỗi quan hệ phải trả lời được test 1 câu (§1); mỗi kế thừa actor phải trả lời is-a (§2.2)."

---

## 5. Checklist nghiệm thu (audit)

- [ ] Có file Bước 0 với bằng chứng từng trách nhiệm tác nhân.
- [ ] Mỗi actor trả lời is-a test (§2.2).
- [ ] Mỗi include trả lời test include (§1).
- [ ] Mỗi extend trả lời test extend + điều kiện 1 câu (§1).
- [ ] Không có actor là phương thức/kênh (SePay, SMTP…) → gộp vào use case.
- [ ] Actor chỉ đứng Lane L/R.
- [ ] Không connector vòng xa.
- [ ] Có bảng traceability (§3.5).
- [ ] Render PNG + SVG, soi ảnh bằng mắt, Proof-of-View ≥ 3 nhãn.
- [ ] Chạy auditor 0 lỗi ĐỎ.

---

## 6. Kết luận

Việc xác định include/extend/kế thừa không phải là "vẽ cho đủ bộ" mà phải **trả lời được test 1 câu nghiệp vụ**. Đặc biệt với nhóm Customer/Viewer/Auditor, rủi ro lớn nhất là:
1. Kế thừa sai (Auditor --|> Viewer) → nhầm quyền.
2. Nhầm include ↔ extend → sai ngữ nghĩa.
3. Actor là phương thức/kênh → sai mô hình.

Skill `use-case-layout` cần bổ sung reference về quyết định quan hệ (include/extend/generalization) để tránh các lỗi trên.