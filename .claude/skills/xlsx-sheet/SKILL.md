---
name: xlsx-sheet
description: Tạo, đọc và sửa bảng tính Excel (.xlsx): công thức, định dạng bảng, biểu đồ, và tính lại công thức để tránh giá trị rỗng. Dùng khi người dùng cần bảng tính, Excel, XLSX, số liệu, dashboard, biểu đồ Excel, hoặc nhắc tới openpyxl, xlsxwriter, pandas, recalculation.
---

# XLSX Sheet Skill

Mục tiêu: file `.xlsx` **công thức có giá trị đúng** (đã recalc) và định dạng rõ ràng.

## Khi nào dùng

- Tạo bảng số liệu/ báo cáo Excel từ dữ liệu.
- Đọc/ghi dữ liệu, thêm sheet, định dạng bảng.
- Thêm biểu đồ Excel.
- Sửa file có sẵn mà giữ công thức.

## Toolchain

| Việc | Thư viện | Ghi chú |
|---|---|---|
| Đọc/ghi, giữ công thức | **openpyxl** | linh hoạt; formula là string, không có cached value |
| Tạo mới hiệu năng cao | **xlsxwriter** | nhanh; write-only, không đọc lại |
| Đọc dữ liệu/phân tích | **pandas** (`read_excel`) | cần giá trị đã cache |
| Recalc công thức | **LibreOffice headless** | bắt buộc trước khi ship |

```bash
pip install openpyxl xlsxwriter pandas
```

## Quy tắc vàng

- **Công thức phải được recalc** trước khi giao: openpyxl/xlsxwriter ghi công thức dưới dạng chuỗi,
  nhiều công cụ đọc (pandas, preview) sẽ thấy **rỗng/None/0** nếu chưa có cached value.
- openpyxl: `data_only=True` trả `None` cho tới khi có engine recalc.
- xlsxwriter: lưu cached result `0` và bật cờ recalc-on-open; truyền tham số thứ 4 của `write_formula` để đặt giá trị cache thật.
- `strings_to_formulas` mặc định BẬT — chuỗi bắt đầu bằng `=` sẽ bị biến thành công thức.
- KHÔNG recalc file có Power Query/custom XML do người khác bảo trì (dễ hỏng).

## Recalc bằng LibreOffice

```bash
python scripts/recalc_xlsx.py report.xlsx
# tương đương: soffice --headless --convert-to xlsx:"Calc MS Excel 2007 XML" report.xlsx
#              với OOXMLRecalcMode=0
```

Sau recalc, đọc kiểm tra lại:

```python
import pandas as pd
df = pd.read_excel("report.xlsx", sheet_name=None)
for name, sheet in df.items():
    print(name, sheet.shape)
```

## Định dạng & biểu đồ

- Header đậm, freeze panes, độ rộng cột hợp lý, định dạng số (`#,##0`), ngày chuẩn.
- Biểu đồ native (openpyxl `BarChart`/`LineChart`/`PieChart`) — có thể sửa trong Excel.
- Bảng dài: dùng `Table`/auto-filter; không tô quá nhiều màu.

## Pitfalls

- Formula cache rỗng → pandas/preview đọc blank → luôn recalc.
- Sheet name: tối đa 31 ký tự, không chứa `: \ / ? * [ ]`.
- Số lớn/năm bị hiểu thành ngày — set `number_format` đúng.
- openpyxl không tính toán công thức; nó chỉ lưu công thức.

## Format phản hồi cuối

```text
File: <report.xlsx>
Sheets: <list>
Formulas: N (recalculated: yes/no)
Charts: N
QA: recalc PASS/FAIL — đọc lại PASS/FAIL
```
