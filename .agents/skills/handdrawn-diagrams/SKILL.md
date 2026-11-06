---
name: handdrawn-diagrams
description: "Vẽ MỌI sơ đồ kỹ thuật bằng tay (SVG sinh từ Python với toạ độ cứng) — thay hẳn PlantUML/Mermaid/Graphviz/drawio cho bản nộp báo cáo, đồ án, luận văn, slide. Quy trình: layout spec toạ độ → generator → render SVG+PNG (SVG KHÔNG nằm cùng thư mục PNG) → bộ kiểm định tất định E1..E6 và E7 từ chối cấu trúc chưa hỗ trợ + selftest chống False PASS. Dùng khi người dùng nói: vẽ tay hết, không dùng PlantUML, không dùng công cụ ngoài, sơ đồ vẽ xấu quá, sơ đồ bị lệch/đè nhãn, cần toạ độ cứng để agent tự vẽ, cần eye audit không cần mắt người, use case, class, ERD, sequence, activity, state machine, DFD, BFD, kiến trúc."
---

# Hand-drawn Diagrams — Vẽ tay 100%, toạ độ cứng, kiểm định tất định

> **Cập nhật 02/11/2026:** đã bổ sung regression và cổng hợp đồng đầu ra. Đọc [giới hạn bộ kiểm](reference/known-audit-gaps.md); kết quả máy không thay thế kiểm ngữ nghĩa và Vision QA.

Mục tiêu: bố cục có chủ ý, tái lập được và có bằng chứng kiểm tra. Mọi sơ đồ cuối cùng là **SVG do chính project sinh ra**
từ những con số toạ độ viết tay trong code — không PlantUML, không Mermaid, không Graphviz,
không phụ thuộc file `.drawio` để render.

---

## 0. LUẬT BẤT BIẾN

1. **SVG vẽ tay là bản nộp.** PlantUML/Mermaid/Graphviz/drawio chỉ được dùng làm **nháp** để
   nghĩ bố cục, **không bao giờ** là file cuối cùng chèn vào Word/Slide.
2. **Toạ độ phải là hằng số trong code**, không random, không auto-layout ngẫu nhiên.
   Cùng input → cùng toạ độ SVG; pixel PNG còn phụ thuộc font và phiên bản trình duyệt. Ghi lại môi trường render.
3. **SVG không nằm cùng thư mục PNG** — mỗi định dạng một thư mục riêng, nghiêm ngặt:
   ```text
   docs/diagrams/spec/      *.json  ← TOẠ ĐỘ CỨNG (nguồn sự thật, máy đọc)
   docs/diagrams/vectors/   *.svg   ← DUY NHẤT ở đây
   docs/diagrams/drawio/    *.drawio ← bản web-editable (tuỳ chọn)
   docs/images/diagrams/    *.png   ← DUY NHẤT ở đây
   ```
   **Cấm:** `.svg` / `.drawio` trong thư mục PNG; `.png` trong `vectors/`.
4. **Không tuyên bố PASS khi chưa có bằng chứng đo được.** Nếu model không xem được ảnh,
   phải nói thẳng `Visual QA unavailable` — **cấm bịa Proof-of-View** ("tôi thấy nhãn X ở …").
5. **CỔNG PASS HAI ĐIỀU KIỆN (bắt buộc, khớp `diagram-auditor` §1.5):** chỉ PASS khi
   **ĐK1 MÁY** (audit 0 lỗi + **file nguồn `.py` generator TỒN TẠI** + **file ảnh `.png` + `.svg` TỒN TẠI >500B**)
   **VÀ ĐK2 VISION** (**model có vision** soi ảnh thật, ghi ≥3 nhãn + vị trí + kết luận "sắp xếp hợp lý chưa"
   + `Vision audit by: <model-id>`). Model text-only **không tính**. Ảnh có mà thiếu `.py` nguồn = **FAIL** (không tái lập được).
6. **Trắng–đen tuyệt đối** cho báo cáo học thuật; không tiêu đề nhúng trong ảnh.

---

## 1. Quy trình 5 bước

```text
B1. Viết spec toạ độ     → docs/diagrams/gen_<ten>.py + spec/<ten>.json
B2. Sinh SVG             → docs/diagrams/vectors/<ten>.svg
B3. Render PNG 2×        → docs/images/diagrams/<ten>.png  (Chrome headless)
B4. Kiểm định tất định   → py -3 scripts/audit_svg.py    (E1..E7, phải 0 lỗi)
B5. Ghi dấu vết audit    → docs/audit/soi-so-do/<ten>/audit.md
```

Một lệnh gộp **cổng máy**, không thực hiện Vision QA: `py -3 scripts/run_diagrams.py --root <project>`.
Chi tiết từng bước + mẫu code: `reference/coordinate-workflow.md`.

---

## 2. Bộ kiểm định tất định — `scripts/audit_svg.py`

Đọc **chính file SVG đã render**, bắt 6 lớp lỗi đo được (không cần mắt người):

| Mã | Lỗi | Cách phát hiện |
|:--|:--|:--|
| **E1** | Phần tử ra ngoài khung | bbox vượt `viewBox` → bị cắt khi in |
| **E2** | Hai nhãn đè nhau | giao bbox > 42% diện tích hộp nhỏ hơn |
| **E3** | Dây cắt xuyên nhãn | Liang–Barsky segment × text-bbox (chỉ xét che khuất trắng đúng thứ tự vẽ; không miễn lỗi chữ đè chữ) |
| **E4** | Chữ tràn khỏi hình bao | bbox text vượt rect/ellipse đang chứa nó |
| **E5** | id trùng | đếm `id` trong DOM |
| **E6** | Text rỗng / toạ độ không hữu hạn | kiểm thuộc tính hình học và nội dung |
| **E7** | Cấu trúc SVG chưa hỗ trợ | từ chối thay vì bỏ qua; xem giới hạn parser |

```bash
py -3 scripts/audit_svg.py                       # quét docs/diagrams/vectors/*.svg
py -3 scripts/audit_svg.py a.svg b.svg --json r.json
```

Mã thoát: `0` PASS · `1` có lỗi E · `2` chỉ cảnh báo.

### 2.1. Chống hội chứng FALSE PASS (bắt buộc)

`scripts/selftest_audit_svg.py` tạo một SVG **hỏng có chủ đích** (đè nhãn, dây xuyên chữ,
chữ tràn khung, text rỗng, id trùng) rồi đòi bộ kiểm bắt **đủ cả 6 mã**.

```bash
py -3 scripts/selftest_audit_svg.py
# Kỳ vọng: các fixture và regression đạt; không thay Vision QA
```

> Nếu selftest FAIL → dừng nghiệm thu, sửa bộ kiểm và kiểm lại đầu ra bị ảnh hưởng. Selftest đạt chỉ chứng minh các fixture đã chạy.
> Đây là bài học thật: bản đầu của `audit_svg.py` bỏ sót E3 vì coi hình nền trắng toàn khung
> là "nền che nhãn" → mọi nhãn được miễn kiểm. Selftest đã bắt được lỗi này.
> Bản sau còn bỏ sót **đường cong**: `Q`/`C` không được mẫu hoá → dây cong cắt nhãn lọt hết.
> Selftest giờ có thêm ca `BAD_CURVE` (path `Q` cắt xuyên nhãn) và bắt buộc phải FAIL.

### 2.2. Cổng riêng cho Use Case — `scripts/check_fan_arc.py`

Luật "1 điểm xuất phát + đường thẳng" có cổng hình học riêng; vẫn phải soi ảnh:

| Mã | Luật | Cách phát hiện |
|:--|:--|:--|
| **F1** | Mọi association của một actor xuất phát từ **đúng 1 điểm** (khuỷu tay) | nhóm path/line theo gốc, đếm số điểm đầu khác nhau |
| **F2** | Mỗi association là **đoạn thẳng** (`<line>` / `M..L..`) | có lệnh `Q`/`C` → FAIL (cung chỉ dùng khi được yêu cầu rõ) |
| **F3** | Dây không đi vào **đầu** actor | khoảng cách mẫu dây ↔ tâm đầu (r=10) |
| **F4** | Dây không cắt **cánh tay / chân** actor | giao đoạn dây ↔ đoạn tay/chân (đọc từ SVG, không hard-code), bỏ qua giao tại điểm xuất phát |
| **F5** | Actor có association | tránh "PASS rỗng" khi không nhận diện được gì |

```bash
py -3 scripts/check_fan_arc.py                # quét vectors/*.svg (bỏ qua file không có actor)
py -3 scripts/check_fan_arc.py uc.svg         # kiểm 1 file
```

> Đây là bài học thật: khi mới đổi sang cung, cổng này bắt được **1 association cắt qua cánh tay**
> (cung dốc nhất của actor trái) — lỗi mà audit E1..E6 **không** phát hiện vì nó chỉ kiểm chữ.


---

## 3. Luật bố cục (áp dụng cho mọi loại sơ đồ)

### 3.1. Sơ đồ hộp (Class / ERD / BFD / kiến trúc)

Ví dụ lưới, **không phải bố cục mặc định cho mọi hình**. Chọn số cột theo cụm quan hệ và khổ chèn:

```text
COL_L = [20, 500, 980, 1460, 1940]   # mép TRÁI 5 cột
BW = 300     HEAD = 40     LH = 21   # rộng hộp / cao vùng tên / giãn dòng
hộp cao = HEAD + LH × số_trường
khe giữa 2 cột = 180 px  → đủ chỗ kênh dọc
```

1. Hai hộp liền kề cùng cột: dùng đoạn thẳng nếu hành lang trống. Có hộp trung gian thì đi kênh bên cạnh; không xuyên hộp.
2. Quan hệ **khác cột** → kênh dọc **giữa 2 cột**, rồi elbow vào đúng vỉa.
3. Kênh khác cột **so le ≥ 16 px**.
4. Đầu mút **phải nằm trên biên hộp** — kiểm bằng `verify_box_layout.py` (E1/E2/E3/E4 hình học).
5. Nhãn bội số đặt cạnh đầu quan hệ, không đè dây hoặc nhãn khác.

### 3.2. Nhãn không bao giờ bị dây cắt

Ưu tiên dời nhãn hoặc đổi tuyến dây để có khoảng trống thật. Halo trắng chỉ là tuỳ chọn tăng độ đọc, không dùng che lỗi giao cắt. Ví dụ tuỳ chọn:

```python
HALO = 'paint-order="stroke" stroke="#fff" stroke-width="3.5" stroke-linejoin="round"'
# <text ... {HALO}>Nhãn</text>
```

### 3.3. Ký hiệu phải TRÙNG AXIS

Với tuyến hộp vuông góc, Crow's foot / gạch bội số có pháp tuyến `(±1,0)` hoặc `(0,±1)`.
**Cấm** tính pháp tuyến từ **tâm hộp** (gây tilt khi hộp không cân) — chọn **cạnh gần nhất**.

Mũi tên trên tuyến chéo (như include/extend) xoay theo tiếp tuyến của chính cạnh, không ép theo trục.

### 3.4. Use Case

- Actor là **người que** đúng tỷ lệ, tên đặt **bên cạnh** (không dưới chân).
- **ĐÚNG 1 ĐIỂM xuất phát:** mọi association của một actor xuất phát từ **đúng 1 điểm ở khuỷu tay**
  = junction thân/tay `(ax, ay − 4)` (`ORIGIN_DY = 18` tính từ tâm đầu). **Không rải neo dọc thân**,
  **không lệch ±12 px** — tất cả các dây phải hội tụ tại một điểm duy nhất.
- **ĐƯỜNG THẲNG, không cung** (quyết định 2026-11-01): mỗi association là **đoạn thẳng** `<line>`
  từ khuỷu tay tới mép ellipse. `CURVE = 0.0` là mặc định; `CURVE > 0` chỉ bật khi được yêu cầu rõ.
  > **"Vòng cung" là hình ELLIPSE (chức năng), KHÔNG phải dây nối.** Người dùng đã bác cách vẽ
  > cung Bézier cho association: nhìn rối, không giống sơ đồ use case chuẩn.
  > Vì sao lấy **khuỷu tay** chứ không phải bụng: tia đi LÊN từ bụng **cắt ngang cánh tay**
  > (đo được 1 cạnh vi phạm F4); xuất phát tại khuỷu tay thì tia "mọc" từ cánh tay, không bao giờ cắt nó.
- **Cánh tay actor `±13 px`**, chân `±13 px` dài 20 px từ `ay + 32` — dùng cho F3/F4.
- **Nhãn «include»/«extend»** đặt tại trung điểm dây với nền trắng 68×16.
- **Mũi tên hở** trên include/extend hướng theo dây cung `p0 → p1`.
- UC phụ (include/extend đích) đặt lệch sang bên partner, dây ngắn < 250 px.
- Chi tiết sinh code: `use-case-layout/scripts/make_drawio.py` + `reference/coordinate-workflow.md`.

### 3.5. State Machine

- Initial = chấm đen; Final = vòng + chấm; **final không có cạnh ra**.
- Nhãn chuyển trạng thái đặt trong khoảng trống sát cạnh, đúng `event [guard] / effect` khi có. Không thêm halo chỉ để vượt E3; đọc state-playbook trước khi vẽ.
- Canvas **chỉ chứa phần tử UML** — cấm note/legend/footer/chữ thuyết minh.

### 3.6. Sequence / Activity / DFD

- Sequence: lane dọc cố định (`LANES`), `BOXW/BOXH`, `TOP/BOT`, danh sách `MSGS` có `y` cứng.
- Activity: swimlane cố định, guard trên cạnh rẽ, **không** để nhãn đè mũi tên.
- DFD: hình tròn/bong bóng tiến trình ở tâm, tác nhân ngoài 2 bên, nhãn luồng có khoảng trống riêng.

---

## 4. Checklist Definition of Done

```text
[ ] SVG sinh từ code có toạ độ HẰNG SỐ (không auto-layout ngẫu nhiên)
[ ] SVG nằm ở docs/diagrams/vectors/  ·  PNG nằm ở docs/images/diagrams/  (KHÔNG lẫn)
[ ] .drawio (nếu có) nằm ở docs/diagrams/drawio/ — KHÔNG lẫn thư mục PNG/vectors
[ ] py -3 scripts/selftest_audit_svg.py  → các fixture đạt
[ ] py -3 scripts/audit_svg.py           → 0 lỗi E1..E7
[ ] py -3 scripts/check_fan_arc.py       → 0 lỗi F1..F5 (Use Case: 1 điểm xuất phát + ĐƯỜNG THẲNG)
[ ] verify_box_layout.py (sơ đồ hộp)      → 0 lỗi hình học
[ ] Ảnh PNG đã được NGƯỜI hoặc model-có-vision xem lại (thẩm mỹ/ngữ nghĩa)
[ ] Nếu không xem được ảnh → ghi "Visual QA unavailable", KHÔNG bịa Proof-of-View
[ ] audit.md ghi rõ: cái gì đo được (máy), cái gì cần mắt (người)
```

---

## 5. Giới hạn phải nói thật

- Bộ kiểm **không phán thẩm mỹ**: cân đối thị giác, mật độ chữ, sơ đồ có đúng *nghiệp vụ* không.
- Bề rộng chữ ước lượng `font-size × 0.55` (Arial) → font khác lệch ±8%.
- **Model không có vision thì không được claim đã "soi ảnh"** — chỉ được báo kết quả đo được
  và yêu cầu người kiểm nhịp cuối.

## 6. Chốt bố cục trước khi vẽ

1. Lập danh sách node/cạnh từ nguồn nghiệp vụ; State phải có bảng chuyển trạng thái và phân biệt as-is/to-be. Không lấy ảnh mẫu làm bằng chứng chức năng.
2. Phác cụm chính, luồng chính và nhánh phụ; đặt node liên quan cạnh nhau. Chọn hướng đọc trái→phải hoặc trên→dưới; không ép mọi loại hình vào cùng lưới.
3. Định trước vùng chữ và hành lang dây. Ưu tiên ít giao cắt, ít góc gãy, nhánh phụ gần node chính; không vòng xa chỉ để giữ cột. Nếu quá dày, tách theo phạm vi có ý nghĩa và giữ bảng truy vết đầy đủ.
4. Render từng hình ở kích thước chèn thực tế và zoom crop. Kiểm nhãn, chiều mũi tên, cân khoảng trống, dây xuyên hình/chữ, dấu tiếng Việt. Sửa nguồn rồi render lại hình ảnh hưởng.
5. Chạy cổng máy, sau đó ghi Proof-of-View riêng cho từng hình. Không kết luận bố cục đẹp chỉ từ số lỗi bằng 0.

### Hợp đồng runner

Mỗi `vectors/<ten>.svg` có PNG và `spec/<ten>.json` cùng stem. Spec bắt buộc chứa `generator` (đường dẫn `.py` tương đối root) và `diagram_type`. Loại hộp thêm `layout` theo schema của `verify_box_layout.py`; Use Case dùng actor mẫu r=10, nếu không nhận diện được phải chuẩn hoá hoặc mở rộng checker. `--audit` không chạy generator; do đó chỉ kiểm đầu ra hiện có, không chứng minh đầu ra mới nhất từ nguồn. PNG hiện được kiểm chữ ký/IHDR, không thay giải mã và mở ảnh thật.
