# Mô hình và nguồn

View: **declared**, bám `backend/src/common/enums.ts:17–38`. Hai composite là nhóm phân cấp để biểu diễn đúng các exit chung của hợp đồng; không phải hai giá trị mới trong DB. Không đổi backend để làm hình đúng.

| State nguồn | Đích | Cách hiển thị |
|---|---|---|
| PendingPayment | Paid | thanh toán |
| PendingPayment | Cancelled | exit chung của Trước vận chuyển |
| Paid | Packed | đóng gói |
| Paid | Cancelled | exit chung của Trước vận chuyển |
| Packed | Shipping | nhận kiện |
| Packed | Cancelled | exit chung của Trước vận chuyển |
| Shipping | Delivered | giao thành công |
| Delivered | DeliveredVerified | xác thực tem |
| Delivered | Completed | exit chung của Sau giao hàng, giải ngân thành công |
| DeliveredVerified | Completed | exit chung của Sau giao hàng, giải ngân thành công |
| DeliveredVerified | Returned | chấp thuận trả hàng |
| Completed | Returned | chấp thuận trả hàng |

Trigger trên hình là tên nghiệp vụ cho hợp đồng khai báo, không phải tên event emitter đã được xác nhận cho mọi cạnh. Đặc biệt hai cạnh trả hàng hậu giao là **DECLARED_ONLY**, chưa tìm thấy service thực hiện đúng cặp source→target này. Hủy Packed cũng DECLARED_ONLY; không có effect “hoàn tiền” đi kèm trên hình.

Nguồn kiểm tra phần đã triển khai: `orders.service.ts:49–53` (hủy pending/paid), `shop.service.ts:265–266` (packed), `delivery.service.ts:667,712–722,744,768–778` (shipping/delivered), `parcel-verified.listener.ts:26–29` (delivered_verified), `tracking.service.ts:44–56` (xác nhận chỉ gọi release khi điều kiện đúng), `escrow.service.ts:157` (completed), `admin.service.ts:211–214` (returned sau xử lý incident).

Giải ngân có thể được kích hoạt bởi xác nhận hợp lệ hoặc bộ lịch quá hạn; nhãn “giải ngân thành công” là kết quả làm đổi Order.status. Hủy không đồng nghĩa hoàn tiền, quét tem không đồng nghĩa giải ngân, mở khiếu nại không đồng nghĩa đã trả hàng. Tùy chọn thời gian kiểm tra đọc cấu hình tại `escrow.service.ts:85`, không in cứng 72 giờ.

Layout: spine ba trạng thái đầu nằm hàng trên trong composite Trước vận chuyển; Shipping bên phải; Delivered và DeliveredVerified trong composite Sau giao hàng; Cancelled bên trái gần composite nguồn, Returned dưới gần nhánh hậu giao. Hai vòng bullseye nằm ngay dưới hai state không có cạnh ra. Không footer/title/note; tên composite là nhãn UML có ý nghĩa, không chú thích.

Kích thước xuất: SVG 1480×1030; PNG 2960×2060. Đích trình bày: full-slide hoặc trang ngang, rộng **25 cm**, min chữ 27px tương đương khoảng 9.7pt. Nếu chèn 15cm thì phải phân rã/tăng chữ; không suy tăng DPI làm chữ lớn hơn.
