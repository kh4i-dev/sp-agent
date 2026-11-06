# Audit Skill ERD & Class Diagram — 2026-11-01

## Phạm vi audit

Audit toàn bộ skill vẽ ERD (Entity-Relationship Diagram) và Class Diagram trong bộ `diagram-orchestrator`, `plantuml-diagrams`, `simplified-diagrams`, `diagram-design` và `diagram-auditor`. Không audit ngữ nghĩa cơ sở dữ liệu/OOP toàn bộ, chỉ audit **bố cục, hướng dẫn, kiểm định** theo chuẩn áp dụng cho báo cáo/đồ án học thuật.

---

## I. Tóm tắt kết quả

| Loại Sơ Đồ | Skill Chính | Trạng thái | Điểm Mạnh | Lỗ Hổng | Độ ưu tiên Sửa |
|---|---|---|---|---|---|
| **ERD (Entity-Relationship)** | `plantuml-diagrams` + `diagram-orchestrator` | ✅ HOÀN THIỆN | Auto-layout PlantUML đẹp; SSOT `tool-sweet-spot.md` rõ | Luật Crow's foot chưa nhấn mạnh; nhãn verb trên dây; phân rã khi > 4 cột | 🟡 MEDIUM |
| **Class Diagram (nhỏ)** | `plantuml-diagrams` | ✅ HOÀN THIỆN | Cú pháp UML chuẩn, zero-color, access modifier rõ | Không có ngưỡng phân rã; hub detection thiếu | 🟡 MEDIUM |
| **Class Diagram (lớn ≥ 6 lớp)** | `diagram-orchestrator` + `plantuml-diagrams` | ⚠️ THIẾU HƯỚNG DẪN | SSOT `class-diagram-layout.md` có, nhưng **agent chưa được dạy khi nào dùng draw.io thay PlantUML** | Threshold bố cục mơ hồ; hidden links không có quy tắc; fallback chưa rõ | 🔴 HIGH |
| **Conceptual Model (rút gọn)** | `simplified-diagrams` | ✅ HOÀN THIỆN | Luật Miller 7±2, 3-tầng lọc, kịch bản thuyết minh | Phân rã Sequence chưa có template mẫu | 🟡 MEDIUM |
| **Audit Tự Động** | `diagram-auditor` | ✅ HOÀN THIỆN | Chặn Crow's foot, đè chữ, cỡ font, zero-color | False-positive `C-FAN` / `S-LADDER` chưa phân quyết | 🟡 MEDIUM |

---

## II. Chi Tiết Phát Hiện

### A. ERD (Entity-Relationship Diagram)

#### ✅ Điểm Mạnh

1. **PlantUML auto-layout để vẽ ERD vừa:** SSOT `tool-sweet-spot.md` §1 rõ ràng: `ERD (vừa, ≤ 4 cột) → PlantUML auto`.
2. **Chuẩn thẩm mỹ:** Luật zero-color, `linetype ortho`, `nodesep 70`, `ranksep 70` có trong `plantuml-diagrams` SKILL.md §1 + §56–§73.
3. **Quy tắc Crow's foot:** `entity` syntax đúng chuẩn UML; pk/fk ghi bằng `<<PK>>` / `<<FK>>`.
4. **Ví dụ mẫu:** `simplified-diagrams` §3.1 có mẫu ERD tinh gọn 7 thực thể với cú pháp PlantUML chuẩn.

#### 🟡 Lỗ Hổng / Suy Nghĩ Còn Thiếu

1. **Luật CẤM nhãn verb trên dây Crow's foot chưa nhấn mạnh rõ**
   - `diagram-auditor` SKILL.md §111 liệt kê "Cấm viết text label lên đường Crow's foot" nhưng **`plantuml-diagrams` chưa cảnh báo tường minh**.
   - Agent dễ viết `User "1" -- "0..*" Order : "places"` → script báo lỗi chặn cứng, nhưng hướng dẫn chưa xác định rõ **"nói nhãn vai trò bằng cách nào thay thế"**.
   - **Sửa:** Thêm phần "Nhãn vai trò trong ERD" vào `plantuml-diagrams` SKILL.md §2.4.

2. **Phân rã ERD khi > 4 cột chưa có quy tắc cứng**
   - `tool-sweet-spot.md` §1 nói: `ERD (rất dày, > 4 cột / > 8 bảng) → Auto + tách, tay khi bí`.
   - Nhưng **`plantuml-diagrams` không dạy agent cách phân rã miền** (domain decomposition).
   - **Sửa:** Thêm playbook "Phân rã ERD theo miền" với mẫu code.

3. **Ngưỡng "vừa" (≤ 4 cột) chưa giải thích metric**
   - "≤ 4 cột" là dựa vào kích thước in A4 (~21cm) hay là số bảng logic?
   - **Sửa:** Ghi cụ thể: "4 cột @ 300DPI ≈ 28cm; nếu > 4 cột → landscape hoặc tách miền".

#### 🎯 Khuyến Nghị

- [ ] Thêm đoạn "Quy tắc nhãn vai trò ERD — Dùng role name, không ghi verb trên dây" vào `plantuml-diagrams` SKILL.md §2.4.
- [ ] Thêm playbook "Phân rã ERD theo miền" với 2–3 ví dụ mẫu.
- [ ] Rõ ràng hóa ngưỡng "4 cột" = bao nhiêu pixel @ 300DPI.

---

### B. Class Diagram (Nhỏ, 4–6 lớp)

#### ✅ Điểm Mạnh

1. **Cú pháp UML chuẩn:** `plantuml-diagrams` SKILL.md §2.4 liệt kê đầy đủ access modifier `+ - # ~` với ký tự text (đặt `classAttributeIconSize 0`).
2. **Ví dụ mẫu:** Mẫu Class Diagram đơn giản trong §2.4 đúng với quy ước.
3. **Zero-color:** Bắt buộc trắng-đen cho báo cáo học thuật.

#### 🟡 Lỗ Hổng

1. **Không có ngưỡng phân rã rõ ràng cho Class nhỏ**
   - `simplified-diagrams` SKILL.md chỉ nói "4–6 lớp là auto"; chưa ghi rõ **"nếu có nhiều association cùng cặp lớp thì sao"**.
   - **Sửa:** Thêm tiêu chí: "Nếu **degree ≥ 5** (một lớp nối ≥ 5 lớp khác) → cân nhắc phân rã hoặc vẽ tay".

2. **Không warning khi association "song song" (parallel)**
   - Class Diagram với Review–User có 2 vai trò `reviewer` / `reviewee` → dễ làm 2 dây chạy gần nhau.
   - Hướng dẫn chưa cảnh báo dấu hiệu này.
   - **Sửa:** Thêm: "Nếu cặp lớp có > 1 association với vai trò khác nhau → ghi rõ role name ở đầu mút".

---

### C. Class Diagram (Lớn ≥ 6 lớp, có hub)

#### ⚠️ LỖƠ HỔ CẨN: Ngưỡng Phân Rã & Fallback Chưa Rõ

**VẤN ĐỀ CỨNG:**
1. `diagram-orchestrator` SKILL.md nói: *"Class Diagram có từ 6 lớp trở lên, lớp trung tâm bậc cao → đọc class-diagram-layout.md"* (§191).
2. Nhưng **agent chưa được dạy KHOẢNG THỜI GIAN KHI NÀO dùng PlantUML auto, và KHI NÀO phải VẼ TAY draw.io**.
3. `tool-sweet-spot.md` §1 liệt kê: *"Class (≥ 6 lớp, có hub bậc ≥ 5) → draw.io tay / phân rã"*, nhưng **đó là SSOT của orchestrator, chứ `plantuml-diagrams` không biết mình phải tự gác lại**.

#### 🔴 ROOT CAUSE

- `plantuml-diagrams` sinh mã `.puml` tự động mà không kiểm tra `degree` từng lớp.
- Khi render, nếu PlantUML sinh ra hình xấu (hub dồn tâm, association song song chồng đè), **agent chưa được dạy dấu hiệu "đây là lúc phải vẽ tay"**.
- `dense-diagram-playbook.md` (cúng trách nhiệm của orchestrator) có hướng dẫn *"thử 1 biến/lần, rồi phân rã"*, nhưng chưa ghi `class-diagram-layout.md` (đó mới là SSOT thực sự cho bố cục Class lớn).

#### 🟡 Lỗ Hổng Chi Tiết

| Lỗ Hổng | Ở đâu | Sửa |
|---|---|---|
| Ngưỡng "≥ 6 lớp" là tuyệt đối hay tương đối? | `tool-sweet-spot.md` + `class-diagram-layout.md` không kết hợp | Thêm: "Nếu degree ≥ 5 hoặc multiplicity phức tạp, dùng draw.io thay auto" |
| Hidden links: bao nhiêu cái là quá nhiều? | `class-diagram-layout.md` §4 nói "không ép lưới 3 cột hàng loạt", nhưng agent không biết bắt đầu với mấy cái | Ghi: "Bắt đầu với 0 hidden links; chỉ thêm nếu render vẫn có giao cắt sau 1 lần sửa" |
| Fallback: khi nào từ bỏ PlantUML? | `manual-fallback.md` nói "≥ 2 vòng FAIL → chuyển draw.io", nhưng agent không biết render PlantUML bao nhiêu lần là "đủ" | Rõ: "Nếu **≥ 2 lần render → audit vẫn FAIL** trên **cùng 1 vấn đề** (giao cắt / hub dồn tâm) → dừng, chuyển draw.io" |
| Class Diagram dày (20+ lớp): tách thành bao nhiêu hình? | `simplified-diagrams` không nói cho Class lớn; chỉ nói cho ERD | Thêm: "Phân rã theo domain; mỗi hình 5–8 lớp; giữ lớp lặp lại với tên thống nhất" |

#### 🎯 Khuyến Nghị

- [ ] **Thêm Bước Kiểm trong `plantuml-diagrams` SKILL.md trước khi sinh mã:**
  ```
  1. Đếm lớp thực từ mô hình.
  2. Tính degree từng lớp = số association đầu mút.
  3. Nếu max(degree) ≥ 5 → cảnh báo: "Lớp hub phát hiện; cân nhắc phân rã hoặc vẽ tay draw.io"
  ```

- [ ] **Rõ ràng hóa fallback threshold trong `tool-sweet-spot.md` & `class-diagram-layout.md`:**
  - "Auto → render → soi → sửa-1-biến → render → soi (lặp này tối đa 2 vòng)."
  - "Nếu vòng 2 vẫn FAIL trên cùng 1 vấn đề → dừng, chuyển draw.io theo `manual-fallback.md`."

- [ ] **Link `class-diagram-layout.md` từ `plantuml-diagrams` SKILL.md § khi lớp ≥ 6.**

---

### D. Conceptual Model (Sơ Đồ Tinh Gọn)

#### ✅ Điểm Mạnh

1. **Luật Miller 7±2 rõ ràng:** `simplified-diagrams` SKILL.md §1.1 định nghĩa "5–9 thực thể".
2. **3-tầng lọc:** Core / Value Objects / Infrastructure được liệt kê rõ (§1.2).
3. **Kịch bản thuyết minh:** Khuyến nghị "mỗi mũi tên = 1 câu chuyện 10 giây" (§1.3).
4. **Template mẫu:** ERD tinh gọn 7 thực thể (§3.1); Sequence tinh gọn 4–5 hình (§2).

#### 🟡 Lỗ Hổng

1. **Phân rã Sequence chưa có template mẫu chi tiết**
   - `simplified-diagrams` SKILL.md §2 liệt kê **5 Use Case trọng điểm** (SEQ-01 ~ SEQ-05), nhưng **không có mẫu `.puml` cụ thể cho từng Sequence**.
   - Agent phải tự viết; dễ viết nhầm nhãn hoặc quên `autonumber`.
   - **Sửa:** Thêm ít nhất 2 mẫu Sequence đầy đủ (Seq-01 + Seq-02).

2. **Kịch bản thuyết minh chưa có template**
   - Khuyến nghị "mỗi mũi tên = 10 giây" nhưng chưa có mẫu **"tôi sẽ nói gì"** để agent học theo.
   - **Sửa:** Thêm phần "Mẫu Kịch Bản Thuyết Minh (60–90s)" với 3–5 câu mẫu cho từng lớp miền.

3. **Không cảnh báo khi phân rã Sequence > 5 hình**
   - Một số hệ thống lớn có > 5 luồng chính; chưa rõ "tối đa bao nhiêu hình?"
   - **Sửa:** Ghi: "Nếu > 5 use case trọng điểm → phân tầng (tầng 1 = overview; tầng 2 = 5 Sequence chi tiết)".

---

### E. Diagram Auditor

#### ✅ Điểm Mạnh

1. **Chặn cứng Crow's foot:** Lỗi ĐỎ "nhãn verb trên dây ERD" (§2 SKILL.md).
2. **Zero-color check:** Bắt tất cả mã màu không phải grayscale (§2).
3. **Cỡ chữ ≥ 9pt:** Bắt font nhỏ dưới ngưỡng in A4 (§2).
4. **Va chạm toạ độ:** Phát hiện nhãn chồng nhau.

#### 🟡 Lỗ Hổng

1. **C-FAN (Quạt GA) & S-LADDER (Thang Máy) là ứng viên, không phải lỗi tự động**
   - `diagram-auditor` SKILL.md §437 ghi: *"C-FAN ≥5 đường xuất phát gần một điểm — quạt ga, chỉ là ứng viên, quạt theo mẫu có thể chấp nhận"*.
   - Nhưng **agent hay nhầm: khi script báo `C-FAN`, agent tưởng là lỗi bắt buộc phải sửa**.
   - **Sửa:** Nhấn mạnh: "`C-FAN` và `S-LADDER` là **CẢNH BÁO VÀNG (tham khảo)**, không phải **LỖI ĐỎ (bắt buộc)**. Agent phán quyết: *nếu mắt thấy quạt rõ ràng, không chồng → `CHAP-NHAN-DUOC`*".

2. **False-positive khi gạch ngang quan hệ hai chiều**
   - `diagram-auditor` script có thể báo "quan hệ trùng lặp" khi thực tế là **2 vai trò khác nhau** (vd `reviewer` ← → `reviewee`).
   - Bản release hiện tại (per `dense-diagram-playbook.md` §6) đã ghi nhận, nhưng **hint này chưa được lên priority "HIGH"**.
   - **Sửa:** Thêm vào SKILL.md: *"Nếu script báo 'quan hệ 2 chiều' nhưng visual thấy 2 mũi tên + 2 nhãn vai trò tách bạch → ghi `BAO-OAN` kèm bằng chứng soi ảnh"*.

---

## III. Bao Quát Phác Thảo Sửa

### Priority 🔴 HIGH (Sửa NGAY)

| # | Vấn đề | Skill | Hành Động | Ước Lượng Công Việc |
|---|---|---|---|---|
| 1 | Class Diagram ≥ 6 lớp: ngưỡng phân rã & fallback chưa rõ | `plantuml-diagrams` + `diagram-orchestrator` | Thêm Bước Kiểm `degree ≥ 5 → draw.io`; link `class-diagram-layout.md`; rõ fallback threshold | 🟡 MEDIUM |
| 2 | Hidden links: không có quy tắc bắt đầu/tối đa | `class-diagram-layout.md` | Ghi: "Bắt đầu 0 links; chỉ +1 nếu render FAIL giao cắt" | 🟢 LOW |

### Priority 🟡 MEDIUM (Sửa Trong Vòng Lặp)

| # | Vấn đề | Skill | Hành Động | Ước Lượng |
|---|---|---|---|---|
| 1 | ERD: nhãn vai trò chưa có quy tắc thay thế verb | `plantuml-diagrams` SKILL.md | Thêm §: "Dùng role name thay verb; đặt gần đầu mút association" | 🟢 LOW |
| 2 | ERD > 4 cột: phân rã miền chưa có playbook | `plantuml-diagrams` | Thêm playbook mẫu với 2–3 ví dụ domain split | 🟡 MEDIUM |
| 3 | Class nhỏ: không warning degree ≥ 5 & parallel association | `simplified-diagrams` | Thêm tiêu chí: "degree ≥ 5 → consider draw.io; parallel → role name rõ" | 🟢 LOW |
| 4 | Conceptual: Sequence tinh gọn chưa có mẫu `.puml` | `simplified-diagrams` | Thêm 2–3 mẫu Sequence đầy đủ (SEQ-01, SEQ-02) | 🟡 MEDIUM |
| 5 | Conceptual: kịch bản thuyết minh chưa có template | `simplified-diagrams` | Thêm phần mẫu kịch bản 60–90s cho từng lớp miền | 🟡 MEDIUM |
| 6 | Auditor: `C-FAN` / `S-LADDER` — cảnh báo vs lỗi chưa rõ | `diagram-auditor` SKILL.md | Nhấn mạnh: "CẢNH BÁO VÀNG, không LỖI ĐỎ; agent phán quyết bằng mắt" | 🟢 LOW |
| 7 | Auditor: false-positive quan hệ 2 chiều | `diagram-auditor` SKILL.md | Thêm: "Nếu 2 vai trò + 2 nhãn tách → `BAO-OAN`; ghi bằng chứng" | 🟢 LOW |

### Priority 🟢 LOW (Tham Khảo / Tối Ưu)

| # | Vấn đề | Skill | Hành Động | Ước Lượng |
|---|---|---|---|---|
| 1 | ERD: rõ ràng hóa ngưỡng "≤ 4 cột" → pixels @ 300DPI | `tool-sweet-spot.md` | Ghi: "4 cột ≈ 28cm @ 300DPI; nếu > → landscape/tách" | 🟢 LOW |
| 2 | Class Diagram lớn: phân rã theo domain cho 20+ lớp | `simplified-diagrams` | Thêm section "Phân Rã Class Diagram Lớn" | 🟡 MEDIUM |

---

## IV. Bài Học Từ Audit

### Từ Use Case (ngành hàng xóm)

- **Bài học từ include/extend/generalization:** Cần **test 1 câu bắt buộc** cho mỗi quan hệ. Class/ERD cũng vậy — mỗi association phải trả lời *"tại sao có quan hệ này"* bằng một câu kinh doanh. Nếu chỉ là kỹ thuật → gộp hoặc ẩn.
- **Bài học từ bố cục:** Vẽ tay (draw.io) là MẶC ĐỊNH khi cần **vị trí tuyệt đối** (actor 2 bên, hub giữa, lane swimlane). PlantUML auto-layout **không kiểm soát được vị trí** → dễ sinh ra hình xấu.

### Áp Dụng Cho Class Diagram

- **Khuyến Nghị:** Class Diagram ≥ 6 lớp (hoặc degree ≥ 5) nên **mặc định đi vẽ tay draw.io**, không chờ auto-layout FAIL 2 lần rồi mới chuyển.
- **Lý Do:** Class (không như Sequence) không có **thứ tự tuyến tính** → auto-layout hay dồn hub vào 1 góc. Lại thường có **nhiều association cùng cặp lớp + vai trò khác nhau** → dây song song dễ chồng đè nhãn.

---

## V. Checklist Sửa (Dần Dần)

- [ ] Thêm BƯỚC KIỂM trong `plantuml-diagrams` SKILL.md: "Nếu lớp có degree ≥ 5 → cảnh báo vẽ tay draw.io"
- [ ] Link `class-diagram-layout.md` từ `plantuml-diagrams` khi lớp ≥ 6
- [ ] Rõ ràng hóa fallback threshold: "Auto render 2 vòng → 1 vấn đề FAIL → dừng, vẽ tay"
- [ ] Thêm §ERD: "Quy tắc nhãn vai trò — dùng role name, không verb trên dây"
- [ ] Thêm playbook phân rã ERD > 4 cột theo miền
- [ ] Thêm 2–3 mẫu `.puml` Sequence tinh gọn vào `simplified-diagrams`
- [ ] Thêm template kịch bản thuyết minh 60–90s
- [ ] Nhấn mạnh trong `diagram-auditor` SKILL.md: "C-FAN / S-LADDER = CẢNH BÁO VÀNG (tham khảo), không LỖI ĐỎ"
- [ ] Thêm ghi chú false-positive quan hệ 2 chiều

---

## VI. Kết Luận

**Skill ERD & Class Diagram không có lỗi CHẶN CỨng**, nhưng **agent chưa được dạy khoảng thời gian KHI NÀO chuyển từ auto-layout sang vẽ tay draw.io**. Ngưỡng "≥ 6 lớp" là danh sách nhưng chưa có dấu hiệu thực tế để agent tự quyết định.

Bảo hành hầu hết skill hoàn thiện được khắc phục bằng **3–4 bài học từ Use Case** (test 1 câu + quyết định vẽ tay khi cần vị trí tuyệt đối) + **rõ ràng hóa ngưỡng & playbook** thay vì viết code mới.

---

**Ngày audit:** 2026-11-01  
**Auditor:** Audit skill comprehensive  
**Status:** ✅ Sẵn sàng cho `skill-feedback` hoặc patch tùy ưu tiên
