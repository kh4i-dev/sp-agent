# Ngữ nghĩa & Quy mô báo cáo — CHỐNG "BÁO CÁO MỎNG"

Mục đích: chặn lỗi AI viết báo cáo/đồ án **quá ít trang, nông, mỗi mục 1–2 câu rồi bỏ qua**.
Đây là **thiết luật về độ sâu**, áp dụng song song với quy tắc format.

## 1. Quy mô tối thiểu (không kể bìa, phụ lục, danh mục)

| Loại | Số trang nội dung tối thiểu | Số từ thân bài (gợi ý) |
|---|---|---|
| **Đồ án PTTKHT** | **40 – 60 trang** | 12.000 – 20.000 từ |
| **Báo cáo bài tập lớn (BTL)** | **15 – 30 trang** | 4.000 – 9.000 từ |
| Báo cáo môn học ngắn | **10 – 15 trang** | 3.000 – 5.000 từ |

> Nếu chỉ viết được ~10 trang cho một đồ án PTTKHT → **SAI**. Phải bổ sung chiều sâu, không được nộp.

## 2. Độ sâu theo chương — Đồ án PTTKHT

| Chương | Trang tối thiểu | Bắt buộc có |
|---|---|---|
| **Chương 1. Khảo sát hệ thống** | 8 – 12 | Giới thiệu tổ chức; sơ đồ tổ chức; hoạt động/quy trình hiện tại; thực trạng; vấn đề cần tháo gỡ; yêu cầu hệ thống mới (chức năng + phi chức năng) |
| **Chương 2. Phân tích hệ thống** | 10 – 15 | Thông tin vào/ra; biểu đồ trạng thái; biểu đồ lớp; biểu đồ hoạt động; biểu đồ use case; **đặc tả use case** (bảng luồng chính/phụ) |
| **Chương 3. Thiết kế hệ thống** | 8 – 12 | Chuẩn hóa quan hệ 1NF→2NF→3NF; mô tả chi tiết từng bảng (cột, kiểu, ràng buộc); **ERD**; thiết kế form/giao diện |
| **Chương 4. Cài đặt chương trình** | 5 – 8 | Ngôn ngữ/công nghệ; kiến trúc; kiểm thử (bảng ca kiểm thử); mã nguồn form chính; **ảnh chụp màn hình thật** |
| **Chương 5. Nhận xét & đánh giá** | 2 – 3 | Kết quả đạt được; hạn chế; hướng phát triển |
| **Kết luận** | ≥ 1 | Tổng kết + hướng phát triển |
| **Tài liệu tham khảo** | — | **≥ 5 – 10** tài liệu, mọi trích dẫn phải có trong danh mục |

## 3. Độ sâu theo chương — Báo cáo BTL

Mỗi chương **≥ 3 – 5 trang**, gồm tối thiểu: Mở đầu (lý do, mục tiêu, phạm vi, phương pháp, bố cục) →
Cơ sở lý thuyết/công nghệ → Phân tích & thiết kế → Cài đặt → Kiểm thử/kết quả → Kết luận & hướng phát triển.

## 4. Quy tắc viết (BẮT BUỘC)

1. **KHÔNG tóm tắt suông**: cấm mỗi mục chỉ 1–2 câu rồi nhảy mục.  
   Mỗi **Heading 3** phải có **≥ 1 đoạn văn hoàn chỉnh (≥ 5–8 câu)** + dẫn chứng (bảng, sơ đồ, số liệu, ví dụ).
2. **Mỗi chương phải đạt số trang tối thiểu** ở bảng trên. Thiếu → mở rộng bằng phân tích, ví dụ, sơ đồ, ca kiểm thử — **không chèn chữ rỗng**.
3. **Có hình/bảng minh hoạ**: PTTKHT cần tối thiểu các sơ đồ (tổ chức, use case, lớp, hoạt động, trạng thái, ERD) + bảng đặc tả. Dùng skill `plantuml-diagrams`/`diagram-orchestrator`.
4. **Source truth**: mọi số liệu/kết quả phải thật. Thiếu dữ liệu → **HỎI người dùng** hoặc đánh dấu `TODO` rõ ràng, **TUYỆT ĐỐI không bịa**.
5. **Kiểm độ dày sau render**: đếm số trang từng chương; nếu mỏng hơn bảng trên → viết bổ sung rồi render lại.
6. Xác nhận với người dùng **mục tiêu số trang** ngay từ đầu nếu đề bài không nêu rõ.

## 5. Dấu hiệu "báo cáo mỏng" (cần viết lại)

```text
[ ] Tổng nội dung < 20 trang cho một đồ án PTTKHT
[ ] Có chương < 2 trang
[ ] Nhiều mục chỉ 1 câu, không có đoạn văn
[ ] Không có sơ đồ / bảng nào
[ ] Chương "Phân tích" thiếu use case / đặc tả
[ ] Chương "Thiết kế" thiếu ERD / mô tả bảng
[ ] Chương "Cài đặt" không có ảnh chụp màn hình thật
[ ] Tài liệu tham khảo trống hoặc < 5
```

## 6. Bộ skill phối hợp để đủ dày & chất

```text
research-report / deep-research  → thu thập & xác minh nguồn
plantuml-diagrams / diagram-orchestrator → vẽ đủ sơ đồ (use case, lớp, hoạt động, trạng thái, ERD)
docx-report                      → dựng cấu trúc, bảng, hình, caption, mục lục
human-report-writing             → biên tập văn phong cho tự nhiên, đủ sâu
```
