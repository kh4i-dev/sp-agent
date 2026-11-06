# Khung nội dung "Sổ tay dự án" + quy ước bảng Đầu vào – Xử lý – Đầu ra

> SSOT cho skill `project-handbook`. Dùng làm khuôn khi viết tài liệu giúp **người khác**
> (giảng viên, người bảo trì, thành viên mới) hiểu **trọn** một dự án.

---

## Định dạng & màu — luật cứng trước khi viết

Tài liệu này là **tài liệu kỹ thuật/học thuật**: chữ **đen**, nền **trắng**, phân cấp bằng
**cỡ chữ + độ đậm + đường kẻ + nền xám**, nhấn mạnh bằng **highlight** (`==chữ==`).
**Cấm chữ màu** (xanh theme, đỏ, cam…). Đồng bộ luật của khối tài liệu (`docx-report`).

- ❌ Chữ xanh cho tiêu đề, chữ đỏ cho cảnh báo, chữ xanh lá cho code.
- ✅ Tiêu đề **đậm** + đường kẻ dưới; cảnh báo trong khối `>` có nền xám + gạch dọc đen;
  code trong khối nền xám; chỗ cần nhấn thì `==highlight==`.
- Vì sao: bản in đen trắng vẫn phải đọc được, và tài liệu "tô màu mè" là dấu hiệu văn do AI sinh.
- Kiểm bằng máy: `python scripts/check_pdf_monochrome.py <out.pdf>` → phải in `SACH`.
  Và tự kiểm bằng mắt trên trang bìa + 1 trang có bảng.

---

## 0. Ba nguyên tắc bất di bất dịch

1. **Nguồn sự thật là MÃ NGUỒN, không phải slide/báo cáo cũ.**
   Trước khi viết bất kỳ dòng nào về nghiệp vụ, phải đọc file thật trong `src/` và ghi lại
   `đường/dẫn/file.ts:dòng` làm bằng chứng. Tài liệu cũ thường lệch (đã từng lệch luật giải ngân
   giữa slide và code). Nếu code và tài liệu cũ mâu thuẫn → **ghi rõ mâu thuẫn**, không im lặng chọn một.
2. **Mọi khẳng định phải truy được về một chỗ trong code** (hàm, endpoint, hằng số, câu lệnh SQL/ORM).
   Câu không truy được = câu phải xoá hoặc đánh dấu `UNKNOWN — cần xác minh`.
3. **Nói thẳng phần chưa xong.** Có mục "Hạn chế đã biết" riêng, liệt kê lỗi/thiếu sót kèm hướng sửa.
   Một tài liệu giấu khuyết điểm là tài liệu **sai**, vì người đọc sẽ tin và làm theo.

---

## 1. Khung nội dung chuẩn (bắt buộc đủ 4 phần)

```
PHẦN I  — HIỂU DỰ ÁN TRONG 5 PHÚT
  1. Dự án giải bài toán gì, cho ai, không làm gì (ranh giới)
  2. Bảng thuật ngữ (term → nghĩa trong dự án này)  ← bắt buộc, đây là thứ chặn hiểu nhầm
  3. Sơ đồ tổng thể (1 hình): các khối, ai gọi ai
  4. Cách chạy thử trong 5 lệnh

PHẦN II — LUỒNG NGHIỆP VỤ TỪ ĐẦU ĐẾN CUỐI
  5. Bản đồ trạng thái (máy trạng thái + bảng chuyển đổi hợp lệ)
  6. Đường đi của tiền / dữ liệu chính (nếu có nghiệp vụ tài chính)
  7. Ví dụ số thật lấy từ dữ liệu mẫu (một ca hoàn hảo, tính tay được)

PHẦN III — ĐẶC TẢ TỪNG TRƯỜNG HỢP  ← phần nặng nhất, xem §2
  8. Nhóm theo TÁC NHÂN (không nhóm theo menu giao diện)
  9. Mỗi trường hợp = 1 bảng Đầu vào / Xử lý hệ thống / Đầu ra + nhánh lỗi
 10. Kịch bản chạy suốt ("kể chuyện") 8–15 ca, mỗi ca là một chuỗi thao tác → số cuối cùng

PHẦN IV — TRA CỨU & TIN CẬY
 11. Bảng tra mã lỗi (mã → nghĩa → người dùng thấy gì)
 12. Hạn chế đã biết + hướng sửa
 13. Bảng kiểm "đã phủ hết chưa" (mỗi dòng có ✅/❌ + nơi tra)
 14. Phụ lục: danh mục endpoint, danh mục hằng số cấu hình
```

**Độ dài hợp lý:** 25–80 trang A4 cho một đồ án cỡ vừa. Ngắn hơn thì thường là **mỏng** (thiếu
trường hợp lỗi và thiếu ví dụ số); dài hơn thì thường là **dán code**.

---

## 2. Quy ước bảng Đầu vào – Xử lý – Đầu ra

Đây là định dạng được yêu cầu nhiều nhất khi bảo vệ, và cũng là định dạng dễ viết ẩu nhất.
Làm đúng theo 6 quy tắc sau.

### 2.1. Mỗi trường hợp là một bảng 3 dòng + 1 dòng nhánh lỗi

```markdown
### A·7 — Đặt hàng «include» Giữ tiền ký quỹ

| | |
|---|---|
| **Đầu vào** | `POST /orders/checkout` — `address_id`, `payment_method` |
| **Xử lý hệ thống** | ① ... ② ... ③ ... |
| **Đầu ra** | Trạng thái đơn, số dư ví, hiệu ứng dữ liệu |
| **Nhánh lỗi** | `CART_EMPTY` · `OUT_OF_STOCK` · ... |
```

Quy tắc:

1. **Đầu vào phải cụ thể**: tên endpoint/hàm + **danh sách tham số**, không viết "người dùng bấm nút".
2. **Xử lý hệ thống đánh số ①②③ theo đúng thứ tự code chạy**, mỗi bước nêu **hệ quả dữ liệu**
   ("đặt `status='paid'`", "giảm `stock`"), không nêu cảm giác ("hệ thống kiểm tra rồi xử lý").
3. **Nói rõ MỘT TRANSACTION hay nhiều**: chỗ nào atomic thì ghi đậm — đây là chi tiết kỹ thuật ăn điểm.
4. **Đầu ra phải nêu hiệu ứng quan sát được**: mã HTTP, trạng thái bản ghi, **số dư/thay đổi số**.
   Tránh "trả về thành công".
5. **Nhánh lỗi là bắt buộc và phải là MÃ**, không phải câu chữ: `STATE_CONFLICT`, `NOT_PICKED_UP`…
   Mã lỗi phải lấy từ code (đối chiếu file xử lý lỗi toàn cục để biết mã nào ra HTTP nào).
6. **Nhánh nghiệp vụ đặc biệt phải tách thành trường hợp riêng** (ví dụ: thao tác có đường thay thế
   khi thiết bị/hình thức chính hỏng), thay vì nhét một dòng "nếu lỗi thì…" vào bảng chính.

### 2.2. Đặt mã trường hợp theo tác nhân, không theo giao diện

| Tiền tố | Nhóm |
|---|---|
| `A·n` | Tác nhân 1 (người dùng chính) |
| `B·n`, `C·n` | Các tác nhân khác |
| `D·n` | Nội bộ / quản trị (tách theo **vai trò thật** trong code) |
| `E·n` | Tác nhân **thời gian / hệ thống** (job, webhook, scheduler) — **đừng bỏ nhóm này**, đây là chỗ hay quên và hay bị hỏi |
| `KB-nn` | Kịch bản chạy suốt (kể chuyện) |

### 2.3. Quan hệ include/extend phải hiện trong bảng

Nếu trường hợp X luôn chạy bước Y → ghi `«include»` trong tên và để Y thành một dòng/bảng riêng.
Nếu Y là nhánh tuỳ chọn → `«extend»`. **Kiểm chứng bằng code**, không suy từ sơ đồ:
đọc hàm thật xem bước đó có bị gọi vô điều kiện không.

### 2.4. Kịch bản chạy suốt (KB) — phần được đọc nhiều nhất

Mỗi ca dài 8–15 bước, ghi theo **thao tác → trạng thái → số tiền/giá trị cụ thể**.
Kết thúc bằng **một con số** ("ví shop +24.291.000") để người đọc kiểm được.
Bắt buộc có các ca "xấu": khách im lặng, tem sai, sự cố, khiếu nại một phần, vượt ngưỡng phê duyệt,
hai người thao tác cùng lúc (race condition), webhook trùng.

### 2.5. Bảng thuật ngữ — thứ chặn hiểu nhầm

Ghi các trạng thái **dễ nhầm** và phân biệt chúng. Ví dụ thật:

| Trạng thái | Nghĩa | Ai đặt |
|---|---|---|
| `delivered` | Đã giao, người nhận **chưa** xác thực | tài xế |
| `delivered_verified` | Đã xác thực — **tiền vẫn đang giữ** | người mua |
| `completed` | **Tiền đã rời** ký quỹ | hệ thống / người mua |

Nếu tài liệu không có bảng này, người đọc sẽ tự suy và suy sai.

### 2.6. Bảng kiểm "đã phủ hết chưa" — chống tài liệu mỏng

Kết tài liệu bằng bảng: **nhóm tình huống → có tài liệu không (✅/❌) → ở mục nào**.
Các nhóm tối thiểu phải có:

- Đăng ký / đăng nhập / quên mật khẩu / đăng xuất
- Tạo hồ sơ, xét duyệt, từ chối, tạm ngưng, đóng
- Đăng bán / thêm dữ liệu + luồng duyệt hoặc gỡ
- Luồng chính (đặt → xử lý → giao → xác nhận → hoàn tất)
- Hoàn tất tự động theo thời gian
- Đánh giá / phản hồi
- Khiếu nại / tranh chấp: mở, trao đổi hai chiều, yêu cầu trả, các kết cục phán quyết
- Sự cố / ngoại lệ vận hành và **từng kết cục** của nó
- Nạp tiền: tự động qua webhook + duyệt tay + từ chối
- Rút tiền: xác thực phụ, hạn mức, phí, tạm giữ, hoàn khi từ chối
- Cấp tài khoản nội bộ; khoá/mở khoá; điều chỉnh số dư nhiều bước
- Ngưỡng phê duyệt; kiểm tra cờ rủi ro
- Hỗ trợ khách hàng: tạo phiếu, trả lời, ghi chú nội bộ
- Nhật ký kiểm toán / tra vết
- Cấu hình toàn hệ thống nhiều bước
- Báo cáo / thống kê
- **Bất biến & tính đúng khi tranh chấp**: cái gì bị chặn khi đang có khiếu nại
- **Chống trùng / idempotency**: webhook, thao tác lặp, hai người cùng lúc

Dòng nào ❌ thì hoặc viết bù, hoặc ghi vào "Hạn chế đã biết" — **không để trống**.

---

## 3. Quy trình viết (bắt buộc theo thứ tự)

| Bước | Việc | Dấu vết |
|---|---|---|
| 1 | Quét cây nguồn, liệt kê module/endpoint/enum/job | danh mục route + enum |
| 2 | Đọc và ghi chú **từng enum/trạng thái + bảng chuyển đổi** | trích dòng |
| 3 | Đọc các service lõi (nghiệp vụ chính) và **ghi lại mã lỗi thật** | trích dòng |
| 4 | Lập bảng phủ trường hợp (§2.6) → chốt danh sách trường hợp cần viết | bảng phủ |
| 5 | Viết từng nhóm theo khung §1 | file .md |
| 6 | **Đối chiếu ngược**: mỗi khẳng định có trích dòng không? | checklist |
| 7 | Xuất PDF (`scripts/md_to_pdf.py`) và **mở PDF soi** ở trang bìa + một trang bảng | ảnh render |
| 8 | Báo cáo: số trang, số trường hợp, phần ❌ còn lại | |

**Bước 6 không được bỏ.** Cách nhanh nhất: đọc lại tài liệu của mình và với mỗi câu hỏi
*"tôi biết điều này vì dòng nào?"* — không trả lời được thì ghi `UNKNOWN` rồi đi xác minh.

**Bước 7 không được bỏ.** PDF có thể hỏng mà không báo lỗi: chữ tiếng Việt mất dấu,
bảng tràn lề, ảnh không nhúng, mã lỗi bị cắt. Phải **mở PDF ra xem** (render trang bìa +
1 trang có bảng + trang cuối) rồi mới tuyên bố xong.

---

## 4. Checklist trước khi giao

```text
[ ] Có bảng thuật ngữ + bảng trạng thái dễ nhầm
[ ] Mọi khẳng định nghiệp vụ có trích file:dòng
[ ] Mỗi trường hợp đủ 4 dòng: Đầu vào / Xử lý hệ thống / Đầu ra / Nhánh lỗi
[ ] Nhánh lỗi ghi bằng MÃ lỗi lấy từ code (không dùng câu chữ chung)
[ ] Có nhóm tác nhân THỜI GIAN / HỆ THỐNG (job, webhook, scheduler)
[ ] Có ít nhất 8 kịch bản chạy suốt, trong đó >= 4 ca "xấu" (lỗi/ngoại lệ/cạnh tranh)
[ ] Có mục "Hạn chế đã biết" với hướng sửa từng mục
[ ] Bảng kiểm phủ trường hợp: không còn dòng trống
[ ] PDF: KHONG chu mau (check_pdf_monochrome.py bao SACH)
[ ] PDF đã xuất và ĐÃ MỞ XEM (bìa + 1 trang bảng + trang cuối)
[ ] PDF: tiếng Việt đủ dấu, không tràn lề, mã lỗi không bị cắt
[ ] Nhan manh chi dung: dam / nghieng / ==highlight== (khong mau chu, khong emoji danh dau)
```
