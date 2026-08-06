# Báo Cáo Phân Tích SQL – Trụ Cột 2: Personalization & Category Preferences Analysis

> **Dự án:** H&M Personalized Fashion Analytics  
> **Tệp phân tích:** Khách hàng VIP (**Champions**)  
> **Nguồn dữ liệu:** `customer_features.parquet`, `cleaned_transactions.parquet`, `cleaned_articles.parquet`  
> **Công cụ xử lý:** DuckDB & SQL Analytics  
> **Ngày thực hiện:** 2026-08-05

---

## 1. Kết Quả Phân Tích Danh Mục Sản Phẩm Của Nhóm Champions

Bảng dưới đây thể hiện sự phân bổ sản lượng (`items_sold`) và doanh thu (`total_revenue`) theo từng nhóm sản phẩm (`product_group_name`) dành riêng cho phân khúc khách hàng VIP (**Champions**):

| STT | Nhóm Sản Phẩm (`product_group_name`) | Sản Lượng Đã Bán (`items_sold`) | Tỷ Trọng Sản Lượng (`%`) | Tổng Doanh Thu (`total_revenue`) | Tỷ Trọng Doanh Thu (`%`) | Giá Trung Bình / SP (`avg_item_price`) |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|
| 1 | **Garment Upper body** | 8,282,631 | 39.45% | $225,961.02 | 38.36% | $0.0273 |
| 2 | **Garment Lower body** | 4,657,256 | 22.18% | $153,837.63 | 26.12% | $0.0330 |
| 3 | **Garment Full body** | 2,464,576 | 11.74% | $89,356.41 | 15.17% | $0.0363 |
| 4 | **Underwear** | 1,657,323 | 7.89% | $34,805.18 | 5.91% | $0.0210 |
| 5 | **Swimwear** | 1,624,633 | 7.74% | $36,177.49 | 6.14% | $0.0223 |
| 6 | **Accessories** | 1,071,318 | 5.10% | $16,627.43 | 2.82% | $0.0155 |
| 7 | **Shoes** | 509,373 | 2.43% | $19,918.54 | 3.38% | $0.0391 |
| 8 | **Socks & Tights** | 423,124 | 2.02% | $4,692.89 | 0.80% | $0.0111 |
| 9 | **Nightwear** | 223,873 | 1.07% | $5,616.83 | 0.95% | $0.0251 |
| 10 | **Unknown** | 68,207 | 0.32% | $1,847.01 | 0.31% | $0.0271 |
| 11 | **Bags** | 4,989 | 0.02% | $166.21 | 0.03% | $0.0333 |
| 12 | **Items** | 3,905 | 0.02% | $43.82 | 0.01% | $0.0112 |
| 13 | **Cosmetic** | 726 | 0.00% | $4.17 | 0.00% | $0.0057 |
| 14 | **Furniture** | 351 | 0.00% | $3.39 | 0.00% | $0.0097 |
| 15 | **Underwear/nightwear** | 273 | 0.00% | $7.65 | 0.00% | $0.0280 |
| 16 | **Garment and Shoe care** | 221 | 0.00% | $3.62 | 0.00% | $0.0164 |
| 17 | **Stationery** | 163 | 0.00% | $0.52 | 0.00% | $0.0032 |
| 18 | **Interior textile** | 47 | 0.00% | $0.75 | 0.00% | $0.0160 |
| 19 | **Fun** | 5 | 0.00% | $0.04 | 0.00% | $0.0080 |

---

## 2. Top 3 Nhóm Sản Phẩm Được Mua Nhiều Nhất Bởi Nhóm Champions

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        TOP 3 PRODUCT GROUPS FOR CHAMPIONS                              │
│                                                                                        │
│   1. Garment Upper body  ───────►  39.45% Sản Lượng ($225,961.02 Doanh Thu)           │
│   2. Garment Lower body  ───────►  22.18% Sản Lượng ($153,837.63 Doanh Thu)           │
│   3. Garment Full body   ───────►  11.74% Sản Lượng ($89,356.41 Doanh Thu)            │
│                                                                                        │
│   ► TỔNG CỘNG TOP 3:  73.37% Sản Lượng  |  79.65% Tổng Doanh Thu Champions ($469.15K)  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

1. **Top 1 – Garment Upper body (Trang phục thân trên):**
   - **Sản lượng:** 8,282,631 sản phẩm (**39.45%** tổng sản lượng Champions).
   - **Doanh thu:** $225,961.02 (**38.36%** tổng doanh thu Champions).
   - **Đặc trưng:** Là nhóm sản phẩm phổ biến nhất với các dòng chủ lực như *Sweater*, *T-shirt*, *Top*, *Blouse*, *Vest top*.

2. **Top 2 – Garment Lower body (Trang phục thân dưới):**
   - **Sản lượng:** 4,657,256 sản phẩm (**22.18%** tổng sản lượng Champions).
   - **Doanh thu:** $153,837.63 (**26.12%** tổng doanh thu Champions).
   - **Đặc trưng:** Là nhóm mang lại giá trị cao trên mỗi đơn vị (`$0.0330`/item), dẫn đầu là dòng sản phẩm *Trousers / Jeans* và *Shorts*.

3. **Top 3 – Garment Full body (Trang phục toàn thân):**
   - **Sản lượng:** 2,464,576 sản phẩm (**11.74%** tổng sản lượng Champions).
   - **Doanh thu:** $89,356.41 (**15.17%** tổng doanh thu Champions).
   - **Đặc trưng:** Giá trị đơn vị cao nhất trong top 3 (`$0.0363`/item), đóng góp chủ đạo bởi mặt hàng *Dress (Váy đầm)*.

---

## 3. Chi Tiết Top 10 Loại Sản Phẩm Chi Tiết (Product Types) Dành Cho Champions

Bảng bóc tách các loại mặt hàng cụ thể (`product_type_name`) có sản lượng mua lớn nhất từ nhóm VIP Champions:

| Top | Loại mặt hàng (`product_type_name`) | Nhóm sản phẩm (`product_group_name`) | Sản lượng bán (`items_sold`) | Doanh thu tích lũy (`total_revenue`) |
|:---:|:---|:---|:---:|:---:|
| 1 | **Trousers** | Garment Lower body | 2,778,966 | $99,939.50 |
| 2 | **Dress** | Garment Full body | 2,262,134 | $82,668.35 |
| 3 | **Sweater** | Garment Upper body | 1,825,108 | $53,323.16 |
| 4 | **T-shirt** | Garment Upper body | 1,420,265 | $19,572.45 |
| 5 | **Top** | Garment Upper body | 1,064,061 | $21,689.89 |
| 6 | **Blouse** | Garment Upper body | 1,029,984 | $29,055.14 |
| 7 | **Vest top** | Garment Upper body | 916,793 | $14,441.32 |
| 8 | **Bra** | Underwear | 870,428 | $20,551.28 |
| 9 | **Shorts** | Garment Lower body | 752,055 | $17,462.40 |
| 10 | **Bikini top** | Swimwear | 701,656 | $15,960.10 |

---

## 4. Định Hướng Cá Nhân Hóa & Thuật Toán Gợi Ý (Recommender System Strategy)

Từ kết quả phân tích SQL trên tệp khách hàng giá trị cao **Champions**, các định hướng cá nhân hóa và gợi ý sản phẩm (Recommendation) được đề xuất như sau:

### 🎯 1. Chiến Lược "Complete-the-Look" (Phối Đồ Đồng Bộ)
- **Cơ sở dữ liệu:** Khách hàng Champions mua tới **39.45% Upper body** và **22.18% Lower body**. Sự kết hợp giữa Áo (Sweater/T-shirt/Blouse) và Quần (Trousers/Jeans) là hành vi cốt lõi.
- **Giải pháp Gợi ý:** Khi khách hàng VIP đang xem hoặc thêm một sản phẩm *Garment Upper body* vào giỏ hàng, thuật toán sẽ tự động đề xuất mặt hàng *Garment Lower body* tương thích về kiểu dáng/màu sắc (và ngược lại) để kích thích mua nguyên bộ (Cross-selling).

### 🛍️ 2. Gợi Ý Phụ Kiện Kèm Theo (Accessories & Underwear Cross-Sell)
- **Cơ sở dữ liệu:** Nhóm *Underwear* (7.89%), *Swimwear* (7.74%) và *Accessories* (5.10%) chiếm tổng cộng **20.73%** sản lượng mua của Champions.
- **Giải pháp Gợi ý:** Tận dụng thuật toán **Market Basket Analysis (Apriori / Association Rules)** để hiển thị thêm các sản phẩm mua kèm nhỏ (Quần lót, Bikini top, Thắt lưng, Tất/Tights) tại bước Checkout/Cart Page.

### 🌟 3. Ưu Tiên Hiển Thị Bộ Sưu Tập Mới (Early Access & Personalized Feed)
- Khách hàng Champions có tần suất mua sắm cực kỳ thường xuyên (trung bình quay lại mỗi 35.5 ngày). 
- **Giải pháp Gợi ý:** Trang chủ (Homepage) và Email newsletter dành riêng cho Champions phải tự động đẩy các mẫu thời trang mới nhất thuộc Top 3 nhóm hàng (*Upper body*, *Lower body*, *Dress*) lên vị trí ưu tiên đầu tiên (Hero Banner & Personalized Recommendation Grid).

---

## 5. Ma Trận Chiến Lược Cá Nhân Hóa (Impact vs Effort Matrix)

| Hành động | Thuật toán / Công nghệ | Mức độ ưu tiên | Tác động doanh thu dự kiến |
|:---|:---|:---:|:---:|
| **Gợi ý phối đồ Upper + Lower Body** | Item-Based Collaborative Filtering | 🔥 Cao (Quick Win) | Tăng AOV (Giá trị đơn hàng) từ 15-20% |
| **Cross-sell Phụ kiện & Swimwear** | Market Basket Analysis (Apriori Rules) | 🔥 Cao | Tăng Basket Size (Số món/đơn) thêm 0.5 - 1.0 món |
| **Bản tin Email Cá Nhân Hóa cho Champions** | Segment-Based Recommendation Feed | 🟡 Trung bình | Tăng tỷ lệ nhấp (CTR) Email thêm > 30% |
