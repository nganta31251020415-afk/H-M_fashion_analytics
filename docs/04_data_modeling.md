# 04. Data Modeling

## 1. Mục tiêu

Mục tiêu của bước Data Modeling là xác định cấu trúc dữ liệu phục vụ cho các giai đoạn phân tích tiếp theo như SQL Analytics, Exploratory Data Analysis (EDA), Power BI Dashboard và Machine Learning.

Sau khi hoàn thành Data Understanding, nhóm tiến hành xác định:

- Grain của từng bảng
- Primary Key
- Foreign Key
- Fact Table
- Dimension Tables
- Quan hệ giữa các bảng
- Các quyết định thiết kế (Design Decisions)

Việc xây dựng mô hình dữ liệu giúp đảm bảo tính nhất quán trong toàn bộ dự án và tạo nền tảng cho các bước phân tích sau này.

---

# 2. Mô hình dữ liệu gốc

Bộ dữ liệu H&M bao gồm ba bảng chính:

- customers
- articles
- transactions_train

Trong đó:

- customers lưu thông tin mô tả khách hàng.
- articles lưu thông tin mô tả sản phẩm.
- transactions_train lưu toàn bộ lịch sử giao dịch.

Quan hệ giữa các bảng:

```
customers (1) ------< transactions_train >------ (1) articles
```

Ý nghĩa:

- Một khách hàng có thể phát sinh nhiều giao dịch.
- Một sản phẩm có thể xuất hiện trong nhiều giao dịch.
- Mỗi giao dịch chỉ thuộc về một khách hàng và một sản phẩm.

---

# 3. Grain

Grain là mức chi tiết nhỏ nhất mà mỗi dòng dữ liệu biểu diễn.

## Customers

Một dòng biểu diễn một khách hàng.

## Articles

Một dòng biểu diễn một sản phẩm.

## Transactions

Một dòng biểu diễn một lần ghi nhận việc mua một đơn vị của một sản phẩm bởi một khách hàng tại một thời điểm thông qua một kênh bán hàng.

Kết quả Data Profiling cho thấy nhiều dòng có cùng:

(customer_id, article_id, t_dat, sales_channel_id)

Theo tài liệu chính thức của H&M, đây không phải dữ liệu trùng lặp mà phản ánh trường hợp khách hàng mua nhiều hơn một đơn vị của cùng một sản phẩm trong cùng một ngày và cùng một kênh bán hàng.

Do đó, các bản ghi này được giữ nguyên và được xem là đặc điểm nghiệp vụ của dữ liệu.

---

# 4. Primary Key

| Bảng | Primary Key |
|------|-------------|
| customers | customer_id |
| articles | article_id |
| transactions_train | Không có Primary Key tự nhiên |

Bảng transactions_train không có một cột hoặc tổ hợp cột nào đảm bảo tính duy nhất tuyệt đối cho mỗi bản ghi.

---

# 5. Foreign Key

| Bảng | Foreign Key | Tham chiếu |
|------|-------------|------------|
| transactions_train | customer_id | customers.customer_id |
| transactions_train | article_id | articles.article_id |

Lưu ý:

Hiện tại `sales_channel_id` chưa được xem là Foreign Key vì bộ dữ liệu không cung cấp bảng Dimension tương ứng (ví dụ: DimSalesChannel).

Trong giai đoạn hiện tại, `sales_channel_id` được xem là một thuộc tính nghiệp vụ (Business Attribute) của Fact Table.

---

# 6. Fact và Dimension

## Fact Table

transactions_train

### Lý do lựa chọn

Đây là bảng ghi nhận các sự kiện giao dịch mua hàng và là trung tâm của hầu hết các bài toán phân tích.

Fact Table sẽ được sử dụng để tính toán các KPI và phục vụ SQL Analytics, Dashboard cũng như Machine Learning.

### Fact Table Attributes

Các thuộc tính chính gồm:

- customer_id (Foreign Key)
- article_id (Foreign Key)
- t_dat
- price
- sales_channel_id

### Measures có thể sử dụng

- price
- transaction_count (COUNT)
- quantity (suy ra từ số dòng giao dịch)

Lưu ý:

Trong bộ dữ liệu H&M, mỗi dòng giao dịch tương ứng với một sản phẩm được mua. Vì vậy quantity mặc định bằng 1 và được tính thông qua số lượng bản ghi.

---

## Dimension Tables

### Customer Dimension

customers

Chứa các thuộc tính mô tả khách hàng như:

- age
- club_member_status
- fashion_news_frequency
- postal_code
- ...

---

### Product Dimension

articles

Chứa các thuộc tính mô tả sản phẩm như:

- product_type_name
- product_group_name
- colour_group_name
- section_name
- garment_group_name
- ...

---

# 7. Star Schema

Phiên bản đầu tiên của mô hình dữ liệu gồm:

## Fact

- transactions_train

## Dimensions

- customers
- articles

Hiện tại chưa xây dựng Date Dimension.

Trường `t_dat` sẽ được sử dụng trực tiếp trong các bước phân tích.

Nếu trong tương lai cần phân tích theo:

- năm
- quý
- tháng
- tuần
- ngày lễ
- mùa

thì Date Dimension sẽ được bổ sung.

---

# 8. Thiết kế quan hệ

```
customers (1)
      |
      |------<
      |
transactions_train
      |
      >------|
             |
articles (1)
```

Cardinality:

- Customers (1) → Transactions (N)
- Articles (1) → Transactions (N)

---

# 9. Các quyết định thiết kế

| Quyết định | Lý do |
|------------|--------|
| Chọn transactions_train làm Fact Table | Đây là bảng ghi nhận các sự kiện giao dịch |
| Chọn customers làm Customer Dimension | Chứa thuộc tính mô tả khách hàng |
| Chọn articles làm Product Dimension | Chứa thuộc tính mô tả sản phẩm |
| Chưa tạo Date Dimension | Trường t_dat đáp ứng nhu cầu phân tích ở giai đoạn hiện tại |
| Giữ nguyên sales_channel_id trong Fact Table | Đây là thuộc tính nghiệp vụ quan trọng để phân tích doanh thu theo kênh bán hàng |
| Giữ toàn bộ khách hàng trong bảng customers, bao gồm cả khách hàng chưa phát sinh giao dịch | Hỗ trợ các bài toán Customer Segmentation, Customer Acquisition và phân tích hành vi khách hàng trong các giai đoạn sau |

---

# 10. Các giả định và hạn chế

Trong giai đoạn hiện tại, mô hình dữ liệu được xây dựng trực tiếp từ ba bảng gốc của bộ dữ liệu H&M.

Một số Dimension thường gặp trong Data Warehouse như:

- Date Dimension
- Sales Channel Dimension

chưa được xây dựng do bộ dữ liệu không cung cấp đầy đủ thông tin và chưa cần thiết cho phạm vi của phiên bản đầu tiên.

Các Dimension này có thể được bổ sung trong những phiên bản mở rộng của dự án.

---

# 11. Kết luận

Sau bước Data Modeling, dự án đã xác định được cấu trúc dữ liệu phục vụ cho các giai đoạn phân tích tiếp theo.

Mô hình hiện tại bao gồm:

- 1 Fact Table
- 2 Dimension Tables

theo mô hình Star Schema đơn giản.

Thiết kế này đáp ứng nhu cầu của các bước:

- Data Cleaning & Validation
- SQL Analytics
- Exploratory Data Analysis (EDA)
- Power BI Dashboard
- Machine Learning

đồng thời vẫn đủ linh hoạt để mở rộng thêm các Dimension trong tương lai khi phạm vi dự án được mở rộng.