# Phần đầu tài liệu TNUT — 2 định dạng (Đồ án vs Báo cáo bài tập lớn)

Trường ĐH Kỹ thuật Công nghiệp (TNUT) dùng **hai định dạng khác nhau** cho phần bìa/phần đầu.
Trước khi sinh bìa, **BẮT BUỘC hỏi người dùng chọn loại nào** (không tự đoán):

| | `--kind doan` — Đồ án PTTKHT | `--kind btl` — Báo cáo bài tập lớn |
|---|---|---|
| Tiêu đề lớn trên bìa | **ĐỒ ÁN PHÂN TÍCH THIẾT KẾ HỆ THỐNG** | **BÁO CÁO BÀI TẬP LỚN** |
| Dòng phụ | — | **MÔN HỌC: …**, **NĂM HỌC: …** |
| Trang thứ 3 | NHIỆM VỤ THIẾT KẾ ĐỒ ÁN PTTKHT HỆ THỐNG | NHIỆM VỤ BÀI TẬP LỚN (+ dòng Môn học) |
| Khối thông tin | GVHD / SV / LỚP / MSSV / NGÀNH / HỆ | GVHD / SV / LỚP / MSSV (+ môn học) |
| Viền trang hoa văn | Bìa chính + Bìa lót | Bìa chính + Bìa lót |
| Cấu trúc thân | 13 phần (Bìa, Bìa lót, Nhiệm vụ, Phiếu điểm, Phiếu thông qua, Mục lục, Lời cam đoan, Danh mục từ viết tắt, Danh mục bảng/hình, Lời nói đầu, Chương, Kết luận, TLTK) | Bìa + Bìa lót + (Mục lục) + Chương; phần đầu gọn hơn |

> Cả hai đều dùng **Times New Roman**, khung viền `thinThickSmallGap`/`thickThinSmallGap`, logo TNUT.

## Sinh phần đầu

```bash
# Đồ án PTTKHT
python scripts/make_cover.py --kind doan --out bia.docx \
    --topic "TÊN ĐỀ TÀI" --gvhd "ThS.Nguyễn Văn B" \
    --sv "Nguyễn Văn A" --lop "K59KMT" --mssv "K235480106022" \
    --khoa-dao-tao "2022-2026" --year 2026

# Báo cáo bài tập lớn
python scripts/make_cover.py --kind btl --out bia.docx \
    --mon-hoc "CÔNG NGHỆ PHẦN MỀM" --nam-hoc "2025-2026" \
    --topic "TÊN ĐỀ TÀI" --gvhd "ThS.Nguyễn Văn B" \
    --sv "Nguyễn Văn A" --lop "K59KMT" --mssv "K235480106022" --year 2026

# Ghép phần đầu lên ĐẦU một báo cáo có sẵn (giữ nguyên nội dung báo cáo)
python scripts/make_cover.py --kind btl --prepend-to report.docx -o report_full.docx --data data.json
```

## Trường dữ liệu (`--data data.json`)

> **KHÔNG hardcode tên SV/GV.** Các trường `de_tai`, `gvhd`, `sinh_vien`, `lop`, `mssv`
> (+ `mon_hoc` nếu BTL) là **BẮT BUỘC** — thiếu thì `make_cover.py` **báo lỗi**.
> Phải **hỏi người dùng từng câu một** (kiểu `grill-me`) rồi mới chạy.

```json
{
  "kind": "doan",
  "tieu_de": "",                          // bỏ trống -> suy theo kind
  "truong": "TRƯỜNG ĐẠI HỌC KỸ THUẬT CÔNG NGHIỆP",
  "khoa": "KHOA ĐIỆN TỬ",
  "bo_mon": "CÔNG NGHỆ THÔNG TIN",
  "mon_hoc": "",                          // tên môn (BTL)
  "nganh": "KỸ THUẬT MÁY TÍNH",
  "he": "ĐẠI HỌC CHÍNH QUY",
  "de_tai": "...", "gvhd": "...", "sinh_vien": "...",
  "lop": "K59KMT", "mssv": "...",
  "khoa_dao_tao": "2022-2026", "nam_hoc": "2025-2026", "nam": 2026,
  "ngay_giao": "08/09/2025", "ngay_hoan_thanh": "25/10/2025",
  "logo": "<đường dẫn logo; mặc định assets/tnut-logo.png>"
}
```

## Cờ dòng lệnh tương ứng

`--kind`, `--tieu-de`, `--truong`, `--khoa-donvi`, `--bo-mon`, `--mon-hoc`, `--nganh`, `--he`,
`--topic`, `--gvhd`, `--sv`, `--lop`, `--mssv`, `--khoa-dao-tao`, `--nam-hoc`,
`--ngay-giao`, `--ngay-ht`, `--year`, `--logo`, `--out`, `--prepend-to`, `-o`, `--data`.

> **Lưu ý đặt tên cờ**: `--khoa-donvi` = đơn vị/khoa (VD "KHOA ĐIỆN TỬ") — **KHÁC** `--khoa-dao-tao`
> = niên khóa (VD "2022-2026"). Đừng nhầm (đây từng gây lỗi "2019-2024" in dưới tên trường).

## Sau khi ghép bìa

Bìa không có số trang. Muốn thân báo cáo đánh số lại từ 1, chạy tiếp bộ đánh số phần đầu:

```bash
python scripts/edit_docx.py report_full.docx --cover-end "LỜI CAM ĐOAN" --body-start "MỞ ĐẦU"
```
