# Directory Contract — Chi Tiết Hợp Đồng Thư Mục Diagram Pack

> SSOT rút gọn nằm trong [`../SKILL.md`](../SKILL.md) §1. File này là bản chi tiết: quy tắc naming,
> luật cặp 1:1, cấu trúc audit, quy tắc docx-swap, và những điều CẤM.

## 1. Cây chuẩn (canonical tree)

```
<TARGET>/                                # 1 thư mục duy nhất, mọi thứ nằm dưới đây
├── domain/                              # Bước 0
│   └── step0-<du-an>.md                 # bài toán, quy mô, tác nhân + nguồn bằng chứng
├── diagrams/                            # SOURCE — nơi MỌI sửa bắt đầu
│   ├── gen_<loai>_svg.py | gen_<loai>_draw.py   # generators
│   ├── svg_render.py                    # SVG -> PNG (Chrome headless, giữ dấu tiếng Việt)
│   ├── check_overlap.py | check_cross.py # kiểm tra đè/chồng nhanh
│   ├── <loai>-model.md                  # mô hình UML (Bước 1)
│   ├── <loai>-layout.md                 # bảng layout (Bước 2.2)
│   └── <loai>-master.md                 # bản chốt (nếu có)
├── images/
│   └── diagrams/                        # OUTPUT — chỉ ảnh render, KHÔNG sửa tay
│       ├── <ten>.svg                    # vector (chèn Word/PDF)
│       ├── <ten>.png                    # raster 2.2x (chèn PPTX, xem nhanh)
│       └── _legacy/                     # ảnh cũ, KHÔNG nhúng, KHÔNG đụng
├── audit/
│   └── soi-so-do/                       # dấu vết soi mắt (proof-of-view)
│       ├── README.md                    # tổng hợp việc đã làm + verdict
│       ├── truoc-khi-sua/<ten>/         # đợt 1: overlay + crops bản CŨ
│       └── sau-khi-sua/<ten>/           # đợt 2: overlay + crops bản ĐÃ SỬA
├── tools/                               # script bổ trợ của DỰ ÁN (khác tools/ của sp-agent)
└── _legacy/                             # tài liệu đời cũ, KHÔNG chạy
```

## 2. Quy tắc naming

1. **Kebab-case cho tiền tố loại** (`usecase-`, `act-`, `seq-`, `state-`, `flow-`); snake_case chấp nhận
   cho tiền tố loại dùng `_` (`erd_01_...`) — giữ nguyên theo pack hiện có, KHÔNG đổi tên hàng loạt.
2. **Số thứ tự** dùng để giữ thứ tự chương: `33a..33d` (use case theo phân hệ), `01..06` (act/flow),
   `34..39` (seq theo mã nghiệp vụ), `erd_01..erd_06` (theo miền dữ liệu).
3. **Phần mô tả**: tiếng Việt không dấu, ngắn, phân tách bằng `-` (hoặc `_` với erd).
4. **Cặp 1:1**: `X.svg` ⇔ `X.png` cùng basename. Không ngoại lệ ngoài `_legacy/`.
5. **Không nhúng số chương Word vào tên file** (`3.3a-...` là sai; dùng `33a-...`) — dấu chấm gây rối
   khi sort và khi grep.

## 3. Luật cặp 1:1 (chi tiết)

| Trường hợp | Hành vi |
|---|---|
| Có `.svg` thiếu `.png` | **LỖI** — chạy lại renderer (`svg_render.py`) cho file đó |
| Có `.png` thiếu `.svg` | **LỖI** — tìm nguồn; nếu png là bản tay cũ → chuyển vào `images/diagrams/_legacy/` |
| Đổi tên một trong hai | **CẤM** tự do — đổi cả cặp trong cùng một commit, cập nhật link trong docx/pptx |
| Kích thước W/H thay đổi | **CẢNH BÁO** — nếu ảnh đang nằm trong docx, `wp:extent` phải sửa theo; giữ canvas nếu chỉ sửa layout |

`check_pack.py` tự quét cặp 1:1 (bỏ qua `_legacy/`, `__pycache__/`) và in bảng orphan.

## 4. Cấu trúc audit (chi tiết)

Mỗi thư mục audit của một hình phải có **đủ 3 thứ**:

```
<ten>/
├── eye-audit.md      # bảng ứng viên: mã (L-ACTORNAME...), zoom path, "mắt thấy gì", verdict
├── overlay.png       # lưới 10×10 + trục giữa đỏ (soi căn trục/nhịp)
└── crops/
    ├── F01-<MA>.png  # zoom 4× từng vùng nghi vấn
    └── ...
```

- `eye-audit.md` **phải điền tay** cột verdict (`THẬT` / `BÁO OÁN` / `CHẤP NHẬN ĐƯỢC`) — script chỉ liệt kê.
- Đợt sửa thứ N đặt tên: `truoc-khi-sua/`, `sau-khi-sua/`, hoặc `-v2/`, `-lan2/`... (đặt tên có ý nghĩa,
  đừng `temp/`, `new/`).
- `README.md` cấp `soi-so-do/` ghi: lệnh đã chạy, số đo parser (node/label/edge/actor), tổng ứng viên
  trước/sau, những lỗi đã sửa và cách sửa — như file `soi-so-do/README.md` của pack btl-cnpm (bản mẫu chuẩn, lưu trong dự án đó).

## 5. Render pipeline (chuẩn tiếng Việt)

```
generator (gen_*.py)  ──sinh──▶  <ten>.svg  ──svg_render.py (Chrome headless + PyMuPDF)──▶  <ten>.png
        │                              │
        └── đặt trong diagrams/        └── cả 2 file nằm trong images/diagrams/
```

- **CẤM CairoSVG** cho tiếng Việt: glyph có dấu lấy font khác → một dòng chữ trộn hai kiểu nét
  (bài học thật 27/10/2026, xem `btl-cnpm/private-docs/diagrams/svg_render.py` header).
- Chrome headless qua CDP `Page.printToPDF` → PyMuPDF rasterize `zoom = scale * 4/3` → đúng
  `W*scale × H*scale` px, khớp `wp:extent` cũ trong DOCX.
- Nếu thiếu Node/Chrome → `svg_render.py` tụt xuống CairoSVG + **in cảnh báo**; khi đó **bắt buộc soi
  kỹ dấu tiếng Việt** ở zoom 4× trước khi bàn giao.

## 6. Docx-swap (khi ảnh đã nghiệm thu)

1. Giữ `W`/`H` canvas SVG không đổi → ảnh cùng kích thước px → `wp:extent` trong DOCX không phải sửa.
2. Dùng `safe-docx-modifier` (ZIP Swap) thay ảnh nhị phân in-place; **không** sinh lại docx từ đầu.
3. Caption do `docx-report` quản (`Hình X.Y: ...`); sơ đồ **không** nhúng title trong ảnh.
4. Sau swap: render trang Word ra PDF/ảnh và **mở soi trang thật** (luật render gate của docx-report).

## 7. Những điều CẤM (bất biến của pack)

1. CẤM sửa trực tiếp `.svg`/`.png` trong `images/diagrams/` — mọi thay đổi phải đi qua source ở `diagrams/`.
2. CẤM xoá `_legacy/` hoặc đổi tên hàng loạt nếu không có yêu cầu tường minh.
3. CẤM đặt script lẻ ở root `<TARGET>/` — script công cụ vào `tools/`, generator vào `diagrams/`.
4. CẤM để `__pycache__/` thành phần của pack — xoá được, `check_pack.py` bỏ qua.
5. CẤM dùng màu trong sơ đồ học thuật (zero-color); chỉ `lucid-blue` khi user yêu cầu tường minh cho slide
   (ghi `override-monochrome` vào audit).
6. CẤM tuyên bố "đã soi" khi chưa mở `overlay.png` + **mọi** `crops/`.
7. CẤM gen lại toàn bộ pack khi chỉ 1 hình cần sửa (minimal patch + re-render hình đó).

## 8. Pack mẫu (canonical example)

`E:\HOC TAP\my-project\btl-cnpm\private-docs` — pack đạt chuẩn:

- `diagrams/`: 7 generator (`gen_usecase_draw.py`, `gen_activity_svg.py`, `gen_flow_svg.py`,
  `gen_sequence_svg.py`, `gen_state_svg.py`, `gen_modules_svg.py`, `gen_erd_svg.py`) + `svg_render.py`
  + `check_overlap.py` + 7 tài liệu model/layout/audit md.
- `images/diagrams/`: 20 cặp `.svg`+`.png` (4 use case, 6 activity, 2 flow, 6 seq, 1 state, 1 modules,
  6 ERD — tổng 26 file ảnh ở 20 tên hiển thị; chính xác: 26 cặp render sau 27/10).
- `audit/soi-so-do/`: `truoc-khi-sua/33a..33d/` + `sau-khi-sua/33a..33d/` — 3 lỗi thật phát hiện
  (2 nhãn tràn 109%, 11 đường cắt tên tác nhân, font dấu tiếng Việt) → sửa trong generator → soi lại sạch.
- `domain/step0-tmdt.md`: 7 tác nhân đã xác minh.

Chạy kiểm tra pack mẫu:

```bash
py -3 "<sp-agent>/.claude/skills/diagram-pack/scripts/check_pack.py" "E:\HOC TAP\my-project\btl-cnpm\private-docs"
```
