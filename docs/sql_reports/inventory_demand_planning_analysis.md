# Báo Cáo Phân Tích SQL – Trụ Cột 3: Inventory & Demand Planning Analysis

> **Dự án:** H&M Personalized Fashion Analytics  
> **Bộ phận mục tiêu:** Merchandising, Supply Chain & Inventory Planning  
> **Nguồn dữ liệu:** `data/marts/product_features.parquet` (105,542 sản phẩm catalog)  
> **Công cụ xử lý:** DuckDB & SQL Analytics  
> **Ngày thực hiện:** 2026-08-05

---

## 1. Phân Tích Hiệu Suất Sản Phẩm Theo Mùa Cao Điểm (Peak Season Performance)

Bảng dưới đây thống kê số lượng mã hàng, doanh thu tích lũy, tổng sản lượng bán và tốc độ bán trung bình 30 ngày đầu phân theo mùa cao điểm (`peak_season`):

| Mùa Cao Điểm (`peak_season`) | Số mã hàng (`article_count`) | Tổng Doanh Thu (`total_revenue`) | Tỷ Trọng Doanh Thu (`%`) | Tổng Sản Lượng Bán (`total_sales_count`) | Tỷ Trọng Sản Lượng (`%`) | Tốc Độ Bán TB 30 Ngày Đầu (`avg_sales_velocity`) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Autumn** | 39,562 | $262,419.47 | 29.66% | 8,321,048 | 26.18% | **62.0 món/SP** |
| **Summer** | 24,291 | $240,151.36 | 27.15% | 10,030,145 | 31.55% | **84.3 món/SP** |
| **Spring** | 20,608 | $218,318.14 | 24.68% | 7,684,164 | 24.17% | **86.2 món/SP** |
| **Winter** | 20,086 | $163,757.00 | 18.51% | 5,752,967 | 18.10% | **58.7 món/SP** |

---

## 2. Phân Tích Hiệu Suất Theo Nhóm Sản Phẩm (Product Group Performance)

Bảng thống kê hiệu suất nhập hàng và tốc độ tiêu thụ theo nhóm danh mục sản phẩm (`product_group_name`):

| STT | Nhóm Sản Phẩm (`product_group_name`) | Số mã hàng (`article_count`) | Tổng Doanh Thu (`total_revenue`) | Tỷ Trọng Doanh Thu (`%`) | Tổng Sản Lượng (`total_sales_count`) | Tốc Độ Bán TB 30 Ngày Đầu (`avg_sales_velocity`) |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|
| 1 | **Garment Upper body** | 42,313 | $338,981.79 | 38.32% | 12,552,755 | **71.9 món/SP** |
| 2 | **Garment Lower body** | 19,661 | $231,774.62 | 26.20% | 7,046,054 | **74.6 món/SP** |
| 3 | **Garment Full body** | 13,160 | $128,478.94 | 14.52% | 3,552,470 | **84.0 món/SP** |
| 4 | **Swimwear** | 3,127 | $57,628.17 | 6.51% | 2,579,222 | **186.7 món/SP** |
| 5 | **Underwear** | 5,447 | $54,395.86 | 6.15% | 2,565,858 | **94.8 món/SP** |
| 6 | **Shoes** | 5,228 | $28,888.36 | 3.27% | 745,521 | **35.2 món/SP** |
| 7 | **Accessories** | 11,023 | $24,893.82 | 2.81% | 1,599,593 | **31.0 món/SP** |
| 8 | **Nightwear** | 1,882 | $8,852.82 | 1.00% | 348,180 | **51.1 món/SP** |
| 9 | **Socks & Tights** | 2,420 | $7,811.14 | 0.88% | 685,712 | **39.8 món/SP** |
| 10 | **Unknown** | 113 | $2,598.73 | 0.29% | 97,040 | **173.3 món/SP** |
| 11 | **Bags** | 25 | $243.88 | 0.03% | 7,313 | **42.6 món/SP** |
| 12 | **Items** | 15 | $61.53 | 0.01% | 5,427 | **77.0 món/SP** |
| 13 | **Underwear/nightwear** | 53 | $15.57 | 0.00% | 559 | **4.2 món/SP** |
| 14 | **Cosmetic** | 48 | $8.77 | 0.00% | 1,500 | **10.4 món/SP** |
| 15 | **Furniture** | 13 | $5.11 | 0.00% | 533 | **17.9 món/SP** |
| 16 | **Garment and Shoe care** | 9 | $4.88 | 0.00% | 279 | **9.7 món/SP** |
| 17 | **Interior textile** | 3 | $1.22 | 0.00% | 74 | **12.0 món/SP** |
| 18 | **Stationery** | 5 | $0.73 | 0.00% | 229 | **25.2 món/SP** |
| 19 | **Fun** | 2 | $0.04 | 0.00% | 5 | **2.5 món/SP** |

---

## 3. Top 10 Sản Phẩm Có Tốc Độ Bán Nhanh Nhất Trong 30 Ngày Đầu (Top Launch Velocity)

Danh sách 10 mã sản phẩm có sản lượng tiêu thụ lớn nhất trong đúng 30 ngày kể từ ngày mở bán đầu tiên (`sales_velocity_30d`):

| Top | Mã SP (`article_id`) | Tên sản phẩm (`prod_name`) | Nhóm hàng (`product_group_name`) | Velocity 30 Ngày Đầu (`sales_velocity_30d`) | Tổng Sản Lượng Bán | Doanh Thu Tích Lũy | Ngày Mở Bán | Mùa Cao Điểm |
|:---:|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|
| 1 | `0689109001` | **Timeless Sports Top** | Swimwear | **5,467 món** | 10,107 | $168.00 | 2018-12-31 | **Winter** |
| 2 | `0599580055` | **Timeless Midrise Brief** | Swimwear | **5,012 món** | 9,387 | $143.41 | 2020-03-29 | **Spring** |
| 3 | `0758064001` | **LS Reggipetto Triangle Top** | Swimwear | **4,703 món** | 5,123 | $167.01 | 2019-06-13 | **Summer** |
| 4 | `0758060001` | **LS Reggipetto Tie Tanga** | Swimwear | **4,264 món** | 4,642 | $113.48 | 2019-06-13 | **Summer** |
| 5 | `0758050001` | **LS Olivia Cheeky Tanga** | Swimwear | **3,630 món** | 4,732 | $108.91 | 2019-06-13 | **Summer** |
| 6 | `0758049001` | **LS Olivia Triangle Top** | Swimwear | **3,612 món** | 4,651 | $130.81 | 2019-06-13 | **Summer** |
| 7 | `0692930001` | **The Low Line Highwaist** | Swimwear | **3,320 món** | 8,782 | $145.99 | 2018-12-22 | **Winter** |
| 8 | `0758084002` | **LS Charlie  Swimsuit** | Swimwear | **3,270 món** | 3,947 | $221.54 | 2019-06-13 | **Summer** |
| 9 | `0559630026` | **Timeless Triangle Top** | Swimwear | **3,086 món** | 4,848 | $113.00 | 2020-03-30 | **Spring** |
| 10 | `0539723005` | **Jade Denim TRS** | Garment Lower body | **3,050 món** | 10,151 | $281.89 | 2018-09-20 | **Autumn** |

---

## 4. Nhận Xét & Insight Quản Lý Tồn Kho (Key Merchandising Takeaways)

### 📌 1. Bùng Nổ Nhu Cầu Theo Mùa Mùa Hè & Mùa Xuân (Velocity Peak)
- **Mùa Hè (Summer):** Dẫn đầu toàn hệ thống về tổng sản lượng tiêu thụ (**10.03 triệu sản phẩm**), đóng góp **$240.15K doanh thu** (27.15%).
- **Mùa Xuân (Spring):** Đạt tốc độ bán trung bình trong 30 ngày đầu cao nhất hệ thống (**86.2 món/sản phẩm**).
- **Mùa Thu (Autumn):** Mang lại doanh thu tích lũy lớn nhất (**$262.42K - 29.66%**) do giá bán đơn vị các dòng thời trang mùa thu (Jacket, Blazer, Jeans) cao hơn.

### 🏊 2. Đột Biến Tốc Độ Bán Ở Nhóm Đồ Bơi (Swimwear Velocity Anomaly)
- Nhóm **Swimwear (Đồ bơi)** có tốc độ bán trung bình 30 ngày đầu lên tới **186.7 món/sản phẩm**, gấp hơn **2.5 lần** so với nhóm quần áo thông thường (~72-75 món/sản phẩm).
- Đặc biệt, **9 trong số Top 10 sản phẩm bán nhanh nhất toàn bộ catalog H&M** thuộc về nhóm **Swimwear** (Ví dụ: `Timeless Sports Top` đạt **5,467 đơn** chỉ trong tháng đầu ra mắt).
- **Rủi ro vận hành:** Đồ bơi là nhóm hàng thời trang có tính chu kỳ bùng nổ cực ngắn. Nếu dự báo thiếu tồn kho ban đầu (Initial Buffer Stock), doanh nghiệp sẽ lập tức rơi vào tình trạng **Stock-out** (cháy hàng) và mất doanh thu mùa cao điểm.

### 👖 3. Sự Ổn Định Dài Hạn Ở Nhóm Garment Upper & Lower Body
- Hai nhóm **Garment Upper body** ($338.98K doanh thu) và **Garment Lower body** ($231.77K doanh thu) chiếm tổng cộng **64.52% doanh thu** toàn hệ thống.
- Tốc độ bán 30 ngày đầu của nhóm này duy trì mức ổn định (~72 - 75 món/SP).

---

## 5. Khuyến Nghị Chiến Lược Cho Bộ Phận Mua Hàng & Chuỗi Cung Ứng (Actionable Merchandising Recommendations)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        INVENTORY ALLOCATION STRATEGY MATRIX                            │
│                                                                                        │
│  ┌─────────────────────────┐               ┌─────────────────────────┐                 │
│  │ HIGH VELOCITY / EXPLOSIVE│               │ CORE / CONTINUOUS SUPPLY│                 │
│  │  (Swimwear / Trends)    │               │  (Upper & Lower Body)   │                 │
│  │ ► Phân bổ tồn kho ban   │               │ ► Nhập hàng liên tục    │                 │
│  │   đầu lớn (Initial Push)│               │   (Continuous Replenish)│                 │
│  └─────────────────────────┘               └─────────────────────────┘                 │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

| Chiến lược | Nhóm sản phẩm mục tiêu | Đề xuất vận hành chi tiết | KPI & Mục tiêu |
|:---|:---|:---|:---|
| **1. Kế hoạch đẩy tồn kho mở bán (Initial Buffer Push)** | Swimwear & Mẫu mốt mới (Trend items) | Chuẩn bị lượng hàng kho ban đầu lớn hơn **50-70%** so với mức trung bình cho 30 ngày đầu ra mắt. Đặt hàng sản xuất trước 8-10 tuần trước mùa cao điểm (tháng 4 cho đồ bơi). | Giảm tỷ lệ cháy hàng (Stock-out rate) < 5% trong tháng đầu ra mắt |
| **2. Bổ sung liên tục (Continuous Replenish)** | Garment Upper/Lower body (Jeans, T-shirt, Sweater) | Áp dụng mô hình dự báo nhu cầu cuốn chiếu (Rolling Demand Forecast) theo tuần để nhập hàng đều đặn, tránh tích trữ tồn kho quá lớn gây đọng vốn. | Tối ưu số vòng quay tồn kho (Inventory Turnover) > 6.0 lần/năm |
| **3. Lịch nhập hàng theo mùa (Seasonal Buying Schedule)** | Toàn bộ các dòng thời trang theo mùa | • **Tháng 2 (Spring Launch):** Đưa hàng Mùa Xuân vào kệ.<br>• **Tháng 5 (Summer Launch):** Đưa hàng Mùa Hè & Swimwear vào kệ.<br>• **Tháng 8 (Autumn Launch):** Đẩy mạnh các dòng Áo khoác & Jeans Thu-Đông. | Đảm bảo 100% đúng tiến độ ra mắt mùa |
