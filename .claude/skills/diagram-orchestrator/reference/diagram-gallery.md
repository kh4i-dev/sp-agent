# Diagram Gallery — Thư Viện Tương Phản Mẫu Tốt & Mẫu Lỗi (Contrastive Gallery)

Thư viện đối chiếu thực tế giữa **Mẫu Thiết Kế Hỏng (Anti-patterns)** và **Mẫu Chuẩn Mực (Best Practices)**. Dành cho Agent học cách đánh giá thiết kế và lựa chọn giải pháp tối ưu thay vì sao chép máy móc.

---

## 1. Use Case Diagram (Sơ Đồ Ca Sử Dụng)

### ❌ Mẫu Lỗi Thường Gặp (Anti-pattern)
* **Triệu chứng:** Biến Use Case thành lưu đồ thuật toán (Flowchart); vẽ các bước bấm nút (`Nhập email`, `Bấm gửi`, `Hiển thị lỗi`) thành các hình elip Use Case riêng; dùng mũi tên nhầm giữa Actor và Use Case.
* **Mã hỏng:**
  ```plantuml
  actor User
  User -> (Nhập User/Pass) : bấm >
  (Nhập User/Pass) -> (Kiểm tra DB) : xử lý >
  (Kiểm tra DB) -> (Báo lỗi sai pass) : nếu sai >
  ```
* **Tại sao hỏng:** Vi phạm nghiêm ngặt chuẩn ISO/UML 2.x. Use Case phải đại diện cho **mục tiêu nghiệp vụ hoàn chỉnh**, không phải từng bước giao diện hay hành động kỹ thuật bên trong.

### ✅ Mẫu Chuẩn Mực (Best Practice)
* **Giải pháp:** Chỉ giữ mục tiêu nghiệp vụ trọn vẹn; dùng quan hệ kết hợp nét thẳng `--` (không mũi tên); gom bước xác thực thành `<<include>>`.
* **Mã chuẩn:**
  ```plantuml
  left to right direction
  skinparam monochrome true
  skinparam shadowing false
  actor "Khách hàng" as Customer
  rectangle "Hệ Thống Mua Sắm" {
    usecase "Đặt hàng trực tuyến" as UC_Order
    usecase "Thanh toán đơn hàng" as UC_Pay
    usecase "Xác thực OTP" as UC_OTP
  }
  Customer -- UC_Order
  UC_Order ..> UC_Pay : <<include>>
  UC_Pay ..> UC_OTP : <<include>>
  ```
* **Vì sao tốt:** Thể hiện rõ ràng phạm vi hệ thống, mục tiêu người dùng và các quan hệ phụ thuộc chuẩn mực UML.

---

## 2. Sequence Diagram (Sơ Đồ Tuần Tự)

### ❌ Mẫu Lỗi Thường Gặp (Sequence Monolith Anti-pattern)
* **Triệu chứng:** Nhồi nhét toàn bộ 15 controller, service, database và hàng chục message vào cùng 1 sơ đồ tuần tự; không có thanh kích hoạt `activate`; không có số thứ tự `autonumber`.
* **Tại sao hỏng:** Sơ đồ trở thành ma trận dây nhợ dày đặc, in ra trang A4 bị thu nhỏ đến mức không thể đọc nổi một chữ nào.

### ✅ Mẫu Chuẩn Mực (Best Practice)
* **Giải pháp:** Phân rã thành từng Use Case trọng điểm (4–6 lifelines, 8–12 bước tương tác); có `autonumber`, `activate/deactivate` và khối `alt/else` xử lý ngoại lệ rõ ràng.
* **Mã chuẩn:**
  ```plantuml
  skinparam monochrome true
  skinparam shadowing false
  autonumber
  actor "Người dùng" as User
  participant "Giao diện Web" as UI
  participant "Auth Service" as Auth
  database "PostgreSQL" as DB

  User -> UI : Gửi thông tin đăng nhập
  activate UI
  UI -> Auth : POST /api/auth/login
  activate Auth
  Auth -> DB : Tìm người dùng theo email
  activate DB
  DB --> Auth : Trả về thông tin + Hash mật khẩu
  deactivate DB
  alt Mật khẩu chính xác
    Auth --> UI : 200 OK + JWT Token
    UI --> User : Điều hướng vào trang chủ
  else Mật khẩu không khớp
    Auth --> UI : 401 Unauthorized
    UI --> User : Báo lỗi "Sai mật khẩu"
  end
  deactivate Auth
  deactivate UI
  ```
* **Vì sao tốt:** Lifeline rõ ràng, quản lý vòng đời kích hoạt chuẩn xác, vừa vặn trọn vẹn nửa trang in A4.

---

## 3. ERD — Sơ Đồ Thực Thể Quan Hệ

### ❌ Mẫu Lỗi Thường Gặp (Anti-pattern)
* **Triệu chứng:** Viết nhãn động từ (`: "sở hữu"`, `: "đặt hàng"`) đè thẳng lên đường nối Crow's foot; vẽ quan hệ 2 chiều lặp lại giữa cùng 2 bảng; đưa hàm xử lý (`search()`, `login()`) vào bảng DB.
* **Tại sao hỏng:** Ký hiệu Crow's foot vốn đã biểu diễn đầy đủ bản số (`1`, `N`, `0..1`). Nhồi thêm nhãn chữ làm Graphviz chém ngang mặt chữ, gây lỗi va chạm nhãn nghiêm trọng.

### ✅ Mẫu Chuẩn Mực (Best Practice)
* **Giải pháp:** Sử dụng chuẩn Crow's foot thuần túy; khóa chính PK và khóa ngoại FK rõ ràng; không viết chữ lên dây nối; gộp thuộc tính danh mục vào mảng nếu là sơ đồ khái niệm.
* **Mã chuẩn:**
  ```plantuml
  skinparam monochrome true
  skinparam shadowing false
  skinparam linetype ortho
  left to right direction

  entity "USERS" as USERS {
    * id : UUID <<PK>>
    --
    * full_name : VARCHAR(100)
    * email : VARCHAR(100) <<UK>>
  }

  entity "ORDERS" as ORDERS {
    * id : UUID <<PK>>
    --
    * user_id : UUID <<FK>>
    * total_amount : DECIMAL(12,2)
    * status : VARCHAR(20)
  }

  USERS ||--o{ ORDERS
  ```
* **Vì sao tốt:** Đường nối thẳng góc, không có nhãn đè rác mắt, chuẩn mực như sách giáo trình CSDL.

---

## 4. Cấu Trúc Dữ Liệu Bộ Nhớ (Prefix Trie & BK-Tree trong Graphviz)

### ❌ Mẫu Lỗi Thường Gặp (Anti-pattern)
* **Triệu chứng:** Dùng PlantUML để vẽ cây Trie khiến các node bị biến thành hình hộp chữ nhật xấu xí; hoặc trong Graphviz dồn toàn bộ các nhánh sang một bên làm trống nửa trang giấy còn lại; tự bịa số khoảng cách Levenshtein sai toán học.
* **Tại sao hỏng:** Cấu trúc thuật toán cây đòi hỏi biểu diễn nút-cạnh tự nhiên và tính chính xác tuyệt đối của trọng số toán học.

### ✅ Mẫu Chuẩn Mực (Best Practice)
* **Giải pháp:** Dùng Graphviz DOT (`rankdir=TB`); node tròn/elip gọn gàng; phân nhánh tỏa đều cân đối; khoảng cách Levenshtein được tính toán chính xác 100%.
* **Mã chuẩn (BK-Tree chuẩn toán học cho tập từ: `book`, `books`, `boo`, `cake`):**
  ```dot
  digraph BKTree {
    dpi=300;
    rankdir=TB;
    bgcolor="#ffffff";
    node [fontname="Segoe UI, Arial, sans-serif", fontsize=11, shape=ellipse, style=solid, color="#000000", fontcolor="#000000"];
    edge [fontname="Segoe UI, Arial, sans-serif", fontsize=10, color="#000000", fontcolor="#000000"];

    root [label="book\n(Root)", penwidth=1.5];
    n_books [label="books"];
    n_boo   [label="boo"];
    n_cake  [label="cake"];

    root -> n_books [label=" d=1 "];
    root -> n_cake  [label=" d=4 "];
    n_books -> n_boo [label=" d=2 "];
  }
  ```
* **Vì sao tốt:** Trọng số `d` chuẩn xác (Levenshtein giữa `book` và `books` là 1; giữa `book` và `cake` là 4; giữa `books` và `boo` là 2). Cây tỏa đều, khoảng trắng cân xứng.
