---
name: coord-data
description: Điều phối khối DỮ LIỆU: BẢNG TÍNH, PDF, BIỂU ĐỒ. Nạp nhanh để đọc/tạo/sửa Excel-CSV-TSV, trích/ghép/OCR PDF, vẽ biểu đồ số liệu. Gom xlsx-sheet, xlsx, pdf-toolkit, pdf, data-visualization. Từ khóa kích hoạt: Excel, bảng tính, xlsx, CSV, số liệu, biểu đồ, PDF, OCR, trích PDF, ghép PDF, matplotlib, plotly.
---

# coord-data — Điều phối khối Dữ liệu (Excel / PDF / Biểu đồ)

> Bản đồ toàn cục: `skill-coordinator`. Baseline chống mâu thuẫn: `docs/rule-conflicts.md`.

## Khi nào nạp

- Bảng tính Excel/CSV/TSV; PDF (đọc/trích/ghép/OCR/điền form); biểu đồ số liệu.

## Khối gồm

| Skill | Vai trò | Khi nào |
|---|---|---|
| `xlsx-sheet` | Bảng tính VN: công thức, định dạng, chart, recalc | Excel tổng quát |
| `xlsx` | Tạo/sửa `.xlsx` chuyên sâu + `recalc.py` | khi có công thức |
| `pdf-toolkit` | Đọc/trích/tạo/OCR/ghép PDF | PDF tổng quát |
| `pdf` | Thao tác PDF chuyên sâu (form, watermark, tách) | case nâng cao |
| `data-visualization` | matplotlib/seaborn/plotly chất lượng công bố | biểu đồ số liệu |

## Thứ tự nạp & chuỗi

```text
[Bảng tính] xlsx / xlsx-sheet → recalc.py (bắt buộc nếu có công thức) → verify giá trị
[Biểu đồ]   data-visualization → chèn vào xlsx/docx/slide
[PDF]       pdf-toolkit / pdf → trích/tạo/OCR → verify từng trang
```

## Quy ước chung

- **Recalc bắt buộc** khi file có công thức; **ngoại lệ**: file Power Query/custom XML → KHÔNG recalc, hỏi người dùng.
- Không bịa số liệu; ghi nguồn cho số hardcoded.

## Anti-patterns

- ❌ Hardcode kết quả thay vì công thức.
- ❌ Recalc file Power Query/custom XML (làm hỏng).
- ❌ Tin exit-code xanh là workbook đúng.

## Definition of Done

```text
[ ] Công thức đúng + đã recalc (hoặc nêu rõ ngoại lệ).
[ ] PDF/ảnh đã kiểm từng trang.
[ ] Số liệu có nguồn, không bịa.
```
