# Cẩm nang Giọng văn Thực chiến & Nhịp điệu (Voice & Cadence)

Tài liệu hướng dẫn chuyên sâu cho skill `human-report-writing`.
Đọc khi cần viết hoặc biên tập văn xuôi báo cáo, tài liệu kỹ thuật, đồ án tốt nghiệp sao cho **sắc sảo, tự nhiên, mang hơi thở của người kỹ sư thực chiến**, không còn cảm giác "văn AI" và "khô cứng kiểu hành chính".

---

## 1. Bản chất vì sao văn AI đọc bị "Cứng" và "Mất hồn"

Văn AI thường rơi vào hai thái cực:
1. **Thái cực sáo rỗng (AI Slop):** Dùng tràn lan tính từ hoa mỹ, từ ngữ phóng đại ("tối ưu hóa", "toàn diện", "đóng vai trò then chốt", "nâng cao trải nghiệm").
2. **Thái cực khô cứng (Sterile Bureaucracy):** Khi bị cấm dùng từ sáo rỗng và cấm định dạng (bold, em dash, bullets), AI rút vào vùng an toàn tuyệt đối và viết như **công văn hành chính hoặc sách giáo khoa lý thuyết**. Câu nào cũng bị động, đều chằn chặn, vô cảm, thiếu hoàn toàn "hơi thở thực tế".

Văn người kỹ sư thật viết **không khô cứng như hành chính**, nhưng cũng **không hoa mỹ như marketing**. Đó là thứ văn **chắc nịch, cụ thể, quyết đoán và có nhịp thở**.

---

## 2. Bốn trụ cột của Văn phong Kỹ sư Thực chiến (Practitioner Voice)

### Trụ cột 1: Đưa ra Sự đánh đổi (Trade-offs & Rationale)
AI luôn khen giải pháp của mình là hoàn hảo. Kỹ sư thật hiểu rằng **mọi quyết định kỹ thuật đều là một sự đánh đổi**.
- *Văn AI:* "Hệ thống sử dụng cơ sở dữ liệu quan hệ PostgreSQL nhằm đảm bảo tính toàn vẹn dữ liệu và tối ưu hóa hiệu năng truy vấn cho toàn bộ ứng dụng."
- *Văn kỹ sư:* "Hệ thống chọn PostgreSQL thay vì MongoDB để tận dụng giao dịch ACID cho luồng thanh toán ký quỹ. Điểm đánh đổi là việc mở rộng bảng dữ liệu khi lượng log tăng đột biến sẽ phức tạp hơn, đòi hỏi phải phân vùng bảng (table partitioning) theo tháng."

### Trụ cột 2: Nêu rõ Trở ngại thực tế (Friction & Edge Cases)
Tài liệu của người làm thật luôn phảng phất những góc khuất, khó khăn và cách xử lý trong quá trình triển khai, chứ không chỉ kể lể tính năng xuôi chèo mát mái.
- *Văn AI:* "Hệ thống tích hợp cổng thanh toán một cách an toàn và xử lý các giao dịch một cách hiệu quả."
- *Văn kỹ sư:* "Trong quá trình tích hợp, khó khăn lớn nhất là độ trễ phản hồi từ webhook của cổng thanh toán (trung bình 2–4 giây). Nếu client gửi request liên tục trong khoảng này, hệ thống rất dễ gặp lỗi ghi đè dữ liệu. Do đó, cơ chế khóa lạc quan (optimistic lock) với trường version được áp dụng cho từng bản ghi đơn hàng."

### Trụ cột 3: Đo lường bằng Cơ chế và Dữ kiện (Mechanisms over Adjectives)
Bỏ toàn bộ các tính từ mơ hồ ("nhanh", "mạnh", "an toàn", "tiên tiến"). Thay bằng cơ chế hoạt động cụ thể.
- *Văn AI:* "Hệ thống áp dụng thuật toán mã hóa tiên tiến để đảm bảo an toàn tuyệt đối cho mật khẩu người dùng."
- *Văn kỹ sư:* "Mật khẩu người dùng được băm bằng bcrypt với salt round bằng 10 trước khi lưu vào bảng `users`. Token xác thực JWT có thời hạn 15 phút, lưu tại bộ nhớ tạm (in-memory) của client để hạn chế nguy cơ tấn công XSS."

### Trụ cột 4: Cắt bỏ "Rác giáo trình" (Cut the Textbook Fluff)
Người đọc báo cáo/đồ án là thầy cô hoặc đồng nghiệp. Họ đã biết React, Docker hay RESTful là gì. Đừng viết 3 đoạn định nghĩa giáo trình vỡ lòng rồi mới vào việc.
- *Văn AI:* "Docker là một nền tảng mã nguồn mở giúp tự động hóa việc triển khai ứng dụng bên trong các container phần mềm nhẹ..."
- *Văn kỹ sư:* "Toàn bộ backend gồm 3 dịch vụ được đóng gói thành Docker image riêng biệt. Cấu hình đa tầng (multi-stage build) giúp rút gọn kích thước image từ 1.2 GB xuống còn 145 MB, giảm thời gian kéo image khi triển khai tự động."

---

## 3. Quy luật Nhịp điệu câu (Sentence Cadence & Burstiness)

Điểm dễ nhận biết nhất của văn máy là **mọi câu đều dài bằng nhau** (trung bình 18–25 từ/câu). Đọc một trang có 10 câu dài bằng nhau sẽ khiến não bộ mệt mỏi và cảm thấy cứng đờ.

Người viết tự nhiên tạo ra **nhịp thở đa dạng**:
1. **Câu ngắn (4–8 từ):** Đanh thép, xác lập quan điểm hoặc chốt hạ luận điểm.
2. **Câu trung bình (12–20 từ):** Diễn giải mối quan hệ nguyên nhân – kết quả.
3. **Câu phức (25–35 từ):** Phân tích luồng kỹ thuật hoặc logic chi tiết.

### Ví dụ về Nhịp thở:
> "Cơ chế đồng bộ trực tiếp đã thất bại. Khi mạng chập chờn, client liên tục gửi lại yêu cầu khiến hàng đợi của máy chủ quá tải trong vòng chưa đầy hai phút. Để giải quyết, nhóm chuyển toàn bộ tác vụ xử lý ảnh sang cơ chế bất đồng bộ qua hàng đợi Redis BullMQ. Máy chủ chỉ nhận file, cấp mã theo dõi rồi trả về ngay cho client. Độ trễ phản hồi ban đầu giảm từ 3,8 giây xuống 120 mili-giây."

*Phân tích nhịp:*
- Câu 1: 8 từ (ngắn, đanh thép, nêu thất bại thực tế).
- Câu 2: 24 từ (trung bình-dài, mô tả cơ chế gây lỗi).
- Câu 3: 20 từ (trung bình, nêu quyết định giải pháp).
- Câu 4: 16 từ (trung bình, giải thích cách hoạt động).
- Câu 5: 14 từ (chốt con số đo lường cụ thể).

---

## 4. Danh sách Đen từ vựng sáo rỗng (Fluff Blacklist)

Khi viết tài liệu kỹ thuật, **cấm tiệt** các cụm từ sau:

| Cụm từ AI sáo rỗng | Vấn đề | Thay thế bằng gì |
|---|---|---|
| "đóng vai trò quan trọng/then chốt" | Sáo rỗng, không có thông tin | Nêu thẳng chức năng: "chịu trách nhiệm...", "quản lý..." |
| "nhằm tối ưu hóa quy trình" | Từ ngữ che đậy sự thiếu hiểu biết | Nêu rõ tối ưu cái gì: "giảm thời gian truy vấn...", "giảm thao tác click..." |
| "mang tính toàn diện và linh hoạt" | Khen ngợi vô căn cứ | Bỏ hẳn, hoặc nêu rõ các trường hợp hỗ trợ |
| "hệ sinh thái phong phú" | Nghe như quảng cáo | "thư viện bên thứ ba", "các module phụ trợ" |
| "trong bối cảnh ngày càng phát triển" | Mở đầu lười biếng, thừa thãi | Vào thẳng vấn đề và số liệu thực tế |
| "giải pháp tối ưu" | Tự mãn vô bằng chứng | "giải pháp phù hợp với tài nguyên hiện tại" |
| "giúp nâng cao trải nghiệm người dùng" | Khẩu hiệu rỗng | "giảm thời gian chờ tải trang", "hạn chế nhập liệu trùng" |
| "không chỉ... mà còn..." | Khuôn mẫu giả tạo sự phong phú | Tách thành hai câu độc lập với dữ kiện rõ ràng |
| "có thể thấy rằng...", "rõ ràng là..." | Ép buộc người đọc đồng ý | Bỏ hẳn, đưa số liệu để tự người đọc thấy |

---

## 5. Nghệ thuật Móc xích Logic (Thay vì dùng từ nối cơ học)

AI phụ thuộc vào các từ nối đóng khuôn ở đầu câu: *Bên cạnh đó, Ngoài ra, Hơn nữa, Đồng thời, Mặt khác*.

Người viết tự nhiên liên kết bằng **mạch logic nội tại**:
- **Liên kết bằng hệ quả:** Dùng nội dung cuối câu trước làm bàn đạp cho câu sau.
- **Liên kết bằng đối lập thực tế:** "Tuy vậy,", "Trên thực tế,", "Trái lại,".
- **Liên kết bằng phương án thay thế:** "Thay vì..., giải pháp ở đây là...", "Để khắc phục điều này,...".

---

## 6. Phá bỏ Khuôn mẫu Đoạn văn 3 thì (Formulaic Triad)

Tránh viết mọi tiểu mục theo mô thức:
`[Câu 1: Giới thiệu chung] -> [Câu 2: Liệt kê chức năng] -> [Câu 3: Kết luận nâng tầm]`.

Hãy linh hoạt mở đầu đoạn văn theo các cách khác nhau:
- **Mở đầu bằng bài toán/yêu cầu nghiệp vụ:** "Quy định sàn yêu cầu tiền hàng chỉ được giải ngân sau khi người mua xác nhận đã nhận đúng kiện hàng hoặc sau 7 ngày không có khiếu nại."
- **Mở đầu bằng kiến trúc dữ liệu:** "Bảng `orders` giữ hai trạng thái độc lập: trạng thái vận chuyển (`shipping_status`) và trạng thái dòng tiền (`payment_status`)."
- **Mở đầu bằng luồng tương tác:** "Khi người dùng ấn thanh toán, client không gọi trực tiếp API ngân hàng mà gửi yêu cầu tạo phiên giao dịch tới backend."
