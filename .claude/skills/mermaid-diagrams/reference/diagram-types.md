# Mermaid — Mẫu cú pháp theo từng loại sơ đồ (reference)

## Flowchart (lưu đồ)

```mermaid
flowchart TD
    A[Khách truy cập] --> B{Đã đăng nhập?}
    B -->|Có| C[Vào Dashboard]
    B -->|Không| D[Trang đăng nhập]
    D --> C
```

## Sequence (tuần tự)

```mermaid
sequenceDiagram
    participant U as Người dùng
    participant S as Server
    participant DB as CSDL
    U->>S: POST /login
    S->>DB: SELECT user
    DB-->>S: user record
    S-->>U: 200 + token
```

## Class (lớp)

```mermaid
classDiagram
    class User {
      +int id
      +string email
      +login() bool
    }
    class Order {
      +int id
      +decimal total
      +checkout()
    }
    User "1" --> "*" Order : đặt
```

## ER (thực thể - quan hệ)

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : "ordered in"
    USER {
      int id PK
      string email
    }
```

Cardinality crow's-foot: `||--o{` (một tới nhiều tùy chọn), `||--|{` (một tới nhiều bắt buộc).

## State (trạng thái)

```mermaid
stateDiagram-v2
    [*] --> ChoDuyet
    ChoDuyet --> DaDuyet : phê duyệt
    ChoDuyet --> TuChoi : từ chối
    DaDuyet --> [*]
```

## Activity (gần đúng bằng flowchart)

Mermaid không có "activity diagram" UML riêng; dùng `flowchart` với node tròn/bổ sung:

```mermaid
flowchart TD
    Start((Bắt đầu)) --> Nhap[Nhập thông tin]
    Nhap --> KiemTra{Hợp lệ?}
    KiemTra -->|Không| Nhap
    KiemTra -->|Có| Luu[Lưu CSDL]
    Luu --> End((Kết thúc))
```

## Use Case

**Ưu tiên PlantUML** cho UML use case chuẩn:

```plantuml
@startuml
left to right direction
actor "Khách hàng" as KH
rectangle HệThống {
  usecase "Đặt hàng" as UC1
  usecase "Thanh toán" as UC2
}
KH --> UC1
KH --> UC2
@enduml
```

Mermaid có **use-case beta** (≈ v12+):

```mermaid
usecase-beta
    actor KH as "Khách hàng"
    usecase UC1 as "Đặt hàng"
    KH --> UC1
```

## C4 / Kiến trúc

```mermaid
flowchart LR
    subgraph Client
      W[Web App]
      M[Mobile App]
    end
    subgraph Backend
      API[API Gateway]
      SVC[Service]
    end
    DB[(Database)]
    W --> API
    M --> API
    API --> SVC
    SVC --> DB
```

## Gantt

```mermaid
gantt
    title Kế hoạch đồ án
    dateFormat YYYY-MM-DD
    section Phân tích
      Khảo sát       :a1, 2026-01-01, 10d
      Đặc tả         :a2, after a1, 7d
    section Thiết kế
      Thiết kế CSDL  :b1, after a2, 7d
    section Cài đặt
      Lập trình      :c1, after b1, 21d
```

## YAML frontmatter (thay cho %%{init}%% đã deprecated)

```mermaid
---
config:
  theme: neutral
  flowchart:
    curve: basis
---
flowchart LR
    A --> B
```

## Accessibility

```mermaid
flowchart TD
    accTitle: Luồng thanh toán
    accDescr: Người dùng chọn sản phẩm rồi thanh toán
    A[Chọn sản phẩm] --> B[Thanh toán]
```
