---
name: human-report-writing
description: Viết và biên tập văn xuôi báo cáo/đồ án theo văn phong tự nhiên như người viết, loại bỏ dấu hiệu văn do AI/máy sinh (câu rào đón, lặp khuôn, bullet tràn lan, câu "hướng dẫn nội bộ", văn sáo rỗng vô cảm, hành chính khô cứng). Use when writing or editing report prose, khi bản thảo "nghe như AI/đọc đỡ máy", hoặc khi người dùng yêu cầu "viết như human", "tự nhiên hơn", "đỡ giống máy", "đổi văn phong", "bớt cứng".
---

# Human Report Writing — Văn phong báo cáo tự nhiên & Sắc bén

Mục tiêu: bản thảo đọc như một kỹ sư/nhà nghiên cứu thực tế viết — **sắc sảo, cụ thể, có chiều sâu chuyên môn và nhịp điệu tự nhiên**, hoàn toàn loại bỏ dấu hiệu văn do AI sinh (cả sự sáo rỗng lẫn sự khô cứng kiểu hành chính).

---

## 1. Khi nào dùng

- Viết hoặc biên tập phần văn xuôi của báo cáo, đồ án môn học, khóa luận, luận văn.
- Bản thảo mắc **văn AI sáo rỗng**: từ ngữ phóng đại, rào đón, bullet tràn lan, câu hướng dẫn nội bộ.
- Bản thảo mắc **văn AI khô cứng (Sterile Bureaucracy)**: câu cú đều chằn chặn, liệt kê vô hồn như công văn, thiếu hơi thở của người trực tiếp làm kỹ thuật.
- Người dùng yêu cầu: "viết như human", "tự nhiên hơn", "đỡ máy", "đổi văn phong", "bớt cứng".

---

## 2. Ba căn bệnh cần tránh (Failure Modes)

1. **AI sáo rỗng (AI Slop):** Lạm dụng tính từ hoa mỹ, tâng bốc tính năng ("tối ưu hóa", "toàn diện", "đóng vai trò then chốt", "tiên tiến", "nâng cao trải nghiệm").
2. **Khô cứng hành chính (Sterile Bureaucracy):** Khi bị cấm hoa mỹ, agent rút vào vùng an toàn tuyệt đối và viết như robot vô hồn: câu nào cũng bị động ("được thực hiện bởi"), nhịp điệu phẳng lì, không có nhận định kỹ thuật.
3. **Quá thân mật / khẩu ngữ (Tech-blog Casual):** Viết như blog cá nhân: "mình", "nhóm mình thử", "nó chạy cực nhanh", "ok", câu cảm thán, tiếng lóng. Tự nhiên nhưng **thiếu nghiêm túc** — không hợp báo cáo/đồ án.

> **Tiêu chuẩn vàng:** Văn phong **nghiêm túc nhưng tự nhiên** — khách quan, dứt khoát, lập luận dựa trên cơ chế và số liệu; câu chữ có nhịp thở, không sáo rỗng, không khô cứng, không xuồng xã.

---

## 3. Bốn trụ cột của Giọng văn Kỹ sư Thực chiến (Practitioner Voice)

### Trụ cột 1: Đưa ra Sự đánh đổi (Trade-offs & Rationale)
Mọi quyết định kỹ thuật đều có giá phải trả. Thay vì chỉ khen giải pháp, hãy nêu lý do chọn A thay vì B và cái giá chấp nhận đánh đổi.
- *AI sáo rỗng:* "Hệ thống sử dụng cơ sở dữ liệu quan hệ PostgreSQL nhằm đảm bảo tính toàn vẹn dữ liệu và tối ưu hóa hiệu năng truy vấn."
- *Kỹ sư thực tế:* "Hệ thống chọn PostgreSQL thay vì MongoDB để tận dụng giao dịch ACID cho luồng thanh toán ký quỹ, dù việc mở rộng bảng dữ liệu lịch sử sau này sẽ tốn chi phí phân vùng hơn."

### Trụ cột 2: Nêu rõ Trở ngại thực tế (Friction & Edge Cases)
Tài liệu của người làm thật luôn phản ánh bài toán thực nghiệm, góc khuất và cách xử lý lỗi, không phải bức tranh màu hồng.
- *AI sáo rỗng:* "Hệ thống tích hợp cổng thanh toán an toàn và xử lý giao dịch linh hoạt."
- *Kỹ sư thực tế:* "Trong thử nghiệm, webhook từ cổng thanh toán có độ trễ 2–4 giây. Để tránh race condition khi người dùng nhấn thanh toán liên tục, hệ thống áp dụng khóa lạc quan (optimistic lock) với trường version trên từng bản ghi đơn hàng."

### Trụ cột 3: Đo lường bằng Cơ chế thay vì Tính từ (Mechanisms over Adjectives)
Loại bỏ tính từ chung chung ("nhanh", "mạnh", "an toàn"). Thay bằng tham số cấu hình, giải thuật, tên bảng, cơ chế hoạt động.
- *AI sáo rỗng:* "Hệ thống bảo mật mật khẩu bằng thuật toán mã hóa tiên tiến."
- *Kỹ sư thực tế:* "Mật khẩu người dùng được băm bằng bcrypt với salt round bằng 10. Token xác thực JWT có thời hạn 15 phút, lưu tại bộ nhớ tạm in-memory để hạn chế nguy cơ tấn công XSS."

### Trụ cột 4: Cắt bỏ "Rác giáo trình" (Cut the Textbook Fluff)
Người đọc báo cáo (thầy cô, hội đồng, đồng nghiệp) đã biết Docker, React, RESTful là gì. Đừng chép lại định nghĩa giáo trình vỡ lòng; tập trung vào *ngữ cảnh áp dụng cụ thể trong dự án*.
- *AI sáo rỗng:* "Docker là nền tảng mã nguồn mở giúp đóng gói ứng dụng vào các container nhẹ..."
- *Kỹ sư thực tế:* "Toàn bộ backend gồm 3 dịch vụ được đóng gói thành Docker image độc lập. Cấu hình đa tầng (multi-stage build) giúp rút gọn image từ 1.2 GB xuống còn 145 MB, giảm thời gian kéo image khi deploy tự động."

---

## 4. Giọng điệu Trang trọng Vừa phải & Kiểm soát Thuật ngữ

Viết tự nhiên **không** đồng nghĩa với xuồng xã hay nhồi thuật ngữ. Giữ cân bằng ở giữa.

### A. Mức trang trọng (Register)
- Khách quan, dứt khoát; **không cảm thán, không tiếng lóng, không teencode**.
- Ngôi kể **nhất quán**: ngôi 3 khách quan ("hệ thống được thiết kế...") hoặc "chúng tôi/em" — chọn một, không trộn.
- Mỗi nhận định có căn cứ; tránh "chắc là", "có lẽ", "hình như".
- Câu dài ngắn đan xen vẫn giữ được vẻ nghiêm túc (nhịp thở khác với khẩu ngữ).

### B. Kiểm soát thuật ngữ ngành (Jargon)
- Chỉ dùng khi cần chính xác; ưu tiên từ ngữ nghiệp vụ dễ hiểu.
- Lần đầu xuất hiện: viết đầy đủ + viết tắt trong ngoặc; các lần sau dùng viết tắt.
- **Không chồng nhiều thuật ngữ trong một câu** (tối đa 1–2 thuật ngữ mới/câu).
- Thuật ngữ dễ gây khó → giải nghĩa ngắn bằng tiếng Việt phổ thông.
- Không dùng thuật ngữ để "khoe"; xen câu diễn đạt thường để giữ mật độ vừa phải.

### C. Ví dụ hiệu chỉnh
| Quá thân mật (blog) | Nghiêm túc nhưng tự nhiên |
|---|---|
| "Nhóm mình thử Redis, nó chạy cực nhanh." | "Nhóm thử nghiệm lớp đệm Redis; thời gian phản hồi giảm rõ rệt." |
| "Cái module auth làm ngon lành." | "Module xác thực đáp ứng đầy đủ yêu cầu phân quyền." |
| "Docker hơi khó cài lúc đầu, sau thì ổn." | "Việc thiết lập Docker ban đầu gặp một số trở ngại, sau đó đã ổn định." |
| "Không thể tin nổi là nhanh vậy!" | (bỏ — không dùng cảm thán trong báo cáo) |

> Chi tiết đầy đủ + mật độ cân bằng: `reference/register-and-jargon.md`.

---

## 5. Quy luật Nhịp điệu câu (Cadence & Burstiness)

Dấu hiệu nhận biết máy móc rõ nhất là **mọi câu đều dài bằng nhau** (18–25 từ/câu). Đọc liên tiếp sẽ tạo cảm giác ru ngủ và cứng đờ.

Hãy chủ động đan xen nhịp thở:
- **Câu ngắn (4–8 từ):** Đanh thép, xác lập quan điểm hoặc chốt luận điểm then chốt.
- **Câu trung bình (12–20 từ):** Diễn giải mối quan hệ nhân quả hoặc giải pháp kỹ thuật.
- **Câu phức (25–35 từ):** Phân tích luồng nghiệp vụ hoặc cơ chế dữ liệu phức tạp.

> *Ví dụ:* "Đồng bộ trực tiếp đã thất bại. Khi mạng chập chờn, client liên tục gửi lại yêu cầu khiến hàng đợi của máy chủ quá tải trong vòng chưa đầy hai phút. Nhóm chuyển toàn bộ tác vụ xử lý sang cơ chế bất đồng bộ với hàng đợi Redis. Máy chủ chỉ nhận việc, cấp mã theo dõi rồi phản hồi ngay cho client. Độ trễ phản hồi ban đầu giảm từ 3,8 giây xuống 120 mili-giây."

---

## 6. Cấm tuyệt đối (Định dạng & Lập luận — Bất biến)

### A. Về định dạng
- **Không in đậm / bôi đậm chữ (bold) trong thân bài.** Nhấn ý bằng cấu trúc câu và từ ngữ, không dùng nét chữ. Ngoại lệ: Tiêu đề chương/mục theo Heading style.
- **Không dùng dấu gạch dài em dash (—).** Dùng dấu phẩy, dấu chấm, hoặc tách câu. (Gạch nối "-" trong từ ghép hoặc gạch đầu dòng dùng bình thường).
- **Không tô nền / highlight màu (đặc biệt nền vàng).**
- **Không bullet tràn lan.** Ưu tiên đoạn văn xuôi; chỉ dùng bullet khi liệt kê thật sự (danh mục thông số, các bước tuần tự).

### B. Về lập luận & từ vựng (Fluff Blacklist)
Cấm tiệt các từ/cụm từ sáo rỗng sau:
- "đóng vai trò quan trọng / then chốt" → *thay bằng chức năng cụ thể*.
- "nhằm tối ưu hóa quy trình" → *nêu rõ tối ưu cái gì (giảm bao nhiêu ms, bớt bao nhiêu bước)*.
- "mang tính toàn diện và linh hoạt" → *bỏ hẳn*.
- "hệ sinh thái phong phú" → *thay bằng "thư viện bên thứ ba", "module hỗ trợ"*.
- "trong bối cảnh ngày càng phát triển" → *bỏ hẳn, vào thẳng vấn đề*.
- "giúp nâng cao trải nghiệm người dùng" → *nêu hành vi cụ thể (giảm thao tác click, tải trang nhanh)*.
- "không chỉ... mà còn..." (dùng liên tục) → *tách thành hai câu độc lập với dữ kiện rõ ràng*.
- "câu hướng dẫn nội bộ" ("trước khi nộp cần đối chiếu...", "khi nộp bài cần...") → *xóa hoặc biến thành câu khẳng định*.

---

## 7. Móc xích Logic & Phá bỏ Khuôn mẫu 3 thì

### Tránh lạm dụng liên từ cơ học
Không mở đầu mọi câu/đoạn bằng: *Bên cạnh đó, Ngoài ra, Hơn nữa, Đồng thời, Mặt khác*.
Thay bằng:
- **Móc xích nhân quả:** Lấy kết quả của câu trước làm chủ ngữ của câu sau.
- **Nghịch chuyển tự nhiên:** "Tuy vậy,", "Trên thực tế,", "Trái lại,".
- **Phương án thay thế:** "Thay vì..., hệ thống chọn...", "Để giải quyết hiện tượng này,...".

### Phá bỏ khuôn mẫu đoạn văn 3 thì
Không viết mọi mục theo công thức: `[Giới thiệu chung] → [Liệt kê tính năng] → [Tự khen nâng tầm]`.
Hãy mở đầu đoạn văn đa dạng:
- Mở đầu bằng bài toán/yêu cầu ràng buộc nghiệp vụ.
- Mở đầu bằng cấu trúc dữ liệu hoặc thực thể trung tâm.
- Mở đầu bằng sự cố kỹ thuật hoặc kết quả benchmark.

---

## 8. Bảng so sánh 3 cấp độ (Evolution Table)

| Cấp 1: AI sáo rỗng (Tệ) | Cấp 2: Sửa vội (Khô cứng hành chính) | Cấp 3: Kỹ sư thực chiến (Chuẩn) |
| :-- | :-- | :-- |
| "Hệ thống áp dụng công nghệ caching tiên tiến nhằm tối ưu hóa hiệu năng và mang lại trải nghiệm liền mạch cho người dùng." | "Hệ thống sử dụng Redis để lưu dữ liệu tạm thời. Việc này giúp giảm thời gian truy vấn vào cơ sở dữ liệu." | "Nhóm đặt một lớp đệm Redis phía trước PostgreSQL với thời gian sống (TTL) 5 phút cho dữ liệu danh mục hàng. Tỷ lệ cache hit đạt 88%, giảm lượng truy vấn đọc trực tiếp vào cơ sở dữ liệu từ 1.200 xuống còn 140 query mỗi phút trong giờ cao điểm." |
| "Điều này cho thấy việc xây dựng hệ thống quản lý tập trung là hoàn toàn cần thiết và đóng vai trò then chốt." | "Cần phải xây dựng hệ thống tập trung để quản lý thông tin." | "Ba hạn chế nêu trên khiến việc duy trì các file Excel rời rạc không còn khả thi. Một cơ sở dữ liệu tập trung là giải pháp bắt buộc để tránh sai lệch số liệu tồn kho giữa các chi nhánh." |
| "Module xác thực không chỉ đảm bảo an toàn tuyệt đối mà còn cung cấp khả năng phân quyền vô cùng linh hoạt." | "Module xác thực thực hiện kiểm tra mật khẩu và cấp quyền cho các tài khoản người dùng khác nhau." | "Module xác thực phân tách quyền hạn thành ba nhóm: Quản trị viên, Thu ngân và Khách hàng. Token JWT gắn kèm danh sách mã quyền tương ứng, giúp API gateway chặn truy cập trái phép ngay tại tầng ngoài cùng mà không cần truy vấn lại cơ sở dữ liệu." |

---

## 9. Quy tắc Bố cục chương & Ngôi kể

1. **Mỗi chương kết thúc bằng một đoạn "Tóm tắt chương"** 2–3 câu (nêu kết luận kỹ thuật chính, không tóm tắt theo kiểu kể lể mục lục).
2. **Nhất quán ngôi kể:** Ưu tiên ngôi thứ 3 khách quan ("nghiên cứu được tiến hành...", "hệ thống được thiết kế...") theo chuẩn các trường ĐH tại Việt Nam; nếu trường cho phép thì dùng một ngôi duy nhất (em/chúng tôi/tác giả) từ đầu đến cuối.
3. **Source truth:** Không bịa số liệu/kết quả; không nâng `PARTIAL`/`NOT_FOUND` thành `DONE`.

---

## 9bis. Bắt buộc: Đọc lại bản thảo (Self-review pass)

Viết xong **chưa phải là xong**. Trước khi giao, **bắt buộc đọc lại toàn bộ** phần văn xuôi đã viết/sửa và tự soát theo checklist §10, **không chỉ** đọc lại đoạn vừa gõ.

Quy trình 2 lượt:

1. **Lượt 1 — Viết:** tạo nội dung theo 4 trụ cột (§3) và nhịp điệu (§5).
2. **Lượt 2 — Đọc lại & sửa:** đọc như một người phản biện độc lập, gạch lỗi rồi sửa:
   - **Dấu hiệu máy:** em dash, in đậm thân bài, highlight, bullet tràn lan, câu rào đón, từ sáo rỗng (Fluff Blacklist §6.B).
   - **Nhịp điệu:** có câu nào "đều đều ~20 từ" không; có lặp khuôn ("Bên cạnh đó / Ngoài ra / Hơn nữa") không.
   - **Nhất quán:** ngôi kể, thuật ngữ (không chồng chất, viết tắt sau lần đầu).
   - **Đọc to** (hoặc đọc trên bản render) để bắt câu nghe khẩu ngữ hoặc hành chính.

> **Không trả bản thảo nếu chưa qua Lượt 2.** Viết nhiều chương thì đọc lại **cả cụm** để bắt trùng ý giữa các mục, không soát rời từng đoạn.

---

## 10. Checklist trước khi giao

```text
[ ] Không có chữ in đậm / bôi đậm trong thân bài.
[ ] Không có dấu gạch dài em dash (—).
[ ] Không có highlight màu / nền vàng.
[ ] Không còn từ sáo rỗng trong Fluff Blacklist (tối ưu hóa, đóng vai trò then chốt, toàn diện...).
[ ] Không có câu "hướng dẫn nội bộ" (trước khi nộp..., cần đối chiếu...).
[ ] Câu có nhịp thở (đan xen câu ngắn 4-8 từ với câu trung bình và câu phức).
[ ] Có lý do đánh đổi (trade-offs) và thông số kỹ thuật cụ thể; không chép rác giáo trình.
[ ] Các đoạn nối nhau bằng logic nội tại, không lặp chuỗi "Bên cạnh đó / Ngoài ra / Hơn nữa".
[ ] Mỗi chương kết thúc bằng "Tóm tắt chương" 2–3 câu thực chất.
[ ] Ngôi kể nhất quán từ đầu đến cuối, không trộn.
[ ] Giọng trang trọng vừa phải: không cảm thán, không tiếng lóng ("cực", "siêu", "ok", "nó").
[ ] Thuật ngữ không chồng chất (≤ 1–2 thuật ngữ mới/câu); lần đầu có viết đầy đủ + viết tắt.
[ ] Đã render và đọc lại trên trang in thật (theo skill docx-report).
```

---

## 11. Tài liệu tham khảo sâu

- Cẩm nang Giọng văn Thực chiến & Nhịp điệu: xem `reference/voice-and-cadence.md`.
- Trang trọng vừa phải & kiểm soát thuật ngữ: xem `reference/register-and-jargon.md`.
- Checklist chi tiết + ví dụ trước/sau: xem `reference/checklist.md`.
- Nguồn học viết báo cáo (quy định 12+ trường VN + quốc tế): xem `reference/sources.md`.
