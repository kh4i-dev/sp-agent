# Audit Use Case btl-cnpm — 01/11/2026

Phạm vi: bốn bản `private-docs/images/diagrams/slide-usecase-{nguoi-mua,nguoi-ban,tai-xe,noi-bo}.png` đang tồn tại, SVG/drawio cùng tên, generator và các controller/service liên quan. Không dùng v5 làm bản hiện hành. Không sửa dự án btl-cnpm. Chưa audit toàn bộ ERD/Activity/Sequence hoặc ảnh nhúng Word/PowerPoint.

Kết luận: **FAIL bố cục** so với ảnh mẫu người dùng. Không xác nhận toàn bộ nghiệp vụ PASS; các lỗi và giới hạn dưới đây độc lập với việc generator chạy được.

## Phát hiện đã xác minh

| Mức | Phát hiện | Bằng chứng | Cách sửa |
|---|---|---|---|
| P1 | Generator bỏ qua phía actor, ép mọi vai trò sang trái | `gen_usecase.py:49` đọc `(name,indices,_)`; `:55` ghi x=150 cho tất cả. Ảnh nội bộ: Quản trị viên, Vận hành, Kỹ thuật, Lãnh đạo đều bên trái | Giữ trường side; bố trí vai trò theo cụm và thử Lãnh đạo phía phải theo mẫu, không đổi quyền để hợp hình |
| P1 | Mọi UC chính bị ép một cột và các cụm nối dài theo chiều dọc | `gen_usecase.py:54,58`: mọi tâm x=570, y tăng 96. Ảnh mua/bán/nội bộ có dải ellipse dài, vùng phải phần lớn trống | Đặt chức năng lệch ngang theo cụm; đưa các nhánh sát chức năng cơ sở; thu khung sau khi xếp node |
| P1 | Gốc association không gắn vào thân actor trên SVG | `gen_usecase.py:82`: gốc `(x+22,y)` trong khi thân ở x; tay ngang nằm tại y−10. Quan sát bốn ảnh: chùm dây xuất phát ở điểm trắng bên phải thân, dưới tay | Neo ở thân/bụng thật; giữ actor kích thước bình thường |
| P1 | SVG và drawio không bảo đảm cùng điểm chạm ellipse cho cạnh chéo | SVG `:82` dùng mép trái cố định `(cx−145,cy)` cho mọi góc; `:96` drawio dùng entryX=0, entryY=0.5 nhưng không khóa entryPerimeter=0. SVG vẽ ellipse sau cạnh nên có thể che đoạn đi vào lòng ellipse | Tính giao điểm tia–ellipse theo hướng cạnh và khóa tọa độ nhất quán hai định dạng; render lại drawio để đối chiếu |
| P2 | Tài liệu audit trỏ bản v6 không còn tồn tại | `use-case-audit.md:6–7` trỏ `*-v6.*`; generator `:113` xuất tên không hậu tố; kiểm kê hiện tại chỉ có v5 và bản không hậu tố | Chọn một bộ hiện hành và sửa liên kết, không để người đọc tìm bản v6 không có |
| P2 | Nguồn Bước 0 và mô hình lịch sử mâu thuẫn quyền hiện tại | `domain/step0-tmdt.md` nói IT chỉ xem cấu hình và Admin không là actor nghiệp vụ; `diagrams/step0-san-tmbt-usecase.md` lại cho IT đề xuất cấu hình. Mã `admin-settings.controller.ts:30–34` cho IT tạo nháp, `:37–44` cho Exec duyệt; ảnh hiện hành vẽ đúng hướng này | Đồng bộ một Bước 0 có nguồn theo hành động; đánh dấu bản cũ rõ ràng |
| P2 | “72 giờ” bị trình bày như hằng số cố định | Ảnh tài xế có “Mở cửa sổ 72 giờ”, ảnh mua ghi tự giải ngân sau 72 giờ. `core/escrow.service.ts:85` đọc `escrow_release_hours` / `ESCROW_AUTO_RELEASE_HOURS`, mặc định 72 | Ghi “Mở thời hạn kiểm tra” và chú thích mặc định 72 giờ, hoặc nêu rõ cấu hình demo 72 giờ đã được kiểm chứng |
| P2 | Include tất toán khiến người đọc dễ hiểu là bảo đảm tất toán thành công dù code có thể nuốt lỗi | Ảnh nội bộ: “Phán quyết khiếu nại” include “Tất toán ký quỹ”. `disputes.service.ts:110,115` bắt lỗi release rồi bỏ qua, sau đó `:120` vẫn ghi resolved | Không coi hình là bằng chứng tiền đã tất toán. Nêu hạn chế hiện thực; nếu cần bảo đảm nghiệp vụ thì có đợt sửa/kiểm thử backend riêng |

Không coi quạt chung gốc là lỗi. Lỗi đã thấy là **gốc lơ lửng**, **xếp cột dài** và **bỏ phía actor**. Cũng không coi thiếu đường quyền dùng chung là lỗi chắc chắn: ảnh nội bộ tự giới hạn ở vai trò phụ trách chính.

## Bằng chứng trực tiếp từ từng ảnh

| Ảnh | Ba nhãn đọc từ ảnh và vị trí | Đè / đều / dễ nhìn |
|---|---|---|
| Người mua | “Khách xem” trái trên; “Xác thực tem nhận hàng” giữa; “Giải ngân ký quỹ” phải giữa | Cột chính dài; actor Người mua ở giữa nhưng dây kéo rất xa lên “Tìm và xem sản phẩm”; vùng phải trống ngoài ba nhánh. Không tuyên bố sạch mọi giao cắt khi chưa có crop audit |
| Người bán | “Người bán” trái giữa; “Đóng gói và in tem QR” giữa trên; “Phản hồi đánh giá” phải giữa | Cùng gốc lơ lửng cạnh thân; chức năng xếp một cột dài; nhánh phải cách xa làm khung rộng |
| Tài xế | “Tài xế” trái giữa; “Xác nhận giao hàng” giữa; “Mở cửa sổ 72 giờ” phải giữa | Dễ nhận nhóm hơn hai hình trên nhưng vẫn một cột; gốc association không chạm thân; hai nét đứt đến/đi chức năng giao hàng cần soi crop |
| Nội bộ | “Quản trị viên” trái trên; “Vận hành” trái giữa; “Lãnh đạo” trái dưới | Bốn vai trò bị xếp một phía; cột chức năng kéo cao; nửa phải phần lớn trắng. Không giống mẫu hai phía người dùng yêu cầu |

Dấu vết SHA256, kích thước và thời gian tệp: `files.json` cùng thư mục. Đã mở riêng cả bốn PNG vào ngữ cảnh thị giác.

## Năm kiểm tra độc lập

1. **Render:** bốn PNG/SVG hiện hành tồn tại và PNG đã mở được. Không chạy sinh lại; chưa đối chiếu render thật từ drawio. Cỡ chữ thực tế trong slide/A4 chưa đo.
2. **Tự động:** đã chạy `audit-diagrams.mjs` cho thư mục SVG, log `static-audit.txt`. 82 báo lỗi thô trên cả thư mục **không phải 82 lỗi đã xác nhận**: nhiều báo thiếu PNG/source do script đòi cùng thư mục trong khi dự án tách `svg/`, `drawio/`, `images/diagrams/`. Các cảnh báo ngoài bốn Use Case chưa soi và chưa kết luận.
3. **Soi ảnh:** FAIL với lỗi cụ thể trong bảng. `eye_audit.py --overlay --dump` đã thử cho nội bộ nhưng không chạy được vì Python mặc định thiếu PyMuPDF. Chưa có overlay/crop đầy đủ; không chứng nhận bất kỳ hình nào PASS.
4. **Nghiệp vụ:** có Bước 0, đã đối chiếu chọn lọc controller/service. IT đề xuất và Exec duyệt cấu hình có mã hỗ trợ. Quét tem và giải ngân là hai việc tách biệt trong mã. Chưa kiểm thử runtime, server hoặc DB; không tuyên bố phát hiện bug runtime đã tái hiện.
5. **Word/slide:** NOT RUN; chưa đọc/render tài liệu chứa hình trong đợt audit này.

Ưu tiên sửa: layout generator và điểm neo → thống nhất nguồn actor/quyền → cập nhật tên tệp/tài liệu → render từng hình và chạy đủ overlay/crop trước khi thay vào Word/slide.
