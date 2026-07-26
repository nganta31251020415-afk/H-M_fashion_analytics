# 03. Data Profiling Report

## 1. Mục tiêu

Mục tiêu của bước Data Profiling là hiểu cấu trúc và chất lượng dữ liệu trước khi thực hiện Data Cleaning.

Các nội dung được kiểm tra bao gồm:

- Số dòng của từng bảng
- Schema
- Kiểu dữ liệu
- Tỷ lệ giá trị thiếu
- Cardinality
- Grain của bảng giao dịch
- Khoảng thời gian dữ liệu
- Dữ liệu mẫu

---

# 2. Dataset Overview

| Bảng | Số dòng | Mô tả |
|------|---------|--------|
| customers | ... | Thông tin khách hàng |
| articles | ... | Thông tin sản phẩm |
| transactions_train | ... | Lịch sử giao dịch |

---

# 3. Schema

DuckDB tự động suy luận kiểu dữ liệu của từng bảng.

Kết quả chi tiết được lưu trong notebook:

```
notebooks/01_data_understanding.ipynb
```

---

# 4. Missing Values

Các cột có giá trị thiếu được ghi nhận để phục vụ bước Data Cleaning.

Ví dụ:

| Bảng | Cột | % NULL |
|------|------|---------|
| customers | FN | ... |
| customers | Active | ... |
| ... | ... | ... |

Lưu ý:

Trong giai đoạn này chỉ ghi nhận tỷ lệ NULL, chưa thực hiện xử lý.

---

# 5. Cardinality

Đã kiểm tra số lượng giá trị duy nhất của các khóa quan trọng.

Ví dụ:

| Cột | Distinct |
|------|----------|
| customers.customer_id | ... |
| articles.article_id | ... |
| transactions.customer_id | ... |
| transactions.article_id | ... |

Nhận xét:

- Không phải tất cả khách hàng đều phát sinh giao dịch.
- Không phải tất cả sản phẩm đều được bán trong khoảng thời gian dữ liệu.

---

# 6. Grain Validation

Đã kiểm tra giả thuyết:

```
(customer_id,
 article_id,
 t_dat,
 sales_channel_id)
```

Kết quả:

- Total rows:
- Distinct rows:

Kết luận:

(ghi theo kết quả thực tế)

---

# 7. Date Range

Ngày bắt đầu:

...

Ngày kết thúc:

...

Khoảng thời gian bao phủ:

...

---

# 8. Các vấn đề phát hiện

- Một số cột có tỷ lệ NULL cao (ví dụ: FN và Active).
- Một số cột cần tra cứu thêm ý nghĩa nghiệp vụ (sales_channel_id, FN, Active).
- Chưa phát hiện vấn đề bất thường về cấu trúc dữ liệu.

---

# 9. Kết luận

Sau bước Data Profiling, nhóm đã:

- Hiểu cấu trúc của cả ba bảng dữ liệu.
- Xác nhận grain của bảng transactions.
- Ghi nhận các cột có giá trị thiếu.
- Xác định khoảng thời gian dữ liệu.
- Chuẩn bị sẵn sàng cho Phase 2 - Data Cleaning & Validation.