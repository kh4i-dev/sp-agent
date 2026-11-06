# Bẫy đã biết — plantuml-diagrams (Class Diagram)

### [WARN] Auto-layout PlantUML cho Class Diagram dễ xấu/crowded (2026-11-01)
- **Triệu chứng:** Render thành công (audit PASS) nhưng hình dài/crowded, chữ đè multiplicity, hub lớp trung tâm kéo dây chằng chịt; người dùng đánh giá "xấu" dù audit xanh.
- **Nguyên nhân:** PlantUML `dot` auto-layout không kiểm soát được vị trí phần tử; ortho + nhiều association cùng hub dễ tạo cạnh vòng xa và nhãn dồn cục.
- **Sửa/phòng:** Với sơ đồ lớp nhiều lớp (≥ 6) hoặc có hub bậc cao, ưu tiên **vẽ tay SVG/draw.io** (giữ bố cục lưới gọn như bản gốc) rồi thêm `+ - # ~` trực tiếp vào text; PlantUML chỉ dùng làm bản nháp. Nếu vẫn dùng PlantUML: giảm số lớp (≤ 5), bỏ package wrapper gây đè, kiểm tra mắt ảnh sau render.
- **Điều kiện tái lập:** Class diagram có ≥ 6 lớp + hub degree ≥ 8 → auto-layout thường xấu.
