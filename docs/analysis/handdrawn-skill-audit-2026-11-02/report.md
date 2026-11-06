# Kiểm tra skill và layout — 02/11/2026

## Kết luận

**Chưa đủ ổn để khẳng định agent sẽ bố trí layout tốt.** Hướng vẽ bằng tọa độ cố định giúp tái lập, nhưng không tự bảo đảm bố cục đẹp. Bộ kiểm mới còn bỏ lọt lỗi; hướng dẫn giữa các skill còn lệch nhau; ảnh Use Case thực tế chưa gọn ở kích thước tài liệu.

Phạm vi: handdrawn-diagrams và sáu script của nó, skill-coordinator, coord-diagrams, một lượt test State hiện hành, hai SVG/PNG Use Case thực tế và ảnh State đã sửa trước đây. Không phải kiểm định nội dung toàn bộ 45 skill. Không sửa ảnh dự án btl-cnpm trong đợt này.

## Bằng chứng chạy thật

| Kiểm tra | Kết quả | Ý nghĩa |
|---|---|---|
| Selftest E1..E6 và ca curve có sẵn | đạt | Chỉ các fixture hiện có được bắt đúng |
| State test suite | 21/21 | Phần State đã sửa vẫn đạt các ca kiểm của nó |
| Kiểm cấu trúc skill của dự án | 45 skill hợp lệ | Không phải chứng nhận bố cục hoặc ngữ nghĩa cả 45 skill |
| So mirror handdrawn/coord/skill-coordinator | 10 file khớp trước ghi finding | Không có lệch mirror gây lỗi trong mẫu kiểm này |
| Audit hai Use Case hiện hành | 0 lỗi / 0 warning | Vẫn chưa đủ để PASS layout |
| Fan gate với Use Case nội bộ | exit 2: không nhận actor r=10 | NOT RUN, không phải PASS |

## Các lỗi bộ kiểm đã tái hiện

1. Hai nhãn trùng vị trí với halo: **0 errors**, bỏ lọt E2. Điều kiện `not has_halo` không hợp lý cho chữ đè chữ.
2. `g transform=translate(500 0)` đẩy text ngoài canvas 400px: **0 errors**, bỏ lọt E1 vì chưa áp transform.
3. `line x1=NaN`: **0 errors**, bỏ lọt E6. Hàm đọc số dùng fallback 0, kiểm NaN chỉ có ở text.
4. Rect trắng rồi text rồi line vẽ sau cắt chữ: **0 errors**, bỏ lọt E3 do chưa xét thứ tự lớp.
5. Shape ra ngoài khung: **0 errors, 1 warning**. Chưa phải cổng cứng như mô tả E1.
6. Đoạn chéo từ (100,80) đến (300,120) xuyên hộp x=150..250, y=50..150: box checker trả **[]**.
7. Runner audit trên project chỉ có một SVG, không PNG/generator: **exit 0**. Lệnh gộp chưa kiểm đầy đủ hợp đồng đầu ra hay tự gọi fan/box/selftest.

Fixture và kết quả: `probes.json`, `extra-probes.json`, các SVG lỗi có chủ đích cùng thư mục. Tái hiện bằng `python tools/check_handdrawn_skill.py`. Các lỗi này **chưa sửa code**; đã bổ sung cảnh báo OPEN trong skill để tránh agent hiểu sai phạm vi kết quả.

## Mâu thuẫn hướng dẫn còn lại

- `handdrawn-diagrams` bắt khuỷu tay nhưng một số đoạn coord/actor-function còn nói thân/bụng. AGENTS.md #13 mới ưu tiên khuỷu tay; cần đồng bộ lời hướng dẫn thay vì bắt agent tự giải xung đột.
- Handdrawn bắt halo cho mọi nhãn State, trong khi state-playbook yêu cầu xếp nhãn tránh nét và không che mất viền. Halo chỉ là công cụ cục bộ, không nên dùng để miễn kiểm mọi giao cắt.
- Skill-coordinator còn dẫn các tool cũ như đường xuất cuối; coord-diagrams phần chính đã đổi sang handdrawn nhưng còn dòng thư mục cũ và nhắc “chọn công cụ”.
- `coordinate-workflow.md` nói có logic đã chép vào `docs/diagrams/usecase_render.py`; đó là mô tả một dự án cụ thể, không bảo đảm file ấy tồn tại ở dự án mới. Không nên coi là tài nguyên sẵn có chung.
- Hướng dẫn vẫn có lưới 5 cột và số kích thước mẫu; agent cần coi đó là ví dụ, không là mặc định cho mọi domain. Chưa có bằng chứng đủ loại sơ đồ (ERD/Class/Activity/Sequence) đều được dựng và soi theo skill mới.

## Quan sát bố cục từ PNG thật

Vision audit by: Codex/GPT-6, phiên hiện tại có vision. Runtime không cung cấp mã model API chi tiết; không tự bịa mã định danh.

Đã nạp riêng ba PNG vào ngữ cảnh thị giác. Đây là lượt kiểm để tìm lỗi, **không phải chứng nhận Visual PASS** vì chưa chạy đủ overlay/crop cho từng ảnh theo quy tắc mới.

- **Người mua:** “Khách xem” trái trên; “Người mua” trái giữa; “Giữ tiền ký quỹ” phải giữa; “Gửi yêu cầu hỗ trợ” dưới trái. Hình có dáng quạt và dây thẳng nhưng quá cao, khung rộng hơn phần nội dung cần dùng, nhiều vùng trắng trên phải/dưới phải, các tia từ Người mua tới nhóm trên dài. Chưa phù hợp để gọi là gọn đẹp khi chèn slide hoặc A4 mà chưa kiểm cỡ chữ thực.
- **Nội bộ:** “Kỹ thuật” trái trên, “Quản trị viên” phải trên, “Lãnh đạo” phải dưới; “Đăng nhập / đăng xuất” ở giữa. Hai phía đã rõ hơn bản toàn actor bên trái, nhưng ellipse đăng nhập dùng chung tạo các dây chéo dài qua nhiều vùng; chữ “Kiểm duyệt sản phẩm” sát mép ellipse. Cần xét lại node dùng chung và khoảng trắng, không chỉ căn đều các node.
- **State:** “Chờ thanh toán” trên trái, “Đã xác thực” giữa phải, “Hoàn tất” dưới phải, “Trả hàng” dưới trái. Luồng và nhánh đã rõ hơn bản gốc, không footer, nhưng model là declared view và vẫn phải giữ audit về lệch runtime. Không suy ví dụ State này chứng minh mọi loại sơ đồ đã đẹp.

## Việc cần làm trước khi gọi skill ổn

Ưu tiên sửa các ca false negative của auditor và mở rộng selftest từng ca; nối cổng source/PNG/fan/box vào runner, báo NOT RUN khi parser không hỗ trợ; đồng bộ SSOT; rồi chọn một bộ ví dụ đại diện có semantic source để render, soi phóng đại và đo chữ ở kích thước chèn thật. Không dùng một con số test xanh để thay cho bước đó.
