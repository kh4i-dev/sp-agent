# Source Log — Mẫu ghi nguồn trong quá trình nghiên cứu

Dùng để agent ghi lại bằng chứng ngay khi truy cập, tránh bịa nguồn lúc viết.

## Bảng nguồn

| # | Tiêu đề | URL | Loại (repo/docs/paper/blog) | Ngày truy cập | Mức tin cậy | Đã fetch? | Ghi chú |
|---|---|---|---|---|---|---|---|
| 1 |  |  |  |  |  |  |  |

## Trích đoạn theo luận điểm

```text
Claim: <luận điểm cần chứng minh>
Sources:
  - [1] <trích đoạn nguyên văn> (URL)
  - [2] <trích đoạn nguyên văn> (URL)
Verification: EXACT / MINOR / MAJOR / HALLUCINATED
Confidence: 0-100
```

## Nhật ký truy vấn

```text
Query: <truy vấn đã chạy>
Tool: exa / tavily / semantic-scholar / arxiv / crossref
Kết quả dùng: [1], [3]
Kết quả loại bỏ: (lý do)
```

## Nhãn mức tin cậy

- `EXACT` — nguồn khớp hoàn toàn tiêu đề/tác giả/năm/DOI.
- `MINOR` — khớp ý nhưng lệch nhỏ (năm, số trang).
- `MAJOR` — chỉ liên quan một phần.
- `HALLUCINATED` — không truy hồi được; loại bỏ.
- `UNVERIFIED` — chưa kiểm; không dùng làm kết luận.
