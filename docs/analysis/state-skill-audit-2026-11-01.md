# Audit skill State — 01/11/2026

Phạm vi: plantuml-diagrams (entrypoint, state-playbook, bộ kiểm/xuất và test), các hướng dẫn điều phối có thể ghi đè State/Use Case, đồng bộ `.claude`/`.agents`. Không phải audit ngữ nghĩa toàn bộ 44 skill. Không sửa backend hoặc sơ đồ trong btl-cnpm ở đợt này.

## Lỗi đã xác minh và sửa

| Mức | Lỗi trước sửa | Bằng chứng và sửa |
|---|---|---|
| P1 | Kiểm model dùng assert, bị vô hiệu với Python -O | Chạy test cũ dưới -O: 5/7 ca thất bại vì model sai được nhận. Thay bằng ValueError luôn thực thi; suite mới đạt 21/21 trong cả hai chế độ |
| P1 | ID 0/1 hoặc ID không an toàn có thể trùng phần tử gốc drawio/đi vào SVG attribute | Tái hiện model dùng id=0 được nhận. Chặn bằng quy tắc named IDs an toàn, dùng chung cho node/edge |
| P1 | Đích composite bị mở rộng thành mọi state con, sai default-entry | Tái hiện nhận composite không có default initial rồi tính A→mọi child. Bộ xuất hiện **từ chối đích composite**, yêu cầu chỉ rõ child; playbook ghi giới hạn, không giả hỗ trợ UML đầy đủ |
| P1 | Hierarchy cycle/child ngoài parent, phần tử ngoài canvas không được kiểm đầy đủ | Thêm kiểm chuỗi parent, containment, canvas bounds và tọa độ hữu hạn; ca cycle kiểm đúng thông báo, không lấy một lỗi khác làm PASS |
| P2 | Đường chéo được nhận nhưng tính offset bằng độ dài Manhattan; đoạn 0 có thể chia cho 0 | Tái hiện route chéo được nhận. Giới hạn bộ xuất ở đoạn trực giao không rỗng, chặn NaN và waypoint ngoài khung |
| P2 | Playbook cho completion không nhãn, code lại bắt có label | Cho phép completion không nhãn; test xuất SVG/drawio thật cho trường hợp này. Đồng thời chặn completion có explicit trigger |
| P2 | Nhãn event có thể giấu ở cạnh initial; cạnh tới final có thể giấu trigger | Initial label chỉ cho effect khởi tạo dạng slash; cạnh có trigger phải có nhãn, kể cả đích final |
| P2 | Bộ kiểm nhận model rỗng, label anchor ngoài ảnh hoặc initial/final không tròn | Bổ sung kiểm có concrete state, anchor hữu hạn/trong canvas và điểm nối thật trên chu vi vòng tròn |
| P2 | Composite con có thể bị nền composite cha vẽ sau che mất; text state nhiều dòng lệch tâm | Sắp ancestor trước descendant khi xuất; căn nhóm dòng quanh tâm state |
| P2 | Hướng dẫn chung vẫn ép State theo số hàng/cột hoặc bắt sửa đủ vòng; đo font in từ font-size SVG | Ghi rõ phạm vi Class/ERD và ưu tiên state-playbook, bỏ lần sửa vô nghĩa, tính cỡ chữ theo bề rộng chèn thực |
| P2 | coord-diagrams còn hard-code vai Phụ huynh/Gia sư và ép bỏ Đăng nhập, 3 cột/10–16 UC | Thay bằng dẫn chiếu SSOT Use Case hiện hành; không biến ví dụ dự án khác thành quy tắc chung |

## Kiểm chứng

- `test_state_model.py`: **21/21**; chạy lại với `python -O`: **21/21**.
- Model Order đã dùng trước đó: **12 cặp** sau mở rộng composite, vẫn được nhận.
- Xuất lại SVG bằng bộ xuất đã sửa: **byte-for-byte giống SVG đã soi trước đó**. Không phát sinh hình mới cần nhận xét lại từ suy đoán.
- `tools/verify-skills.ps1`: **44 skill hợp lệ** theo bộ kiểm cấu trúc của dự án; đây không phải chứng nhận chất lượng nội dung cả 44 skill.
- Validator skill-creator cho plantuml-diagrams: **Skill is valid**.
- Các link nội bộ State và entrypoint đã rà. Hai chuỗi `](path)` trong ví dụ Markdown là placeholder minh họa định dạng, không phải link tài nguyên bị mất.

## Giới hạn còn lại

Bộ kiểm không xác minh rằng `evidence` trỏ đúng đoạn mã hoặc `shared_exit_verified` là sự thật. Nó không thay reviewer đọc nghiệp vụ, kiểm reachability/phạm vi và soi ảnh. Bộ xuất chủ đích chưa hỗ trợ history, choice, fork/join, orthogonal region, default-entry composite hoặc internal transition. Những sơ đồ đó cần nguồn vẽ tay riêng và review thủ công.

Các bản helper từng sao chép vào btl-cnpm hoặc pack minh họa không tự cập nhật theo skill. Bản chuẩn đã sửa ở `.claude/skills/plantuml-diagrams/scripts/` và mirror `.agents`; đợt audit này không ghi đè bản helper của dự án khác.
