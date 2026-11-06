# Nghiệm thu bằng MẮT — protocol đầy đủ (chống "gen hàng loạt rồi tuyên bố đạt")

> Đây là SSOT cho **Bước 4 — Visual Review** của skill `use-case-layout`.
> Đọc trọn file này trước khi tuyên bố bất kỳ sơ đồ nào là "đạt".

---

## 0. Vì sao cần protocol này (đọc phần này để không làm hình thức)

Khi sơ đồ được chèn vào Word khổ A4, bề rộng ảnh chỉ ~15 cm. Một đoạn đường nối
xuyên qua chữ lúc đó dày **~1–2 px**. Ở tỉ lệ đó, **mắt người gần như chắc chắn bỏ sót**.
Đó là lý do tồn tại của hai thứ:

| Công cụ | Việc nó làm | Việc nó **KHÔNG** làm |
|---|---|---|
| `scripts/eye_audit.py` | Tìm **ứng viên** lỗi hình học bằng số đo; cắt **ảnh phóng to 4×** từng vùng nghi vấn; xuất **overlay có lưới** | Không phán PASS/FAIL. Không biết "đẹp/đều/dễ nhìn". Có thể báo oan và có thể bỏ sót |
| Mắt của bạn (agent) | Nhìn ảnh phóng to + overlay → **phán**: thật hay báo oan, có phải sửa không | Không đo được con số. Không nhìn thấy ở 100% zoom |

**Công thức:** script **thu hẹp** phạm vi cần nhìn → mắt **phán quyết** trên vùng hẹp đó.
Thiếu một trong hai là quy trình hỏng:

- Chỉ chạy script rồi PASS → **vi phạm** (script từng báo oan `T-OVERFLOW` cho nhãn chỉ *sát* vỉa).
- Chỉ nhìn ảnh 100% rồi PASS → **vi phạm** (đã bỏ sót lỗi đường nối xuyên qua tên actor — xem §5).

---

> **Cập nhật 2026-11-01:** với bố cục actor/chùm tia, áp dụng [actor-function-composition.md](actor-function-composition.md). Các ca lịch sử bên dưới giữ làm bằng chứng lỗi từng hình; không suy ra cấm mọi quạt chung gốc, bắt buộc rải neo hoặc bắt buộc cột bậc thang. C-FAN không phải lỗi tự động; không kéo dài actor để tắt cảnh báo.

## 1. LUẬT CẤM GEN HÀNG LOẠT

> [!CAUTION]
> **CẤM sinh N sơ đồ rồi tuyên bố "cả N đều đạt" trong một câu.**
> Mỗi sơ đồ là **một vòng nghiệm thu riêng**, có **file `*-audit.md` riêng**, có **bảng bằng chứng riêng**.
>
> Cụ thể, mỗi hình phải có **đủ 4 dấu vết** dưới đây, nếu thiếu 1 thì kết luận **không hợp lệ**:
> 1. `docs/diagrams/<ten>-audit.md` — bảng ứng viên đã điền đủ cột "Mắt thấy gì / Thật hay báo oan".
> 2. `docs/diagrams/<ten>-audit/overlay.png` — ảnh có lưới, và **đã mở**.
> 3. `docs/diagrams/<ten>-audit/crops/F01..FNN-*.png` — **mọi** crop đã mở (không phải chỉ 1 cái).
> 4. Trong audit: ≥ **3 nhãn đọc nguyên văn + vị trí** và trả lời đủ 3 câu **đè? đều? dễ nhìn?**
>
> Câu hỏi tự vấn trước khi ghi PASS: *"Nếu thầy/cô mở ảnh và zoom vào chỗ tôi vừa khen, tôi có dám
> chỉ đúng chỗ đó không?"* Không dám chỉ → chưa soi.

**Hệ quả cho việc sửa:** sửa sơ đồ thì **chạy lại đúng vòng nghiệm thu đó cho chính hình đó**
(render lại → `eye_audit.py` lại → mở lại crop). Cấm "sửa rồi suy ra là đẹp".

---

## 2. BA CÂU BẮT BUỘC — trả lời bằng mô tả cụ thể, không bằng tính từ suông

| Câu | Phải trả lời được | Ví dụ ĐẠT | Ví dụ KHÔNG ĐẠT (bị trả lại) |
|---|---|---|---|
| **1. ĐÈ?** | Có đường nối nào đè lên ellipse / chữ / **tên actor** / nhãn `«include»`,`«extend»` không? Hai node/nhãn có chồng không? | "Khung crop F01: 4 đường association từ ngực 'Khách hàng' cắt ngang chữ **hàng** — có đè, phải sửa." | "Nhìn chung không bị đè." |
| **2. ĐỀU?** | Nhịp có ổn **TRONG từng cụm** không (giữa các cụm được rộng hơn — bố cục theo nhóm, §3.2b skill)? Có **căn cùng trục trong cụm** không? Bố cục có bị dồn cục / trống hoác một nửa / **lưới một bước đều máy móc** không? | "Cụm 'Quản lý kho' 4 node nhịp ~95 px đều; cụm cách cụm ~190 px — tách nhóm rõ, không phải lưới một bước đều." | "Khoảng cách trông ổn." |
| **3. DỄ NHÌN?** | Nhìn 3 giây có hiểu luồng không? Mỗi đường có **lần theo được** không? Có **vòng xa** không? Chữ có bị cắt/nhỏ quá không? | "Đường nối chỉ ngắn trong 1 cột; 3 đường `«extend»` đi ngang 106 px sang cột phải, lần theo được, không có vòng xa." | "Sơ đồ nhìn dễ hiểu." |

**Bằng chứng bắt buộc kèm theo:** ≥ **3 nhãn đọc nguyên văn + vị trí**, ví dụ:
`"Rút tiền" ở cột giữa hàng 8`, `"Gửi duyệt sản phẩm" ở cột phải hàng 3`,
`tên actor "Người bán" ở đáy cột trái`. Nếu bạn **không đọc nổi** 3 nhãn từ ảnh thì
bạn **chưa mở ảnh ở độ phân giải đủ** — mở lại, đừng bịa.

---

## 3. KỸ THUẬT ĐO BẰNG MẮT (7 cách, dùng hết)

Mắt đo được nếu bạn **tạo điều kiện cho nó đo**. Bảy kỹ thuật dưới đây là phần
"tìm mọi cách soi ra như mắt người":

### 3.1. Lưới + trục giữa (overlay)
`eye_audit.py --overlay` xuất `overlay.png` có lưới 10×10 và **trục giữa màu đỏ**.
- Tâm các ellipse **cùng cụm** nằm gần một trục dọc — soi bằng cách so với trục lưới; lệch nhỏ **có chủ đích giữa các cụm** (stagger, §3.2b skill) được chấp nhận. Một cột dài đơn điệu từ trên xuống dưới là dấu hiệu **lưới máy móc**.
- Khoảng cách hàng: đếm số ô lưới giữa hai tâm; **trong cụm** các hàng phải rơi vào **cùng nhịp**; nhịp **giữa các cụm** được (và nên) lớn hơn.
- Bố cục cân: khối nội dung phải nằm quanh trục giữa, không lệch hẳn sang một bên.

### 3.2. Zoom 300–400% từng nhãn
Mở `crops/*.png`. Mắt chỉ đọc được chữ nhỏ khi nó được phóng to.
Với mỗi nhãn, tự hỏi: *chữ có chạm/thò ra khỏi vòng ellipse không? đường có cắt qua chữ không?*

### 3.3. Truy nét bằng ngón tay
Đặt ngón tay (hoặc con trỏ) lên **đầu** mỗi connector rồi trượt theo nét tới **cuối**:
- Nếu phải "nhảy qua" một ellipse/chữ/nhãn → đó là lỗi đè.
- Nếu phải đi một vòng dài → đó là **vòng xa**.
- Nếu cuối nét **không chạm** node/actor nào → **neo lơ lửng**.
Kỹ thuật này bắt được lỗi mà liếc tổng thể bỏ qua.

### 3.4. Bài test "nheo mắt" (visual weight)
Nheo mắt / thu nhỏ ảnh còn ~25%: mắt chỉ còn thấy **khối sáng-tối**.
- Sơ đồ tốt: thấy **các cụm rõ ràng** — mỗi cụm là một khối đậm có nhịp đều, giữa các cụm có **khe sáng tách nhóm**.
- Sơ đồ xấu 1: **một dải node trải đều từ trên xuống dưới như thang máy** — lưới máy móc, không tách nhóm (§3.2b skill).
- Sơ đồ xấu 2: thấy **một cục đen lổn nhổn ở góc**, một nửa còn lại trắng trơn.
Đây là cách nhanh nhất để phát hiện "dồn cục" mà đọc từng nhãn không thấy.

### 3.5. Bài test in A4 ~15 cm
Thu ảnh về đúng bề rộng **15 cm** rồi nhìn: nhãn nhỏ nhất có đọc được không?
Nếu không → **phân rã sơ đồ**, tuyệt đối không thu nhỏ thêm để nhét vừa trang.

### 3.6. Bài test cây thước (đo 3 khoảng liên tiếp)
Chọn 3 khoảng cách liên tiếp trong một cột. So bằng mắt xem chúng có bằng nhau không,
rồi **đối chiếu con số** trong báo cáo `eye_audit` (mục `G-GAP`). Lệch > ~20% là thấy được.
Kỹ thuật này biến "cảm giác hơi lệch" thành **phán quyết có số**.

> **Lưu ý chống máy móc:** `G-GAP` / `N-UNALIGN` / `A-SKEW` / `C-FAN` / `S-LADDER` là **ứng viên thiết kế (mức LOW)**,
> không phải lỗi chặn. Nếu khoảng cách/trục khác nhau là **chủ đích nhóm** (đều trong cụm,
> rộng giữa cụm — §3.2b skill) → ghi `BAO-OAN` kèm lý do nhóm; nếu là lệch **vô ý trong cùng
> một cụm** → sửa về nhịp cụm.

### 3.7. Bài test đọc thành tiếng
Đọc to tên actor và các nhãn quan hệ. Nếu phải "né" một nét để đọc được chữ → **có đè**.
Đây chính là bài test đã phát hiện lỗi §5.

---

## 4. THANG ƯU TIÊN KHI SỬA (bắt buộc theo đúng thứ tự)

Khi phát hiện lỗi bố cục, sửa theo đúng thứ tự này — **không nhảy bậc**:

0. **KIỂM BỐ CỤC GỐC TRƯỚC KHI SỬA NÉT** — nếu use case đang nằm trên **một cung tròn / đường tròn
   đồng tâm với actor** thì **đập bố cục, đừng sửa dây**: mọi association sẽ là bán kính → hội tụ một điểm
   ("con nhện") + khoảng trống giữa cung. Thay bằng **cột theo cụm, cụm sau lùi phải (bậc thang)**
   (SKILL §3.2b; ca thật ở §5c dưới đây). Sửa dây trên một bố cục sai chỉ làm lỗi trông "gọn" hơn.
1. **DI CHUYỂN NODE** (đổi `row`/`lane`, đưa 2 đầu lại gần, **tách 1 cột dài thành 2–3 cột theo cụm** — chữa `S-LADDER`).
   → Sửa được ~80% lỗi, và là bậc **bắt buộc thử trước**.
2. **GỘP / TÁCH NHÓM** (gộp 2 nhóm gần nhau, hoặc tách sơ đồ thành 2 hình; **dãn cụm cho không dồn nửa hình** — chữa `U-OCCUPY`).
3. **ĐỔI ĐIỂM NEO** — neo vào **cạnh gần nhất** của ellipse (la bàn 8 hướng), neo **thân** thay vì ngực;
   chùm ≥ 3 cạnh từ một actor → **toả từ các điểm neo rải dọc THÂN, góc chênh dần, không bắn cả chùm từ một điểm**
   (chữa `C-FAN`). Dải neo phải nằm trong **thân** (`exitY 0.33–0.87` của hình actor) — **không rời từ đầu/cổ**,
   vì dây mọc ra từ đầu trông như lỗi render dù hình học "đúng".
4. **CONG NHẸ hoặc BẺ GÓC** — fan-out / `include`–`extend` giữa node kề → **cong nhẹ (bezier, độ võng nhỏ)**
   đọc tự nhiên hơn; né chướng ngại → **orthogonal/elbow**, không bẻ quá 2 gấp khúc. Mọi đường (kể cả cong)
   vẫn cấm xuyên ellipse/chữ/tên actor và vẫn qua đủ 3 nhịp soi mắt.
5. **ĐI VÒNG** — **CẤM** (xem SKILL §3.5). Không bao giờ là phương án.

> **Mapping ứng viên → bậc sửa:** `C-FARLOOP`, `L-INSIDE`, `S-LADDER` → bậc 1–2 (đổi node/cụm trước, tuyệt đối không vá bằng dây) ·
> `L-ACTORNAME` → bậc 1 rồi 3 · `C-FAN` → bậc 3 rồi 4 (cong nhẹ) · `L-TEXT`, `T-OVERFLOW`, `T-TIGHT`, `N-OVERLAP`, `S-BOUNDARY` → bậc 1–2 ·
> `G-GAP`, `N-UNALIGN`, `A-SKEW` → mắt phán trước: chủ đích nhóm thì `BAO-OAN`, vô ý thì bậc 1.

Sau mỗi lần sửa: **chạy lại vòng nghiệm thu của chính hình đó** (§1).

---

## 5. VÍ DỤ THẬT — lỗi mà MẮT 100% ĐÃ BỎ SÓT, SCRIPT + ZOOM BẮT ĐƯỢC

Đây là ca thật đã xảy ra trong bộ 4 sơ đồ Use Case của một đồ án (33a–33d),
ghi lại để thấy vì sao phải làm cả hai bước:

1. **Nhìn ảnh 100%** (cả hình dài ~1370 px): kết luận "nhìn ổn, đường nối gọn, không đè".
2. **Chạy `eye_audit.py`**: script báo `L-ACTORNAME` — *"Đường #9/#10/#11 xuyên qua TÊN ACTOR 'Người bán'"*.
3. **Mở crop `F01-L_ACTORNAME.png` (zoom 4×)**: thấy rõ **6 đường association cắt ngang chữ "bán"**.
   Ở 33a, 4 đường cắt ngang chữ **"hàng"** trong "Khách hàng".
4. **Verdict của mắt**: **THẬT** — luật "tên actor không bị đường nối xuyên qua" bị vi phạm;
   vi phạm nặng nhất về mặt thẩm mỹ vì tên actor là thứ người đọc nhìn đầu tiên.
5. **Cách sửa đúng (theo thang §4)**: **đổi điểm neo** — neo association vào **vai/đỉnh đầu**
   actor (hoặc vào một "trục dọc" phía trên tên) thay vì ngực, **và** đẩy tên actor xuống
   dưới chân actor thêm ~15–20 px. Không kéo dây vòng, không nhét tên vào giữa.

Cùng vòng đó, `G-GAP` cũng bắt được **một** cặp node lệch nhịp (136 px thay vì 100 px)
mà mắt đọc là "trông ổn". Và `T-TIGHT` báo 4 nhãn **sát vỉa 98–103%** — mắt phán:
*"sát nhưng chưa tràn → nên tăng `ry` ~15% cho an toàn khi đổi font"*, tức **không phải**
lỗi chặn cứng nhưng vẫn nên sửa.

**Bài học:** script báo **ứng viên**, mắt phán **thật/báo oan**. Cả hai bước đều không bỏ được.

---

## 5b. VÍ DỤ THẬT THỨ HAI — lỗi do CHÍNH VIỆC SỬA sinh ra, và chỉ MẮT phát hiện

Vẫn bộ 4 sơ đồ trên. Sau khi sửa lỗi §5 (dời tên tác nhân), tôi chuyển tên sang **bên trái hình người,
ngang tầm thân**, và **giữ nguyên nền trắng** của nhãn (nền này trước đây dùng để che đường nối đi qua).

Hệ quả: **nền trắng đó che mất một phần MŨI TAM GIÁC của quan hệ generalization** — ở vùng zoom
*"Người xem"* chỉ còn một mảnh tam giác trông như một vết mực lạc.

- Script **không** báo gì: đây không phải "đường xuyên qua nhãn", cũng không phải "nhãn tràn ellipse".
- **Mắt bắt được** khi soi crop: *"mũi tam giác bị cắt còn một mảnh"* (kỹ thuật §3.6 — bài test cây thước/truy nét).
- Cách chữa: **bỏ hẳn nền trắng của nhãn** (không còn cần, vì nhãn đã ở chỗ không đường nào đi qua),
  và chỉnh vị trí dọc của nhãn cho khỏi trùng đường ngang.

**Từ ca này, công cụ được bổ sung phép kiểm `C-MASKED`** (*"nền trắng của nhãn che một phần đường nối"*) để
lần sau lỗi này bị bắt tự động. Phân biệt với `I-MASKED`: `I-MASKED` = đường **đi xuyên qua** nhãn (đúng thiết kế,
được che); `C-MASKED` = có **điểm neo nằm trong** nền trắng còn phần khác ở ngoài (đang bị cắt).

> **Bài học lớn hơn — luật bất di bất dịch của skill này:**
> **Mỗi lần sửa bố cục thì phải chạy lại đúng vòng nghiệm thu đó cho chính hình đó.**
> Sửa một chỗ có thể sinh lỗi ở chỗ khác. "Sửa rồi suy ra là đẹp" là cách tự lừa mình nhanh nhất.
> Và hãy để lại **phép kiểm** cho loại lỗi vừa gặp — đừng chỉ sửa tay rồi đi tiếp.

---

## 5c. VÍ DỤ THẬT THỨ BA — "CON NHỆN": bố cục cung tròn quanh actor (2026-10-29)

Sơ đồ Use Case đồ án *Quản lý rạp chiếu phim* (15 UC / 3 actor). Bản `v2` được sinh bằng script với
bố cục **"vòng cung tự nhiên": actor ở tâm, các use case xếp trên một cung bán kính ~380px.**

Kết quả — người dùng trả lại ngay, và đúng:

- **6 association của actor chính hội tụ đúng một điểm trên ngực actor** (mọi đường là **bán kính** của
  cùng một đường tròn) → hình *con nhện / đuôi công*, không phải sơ đồ.
- **Giữa cung là một khoảng trống khổng lồ** vì node bị đẩy ra rìa, boundary phình to vô ích.
- Mọi đường **dài gần bằng nhau** → mắt không phân biệt được cụm nghiệp vụ nào với cụm nào.

Điều đáng chú ý: **`eye_audit.py` bản cũ KHÔNG báo gì** (HIGH=0) — vì từng đường đều "sạch": không xuyên
ellipse, không xuyên chữ, neo đúng biên. **Lỗi nằm ở BỐ CỤC, không nằm ở từng nét.** Đây là lý do tuyệt đối
không được coi "script 0 đỏ" là bằng chứng đẹp.

Cách chữa (v3) — và là chuẩn từ nay:

1. **Bỏ hoàn toàn cung tròn.** Use case xếp **cột dọc theo cụm nghiệp vụ**; cụm sau **lùi sang phải 15–45px**
   (bậc thang) để silhouette không thành một đường kẻ.
2. Cột dọc làm **thứ tự `y` của đích đơn điệu** → association **không thể cắt nhau** (chứng minh hình học,
   không phải "may mắn").
3. Chùm dây rời actor từ **nhiều điểm rải dọc thân** (`exitY 0.33–0.87`), không phải một điểm, và **không rời từ đầu**.
4. Tên actor đặt **bên cạnh** hình (trái với Lane L, phải với Lane R) thay vì dưới chân — chùm dây toả rộng
   > 45° sẽ cắt ngang tên nếu tên nằm dưới chân.
5. Bổ sung 2 phép kiểm để lần sau bắt tự động: **`C-FAN`** (≥4–5 đường xuất phát gần một điểm **và** góc
   giữa 2 đường kề < 8° với độ dài ≥ 120px) và **`S-LADDER`** (≥8 node trong dải dọc ~80px).

> **Luật rút ra (đã ghi vào SKILL §3.2b):** *CẤM đặt toàn bộ use case trên một cung tròn/đường tròn đồng tâm
> với actor.* Cung tròn biến mọi association thành bán kính — hình học sai **trước khi** vẽ nét đầu tiên.

---

## 6. BẢNG TỪ VỰNG VERDICT (ghi đúng để không tự lừa)

| Verdict | Nghĩa | Được ghi PASS? |
|---|---|---|
| `THAT` | Mắt xác nhận lỗi có thật | **Không** — phải sửa rồi soi lại |
| `BAO-OAN` | Script báo nhưng mắt thấy ổn | Có — nhưng phải **ghi lý do** vì sao báo oan |
| `CHAP-NHAN-DUOC` | Có lệch/sát nhỏ, không ảnh hưởng đọc hiểu | Có — nhưng **ghi rõ** mức chấp nhận và **cách khắc phục rẻ nhất** nếu có thời gian |
| `CHUA-SOI` | Chưa mở ảnh / chưa đọc được nhãn | **Không** — quay lại mở ảnh |

Với mỗi dòng `BAO-OAN` / `CHAP-NHAN-DUOC`, ghi 1 câu lý do. Không có lý do → coi như `CHUA-SOI`.

---

## 7. CHECKLIST NGHIỆM THU (dán vào `*-audit.md`)

```text
[ ] Da chay: python scripts/eye_audit.py <file.svg> --overlay --dump
[ ] Parser doc dung?  node=<n> khop so ellipse thuc te?  actor=<m> khop so actor?
      (neu KHONG khop -> dung lai, sua tham so nhan dang TRUOC khi tin ket qua)
[ ] Da mo: <ten>-audit/overlay.png
[ ] Da mo: TAT CA file trong <ten>-audit/crops/   (dem: <n> file)
[ ] Bang ung vien da dien du cot "Mat thay gi / That hay bao oan / Da sua?"
[ ] >= 3 nhan doc nguyen van + vi tri: ...................................
[ ] DE?      .............................................................
[ ] DEU? (deu TRONG tung nhom; giua cac nhom duoc rong hon chu dich — §3.2b) ..
[ ] DE NHIN? .............................................................
[ ] Ten actor co bi duong noi xuyen khong?  ..............................
[ ] Co vong xa / connector dai bat thuong khong?  ........................
[ ] Co chum 'quat ga' tu mot diem (C-FAN) / cot 'thang may' (S-LADDER) khong? ...
[ ] Co line/mui ten nao bi NEN TRANG cua nhan che khong? (C-MASKED)  ......
[ ] Sau khi sua: DA CHAY LAI vong nghiem thu nay?  ......................
```
