# Audit và vẽ lại State Order — 01/11/2026

## Kết luận và phạm vi

**Mô hình khai báo: đủ 9 state, 12 cặp chuyển sau mở rộng composite. Bố cục bản PNG Chromium đã soi: đạt trong phạm vi và kích thước trình bày đã chọn. Chưa xác nhận runtime tương ứng toàn bộ 12 cặp.** Không thay hình trong Word/slide.

## Lỗi ảnh người dùng gửi

- Thiếu điểm bắt đầu; state vuông; dùng hộp viền đôi cho Hoàn tất/Trả hàng/Đã hủy thay FinalState bullseye.
- “Hoàn tất” còn đường ra Trả hàng: không thể dùng ký hiệu final cho chính state này.
- Nhiều đường hủy/hoàn tiền kéo qua nửa hình, cạnh đứng sát nhau bên phải, khó lần nguồn/đích.
- Bốn dòng chú thích nằm trong ảnh dù dự án cấm chú thích. Từ “trạng thái kép” diễn giải tên DeliveredVerified không chứng minh state phân cấp UML.
- Đánh đồng hủy với hoàn tiền, khiếu nại với trả hàng; ghi cứng 72 giờ bỏ cấu hình và điều kiện tiền/tranh chấp.

Lưu ý: trong lúc audit, bản file trên đĩa đã khác ảnh chụp người dùng gửi: generator hiện có state bo góc và đã bỏ note. Không gán mọi lỗi ảnh cũ cho bản nguồn mới. Các file bị thay được chụp hash trước khi publish để tránh đè thay đổi đang diễn ra.

## Những sai lệch nghiệp vụ phát hiện khi đọc code

| Phát hiện | Bằng chứng | Kết luận |
|---|---|---|
| Bảng ORDER_TRANSITIONS chỉ được khai báo, không có nơi dùng trong src | tìm toàn `backend/src` cho ORDER_TRANSITIONS | Đếm đủ 12 cạnh chỉ chứng minh khớp hợp đồng, không chứng minh runtime |
| Checkout tạo thẳng Paid | `core/split-order.service.ts:91` | Initial PendingPayment thuộc mô hình khai báo, không mô tả entry của checkout ví hiện tại |
| Bảng cho Packed→Cancelled nhưng hàm cancel chỉ cho pending/paid | `modules/orders/orders.service.ts:49–53` | DECLARED_ONLY ở nhánh hủy Packed |
| Cancel không gọi hoàn tiền | cùng hàm cancel | Bỏ effect hoàn tiền khỏi nhãn hủy; không sửa backend |
| Hai cạnh trả hàng hậu giao được khai báo nhưng writer Returned thực tế thuộc incident | `modules/admin/admin.service.ts:211–214`; bảng enums `:34–35` | Không gọi hai cạnh này IMPLEMENTED; cần đợt thiết kế/kiểm thử riêng để đồng bộ |
| Quét tem chỉ xác thực | `core/parcel-verified.listener.ts:26–29` | Không gắn effect giải ngân cho quét tem |
| Completed do escrow.release ghi; xác nhận và scheduler gọi có điều kiện | `escrow.service.ts:157`, `tracking.service.ts:50–52`, `escrow-auto-release.service.ts:37–53` | Dùng nhãn kết quả “giải ngân thành công”; giải thích điều kiện ngoài ảnh |
| Deadline không cố định 72h | `escrow.service.ts:85` | Không in timeout cứng trong sơ đồ |

## Năm kiểm tra độc lập

| Cổng | Trạng thái và bằng chứng |
|---|---|
| Nguồn/UML | Đạt cho **declared view**; 12 cặp được lấy độc lập từ enums và khớp sau mở rộng. Không PASS runtime. Initial, FinalState, composite và Completed kiểm theo model |
| Render | SVG hợp lệ; PNG Chromium 2960×2060, có metadata 300DPI; 21 text dòng chỉ là nhãn UML, không chú thích. Drawio chỉnh sửa được và anchor dùng cùng tọa độ; chưa render trong editor drawio |
| Tự động | Bộ kiểm model + 7 regression cases chạy thành công. Chromium đo 0 cạnh cắt bbox chữ; text khớp danh mục model, min font 27px ≈9.7pt tại rộng 25cm. Eye-audit vòng cuối HIGH=0/MEDIUM=7/LOW=2, ứng viên đã phán dưới đây |
| Soi mắt | Mở PNG, overlay, 9/9 crop tự động và 3/3 crop pixel Chromium. Một vòng sửa đã bỏ nền nhãn làm mất viền; vòng kế phát hiện/sửa nhãn giải ngân cắt dây trả hàng; vòng 3 soi lại đạt |
| Word/slide | NOT RUN. Không thay tài liệu chứa ảnh; không khẳng định bố cục A4 dọc 15cm đạt |

## Proof-of-View

“Chờ thanh toán” ở trái trên trong Trước vận chuyển; “Đã xác thực” ở giữa phải trong Sau giao hàng; “Hoàn tất” ở dưới phải, “Trả hàng” ở dưới trái; hai state cuối này có mũi tên đi từ Hoàn tất về Trả hàng, chỉ Trả hàng đi vào final.

**Đè:** không thấy nét cắt chữ hoặc nền nhãn che viền ở bản Chromium cuối; nhãn giải ngân hai dòng ở bên phải đường đứng, không cắt đường trả hàng. **Đều:** state thường cùng 220×76, spine thẳng hàng, nhánh có khoảng thoáng. **Dễ nhìn:** luồng chính sang phải rồi xuống; hai nhánh hủy và trả tách trái; không còn bó dây vòng mép canvas hay footer. Tên composite là nhãn cấu trúc UML hợp lệ.

## Verdict ứng viên vòng 3

| Crop | Verdict | Mắt đã thấy |
|---|---|---|
| F01 C-DANGLE | BAO-OAN | góc bo trên phải của composite Trước vận chuyển, viền liền; không phải connector lơ lửng |
| F02 C-DANGLE | BAO-OAN | cùng góc bo được parser đọc hai đầu của path kín |
| F03 C-DANGLE | BAO-OAN | góc bo composite Sau giao hàng, viền nối liên tục |
| F04 C-DANGLE | BAO-OAN | cùng viền kín composite bị tính như connector |
| F05 C-DANGLE | BAO-OAN | cạnh rời chấm initial và đi vào state; parser không nhận chấm đen là node |
| F06 C-DANGLE | BAO-OAN | cạnh chạm vòng ngoài bullseye sau Đã hủy; parser bỏ FinalState |
| F07 C-DANGLE | BAO-OAN | cạnh chạm bullseye sau Trả hàng; không neo lơ lửng |
| F08 S-FONT | BAO-OAN đối với PNG bàn giao | PyMuPDF dùng font fallback và không hiện marker; đã đối chiếu 3 crop Chromium thấy Arial dấu rõ, đủ đầu mũi tên. Không dùng ảnh crop MuPDF làm ảnh giao |
| F09 D-DUP | CHAP-NHAN-DUOC | hai nhãn chấp thuận trả hàng thuộc hai nguồn state khác nhau, đúng hai cặp khai báo; không gộp làm mất nghĩa |

Parser đọc 9 state thường, 20 khối nhãn (21 dòng), **14 path trong đó 2 path là viền composite**; thực tế có 12 connector vẽ (9 cạnh nghiệp vụ nén + initial + 2 completion final). Không lấy con số 14 này làm số chuyển hợp đồng.

## Nguồn web đã đọc

[OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1) (trang đặc tả; PDF quá lớn không tải được qua web tool); [Quantum Leaps Crash Course](https://www.state-machine.com/doc/AN_Crash_Course_in_UML_State_Machines.pdf) §1.2.2, §1.2.5, §2.1; [Initial transitions](https://www.state-machine.com/qm/sm_init.html); [Transitions](https://www.state-machine.com/qm/sm_tran.html); [Sparx Transition](https://www.sparxsystems.com/enterprise_architect_user_guide/17.2/modeling_languages/transition.html).

Không chú thích trên canvas là yêu cầu của dự án/người dùng, không phải một lệnh cấm UML. Không dùng nguồn internet để thay nguồn nghiệp vụ của dự án.
