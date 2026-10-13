# Chuẩn Kiến Trúc & Hệ Sinh Thái Tham Chiếu — OpenAI Codex & Anthropic Claude Code

Tài liệu định hướng kiến trúc chuẩn hóa cho AI Agent dựa trên 4 repository chính thức từ OpenAI và Anthropic.

---

## 1. Bốn Repository Chuẩn Mực (Authoritative Benchmarks)

### A. Hai Repository Mã Nguồn Agent (Agent Architecture & Execution Engine)
1. **OpenAI Codex** — [github.com/openai/codex](https://github.com/openai/codex) (Apache-2.0)
   * **Giá trị nghiên cứu:** Cách tổ chức coding agent trong môi trường terminal CLI, vòng lặp thực thi công cụ (tool loop), quản lý tiến trình nền (background tasks), và cơ chế thao tác mã nguồn an toàn.
2. **Anthropic Claude Code** — [github.com/anthropics/claude-code](https://github.com/anthropics/claude-code)
   * **Giá trị nghiên cứu:** Cách đóng gói và cấu hình coding agent, tích hợp sâu vào workflow lập trình hàng ngày của kỹ sư, quản lý ngữ cảnh qua hooks và hệ thống mở rộng plugin.

### B. Hai Repository Mẫu Kỹ Năng (Skill Authoring & Workflow Packaging)
3. **Anthropic Skills** — [github.com/anthropics/skills](https://github.com/anthropics/skills)
   * **Giá trị nghiên cứu:** Cung cấp các mẫu skill tiêu chuẩn chia theo chuyên mục: *Creative & Design*, *Development & Technical*, *Document Skills*. Chứa đặc tả `SKILL.md` mẫu, kỹ thuật kiểm soát độ tự do (degrees of freedom) và cách viết kịch bản hướng dẫn agent không bị mơ hồ.
4. **OpenAI Plugins / Skills** — [github.com/openai/plugins](https://github.com/openai/plugins)
   * **Giá trị nghiên cứu:** Cách đóng gói các workflow phức tạp cho Codex thành plugin tái sử dụng; quản lý companion surfaces (`skills/`, `.mcp.json`, `hooks.json`, `evals`). *(Lưu ý: repo `openai/skills` cũ đã deprecated, tập trung vào `openai/plugins`).*

---

## 2. Lộ Trình Nghiên Cứu 3 Bước Cho Kỹ Sư Agent

```text
[Bước 1: anthropics/skills] ──► Hiểu cách viết SKILL.md: cấu trúc, độ tự do, progressive disclosure.
            │
            ▼
[Bước 2: openai/plugins]    ──► Học cách đóng gói workflow: phối hợp tool, script, hooks, evals.
            │
            ▼
[Bước 3: codex & claude-code]► Đào sâu lõi thực thi: tool-calling engine, task lifecycle, context safety.
```

---

## 3. Bài Học Cốt Lõi: Biến Yêu Cầu Mơ Hồ Thành Quy Trình Có Thể Kiểm Chứng

Không sao chép nguyên xi văn bản của các repo trên. Giá trị lớn nhất cần áp dụng vào `sp-agent` là:

1. **Chống phình to luật cấm (Anti-Rule Bloat):**
   * Càng nhồi nhét hàng tá luật cấm ("CẤM cái này, CẤM cái kia"), model càng dễ bị co cụm, hallucination hoặc suy giảm khả năng tổng hợp.
   * Thay vào đó, cung cấp: **Nguyên tắc tư duy thiết kế** + **Thư viện tương phản (Good vs Bad)** + **Bộ bài kiểm thử (Evals)**.
2. **Nguyên lý Progressive Disclosure:**
   * `SKILL.md` giữ dưới 300 dòng, chỉ đóng vai trò nhạc trưởng định tuyến và điều phối.
   * Chi tiết thiết kế sâu đưa vào `reference/design-principles.md`.
   * Ví dụ thực chiến đưa vào `reference/diagram-gallery.md`.
   * Bộ đánh giá tự động đưa vào `evals/`.
3. **Khung đánh giá độc lập (Adversarial Evals):**
   * Sau mỗi lần chỉnh sửa skill, agent không tự khen mình tốt hơn. Bắt buộc phải chạy lại toàn bộ bộ kiểm thử cố định trong `evals/` để đo lường định lượng tỷ lệ đè nhãn, cắt nét và tính đúng đắn kỹ thuật.
