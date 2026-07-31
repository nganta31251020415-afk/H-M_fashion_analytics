# 05. Data Cleaning & Data Validation Report

Tài liệu ghi nhận toàn bộ quy trình làm sạch (Data Cleaning) và xác thực dữ liệu (Data Validation) cho dự án phân tích dữ liệu H&M Personalized Fashion Analytics.

---

## Articles Table Cleaning Log

### 1. Phát hiện bài toán (Profiling Summary)

Trước khi thực hiện làm sạch, bảng `articles.csv` thô trong `data/raw/` được kiểm tra tổng thể về số lượng bản ghi, tính duy nhất của khóa chính, kiểu dữ liệu và tỷ lệ giá trị thiếu (NULLs).

* **Tổng số dòng ban đầu:** 105,542 dòng.
* **Tổng số cột:** 25 cột.
* **Kiểm tra Primary Key (`article_id`):** 105,542 giá trị duy nhất (không có bản ghi trùng lặp, không có NULL).
* **Vấn đề Định dạng & Kiểu dữ liệu:**
  * Cột `article_id` ban đầu chứa các mã chuỗi số dài 10 ký tự có số `0` ở đầu (ví dụ: `'0108775015'`). Khi đọc dữ liệu tự động bằng một số công cụ (pandas/excel), cột này bị ép thành kiểu số nguyên `INT64` làm mất các số `0` ở đầu (biến đổi thành `108775015`), dẫn tới nguy cơ sai lệch mã định danh khi JOIN với bảng giao dịch `transactions_train`.
  * Cột `product_code` là mã chuỗi 7 ký tự có số `0` ở đầu (ví dụ: `'0108775'`), cũng gặp nguy cơ mất số `0` nếu ép kiểu sai.
  * Các cột chuỗi/văn bản có nguy cơ chứa khoảng trắng thừa (leading/trailing whitespace).
* **Phân tích Missing Values (Dữ liệu bị khuyết):**

| Tên Cột | Số Dòng Khuyết (NULL) | Tỷ Lệ NULL (%) | Tình Trạng Dữ Liệu |
| :--- | :---: | :---: | :--- |
| `detail_desc` | **416** | **0.394%** | Chi tiết mô tả sản phẩm bị khuyết |
| *24 cột còn lại* | **0** | **0.000%** | Đầy đủ 100% dữ liệu |

---

### 2. Quyết định xử lý & Lý do Business (Decision Log)

Mọi quyết định làm sạch dữ liệu đều được cân nhắc trên cả hai khía cạnh **Yêu cầu Nghiệp vụ (Business Rationale)** và **Kỹ thuật dữ liệu (Technical Rationale)**:

#### 2.1. Xử lý Missing Value đối với cột `detail_desc` (416 NULLs - 0.394%)
* **Cột thiếu:** `detail_desc` (Mô tả chi tiết sản phẩm).
* **Tỷ lệ thiếu:** 416 / 105,542 dòng (~ 0.394%).
* **Phương pháp áp dụng:** **Impute bằng giá trị mặc định** (`'No description available'`).
* **Giải thích góc độ Kinh doanh (Business Rationale):**
  * `article_id` là khóa chính thuộc bảng Dimension đại diện cho danh mục sản phẩm của H&M. Xóa 416 sản phẩm này khỏi hệ thống sẽ khiến các giao dịch phát sinh mua bán liên quan tới 416 mã sản phẩm đó trong quá khứ bị biến thành **"bản ghi mồ côi" (orphaned transactions)** trong bảng Fact `transactions_train`.
  * Điều này gây sai lệch tổng doanh thu, số lượng bán ra và vi phạm nghiêm trọng tính toàn vẹn tham chiếu (Referential Integrity) của Data Model.
* **Giải thích góc độ Kỹ thuật (Technical Rationale):**
  * Việc thay thế NULL bằng chuỗi cố định `'No description available'` giúp tránh lỗi NullPointerException / NaN khi đưa dữ liệu vào Power BI Dashboard, tạo bảng báo cáo catalog sản phẩm, hoặc thực hiện các kỹ thuật xử lý ngôn ngữ tự nhiên (NLP Text Vectorization) trong giai đoạn Machine Learning tiếp theo mà không phải bỏ đi bất kỳ dòng dữ liệu nào.

#### 2.2. Xử lý Định dạng & Ép kiểu cho `article_id` và `product_code`
* **Phương pháp áp dụng:** Ép kiểu về `VARCHAR` và áp dụng hàm `LPAD`:
  * `article_id`: `LPAD(TRIM(article_id), 10, '0')`
  * `product_code`: `LPAD(TRIM(product_code), 7, '0')`
* **Giải thích:** Đảm bảo 100% mã sản phẩm giữ đúng độ dài cố định và không bị mất các ký tự số `0` đứng đầu khi lưu trữ hoặc liên kết bảng.

#### 2.3. Xử lý Khoảng trắng cho các Cột Text
* **Phương pháp áp dụng:** Áp dụng `TRIM()` cho toàn bộ 14 cột dạng văn bản (`prod_name`, `product_type_name`, `product_group_name`, `graphical_appearance_name`, `colour_group_name`, `perceived_colour_value_name`, `perceived_colour_master_name`, `department_name`, `index_code`, `index_name`, `index_group_name`, `section_name`, `garment_group_name`, `detail_desc`).
* **Giải thích:** Loại bỏ khoảng trắng thừa hai đầu chuỗi để tránh việc gom nhóm (GROUP BY) bị phân tách nhầm thành các giá trị khác nhau do khoảng trắng ẩn.

---

### 3. Kết quả xác thực (Validation Results)

Pipeline tự động `src/data/clean_articles.py` đã thực thi và kiểm tra thành công tất cả các tiêu chuẩn Data Validation:

| Tiêu Chi Xác Thực (Validation Metric) | Trước Khi Clean (`articles.csv`) | Sau Khi Clean (`cleaned_articles.parquet`) | Trạng Thái Validation |
| :--- | :---: | :---: | :---: |
| **Tổng số dòng (Row Count)** | 105,542 | 105,542 | ✅ Đã xác nhận (Bảo toàn 100%) |
| **Số `article_id` duy nhất (Primary Key)** | 105,542 | 105,542 | ✅ Đã xác nhận (Không trùng lặp) |
| **Số dòng có `article_id` độ dài != 10** | 0 (nếu dạng str) | 0 | ✅ Đã xác nhận (Đủ 10 ký tự `0` đầu) |
| **Số dòng có `product_code` độ dài != 7** | 0 (nếu dạng str) | 0 | ✅ Đã xác nhận (Đủ 7 ký tự `0` đầu) |
| **Số giá trị NULL ở cột `detail_desc`** | 416 (0.394%) | 0 | ✅ Đã xác nhận (Đã impute) |
| **Tổng số giá trị NULL trên toàn bộ 25 cột** | 416 | **0** | ✅ Đã xác nhận (100% Clean) |
| **Định dạng file lưu trữ** | `.csv` (36.1 MB) | `.parquet` (5.98 MB) | ✅ Giảm dung lượng 83.4%, nén Snappy |

---

### 📁 Tệp đầu ra đã tạo (Outputs Created):
1. **Script xử lý dữ liệu:** [src/data/clean_articles.py](file:///d:/MindX_3/Final_Project/hm-fashion-analytics/src/data/clean_articles.py)
2. **Dữ liệu sạch Parquet:** `data/processed/cleaned_articles.parquet` (5.98 MB)
3. **Báo cáo Data Cleaning:** [docs/05_data_cleaning_validation.md](file:///d:/MindX_3/Final_Project/hm-fashion-analytics/docs/05_data_cleaning_validation.md)

---
---

## Customers Table Cleaning Log

### 1. Phát hiện bài toán (Profiling Summary)

Trước khi thực hiện làm sạch dữ liệu khách hàng, tệp `customers.csv` thô trong `data/raw/` được phân tích tổng thể nhằm phát hiện tỷ lệ dữ liệu thiếu, kiểm tra tính duy nhất của mã khách hàng và phân phối thuộc tính nhân khẩu học.

* **Tổng số dòng ban đầu:** 1,371,980 khách hàng.
* **Tổng số cột:** 7 cột.
* **Kiểm tra Primary Key (`customer_id`):** 1,371,980 chuỗi Hexadecimal 64 ký tự duy nhất (100% Unique, không có bản ghi trùng lặp, không có NULL).
* **Phân tích Missing Values (Dữ liệu bị khuyết):**

| Tên Cột | Số Dòng Khuyết (NULL) | Tỷ Lệ NULL (%) | Ý Nghĩa Dữ Liệu Thô |
| :--- | :---: | :---: | :--- |
| `Active` | **907,576** | **66.1508%** | Trạng thái hoạt động tương tác với tin tức thời trang |
| `FN` | **895,050** | **65.2378%** | Trạng thái đăng ký nhận bản tin thời trang (Fashion News) |
| `fashion_news_frequency` | **16,009** | **1.1669%** | Tần suất nhận bản tin thời trang |
| `age` | **15,861** | **1.1561%** | Độ tuổi khách hàng |
| `club_member_status` | **6,062** | **0.4418%** | Trạng thái thành viên CLB khách hàng |
| `customer_id` | **0** | **0.0000%** | Mã định danh khách hàng (Hex 64 chars) |
| `postal_code` | **0** | **0.0000%** | Mã bưu chính đã mã hóa |

---

### 2. Quyết định xử lý & Lý do Business (Decision Log)

Mọi thao tác làm sạch được thiết kế để **bảo toàn 100% 1,371,980 bản ghi khách hàng**, không loại bỏ bất kỳ dòng nào nhằm phục vụ các bài toán Customer Segmentation, Conversion Rate và RFM Analysis.

#### 2.1. Xử lý Cờ Nhị Phân: `FN` (65.24% NULL) và `Active` (66.15% NULL)
* **Phương pháp áp dụng:** Quy ước `NULL` $\rightarrow$ `0` (không đăng ký / không active), giá trị `'1.0'` $\rightarrow$ `1`. Ép kiểu thành `INT8` (`TINYINT`).
* **Lý do Kinh doanh (Business Rationale):** 
  * `FN` (Fashion News Direct Mail Newsletter) và `Active` là các cờ nhị phân mang ý nghĩa "opt-in" (chủ động đăng ký). Khi dữ liệu ghi nhận `NULL`, điều đó phản ánh thực tế rằng khách hàng không chủ động đăng ký nhận tin hoặc không ở trong trạng thái active communication.
  * Quy ước về `0` vừa phản ánh chính xác hành vi kinh doanh, vừa bảo toàn 1,371,980 khách hàng trong Customer Dimension.
* **Lý do Kỹ thuật (Technical Rationale):** 
  * Chuyển đổi từ chuỗi/float dạng `1.0` và `NULL` về số nguyên `0` và `1` (`INT8`) giúp tối ưu bộ nhớ lưu trữ và cho phép các thuật toán Machine Learning (Tree-based, Logistic Regression, Clustering) trích xuất làm feature nhị phân trực tiếp.

#### 2.2. Xử lý Missing Value Độ Tuổi (`age` - 1.16% NULL - 15,861 dòng)
* **Phương pháp áp dụng:** **Distribution-based Random Sampling Imputation** (Lấy mẫu ngẫu nhiên trực tiếp từ phân phối thực tế của các giá trị `age` không bị thiếu, sử dụng fixed random seed = 42).
* **Lý do Kinh doanh & Kỹ thuật (Why NOT Mean / Median?):**
  * **TẠI SAO KHÔNG DÙNG MEAN (36.39) HOẶC MEDIAN (32.0):** Nếu điền 15,861 dòng thiếu bằng giá trị Mean (36) hoặc Median (32), sẽ tạo ra một **đỉnh nhọn nhân tạo (artificial spike)** tại độ tuổi đó. Điều này làm giảm phương sai, giảm độ lệch chuẩn và làm bóp méo hình dáng histogram độ tuổi thực tế của H&M (vốn có 2 đỉnh tập trung chính là nhóm khách hàng trẻ ~20-25 tuổi và nhóm trung niên ~50 tuổi).
  * **ƯU ĐIỂM CỦA SAMPLING DỰA TRÊN PHÂN PHỐI:** Phương pháp lấy mẫu ngẫu nhiên từ phân phối thực giúp bảo toàn chính xác 100% hình dạng histogram, giữ cho Mean, Std, và các giá trị phân vị (P25, P50, P75) gần như hoàn toàn không thay đổi trước và sau khi impute.

#### 2.3. Xử lý Cột Categorical (`club_member_status`, `fashion_news_frequency`)
* **`club_member_status`:** Xóa khoảng trắng thừa `TRIM()`, chuẩn hóa chữ hoa, chuyển `NULL` và chuỗi rỗng $\rightarrow$ `'NONE'`.
* **`fashion_news_frequency`:** Standardize về các giá trị chuẩn (`'NONE'`, `'Regularly'`, `'Monthly'`), chuyển các dạng `NULL`, `'None'`, `''` $\rightarrow$ `'NONE'`.

#### 2.4. Xử lý Chuỗi Mã Định Danh (`customer_id`, `postal_code`)
* **Áp dụng:** `TRIM()` loại bỏ khoảng trắng thừa ẩn. Đảm bảo giữ nguyên dạng chuỗi Hex 64 ký tự.

---

### 3. Kết quả xác thực (Validation Results)

Pipeline tự động `src/data/clean_customers.py` đã thực thi và vượt qua tất cả các bài test kiểm tra tự động:

#### 3.1. So sánh Thống kê Độ tuổi (`age`) Trước & Sau khi Impute

| Chỉ Số Thống Kê (Age Metric) | Trước Khi Impute (`customers.csv`) | Sau Khi Impute (`cleaned_customers.parquet`) | Mức Độ Biến Đổi |
| :--- | :---: | :---: | :---: |
| **Số lượng bản ghi có tuổi** | 1,356,119 | **1,371,980** | +15,861 dòng (Đã làm sạch 100%) |
| **Giá trị trung bình (Mean)** | 36.3870 | **36.3862** | $\Delta = 0.000732$ (Không đáng kể) |
| **Độ lệch chuẩn (Std Dev)** | 14.3136 | **14.3143** | $\Delta = 0.000694$ (Bảo toàn phương sai) |
| **Giá trị nhỏ nhất (Min)** | 16.0 | **16.0** | Giữ nguyên |
| **Phân vị 25% (P25)** | 24.0 | **24.0** | Giữ nguyên |
| **Trung vị (Median / P50)** | 32.0 | **32.0** | Giữ nguyên |
| **Phân vị 75% (P75)** | 49.0 | **49.0** | Giữ nguyên |
| **Giá trị lớn nhất (Max)** | 99.0 | **99.0** | Giữ nguyên |

> **Nhận xét:** Sự lệch giữa Mean và Std trước và sau Impute nhỏ hơn $0.001$, khẳng định phương pháp Distribution-based Random Sampling bảo toàn hoàn hảo phân phối độ tuổi khách hàng ban đầu.

#### 3.2. Bảng Xác thực Chất lượng Dữ liệu Tổng thể

| Tiêu Chi Xác Thực (Validation Metric) | Trước Khi Clean (`customers.csv`) | Sau Khi Clean (`cleaned_customers.parquet`) | Trạng Thái Validation |
| :--- | :---: | :---: | :---: |
| **Tổng số dòng (Row Count)** | 1,371,980 | 1,371,980 | ✅ Bảo toàn 100% dòng |
| **Số `customer_id` duy nhất (Primary Key)** | 1,371,980 | 1,371,980 | ✅ Khóa chính 100% Unique |
| **Số `customer_id` có độ dài != 64** | 0 | 0 | ✅ Chuẩn Hex 64 ký tự |
| **Số giá trị NULL ở `FN` & `Active`** | ~1.8 triệu NULLs | 0 (Đã quy ước về 0/1) | ✅ Đã ép kiểu `INT8` (0 hoặc 1) |
| **Số giá trị NULL ở `age`** | 15,861 (1.16%) | 0 (Đã Impute Sampling) | ✅ Không biến dạng phân phối |
| **Tổng số giá trị NULL trên cả 7 cột** | 1,836,558 | **0** | ✅ Clean 100% (0 NULLs) |
| **Định dạng file & Dung lượng** | `.csv` (207.1 MB) | `.parquet` (160.03 MB) | ✅ Nén Parquet Snappy tối ưu |

---

### 📁 Tệp đầu ra đã tạo (Outputs Created):
1. **Script xử lý dữ liệu:** [src/data/clean_customers.py](file:///d:/MindX_3/Final_Project/hm-fashion-analytics/src/data/clean_customers.py)
2. **Dữ liệu sạch Parquet:** `data/processed/cleaned_customers.parquet` (160.03 MB)
3. **Báo cáo Data Cleaning:** [docs/05_data_cleaning_validation.md](file:///d:/MindX_3/Final_Project/hm-fashion-analytics/docs/05_data_cleaning_validation.md)

---
---

## Transactions Table Cleaning Log

### 1. Phát hiện bài toán (Profiling Summary)

Tệp dữ liệu giao dịch `transactions_train.csv` trong `data/raw/` chứa hơn 31.7 triệu bản ghi chi tiết các đơn hàng bán lẻ của H&M.

* **Tổng số dòng ban đầu:** 31,788,324 giao dịch.
* **Tổng số cột:** 5 cột (`t_dat`, `customer_id`, `article_id`, `price`, `sales_channel_id`).
* **Khoảng thời gian giao dịch:** 2018-09-20 đến 2020-09-22 (734 ngày).
* **Phân tích Missing Values (Dữ liệu bị khuyết):** **0 NULLs** trên toàn bộ 5 cột (Dữ liệu hoàn toàn đầy đủ 100%).
* **Phân tích Giá bán (`price`):**
  * Giá trị nhỏ nhất (Min): `0.000017`
  * Giá trị trung bình (Avg): `0.027829`
  * Giá trị lớn nhất (Max): `0.591525`
  * **Số dòng có $price \le 0$:** **0 dòng** (Không có lỗi dữ liệu giá âm hoặc bằng 0).
  * *Ghi chú nghiệp vụ:* Giá trị cột `price` trong dataset H&M Kaggle đã được chuẩn hóa theo tỷ lệ (scaled) thay vì giữ đơn vị tiền tệ thô.
* **Kênh bán hàng (`sales_channel_id`):**
  * Kênh 1: 9,408,462 giao dịch (~ 29.60%)
  * Kênh 2: 22,379,862 giao dịch (~ 70.40%)

---

### 2. Quyết định xử lý & Lý do Business (Decision Log)

Mọi quyết định xử lý được đưa ra dựa trên nguyên tắc **bảo toàn đúng bản chất hạt dữ liệu (Data Grain)** và đảm bảo tính toàn vẹn tham chiếu dữ liệu (Referential Integrity):

#### 2.1. Bảo tồn Grain & Xử lý Dòng Trùng Lặp Nghiệp Vụ (Multiple Quantity Purchases)
* **Phát hiện:** Có **3,204,435 dòng** có trùng khớp hoàn toàn tổ hợp 4 thuộc tính `(customer_id, article_id, t_dat, sales_channel_id)`.
* **Phương pháp áp dụng:** **TUYỆT ĐỐI KHÔNG XÓA DÒNG TRÙNG LẶP**. Bảo toàn 100% 31,788,324 dòng giao dịch.
* **Lý do Nghiệp vụ (Business Rationale):** 
  * Bảng `transactions_train` không chứa cột số lượng `quantity`. Theo mô tả chính thức của H&M trên Kaggle, khi một khách hàng mua $N$ sản phẩm cùng loại trong cùng một giao dịch (ngày & kênh bán hàng), hệ thống ghi nhận $N$ bản ghi riêng biệt cho từng sản phẩm.
  * Việc xóa các dòng trùng tổ hợp này sẽ làm sụt giảm giả tạo **3,204,435 sản phẩm đã bán**, gây sai lệch nghiêm trọng báo cáo tổng doanh thu và sản lượng bán hàng.

#### 2.2. Chuẩn hóa Khóa & Ép kiểu Dữ liệu
* **`article_id`:** Ép kiểu thành `VARCHAR` và dùng `LPAD(TRIM(article_id), 10, '0')` để bảo toàn 10 ký tự chuỗi có số `0` ở đầu, khớp với Primary Key của bảng `cleaned_articles.parquet`.
* **`customer_id`:** Áp dụng `TRIM(customer_id)` giữ nguyên chuỗi Hexadecimal 64 ký tự, khớp với Primary Key của bảng `cleaned_customers.parquet`.
* **`t_dat`:** Ép kiểu từ `VARCHAR` về `DATE` chuẩn ISO (`YYYY-MM-DD`).
* **`sales_channel_id`:** Ép kiểu từ `INT64` về `INT8` (`TINYINT`) để tiết kiệm dung lượng lưu trữ.

#### 2.3. Xác thực Liên kết Khóa (Referential Integrity Check)
* **Xác thực với bảng Customer Dimension (`cleaned_customers.parquet`):** 
  * Số `customer_id` mồ côi (không tồn tại trong bảng khách hàng): **0**.
  * $\rightarrow$ 100% khách hàng trong lịch sử giao dịch đều có thông tin trong bảng Customer Dimension.
* **Xác thực với bảng Article Dimension (`cleaned_articles.parquet`):**
  * Số `article_id` mồ côi (không tồn tại trong bảng sản phẩm): **0**.
  * $\rightarrow$ 100% mã sản phẩm phát sinh giao dịch đều có thông tin trong bảng Article Dimension.

---

### 3. Kết quả xác thực (Validation Results)

Pipeline tự động `src/data/clean_transactions.py` (sử dụng DuckDB) đã thực thi thành công và kiểm tra toàn bộ tiêu chuẩn dữ liệu:

| Tiêu Chi Xác Thực (Validation Metric) | Trước Khi Clean (`transactions_train.csv`) | Sau Khi Clean (`cleaned_transactions.parquet`) | Trạng Thái Validation |
| :--- | :---: | :---: | :---: |
| **Tổng số dòng (Row Count)** | 31,788,324 | **31,788,324** | ✅ Bảo toàn 100% bản ghi giao dịch |
| **Tổng số giá trị NULL (All 5 cols)** | 0 | **0** | ✅ Clean 100% (0 NULLs) |
| **Khoảng thời gian giao dịch** | 2018-09-20 đến 2020-09-22 | **2018-09-20 đến 2020-09-22** | ✅ Đã xác nhận chuẩn ISO `DATE` |
| **Số dòng có $price \le 0$** | 0 | **0** | ✅ 100% giao dịch có $price > 0$ |
| **Khách hàng mồ côi (Orphan `customer_id`)** | 0 | **0** | ✅ 100% Khóa ngoại khớp với Customers |
| **Sản phẩm mồ côi (Orphan `article_id`)** | 0 | **0** | ✅ 100% Khóa ngoại khớp với Articles |
| **Định dạng file & Dung lượng** | `.csv` (3.48 GB / 3,488 MB) | `.parquet` (**769.19 MB**) | ✅ Nén Parquet Snappy (Giảm 78% dung lượng) |

---

### 📁 Tệp đầu ra đã tạo (Outputs Created):
1. **Script xử lý dữ liệu:** [src/data/clean_transactions.py](file:///d:/MindX_3/Final_Project/hm-fashion-analytics/src/data/clean_transactions.py)
2. **Dữ liệu sạch Parquet:** `data/processed/cleaned_transactions.parquet` (769.19 MB)
3. **Báo cáo Data Cleaning:** [docs/05_data_cleaning_validation.md](file:///d:/MindX_3/Final_Project/hm-fashion-analytics/docs/05_data_cleaning_validation.md)
