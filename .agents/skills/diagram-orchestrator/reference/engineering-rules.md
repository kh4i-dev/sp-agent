# Hướng Dẫn Kỹ Thuật Chi Tiết 16 Loại Sơ Đồ — Diagram Orchestrator

Tài liệu cẩm nang thực chiến đào sâu nguyên tắc thiết kế, bẫy thường gặp (pitfalls) và tiêu chuẩn nghiệm thu cho 16 loại sơ đồ phần mềm và thuật toán.

---

## 1. Use Case Diagram — Sơ đồ ca sử dụng
- **Mục đích:** Thể hiện tác nhân bên ngoài tương tác với hệ thống để đạt mục tiêu nghiệp vụ.
- **Công cụ:** PlantUML (`.puml`).
- **Câu hỏi cần trả lời:** Ai sử dụng hệ thống? Họ muốn hoàn thành việc gì? Phạm vi hệ thống nằm ở đâu?
- **Kinh nghiệm cốt lõi:**
  - Tên Use Case là mục tiêu nghiệp vụ: `Gửi yêu cầu kết nối`, `Tìm kiếm gia sư`, `Thanh toán gói`.
  - Actor là vai trò tương tác, không phải người cụ thể.
  - Vẽ rõ khung ranh giới hệ thống: Actor nằm ngoài, Use Case hình elip nằm trong.
  - `<<include>>`: Hành vi tách ra là phần bắt buộc phải thực hiện trong Use Case gốc.
  - `<<extend>>`: Hành vi mở rộng có điều kiện (chiều mũi tên từ nhánh mở rộng trỏ về ca gốc).
  - Không vẽ thao tác giao diện vụn vặt (nhấn nút, nhập text) thành Use Case riêng.
- **Tiêu chuẩn nghiệm thu:** Mỗi Use Case mô tả được bằng 1 luồng chính, điều kiện đầu vào và kết quả đầu ra rõ ràng.

---

## 2. Class Diagram — Sơ đồ lớp
- **Mục đích:** Thể hiện các lớp, thuộc tính, phương thức và quan hệ cấu trúc giữa chúng.
- **Công cụ:** PlantUML (`.puml`).
- **Câu hỏi cần trả lời:** Những đối tượng nào tồn tại? Chúng chịu trách nhiệm gì? Liên kết/phụ thuộc nhau ra sao?
- **Kinh nghiệm cốt lõi:**
  - Tách trách nhiệm theo vai trò (Single Responsibility Principle).
  - Chỉ ghi thuộc tính/phương thức trọng tâm trong phạm vi báo cáo; không nhồi getter/setter vụn vặt.
  - Sử dụng chính xác 5 kiểu quan hệ UML:
    - *Association (`-->`):* Liên kết giữa các đối tượng.
    - *Dependency (`..>`):* Một thành phần tạm thời sử dụng thành phần khác.
    - *Generalization (`--|>`):* Kế thừa.
    - *Composition (`*--`):* Toàn thể - bộ phận vòng đời chặt chẽ (cha chết, con chết).
    - *Aggregation (`o--`):* Toàn thể - bộ phận độc lập vòng đời.
  - Bội số bắt buộc (`1`, `0..1`, `0..*`, `1..*`).
- **Tiêu chuẩn nghiệm thu:** Xác định rõ trách nhiệm mỗi lớp và các phương thức quan trọng mà không cần phải đoán.

---

## 3. ERD — Sơ đồ thực thể & quan hệ cơ sở dữ liệu
- **Mục đích:** Thể hiện thực thể/bảng, thuộc tính, khóa và quan hệ dữ liệu lưu trữ.
- **Công cụ:** PlantUML (`.puml`) theo chuẩn Crow's foot.
- **Câu hỏi cần trả lời:** Dữ liệu nào được lưu? Định danh ra sao? Bảng nào tham chiếu bảng nào? Bội số là gì?
- **Kinh nghiệm cốt lõi:**
  - Phân biệt ERD khái niệm, logic và vật lý.
  - Khóa chính (PK), khóa ngoại (FK), khóa duy nhất (UK) phải khớp 100% với schema/migration thật.
  - Quan hệ N-N trong CSDL quan hệ bắt buộc qua bảng join trung gian.
  - Tuyệt đối KHÔNG đưa hàm xử lý (`search()`, `validate()`) vào ERD.
  - Tuyệt đối KHÔNG đưa cấu trúc RAM (Trie, BK-Tree) thành bảng CSDL chỉ vì chúng dùng để tìm kiếm!
  - CẤM viết nhãn hành động (verb) lên đường Crow's foot vì gây đè nét/cắt chữ.

---

## 4. Sequence Diagram — Sơ đồ tuần tự
- **Mục đích:** Thể hiện các participant trao đổi thông điệp theo trục thời gian.
- **Công cụ:** PlantUML (`.puml`).
- **Câu hỏi cần trả lời:** Khi hành động xảy ra, thành phần nào gọi thành phần nào theo thứ tự gì, nhánh lỗi ra sao?
- **Kinh nghiệm cốt lõi:**
  - Đọc mã nguồn thật để lấy thứ tự lời gọi. Không tự chèn service/database ảo mà hệ thống không có.
  - Tên message mang tính hành động: `searchPrefix(query)`, `createOrder()`.
  - Dùng `alt/else` cho nhánh rẽ, `opt` cho tùy chọn, `loop` cho vòng lặp.
  - Dùng participant box (`participant "PostgreSQL (Prisma)" as DB`) thay vì cylinder shape để tránh lifeline cắt chữ.
  - Phân rã thành 4-5 sơ đồ use case trọng điểm (chống Sequence Monolith).

---

## 5. Activity Diagram — Sơ đồ hoạt động
- **Mục đích:** Thể hiện trình tự hành động, điều kiện rẽ nhánh, luồng lặp và luồng song song.
- **Công cụ:** PlantUML Activity (`.puml`).
- **Câu hỏi cần trả lời:** Quy trình vận hành ra sao? Điều kiện nào làm đổi hướng xử lý?
- **Kinh nghiệm cốt lõi:**
  - Activity tập trung vào quy trình nghiệp vụ; Sequence tập trung vào trao đổi giữa các object theo thời gian.
  - Mỗi nhánh quyết định phải có điều kiện rõ ràng: `then (hợp lệ)`, `else (lỗi)`.
  - Phân biệt merge (hợp nhất lựa chọn) và join (đồng bộ song song).

---

## 6. State Machine Diagram — Sơ đồ máy trạng thái
- **Mục đích:** Mô tả các trạng thái và chuyển đổi hợp lệ trong vòng đời của một đối tượng dữ liệu.
- **Công cụ:** PlantUML State (`.puml`).
- **Câu hỏi cần trả lời:** Đối tượng có những trạng thái nào? Sự kiện nào kích hoạt chuyển đổi? Trạng thái nào là điểm kết thúc không thể đảo ngược?
- **Kinh nghiệm cốt lõi:**
  - Trạng thái là danh từ/tính từ (`PENDING`, `VERIFIED`, `REJECTED`), không phải hành động.
  - Phân biệt trạng thái nghiệp vụ đối tượng với trạng thái giao diện UI (`Loading...`).
  - Không vẽ mũi tên 2 chiều bừa bãi giữa mọi trạng thái.

---

## 7. Component Diagram — Sơ đồ thành phần
- **Mục đích:** Thể hiện các khối phần mềm lớn và sự phụ thuộc giữa chúng.
- **Công cụ:** PlantUML hoặc tldraw.
- **Kinh nghiệm cốt lõi:**
  - Component đại diện cho đơn vị kiến trúc có ranh giới rõ ràng.
  - Không biến danh sách thư viện thành component (React, Tailwind là công nghệ, không phải component).
  - Không bịa thêm message broker, microservice nếu hệ thống thực chất là monolith.

---

## 8. Deployment Diagram — Sơ đồ triển khai
- **Mục đích:** Thể hiện phần mềm chạy ở đâu, trên phần cứng/node nào, môi trường và kết nối mạng ra sao.
- **Công cụ:** PlantUML hoặc tldraw.
- **Kinh nghiệm cốt lõi:**
  - Phân biệt phần mềm với môi trường triển khai phần cứng.
  - Ghi rõ node, môi trường chạy (Docker, Nginx, Ubuntu, Port 443).
  - Nếu ứng dụng desktop chạy cục bộ, vẽ mô hình 1 máy chính xác, không tự thêm cloud server ảo.

---

## 9. DFD — Data Flow Diagram (Sơ đồ luồng dữ liệu)
- **Mục đích:** Mô tả dòng dữ liệu đi từ nguồn ngoài, qua các tiến trình xử lý, vào kho dữ liệu.
- **Kinh nghiệm cốt lõi:**
  - Tên luồng là Danh từ (dữ liệu): `Từ khóa`, `Kết quả`. Tên process là Động từ: `Chuẩn hóa`.
  - Không vẽ luồng dữ liệu trực tiếp giữa 2 thực thể ngoài hoặc giữa 2 kho dữ liệu.

---

## 10. Flowchart — Lưu đồ thuật toán
- **Mục đích:** Mô tả từng bước xử lý logic của một thuật toán cụ thể.
- **Công cụ:** Graphviz hoặc PlantUML.
- **Kinh nghiệm cốt lõi:** Ký hiệu bắt đầu/kết thúc (elip), xử lý (chữ nhật), điều kiện (hình thoi) chuẩn mực. Vòng lặp phải có điểm thoát rõ ràng.

---

## 11. Sơ đồ cấu trúc dữ liệu: Prefix Trie & BK-Tree
- **Mục đích:** Minh họa cấu trúc dữ liệu trong bộ nhớ RAM phục vụ tìm kiếm.
- **Công cụ:** **Bắt buộc dùng Graphviz DOT (`.dot`)**.
- **Kinh nghiệm cốt lõi:**
  - *Prefix Trie:* Node gốc `root`, mỗi cạnh mang 1 ký tự, node kết thúc từ đánh dấu `doublecircle`.
  - *BK-Tree:* Mỗi node là 1 từ, nhãn cạnh là khoảng cách Levenshtein chính xác 100% về mặt toán học. Tuyệt đối không bịa khoảng cách sai lệch chỉ để cân đối hình cây.

---

## 12. System Context Diagram — Sơ đồ ngữ cảnh hệ thống
- **Mục đích:** Xác định ranh giới hệ thống với môi trường ngoài (người dùng, hệ thống tích hợp bên thứ ba).
- **Vị trí:** Đặt ở đầu chương phân tích hệ thống.

---

## 13. Package Diagram — Sơ đồ gói
- **Mục đích:** Giải thích cách tổ chức mã nguồn thành các module/thư mục và phụ thuộc giữa chúng.

---

## 14. Object Diagram — Sơ đồ đối tượng
- **Mục đích:** Ảnh chụp (Snapshot) các instance cụ thể tại một thời điểm runtime với giá trị cụ thể.

---

## 15. Communication Diagram — Sơ đồ giao tiếp
- **Mục đích:** Tương tác đối tượng nhấn mạnh cấu trúc liên kết mạng lưới thay vì trục thời gian tuyến tính.

---

## 16. BPMN — Mô hình quy trình nghiệp vụ
- **Mục đích:** Mô tả quy trình nghiệp vụ đa phòng ban/tác nhân theo chuẩn BPMN (Pool, Lane, Gateway, Event, Task).
