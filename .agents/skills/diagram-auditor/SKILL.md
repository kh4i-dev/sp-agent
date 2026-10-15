---
name: diagram-auditor
description: Audit và kiểm định chất lượng sơ đồ kỹ thuật (PlantUML, Graphviz DOT, tldraw, SVG, PNG) trước khi gửi hoặc chèn vào báo cáo Word. Chặn hội chứng False PASS (script 0 lỗi nhưng mắt thấy FAIL: đè nhãn, dồn cục, méo lệch). Bắt buộc Visual QA: đưa ảnh PNG vào ngữ cảnh model + LUẬT BẰNG CHỨNG SOI ẢNH (trích ≥3 nhãn nguyên văn + vị trí + dấu vết file). Áp ZERO-COLOR (chỉ thang độ xám, cấm mọi mã màu kể cả khi ảnh mẫu có màu) và cổng bố cục đẹp (chữ ≥9pt, tỷ lệ khung 0.5–2.4, chống node mồ côi/dồn cục/lệch trọng tâm). GATE 0: bắt buộc file Bước 0 đã xác minh bằng bằng chứng (chưa rõ ghi UNKNOWN). Hai cổng tách biệt — Semantic Review (nghiệp vụ/UML) vs Visual Review (hình học): thiếu Bước 0 = FAIL nghiệp vụ dù hình đẹp; cấm căn chỉnh bố cục che lỗi mô hình. Báo cáo 5 kết quả độc lập.
---

# Diagram Auditor Skill — Cổng Kiểm Định Chất Lượng Sơ Đồ & Visual QA Thực Tế

Mục tiêu: Đảm bảo **100% sơ đồ xuất bản** đạt chuẩn kỹ thuật và thẩm mỹ in ấn học thuật cao cấp. Chặn đứng tận gốc tình trạng **"Script báo PASS nhưng mắt nhìn thấy FAIL"** — tức là file render được không lỗi cú pháp nhưng bố cục chật chội, nhãn đè nhau, khoảng trắng bất hợp lý, hoặc nhầm lẫn hình ảnh trong tài liệu.

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

## 2. QUY CHUẨN BẮT BUỘC: VISUAL QA — IMAGE MUST ACTUALLY BE VIEWED

> [!CAUTION]
> **LUẬT BẰNG CHỨNG SOI ẢNH (PROOF-OF-VIEW) — KHÔNG CÓ BẰNG CHỨNG THÌ KHÔNG PHẢI PASS.**
> Việc "đã mở ảnh" là vô nghĩa nếu không để lại **bằng chứng quan sát cụ thể**. Agent BẮT BUỘC ghi lại:
> 1. **≥ 3 nhãn/chữ đọc được nguyên văn** từ chính ảnh PNG (không lấy từ file `.puml`).
> 2. **Vị trí tương đối** các khối chính (ví dụ: "Actor Khách ở cột trái, hàng giữa").
> 3. **Danh sách lỗi phát hiện hoặc xác nhận "không lỗi"** cho từng mục trong Danh mục lỗi bắt buộc (Mục 2, điểm 5) và 13 tiêu chí bố cục đẹp.
> 4. **Mã băm / dấu vết của đúng file đã soi** (tên file + dung lượng + thời điểm render) để chứng minh đã soi ảnh *sau* lần render cuối, không soi ảnh cũ.
> Không có 4 mục bằng chứng này → trạng thái **KHÔNG THỂ là PASS** (tối đa `PASS WITH CONDITIONS` hoặc `BLOCKED`).

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

1. **Render validation:** File PNG & SVG tồn tại trên đĩa, không rỗng (> 500 bytes), biên dịch sạch sẽ không có banner cảnh báo compiler (`Please use...`, `Warning`), và SVG **không chứa mã màu phi thang độ xám**.
2. **Automated audit:** Kết quả từ script `audit-diagrams.mjs` (0 lỗi ĐỎ): không va chạm tọa độ chữ, không đường cắt ngang chữ, không nhãn trên Crow's foot ERD, **màu grayscale đạt luật zero-color**, **cỡ chữ nhỏ nhất ≥ 9pt**, tỷ lệ aspect ratio hợp lý (0.5–2.4). Các cảnh báo VÀNG phải được Agent phân xử.
3. **Actual visual inspection:** Kết quả từ việc Agent trực tiếp mở ảnh PNG bằng công cụ xem ảnh vào ngữ cảnh model, **kèm bằng chứng soi ảnh ở Mục 2** (soi nét chữ thông thoáng, không chen chúc nhãn giữa các tầng, bố cục cân đối không lệch dồn cục, không node mồ côi, luồng rõ ràng, đạt 13 tiêu chí bố cục đẹp).
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

**Giới hạn static audit phải nói rõ:** script mặc định quét đệ quy các SVG, FAIL nếu scope không có SVG, kiểm tra cặp PNG và yêu cầu có nguồn chỉnh sửa được cùng tên (.puml/.dot/.drawio/.tldr/.mmd/.json). Dùng --top-level-only khi cần giới hạn đúng một thư mục. Các cảnh báo class graph (hub, association song song, density, nhiều hidden constraints) chỉ là tín hiệu để reviewer soi ảnh; chúng không chứng minh sơ đồ có hay không có giao cắt. Script hiện kiểm tra xấp xỉ một số điểm/path vertex trong bounding box chữ, **không** phải bộ giải hình học đầy đủ để phát hiện tất cả giao cắt giữa hai path hoặc va chạm node-edge. Vì vậy static pass ≠ Visual PASS, và tuyệt đối không gọi đây là “100% thẩm mỹ”.

Chạy script kiểm định tích hợp:

```bash
# Kiểm tra toàn bộ thư mục export sơ đồ (mặc định BẬT luật zero-color)
node .claude/skills/diagram-auditor/scripts/audit-diagrams.mjs <duong-dan-thu-muc>

# Chỉ dùng khi có ghi đè tường minh override-monochrome: true
node .claude/skills/diagram-auditor/scripts/audit-diagrams.mjs <duong-dan-thu-muc> --allow-color
```

- **Lỗi ĐỎ (`FAIL`)** chặn cứng: banner compiler, SVG hỏng, thiếu PNG, `title` nhúng, nhãn ERD trên Crow's foot, quan hệ trùng, đè chữ, đường cắt chữ, **màu phi thang độ xám**, **cỡ chữ < 9pt**, tỷ lệ khung ngoài 0.5–2.4.
- **Cảnh báo VÀNG (advisory)** không chặn CI nhưng Agent **phải phân xử bằng mắt**: trọng tâm lệch, cụm dồn cục, tổng số nhãn lớn (gợi ý phân rã).
