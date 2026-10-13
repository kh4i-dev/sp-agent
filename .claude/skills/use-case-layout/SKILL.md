---
name: use-case-layout
description: "Thiết kế Use Case Diagram UML vừa ĐÚNG nghiệp vụ vừa GỌN - ĐẸP - DỄ NHÌN: mô hình hóa, lập bố cục lane có chủ đích, vẽ tay/draw.io hoặc PlantUML, render và audit. Luật cứng: không xác định bài toán/tác nhân (Bước 0) thì cấm vẽ; CẤM connector VÒNG XA dài ngoằng — connector phải ngắn và trực tiếp, gặp đường phải đi vòng thì DI CHUYỂN NODE chứ không vẽ vòng; chuyển sang draw.io thủ công khi auto-layout không sạch. Dùng khi cần vẽ use case, bố cục use case cân đối, đường nối use case sạch, sơ đồ use case dễ đọc, tránh dây rối/vòng xa."
---

# Skill: Thiết kế Use Case Diagram đúng nghiệp vụ, bố cục cân đối, đường nối sạch

## 1. Mục tiêu

Tạo sơ đồ Use Case UML vừa **đúng mô hình nghiệp vụ**, vừa **dễ đọc khi in A4 hoặc chèn vào Word**. Ưu tiên bố trí có chủ đích và kiểm chứng hình render, không chấp nhận sơ đồ tự động sinh ra rồi mặc định là đạt.

Skill này hướng dẫn Agent lập mô hình, chọn bố cục, vẽ bằng công cụ hoặc vẽ tay/draw.io, render và audit. **Không dùng công cụ tạo ảnh để thay cho sơ đồ UML có cấu trúc**: sơ đồ phải sửa được, quan hệ phải kiểm tra được và phải có mã nguồn/tệp gốc.

> [!CAUTION]
> **3 LUẬT THẨM MỸ KHÔNG THƯƠNG LƯỢNG (áp cho MỌI sơ đồ Use Case):**
> 1. **GỌN** — ít giao cắt, khoảng cách đều, nhóm rõ ràng.
> 2. **ĐẸP** — căn chỉnh, nhãn ngắn, ellipse nhất quán.
> 3. **DỄ NHÌN** — đường nối **ngắn và trực tiếp**; **TUYỆT ĐỐI KHÔNG VẼ VÒNG XA** (xem §3.5).

## 2. Luật chặn cứng

> **Không xác định bài toán và tác nhân thì cấm vẽ.**

Trước khi tạo `.puml`, XML draw.io, SVG hoặc sơ đồ ở bất kỳ định dạng nào, bắt buộc tạo và hoàn thiện `docs/diagrams/<ten-so-do>-step0.md` theo mẫu [step0-bai-toan-va-tac-nhan.md](file:///E:/HOC%20TAP/my-project/sp-agent/.claude/skills/use-case-layout/reference/step0-bai-toan-va-tac-nhan.md) (bài toán, quy mô, tác nhân + trách nhiệm **kèm nguồn bằng chứng / UNKNOWN**).

Nếu chưa có file này hoặc thông tin cốt lõi chưa được xác minh:

1. Phát đúng thông báo: `⚠️ VI PHẠM KỶ LUẬT: chưa xác định bài toán/tác nhân (thiếu Bước 0).`
2. Dừng việc vẽ và tối ưu bố cục.
3. Hoàn thành Bước 0; ghi rõ nội dung chưa biết là `UNKNOWN` và yêu cầu xác nhận khi cần. Không tự bịa vai trò để lấp chỗ trống.

Reviewer phải trả `FAIL — lỗi tư duy mô hình hóa, không phải lỗi bố cục` với mọi sơ đồ không có Bước 0 đạt yêu cầu.

## 3. Luồng thực thi bắt buộc

### Bước 0 — Xác định bài toán, quy mô, tác nhân

Tạo file Markdown trước khi tạo bất kỳ sơ đồ nào. Phải làm rõ:

- Vấn đề hiện tại, đối tượng gặp vấn đề và mục tiêu hệ thống.
- Quy mô đã biết: nhóm người dùng/vận hành, tần suất, tải hoặc khối lượng. Nếu không có số liệu thì ghi `UNKNOWN`, không tự ước lượng như dữ kiện.
- Mỗi actor: mục tiêu, trách nhiệm, quyền hạn và điều actor **không** làm.
- Phân biệt người xử lý nghiệp vụ với người sửa lỗi kỹ thuật; người kiểm duyệt với quản trị viên; quản trị tài khoản với vận hành nghiệp vụ.
- Hệ thống nằm trong phạm vi và hệ thống/dịch vụ bên ngoài nằm ngoài phạm vi.
- Mức trừu tượng và chiến lược phân rã: sơ đồ tổng quan hay nhiều sơ đồ con. Nếu quá **15 use case trong một hình**, mặc định đề xuất chia nhỏ; chỉ giữ một hình khi có lý do rõ ràng.
- Các giả định, điểm còn thiếu và **nguồn chứng cứ** cho từng quyết định quan trọng.

Không đưa nút bấm, trường nhập liệu, thao tác điều hướng hoặc chi tiết giao diện thành use case độc lập, trừ khi chúng thực sự là mục tiêu nghiệp vụ của actor.

### Bước 1 — Chốt mô hình UML

Từ Bước 0, lập danh sách có kiểm soát:

- Actor và mục tiêu actor. Use case và actor nào khởi tạo/tham gia.
- Ranh giới hệ thống. Quan hệ association, `<<include>>`, `<<extend>>` và generalization nếu có căn cứ.
- Các luồng nghiệp vụ chính, ngoại lệ và quyền hạn ảnh hưởng đến sơ đồ.

Quy tắc quan hệ:

- Association là đường liền giữa actor và use case; **không vẽ mũi tên** nếu không có quy ước cụ thể cần thể hiện.
- `<<include>>` dùng khi use case cơ sở **luôn** gọi hành vi dùng chung bắt buộc; mũi tên nét đứt hướng **về use case được include**.
- `<<extend>>` dùng cho hành vi mở rộng **có điều kiện**; mũi tên nét đứt hướng **về use case cơ sở được mở rộng**.
- Generalization dùng khi thật sự có quan hệ kế thừa actor/use case; tam giác rỗng hướng về phần tử tổng quát.
- **Không thêm quan hệ để sơ đồ "trông giống UML mẫu".** Nếu quan hệ khó giải thích bằng một câu nghiệp vụ rõ ràng → bỏ hoặc xác minh lại.
- Use case đặt tên theo mục tiêu/hành động nghiệp vụ, ngắn, nhất quán, không mô tả thao tác UI.

Lưu file mô hình hoặc bảng traceability trước khi bố trí hình. **Không thay đổi ý nghĩa nghiệp vụ chỉ để làm đường nối đẹp hơn.**

### Bước 2 — Chọn bố cục trước khi vẽ đường nối

#### 2.1 Phân vùng

- Vẽ **system boundary trước**; tên hệ thống đặt ở mép trên bên trong khung.
- Nhóm use case theo chức năng hoặc mục tiêu actor bằng `package`, vùng hoặc khung nhóm. Không nhóm chỉ theo vị trí tiện lợi.
- Actor chính/khởi tạo luồng **thường đặt bên trái**; actor hỗ trợ, dịch vụ bên ngoài **thường đặt bên phải**. Mặc định, không tuyệt đối: nếu luồng nghiệp vụ yêu cầu khác, ghi lý do.
- Nếu nhiều actor, chia theo nhóm vai trò ở hai bên; không xếp mọi actor thành một cụm trên một cạnh.
- Actor **không được đè** lên system boundary, package hoặc use case. Tên actor gần actor và không bị đường nối xuyên qua.
- Use case cùng nhóm xếp thành cột/hàng **khoảng cách đều**; ưu tiên căn tâm và ellipse kích thước nhất quán.
- Tránh đặt use case "nhiều kết nối" ở vị trí khiến mọi đường phải xuyên qua use case khác.

#### 2.2 Lập bảng layout TRƯỚC khi nối dây

Tạo bảng với ít nhất: `element_id`, `label`, `group`, `side/lane`, `row`, `connected_actors`, `relationship_edges`. **Chọn vị trí actor và use case trước, rồi mới vẽ cạnh.**

Dùng các lane khái niệm:

- **Lane L:** actor/nhóm actor bên trái.
- **Lane C-L / C-R:** nhóm use case bên trong hệ thống.
- **Lane R:** actor phụ hoặc hệ thống ngoài.
- **Lane R-REL:** vùng dành cho quan hệ nét đứt (`include/extend`) nếu thật cần.

> [!IMPORTANT]
> **Đặt cặp use case có quan hệ `include/extend` Ở GẦN NHAU (ngang hàng hoặc liền kề) ngay từ bước lập bảng layout** — đây là cách phòng ngừa vòng xa hiệu quả nhất. Nếu base và target phải nối mà ở xa nhau → **đổi `row`/`lane` cho chúng gần lại** trước khi vẽ.

### Bước 3 — Đi dây để giảm giao cắt

#### 3.1 Thứ tự nối

1. Nối **association** chính của từng actor tới use case **gần nhất**.
2. Nối association ít cạnh tranh hơn.
3. Nối `include`, `extend`, generalization **sau cùng**.
4. Đặt **nhãn quan hệ sau khi hình học đã ổn định**.

#### 3.2 Quy tắc hình học

- Ưu tiên đường **ngắn, thẳng, dễ lần theo**.
- Hạn chế giao cắt; **cấm đường nối xuyên qua ellipse/use case, tên actor hoặc nhãn quan hệ**.
- Không chạy đường nối qua nội dung trong package để tới phần tử phía bên kia.
- Không để connector trùng khít tới mức không phân biệt được cạnh nào tới use case nào.
- Với đường chéo sẽ đâm xuyên thành phần: dùng connector **orthogonal/elbow**. Chỉ bẻ góc khi nó **thực sự làm đường rõ hơn**; không bẻ quá nhiều thành mê cung.
- Khi nhiều cạnh giao nhau, **ĐỔI VỊ TRÍ NODE TRƯỚC**, không lập tức thêm hàng loạt điểm gấp.
- Actor liên kết nhiều use case → đặt actor ngang **vùng trung tâm** của cụm use case liên quan; sắp use case theo thứ tự luồng/nhóm để các cạnh tỏa gọn.
- Nhiều actor liên kết cùng một use case → đặt use case gần ranh giới giữa nhóm liên quan (vẫn trong đúng package).
- Nhãn use case **ngắn, lý tưởng 1 dòng, ≤ 25 ký tự**; nếu bắt buộc dài hơn → đổi cách diễn đạt hoặc phân rã, **không bóp méo ellipse để nhét chữ**.
- `nodesep`/`ranksep` chỉ là **tham số khởi đầu**, KHÔNG phải bằng chứng hình đã đẹp. Điều chỉnh theo **bản render** và kích thước in thực tế.

#### 3.3 Quy tắc khi dùng PlantUML

- Bố trí logic theo nhóm và lane; alias ổn định; dùng `left/right` hoặc liên kết ẩn **chỉ khi thực sự** giúp ổn định thứ tự.
- **Không tạo liên kết nghiệp vụ giả chỉ để điều khiển layout.**
- Không giả định PlantUML cho ra vị trí đúng nhờ `left to right direction`, `nodesep` hay `ranksep`.
- Nếu PlantUML **vẫn sinh connector chồng chéo/vòng xa sau vài lần chỉnh hợp lý** → **chuyển sang draw.io** để định vị thủ công (giữ nguyên mô hình UML đã duyệt). Đừng vá mã vô hạn.

#### 3.4 Quy tắc khi vẽ tay / draw.io

- Đặt system boundary, vùng chức năng, ellipse và actor **trước**; kiểm khoảng trống rồi mới nối dây.
- Dùng grid/snap và căn chỉnh; cùng hàng/cột thì căn tâm/mép nhất quán.
- Connector endpoint đặt **đúng** vào actor/use case; không để đường kết thúc lơ lửng hoặc chạm sai phần tử.
- **Di chuyển ellipse để giải quyết giao cắt**; không kéo actor ra ngoài ranh giới theo cách gây hiểu nhầm actor thuộc hệ thống.
- Bật/tắt điểm bẻ connector **có chủ đích**; không để các đường cùng loại quan hệ có hình thức khác nhau ngẫu nhiên.
- **Lưu tệp gốc chỉnh sửa được** (`.drawio`, `.puml`…); PNG chỉ là **sản phẩm render**, không phải nguồn duy nhất.

#### 3.5 CẤM VÒNG XA (NO FAR LOOPS) — luật hình học quan trọng nhất

> [!CAUTION]
> **KHÔNG BAO GIỜ kéo connector vòng qua mép canvas (trái/phải/trên/dưới) rồi quay ngược lại để tới đích.**
> Một đường `<<include>>`/`<<extend>>`/association đi một vòng dài ngoằng là **dấu hiệu SAI BỐ CỤC**, không phải vấn đề nét vẽ.

Quy tắc bắt buộc:

1. **Connector phải NGẮN và TRỰC TIẾP.** Chiều dài đường nối không được vượt quá vài lần khoảng cách thẳng giữa hai đầu.
2. Gặp một quan hệ buộc phải đi vòng xa → **DI CHUYỂN NODE** (đưa use case nguồn và đích lại gần nhau, đổi `row`/`lane`/thứ tự khai báo), **KHÔNG kéo dây vòng qua canvas**.
3. Không dùng "ống dẫn" vòng mép phải để gom nhiều `include/extend` rồi túa ngược về bên trái. Đây là anti-pattern của sơ đồ trong ảnh mẫu lỗi.
4. Nếu hai nhóm buộc liên hệ mà ở xa: **gộp nhóm lại** hoặc **phân rã thành sơ đồ con** — không bắc cầu vòng.
5. Mọi connector còn lại phải **lần theo được** và không gây nhầm cạnh; nếu không lần được → sửa bố cục, không thêm điểm gấp.

### Bước 4 — Render, kiểm tra A4 và nghiệm thu

Xuất ít nhất **PNG** để soi hình, và **SVG/PDF** nếu quy trình báo cáo yêu cầu. **Không kết luận đạt chỉ dựa vào mã nguồn.**

Kiểm tra ở hai mức:

**Semantic Review — đúng nghiệp vụ/UML**

- Có file Bước 0 và đã được xem xét.
- Tác nhân khớp vai trò được xác minh.
- Mỗi use case thể hiện mục tiêu actor, không phải thao tác UI vụn vặt.
- Ranh giới hệ thống đúng.
- Hướng quan hệ `include/extend/generalization` đúng.
- Không có actor, use case hoặc quan hệ tự thêm chỉ để trang trí/bố trí.

**Visual Review — đúng hình học/trình bày**

- **Không có connector VÒNG XA / dài ngoằng** (vi phạm §3.5 → FAIL ngay).
- Không có đường nối xuyên qua ellipse, chữ, actor hoặc nhãn.
- Không có node/nhãn bị cắt, chồng nhau hoặc ngoài trang.
- Actor không chồng lên system boundary; phân biệt rõ tác nhân trong/ngoài.
- Các ellipse cùng nhóm **căn chỉnh, khoảng cách nhất quán**.
- Giao cắt ở mức tối thiểu; mọi giao cắt còn lại **lần theo được**.
- Nhãn `include/extend` gắn rõ với đúng quan hệ.
- Tỷ lệ ~15 cm/A4 vẫn đọc được; nếu chữ quá nhỏ → **phân rã sơ đồ**, không ép lên một trang.
- Kiểm ở **100% zoom lẫn bản xem như in/chèn Word**.
- Chạy `node .claude/skills/diagram-auditor/scripts/audit-diagrams.mjs <thư-mục>`; lưu kết quả. Nếu không có script → ghi `NOT RUN` và tự làm checklist thủ công.

### Cổng nghiệm thu

Chỉ ghi `PASS` khi **cả hai** cổng Semantic Review và Visual Review đều đạt.

- Thiếu Bước 0 → `FAIL — lỗi tư duy mô hình hóa, không phải lỗi bố cục`.
- Mô hình đúng nhưng hình chưa rõ (gồm cả vòng xa) → `BLOCKED — Visual Review`; sửa layout rồi render lại.
- Hình đẹp nhưng nghiệp vụ/UML sai → `FAIL — Semantic Review`; quay lại Bước 0/1, **không chỉnh hình để che lỗi**.
- Không mở/soi được ảnh render → **không được tuyên bố đã hoàn tất Proof-of-View**.

## 4. Đầu ra bắt buộc

Tùy cấu trúc repo, tạo/cập nhật tối thiểu:

1. `docs/diagrams/<name>-step0.md` — bài toán, quy mô, actor, phạm vi, UNKNOWN và nguồn xác minh.
2. `docs/diagrams/<name>-model.md` — actor/use case/quan hệ + giải thích quyết định UML.
3. Tệp nguồn chỉnh sửa được: `.puml`, `.drawio` hoặc tương đương.
4. Bản render **PNG**; SVG/PDF nếu phù hợp.
5. `docs/diagrams/<name>-audit.md` — kết quả Semantic + Visual Review, lệnh render/audit đã chạy, phát hiện còn tồn tại, trạng thái PASS/FAIL.

Không ghi "đã chạy" cho lệnh chưa chạy, không ghi "đã nhìn ảnh" nếu chưa mở ảnh, không tự gắn PASS khi còn mục bắt buộc chưa xác minh.

## 5. Cách làm việc với repository

1. Đọc hướng dẫn repo và tài liệu nghiệp vụ liên quan trước khi sửa.
2. Kiểm tra file đích đã tồn tại chưa; **không ghi đè tài liệu hiện có một cách im lặng**.
3. Không sửa SSOT nghiệp vụ chỉ để thuận tiện vẽ. Gặp mâu thuẫn → ghi finding và **dừng phần bị ảnh hưởng** để xác minh.
4. Thay đổi nhỏ, truy vết được; bảo toàn bản nguồn; tránh xóa/commit tự động.
5. Sau render, **mở ảnh thật** để xem connector, chữ và bố cục. Chỉnh theo **bằng chứng từ ảnh**, không suy đoán từ mã.
6. Báo cáo cuối theo mẫu:

```text
Status: PASS | FAIL | BLOCKED
Step 0: <path> — VERIFIED | MISSING | INCOMPLETE
Semantic Review: PASS | FAIL
Visual Review: PASS | FAIL | NOT RUN   (đã kiểm vòng xa? YES/NO)
Source diagram: <path>
Rendered image: <path>
Automated audit: <command/result or NOT RUN>
Changed: <files changed>
Findings: <remaining issues>
Limitations: <known limitations>
```

## 6. Chỉ thị ngắn cho Agent

> Đừng bắt đầu bằng cách viết sơ đồ. Đọc yêu cầu và repo → tạo, hoàn thiện và kiểm tra file **Bước 0** → chốt **mô hình UML** → lập **layout lane** (đặt cặp include/extend **gần nhau**) → **đặt node trước rồi nối dây** → render và **mở ảnh** → kiểm **cả semantic lẫn visual** → chỉ PASS khi có bằng chứng.
> **Ưu tiên đổi vị trí node trước khi bẻ đường nối. Không để đường nối xuyên ellipse. VÀ TUYỆT ĐỐI KHÔNG BAO GIỜ VẼ VÒNG XA.** Nếu auto-layout không đạt bố cục sạch → chuyển sang công cụ định vị thủ công (draw.io) thay vì vá mã vô hạn.
