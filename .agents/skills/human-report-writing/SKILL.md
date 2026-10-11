---
name: human-report-writing
description: Viết và biên tập văn xuôi báo cáo/đồ án theo văn phong tự nhiên như người viết, loại bỏ dấu hiệu văn do AI/máy sinh (câu rào đón, lặp khuôn, bullet tràn lan, câu "hướng dẫn nội bộ"). Use when writing or editing report prose, khi bản thảo "nghe như AI/đọc đỡ máy", hoặc khi người dùng yêu cầu "viết như human", "tự nhiên hơn", "đỡ giống máy", "đổi văn phong".
---

# Human Report Writing — văn phong báo cáo như người viết

Mục tiêu: bản thảo đọc như một sinh viên/kỹ sư thật viết, **không lộ dấu hiệu văn do AI sinh**,
mà vẫn giữ đúng dữ kiện, đúng thuật ngữ và đúng cấu trúc báo cáo.

## Khi nào dùng

- Viết hoặc biên tập phần văn xuôi của báo cáo/đồ án/luận văn.
- Bản thảo "nghe như AI": câu rào đón, lặp khuôn, kể lể, bullet tràn lan.
- Người dùng nói: "viết như human", "tự nhiên hơn", "đỡ máy", "đổi giọng".

## Nguyên tắc cốt lõi (bất biến)

1. **Kể câu chuyện.** Vấn đề → vì sao quan trọng → giải pháp → kết quả. Thông điệp chính được
   nhắc lại ở Tóm tắt, Mở đầu và Kết luận.
2. **Câu văn hoàn chỉnh.** Ưu tiên đoạn văn; **hạn chế gạch đầu dòng**. Chỉ dùng danh sách khi
   liệt kê thật sự (bảng, bước quy trình).
3. **Mỗi chương kết thúc bằng một đoạn "Tóm tắt chương"** 2–3 câu (tóm các kết luận chính);
   đầu chương có thể có 1 câu dẫn giới thiệu các phần sẽ trình bày.
4. **Nhất quán ngôi kể.** Chọn một ngôi (thường "em") và giữ xuyên suốt; không trộn "em" với
   "chúng tôi"/"tác giả".
5. **Source truth.** Không bịa số liệu/kết quả; không nâng `PARTIAL`/`NOT_FOUND` thành `DONE`.

## Dấu hiệu "văn AI" cần loại bỏ

- **Câu kiểu hướng dẫn nội bộ** (không phải nội dung báo cáo):
  "trước khi nộp báo cáo, cần đối chiếu…", "khi nộp bài cần bảo đảm…", "nên ghi rõ là dữ liệu mô phỏng…".
  → Chuyển thành câu khẳng định nội dung, hoặc xoá.
- **Lặp khuôn câu**: "cần được", "điều này cho thấy", "bên cạnh đó", "một khía cạnh quan trọng khác",
  "không chỉ … mà còn …". Mỗi khuôn chỉ nên xuất hiện vài lần trong cả báo cáo.
- **Rào đón/quá dài**: câu nhiều mệnh đề "nhằm … đồng thời … trong khi …". Tách thành câu ngắn.
- **Bullet tràn lan** thay cho lập luận.
- **Chung chung**: "nhiều vấn đề", "rất quan trọng" mà không có ví dụ/số liệu cụ thể.
- **Tuyệt đối hoá** khi thiếu bằng chứng: "luôn luôn", "tất cả", "chắc chắn 100%".
- **Cặp dấu hai chấm liệt kê** lặp lại: "gồm: A; B; C." ở mọi mục.

## Quy trình biên tập

```text
1. Đọc cả đoạn để nắm ý (đừng sửa từng câu rời).
2. Đánh dấu câu "AI": hướng dẫn nội bộ, rào đón, lặp khuôn, bullet thừa.
3. Viết lại: câu chủ động, cụ thể, độ dài câu đa dạng.
4. Thêm "Tóm tắt chương" ở **cuối** mỗi chương.
5. Đọc lại toàn bài: khuôn câu có lặp quá không? ngôi kể có nhất quán không?
6. Render (theo skill docx-report) rồi đọc lại trên trang thật.
```

## Bảng: câu AI → câu người

| Câu AI (tránh) | Câu người (nên) |
| :-- | :-- |
| "Điều này cho thấy việc xây dựng hệ thống là cần thiết." | "Ba vấn đề trên khiến em chọn xây dựng hệ thống." |
| "Cần được lưu ý rằng…" | (bỏ, vào thẳng nội dung) |
| "Trước khi nộp, cần đối chiếu số liệu." | "Số liệu dưới đây lấy từ Báo cáo TMĐT 2024 của Bộ Công Thương." |
| "Hệ thống không chỉ đảm bảo an toàn mà còn…" | "Hệ thống giữ tiền trong ký quỹ và chặn giải ngân khi có tranh chấp." |
| "Có thể nói rằng…", "Nhìn chung…" | (bỏ, nêu thẳng ý) |

## Checklist trước khi giao

```text
[ ] Không còn câu "hướng dẫn nội bộ".
[ ] Mỗi chương kết thúc bằng "Tóm tắt chương" 2–3 câu.
[ ] Ngôi kể nhất quán.
[ ] Không khuôn câu nào lặp quá ~3 lần toàn bài.
[ ] Ưu tiên đoạn văn; bullet chỉ khi cần liệt kê.
[ ] Số liệu/ví dụ cụ thể, không chung chung.
[ ] Đã render và đọc lại trên trang.
```

## Tài liệu tham khảo

- Checklist chi tiết + nhiều ví dụ before/after: xem `reference/checklist.md`.
- Hướng dẫn cấu trúc & hình thức báo cáo (HCMUS/UET) được nhắc trong `reference/checklist.md`.

> Skill này **chỉ lo văn phong**. Để dựng file Word, caption, TOC và render: dùng skill `docx-report`.
