# Pitfalls — use-case-layout

> Bài học do agent đóng góp khi gặp lỗi/biến chứng mà SKILL.md chưa nói đến.
> Quy trình đóng góp: skill `skill-feedback` (xác minh → chống trùng → ghi → cập nhật
> bản đồ lessons-learned → verify + sync). Bài học mức IRON phải được chuyển lên SKILL.md.

> **Hiệu chỉnh 2026-11-01:** nhãn IRON về “tụ một điểm” dưới đây là lịch sử, không còn là luật cấm. SSOT hiện hành: [actor-function-composition.md](actor-function-composition.md). Vấn đề cần sửa là bố trí node/nhãn; quạt thẳng chung gốc đúng ảnh mẫu được phép, actor luôn giữ tỷ lệ bình thường.

## Bẫy đã đóng góp

| Ngày | Mức | Bẫy |
|---|---|---|
| 2026-11-01 | IRON | Chùm association tụ trên ngực actor tại 1 điểm (\"con nhện\") khi số hàng UC lớn |
| 2026-11-01 | HIGH | Generator tự viết bỏ qua `side` L/R, ép mọi actor về trái + không đồng bộ entry ellipse SVG ↔ draw.io |
| 2026-11-01 | HIGH | `<<include>>` "Tất toán ký quỹ" bị đọc là **bảo đảm thành công** của code hiện thực, trong khi code bắt lỗi release rồi bỏ qua — diagram = intent, không phải proof |
| 2026-11-01 | MEDIUM | Nhiều Bước 0 mâu thuẫn cùng dự án → agent chọn nhầm bản, vẽ quan hệ sai quyền (IT/Admin) |

### [IRON] Chùm association tụ trên ngực actor tại 1 điểm (\"con nhện\") khi số hàng UC lớn (2026-11-01)

- **Triệu chứng:** Sơ đồ use case fan nhiều hàng (≥9 UC): mọi dây association rời body
  actor gần như CHÍNH XÁC một điểm trên ngực → hình "con nhện / đuôi công", người dùng
  trả lại kèm nhận xét "nói từ 1 điểm thui — nói này xấu quá" (btl-cnpm, slide use case).
- **Nguyên nhân:** exit rải trong ~109px chiều cao figure chuẩn, trong khi dải hàng các UC
  chạy ±500px → góc từng dây gần bằng nhau và hội tụ về cùng một gốc. Công thức exit
  0.28..0.84 chỉ đủ khi số hàng ≤ 8. `eye_audit.py` không bắt được ở mức HIGH.
- **Sửa/phòng (làm trước khi vẽ):** kiểu **tia thẳng từ 1 điểm** (star-fan) như ảnh mẫu
  người dùng gửi: anchor `P = (ACT_X, ay + 30)` — một điểm duy nhất ở bụng actor; mọi
  association là TIA THẲNG từ P tới mép ellipse; tia từ 1 điểm KHÔNG bao giờ cắt nhau →
  quạt đều như sao. Figure giữ kích thước CHU (r13, torso 55px, arms ±24, legs tới
  +58), nhãn đặt DƯỚI figure (ay+78). CẤM rải exit dọc thân figure nhỏ (đó mới là thứ
  làm dây cắt nhau và kéo-looking "1 điểm ở cổ") và CẤM scale figure thành người khổng lồ
  (người dùng từ chối vì không giống mẫu).
- **Biến thể đã thử & bị từ chối (2026-11-01):**
  1. `TH = min(300, 150+0.42*span)` + exit 0.28..0.86 → vẫn tụ ở cổ.
  2. `TH = spanUC + 3*RY` (figure cao bằng cột UC) + exit 0.30..0.90 → người dùng nói
     "này là 1 điểm kéo ra — vẽ sai".
- **Điều kiện tái lập:** sơ đồ use case ≥ 9 hàng, một actor nối hết các UC.
- **Bằng chứng:** `private-docs/diagrams/uc-v5-nguoi-ban-audit/overlay.png` (bản star-fan)
  và ảnh mẫu người dùng gửi.

### [HIGH] Generator tự viết bỏ qua `side` L/R — ép mọi actor về một phía + neo lộn xộn (2026-11-01)

- **Triệu chứng:** Generator đọc model có trường `side` (`L`/`R`) nhưng code viết:
  `(name, indices, _)` rồi gán `x = 150` cho mọi actor — 4 vai trò (Quản trị, Vận hành, Kỹ thuật, Lãnh đạo) bị dồn hết bên trái. association neo `(x+22, y)` thay vì thân/bụng actor. SVG dùng mép trái cố định `(cx−rx, cy)` cho mọi góc còn draw.io dùng `entryX=0; entryY=0.5` — **không cùng điểm chạm ellipse**. Use case xếp một cột dọc với `y += hằng số` — nửa khung bên phải trống hoác.
- **Nguyên nhân:** generator tự viết không tuân thủ hợp đồng đã ghi trong SKILL §3.4.
- **Sửa/phiên bản sau:** Áp **Hợp đồng Generator** (§3.4 SKILL.md): giữ `side`, neo thân/bụng `exitY≈0.667`, entry ellipse tính giao điểm theo hướng cạnh đồng bộ SVG ↔ draw.io, cấm layout 1 cột duy nhất. Nếu chưa đạt → fallback vẽ tay draw.io/SVG ngay.

### [HIGH] `<<include>>` ≠ bảo đảm kết quả code hiện thực (2026-11-01)

- **Triệu chứng:** Ảnh Use Case có cạnh `<<include>>` từ "Phán quyết khiếu nại" → "Tất toán ký quỹ". Người đọc dễ hiểu là **hệ thống bảo đảm tất toán thành công**.
- **Thực tế:** Code hiện thực (`disputes.service.ts:110,115`) bắt lỗi release rồi bỏ qua; sau đó `:120` vẫn ghi `resolved` — bao gồm cả khi release thất bại. Hình vẽ đúng logic nghiệp vụ (nếu tất toán thì phán quyết), **nhưng không phải bằng chứng rằng code đã triển khai đúng**.
- **Bài học:** Diagram edge là **thiết kế intent**, không phải **proof of implementation**. Khi ghi audit, phải phân biệt rõ:
  - **PASS (semantic)** — use case + quan hệ đúng theo spec/BRD/Step 0.
  - **NOT PROOF (implementation)** — không tuyên bố "code đã đúng" chỉ vì hình include được vẽ. Muốn kiểm tra code phải đọc source + test runtime riêng.
- **Cách ghi audit:** Thêm dòng `Findings (Semantic): include có căn cứ BRD` và `Findings (Implementation): cần test riêng`; không gộp thành một câu "PASS".

### [MEDIUM] Nhiều Bước 0 mâu thuẫn cùng dự án (2026-11-01)

- **Triệu chứng:** Dự án có 2+ file `step0-*.md` với nội dung mâu thuẫn (ví dụ: `domain/step0-tmdt.md` nói IT chỉ xem cấu hình, `diagrams/step0-san-tmbt-usecase.md` lại cho IT đề xuất cấu hình). Agent chọn nhầm file → vẽ quyền sai.
- **Sửa/phòng:**
  1. Chọn **một** Bước 0 làm bản hiện hành; đánh dấu bản cũ rõ ràng (ví dụ: `step0-*.md.bak`).
  2. Không để agent tự quyết file nào là "đúng" — yêu cầu người dùng xác nhận hoặc chỉ rõ trong `CONTEXT.md`.
  3. Generator script phải đọc Bước 0 từ **một path cố định** đã thỏa thuận, không scan random.

### [IRON] Chùm association tụ trên ngực actor tại 1 điểm (\"con nhện\") khi số hàng UC lớn (2026-11-01)

- **Triệu chứng:** Sơ đồ use case fan nhiều hàng (≥9 UC): mọi dây association rời body
  actor gần như CHÍNH XÁC một điểm trên ngực → hình "con nhện / đuôi công", người dùng
  trả lại kèm nhận xét "nói từ 1 điểm thui — nói này xấu quá" (btl-cnpm, slide use case).
- **Nguyên nhân:** exit rải trong ~109px chiều cao figure chuẩn, trong khi dải hàng các UC
  chạy ±500px → góc từng dây gần bằng nhau và hội tụ về cùng một gốc. Công thức exit
  0.28..0.84 chỉ đủ khi số hàng ≤ 8. `eye_audit.py` không bắt được ở mức HIGH.
- **Sửa/phòng (làm trước khi vẽ):** kiểu **tia thẳng từ 1 điểm** (star-fan) như ảnh mẫu
  người dùng gửi: anchor `P = (ACT_X, ay + 30)` — một điểm duy nhất ở bụng actor; mọi
  association là TIA THẲNG từ P tới mép ellipse; tia từ 1 điểm KHÔNG bao giờ cắt nhau →
  quạt đều như sao. Figure giữ kích thước CHU (r13, torso 55px, arms ±24, legs tới
  +58), nhãn đặt DƯỚI figure (ay+78). CẤM rải exit dọc thân figure nhỏ (đó mới là thứ
  làm dây cắt nhau và kéo-looking "1 điểm ở cổ") và CẤM scale figure thành người khổng lồ
  (người dùng từ chối vì không giống mẫu).
- **Biến thể đã thử & bị từ chối (2026-11-01):**
  1. `TH = min(300, 150+0.42*span)` + exit 0.28..0.86 → vẫn tụ ở cổ.
  2. `TH = spanUC + 3*RY` (figure cao bằng cột UC) + exit 0.30..0.90 → người dùng nói
     "này là 1 điểm kéo ra — vẽ sai".
- **Điều kiện tái lập:** sơ đồ use case ≥ 9 hàng, một actor nối hết các UC.
- **Bằng chứng:** `private-docs/diagrams/uc-v5-nguoi-ban-audit/overlay.png` (bản star-fan)
  và ảnh mẫu người dùng gửi.
