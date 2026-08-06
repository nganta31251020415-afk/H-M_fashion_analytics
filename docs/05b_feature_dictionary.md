# Feature Dictionary (Từ Điển Đặc Trưng)
## Dự án Phân tích Dữ liệu & Machine Learning – H&M Personalized Fashion Analytics

> **Phiên bản tài liệu:** v1.0  
> **Trạng thái:** Hoàn thành Phase 3 – Feature Engineering & Feature Store Documentation  
> **Vị trí dữ liệu:**  
> - Customer Mart: `file:///d:/MindX_3/Final_Project/hm-fashion-analytics/data/marts/customer_features.parquet`  
> - Product Mart: `file:///d:/MindX_3/Final_Project/hm-fashion-analytics/data/marts/product_features.parquet`

---

# 1. Giới thiệu chung (Overview & Purpose)

Tài liệu **Feature Dictionary** đóng vai trò là Feature Store trung tâm cho toàn bộ dự án H&M Fashion Analytics. Bộ dữ liệu đặc trưng này được tổng hợp từ dữ liệu thô đã làm sạch (`cleaned_transactions.parquet`, `cleaned_customers.parquet`, `cleaned_articles.parquet`) thông qua pipeline tính toán hiệu năng cao bằng DuckDB.

Các đặc trưng (features) được thiết kế nhằm phục vụ trực tiếp **3 bài toán kinh doanh trọng tâm** của dự án:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   FEATURE STORE CORE PURPOSES                                   │
└───────────────────────────────────────────────┬────────────────────────────────────────────────┘
                                                │
         ┌──────────────────────────────────────┼──────────────────────────────────────┐
         ▼                                      ▼                                      ▼
┌─────────────────────────┐            ┌─────────────────────────┐            ┌─────────────────────────┐
│       TRỤ CỘT 1         │            │       TRỤ CỘT 2         │            │       TRỤ CỘT 3         │
│  Tăng Retention & Giảm  │            │   Cá Nhân Hóa Trải      │            │   Quyết Định Nhập Hàng  │
│      Rời Bỏ (Churn)     │            │    Nghiệm Mua Sắm       │            │    Dựa Trên Dữ Liệu     │
└─────────────────────────┘            └─────────────────────────┘            └─────────────────────────┘
```

1. **Trụ cột 1 (Customer Retention & Churn Reduction):** Cung cấp các biến hành vi khách hàng (Recency, Frequency, Monetary, Tenure, RFM Scores, Churn Signals) để phân nhóm khách hàng (RFM Segmentation) và xây dựng mô hình dự báo rủi ro rời bỏ (Customer Churn Prediction).
2. **Trụ cột 2 (Personalization & Next Best Action):** Cung cấp các biến về sở thích khách hàng (Category Diversity, Product Preference, Age, Member Status) và tương quan sản phẩm để xây dựng các thuật toán gợi ý sản phẩm mua kèm (Market Basket Analysis) và cá nhân hóa trải nghiệm.
3. **Trụ cột 3 (Data-Driven Merchandising & Demand Forecasting):** Cung cấp các biến hiệu suất sản phẩm (Total Revenue, Sales Count, Sales Velocity trong 30 ngày đầu, Seasonality breakdown, Peak Season) nhằm dự báo nhu cầu nhập hàng và quản lý vòng đời sản phẩm thời trang (Fast Fashion Product Lifecycle).

---

# 2. Customer & RFM Features (`customer_features.parquet`)

- **Đường dẫn file:** `data/marts/customer_features.parquet`
- **Grain:** Cấp độ Khách hàng (1 dòng = 1 `customer_id`)
- **Tổng số dòng:** 1,371,980 khách hàng (Bảo toàn 100% tệp khách hàng trong hệ thống)
- **Dung lượng file:** ~99.37 MB (Định dạng Parquet, nén ZSTD)

### Chi tiết các cột trong bảng Customer Features:

| Tên cột (Column Name) | Kiểu dữ liệu (Data Type) | Mô tả ý nghĩa nghiệp vụ | Trụ cột phục vụ |
|:---|:---:|:---|:---:|
| `customer_id` | `VARCHAR` | Khóa chính duy nhất định danh từng khách hàng (Mã băm 64 ký tự). | Cả 3 Trụ cột |
| `FN` | `TINYINT` | Trạng thái nhận bản tin Fashion News từ H&M (`1`: Có đăng ký, `NULL/0`: Không). | Trụ cột 1 & 2 |
| `Active` | `TINYINT` | Trạng thái hoạt động truyền thông (`1`: Đang hoạt động nhận tin, `NULL/0`: Không). | Trụ cột 1 |
| `club_member_status` | `VARCHAR` | Trạng thái thành viên câu lạc bộ khách hàng (`ACTIVE`, `PRE-CREATE`, `LEFT CLUB`). | Trụ cột 1 & 2 |
| `fashion_news_frequency` | `VARCHAR` | Tần suất nhận tin thời trang (`NONE`, `Regularly`, `Monthly`). | Trụ cột 1 & 2 |
| `age` | `BIGINT` | Độ tuổi của khách hàng (Từ 16 đến 99 tuổi). | Trụ cột 2 |
| `postal_code` | `VARCHAR` | Mã băm khu vực địa lý / bưu chính của khách hàng. | Trụ cột 2 |
| `first_purchase_date` | `DATE` | Ngày phát sinh giao dịch đầu tiên trong lịch sử dữ liệu của khách hàng. | Trụ cột 1 |
| `last_purchase_date` | `DATE` | Ngày phát sinh giao dịch gần nhất của khách hàng. | Trụ cột 1 |
| `recency` | `BIGINT` | Số ngày tính từ lần mua cuối cùng (`last_purchase_date`) đến ngày max của dataset (`2020-09-22`). Giá trị nhỏ hơn nghĩa là khách hàng mua gần đây hơn. | Trụ cột 1 |
| `frequency` | `INTEGER` | Tổng số ngày giao dịch `t_dat` khác nhau mà khách hàng đã thực hiện giao dịch (`COUNT(DISTINCT t_dat)`). | Trụ cột 1 |
| `monetary` | `DOUBLE` | Tổng số tiền (giá niêm yết) khách hàng đã chi tiêu trong toàn bộ lịch sử (`SUM(price)`). | Trụ cột 1 |
| `tenure` | `INTEGER` | Số ngày gắn bó tính từ lần mua đầu tiên đến lần mua cuối cùng (`DATEDIFF(last_purchase_date, first_purchase_date)`). | Trụ cột 1 |
| `category_diversity` | `INTEGER` | Số lượng sản phẩm (`article_id`) duy nhất khách hàng đã từng mua (`COUNT(DISTINCT article_id)`). Đo lường độ đa dạng trong gu thời trang. | Trụ cột 2 |
| `has_transactions` | `BOOLEAN` | Cờ ghi nhận khách hàng đã từng phát sinh giao dịch hay chưa (`TRUE`: Có giao dịch, `FALSE`: Chưa từng mua). | Trụ cột 1 |
| `r_score` | `TINYINT` | Điểm Recency phân theo Quintile 1 - 5 (`5`: Mua gần đây nhất, `1`: Mua lâu nhất về trước). | Trụ cột 1 |
| `f_score` | `TINYINT` | Điểm Frequency phân theo Quintile 1 - 5 (`5`: Tần suất mua nhiều nhất, `1`: Mua ít nhất). | Trụ cột 1 |
| `m_score` | `TINYINT` | Điểm Monetary phân theo Quintile 1 - 5 (`5`: Chi tiêu nhiều nhất, `1`: Chi tiêu ít nhất). | Trụ cột 1 |
| `rfm_score` | `VARCHAR` | Chuỗi kết hợp điểm RFM (Ví dụ: `'555'` đại diện cho khách VIP cao nhất). | Trụ cột 1 |
| `rfm_segment` | `VARCHAR` | Phân nhóm khách hàng theo luật ưu tiên RFM (`Champions`, `Loyal`, `New Customers`, `At Risk`, `Lost`, `Others`). | Trụ cột 1 & 2 |

---

### Quy tắc logic phân nhóm RFM (`rfm_segment`):

1. **Champions**: `r_score >= 4` AND `f_score >= 4` AND `m_score >= 4` (Khách hàng VIP, mua gần đây, mua thường xuyên và chi tiêu lớn).
2. **Loyal**: `f_score >= 4` (Khách hàng trung thành có tần suất mua hàng cao).
3. **New Customers**: `r_score >= 4` AND `f_score == 1` (Khách hàng mới phát sinh đơn gần đây nhưng mới mua 1 lần).
4. **At Risk**: `r_score <= 2` AND `f_score >= 3` (Khách hàng từng mua nhiều nhưng đã lâu không quay lại -> Nguy cơ rời bỏ cao).
5. **Lost**: `r_score <= 2` AND `f_score <= 2` (Khách hàng đã rời bỏ, chi tiêu thấp và không mua hàng trong thời gian dài).
6. **Others**: Các trường hợp phân bổ còn lại.

---

# 3. Product & Time Features (`product_features.parquet`)

- **Đường dẫn file:** `data/marts/product_features.parquet`
- **Grain:** Cấp độ Sản phẩm (1 dòng = 1 `article_id`)
- **Tổng số dòng:** 105,542 sản phẩm (Bảo toàn 100% danh mục catalog H&M)
- **Dung lượng file:** ~9.20 MB (Định dạng Parquet, nén ZSTD)

### Chi tiết các cột trong bảng Product Features:

| Tên cột (Column Name) | Kiểu dữ liệu (Data Type) | Mô tả ý nghĩa nghiệp vụ | Trụ cột phục vụ |
|:---|:---:|:---|:---:|
| `article_id` | `VARCHAR` | Mã định danh sản phẩm duy nhất (Định dạng 10 chữ số). | Cả 3 Trụ cột |
| `product_code` | `VARCHAR` | Mã kiểu dáng/dòng sản phẩm chung (Một product_code có thể có nhiều biến thể màu sắc article_id). | Trụ cột 3 |
| `prod_name` | `VARCHAR` | Tên thương mại của sản phẩm. | Trụ cột 2 & 3 |
| `product_type_no` | `BIGINT` | Mã số loại sản phẩm. | Trụ cột 3 |
| `product_type_name` | `VARCHAR` | Tên loại sản phẩm (Ví dụ: `Trousers`, `Dress`, `Sweater`, `Jacket`). | Trụ cột 3 |
| `product_group_name` | `VARCHAR` | Tên nhóm sản phẩm cao hơn (Ví dụ: `Garment Lower body`, `Garment Upper body`, `Swimwear`). | Trụ cột 3 |
| `graphical_appearance_no` | `BIGINT` | Mã họa tiết/kiểu trang trí. | Trụ cột 2 |
| `graphical_appearance_name` | `VARCHAR` | Tên họa tiết (Ví dụ: `Solid`, `Stripe`, `Denim`, `Check`). | Trụ cột 2 |
| `colour_group_code` | `VARCHAR` | Mã nhóm màu sắc. | Trụ cột 2 |
| `colour_group_name` | `VARCHAR` | Tên màu sắc chi tiết (Ví dụ: `Black`, `Dark Blue`, `White`, `Off White`). | Trụ cột 2 |
| `perceived_colour_value_id` | `BIGINT` | Mã độ đậm/sáng của màu. | Trụ cột 2 |
| `perceived_colour_value_name` | `VARCHAR` | Tên độ sáng màu (Ví dụ: `Dark`, `Dusty Light`, `Medium Dusty`). | Trụ cột 2 |
| `perceived_colour_master_id` | `BIGINT` | Mã màu chủ đạo gốc. | Trụ cột 2 |
| `perceived_colour_master_name` | `VARCHAR` | Tên màu chủ đạo gốc (Ví dụ: `Black`, `Blue`, `White`). | Trụ cột 2 |
| `department_no` | `BIGINT` | Mã số phòng ban hàng hóa. | Trụ cột 3 |
| `department_name` | `VARCHAR` | Tên phòng ban quản lý hàng hóa (Ví dụ: `Trouser`, `Express Classic`, `Swimwear`). | Trụ cột 3 |
| `index_code` | `VARCHAR` | Mã chỉ mục phân loại đối tượng khách hàng (Ví dụ: `A`, `B`, `F`). | Trụ cột 2 & 3 |
| `index_name` | `VARCHAR` | Tên phân loại dòng sản phẩm (Ví dụ: `Ladieswear`, `Menswear`, `Baby/Children`). | Trụ cột 2 & 3 |
| `index_group_no` | `BIGINT` | Mã nhóm chỉ mục. | Trụ cột 3 |
| `index_group_name` | `VARCHAR` | Tên nhóm phân loại lớn (Ví dụ: `Ladieswear`, `Menswear`, `Divided`, `Baby/Children`). | Trụ cột 2 & 3 |
| `section_no` | `BIGINT` | Mã số phân khu hàng hóa. | Trụ cột 3 |
| `section_name` | `VARCHAR` | Tên phân khu chi tiết trong cửa hàng/website (Ví dụ: `Womens Everyday Collection`, `Men Underwear`). | Trụ cột 2 & 3 |
| `garment_group_no` | `BIGINT` | Mã nhóm loại trang phục. | Trụ cột 3 |
| `garment_group_name` | `VARCHAR` | Tên nhóm trang phục (Ví dụ: `Trousers`, `Jersey Fancy`, `Dresses Casual`). | Trụ cột 3 |
| `detail_desc` | `VARCHAR` | Mô tả chi tiết sản phẩm bằng ngôn ngữ tự nhiên. | Trụ cột 2 |
| `has_transactions` | `BOOLEAN` | Cờ ghi nhận sản phẩm đã từng được bán hay chưa (`TRUE`: Đã bán, `FALSE`: Chưa từng giao dịch). | Trụ cột 3 |
| `first_sale_date` | `DATE` | Ngày mở bán đầu tiên (giao dịch đầu tiên) của sản phẩm trong lịch sử. | Trụ cột 3 |
| `last_sale_date` | `DATE` | Ngày phát sinh giao dịch gần nhất của sản phẩm. | Trụ cột 3 |
| `selling_lifecycle_days` | `INTEGER` | Độ dài vòng đời mở bán tính bằng số ngày (`DATEDIFF(last_sale_date, first_sale_date)`). Đo lường độ lâu bền của mã hàng Fast Fashion. | Trụ cột 3 |
| `total_revenue` | `DOUBLE` | Tổng doanh thu tích lũy tạo ra bởi sản phẩm (`SUM(price)`). | Trụ cột 3 |
| `total_sales_count` | `INTEGER` | Tổng số lượt/sản lượng sản phẩm đã bán ra (`COUNT(*)`). | Trụ cột 3 |
| `unique_customers` | `INTEGER` | Số lượng khách hàng khác nhau đã mua sản phẩm này (`COUNT(DISTINCT customer_id)`). | Trụ cột 2 & 3 |
| `avg_price` | `DOUBLE` | Mức giá bán trung bình thực tế của sản phẩm (`AVG(price)`). | Trụ cột 3 |
| `sales_velocity_30d` | `INTEGER` | **Tốc độ bán trong 30 ngày đầu:** Tổng sản lượng bán được của mã hàng trong đúng 30 ngày kể từ ngày mở bán đầu tiên (`first_sale_date`). Đây là chỉ số quan trọng đo lường độ "hot" khi sản phẩm mới tung ra thị trường. | Trụ cột 3 |
| `spring_sales_count` | `INTEGER` | Số lượng sản phẩm bán ra trong Mùa Xuân (Các tháng 3, 4, 5). | Trụ cột 3 |
| `summer_sales_count` | `INTEGER` | Số lượng sản phẩm bán ra trong Mùa Hè (Các tháng 6, 7, 8). | Trụ cột 3 |
| `autumn_sales_count` | `INTEGER` | Số lượng sản phẩm bán ra trong Mùa Thu (Các tháng 9, 10, 11). | Trụ cột 3 |
| `winter_sales_count` | `INTEGER` | Số lượng sản phẩm bán ra trong Mùa Đông (Các tháng 12, 1, 2). | Trụ cột 3 |
| `spring_revenue` | `DOUBLE` | Tổng doanh thu phát sinh trong Mùa Xuân. | Trụ cột 3 |
| `summer_revenue` | `DOUBLE` | Tổng doanh thu phát sinh trong Mùa Hè. | Trụ cột 3 |
| `autumn_revenue` | `DOUBLE` | Tổng doanh thu phát sinh trong Mùa Thu. | Trụ cột 3 |
| `winter_revenue` | `DOUBLE` | Tổng doanh thu phát sinh trong Mùa Đông. | Trụ cột 3 |
| `peak_season` | `VARCHAR` | **Mùa cao điểm:** Mùa bán chạy nhất của sản phẩm (`Spring`, `Summer`, `Autumn`, `Winter`, hoặc `None`). Hỗ trợ chiến dịch nhập hàng theo mùa vụ. | Trụ cột 3 |

---

# 4. Hướng dẫn sử dụng Feature Store cho các bước tiếp theo

1. **Giai đoạn SQL Analytics & EDA (Phase 4):**
   - Sử dụng `customer_features.parquet` để phân tích tỷ lệ giữ chân, sự phân bổ RFM và hành vi giữa các phân khúc tuổi.
   - Sử dụng `product_features.parquet` để phân tích các mặt hàng bán chạy (Top Sellers), mặt hàng bán nhanh nhất khi ra mắt (High Velocity Items), và tính mùa vụ (Seasonality Index).

2. **Giai đoạn Power BI Dashboard (Phase 5):**
   - Import trực tiếp 2 file Mart Parquet vào Power BI làm Fact/Dimension tổng hợp.
   - Xây dựng các Tab Dashboard chuẩn FOXIA: *Tab Overview*, *Tab Customer Analytics & Churn*, *Tab Product & Merchandising*, *Tab Diagnostic Deep-dive*.

3. **Giai đoạn Machine Learning (Phase 6):**
   - **Churn Prediction Model:** Xây dựng biến mục tiêu `is_churn` từ `recency` và dùng các biến `frequency`, `monetary`, `tenure`, `category_diversity`, `age` làm feature đầu vào.
   - **Market Basket & Recommender Engine:** Kết hợp `category_diversity` và danh mục sản phẩm từ `product_features.parquet` để thực hiện luật kết hợp Apriori/FP-Growth.
   - **Demand Forecasting Model:** Dùng các biến `spring_sales_count`, `summer_sales_count`, `autumn_sales_count`, `winter_sales_count`, `sales_velocity_30d` để dự báo sản lượng tiêu thụ theo danh mục cho mùa tiếp theo.
