# Tư duy bố cục cho AI (Layout Thinking) — SSOT

> **Vị trí:** `diagram-orchestrator/reference/layout-thinking.md` là **SSOT cho cách NGHĨ trước khi vẽ**.
> Các skill (`plantuml-diagrams` Beautify Loop, `use-case-layout` lập lane, `tldraw-diagrams`,
> `simplified-diagrams`, `diagram-auditor` Visual Review) defer về đây, không diễn giải lại.
> Quy tắc này sinh ra từ lỗi thật: node xếp theo thứ tự khai báo → cạnh bay vòng quanh hình,
> nhãn cụt không dấu, thiếu đường quan hệ, nửa khung bỏ trống.

## 0. Nguyên tắc mẹ: topology trước, tọa độ sau

Auto-layout (PlantUML/Graphviz) chỉ tối ưu cục bộ theo **thứ tự khai báo**.
Phần việc của kiến trúc sư — quyết định **ai Ở GẦN ai** — AI phải làm **trước khi viết
một dòng code**, bằng 6 bước dưới đây. Không bước nào được bỏ qua bằng cảm tính
("nhìn là biết", "render ra rồi tính").

## 1. Tiền-bố-cục bắt buộc (Adjacency-first)

Trước khi viết `.puml`/`.drawio`, lập bảng 3 cột (giấy nháp hoặc `<name>-model.md`):

| Quan hệ (A — B) | Bắt-buộc-ngắn? | Zone dự kiến |
|---|---|---|
| VD: USER — CONNECTION_REQUEST (FK senderId) | CÓ | trái — giữa |

Quy tắc điền bảng:
1. **ERD: mỗi FK trong schema = đúng một dòng.** FK nào không có đường trên hình
   là **thiếu sót ngữ nghĩa** (case thật: `TUTOR_PROFILE.userId → USER` có trong schema
   nhưng hình không vẽ). Đếm FK trước, đếm đường sau, hai số phải khớp.
2. **Class: mỗi association = một dòng**, ghi kèm degree hai đầu; node degree ≥ 5 là hub.
3. **Use Case: mỗi cặp actor–usecase và include/extend = một dòng** (khớp lane L/C/R).
4. Cột "bắt-buộc-ngắn": quan hệ lõi luồng chính + mọi quan hệ của hub = CÓ.
5. Xếp zone sao cho các dòng CÓ nằm cùng/kề zone. **Thứ tự khai báo trong code = thứ tự
   zone** (trái→phải / trên→dưới). Hub đặt ở **trung tâm vùng liên quan**, cấm đẩy ra góc.
6. Chỉ sau khi bảng xong mới được viết code. Đổi zone sau này = quay lại sửa bảng.

> **Bằng chứng vòng lặp (PlantUML qua Kroki, ERD 6 bảng, đã render + soi):** đổi thứ tự
> khai báo + hidden-link khóa rank KHÔNG giữ được rank dự kiến khi cạnh ngữ nghĩa kéo
> mạnh — engine tự xếp zigzag, bỏ qua lock (v2→v3 không tiến triển, điểm đứng yên).
> Kết luận: mọi cơ chế khóa rank (thứ tự khai báo, hidden-link, together) chỉ là
> **gợi ý yếu**. Quy tắc dừng: **1 lần thử khóa** → render → rank không giữ thì CẤM thử
> cơ chế khóa thứ hai; phân rã hoặc vẽ tay ngay (manual-fallback Lối B).
> Vá tham số vô hạn chính là bệnh mà skill này chữa — kể cả khi người vá là AI làm theo skill.

## 2. Trục luồng cho Deployment/Kiến trúc (flow-axis)

1. Liệt kê luồng dữ liệu/request theo thứ tự chạy thật
   (VD: Browser → Cloudflare → Tunnel → Frontend → Backend → DB).
2. Đặt các node con **dọc trục luồng**, không xếp chồng một phía.
3. Container phải **ôm sát con**: void bên trong một node > 25% diện tích = sai bố cục
   (case thật: hộp VM rỗng ~40% góc trên-trái). Rỗng thì thu hẹp/kéo con ra, không để hộp thừa.
4. Nhãn luồng đặt **trên đoạn cạnh ngắn**, cấm thả nhãn giữa khoảng trống.

> **Bằng chứng vòng lặp (deployment, hint `FE -right-> BE`, đã render + soi):** hint hướng
> chỉ đổi phía ra của cạnh, KHÔNG đảm bảo hai node con nằm ngang hàng — v1 thành chuỗi
> dọc (cạnh ngắn lại nhưng void nửa hộp còn nguyên). Quy tắc: sau mỗi hint, kiểm bằng
> render; chuỗi dọc cạnh ngắn, không giao cắt = PASS WITH CONDITIONS chấp nhận được;
> muốn ngang hàng thật thì vẽ tay. Cấm ghi "đã căn ngang" khi chưa soi ảnh.

## 3. Ngân sách cạnh + test 4 góc (chống dồn một bên)

Sau render, kiểm tra bằng mắt, không đoán từ code:
1. **Ngân sách cạnh:** không cạnh nào dài quá **2.5× trung vị**; không cạnh nào xuyên qua
   **> 1 node/entity không liên quan**. Cạnh `USER→MESSAGE` chạy ngang đỉnh toàn hình
   hay `User→Participant` vòng chữ U quanh hình đều là FAIL bố cục.
2. **Test 4 góc phần tư:** chia khung thành 4; góc nào < 10% mực, hoặc một nửa khung chứa
   > 75% node → **chia lại zone** (quay về §1), không vá bằng tham số.
3. Sửa luôn bằng **DI CHUYỂN NODE** (đưa hai đầu lại gần nhau). Cấm kéo dây vòng,
   cấm nối dài để "né" (xem `use-case-layout` §3.5 NO FAR LOOPS).

## 4. Ngân sách nhãn + toàn vẹn tiếng Việt

1. Mỗi cạnh **1 nhãn nghĩa + multiplicity ở hai đầu**; các cạnh song song phải **so le**
   vị trí nhãn (case thật: `receives`/`sends` đè nhau ở dải giữa; `opens` + `0..1` dồn cục).
2. **Dấu tiếng Việt là NỘI DUNG, không phải trang trí.** Cấm viết nhãn cụt không dấu
   (`gui`, `nhan`, `chua`, `gom`) hay cắt từ để vừa render. Chuỗi font phải hỗ trợ VN:
   `"Segoe UI", Arial, "DejaVu Sans", sans-serif`.
3. Glyph vỡ (ô vuông/tofu) → **đổi font**, không bao giờ sửa chữ. Nhãn ≤ 25 ký tự,
   viết lại câu cho ngắn thay vì cụt từ.
4. Nhãn cấm đè lên đường/box khác; multiplicity đặt sát đúng đầu mút của mình.

## 5. Sàn khoảng cách (spacing floor)

`nodesep`/`ranksep` tối thiểu trong skill là **SÀN, không phải gợi ý**
(PlantUML chi tiết: 60–80 / 60–90). Không vừa trang A4 → **phân rã sơ đồ**,
tuyệt đối cấm nén spacing xuống dưới sàn để nhét (case thật: `nodesep 30/ranksep 45`
là nguyên nhân trực tiếp gây đè nhãn).
Ngoại lệ duy nhất: ERD không nhãn động từ được dùng rank hẹp 40–50 (xem §9.4).

## 9. ERD gọn như ảnh mẫu (reference-style ERD)

> Ground truth thị giác: 4 ảnh ERD mẫu do người dùng cung cấp (kiểu Sakila/MySQL,
> Lucidchart, Thinnotes, dbdiagram) + vòng lặp gen v1→v4 đã render + soi từng ảnh
> (điểm checklist: cũ 0.5 → v1 3.5 → v2 4.5 → v3 4.0 dừng → v4 5/6).

1. **Cột cụm theo FK, hub đặt giữa.** Xếp bảng thành cột sao cho mọi FK nối sang cột
   kề; hub (degree cao nhất) vào cột giữa (kiểu bảng Account ở giữa của Thinnotes).
   Cạnh xa nhất ≤ 1 cột. [S2]#2,#3,#5 + [S1](n),(ev).
2. **Cạnh kề + trực giao + chân quạ thay lời.** Mọi quan hệ đi ngang/dọc tới bảng kề,
   tối đa 1–2 gãy. [S1](o),(b) + [S3]#3 (phạm vi sơ đồ UML kỹ thuật).
3. **Mặc định KHÔNG nhãn động từ trên đường ERD.** Chân quạ + multiplicity đã đủ ngữ
   nghĩa — cả 4 ảnh mẫu đều không ghi verb. [S3]#14 (chỉ vẽ cái cần). Nếu hội đồng yêu
   cầu diễn giải tiếng Việt → lập **bảng companion** (Bảng X.Y: diễn giải quan hệ) trong
   Word, cấm viết lên đường. Quy tắc này triệt tiêu cả lớp lỗi nhãn cụt/đè/dấu
   (`gui/nhan/chua`).
4. **Mật độ tương đối.** Không nhãn trên đường → ranksep/nodesep 40–50 được phép
   (ảnh mẫu đều đặc mà vẫn đọc được). Có nhãn → giữ sàn 60+. [S3]#10 (khoảng trắng
   để ĐẶT nhãn — không nhãn thì không cần nhiều).
5. **ERD rộng đi trang ngang.** 5 cột ở 300 DPI ≈ 35cm > khổ A4 dọc (15cm). Quy tắc:
   ERD > 4 cột hoặc > 8 bảng → trang landscape trong Word, hoặc tách theo miền
   (identity/connection/trust). [S3]#17 + [S1](n) (vừa khung hình).
6. **Bằng chứng vòng lặp.** Bước nhảy điểm lớn nhất (3.5 → 5/6) đến từ §9.2 + §9.3
(bỏ nhãn + cạnh kề), không phải từ cơ chế khóa rank — khớp quy tắc dừng §1
(khóa rank là gợi ý yếu).

## 10. Class gọn như ảnh mẫu (reference-style Class)

> Ground truth thị giác: 5 ảnh Class mẫu do người dùng cung cấp (4 đẹp: Lucid
> Fleet/Vehicle, EdrawMax Restaurant/University/Hotel + 1 phản-ví dụ CodeRanch:
> đường chéo xuyên hộp, chữ li ti, nhét tiêu đề trong canvas) + vòng lặp gen class
> v1→v2 đã render + soi (cũ ~2/6 → v1 ~3.5/6 → v2 không đổi → DỪNG auto theo luật §1).

1. **Hub/top-center, kế thừa con-nằm-dưới.** Lớp nhiều quan hệ nhất (hoặc root phân cấp)
   đặt giữa/trên-giữa (kiểu Vehicle giữa, Staff cột giữa, University trên-giữa,
   Course trung tâm). Lớp con kế thừa nằm DƯỚI lớp cha, mũi tên hướng lên.
   [S2]#1,#5 + ảnh mẫu.
2. **Cột theo miền, rộng đều.** Gom lớp cùng nghiệp vụ thành cột, box cùng cột rộng
   bằng nhau; ≤ 9 lớp/ hình (7±2 Miller [S3]#16); 10–12 lớp chỉ chấp nhận khi cột
   nghiêm + 0 giao cắt, nếu không thì tách overview (tên lớp) + chi tiết.
3. **Trực giao ≤ 1 gãy, nhãn ngắn.** Mọi association đi ngang/dọc, tối đa một khuỷu;
   nhãn = 1 từ EN ngắn (role: sends/opens/includes/is-a/aggregates) + multiplicity ở
   hai đầu; các nhãn song song so le nhau. [S1](o),(b) + [S3]#6 + [S2]#7.
4. **Kênh định tuyến.** Giữ dải trắng giữa các cột cho cạnh đi; cấm cạnh xuyên qua box
   (ảnh CodeRanch là FAIL mẫu: chéo + xuyên + chữ nhỏ).
5. **Tiêu đề ngoài canvas.** Ảnh EdrawMax nhúng title trong hình — quy tắc học thuật giữ
   nguyên: caption `Hình X.Y` ngoài ảnh (zero-title).
6. **Bằng chứng vòng lặp.** Class v1 (lưới 3×2 + hub-center trên giấy) và v2 (khai báo
   lại theo cột + lock khác) render ra **hình học Y HỆT nhau** — engine quyết định bởi
   cấu trúc graph, phớt lờ gợi ý zone. Kết luận: plan lưới/hub-center cho Class là
   **kế hoạch để VẼ TAY (draw.io) hoặc PHÂN RÃ**, không phải để ép auto; auto được
   đúng 1 vòng (đã dùng ở v1), sang vòng 2 không tiến triển thì dừng. Đây là lần thứ
   hai luật dừng §1 được kích hoạt bằng thực nghiệm (sau ERD v2→v3).

## 11. Use Case gọn như ảnh mẫu (reference-style Use Case)

> Ground truth: 6 ảnh — RG enhanced UC (Bolloju), Wikipedia restaurant, Ambler
> seminar/shopping/whiteboard (4 ảnh tự tải về, đã soi từng ảnh) + vòng uc-poc1
> render + soi (cũ ~2/6 → mới ~3.5–4/6).

1. **Quạt ngắn (fan).** Mỗi actor nối chùm đường thẳng NGẮN tới MỘT cột UC kề bên
   (Ambler seminar/whiteboard/shopping). Cột UC của actor nào ở cạnh actor đó.
2. **Actor hai bên, mỗi bên phục vụ cột kề.** Wikipedia: trái Waiter/Client/Cashier +
   phải Chef; shopping: Customer trái + Processor/Support phải; RG: actor 4 phía.
   Cột UC dùng chung đặt giữa.
3. **Cặp include/extend KỀ NHAU, nét đứt NGANG**, nhãn `<<include>>`/`<<extend>>` +
   điều kiện (Wikipedia 3 cặp ngang; Ambler; RG). (Đã có ở `use-case-layout` §3 — giữ.)
4. **Mặc định KHÔNG nhãn trên association** (Ambler/RG/shopping: 0 nhãn). Ngoại lệ
   Wikipedia: ≤ 3 từ, chỉ trên cạnh ngắn không cắt. Cấm nhãn trên cạnh dài/chéo.
5. **Boundary làm nhóm.** Wikipedia System Boundary; shopping Release 1/2/3; RG 2 lớp
   Work System > Information System. Package = cột chức năng.
6. **Giới hạn auto đã chứng minh (uc-poc1).** Bỏ hidden zigzag + font đủ dấu + 1 cột
   package → hết giao cắt, chữ Việt render chuẩn. NHƯNG PlantUML không chia 2 cột UC
   với actor hai bên (dồn 1 cột + actor 1 phía, cạnh quạt dài). Multi-actor multi-column
   = **VẼ TAY (draw.io)** theo đúng lane đã lập. Không thử hidden thứ hai.

## 12. Sequence gọn như ảnh mẫu (reference-style Sequence)

> Ground truth: Ambler alternate-course sequence (tự tải, đã soi) + vòng lặp
> seq-naive vs seq-guided (cùng 11 bước, đã render + soi cả hai).
> Ảnh Wikipedia seq tải về bị hỏng (ô đen) — ghi nhận âm tính: kể cả nguồn lớn cũng
> có render lỗi, nên mọi ảnh phải tự soi chứ không tin nguồn.

1. **Lifeline theo thứ tự gọi đầu tiên**, actor trái nhất (Ambler). 4–6 lifeline/hình;
   quá thì tách theo use case (như SEQ-01…05 của simplified-diagrams).
2. **autonumber mọi message**; nhãn ngắn (động từ + đối tượng, ≤ 25 ký tự); returns nét
   đứt; `activate/deactivate` đúng thời gian xử lý.
3. **alt/opt/loop cho mọi nhánh** (không giấu nhánh fail); guard trên alt.
4. **Note lề** cho điều kiện đầu vào/giả thiết (kiểu C6–C9 và note góc của Ambler),
   không nhồi chữ vào nhãn message.
5. **Bằng chứng vòng lặp.** Naive (nhãn câu dài, không số/không activate/không alt)
   dàn trải khó lần; guided (đánh số 1–11, alt conflict, note điều kiện) đọc được ngay —
   cùng nội dung, khác tư duy.

## 13. Activity gọn như ảnh mẫu (reference-style Activity)

> Ground truth: Wikipedia Conducting + Ambler Enroll + Ambler Swimareas (tự tải, đã soi cả 3).

1. **Một spine chính trên-xuống** (thường cột trái), nhánh rẽ phải rồi quay về
   (wiki Conducting). Không cho luồng chính đi zigzag.
2. **Mọi lối ra của decision đều có guard** `[điều kiện]` (cả 3 ảnh đều thế).
3. **Fork/join bar** cho song song; **merge diamond** cho vòng lặp (wiki).
4. **Swimlane tách luồng chính/ngoại lệ** (Ambler swimareas: Basic Course vs
   Not-Eligible vs Appears...). Luồng phụ không chen vào spine chính.
5. Start trên cùng, end dưới cùng; chỗ cắt nhau vẽ **nhảy (jump/bridge)** (wiki).

## 14. State gọn theo chuẩn (reference-style State)

> Ground truth: legend notation Wikipedia (đã soi: state/transition/condition/entry
> action) + văn bản Booch–Rumbaugh–Jacobson UML User Guide ch.8 (đã fetch).
> Chưa tải được ảnh layout state hoàn chỉnh (Whimsical chỉ cho ảnh marketing) —
> mục này dựa trên text đã xác minh,诚实 ghi nhận.

1. **Happy path thẳng hàng** theo chiều đọc (trái→phải hoặc trên→dưới).
2. **Nhãn chuyển đủ cú pháp `Event [Guard] / Effect`**; các guard cùng state loại trừ
   nhau (mutually exclusive) (flylib).
3. **Superstate gom exits chung** (cancel/timeout): 1 đường từ superstate thay cho N
   đường song song — Fig 8-3 rõ hơn 8-2 (flylib).
4. **Entry/do/exit ghi trong state** (legend); initial + final bắt buộc.
5. State nào > 4 transitions ra → tách superstate/composite **[heuristic]**.

## 6. Nguồn-đi-kèm (source-or-nothing)

Mỗi `.png`/`.svg` bàn giao phải có **tệp nguồn cùng tên, cùng thư mục**
(`.puml`/`.dot`/`.drawio`/`.tldr`). Không nguồn = không được chèn vào báo cáo,
`diagram-auditor` chặn cứng. Cấm nộp hình "vẽ đâu đó rồi export" không truy vết được.

## 7. Checklist 60 giây sau mỗi lần render

Trả lời YES/NO bằng mắt trên ảnh PNG, không suy từ code:
1. Bốn góc khung đều có mực? (không góc chết > 25% khung)
2. Cạnh dài nhất có ngắn hơn 2.5× cạnh trung bình không?
3. Có nhãn cụt/không dấu/đè nhau không?
4. Mọi FK/association trong bảng §1 đều có đúng một đường không?
5. Container nào rỗng > 25% không?
6. Đọc được toàn bộ chữ ở cỡ in A4 thật không?

6 YES mới được chuyển sang `diagram-auditor`. 1 NO = quay lại §1–§5, sửa **một biến**,
render lại, soi lại.

## 8. Căn cứ khoa học (đã truy cập toàn văn — không phải ý kiến riêng của model)

> Ba nguồn dưới đây đều đã được fetch và đọc nội dung. Quy tắc nào suy ra từ nguồn
> ghi `[nguồn]`; ngưỡng vận hành do skill đặt thêm để đo được ghi `[heuristic]`.

**[S1] Purchase, McGill, Colpoys & Carrington (2001), "Graph drawing aesthetics and the
comprehension of UML class diagrams: an empirical study", Univ. of Queensland,
Australian Symposium on Information Visualisation.**
`https://courses.ischool.berkeley.edu/i247/f05/readings/Purchase_UML_OzIV01.pdf`
7 tiêu chí đã kiểm chứng thực nghiệm trên sơ đồ UML: (b) ít điểm gãy — đỡ;
(n) node phân bố đều trong khung — đỡ §3; (ev) độ dài cạnh đồng đều — đỡ §3;
(f) hướng luồng nhất quán — đỡ §1–§2; (o) trực giao — đỡ cấu hình PlantUML;
(el) cạnh ngắn (nhưng không quá ngắn) — đỡ §3; (s) đối xứng khi có thể.
Luận điểm then chốt: *"actual semantics of the given graph may need to be considered
before an appropriate graph drawing can be produced"* — chính là cơ sở của §1
(adjacency-first: ngữ nghĩa trước, tọa độ sau). Nghiên cứu trước đó (Purchase 1997;
Ware et al. 2002) còn chốt: **giao cắt cạnh là yếu tố gây hại nhất cho hiểu biểu đồ**.

**[S2] Eichelberger & von Gudenberg (2003), "UML Class Diagrams — State of the Art
in Layout Techniques", VISSOFT, Univ. of Würzburg.**
`https://www.cs.uvic.ca/~mstorey/vissoft2003/submissions/eichelberger_pospaper.pdf`
8 quy tắc layout dựa trên ngữ nghĩa (không phải graph trừu tượng):
(1) thứ bậc (hierarchy) làm tiêu chí sắp xếp cạnh — đỡ §2 trục luồng;
(2) vị trí không gian mã hóa coupling/cohesion/tầm quan trọng — đỡ §1 zone theo miền;
(3) gom cụm theo ngữ nghĩa — đỡ §1; (4) tránh giao cắt/chồng — đỡ §3;
(5) đặt node quan trọng ở trung tâm — đỡ quy tắc hub-trung-tâm §1;
(6) note/ràng buộc ở gần chủ thể; (7) adornments (multiplicity/role) gán rõ vào đúng
cạnh — đỡ §4; (8) tiêu chí graph chung chỉ ưu tiên thấp nhất.
Câu mở đầu bài báo — *"applying the layout algorithms of these CASE tools to the user
defined diagrams, usually horrible results are produced"* — chính là bệnh mà skill này chữa.

**[S3] Ambler, "The Elements of UML 2.0 Style", Cambridge Univ. Press, ch.2
(General Diagramming Guidelines).**
`https://assets.cambridge.org/97805216/16782/excerpt/9780521616782_excerpt.htm`
#1 tránh giao cắt; #2 chỗ cắt vẽ nhảy (jump); #3 ưu tiên đường ngang/dọc, tránh
chéo/cong **(phạm vi: sơ đồ UML kỹ thuật; sơ đồ kiến trúc tự do dùng tldraw được
cong — đã phân scope, không mâu thuẫn)**; #6 nhãn canh ngang; #7 đối xứng;
#10 khoảng trắng; #11 luồng trái→phải, trên→dưới; #12 tránh nhiều đường sát nhau — đỡ §4;
#14 chỉ vẽ cái cần; #16 ≤ 9 symbol (7±2 của Miller), sơ đồ lớn tách nhỏ — đỡ §5;
#17 một trang, cấm thu chữ/nhồi — đỡ §5; #18 nội dung trước, đẹp sau;
#19 font Arial/Times, cấm < 10pt — đỡ §4 (ngưỡng skill là ≥ 9pt in A4, tương đương).

**Ngưỡng [heuristic] do skill đặt để đo được** (suy từ [S1]–[S3], không có trong nguồn):
cạnh ≤ 2.5× trung vị; góc phần tư < 10% mực; nửa khung > 75% node; void trong
container > 25%; nodesep/ranksep sàn 60–80/60–90.
