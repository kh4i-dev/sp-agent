# Nghiên cứu bổ sung: Tư duy bố cục sơ đồ dựa trên bằng chứng

**Ngày nghiên cứu:** 2026-10-16  
**Phạm vi:** `diagram-orchestrator/reference/layout-thinking.md`, lựa chọn engine và quy trình kiểm tra bố cục.  
**Mục đích:** phân biệt điều đã được nguồn kỹ thuật xác nhận, điều rút ra từ nghiên cứu khả năng đọc sơ đồ và heuristic vận hành của repo.

## 1. Kết luận chính

1. **Không đồng nhất mọi auto-layout.** Graphviz `dot` là layout phân tầng: nó cố gắng giữ hướng cạnh, giảm giao cắt và độ dài cạnh. Đây là mục tiêu tối ưu của thuật toán, không phải cam kết hình cuối không có giao cắt. PlantUML có thể dùng cơ chế/layout engine khác nhau theo cấu hình và renderer; không được mô tả mọi PlantUML/Graphviz như cùng một thuật toán.
2. **`nodesep`, `ranksep`, `rankdir` có phạm vi và đơn vị riêng theo engine.** Graphviz `dot` định nghĩa `nodesep` theo inch cho khoảng cách tối thiểu giữa node cùng rank và `ranksep` theo inch giữa rank. Không chuyển nguyên trị số giữa Graphviz và PlantUML nếu chưa xác nhận cách renderer diễn giải.
3. **Hidden edges / rank constraints là công cụ điều khiển, không phải bằng chứng hình học.** Tài liệu PlantUML nói `together` và hidden links có thể ảnh hưởng layout; tài liệu Graphviz cho thấy constraint/rank/group có tác dụng khác nhau. Mỗi ràng buộc phải có mục tiêu quan sát được, và phải kiểm tra tác dụng phụ lên cạnh thật.
4. **Tách semantic correctness khỏi visual quality.** Không bao giờ xóa quan hệ nghiệp vụ để giảm giao cắt. Nếu bố cục không đạt, đổi cách sắp xếp, chia góc nhìn, đổi engine hoặc dùng bố cục thủ công sau khi đóng băng mô hình.
5. **Ngưỡng trong repo là heuristic cho review, không phải định luật khoa học.** Các ngưỡng như cạnh dài hơn 2.5× trung vị, góc phần tư ít mực, hub degree ≥ 5, hay void container > 25% cần được gắn nhãn heuristic và hiệu chỉnh bằng benchmark thực tế của repo.

## 2. Nguồn đã tra cứu

### S1 — Graphviz: DOT layout engine
https://graphviz.org/docs/layouts/dot/

Tài liệu mô tả `dot` phù hợp với đồ thị phân tầng có hướng; mục tiêu là hướng cạnh theo cùng một chiều và cố gắng giảm giao cắt cạnh, đồng thời giảm độ dài cạnh. Tài liệu liệt kê các thuộc tính như `constraint`, `group`, `minlen`, `rank`, `rankdir`, `ranksep` và `remincross`.

**Áp dụng:** mô tả đúng là “thuật toán cố gắng giảm giao cắt theo mục tiêu layout”, không phải “đảm bảo không giao cắt” hoặc “chỉ tối ưu theo thứ tự khai báo”.

### S2 — Graphviz: `nodesep`
https://graphviz.org/docs/attrs/nodesep/

Với `dot`, `nodesep` xác định khoảng cách tối thiểu giữa hai node liền kề cùng rank; đơn vị là inch. Ý nghĩa của thuộc tính này thay đổi với layout engine khác.

**Áp dụng:** không dùng một trị số nodesep như ngưỡng phổ quát cho mọi engine. Đo ảnh render ở kích thước đầu ra cuối cùng.

### S3 — Graphviz: `ranksep`
https://graphviz.org/docs/attrs/ranksep/

Với `dot`, `ranksep` xác định khoảng cách giữa các rank theo inch. Đây là khoảng cách hình học giữa các tầng, không phải bộ giải giao cắt độc lập.

**Áp dụng:** điều chỉnh ranksep có thể tạo thêm không gian nhưng không sửa được một topology sai hoặc bảo đảm cạnh không cắt nhau.

### S4 — Graphviz: `rankdir`
https://graphviz.org/docs/attrs/rankdir/

`rankdir` định hướng phân tầng TB/BT/LR/RL của `dot`; không tự bảo đảm vị trí tuyệt đối của node.

**Áp dụng:** dùng để chọn trục đọc phù hợp; không tuyên bố “đã căn ngang chính xác” nếu chưa kiểm tra ảnh.

### S5 — PlantUML: Class Diagram — Help on layout
https://plantuml.com/class-diagram

PlantUML ghi rõ layout mặc định đôi lúc không hoàn hảo; `together` và hidden links có thể được dùng để tác động bố cục.

**Áp dụng:** hidden links là gợi ý có tác động thật nhưng không phải tọa độ cứng. Thử một ràng buộc tại một thời điểm, render lại, và loại bỏ nếu không cải thiện hoặc làm hỏng cạnh khác.

### S6 — Purchase, McGill, Colpoys & Carrington (2001)
“Graph drawing aesthetics and the comprehension of UML class diagrams: an empirical study.”  
https://courses.ischool.berkeley.edu/i247/f05/readings/Purchase_UML_OzIV01.pdf

Nghiên cứu xem xét các yếu tố thẩm mỹ đồ thị và khả năng hiểu sơ đồ lớp UML. Nó hỗ trợ việc quan tâm đến giao cắt, độ dài cạnh, hướng, phân bố node và kiểu cạnh; không thiết lập các ngưỡng số học riêng của repo như 2.5× hoặc 10%.

**Áp dụng:** giữ các ngưỡng hiện tại như tiêu chí sàng lọc nội bộ, không gán nhầm chúng thành kết luận của nghiên cứu.

### S7 — Anthropic: Skill authoring best practices
https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

Tài liệu khuyến nghị skill ngắn gọn, mô tả trigger rõ, tách tài liệu tham khảo khi cần, và tạo evaluation trước khi mở rộng chỉ dẫn; thử với tình huống đại diện rồi cải tiến theo quan sát.

**Áp dụng:** thay đổi layout-thinking cần có eval cố định, baseline và bằng chứng render; không chỉ tăng số lượng quy tắc.

## 3. Quy trình ra quyết định đề xuất

### Bước A — Freeze semantics
- Xác định nguồn sự thật: schema/code/SSOT đã duyệt.
- Liệt kê node, quan hệ, multiplicity, role, hướng luồng và các ràng buộc nghiệp vụ.
- Đếm và đối chiếu quan hệ trước/sau render.
- Đánh dấu riêng fact, inference và unknown.

### Bước B — Chọn engine theo cấu trúc
- UML có ký pháp chuẩn: ưu tiên PlantUML khi layout tự động đủ; nếu cần vị trí/lane chính xác thì dùng nguồn có điều khiển tọa độ như draw.io.
- Graph phân tầng/cây: cân nhắc Graphviz `dot`.
- Đồ thị không phân tầng dày: đánh giá engine khác theo topology, không ép `dot` vào mọi trường hợp.
- Chọn theo loại sơ đồ và khả năng tái tạo, không theo thói quen.

### Bước C — Đặt giả thuyết có thể kiểm tra
Ví dụ: “Đặt nhóm Review cạnh User sẽ giảm cạnh xuyên nhóm mà không đổi số quan hệ.”  
Ghi baseline, thay một biến, render lại và so sánh ở cùng kích thước. Không gộp nhiều thay đổi vào một vòng nếu mục tiêu là tìm nguyên nhân.

### Bước D — Đánh giá theo 2 trục độc lập
**Semantic gate**
- Node/actor/class đủ và không thừa.
- Mọi quan hệ có căn cứ được giữ; multiplicity/role/guard đúng.
- Không thêm quan hệ chỉ để bố cục đẹp.

**Visual gate**
- Không có node chồng, nhãn bị cắt hoặc gán nhầm cạnh.
- Giao cắt, cạnh vòng xa, phân bố không cân đối được ghi nhận.
- Chữ đọc được ở kích thước xuất bản.
- Nguồn chỉnh sửa và ảnh render cùng phiên bản.

Một hình chỉ đạt khi qua cả hai gate. Static checks không thay thế kiểm tra hình học.

### Bước E — Điều kiện dừng
- Dừng ngay khi đã đạt cả semantic và visual gates.
- Nếu một thay đổi không cải thiện chỉ số mục tiêu hoặc tạo regression, revert biến đó.
- Nếu hai vòng thử có ý nghĩa không cải thiện, hoặc đã biết engine không thể đáp ứng vị trí yêu cầu, chuyển sang phân rã/engine khác/vẽ tay.
- Không tiếp tục đổi tham số ngẫu nhiên để cố đạt một hình.

## 4. Benchmark tối thiểu cần có

Mỗi case lưu:
- Source model + source diagram.
- Ảnh baseline và ảnh candidate cùng tỷ lệ.
- Loại engine, version, lệnh render và kích thước ảnh.
- Semantic diff: số node, số quan hệ, multiplicity/labels.
- Visual checklist: giao cắt, nhãn đè, cạnh vòng xa, vùng trắng, độ đọc.
- Quyết định PASS / FAIL / UNKNOWN kèm lý do.

Bộ eval phải gồm ít nhất: hub class nhiều cạnh; nhiều quan hệ giữa cùng cặp node; Use Case nhiều actor; ERD nhiều FK; graph cây; sơ đồ kiến trúc có container. Bao gồm cả case âm tính mà đúng quyết định là **không đổi gì** hoặc **tách sơ đồ**.

## 5. Ranh giới của kết luận

- Tài liệu chính thức mô tả hành vi/thuộc tính của engine; nó không xác nhận sơ đồ cụ thể trong repo đã đẹp.
- Nghiên cứu học thuật hỗ trợ nguyên tắc thẩm mỹ/khả năng hiểu; không chứng minh mọi threshold nội bộ.
- Heuristic của repo phải tiếp tục được kiểm chứng qua eval và render thật.
- Nếu không có ảnh/metrics, kết luận bắt buộc là UNKNOWN — không suy đoán từ source code.
