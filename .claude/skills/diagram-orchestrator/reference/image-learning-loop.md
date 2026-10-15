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

## 3. Bổ sung: nghiên cứu có thể truy vết và học có kiểm soát

Trước khi thêm một quy tắc layout mới:

1. **Nêu câu hỏi hẹp** (ví dụ: “khi nào hidden edge làm bố cục Class Diagram tệ hơn?”), không tìm chung chung “diagram đẹp”.
2. **Ưu tiên nguồn gốc:** tài liệu chính thức của renderer/engine; nghiên cứu học thuật; sau đó mới đến blog/vendor làm ví dụ thị giác. Ghi rõ loại nguồn.
3. **Kiểm tra nội dung trang thực tế:** không chỉ lấy snippet tìm kiếm hoặc tiêu đề. Ghi ngày truy cập, URL, nội dung hỗ trợ và điều nguồn không chứng minh.
4. **Không suy rộng từ ảnh đơn lẻ:** một ảnh có thể là ví dụ thẩm mỹ, không chứng minh thuật toán/quan hệ nhân quả. Mẫu ảnh chỉ giúp hình thành giả thuyết.
5. **Chạy PoC đại diện:** giữ nguyên topology/semantics giữa baseline và candidate; lưu nguồn, ảnh, cấu hình và checklist. Nếu không render/xem được ảnh, ghi UNKNOWN.
6. **Mã hóa quy tắc theo nhãn:** [source-backed], [empirical-in-repo], [heuristic], hoặc [preference]. Không đổi heuristic thành hard gate khi chưa có dữ liệu đủ.
7. **Kiểm tra tác dụng phụ:** mỗi quy tắc mới phải được thử ít nhất một case dương tính và một case âm tính/regression; cập nhật eval tương ứng.
8. **Đồng bộ mirror và xác minh:** cập nhật .claude/skills trước, sync sang .agents/skills, kiểm tra hash/nội dung trùng; không sửa hai bản độc lập.

Không tải/nhúng ảnh tham khảo có bản quyền vào sản phẩm. Chỉ ghi nhận đặc tính bố cục bằng lời và dẫn nguồn.