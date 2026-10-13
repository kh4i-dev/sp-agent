---
name: anti-slop
description: Bộ lọc chống thiết kế "AI slop" cho giao diện (web/app) và bố cục thị giác (slide/deck, dashboard, landing page): gradient tím-xanh, glassmorphism tràn lan, icon-trong-ô, emoji làm hoạ tiết, card lồng card, accent dàn trải. Dùng khi người dùng yêu cầu thiết kế/làm lại UI, audit giao diện, "đừng để giống AI", "anti-slop", "unslop", "no-slop", "clean design", "trông đỡ generic", hoặc khi tạo slide/dashboard cần kiểm soát thẩm mỹ.
---

# Anti-Slop Skill — Bộ lọc chống "AI slop"

Mục tiêu: kết quả trông **được thiết kế có chủ đích**, không phải mặc định của model.
Đây là **bộ lọc**, KHÔNG phải style guide: không áp màu/font/layout cố định, chỉ chặn
những "dấu hiệu AI" và buộc mỗi quyết định thị giác phải có lý do.

> Nguồn gốc & tham chiếu đầy đủ: repo `miqdadbadjuber/anti-slop` (MIT, ~3.9k⭐) —
> hệ thống 6 skill. Bản này là bản Việt hoá, tinh gọn cho sp-agent.
> Quy tắc chi tiết theo nhóm: xem `reference/rules.md`.

## Cách dùng (bắt buộc hỏi trước)

Khi nhận việc thị giác (UI/slide/dashboard), hỏi người dùng theo ngôn ngữ của họ:

```
Bạn muốn dùng anti-slop theo kiểu nào?
1. TRONG LÚC làm — áp luật ngay khi dựng, slop không xuất hiện từ đầu.
2. SAU KHI xong — audit cái đã có: liệt kê phát hiện có số thứ tự + mức ưu tiên,
   bạn chọn số nào thì tôi sửa số đó.
```

Không bắt đầu cho tới khi họ trả lời.

- **Mode 1 (During):** theo luật trong lúc sinh; kết thúc bằng Delivery Gate.
- **Mode 2 (After):** audit dự án đã xong → sinh `anti-slop/audit-NNN-YYYY-MM-DD.md`,
  mỗi phát hiện nêu rõ luật vi phạm (R-XX) + 1 dòng lý do; ưu tiên theo tier
  (Hard Gate = HIGH, Purpose-Gate = MEDIUM, Quality Locks = LOW). **Không sửa gì**
  cho tới khi người dùng duyệt số cụ thể.

## Đây là gì (và không là gì)

- **Là filter, không phải nguồn định hướng.** Muốn kết quả "sống" cần có *direction*
  (identity, palette, typography, mood) — do người dùng cung cấp (không bịa).
- **Không cấm kỹ thuật** (gradient, glass, badge, card grid). Cấm **kỹ thuật phi mục đích**.
- Hai việc duy nhất nó làm:
  1. **Purpose test:** mỗi quyết định thị giác phục vụ điều gì? Viết lý do ra.
  2. **Liveliness bar:** kết quả phải *sống* và cụ thể, không chỉ "sạch".

## Cơ chế: Purpose Test + 3 tầng luật

Mỗi quyết định phải vượt **Purpose Test** (R-01): nêu được nó phục vụ gì. Không nêu được → bỏ.

- **Tầng 1 — Hard Gate (HIGH):** vi phạm là chặn ship.
  Ví dụ: gradient xanh→tím làm chủ đạo; số liệu/logo bịa; CTA giả; contrast không đủ.
- **Tầng 2 — Purpose-Gate (MEDIUM):** chỉ hợp lệ khi có lý do viết ra.
  Ví dụ: glass, glow, radius, shadow, texture — dùng có liều lượng + lý do.
- **Tầng 3 — Quality Locks (LOW):** tinh chỉnh/nhất quán (rhythm, spacing, state).

## "Tells" phải chặn (rút gọn)

**Màu & nền**
- Gradient xanh→tím / tím→hồng / rainbow làm màu chủ đạo, hoặc quầng sáng (glow/orb) sau hero.
- Nền tối mặc định "vì trông tech" mà không có lý do thương hiệu.
- Palette > 3 màu lõi + 1 accent; accent dàn trải khắp nơi (accent ở mọi thứ = không accent).

**Bề mặt & hình khối**
- Glassmorphism đồng loạt (navbar + card + modal + sidebar cùng blur).
- Radius "viên thuốc" cho mọi thứ; shadow to cho mọi card (trang như đang bay).
- Glow trên card/button/icon/border cùng lúc.
- Grid/dot/blueprint làm nền chỉ để "trông kỹ thuật".

**Bố cục & thành phần**
- Layout template lặp: hero → 2 CTA → screenshot → feature grid → testimonial → FAQ → CTA.
- Feature card giống hệt nhau (cùng size/icon/padding) bất kể trọng số nội dung.
- Bento grid khi mọi ô gần bằng nhau; "How It Works" luôn đúng 3 bước.
- Spacing đồng nhất mọi section (mất nhịp); icon-trong-ô vuông bo trang trí; emoji làm hoạ tiết.
- Card lồng card lồng card.

**Chữ & nội dung**
- Font serif trang trí cho body; tiêu đề hero serif mặc định (Playfair/Instrument Serif).
- Dùng emoji trong heading chuyên nghiệp; text căn giữa cho đoạn văn dài.
- Số liệu bịa ("10x faster", "500,000 founders", logo khách hàng giả) — **Hard Gate**.
- Copy rào đón/marketing rỗng: "revolutionary", "seamlessly", "unleash".

## Nguyên tắc "đối trọng" (khi có direction)

- Dùng **khoảng trắng như cấu trúc**: section pad 80–120px (không 40px); max-width ~1200–1400px.
- **Bất đối xứng** (60/40, 70/30) thay vì căn giữa mặc định; phá grid 1 lần/trang.
- Phân cấp bằng cả **họ font + weight + size + spacing + màu**, không chỉ size.
- Mỗi kỹ thuật "tốn" (glass/glow/shadow) tối đa 1–2 chỗ, có lý do.
- Chỉ **1 accent** cho khoảnh khắc quan trọng; còn lại trung tính.
- **Mọi con số/logo/testimonial phải có thật.** Không có thật → bỏ, dùng typography.

> Lưu ý: anti-slop không tự "đẹp lên" nếu thiếu direction. Kết quả nhạt = thiếu direction,
> không phải filter hỏng (R-37). Nếu người dùng chưa có định hướng, nói thẳng và đề nghị
> họ bổ sung, KHÔNG tự bịa palette/font.

## Liên quan trong sp-agent

- Văn xuôi báo cáo (chống giọng văn AI): skill `human-report-writing`.
- Trình bày slide/deck: skill `pptx-deck` (áp các tell ở đây cho bố cục slide).
- Sơ đồ: skill `plantuml-diagrams` / `diagram-orchestrator` (chuẩn trắng-đen học thuật, tránh màu mè, "hộp neo" nổi).

## DELIVERY GATE — bắt buộc trước khi ship

Chạy báo cáo PASS/FAIL 4 khối, chỉ ship khi qua hoặc đã khai báo ngoại lệ:

```text
ANTI-SLOP GATE
1. Purpose      : mọi kỹ thuật thị giác đều nêu được lý do?      PASS/FAIL
2. Hard Gate    : không còn tell tầng 1 (gradient default,
                  số liệu/logo bịa, contrast fail)?             PASS/FAIL
3. Liveliness   : có ít nhất 1 ý/chi tiết đặc trưng, không nhạt? PASS/FAIL
4. Direction    : palette/font bám direction có thật (không bịa)? PASS/FAIL
Ngoại lệ đã khai báo: ...
```

## Format phản hồi cuối

```text
Scope: <UI/slide/dashboard nào>
Mode: during | after
Tells chặn được:
- ...
Direction dùng: <nguồn: người dùng / DESIGN.md / chưa có>
Gate: PASS/FAIL (kèm ngoại lệ)
Known limitations:
- ...
```
