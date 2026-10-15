# Class Diagram Layout — Quy tắc bố cục có kiểm chứng

> **Owner / SSOT:** diagram-orchestrator. Các skill PlantUML, use-case-layout, simplified-diagrams và diagram-auditor phải dùng tài liệu này khi sơ đồ có nhiều lớp/quan hệ. Đây là quy tắc dành cho UML Class Diagram; không được áp máy móc sang ERD hoặc Use Case.

## 1. Mục tiêu và nguyên nhân thường gặp

Một Class Diagram có thể render đúng cú pháp nhưng vẫn không dùng được khi:
- Một lớp trung tâm (ví dụ User) có nhiều quan hệ tới hồ sơ, yêu cầu, hội thoại, đánh giá, báo cáo và mục yêu thích.
- Hai lớp có nhiều association có ý nghĩa khác nhau (ví dụ reviewer và reviewee) tạo đường gần trùng, nhãn mơ hồ.
- Nhiều lớp đặt thành hàng nhưng các quan hệ thật nối chéo giữa nhiều hàng.
- Ràng buộc hidden link tạo thứ tự bố trí cứng, trong khi các association thật lại phải chạy vòng xa.
- linetype ortho, nodesep và ranksep bị hiểu nhầm là bộ giải giao cắt. Chúng chỉ ảnh hưởng kiểu định tuyến/khoảng cách; không bảo đảm đồ thị không giao cắt.
- Một hình chứa đồng thời quá nhiều thuộc tính, phương thức và quan hệ nên phải nén chữ hoặc để các cạnh dài.

## 2. Trước khi viết .puml: lập bảng cấu trúc

Tạo/ghi trong file mô hình một bảng trước khi bố trí:

| Trường | Nội dung |
|---|---|
| class_id | Alias ổn định trong PlantUML |
| responsibility | Trách nhiệm theo code/SSOT |
| domain_group | Nhóm nghiệp vụ thực sự |
| degree | Số association đầu mút; tính riêng cạnh hidden |
| hub | YES khi degree >= 5; đây là tín hiệu cần xem layout, không phải lỗi nghiệp vụ |
| parallel_roles | Các association cùng cặp lớp nhưng mang ý nghĩa khác nhau |
| layout_zone | Khu vực dự kiến trên trang |
| evidence | File/line hoặc nguồn xác nhận quan hệ |

Đếm riêng:
- Số lớp khai báo và số lớp thật sự có quan hệ.
- Số association nghiệp vụ và số hidden constraint.
- Bậc từng lớp (degree), đặc biệt lớp có bậc cao.
- Cặp lớp có nhiều quan hệ mang vai trò khác nhau.
- Mật độ quan hệ: E / V và bậc trung bình 2E / V. Chỉ dùng để cảnh báo độ phức tạp, không dùng làm tiêu chí tự động kết luận mô hình sai.

Nếu mô hình quá dày, chọn một sơ đồ tổng quan nhỏ + các sơ đồ chi tiết theo câu hỏi. Không nhân bản lớp sang nhiều hình mà không đánh dấu chúng là các góc nhìn của cùng mô hình.

## 3. Bố trí node theo cấu trúc quan hệ

1. **Nhóm theo miền nghiệp vụ**, không theo thứ tự khai báo thuận tiện. Ví dụ tùy code: tài khoản/hồ sơ; kết nối; hội thoại/tin nhắn; đánh giá/kiểm duyệt.
2. **Đặt hub có chủ đích.** Lớp có degree cao không tự động phải nằm chính giữa trang, nhưng không được đẩy ra góc nếu phần lớn cạnh phải xuyên qua toàn sơ đồ. Thử vị trí gần trung tâm của các nhóm liên quan, hoặc tách góc nhìn.
3. **Đưa cặp liên kết mạnh/đặc biệt gần nhau.** Nếu hai lớp có nhiều association khác vai trò, đặt sát nhau chỉ khi vẫn phân biệt được từng cạnh và nhãn. Nếu không thể tách bằng bố cục thì tách sơ đồ hoặc dùng association-end role/association class khi đúng UML và đúng nghiệp vụ.
4. **Không ép lưới 3 cột bằng hidden links cho mọi lớp.** Bắt đầu bằng ít ràng buộc nhất; chỉ thêm một hidden link khi nó giải quyết một vấn đề bố cục được quan sát. Mỗi hidden link mới phải kiểm tra lại tất cả cạnh thật.
5. **Không để các association nối xa qua nhiều vùng.** Nếu một lớp nối tới nhiều nhóm ở xa, cân nhắc chuyển vị trí node hoặc tạo các góc nhìn theo domain. Không xóa quan hệ thật để làm hình đẹp.
6. **Đặt tên vai trò rõ ràng.** Nhãn association không được làm người đọc nhầm vai trò đầu mút. Với Review–User, reviewer và reviewee là hai vai trò khác nhau; không gộp chúng vì hình học. Xác minh multiplicity và đặt role name ở đúng đầu mút nếu biểu diễn đó chính xác.
7. **Phương thức/thuộc tính là một chiều phức tạp riêng.** Nếu Class Diagram đầy đủ không đọc được ở A4, tạo class overview chỉ gồm tên và quan hệ, còn phương thức/thuộc tính đi vào hình chi tiết hoặc bảng trách nhiệm. Không xóa thành phần nghiệp vụ âm thầm.

## 4. Quy tắc thử PlantUML

Thử theo đúng thứ tự, một thay đổi mỗi vòng:
1. **Baseline:** render nguyên nguồn, ghi kích thước và lỗi quan sát được.
2. Rút gọn nhãn dài mà không làm mất ý nghĩa; giữ thuộc tính/phương thức theo mức trừu tượng đã duyệt.
3. Thử hướng tổng thể phù hợp (left to right direction hoặc bố cục trên-xuống) và thứ tự khai báo/nhóm.
4. Thử linetype ortho so với polyline khi cạnh vòng xa hoặc nhiều đường chạy song song. Không có kiểu nào luôn tốt hơn.
5. Thêm/bỏ một hidden constraint; render lại để quan sát ảnh hưởng lên mọi cạnh.
6. Nếu vẫn còn cạnh vòng xa, các lớp dồn cục hoặc vùng trắng mất cân đối sau hai vòng có ích, dừng vá tham số và chuyển sang draw.io/định vị thủ công theo manual-fallback.md.

Không tuyên bố “đã giảm giao cắt” chỉ từ source diff. So sánh hai ảnh render cùng tỷ lệ.

## 5. Khi nào phải phân rã

Phân rã nếu một trong các điều kiện sau khiến hình không còn dễ lần theo:
- Lớp hub có nhiều cạnh xuyên qua các nhóm.
- Có nhiều quan hệ song song/đồng cặp khiến nhãn khó gán cho đúng cạnh.
- Nhiều đường nối dài hơn nhiều lần khoảng cách thẳng giữa hai đầu.
- Phương thức/thuộc tính làm chữ nhỏ dưới tiêu chuẩn in.
- Cấu trúc không thể bố trí cân bằng nếu không thêm hàng loạt hidden links.

Mỗi hình chi tiết cần câu hỏi riêng, tên/caption riêng, cùng alias/tên lớp thống nhất với mô hình gốc. Không làm cho hình nhẹ hơn bằng cách bỏ association thật mà không ghi nhận.

## 6. Kiểm định hình học

Visual Review phải ghi cụ thể:
- Các cặp đường giao cắt (hoặc UNKNOWN nếu chưa thể xác nhận).
- Cạnh chạy xuyên hộp lớp, nhãn, hoặc vùng nhóm.
- Cạnh vòng xa, số lần bẻ góc và các bó đường gần song song.
- Hub/bậc cao, vị trí tương đối và khoảng trắng.
- Nhãn association có gắn đúng cạnh; role và multiplicity có đọc được.
- Khả năng đọc ở kích thước nội dung thực tế trên A4, không chỉ ở zoom lớn.

Bộ kiểm tra tự động có thể cảnh báo độ dày đồ thị và một số va chạm hình học; nó không được tuyên bố không giao cắt nếu chưa phân tích đầy đủ các path segment. Proof-of-View vẫn bắt buộc.

## 7. Bài học từ ví dụ class_rutgon

Trong ví dụ được cung cấp, nguồn liệt kê 12 khai báo lớp dù comment ghi “11 lớp”; quan hệ tập trung mạnh quanh User và có hai quan hệ khác vai trò giữa Review–User, cùng hai quan hệ giữa Report–User. Ảnh chụp cho thấy các lớp dồn về phía phải, nhiều đường đứng gần song song và khoảng trắng lớn bên trái. Đây là hai loại finding riêng:
- **Source/model consistency:** số lượng lớp và quan hệ phải đối chiếu với hình render; không thể dựa vào comment.
- **Visual layout:** cần bố trí lại hub/nhóm hoặc phân rã, không chỉ tăng nodesep/ranksep.

Không tự kết luận association là sai chỉ vì chúng chồng hình; cần kiểm ngữ nghĩa từ mã nguồn và dữ liệu trước khi sửa.
