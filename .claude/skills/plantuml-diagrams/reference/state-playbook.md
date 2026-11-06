# State Machine: mô hình trước, bố cục sau

Đây là SSOT cho State, thay thế hướng dẫn cũ ép hai hàng Login hoặc bắt mọi cạnh có nhãn/guard đối nhau. Vẽ tay draw.io/SVG với tọa độ chủ động. Trắng–đen. PlantUML chỉ làm nháp.

## 0. Không chú thích trên canvas

**Ảnh chỉ chứa phần tử UML và nhãn của chúng.** Cấm title/banner, note box, legend, footer, chữ giải thích rời, nguồn và kết luận audit. Giải thích nằm trong model/audit hoặc văn xuôi ngoài ảnh. Không chỉ tìm từ khóa `note`: phải kiểm từng text element.

Tên composite/region là nhãn cấu trúc UML hợp lệ. `entry /`, `do /`, `exit /` chỉ xuất nếu đó là hành vi có nguồn cần cho góc nhìn; không dùng compartment để lách luật nhét văn thuyết minh vào hình. Quy tắc cấm chú thích là yêu cầu dự án/người dùng, **không phải** lệnh cấm note của UML.

## 1. Ba quyết định trước khi vẽ

1. **Đối tượng:** một vòng đời của Order, Payment, Parcel... Không trộn trạng thái đơn, ký quỹ, khiếu nại và trang UI thành một tập. Tên `DeliveredVerified` không tự động là composite UML.
2. **Góc nhìn:** chọn `as-is` (mã thực thi), `declared` (hợp đồng/ma trận khai báo), hoặc `to-be` (đề xuất), ghi ngoài ảnh. Đọc **cả bảng chuyển trạng thái và lệnh ghi trạng thái**. Một hằng số không được service sử dụng không chứng minh rule được cưỡng chế.
3. **Phạm vi:** đủ vòng đời hay luồng chính đã chọn; ghi phần loại ra. Không gọi luồng chính là kiểm chứng toàn bộ hệ thống.

Lưu bảng `id | state nguồn | event | guard | effect | state đích | file:dòng | evidence_kind`. Chưa có nguồn ghi UNKNOWN; không đoán trigger từ tên state. Với tiền, phân biệt yêu cầu, thử gọi và thành công; `catch` bỏ lỗi không được biến thành bảo đảm thành công trên hình.

## 2. Ký hiệu và phép tự kiểm

| Phần tử | Vẽ | Chặn sai |
|---|---|---|
| State thường | Chữ nhật bo góc vừa, tên căn giữa | Không bắt buộc stadium/oval; Loading hợp lệ nếu mô hình UI có nguồn |
| Initial | Chấm đen, một cạnh ra | Không cạnh vào; khởi tạo mặc định không trigger/guard, effect tùy chọn |
| FinalState | Vòng ngoài và chấm đen trong | Không cạnh ra; **không dùng chữ nhật viền đôi** |
| State tên Hoàn tất | Vẫn là state thường nếu còn chuyển ra hợp lệ | Không suy final từ tên hoặc `status=completed` |
| Transition | Mũi tên một chiều chạm biên | `event [guard] / effect`; slash phân cách effect, không nghĩa “hoặc” |
| Composite | State bo góc chứa state con thật | Exit chung chỉ khi event/guard/effect áp dụng cho **mọi** state con liên quan, xét ưu tiên cạnh nội bộ |

FinalState chỉ thêm khi region thực sự hoàn thành; không bắt buộc cho vòng đời mở. Initial/completion edge có thể không nhãn: không bịa event chỉ để mọi cạnh có chữ. Nhiều trigger cùng hành vi có thể dùng danh sách trigger. Kiểm xung đột guard của các cạnh cùng xử lý một event, không ép guard của hai event khác nhau thành phủ định. Chủ đích nondeterminism/priority phải giải thích ngoài ảnh.

## 3. Công thức bố cục cho agent ít kinh nghiệm

1. Nháp **chỉ state và spine chính**, chọn trái→phải hoặc trên→dưới. Không áp mẫu Login hai hàng vào mọi domain.
2. Liệt kê nhánh rẽ và đích chung. Đặt đích gần các nguồn; gom composite chỉ sau khi chứng minh mục §2, không gom để che cạnh thiếu.
3. Đặt ngoại lệ bên đoạn phát sinh, không dồn hết góc dưới phải. Chừa hành lang nhãn ngay lúc đặt node.
4. Nối spine, nhánh, rồi final. Mỗi cạnh có ID, anchor, waypoint, vùng nhãn tường minh. Dây chạy vòng mép toàn canvas → đổi node/nhóm/phân rã.
5. Nhãn sát đoạn dễ gán đúng cạnh, thường cách nét 12–30 px ở kích thước thiết kế. Xa hơn phải kiểm mắt. Nhãn dài: rút đúng nghĩa hoặc xuống dòng. **Không dùng rect trắng che viền state/đầu mũi tên để chữa đè**.
6. State cùng loại có kích thước nhất quán, padding chữ ≥12 px. Render Chromium để giữ dấu. Tính `pt = font_px × insert_width_cm / canvas_width_px × 72 / 2.54`. Dưới 9pt thì tăng chữ/phân rã/chọn trang ngang; tăng DPI không cứu chữ nhỏ.
7. So sánh flat và composite hoặc đổi chiều spine theo số giao cắt, cạnh quay xa, vùng nhãn. Chọn phương án đơn giản có bằng chứng, không render biến thể chỉ đổi khoảng cách.

## 4. Bộ kiểm trước render

Chạy `python scripts/render_state_model.py <model.json> --check-only`; thêm `--out <stem>` để xuất SVG + drawio. **Script không tự xếp layout.** Tọa độ do agent quyết định theo §3.

Phạm vi bộ xuất hiện tại: state, initial/final tròn và composite với exit chung; không hỗ trợ history/choice/fork/orthogonal regions/internal transition. Với các cấu trúc đó, dùng nguồn drawio/SVG tay riêng và kiểm ngữ nghĩa thủ công. Đích của cạnh phải là child cụ thể; bộ kiểm từ chối đích composite thay vì suy sai rằng mọi child cùng được vào.

Model: `view,width,height,nodes,edges,expected_pairs`. Node có `id,kind,label,x,y,w,h,evidence,parent?`; edge có `id,source,target,points,label,label_at,trigger?,guard?,completion?,evidence,shared_exit_verified?`. Chọn điểm đầu/cuối trên biên. `expected_pairs` lấy độc lập từ nguồn, không chép ngược từ hình để test luôn xanh.

Script chặn ID trùng, cạnh ra final, cạnh vào initial, trigger/guard ở initial, nguồn thiếu, chú thích top-level, tọa độ không hữu hạn/ngoài canvas, cây parent vòng lặp hoặc child ngoài composite, đoạn tuyến không trực giao/độ dài 0, thiếu/thừa cạnh sau **mở rộng composite**. Validation dùng ValueError nên vẫn hoạt động với Python `-O`. Nó không chứng minh evidence thật, không phát hiện mọi che nét, không xác nhận hình đẹp. Nhãn ngắn trên ảnh phải khớp ý nghĩa trigger đầy đủ trong model.

## 5. Nghiệm thu

1. Kiểm nguồn/UML, reachability theo phạm vi; đếm cạnh **sau mở rộng composite**, không chỉ số mũi tên.
2. SVG/PNG + drawio/model dùng cùng ID, tọa độ, anchor, nhãn. Khóa `exitPerimeter=0;entryPerimeter=0` nếu đã tính điểm biên. Chưa render drawio trong editor thì không khẳng định hai ảnh giống nhau tuyệt đối.
3. Mở PNG Chromium; chạy `eye_audit.py --overlay --dump`, đối chiếu parser. Parser có thể nhầm viền composite thành connector và bỏ initial/final: ghi sai số. Mở overlay và **mọi crop**, ghi verdict từng ứng viên. Crop có font fallback phải so lại pixel Chromium cùng vùng.
4. Kiểm mọi text: chỉ state/composite/region, transition hoặc hành vi UML hợp lệ. Có câu thuyết minh khác = FAIL, kể cả footer không có hộp. Kiểm mất viền vì nền nhãn trắng.
5. Tách kết quả nguồn/UML, render, tự động, mắt soi, Word/slide. NOT RUN nếu chưa làm. Không tạo lần sửa vô nghĩa nếu bản đầu đạt; sau mỗi sửa thật phải render và soi lại.

## 6. Bài kiểm chống tái phạm

- Completed còn cạnh tới Returned → vẫn là state thường.
- Có note/footer dù nội dung đúng → từ chối xuất, giữ nguồn ở ngoài ảnh.
- Ma trận A→C nhưng service A→B → báo lệch declared/as-is, không hợp nhất thành “đã triển khai”.
- Ba state chia cancel → một cạnh composite chỉ khi điều kiện/hành vi chung thật; mở rộng phải ra ba cặp nguồn.
- Hai event khác nhau → không ép guard đối nhau; không ép initial/final phải có chữ.
- Nền nhãn trắng cắt viền hộp → FAIL dù script 0 lỗi.

## 7. Nguồn đã truy cập 01/11/2026

- [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1): trang đặc tả chính thức; PDF lớn không tải được trong web tool phiên này, không giả nhận đã đọc toàn bộ.
- [Quantum Leaps — A Crash Course in UML State Machines](https://www.state-machine.com/doc/AN_Crash_Course_in_UML_State_Machines.pdf), §1.2.2, §1.2.5 và §2.1: ký hiệu, guard và phân cấp hành vi.
- [Quantum Leaps — Initial transitions](https://www.state-machine.com/qm/sm_init.html): initial và effect tùy chọn.
- [Quantum Leaps — Transitions](https://www.state-machine.com/qm/sm_tran.html): cạnh chạm state, internal/self-transition; trang tự chỉ rõ ký hiệu riêng QM không chuẩn UML.
- [Sparx — Transition](https://www.sparxsystems.com/enterprise_architect_user_guide/17.2/modeling_languages/transition.html): trigger, guard, effect và danh sách trigger.

Không gán gu bố cục, số hàng hoặc ngưỡng hình học địa phương thành luật UML.
