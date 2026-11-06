
> **Quy tắc hiện hành (02/11/2026):** bản cuối dùng `handdrawn-diagrams`: Python toạ độ cố định → `docs/diagrams/vectors/*.svg` + `docs/images/diagrams/*.png`, spec JSON riêng. PlantUML/Graphviz/Mermaid/drawio/tldraw trong các ví dụ bên dưới chỉ dùng nháp. Nguồn `.py` là bắt buộc. Duyệt ngữ nghĩa theo nguồn, chạy `run_diagrams.py` (cổng máy), rồi Vision QA từng hình; không suy PASS bố cục từ exit 0. Use Case chung gốc ở junction thân–tay `(ax, ay−4)` = tâm đầu +18 với mẫu hiện hành, không ở bụng. State đọc `plantuml-diagrams/reference/state-playbook.md`, không note/legend/footer trên canvas. Khi hướng dẫn cũ trái khối này, áp dụng khối này.

# Bố trí actor và chức năng theo ảnh mẫu (2026-11-01)

Áp dụng cho Use Case; đây là SSOT thay thế hướng dẫn cũ cấm chùm dây một điểm hoặc kéo dài actor. Ảnh người dùng cung cấp là tham chiếu bố cục, không phải nguồn xác nhận nghiệp vụ.

## Nghĩ theo vai trò trước khi đặt tọa độ

1. Lập ma trận actor × mục tiêu từ nguồn dự án. Không gộp Kỹ thuật, Nhân viên, Lãnh đạo thành Admin chỉ để giảm số actor; cũng không tự thêm những vai trò này nếu nguồn chưa xác nhận.
2. Chọn phía theo cụm chức năng: actor khởi tạo hoặc vận hành có thể đứng trái **hoặc phải**. Phía phải không dành riêng cho dịch vụ ngoài. Với nhiều vai trò, thử bố cục hai bên trước khi chọn toàn bộ bên trái; một actor hoặc các actor kế thừa cùng phía vẫn hợp lý.
3. Đặt actor ngang trọng tâm cụm của mình, giữ người que nhỏ, tỷ lệ bình thường và cùng kích thước giữa các vai trò. Không kéo thân cao bằng cả cột chức năng.
4. Xếp chức năng chính thành cụm lệch hàng, lệch khoảng cách ngang có chủ đích, tạo dáng quạt mở như ảnh mẫu. Không ép mọi ellipse vào một cột dài, cũng không đặt tất cả lên một đường tròn có bán kính cố định. Dáng quạt không đồng nghĩa cung tròn toán học.
5. Chức năng phụ có include/extend nằm gần chức năng cơ sở, phía xa actor hơn hoặc trong khe trống giữa hai cụm. Dành khoảng trống cho nhãn nét đứt ngay khi đặt node.

## Nét nối theo mẫu

- Mỗi association là một đường liền riêng, ưu tiên **tia thẳng từ cùng một điểm ở junction thân–tay actor tới mép ellipse**. Hội tụ ở actor là chủ đích hợp lệ, không tự động là lỗi “con nhện”. Không thêm chấm junction, bus chung hoặc đoạn gốc chung làm mất danh tính cạnh.
- Điểm neo thuộc hình actor thật, không ở một điểm lơ lửng cạnh tay. Với draw.io `umlActor`, có thể bắt đầu bằng `exitX=0.5, exitY≈0.667`; SVG dùng tọa độ thân thực tế, không áp mù tỷ lệ của shape khác.
- Nhãn actor đặt phía ngoài chùm tia: bên trái actor trái, bên phải actor phải, hoặc dưới chân nếu mọi tia tránh được vùng chữ. Kiểm cả tia dốc nhất. Không ép nhãn luôn ở dưới.
- Chỉnh vị trí ellipse để tia tránh các ellipse khác. Cùng gốc chỉ bảo đảm hai tia khác hướng không cắt nhau ngoài gốc; **không bảo đảm** tránh node, nhãn, tia trùng hướng hoặc dây từ actor khác.
- Không dùng đường cong hoặc elbow chỉ để “tự nhiên”. Chỉ đổi kiểu khi có trở ngại thật; ưu tiên xếp lại node.
- Giữ chuẩn UML: association thường không mũi tên; include hướng đến hành vi bắt buộc; extend hướng đến use case cơ sở; kế thừa hướng tam giác rỗng về cha. Không sao chép sai hướng/quan hệ từ ảnh mẫu.

## Hai mẫu đọc từ ảnh người dùng

- Ảnh 1: “Người xem” phía trái trên, “Khách hàng” phía trái giữa; các mục tiêu tỏa vào vùng giữa/phải; chức năng phụ như “Giải ngân ký quỹ” đứng gần chức năng cơ sở. Đây là bố cục nhiều khoảng cách ngang, không phải một cột cố định.
- Ảnh 2: “Kỹ thuật / System” trái trên, “Nhân viên” trái dưới, “Lãnh đạo / Sếp” bên phải. Chức năng của mỗi vai trò nằm về phía trong; quan hệ liên vai trò dùng vùng giữa. Không biến sự phân vai trong hình này thành yêu cầu của mọi dự án.
- Bản `btl-cnpm/private-docs/images/diagrams/slide-usecase-noi-bo-v6.png` đã xem: “Quản trị viên” trái trên, “Vận hành” trái giữa, “Kỹ thuật” trái dưới; “Duyệt yêu cầu rút tiền” nằm trong cùng một cột chức năng rất dài. Đây là đối chứng cần cải thiện: thử phân cụm hai phía và giảm chiều cao trước khi tăng khung hoặc thu chữ.

## Kiểm trước khi bàn giao

Ở bản thu nhỏ phải nhận ra từng actor cùng cụm chức năng; không còn một dải ellipse kéo dài và nửa khung trống. Ở bản phóng đại lần theo từng tia đến đúng ellipse; không xuyên chữ, tên actor hay ellipse khác. `C-FAN` chỉ là ứng viên: nếu quạt đúng mẫu, các tia phân biệt được và không đè, ghi `CHAP-NHAN-DUOC` kèm bằng chứng; không sửa thành actor khổng lồ hoặc rải neo chỉ để tắt cảnh báo. Vẫn thực hiện đầy đủ visual-audit-protocol, không lấy bố cục mẫu thay cho kiểm ảnh.
