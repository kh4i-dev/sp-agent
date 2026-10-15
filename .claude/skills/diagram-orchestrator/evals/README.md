# Diagram Evals — Bộ Bài Kiểm Thử Cố Định Đánh Giá Chất Lượng Sơ Đồ

Bộ kiểm thử chuẩn (Benchmark Suite) dùng để đánh giá độc lập xem sau mỗi lần tinh chỉnh skill, chất lượng sơ đồ của Agent có thực sự tiến bộ hay không.

---

## Danh Sách 5 Bài Kiểm Thử Cố Định (Fixed Litmus Evals)

| Mã bài test | Tên bài kiểm tra | Thách thức kỹ thuật đặt ra | Tiêu chuẩn ĐẠT (PASS) |
|---|---|---|---|
| **EVAL-01** | `01_long_labels` | Nhãn cạnh dài cắt qua ranh giới package/cluster trong Graphviz. | Không bị đường viền cluster chém ngang chữ; nhãn thoáng đạt rõ ràng. |
| **EVAL-02** | `02_nested_packages` | Kiến trúc 3 tầng lồng nhau (Presentation -> Application -> Infrastructure). | Không có quan hệ nhảy cóc tầng, không đè hộp, bo góc chuẩn mực. |
| **EVAL-03** | `03_crowded_erd` | ERD 8+ bảng có quan hệ phức tạp. | Không có nhãn đè lên đường Crow's foot, không trùng lặp đường nối 2 chiều. |
| **EVAL-04** | `04_balanced_trie` | Cây tiền tố Prefix Trie và BK-Tree. | Phân nhánh tỏa đều hai bên, không dồn cục khoảng trắng, đúng trọng số Levenshtein. |
| **EVAL-05** | `05_sequence_a4` | Sơ đồ tuần tự đầy đủ 5 lifelines và nhánh alt/else. | Vừa vặn trang in A4 (chiều ngang không quá dài), có `autonumber` và `activate`. |
| **EVAL-06** | `06_class_rutgon_hub` | Class Diagram có hub User, association khác vai trò, nhiều hidden constraints và comment đếm lớp sai có chủ ý. | Auditor cảnh báo hub/parallel associations/hidden constraints/source count mismatch; warning không tự động bị coi là visual failure. |
| **EVAL-07** | `07_use_case_multi_actor` | Use Case có 4 actor, 18 use case, 3 package và 5 hidden constraints. | Auditor cảnh báo độ phức tạp actor/use case và hidden layout constraints; mở PNG để kiểm tra routing riêng. |

---

## Cách Chạy Bộ Kiểm Thử (Test Runner)

```bash
# Chạy toàn bộ 5 bài test và báo cáo kết quả
node .claude/skills/diagram-orchestrator/scripts/run-evals.mjs
```

Script sẽ tự động:
1. Render toàn bộ các file nguồn trong `evals/` ra SVG và PNG 300 DPI.
2. Gọi `diagram-auditor` để quét lỗi đè chữ, cắt nét, thiếu file và kích thước khung hình.
3. Xuất bảng tổng kết điểm số Benchmark (100% PASS mới được coi là đạt chuẩn).


## Ranh giới bằng chứng

Runner chỉ nghiệm thu **các kiểm tra tĩnh mà script thực sự triển khai** và các cảnh báo regression mong đợi. Nó không mở/soi ảnh, không chứng minh UML đúng ngữ nghĩa, và không phát hiện đầy đủ mọi giao cắt giữa các đoạn path. Vì vậy 100% static pass không tương đương 100% thẩm mỹ; Proof-of-View và Semantic Review vẫn là gate bắt buộc.
