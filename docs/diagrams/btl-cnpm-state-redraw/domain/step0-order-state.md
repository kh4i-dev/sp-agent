# Bước 0 — vòng đời Order

Đối tượng: `Order.status`, không phải `EscrowHold.status`, `ReturnRequest.status` hay trạng thái trang giao diện. Mục tiêu: diễn đạt gọn hợp đồng chuyển trạng thái đã khai báo để thay ảnh State sai ký hiệu/dày dây. Vai trò phát sinh sự kiện: người mua thanh toán/hủy/xác thực/xác nhận, người bán đóng gói, tài xế nhận/giao, hệ thống giải ngân theo điều kiện, vận hành xử lý sự cố. Vai trò dựa trên các module orders/shop/delivery/tracking/admin và core escrow, không tự thêm actor vào State.

**Góc nhìn được chọn: declared**, theo `backend/src/common/enums.ts:17–38`. Chín giá trị state và 12 cặp khai báo được giữ đầy đủ sau mở rộng composite. Đây không phải tuyên bố 12 cặp đã được triển khai/cưỡng chế. Các lệch service nằm ở audit; không chỉnh backend trong công việc vẽ hình.

Quy mô dữ liệu thực tế không cần để quyết định mô hình này: UNKNOWN. Trạng thái kết thúc vùng chỉ được đặt sau Cancelled/Returned vì hợp đồng không có cạnh ra; Completed còn tới Returned nên không phải FinalState.
