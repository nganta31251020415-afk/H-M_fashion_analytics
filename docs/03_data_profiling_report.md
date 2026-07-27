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
| customers | 1,371,980 | Thông tin khách hàng |
| articles | 105,542 | Thông tin sản phẩm |
| transactions_train | 31,788,324 | Lịch sử giao dịch |

---

# 3. Schema

DuckDB được sử dụng để đọc dữ liệu CSV và tự động suy luận kiểu dữ liệu (data type) của từng cột.

Việc kiểm tra schema nhằm:

- Hiểu cấu trúc của từng bảng dữ liệu.
- Xác định kiểu dữ liệu ban đầu của mỗi cột.
- Làm cơ sở cho bước Data Cleaning và Data Validation.

Kết quả chi tiết được lưu trong notebook:

notebooks/01_data_understanding.ipynb

---

# 4. Missing Values

Các cột có giá trị thiếu được ghi nhận để phục vụ bước Data Cleaning.

Ví dụ:

| Bảng | Cột | % NULL |
|------|------|---------|
| customers | FN | 65.24% |
| customers | Active | 66.15% |
| customers | club_member_status | 0.44% |
| customers | fashion_news_frequency | 1.17% |
| customers | age | 1.16% |
| articles | detail_desc | 0.39% |

Lưu ý:

Trong giai đoạn này chỉ ghi nhận tỷ lệ NULL, chưa thực hiện xử lý.

---

# 5. Cardinality

Đã kiểm tra số lượng giá trị duy nhất của các khóa quan trọng.

Ví dụ:

| Cột | Distinct |
|------|----------|
| customers.customer_id | 1,371,980 |
| articles.article_id | 105,542 |
| transactions.customer_id | 1,362,281 |
| transactions.article_id | 104,547 |

Nhận xét:

- Không phải tất cả khách hàng trong bảng customers đều phát sinh giao dịch trong khoảng thời gian quan sát.
- Không phải tất cả sản phẩm trong bảng articles đều được mua.
- Điều này là hợp lý trong dữ liệu bán lẻ và cần được lưu ý khi thực hiện các phân tích về khách hàng hoặc sản phẩm.

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

- Total rows: 31,788,324
- Distinct rows: 28,583,889

Kết luận:

Kết quả kiểm tra cho thấy tổ hợp
(customer_id, article_id, t_dat, sales_channel_id)
không phải là khóa duy nhất của bảng transactions_train.

Có 3,204,435 dòng có cùng giá trị trên bốn cột này. Tuy nhiên, theo mô tả chính thức của bộ dữ liệu H&M trên Kaggle, các dòng này đại diện cho trường hợp một khách hàng mua nhiều hơn một đơn vị của cùng một sản phẩm trong cùng một ngày và cùng một kênh bán hàng.

Do đó, đây là đặc điểm nghiệp vụ của dữ liệu (business behavior), không phải dữ liệu trùng lặp (duplicate) hay lỗi dữ liệu. Các bản ghi này sẽ được giữ nguyên trong các bước phân tích và mô hình hóa tiếp theo.

**Lưu ý:**

Bảng `transactions_train` không có Primary Key tự nhiên.
Mỗi dòng biểu diễn một lần ghi nhận giao dịch, trong đó nhiều dòng có thể có cùng
(customer_id, article_id, t_dat, sales_channel_id)
để phản ánh việc khách hàng mua nhiều sản phẩm giống nhau trong cùng một ngày.

---

# 7. Date Range

Ngày bắt đầu:

2018-09-20

Ngày kết thúc:

2020-09-22

Khoảng thời gian bao phủ: 

734 ngày

Nhận xét:

Dữ liệu bao phủ gần hai năm giao dịch, đủ dài để thực hiện phân tích xu hướng theo thời gian, mùa vụ và xây dựng các mô hình dự báo.

---

# 8. Các vấn đề phát hiện

## Các vấn đề phát hiện

- Hai cột `FN` và `Active` có tỷ lệ giá trị thiếu trên 65%, cần đánh giá mức độ hữu ích trước khi quyết định giữ lại hoặc loại bỏ.
- Một số cột (FN, Active, sales_channel_id) cần được tra cứu thêm ý nghĩa nghiệp vụ từ tài liệu chính thức của H&M.
- Bảng `transactions_train` không có Primary Key tự nhiên; cần lưu ý khi thiết kế mô hình dữ liệu.
- Một số khách hàng và sản phẩm không phát sinh giao dịch trong khoảng thời gian quan sát.
- Chưa phát hiện bất thường về cấu trúc dữ liệu ở bước Data Profiling.

---

# 9. Kết luận

## Kết luận

Sau bước Data Profiling, dự án đã:

- Hiểu cấu trúc của ba bảng dữ liệu.
- Xác nhận đặc điểm của bảng giao dịch và grain của dữ liệu.
- Ghi nhận các cột có giá trị thiếu.
- Xác định phạm vi thời gian của dữ liệu.
- Xác định các vấn đề cần xử lý trong giai đoạn Data Cleaning và Validation.

Kết quả của bước này là cơ sở để thiết kế mô hình dữ liệu (Data Modeling) và thực hiện Data Cleaning ở các giai đoạn tiếp theo.