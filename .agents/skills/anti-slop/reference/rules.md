# Anti-Slop — Quy tắc chi tiết

> Tinh gọn từ repo `miqdadbadjuber/anti-slop` (MIT) — hệ thống core + 5 skill con:
> `antislop` (core), `antislop-ui`, `antislop-copywriting`, `antislop-human`,
> `antislop-layoutmobile`, `antislop-code`. Bản dưới là bản Việt hoá, gộp cho sp-agent.
> Đối chiếu upstream: https://github.com/miqdadbadjuber/anti-slop

## 1. Ba tầng luật

| Tier | Mức | Ý nghĩa | Ví dụ |
|---|---|---|---|
| Hard Gate | HIGH | Vi phạm = chặn ship | gradient default, số liệu/logo bịa, contrast fail, CTA giả |
| Purpose-Gate | MEDIUM | Chỉ hợp lệ khi có lý do viết ra | glass, glow, radius, shadow, texture, motion |
| Quality Locks | LOW | Tinh chỉnh, nhất quán | rhythm, spacing scale, state, accessibility |

**Purpose Test (R-01):** mỗi kỹ thuật thị giác phải trả lời "nó phục vụ gì". Không trả lời được → cắt.

## 2. UI / thị giác (`antislop-ui`)

Mỗi mục có dạng **Tell** (dấu hiệu) → **Why** (vì sao là slop) → **Fix**.

### Màu & nền
- **Gradient xanh→tím (blue-purple)** — xử lý màu phổ biến nhất trong training data → tín hiệu
  "không có brand". Fix: lấy palette từ identity; gradient chỉ giữ khi là chức năng phân cấp, có lý do (R-01).
- **Glassmorphism tràn lan** — blur làm mất texture, mọi bề mặt cùng một lớp sương → mất phân cấp.
  Fix: glass là accent, tối đa 1–2 phần tử (R-10).
- **Radius viên thuốc mọi nơi** — xoá ngôn ngữ "đây là input/đây là card". Fix: bộ radius nhỏ, áp có chủ đích (R-11).
- **Shadow mềm khắp nơi** — mọi thứ nổi thì không gì nổi. Fix: shadow chỉ đánh dấu elevation có lý do (R-12).
- **Glow mọi nơi** — khuếch đại sự chú ý mà không có gì để chú ý. Fix: glow tối đa 1–2 phần tử (R-13).
- **Nền grid/blueprint** — "trông kỹ thuật" mà không làm việc thật. Fix: texture chỉ khi phục vụ identity (R-07).
- **Dark mode mặc định vô cớ** — dark là quyết định, không phải default. Fix: chọn theme từ brand/product/audience (R-21).
- **Palette > 3 màu lõi**; **accent dàn trải**. Fix: 2–3 màu lõi + 1 accent (R-29); accent chỉ ở khoảnh khắc quan trọng.

### Bố cục & thành phần
- **Layout template lặp** (hero→CTA→screenshot→features→testimonial→FAQ→CTA). Fix: dựng theo nhu cầu nội dung (R-05).
- **Feature card đồng nhất** — mọi feature trông bằng nhau. Fix: biến thiên theo trọng số nội dung (R-14).
- **Bento grid** chỉ đúng khi nội dung thật sự có ô khác cỡ (R-05).
- **Spacing đồng nhất** — mất nhịp. Fix: tạo spacing scale, dùng nhiều mức; whitespace là cấu trúc.
- **"How It Works" luôn 3 bước** — ép quy trình vào khuôn. Fix: trình bày đúng như thực tế.
- **"Trusted By" logo bar** — claim niềm tin không bằng chứng (thường là logo bịa).

### Motion
- Entrance animation cho mọi thứ → chậm, giả. Chỉ animate có mục đích, tôn trọng `prefers-reduced-motion`.

## 3. Copy / văn bản (`antislop-copywriting`)

- **Headline rỗng** ("Revolutionize your workflow") — thay bằng lợi ích cụ thể.
- **CTA mơ hồ** ("Get Started", "Learn More") ở mọi nút — CTA phải nói rõ hành động & kết quả.
- **Số liệu/khách hàng bịa** ("Trusted by 500,000 founders") — **Hard Gate**, phải có thật hoặc bỏ.
- **Từ ngữ sáo** ("seamlessly", "unleash", "next-gen", "cutting-edge") — cắt.
- **Markdown hygiene**: không lạm dụng emoji/caps lock trong heading chuyên nghiệp.

## 4. Con người / accessibility (`antislop-human`)

- Contrast đủ (text thường ≥ 4.5:1; chữ lớn ≥ 3:1); không dùng màu làm tín hiệu duy nhất.
- Keyboard: focus visible, thứ tự tab hợp lý; mọi control có state (hover/focus/active/disabled/error).
- Không mất nội dung khi zoom/đổi font.

## 5. Mobile / responsive (`antislop-layoutmobile`)

- Breakpoint có chủ đích; tap target ≥ 44×44px; không tràn ngang.
- Grid/flex co giãn đúng; không dùng fixed width cứng.

## 6. Code comment (`antislop-code`)

- Xoá comment "slop" của AI (`# Initialize the variable`, comment lặp lại code).
- Giữ comment giải thích **why**, không phải **what**. Không sửa code khi chỉ dọn comment.

## 7. Liveliness Toolkit — để không "sạch mà chết"

Ba "núm" điều chỉnh cùng **Design Read** (đọc ngữ cảnh):

- **ENERGY** — mức táo bạo của bố cục/tương phản (1 = tối giản, 5 = táo bạo).
- **RHYTHM** — mức biến thiên nhịp giữa các section (1 = đều, đây là lựa chọn có chủ đích; 3+ = thấy rõ khác biệt).
- **MOTION** — mức chuyển động (1 = gần như tĩnh; giữ tôn trọng reduced-motion).

**R-37:** kết quả không có direction phải gắn nhãn *"draft without direction"* với dial 1/1/1 — không phải sản phẩm ship được.

## 8. Checklist nhanh (dùng khi tự soi)

```text
[ ] Không có gradient xanh→tím / orb / glow làm mặc định
[ ] Palette ≤ 3 màu lõi + 1 accent; accent xuất hiện có điểm nhấn
[ ] Glass/glow/radius/shadow: có lý do, liều lượng ≤ 1–2
[ ] Layout theo nội dung, không theo template; có ít nhất 1 chỗ phá đối xứng
[ ] Spacing có scale & nhịp; heading/paragraph có tỉ lệ hợp lý
[ ] Không số liệu/logo/testimonial bịa
[ ] Copy cụ thể, không sáo; CTA nói rõ hành động
[ ] Contrast đủ; keyboard/focus/state đầy đủ
[ ] Có "second-read moment" (một chi tiết đặc trưng đáng nhớ)
```
