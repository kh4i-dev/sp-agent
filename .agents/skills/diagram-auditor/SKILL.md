---
name: diagram-auditor
description: "Audit và kiểm định chất lượng sơ đồ kỹ thuật (PlantUML, Graphviz DOT, tldraw, SVG, PNG) trước khi gửi/chèn báo cáo Word. CỔNG PASS HAI ĐIỀU KIỆN — thiếu một là FAIL: (1) MÁY: script audit-diagrams.mjs 0 lỗi đỏ + file nguồn (.py generator / .puml / .dot / .tldr) TỒN TẠI + file ảnh (.png + .svg) TỒN TẠI >500B + zero-color + font ≥9pt + aspect 0.5–2.4; (2) MẮT/VISION: BẮT BUỘC model có VISION (multimodal) soi ảnh thật, ghi Proof-of-View ≥3 nhãn nguyên văn + vị trí + đánh giá 'sắp xếp đã hợp lý chưa' + 'Vision audit by: <model-id>'; model text-only không tính. Chống False PASS (script 0 đỏ nhưng mắt thấy FAIL). GATE 0: bắt buộc file Bước 0 đã xác minh (chưa rõ ghi UNKNOWN). Tách Semantic Review (nghiệp vụ/UML) vs Visual Review (hình học), không gộp, không lấy bố cục che lỗi mô hình. Báo cáo 5 kết quả độc lập."
---

# Diagram Auditor Skill — Cổng Kiểm Định Chất Lượng Sơ Đồ & Visual QA Thực Tế

Mục tiêu: Đảm bảo **100% sơ đồ xuất bản** đạt chuẩn kỹ thuật và thẩm mỹ in ấn học thuật cao cấp. Chặn đứng tận gốc tình trạng **"Script báo PASS nhưng mắt nhìn thấy FAIL"** — tức là file render được không lỗi cú pháp nhưng bố cục chật chội, nhãn đè nhau, khoảng trắng bất hợp lý, hoặc nhầm lẫn hình ảnh trong tài liệu.

**Cổng chữ trên canvas:** kiểm từng text element, không chỉ từ khóa `title/note`. Cấm cả footer, legend và chữ thuyết minh rời không có hộp. State chỉ chứa phần tử/nhãn UML; đọc `plantuml-diagrams/reference/state-playbook.md` để phân biệt nhãn composite/hành vi UML với chú thích và để tách declared/as-is/to-be. So khớp số cạnh sau mở rộng composite; không lấy đủ cạnh trong hằng số làm bằng chứng service đã cưỡng chế.

> **Phạm vi & đồng bộ (Scope):** skill này áp cho **sơ đồ học thuật** (zero-color, in A4): PlantUML / Graphviz / tldraw / draw.io / SVG. Tỷ lệ khung *khuyến nghị* **0.5–2.4**, nhưng **hard-fail** khi `> 3.8` hoặc `< 0.28` (khớp `scripts/audit-diagrams.mjs`) — hai ngưỡng này là **cùng một luật**, không mâu thuẫn. Bắt buộc đủ **cặp SVG + PNG** cho sơ đồ học thuật. KHÔNG áp cho sơ đồ branded/HTML của `diagram-design`.

---

## 0. CỔNG TIỀN KIỂM ĐỊNH (GATE 0) — BẮT BUỘC CÓ FILE BƯỚC 0 TRƯỚC KHI AUDIT

> [!CAUTION]
> **CẤM AUDIT SƠ ĐỒ USE CASE / MÔ HÌNH MIỀN KHI CHƯA CÓ FILE BƯỚC 0.**
> Trước khi audit bất kỳ sơ đồ Use Case / domain / actor nào, Reviewer **BẮT BUỘC** xác minh tồn tại file `docs/domain/step0-<du-an>.md` (template: [`diagram-orchestrator/reference/step0-bai-toan-va-tac-nhan.md`](../diagram-orchestrator/reference/step0-bai-toan-va-tac-nhan.md)), và file đó đã trả lời đủ: bài toán, quy mô, số người vận hành, **trách nhiệm từng tác nhân** (phân biệt ai sửa lỗi IT vs ai không sửa lỗi IT nhưng chịu trách nhiệm nghiệp vụ), ranh giới hệ thống.
> - **Không có file Bước 0** → trạng thái **BLOCKED** (thiếu nguồn sự thật), KHÔNG được audit và KHÔNG được PASS. Ghi nguyên văn: `⚠️ VI PHẠM KỶ LUẬT: thiếu Bước 0 — lỗi tư duy mô hình hóa, không phải lỗi bố cục.`
> - **Có file nhưng tác nhân/trách nhiệm mâu thuẫn với sơ đồ** (ví dụ một tác nhân nghiệp vụ *không* sửa lỗi IT lại bị vẽ như người xử lý lỗi kỹ thuật) → **FAIL**.

---

## 1. HỌC THUYẾT KIỂM ĐỊNH ĐỘC LẬP: HARD ACCEPTANCE GATE — NO SELF-CERTIFIED PASS

> [!CAUTION]
> **5 NGUYÊN NHÂN GỐC KHIẾN AGENT BỊ "FALSE PASS" (BÁO ẢO):**
> 1. **Nhầm lệnh chạy thành công với sản phẩm đạt yêu cầu:** Tạo `.puml` chạy renderer thành công và auditor báo 0 lỗi, nhưng kết quả ấy không chứng minh sơ đồ đúng kiến trúc hay dễ đọc khi in.
> 2. **Sửa hình nhưng chưa kiểm tra mô hình bên dưới:** Ví dụ trong sơ đồ kiến trúc 3 lớp, file có đường `UI_Main --> Store` nhảy cóc qua `Engine` (Tầng nghiệp vụ). Đây là mâu thuẫn kiến trúc nghiêm trọng nhưng agent chỉ lo vẽ đẹp mũi tên mà không sửa mô hình logic! Chưa làm rõ đang mô tả kiến trúc hiện tại (As-Is) hay mục tiêu (To-Be).
> 3. **"Mở ảnh" chưa chắc là "đã xem ảnh":** Chạy `Start-Process`, `os.startfile()` hay đọc metadata chỉ mở file trên máy tính hoặc lấy kích thước bytes. Chúng không đưa pixel vào thị giác của model.
> 4. **Công cụ audit tự động kiểm tra thiếu tiêu chí:** Script chỉ phát hiện toạ độ thô hoặc SVG hợp lệ, bỏ sót mật độ nhãn dày đặc, mũi tên gây hiểu nhầm, hoặc sai lệch quan hệ.
> 5. **Agent tự sinh rồi tự tuyên bố đạt:** Cùng một agent vừa vẽ, vừa quyết định thế nào là đẹp, vừa khen mình làm tốt. Cần cơ chế kiểm định độc lập (Adversarial Review) với quyền bác bỏ (`REJECT`).

### Nguyên tắc chỉ thị cốt lõi (Hard Acceptance Gate):
- Mục tiêu của nhiệm vụ là **chất lượng đã được kiểm chứng của sản phẩm cuối cùng**, KHÔNG PHẢI là việc thực thi thành công các lệnh render hay exit code 0 của script.
- Bắt buộc kiểm tra 5 cổng độc lập có bằng chứng. Một lệnh thành công, một file SVG hợp lệ hay lời tự nhận của agent tạo sơ đồ **KHÔNG PHẢI là bằng chứng hoàn thành**.
- **Quyền Bác Bỏ (Right to Reject):** Lượt kiểm định (Reviewer) phải chủ động tìm lỗi để bác bỏ sản phẩm chưa đạt. Không tối ưu hóa số lượng kết quả PASS; tối ưu hóa tính đúng đắn và độ tin cậy của sản phẩm bàn giao!
- **4 Trạng thái nghiệm thu bắt buộc:**
  - `PASS`: Tất cả các cổng bắt buộc đều có bằng chứng hỗ trợ rõ ràng.
  - `PASS WITH CONDITIONS`: Còn một số giới hạn nhưng được ghi nhận rõ ràng và được dự án chấp thuận.
  - `FAIL`: Còn tồn tại lỗi cụ thể chưa được khắc phục.
  - `BLOCKED`: Một kiểm tra bắt buộc không thể thực hiện được (ví dụ thiếu tool xem ảnh, thiếu schema).

---

## 1.5. CỔNG PASS HAI ĐIỀU KIỆN — "MÁY" + "MẮT" (TWO-CONDITION PASS GATE)

> [!CAUTION]
> **PASS CHỈ ĐƯỢC CÔNG NHẬN KHI ĐỦ CẢ HAI ĐIỀU KIỆN. THIẾU MỘT = FAIL.**
> "Script báo 0 đỏ" **KHÔNG** phải PASS. Nói miệng "tôi thấy ổn" mà **không có Proof-of-View từ vision** cũng **KHÔNG** phải PASS. Phải có **cả hai**: script xanh **và** vision soi ảnh thật có bằng chứng.

| # | Điều kiện | Ai thực hiện | Bằng chứng bắt buộc |
| :-- | :--- | :--- | :--- |
| **ĐK1 — MÁY** (Automated) | Script `audit-diagrams.mjs` + kiểm tra tệp trên đĩa | Script/CI | **0 lỗi ĐỎ**; **file nguồn (`.py` generator nếu sinh bằng Python / `.puml` / `.dot` / `.tldr`) TỒN TẠI**; **file ảnh `.png` + `.svg` TỒN TẠI > 500 bytes**; zero-color; font ≥ 9pt; aspect 0.5–2.4 |
| **ĐK2 — MẮT / VISION** (Vision Audit) | **BẮT BUỘC model CÓ VISION (multimodal) thực hiện** — pixel ảnh phải vào ngữ cảnh model, không suy luận từ text/SVG | Agent có vision (hoặc vision subagent) | Proof-of-View: **≥ 3 nhãn nguyên văn + vị trí**, **kết luận rõ "sắp xếp đã hợp lý chưa"** (bố cục cân đối, khoảng trắng đều, không đè/chồng, luồng đọc rõ, không dồn cục, không node mồ côi) + **tên/ID model vision đã soi** + SHA256 + dung lượng + thời điểm render |

**Ba luật chặn cứng:**

1. **Chỉ chạy script (ĐK1) mà chưa soi ảnh (ĐK2)** → `FAIL — visual QA missing` (dù script 0 đỏ).
2. **Chỉ soi ảnh (ĐK2) mà script còn lỗi ĐỎ / thiếu file nguồn `.py` / thiếu file ảnh** → `FAIL — automated gate not met`.
3. **Tệp nguồn (`.py` generator) KHÔNG được thay bằng file ảnh:** có ảnh mà không có `.py`/`.puml`/`.dot` gốc = **FAIL** (không tái lập được); ngược lại nguồn có mà chưa render ra ảnh = **FAIL** (chưa có sản phẩm để soi).

**Chuỗi bàn giao bắt buộc đủ 3 mắt xích — mỗi mắt xích phải qua đủ 2 điều kiện của chính nó:**

```text
file python vẽ (gen_*.py) ──(ĐK1: tồn tại + chạy ra ảnh)──> ảnh sơ đồ (.png/.svg)
      ──(ĐK1 script + ĐK2 VISION soi ảnh)──> DOCX ──(render PDF/PNG + VISION soi từng trang)──> giao
```

Thiếu bất kỳ mắt xích nào = **chưa xong**, không được báo PASS. DOCX dùng cổng hai điều kiện tương ứng ở `docx-report` mục **RENDER & VISUAL QA**.

> [!CAUTION]
> **ĐK2 PHẢI LÀ VISION AUDIT — KHÔNG PHẢI ĐỌC TEXT.**
> - Người/agent chấm **BẮT BUỘC** là **model có năng lực thị giác (multimodal/vision)**; ảnh `.png` phải được đưa **thẳng vào ngữ cảnh model** (ví dụ `tools.browser.preview`, đọc file `.png` bằng công cụ ảnh, hoặc giao **vision subagent**).
> - **CẤM** thay vision bằng: đọc mã `.py`/`.svg`/`.puml` dạng text, đọc metadata (width/height/DPI), đọc kích thước file, hay suy luận "chắc là ổn vì toạ độ đúng". Đó là **audit text**, không phải **audit vision**.
> - Nếu model đang chạy **không đọc được ảnh** → **BẮT BUỘC giao cho vision subagent/model** và ghi rõ model ID; không có vision nào khả dụng → `BLOCKED — Vision Audit unavailable`, **cấm PASS**.
> - Báo cáo bắt buộc ghi dòng: **`Vision audit by: <model-id>`** + đường dẫn ảnh đã soi + verdict "sắp xếp hợp lý / chưa hợp lý".

---

## 2. QUY CHUẨN BẮT BUỘC: VISION AUDIT — IMAGE MUST ACTUALLY BE SEEN BY A VISION MODEL

> [!CAUTION]
> **LUẬT BẰNG CHỨNG SOI ẢNH (PROOF-OF-VIEW) — KHÔNG CÓ BẰNG CHỨNG THÌ KHÔNG PHẢI PASS.**
> **VISION MODEL BẮT BUỘC:** 4 mục dưới đây phải do **model có năng lực thị giác (multimodal/vision)** trích ra từ pixel của chính ảnh `.png`; model text-only đọc mã nguồn/SVG **không được tính**. Báo cáo ghi kèm dòng `Vision audit by: <model-id>`.
> Việc "đã mở ảnh" là vô nghĩa nếu không để lại **bằng chứng quan sát cụ thể**. Agent BẮT BUỘC ghi lại:
> 1. **≥ 3 nhãn/chữ đọc được nguyên văn** từ chính ảnh PNG (không lấy từ file `.puml`).
> 2. **Vị trí tương đối** các khối chính (ví dụ: "Actor Khách ở cột trái, hàng giữa").
> 3. **Danh sách lỗi phát hiện hoặc xác nhận "không lỗi"** cho từng mục trong Danh mục lỗi bắt buộc (Mục 2, điểm 5) và 13 tiêu chí bố cục đẹp.
> 4. **Mã băm / dấu vết của đúng file đã soi** (tên file + dung lượng + thời điểm render) để chứng minh đã soi ảnh *sau* lần render cuối, không soi ảnh cũ.
> Không có 4 mục bằng chứng này → trạng thái **KHÔNG THỂ là PASS** (tối đa `PASS WITH CONDITIONS` hoặc `BLOCKED`).
>
> **LUẬT CHỐNG LÀM ẨU (ANTI-RUSH) — vì Agent hay vẽ nhanh rồi báo xong mà KHÔNG xem lại:** Trước mọi chữ `PASS`/`xong`, **BẮT BUỘC model có VISION nạp ảnh PNG vào ngữ cảnh model** (qua `tools.browser.preview` / đọc file ảnh / vision subagent). Model text-only đọc mã `.py`/`.svg`/`.puml` dạng text **không tính**. Tự hỏi: "Tôi trích được ≥ 3 nhãn nguyên văn từ ảnh không?". Không trích được = **chưa hề xem ảnh** = **CẤM PASS**. Nếu môi trường không có công cụ đưa ảnh vào tầm nhìn của model có vision → báo `BLOCKED — Vision Audit unavailable`, **thà nói chưa xong còn hơn bàn giao ảnh chữ đè/dây rối mà chưa nhìn**. "Render exit 0" và "script 0 đỏ" **KHÔNG phải** bằng chứng đã soi ảnh.

### 2.0. LUẬT CHỐNG SAO CHÉP MÀU ẢNH MẪU (REFERENCE-COLOR PROHIBITION)
> [!IMPORTANT]
> Nếu người dùng gửi sơ đồ mẫu **có màu**, đó KHÔNG phải lệnh cho phép dùng màu. Agent chỉ sao chép **cấu trúc/bố cục/nhóm/quan hệ** từ ảnh mẫu, và **BẮT BUỘC xuất B&W**. Mọi mã màu phi thang độ xám phát hiện trong SVG render → **FAIL** (hard-block), kể cả khi người dùng nài nỉ (trừ khi có ghi đè tường minh `override-monochrome: true`).

Sau khi render mỗi sơ đồ, Agent **BẮT BUỘC** thực hiện quy trình kiểm tra thị giác nghiêm ngặt sau:

1. **Xác minh file vật lý:** File PNG tồn tại trên đĩa, dung lượng > 0 bytes và mở được bình thường.
2. **Đưa ảnh trực tiếp vào ngữ cảnh model:** Dùng công cụ xem ảnh có khả năng đưa nội dung hình ảnh vào ngữ cảnh của model (như `view_file` trên tệp `.png`) để trực tiếp kiểm tra hình ảnh thực tế.
3. **CẤM giả định việc xem ảnh:** Tuyệt đối **KHÔNG** được coi các thao tác sau là bằng chứng đã trực tiếp kiểm tra hình ảnh:
   - Chạy lệnh hệ thống `os.startfile()` hoặc `Start-Process`.
   - Đọc kích thước file trên đĩa (bytes / KB).
   - Phân tích metadata ảnh (width, height, DPI).
   - Đọc mã nguồn `.puml`, `.dot` hoặc tệp SVG dạng text.
4. **Kiểm tra riêng từng sơ đồ:** Mở riêng từng hình ở kích thước đủ lớn để soi chi tiết. Nếu có nhiều sơ đồ, có thể dùng contact sheet để có cái nhìn tổng quan, nhưng vẫn bắt buộc phải mở từng hình để kiểm tra chi tiết từng thành phần.
5. **Danh mục lỗi bắt buộc phải soi và ghi nhận cụ thể:**
    - **Tư duy bố cục (theo SSOT `diagram-orchestrator/reference/layout-thinking.md` §7):**
      checklist 60 giây — 4 góc đều có mực; cạnh dài nhất ≤ 2.5× trung vị; nhãn đủ dấu
      tiếng Việt, không cụt/đè; mọi FK/association có đúng một đường; container không rỗng > 25%.
    - **Đứt nét viền / Mất nét ô**: Kiểm tra viền hộp có bị mất nét do rect trắng đè viền hoặc do nhãn đè viền hay không (`rx=0, ry=0` phải vuông vức và liền mạch 100%).
    - **Tab Frame Sequence đè chữ**: Khung nhóm/Transaction (`alt`, `opt`, `group`) có khoảng đệm >= 30px từ đỉnh khung xuống thông điệp đầu tiên, không để đè chữ lên tab.
    - **Cự ly thở Sequence**: Khoảng cách dọc giữa các bước thông điệp phải >= 45px, không nén chật chội.
    - **Nhãn chuyển trạng thái / Mũi tên kết thúc**: Cách mép hộp >= 35px, không dính sát vào thành hộp.
    - **Tiêu đề hoặc Chú thích nhúng trong canvas**: Phát hiện và loại bỏ tiêu đề to (`title`) hoặc hộp chú thích nét đứt (`legend`/`note box`) bên trong ảnh (vi phạm chuẩn học thuật).
   - Chữ đè lên chữ, text đè lên đường kẻ.
   - Nhãn không gắn đúng vào đường nối tương ứng (lơ lửng, lệch vị trí).
   - Mũi tên sai hướng logic hoặc đi chéo ngang mặt khối khác.
   - Đường nối cắt xuyên qua khung hoặc cắt qua nội dung của box.
   - Cỡ chữ quá nhỏ so với tỷ lệ chung (< 9pt), không đọc được khi in ra A4.
   - Khoảng trắng bất hợp lý (lệch dồn cục sang một bên, để trống hoác bên còn lại).
   - Luồng nghiệp vụ rối rắm, khó hiểu cho người đọc.
   - **Màu phi thang độ xám lọt vào ảnh** (dấu hiệu copy màu từ ảnh mẫu) → vi phạm zero-color.
   - **Node mồ côi** (khối không có đường nối nào) hoặc **node trùng chồng** lên nhau.
   - **Cụm dồn cục (clustering):** ≥ 3 node cách nhau < 30px.
   - **Trọng tâm lệch:** các khối dồn về một góc, để trống hoác phần lớn khung hình.
   - **Tỷ lệ khung hình** ngoài khoảng 0.5–2.4 (dẹt lép hoặc dài ngoằng).
6. **Vòng lặp sửa lỗi thực nghiệm bằng cô lập biến số (Single-Variable Empirical Isolation):** Chỉ sửa sau khi đã xác định chính xác giả thuyết lỗi; **chỉ thay đổi một biến số duy nhất tại một thời điểm** (ví dụ: gỡ nhãn cạnh nghi vấn trước, giữ nguyên cấu trúc package và layout); sau khi sửa bắt buộc render lại và **mở xem ảnh mới** để so sánh trực tiếp với ảnh mốc (baseline). Tuyệt đối không thay đổi đồng loạt nhiều yếu tố rồi võ đoán nguyên nhân.
7. **Xử lý khi thiếu công cụ xem ảnh:** Nếu môi trường thiếu công cụ xem ảnh đưa được pixel vào ngữ cảnh model, Agent phải dừng lại và báo:
   `BLOCKED — Visual QA unavailable`. Tuyệt đối không được đoán mò kết quả dựa trên output của renderer hay script auditor!

---

## 3. BẢNG PHÂN ĐỊNH RANH GIỚI KIỂM ĐỊNH (AUDIT SCOPE & LIMITATIONS)

| Tiêu chí kiểm tra | Script tự động `audit-diagrams.mjs` | Agent soi mắt & đối chiếu thực tế |
| :--- | :---: | :---: |
| Banner cảnh báo compiler (`Please use...`, `Warning`, `Syntax`) | **Kiểm tra được 100%** | Xác nhận lại |
| Cú pháp thẻ SVG hợp lệ, kích thước file > 500B | **Kiểm tra được 100%** | Không cần |
| Tồn tại đồng thời cặp SVG vector và PNG raster 300DPI | **Kiểm tra được 100%** | Xác nhận kích thước in ấn |
| Chống nhúng từ khóa `title` bên trong canvas ảnh | **Kiểm tra được 100%** | Kiểm tra caption bên ngoài |
| Chữ đè chữ toạ độ thô & Đường nối xẻ ngang chữ ngắn | **Kiểm tra được 100%** | Soi các cụm chữ phức tạp |
| Cấm viết text label lên đường Crow's foot trong ERD | **Kiểm tra được 100%** | Kiểm tra đúng thực thể |
| **Mật độ nhãn chen chúc giữa các tầng kiến trúc** | Cảnh báo dải Y hẹp | **BẮT BUỘC Agent soi mắt** |
| **Sự cân đối khoảng trắng (Whitespace balance)** | Cảnh báo aspect ratio cực đoan | **BẮT BUỘC Agent soi mắt** |
| **Luật zero-color (chỉ cho phép thang độ xám)** | **Kiểm tra được 100%** (quét mọi `fill`/`stroke`/`rgb()`) | Xác nhận lại |
| **Cỡ chữ tối thiểu (≥ 9pt) & tỷ lệ khung 0.5–2.4** | **Kiểm tra được 100%** | Xác nhận lại |
| **Node mồ côi / node trùng chồng** | Cảnh báo heuristic | **BẮT BUỘC Agent soi mắt** |
| **Trọng tâm khối bị lệch (centroid skew)** | Cảnh báo heuristic (lệch > 20%/trục) | **BẮT BUỘC Agent soi mắt** |
| **Tính đúng đắn ngữ nghĩa (Đúng code, đúng schema DB)** | *Không kiểm tra được* | **BẮT BUỘC Agent đối chiếu** |
| **Khớp hình ảnh với Caption trong Word DOCX** | *Không kiểm tra được* | **BẮT BUỘC Agent đối chiếu** |
| **Bố cục in ấn trang Word A4 (Chống rớt trang, rớt caption)** | *Không kiểm tra được* | **BẮT BUỘC Agent đối chiếu** |
| **Giả định "đã dùng package/nodesep/ranksep nên hết giao cắt"** | *Không kiểm tra được* (cấu hình KHÔNG phải bằng chứng) | **BẮT BUỘC render + soi ảnh thật** |

---

## 3.5. HAI CỔNG NGHIỆM THU TÁCH BIỆT (SEMANTIC REVIEW vs VISUAL REVIEW)

> [!CAUTION]
> **KHÔNG ĐƯỢC GỘP — VÀ THỨ TỰ BẤT BIẾN.**
> Nghiệm thu gồm **HAI cổng độc lập**, mỗi cổng có quyền phán riêng:

| Cổng | Phán cái gì | Gồm các mục | Điều kiện FAIL |
| :--- | :--- | :--- | :--- |
| **A. Semantic Review (Nghiệp vụ/UML)** | Mô hình **ĐÚNG hay SAI** | Bước 0 (đủ + có bằng chứng/`UNKNOWN` khai báo), đối chiếu schema/code/kiến trúc, đúng quan hệ include/extend/kế thừa, đúng tác nhân & ranh giới | **Thiếu Bước 0 đã xác minh** = FAIL nghiệp vụ; tác nhân/trách nhiệm mâu thuẫn = FAIL |
| **B. Visual Review (Hình học)** | Hình **ĐỌC ĐƯỢC hay KHÓ ĐỌC** | Render thật + đo kích thước + soi PNG (Proof-of-View) + chạy `audit-diagrams.mjs` + 13 tiêu chí bố cục | Đè chữ/cắt nét/màu phi xám/chữ <9pt/dồn cục = FAIL thị giác |

**Ba luật bất di bất dịch:**
1. **Không có Bước 0 đã XÁC MINH → KHÔNG VẼ, KHÔNG AUDIT** (BLOCKED).
2. **Có Bước 0 nhưng mô hình SAI → KHÔNG được căn chỉnh bố cục để che lỗi** (sửa mô hình trước; cấm dùng mẹo trình bày để giấu lỗi nghiệp vụ).
3. **Mô hình ĐÚNG nhưng hình KHÓ ĐỌC → tiếp tục tối ưu bố cục + kiểm tra lại** — **FAIL ở cổng B KHÔNG làm mất hiệu lực của cổng A**, và ngược lại: **cổng A FAIL thì mọi nỗ lực làm đẹp ở cổng B đều vô nghĩa** — không được lấy hình đẹp để bù cho mô hình sai.

---

## 4. BÁO CÁO ĐỘC LẬP 5 KẾT QUẢ KIỂM CHỨNG (SEPARATE 5-POINT VERIFICATION)

> [!IMPORTANT]
> **QUY TẮC BẤT BIẾN:**
> **KHÔNG GỘP NĂM KẾT QUẢ DƯỚI ĐÂY THÀNH MỘT TRẠNG THÁI PASS DUY NHẤT NẾU CÒN BƯỚC CHƯA ĐƯỢC KIỂM CHỨNG.**
> Báo cáo nghiệm thu bắt buộc phải trình bày riêng rẽ từng mục:

1. **Render validation:** File PNG & SVG tồn tại trên đĩa, không rỗng (> 500 bytes), **file nguồn (.py generator nếu dùng Python / .puml / .dot / .tldr) TỒN TẠI** (bằng chứng tái lập), biên dịch sạch sẽ không có banner cảnh báo compiler (`Please use...`, `Warning`), và SVG **không chứa mã màu phi thang độ xám**.
2. **Automated audit:** Kết quả từ script `audit-diagrams.mjs` (0 lỗi ĐỎ): không va chạm tọa độ chữ, không đường cắt ngang chữ, không nhãn trên Crow's foot ERD, **màu grayscale đạt luật zero-color**, **cỡ chữ nhỏ nhất ≥ 9pt**, tỷ lệ aspect ratio hợp lý (0.5–2.4). Các cảnh báo VÀNG phải được Agent phân xử.
3. **Actual visual inspection:** Kết quả từ việc Agent trực tiếp mở ảnh PNG bằng công cụ xem ảnh vào ngữ cảnh model, **kèm bằng chứng soi ảnh ở Mục 2** (soi nét chữ thông thoáng, không chen chúc nhãn giữa các tầng, bố cục cân đối không lệch dồn cục, không node mồ côi, luồng rõ ràng, đạt 13 tiêu chí bố cục đẹp). **AGENT PHẢI NÉN THÀNH 1 CÂU KẾT LUẬN RÕ: "SẮP XẾP HỢP LÝ" HOẶC "CHƯA HỢP LÝ (do X)"**. Thiếu câu kết luận = FAIL ĐK2.
4. **Semantic correctness (Cổng A — Nghiệp vụ):** Xác minh **Bước 0 đã có và có bằng chứng** (mỗi trách nhiệm tác nhân trỏ nguồn, chỗ chưa rõ ghi `UNKNOWN`), rồi đối chiếu 100% với schema CSDL, mã nguồn thật hoặc kiến trúc quy chuẩn (không vi phạm nhảy cóc tầng như `UI -> Store`, đúng tên bảng/class, đúng khóa PK/FK, đúng khoảng cách Levenshtein toán học trên cạnh BK-Tree). **Thiếu Bước 0 đã xác minh → FAIL nghiệp vụ, bất kể hình đẹp tới đâu.**
5. **DOCX rendered-page inspection:** Đã kiểm tra trực quan trang văn bản sau khi chèn hình (chiều rộng 14–15.5 cm căn giữa, khớp 100% hình với Caption `Hình X.Y`, có câu văn dẫn dắt, có thuộc tính `keep_with_next` chống rớt caption sang trang sau).

---

## 5. CỔNG NGƯỜI DÙNG NGHIỆM THU — HỎI TRƯỚC KHI THAY VÀO DOCX

> [!IMPORTANT]
> **QUY TẮC CHỜ NGƯỜI DÙNG DUYỆT (USER ACCEPTANCE CHECKPOINT):**
> Sau khi tạo ảnh và báo cáo kiểm định 5 cổng, Agent **DỪNG LẠI**, tuyệt đối **KHÔNG TỰ Ý GHI ĐÈ/SWAP ẢNH VÀO FILE WORD** nếu chưa có sự xác nhận của người dùng!
> 
> Agent phải hiển thị ảnh trực quan và hỏi người dùng câu hỏi nghiệm thu chuẩn:
> *"Tôi đã hoàn thành bản vẽ và kiểm định 5 cổng phía trên. Bạn kiểm tra trực quan giúp tôi: Ảnh đã đạt yêu cầu để thay thế luôn vào tài liệu Word chưa, hay cần sửa đổi/tinh chỉnh ảnh nào? Vui lòng phản hồi để tôi tiến hành bước tiếp theo!"*

---

## 6. BÀN GIAO TRỰC QUAN SẠCH — CẤM XẢ MÃ NGUỒN (ZERO CODE DUMPS)

- File mã nguồn (`.puml`, `.dot`, `.tldr`) **chỉ được lưu trên ổ đĩa**, tuyệt đối **KHÔNG in khối code nguồn** ra câu trả lời chat làm tràn màn hình.
- Phản hồi bàn giao **BẮT BUỘC CHỈ GỒM**:
  1. **Ảnh sơ đồ trực quan (Rendered Preview):** `![Hình X.Y: Tên sơ đồ](path/to/diagram.png)`.
  2. **Tiêu đề sơ đồ chuẩn:** `*Hình X.Y: Tên sơ đồ*`.
  3. **Báo cáo chi tiết 5 kết quả kiểm chứng độc lập** (không gộp tắt).
  4. **Câu hỏi xin ý kiến nghiệm thu người dùng** (theo Mục 5).
  5. **Đường dẫn tệp nguồn (Link Markdown ngắn gọn):** `[Mã nguồn .puml](file:///path/to/diagram.puml)`.

### 6.1. Quy chuẩn Thư mục Lưu trữ: Sơ đồ ra Sơ đồ, Ảnh chụp ra Ảnh chụp
- **`docs/screenshots/`**: 100% CHỈ chứa ảnh chụp màn hình UI thực tế của phần mềm (`01_tong_quan_giao_dien.png`, `02_...png`). Tuyệt đối CẤM để sơ đồ hoặc file `.puml`/`.dot` vào đây.
- **`docs/diagrams/`**: Chứa toàn bộ mã nguồn vector (`.dot`, `.puml`, `.tldr`) và file xuất vector/raster (`.svg`, `.png`).
- **`docs/tools/` hoặc `tools/`**: Toàn bộ script hỗ trợ (render, audit, convert) phải nằm trong thư mục công cụ, CẤM rải rác ở thư mục gốc dự án.

---

## 7. TOOLCHAIN KIỂM ĐỊNH TỰ ĐỘNG

**Giới hạn static audit phải nói rõ:** script mặc định quét đệ quy các SVG, FAIL nếu scope không có SVG, kiểm tra cặp PNG và yêu cầu có nguồn chỉnh sửa được cùng tên (.py generator, .puml, .dot, .drawio, .tldr, .mmd, .json). Dùng --top-level-only khi cần giới hạn đúng một thư mục. Các cảnh báo class graph (hub, association song song, density, nhiều hidden constraints) chỉ là tín hiệu để reviewer soi ảnh; chúng không chứng minh sơ đồ có hay không có giao cắt. Script hiện kiểm tra xấp xỉ một số điểm/path vertex trong bounding box chữ, **không** phải bộ giải hình học đầy đủ để phát hiện tất cả giao cắt giữa hai path hoặc va chạm node-edge. Vì vậy static pass ≠ Visual PASS, và tuyệt đối không gọi đây là "100% thẩm mỹ". **Với Use Case, cổng bố cục (đường nối có đè? khoảng cách có đều? nhìn có dễ?) do MẮT SOI ẢNH quyết định — KHÔNG giao cho script** (xem `use-case-layout` Bước 4).

Chạy script kiểm định tích hợp:

```bash
# Kiểm tra toàn bộ thư mục export sơ đồ (mặc định BẬT luật zero-color)
node .claude/skills/diagram-auditor/scripts/audit-diagrams.mjs <duong-dan-thu-muc>

# Chỉ dùng khi có ghi đè tường minh override-monochrome: true
node .claude/skills/diagram-auditor/scripts/audit-diagrams.mjs <duong-dan-thu-muc> --allow-color
```

- **Lỗi ĐỎ (`FAIL`)** chặn cứng: banner compiler, SVG hỏng, thiếu PNG, `title` nhúng, nhãn ERD trên Crow's foot, quan hệ trùng, đè chữ, đường cắt chữ, **màu phi thang độ xám**, **cỡ chữ < 9pt**, tỷ lệ khung ngoài 0.5–2.4.
- **Cảnh báo VÀNG (advisory)** không chặn CI nhưng Agent **phải phân xử bằng mắt**: trọng tâm lệch, cụm dồn cục, tổng số nhãn lớn (gợi ý phân rã).

---

## ⚡ PROMPT BẮT BUỘC KHI GỌI SKILL NÀY (COPY VÀO PROMPT AGENT)

> **KHI BẠN ĐƯỢC YÊU CẦU AUDIT SƠ ĐỒ, BẮT BUỘC THỰC HIỆN ĐÚNG 5 CỔNG NGHIỆM THU — KHÔNG GỘP, KHÔNG BỎ QUA:**
>
> **PASS = ĐIỀU KIỆN 1 (MÁY) + ĐIỀU KIỆN 2 (MẮT). THIẾU MỘT = FAIL.** ĐK1: script 0 lỗi đỏ **+ file nguồn (.py generator / .puml / .dot) TỒN TẠI + file ảnh (.png + .svg) TỒN TẠI >500B**. ĐK2: Agent soi ảnh thật, **≥3 nhãn nguyên văn + vị trí + câu kết luận "sắp xếp đã hợp lý chưa"**.
>
> 1. **GATE 0 — KIỂM TRA BƯỚC 0:** Nếu sơ đồ Use Case/Domain → kiểm tra `docs/domain/step0-<du-an>.md` tồn tại + có bằng chứng từng trách nhiệm (`[REQ-xx]`, `[code:file:line]`, `[user-confirmed]`). **Thiếu = BLOCKED**, báo: `⚠️ VI PHẠM KỶ LUẬT: thiếu Bước 0 — lỗi tư duy mô hình hóa.`
> 2. **RENDER VALIDATION (ĐK1):** Chạy script audit, phải 0 lỗi ĐỎ. **File nguồn (.py/.puml/.dot) tồn tại + File PNG+SVG tồn tại >500 bytes**, không banner, không title nhúng, zero-color pass, font ≥9pt, aspect ratio 0.5–2.4.
> 3. **VISION AUDIT — PROOF-OF-VIEW (ĐK2 = VISION, BẮT BUỘC):** **BẮT BUỘC model có VISION soi ảnh** (ảnh `.png` vào thẳng ngữ cảnh model qua `tools.browser.preview` / đọc file ảnh / vision subagent; model text-only **không tính**). Mở PNG vào ngữ cảnh model, ghi **4 mục + Vision audit by**:
>    - ≥ 3 nhãn đọc được nguyên văn + vị trí
>    - Vị trí khối chính
>    - Danh sách lỗi/không lỗi cho 13 tiêu chí + **câu kết luận: "SẮP XẾP HỢP LÝ" hay "CHƯA HỢP LÝ (do X)"**
>    - SHA256 file + dung lượng + thời gian render
>    - **`Vision audit by: <model-id>`** (nếu model hiện tại không có vision → giao vision subagent/model; không có vision nào → `BLOCKED — Vision Audit unavailable`)
>    **Thiếu 1 mục = KHÔNG PASS** (tối đa PASS WITH CONDITIONS hoặc BLOCKED).
> 4. **SEMANTIC REVIEW (CỔNG A):** Đối chiếu mô hình với schema DB / code thật / kiến trúc. Không nhảy tầng (UI→Store), đúng PK/FK, đúng tên class/bảng. **Thiếu Bước 0 = FAIL nghiệp vụ dù hình đẹp.**
> 5. **DOCX RENDERED-PAGE INSPECTION:** Kiểm tra hình trong Word A4 (rộng 14–15.5cm, căn giữa, khớp caption `Hình X.Y`, có `keep_with_next`).
>
> **BÁO CÁO PHẢI TRÌNH BÀY RIÊNG 5 KẾT QUẢ** — cấm gộp thành 1 PASS duy nhất.
>
> **ADVERSARIAL REVIEWER MINDSET:** Bạn là người **chủ động tìm lỗi để bác bỏ**, không phải người tìm cách PASS. Hãy hỏi: *"Đâu là 3 lỗi tôi có thể tìm ra để FAIL sơ đồ này?"* Nếu không tìm được → PASS.
>
> **ZERO CODE DUMPS:** Chỉ hiển thị ảnh `![Hình X.Y](path)`, caption, báo cáo 5 cổng, câu hỏi nghiệm thu user, link `.puml`. **CẤM xả code nguồn ra chat.**
>
> **KHI THIẾU CÔNG CỤ XEM ẢNH:** Báo `BLOCKED — Visual QA unavailable`. Tuyệt đối không đoán mò.
