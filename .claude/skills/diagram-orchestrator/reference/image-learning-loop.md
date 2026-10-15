# Vòng lặp tự học ảnh mẫu (Image Learning Loop) — SSOT quy trình

> Dùng khi cần nâng cấp tư duy vẽ cho một loại sơ đồ mà KHÔNG có ảnh mẫu từ người dùng:
> agent tự tìm — tải — soi — rút pattern — mã hóa vào skill — gen so sánh.
> Quy trình này đã chạy thành công cho ERD (§9), Class (§10), Use Case (§11).

## 1. Các bước (làm đúng thứ tự, không bỏ)

1. **Tìm (search):** `websearch` ảnh/bài mẫu đúng loại sơ đồ (`<loại> diagram layout
   guidelines examples`). Ưu tiên: tài liệu học thuật, Wikipedia, blog tác giả chuẩn
   (Ambler), vendor vẽ (Lucid/EdrawMax) làm ground truth thị giác.
2. **Tải (download):** trang thường có `og:image` hoặc `<img>` nội dung. PowerShell:
   `Invoke-WebRequest <page> -UseBasicParsing` → regex `og:image` hoặc `src="...uploads...png|jpg|gif"`
   → `Invoke-WebRequest <img> -OutFile <temp>\<ten-go>.png`. Lưu vào thư mục temp
   ngoài repo. Đặt tên file DUY NHẤT theo lần gen (tránh đè khi có phiên khác cùng làm).
3. **Soi (view):** `read` từng ảnh vào ngữ cảnh model. Ghi ≥ 3 nhãn đọc được + bố cục
   (cột/lane/hub ở đâu, cạnh đi thế nào) + điểm tốt/xấu cụ thể từng ảnh.
4. **Rút pattern:** liệt kê điểm CHUNG của ảnh đẹp + điểm TRỪ của ảnh xấu (kể cả ảnh
   trong tập mẫu — VD CodeRanch chéo xuyên hộp = FAIL mẫu). Mỗi pattern phải gắn được
   với ít nhất 2 ảnh hoặc 1 nguồn chữ ([S1]–[S3]).
5. **Mã hóa vào skill:** thêm mục `reference-style <loại>` vào `layout-thinking.md`
   (không tạo skill mới), móc 1 dòng từ skill công cụ tương ứng. Mỗi luật ghi rõ
   `[nguồn]` hay `[heuristic]` hay `[vòng lặp gen]`.
6. **Gen–so–chấm:** vẽ lại 1 sơ đồ thật theo pattern (temp, không đụng repo), render,
   soi, chấm checklist §7 + so với bản cũ. Đổi đúng 1 biến mỗi vòng; vòng sau không
   tiến triển thì DỪNG và ghi luật dừng (như §1, §10).
7. **Đồng bộ + kiểm:** `sync-skills.ps1` → `verify-skills.ps1` (40/40) → báo cáo + hỏi
   commit (không tự commit).

## 2. Luật bản quyền & vệ sinh (bất biến)

- Ảnh tải về chỉ để **phân tích bố cục** (học ý tưởng, không sao chép biểu đạt).
  **Cấm** nhúng ảnh tải về vào báo cáo/luận văn/repo. Chỉ trích pattern chữ + URL đã truy cập.
- Trang chặn bot (VD ResearchGate 403) → ghi nhận `UNFETCHED`, dùng screenshot tay của
  người dùng nếu có, không cố vượt rào.
- File PoC trong temp phải có hậu tố version (`-poc1`, `-v2`) + không bao giờ lẫn vào
  `docs/diagrams/` của repo đồ án.
