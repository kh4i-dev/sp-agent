# Audit toàn bộ nhóm skill vẽ sơ đồ — 2026-10-15

- Repository: https://github.com/kh4i-dev/sp-agent
- Base main: 60c60564ac99fcae9f7c642f8fcc1fa0a5a5919c
- Branch audit: audit/diagram-skills-layout-2026-10-15
- Commit tại lúc lập báo cáo: 88bb3a9d1eac25201ccac16c0981c9679cd95c46
- Phạm vi: coordinator, orchestrator, PlantUML, Use Case, simplified diagrams, diagram auditor, tldraw, diagram-design, benchmark/evals và mirror.
- Trạng thái: thay đổi đã được ghi trên nhánh audit, chưa merge vào main.
- Giới hạn: đã đọc mã nguồn/tài liệu trên GitHub và sửa theo finding. Node runtime, render benchmark, mở PNG sau khi sửa, PowerShell parity audit và Proof-of-View chưa chạy trong môi trường này. Đây chưa phải kết luận runtime/visual PASS.

## 1. Kết luận điều hành

Nguyên nhân không đơn giản là thiếu vài tham số PlantUML. Nhóm skill đã có nguyên tắc tốt — xác định nghiệp vụ trước, tránh đường vòng xa, render PNG, fallback sang draw.io — nhưng chưa chuyển hết các nguyên tắc thành pipeline có thể kiểm chứng. Có script có thể báo thành công quá sớm; benchmark trước đây đánh đồng static audit với thẩm mỹ; renderer tldraw không tối ưu topology dù tài liệu khiến người đọc có thể hiểu đó là auto-layout; và chưa có eval cho đúng loại đồ thị gây lỗi.

Với ví dụ class_rutgon, cần phân biệt ba nguyên nhân:

1. Độ phức tạp đồ thị: User là hub có nhiều cạnh; một số cặp lớp có nhiều association mang các vai trò khác nhau.
2. Ràng buộc bố cục: chuỗi hidden links ép thứ tự nhưng không đảm bảo quan hệ thật được định tuyến gọn.
3. Thiếu kiểm định nguồn: comment nói “11 lớp” nhưng source có 12 khai báo. Screenshot chưa đủ để khẳng định nguồn và ảnh render cùng phiên bản/phạm vi.

Do đó, chỉ đổi ortho thành polyline hoặc tăng nodesep/ranksep không giải quyết tận gốc. Cần kiểm tra mô hình, đo cấu trúc quan hệ, bố trí node trước khi nối, render thực tế và review độc lập. Nếu cần vị trí chính xác hoặc graph routing sạch mà PlantUML không làm được, chuyển sang draw.io có kiểm soát thay vì vá tham số vô hạn.

## 2. Thang mức độ

- P0 — chặn bàn giao: có thể báo PASS dù kiểm tra bắt buộc chưa xảy ra, hoặc âm thầm làm mất quan hệ.
- P1 — ảnh hưởng lớn: thiếu benchmark/phân tích khiến lỗi bố cục thường gặp tái diễn hoặc mô tả khả năng công cụ sai.
- P2 — độ tin cậy/bảo trì: link phụ thuộc máy cá nhân, quy tắc chồng chéo hoặc kiểm định chưa minh bạch.

## 3. Bảng finding và cập nhật

| ID | Mức | Finding / bằng chứng | Rủi ro | Cập nhật trên nhánh |
|---|---|---|---|---|
| DIA-01 | P0 | Auditor trước đây thoát 0 nếu scope không có SVG. | Thư mục rỗng có thể bị coi là audit thành công. | Không có SVG nay trả lỗi/exit 1. |
| DIA-02 | P0 | Auditor chỉ tìm SVG ở thư mục gốc. | File nằm trong thư mục con có thể bị bỏ sót. | Quét đệ quy mặc định; có cờ top-level-only khi cần giới hạn rõ ràng. |
| DIA-03 | P0 | Auditor không yêu cầu nguồn chỉnh sửa tương ứng. | Có thể bàn giao ảnh không bảo trì được. | Yêu cầu nguồn cùng tên .puml/.dot/.drawio/.tldr/.mmd/.json và PNG hợp lệ tối thiểu 500 byte. |
| DIA-04 | P0 | Benchmark từng in “100% thẩm mỹ” khi renderer và static audit thành công. | Static success bị đánh đồng với semantic correctness và visual quality. | Runner chỉ kết luận STATIC-GATE, nêu rõ chưa phải Visual PASS. |
| DIA-05 | P1 | Benchmark cũ thiếu class hub/parallel association và Use Case nhiều actor. | Lỗi thực tế không được kiểm thử hồi quy. | Thêm EVAL-06 class_rutgon_hub và EVAL-07 use_case_multi_actor, có expected-warning checks. |
| DIA-06 | P1 | Auditor chưa cảnh báo class hub, nhiều association cùng cặp, density và số hidden links. | Agent dễ tăng spacing mà không thấy graph quá dày hoặc layout bị over-constrained. | Thêm cảnh báo heuristic hub/degree, association song song, density, hidden constraints và mismatch số lớp trong comment. |
| DIA-07 | P1 | Thiếu hướng dẫn SSOT riêng cho Class Diagram nhiều quan hệ; luật Use Case hoặc lưới ba cột có thể bị áp máy móc. | Hình sai bố cục dù skill đã có nhiều nguyên tắc chung. | Thêm reference/class-diagram-layout.md; liên kết từ orchestrator, PlantUML, coordinator; thêm scope guard cho Use Case và simplified diagram. |
| DIA-08 | P1 | Manual fallback yêu cầu chờ ≥2 vòng nhưng skill khác cho fallback sớm khi cần tọa độ tuyệt đối/nhiều actor. | Agent có thể vá tham số vô hạn hoặc chuyển công cụ thiếu căn cứ. | Tách lối fallback sớm do giới hạn công cụ và fallback sau thử nghiệm; freeze ngữ nghĩa trước khi vẽ tay. |
| DIA-09 | P1 | Tldraw renderer dùng lưới theo thứ tự group/node, không tối ưu topology; edge có endpoint không tồn tại trước đây chỉ bị bỏ qua sau cảnh báo; arrow kind mặc định luôn arc. | Tài liệu kỳ vọng quá mức và quan hệ có thể mất âm thầm. | Ghi đúng giới hạn grid; fail-fast với direction/ID/endpoint lỗi; bend=0 mặc định straight. |
| DIA-10 | P2 | diagram-design trỏ tới scripts/verify-geometry.py không tồn tại; self_check.py kiểm tra accessibility/safety chứ không kiểm tra hình học đường nối. | Agent có thể tuyên bố đã chạy một check không có. | Ghi rõ geometry check chưa được tự động hóa; yêu cầu NOT AUTOMATED và soi ảnh thủ công. |
| DIA-11 | P2 | Link file:///E:/HOC TAP/... phụ thuộc máy cá nhân. | Link không hoạt động với người khác/GitHub. | Chuyển link ở orchestrator/auditor/PlantUML/Use Case sang path tương đối. |
| DIA-12 | P2 | Mirror .claude ↔ .agents dễ drift khi sửa riêng từng bản. | Agent khác nhau có thể đọc quy tắc/renderer khác nhau. | Đồng bộ mirror trong phạm vi audit trên branch; cần chạy audit skill sau checkout. |

## 4. Phân tích nguyên nhân của class_rutgon

### 4.1 Bằng chứng từ source

- Comment nói 11 lớp nhưng có 12 khai báo: User, Profile, TutorProfile, TutorVerificationDocument, ConnectionRequest, Conversation, ConversationParticipant, Message, Review, Report, TutorPost, Favorite.
- Quan hệ tập trung quanh User; đây là hub bậc cao, không thể bố trí như một lớp ít liên kết.
- Review–User có các vai trò reviewer và reviewee; Report–User có files và resolves. Đây không mặc định là quan hệ trùng. Chỉ được gộp/xóa khi mô hình/code chứng minh hai association thực sự trùng nghĩa.
- Có 11 hidden links. Đây là số lượng cần xem lại vì hidden link ép thứ tự tương đối, không ghim vị trí tuyệt đối và không đảm bảo đường nối đẹp.
- Ảnh cho thấy vùng trắng lớn phía trái, lớp tập trung phía phải và nhiều đường gần song song ở giữa/phải. Đây là finding thị giác từ ảnh người dùng, chưa phải phép đo đầy đủ số giao cắt.

### 4.2 Quy trình giải quyết đúng

1. Render baseline từ đúng source và giữ ảnh đối chiếu.
2. Lập bảng lớp gồm domain group, degree, cặp association song song, hidden constraints và nguồn xác nhận.
3. Mỗi vòng chỉ đổi một yếu tố: nhóm/lane, hướng tổng thể, thứ tự khai báo, kiểu line hoặc một hidden link.
4. Nếu graph vẫn dồn, cạnh vẫn vòng xa hoặc nhãn khó gán đúng đường sau hai vòng hợp lý, dừng tăng spacing. Tách sơ đồ theo câu hỏi nghiệp vụ hoặc chuyển draw.io để định vị.
5. Không xóa association/multiplicity vì thẩm mỹ. Khi phân rã, giữ tên/role nhất quán và ghi rõ đó là các góc nhìn của cùng mô hình.

### 4.3 Trade-off công cụ

- PlantUML: nguồn gọn, dễ diff/review/tái tạo; không ghim được tọa độ tuyệt đối cho mọi đồ thị.
- draw.io: kiểm soát node/route tốt hơn, phù hợp hình cần nộp; phải giữ source chỉnh sửa và kiểm tra thủ công.
- Phân rã: giảm mật độ và tăng khả năng đọc; cần giữ nhất quán các lớp dùng chung.
- Heuristic auditor: cảnh báo sớm; có thể false positive/false negative và không chứng minh không có giao cắt.

## 5. Các thành phần được cập nhật

| Thành phần | Thay đổi |
|---|---|
| diagram-orchestrator/reference/class-diagram-layout.md | SSOT mới về hub/degree, density, association song song, hidden links, phân rã và thử nghiệm PlantUML. |
| diagram-orchestrator/SKILL.md | Thêm mục Class Diagram density/layout và điều kiện đọc SSOT. |
| plantuml-diagrams/SKILL.md | Bổ sung quy tắc class graph; nhấn mạnh ảnh render thay vì tin tham số. |
| use-case-layout/SKILL.md | Thêm scope guard: luật Use Case không tự động áp sang Class/ERD. |
| simplified-diagrams/SKILL.md | Giới hạn hidden links hàng loạt cho sơ đồ khái niệm đơn giản; class graph dày defer về SSOT. |
| diagram-auditor/scripts/audit-diagrams.mjs | Empty scope fail; scan recursive; kiểm PNG + source; đọc SVG text có tspan; cảnh báo graph Use Case/Class; công khai giới hạn kiểm tra giao cắt. |
| diagram-auditor/SKILL.md | Ghi rõ static/semantic/visual là các cổng khác nhau. |
| diagram-orchestrator/reference/manual-fallback.md | Thống nhất hai lối fallback, tránh mâu thuẫn ngưỡng. |
| diagram-orchestrator/scripts/run-evals.mjs | Thêm EVAL-06/EVAL-07, expected warnings và thông điệp static-only. |
| evals/06_class_rutgon_hub/ | Fixture class graph có hub, association khác vai trò, hidden constraints và comment đếm lớp cố ý sai. |
| evals/07_use_case_multi_actor/ | Fixture 4 actor, 18 use case, 3 package, 5 hidden links và step0-fixture.md. |
| tldraw-diagrams/scripts/render.mjs | Fail-fast khi direction/ID/endpoint sai; bend=0 mặc định straight. |
| tldraw-diagrams/SKILL.md | Nêu rõ fixed-grid-by-order, không quảng bá là topology-aware auto-layout. |
| diagram-design/SKILL.md + references/primitives-core.md | Bỏ tham chiếu geometry checker không tồn tại; ghi geometry QA hiện chưa tự động. |
| docs/rule-conflicts.md | Thêm DIAG-13 đến DIAG-19 vào sổ đăng ký finding. |
| .agents/skills/ | Đồng bộ mirror tương ứng trong phạm vi cập nhật. |

## 6. Việc còn lại — không tuyên bố đã hoàn tất

Các việc sau vẫn là gate bắt buộc trước khi xác nhận PASS:

1. Chạy node --check cho auditor, eval runner và tldraw renderer.
2. Chạy node .claude/skills/diagram-orchestrator/scripts/run-evals.mjs; xác nhận cả 7 case render thành công và expected warnings được nhận diện.
3. Test auditor với scope rỗng, scope có thư mục con và SVG thiếu nguồn.
4. Chạy tools/audit-skills.ps1 -Block coord-diagrams, tools/verify-skills.ps1 và kiểm parity giữa .claude/skills với .agents/skills.
5. Mở từng PNG EVAL-06/EVAL-07 ở kích thước đọc được như in A4; ghi Proof-of-View và lỗi quan sát cụ thể.
6. Cân nhắc xây geometry checker thực sự cho giao cắt edge-edge, node-edge và label-edge. Việc này chưa được tự động hóa trong thay đổi hiện tại.

## 7. Điều kiện nghiệm thu sau runtime

| Gate | Điều kiện PASS |
|---|---|
| Source/runtime | Script syntax hợp lệ; bảy eval chạy; warnings regression được bắt; edge sai không bị âm thầm bỏ. |
| Artifact completeness | Mỗi SVG có PNG và nguồn chỉnh sửa cùng tên; scope rỗng không thể pass. |
| Semantic | Bước 0 có bằng chứng; association/role/multiplicity không bị sửa chỉ để làm đẹp. |
| Visual | Đã mở ảnh; không node/label overlap, connector xuyên hộp, đường vòng xa khó lần, dồn hub hoặc chữ không đọc được ở A4. |
| Mirror/governance | .claude và .agents parity; link tương đối hoạt động; report ghi rõ phần chưa kiểm chứng. |

**Trạng thái hiện tại: CHANGES PREPARED — RUNTIME / VISUAL VERIFICATION NOT RUN.** Không ghi PASS cho sơ đồ hay toàn nhóm skill cho đến khi các gate ở mục 6 được chạy và có bằng chứng lưu lại.
