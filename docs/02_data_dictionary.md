# 02. Data Dictionary

## Mục đích

Tài liệu này mô tả ý nghĩa của các bảng và các cột trong bộ dữ liệu **H&M Personalized Fashion Recommendations**.

Lưu ý:

- Ý nghĩa được tổng hợp từ Kaggle Data Description và tài liệu chính thức của cuộc thi.
- Một số cột không được H&M giải thích chi tiết. Các mô tả này được suy luận dựa trên tên cột và ngữ cảnh nghiệp vụ, đồng thời sẽ được xác minh thêm trong quá trình phân tích.

---

# 1. customers.csv

## Mô tả

Chứa thông tin mô tả (metadata) của khách hàng.

| Cột | Kiểu dữ liệu | Ý nghĩa |
|------|--------------|----------|
| customer_id | VARCHAR | Mã định danh duy nhất của khách hàng. |
| FN | BIGINT | Cờ (flag) liên quan đến chương trình Fashion News. H&M không giải thích chi tiết ý nghĩa của giá trị và NULL. |
| Active | BIGINT | Cờ thể hiện trạng thái hoạt động của khách hàng. Ý nghĩa cụ thể chưa được H&M mô tả rõ. |
| club_member_status | VARCHAR | Trạng thái thành viên của chương trình khách hàng thân thiết. |
| fashion_news_frequency | VARCHAR | Tần suất khách hàng đăng ký nhận Fashion News (ví dụ: Regularly, Monthly, None...). |
| age | BIGINT | Tuổi của khách hàng. |
| postal_code | VARCHAR | Mã bưu chính của khách hàng (đã được mã hóa để bảo vệ quyền riêng tư). |

---

# 2. articles.csv

## Mô tả

Chứa thông tin mô tả của từng sản phẩm.

### Thông tin định danh

| Cột | Kiểu dữ liệu | Ý nghĩa |
|------|--------------|----------|
| article_id | BIGINT | Mã định danh duy nhất của sản phẩm. |
| product_code | BIGINT | Mã sản phẩm ở cấp độ tổng quát. Một product_code có thể bao gồm nhiều article_id (biến thể màu sắc, kích thước...). |

---

### Phân loại sản phẩm

| Cột | Ý nghĩa |
|------|----------|
| product_type_no | Mã loại sản phẩm. |
| product_type_name | Tên loại sản phẩm (T-shirt, Dress, Jeans...). |
| product_group_name | Nhóm sản phẩm lớn hơn (Garment Upper Body, Shoes, Accessories...). |

---

### Thuộc tính hình ảnh

| Cột | Ý nghĩa |
|------|----------|
| graphical_appearance_no | Mã kiểu họa tiết. |
| graphical_appearance_name | Tên kiểu họa tiết (Solid, Stripe, Printed...). |
| colour_group_code | Mã nhóm màu. |
| colour_group_name | Tên nhóm màu. |
| perceived_colour_value_id | Mã độ sáng/tối của màu sắc. |
| perceived_colour_value_name | Mô tả độ sáng/tối của màu sắc. |
| perceived_colour_master_id | Mã màu chủ đạo. |
| perceived_colour_master_name | Tên màu chủ đạo. |

---

### Thông tin bộ phận kinh doanh

| Cột | Ý nghĩa |
|------|----------|
| department_no | Mã bộ phận kinh doanh. |
| department_name | Tên bộ phận kinh doanh. |

---

### Phân cấp trưng bày của H&M

Lưu ý:

Đây **không phải** phân loại sản phẩm, mà là cách H&M tổ chức danh mục trong cửa hàng hoặc website.

| Cột | Ý nghĩa |
|------|----------|
| index_code | Mã danh mục. |
| index_name | Tên danh mục. |
| index_group_no | Mã nhóm danh mục. |
| index_group_name | Tên nhóm danh mục. |
| section_no | Mã khu vực trưng bày. |
| section_name | Tên khu vực trưng bày. |
| garment_group_no | Mã nhóm hàng may mặc. |
| garment_group_name | Tên nhóm hàng may mặc. |

---

### Mô tả sản phẩm

| Cột | Ý nghĩa |
|------|----------|
| detail_desc | Mô tả chi tiết của sản phẩm. |

---

# 3. transactions_train.csv

## Mô tả

Chứa lịch sử giao dịch mua hàng của khách hàng.

| Cột | Kiểu dữ liệu | Ý nghĩa |
|------|--------------|----------|
| t_dat | DATE | Ngày phát sinh giao dịch. |
| customer_id | VARCHAR | Mã khách hàng. |
| article_id | BIGINT | Mã sản phẩm được mua. |
| price | DOUBLE | Giá bán đã được chuẩn hóa trong bộ dữ liệu. Đây **không phải** giá tiền thực tế theo đơn vị tiền tệ. Chỉ nên sử dụng để so sánh tương đối giữa các giao dịch hoặc tính các chỉ số trong phạm vi bộ dữ liệu. |
| sales_channel_id | BIGINT | Kênh bán hàng. Theo cộng đồng Kaggle: **1 = Online**, **2 = Cửa hàng (Offline)**. H&M không ghi rõ trong Data Description chính thức. |

---

# Các lưu ý quan trọng

## 1. Duplicate trong transactions

Các dòng trùng nhau trong `transactions_train.csv` **không nhất thiết là lỗi dữ liệu**.

Một khách hàng có thể mua nhiều đơn vị của cùng một sản phẩm trong cùng một ngày và cùng một kênh bán hàng.

---

## 2. Giá bán

Cột `price` đã được chuẩn hóa.

Không nên diễn giải:

- Doanh thu = xxx USD
- Giá trung bình = xxx USD

Chỉ nên sử dụng để:

- So sánh tương đối.
- Phân tích xu hướng.
- Xây dựng các chỉ số nội bộ của bộ dữ liệu.

---

## 3. Hai hệ thống phân cấp trong articles

Cần phân biệt hai nhóm cột:

### Nhóm 1 - Phân loại sản phẩm

```
product_code
↓
product_type
↓
product_group
```

Dùng để mô tả bản chất của sản phẩm.

### Nhóm 2 - Phân cấp trưng bày

```
index
↓
index_group
↓
section
↓
garment_group
```

Dùng để tổ chức và trưng bày sản phẩm trong hệ thống của H&M.

Hai hệ thống này phục vụ các mục đích nghiệp vụ khác nhau và không nên nhầm lẫn khi xây dựng mô hình dữ liệu.

---

# Nguồn tham khảo

- Kaggle Competition: H&M Personalized Fashion Recommendations
- Kaggle Data Description
- Kaggle Discussions (đối với `sales_channel_id`)