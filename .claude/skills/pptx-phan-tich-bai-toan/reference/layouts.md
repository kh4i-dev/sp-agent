# Layouts & kiểu chữ — pptx-phan-tich-bai-toan

Kích thước slide **16:9 = 13,333 × 7,5 in**. Lề ngang `M = 0,62"`, vùng nội dung `CW = 12,093"`.
Tiêu đề kết thúc quanh `y ≈ 1,10"` (có kicker) hoặc `y ≈ 0,44"` (không kicker). Footer ở `y = 7,08"`.

## Bảng màu (học thuật — nền sáng, 1 màu chủ đạo + 1 accent)

| Vai trò | Mã | Dùng cho |
|---|---|---|
| `ink` | `#122F38` | Tiêu đề, chữ nhấn |
| `body` | `#2E4A54` | Chữ thường |
| `muted` | `#6C848E` | Phụ đề, nguồn, footer, số trang |
| `brand` | `#0E7490` | Số liệu, nhãn, kicker, marker |
| `brand_dk` | `#0A4E60` | Nền section, thanh tiêu đề bảng so sánh |
| `brand_soft` | `#E9F3F6` | Nền phụ (card nhấn, chip mới) |
| `surface` | `#F5F9FA` | Nền thẻ, dòng bảng so le |
| `line` | `#D7E4EA` | Đường kẻ hairline |
| `good` / `good_soft` | `#1B7F4B` / `#EAF6EE` | Khối "Ưu điểm" |
| `bad` / `bad_soft` | `#B42318` / `#FBECEA` | Khối "Nhược điểm" |
| `warn` / `warn_soft` | `#A45A03` / `#FBF1E4` | Cảnh báo (ít dùng) |

**Chỉ 1 màu nhấn** mỗi slide. Không gradient. Không bóng. Không viền nhiều màu.

## Kiểu chữ

| Thành phần | Font | Cỡ | Ghi chú |
|---|---|---|---|
| Tiêu đề slide | Arial | 25 | bold, line 1,0 — **câu khẳng định**, không gạch chân |
| Kicker (nhãn nhỏ) | Arial | 11,5 | chữ thường, màu `brand` |
| Dẫn đề (lead) | Times New Roman | 14–14,5 | line 1,25 |
| Thân / bullet | Times New Roman | 15–15,5 | line 1,18 |
| Thân thẻ (cards) | Times New Roman | 13,5 | line 1,32 |
| Bảng | Times New Roman | 12,5 | header Arial bold nền `brand_soft` |
| Số liệu KPI | Arial | 38 | bold, màu `brand` |
| Chú thích/nguồn | Times New Roman | 10,5 | nghiêng, màu `muted` |

**Tuyệt đối không < 9pt.** Font ngoài danh sách an toàn (Arial/Times New Roman/Calibri/
Cambria) sẽ bị thay thế khi render → lỗi dấu tiếng Việt.

## Quy tắc từng layout

| Layout | Field bắt buộc | Cap nội dung | Trang trí |
|---|---|---|---|
| `cover` | `title`, `meta_lines` | tiêu đề ≤ 18 từ; 3–4 dòng meta | dải nền nhạt phải + **ảnh thật** |
| `agenda` | `items[]` | 4 mục (2×2), mỗi mục `text` + `sub` | số thứ tự mờ 26pt + khối nền `surface` |
| `kpi` | `items[{value,label}]`, `source` | 2–4 chỉ số; label ≤ 14 từ | số lớn + hairline; **nguồn bắt buộc** |
| `cards` | `items[{title,body}]` | 3 thẻ; body ≤ 25 từ | số 01/02/03 mờ + khối `surface` |
| `flow` | `steps[{text,sub}]` | 3–6 bước | chevron mũi tên native, tô nhạt dần |
| `bullets` | `items[]` | ≤ 6 ý; mỗi ý ≤ 10 từ | ô vuông marker native |
| `split` | `items[]`, `image` | chữ ≤ 5 ý; ảnh 16:9 | khung ảnh bo góc hairline |
| `table` | `columns[]`, `rows[][]` | ≤ 8 dòng × ≤ 4 cột | header `brand_soft`, dòng so le, cột đầu đậm |
| `compare` | `plans[{name,pros,cons}]` | 2 phương án; ≤ 4 ý/khối; ≤ 10 từ/ý | 2 khối ưu/nhược tô `good_soft`/`bad_soft` |
| `chips` | `items[{code,text}]` | ≤ 14 ô (2 hàng × 7) | chip `surface`; ô "mới" `brand_soft` |
| `diagram` | `image`, `caption` | 1 sơ đồ CHÍNH | full chiều rộng, caption nguồn dưới |
| `section` | `title`, `kicker` | 1 câu dẫn | nền `brand_dk`, vạch dọc nhấn |
| `closing` | `title` | 1 câu chốt | dải màu trên + căn giữa |

## Field tuỳ chọn hay dùng

`kicker` (nhãn nhỏ trên tiêu đề), `lead` (câu dẫn dưới tiêu đề), `caption` (nguồn/chú thích),
`source` (nguồn số liệu), `legend` (chú giải chip), `widths` (tỉ lệ cột bảng),
`font_size` (cỡ chữ bảng), `cols` (số cột chip), `bold_first` (đậm cột 1 của bảng).

## Z-order & layer

- Ảnh có **khung hairline** chèn xuống dưới ảnh → khi sửa, khung không che ảnh.
- Mỗi shape được **đặt tên** (`card_1`, `kpi_num_2`, `cmp_pros_1`, `flow_arrow_3`…) để chọn
  đúng layer trong PowerPoint (Home → Select → Selection Pane).
- Muốn đổi nhanh cả bộ: sửa JSON rồi sinh lại. Muốn chỉnh lẻ: sửa trực tiếp layer trong PowerPoint.
