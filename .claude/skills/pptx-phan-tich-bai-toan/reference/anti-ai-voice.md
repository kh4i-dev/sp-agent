# Chống "mùi AI" trong slide học thuật

Cô giáo và các bạn nhận ra slide do AI làm không phải vì nó xấu, mà vì nó **trơn**:
câu nào cũng cân đối, từ nào cũng hoa mỹ, và không có chi tiết riêng của đồ án.
Cách chống tốt nhất: **cụ thể hoá** — số liệu thật, tên thật, quyết định thật, và câu ngắn.

## 1. Bộ từ / cấu trúc CẤM

| Cấm | Vì sao | Thay bằng |
|---|---|---|
| "Trong thời đại số ngày nay…" | mở bài rỗng | Đi thẳng vào số liệu/vấn đề |
| "Không chỉ X mà còn Y" | khuôn AI | Tách 2 câu, hoặc bỏ |
| "giải pháp toàn diện", "đột phá", "tối ưu hoá trải nghiệm" | tính từ rỗng | Nêu **cơ chế cụ thể** làm được gì |
| "đóng vai trò then chốt", "vô cùng quan trọng" | nhấn mạnh rỗng | Bỏ hẳn |
| "hành trình", "chạm đến", "lan toả" | marketing | Từ kỹ thuật thật |
| "Kết luận: đây là bước tiến lớn" | kết rỗng | Nêu kết quả đo được |
| 3 gạch đầu dòng **cùng độ dài, cùng cấu trúc** | dấu hiệu AI rõ nhất | Để độ dài/cấu trúc khác nhau tự nhiên |
| em-dash (—) dày đặc, ngoặc kép "nhấn mạnh" | giọng AI | Chấm câu, bỏ ngoặc |
| IN HOA + giãn chữ (tracking) trên nhãn | slop thị giác | chữ thường, `font-medium` |
| emoji (✅🚀💡) | slop + không học thuật | ô vuông/shape native, hoặc bỏ |
| Số liệu "uy tín" không nguồn | bịa đặt | Số thật + nguồn, hoặc bỏ |

## 2. Sáu luật viết

1. **Tiêu đề là một khẳng định có nội dung.**
   - Kém: "Tổng quan về vấn đề" · "Giải pháp đề xuất"
   - Tốt: "COD buộc người mua trả tiền trước khi được kiểm hàng"
2. **Một câu = một ý.** Câu dài → cắt thành hai.
3. **Số cụ thể thắng tính từ.** "17,3% đơn COD có gian lận (Cục TMĐT & KTS, 2024)"
   thay vì "tỷ lệ gian lận rất cao".
4. **Nói rõ đánh đổi.** Câu "nhược điểm / giới hạn" làm slide đáng tin hơn câu khen.
5. **Thuật ngữ Việt + tiếng Anh trong ngoặc** ở lần đầu: "ký quỹ (escrow)", "tem ký số".
6. **Bỏ câu mà nếu xoá đi không mất gì.** Câu nào đúng với mọi đồ án = câu rỗng.

## 3. Ví dụ sửa (before → after)

- Before: "Hệ thống được xây dựng với kiến trúc hiện đại, tối ưu và dễ mở rộng."
  After: "Ba tầng: Nuxt 3 (giao diện), NestJS 14 module (nghiệp vụ), Prisma 44 model (dữ liệu)."

- Before: "Việc bảo vệ dữ liệu cá nhân là vô cùng quan trọng trong thời đại số."
  After: "Số điện thoại và địa chỉ được che mờ trên vận đơn; mỗi lần lộ đều ghi vết kiểm toán."

- Before: "Giải pháp không chỉ đảm bảo an toàn mà còn nâng cao trải nghiệm người dùng."
  After: "Tiền chỉ được giải ngân khi người mua quét tem hợp lệ. Sai mã thì tiền bị đóng băng chờ trọng tài."

- Before (3 bullet song song): "Minh bạch · An toàn · Hiệu quả"
  After: "Tiền giữ ở quỹ ký quỹ, chỉ chia khi tem được xác thực. Tem dùng một lần nên quét lại sẽ bị từ chối."

## 4. Checklist tự soát trước khi render

- [ ] Đọc to từng tiêu đề — cái nào nghe như tiêu đề mẫu thì viết lại.
- [ ] Mỗi slide ≥ 1 chi tiết **chỉ đồ án này mới có** (số, tên module, quyết định).
- [ ] Grep bộ từ cấm ở §1 trong spec (`grep -iE "toàn diện|đột phá|then chốt|hành trình"`).
- [ ] Không số liệu nào thiếu nguồn.
- [ ] Slide không có 3 dòng bullet cùng khuôn.
- [ ] Không emoji, không icon cạnh chữ, không gradient.
