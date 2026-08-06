# Phân Tích Dữ Liệu Khám Phá (EDA)

> **Dự án:** H&M Personalized Fashion Analytics  
> **Nguồn dữ liệu:** Dữ liệu đã làm sạch (`data/processed`) và Feature Store (`data/marts`)  
> **Ngày thực hiện:** 2026-08-06

---

## 1. Phân Tích Đơn Biến (Univariate Analysis)

### 1.1 Phân Phối Độ Tuổi Khách Hàng (Customer Age Distribution)

![Age Distribution](../../reports/figures/age_distribution.png)

* **Thống kê mô tả:**
  * Thấp nhất (Min): 16 tuổi
  * Cao nhất (Max): 99 tuổi
  * Trung bình (Mean): 36.39 tuổi

**Observation $\rightarrow$ Insight:**
* **Observation:** Đa số khách hàng tập trung ở độ tuổi từ 20 đến 30 tuổi, tạo thành một đỉnh (peak) rõ rệt. Tuy nhiên, phân phối có đuôi dài (right-skewed) trải dài đến tận độ tuổi 50-60, chứng tỏ thương hiệu vẫn duy trì được một lượng khách hàng trung niên đáng kể.
* **Insight:** Mặc dù nhóm khách hàng mục tiêu cốt lõi là Gen Z và Millennials, chiến lược cá nhân hóa (Personalization) vẫn cần có các cụm sản phẩm phù hợp với nhóm khách hàng trung niên. Các chiến dịch marketing (như giảm Churn) nên được thiết kế khác biệt cho hai nhóm tuổi này.

### 1.2 Phân Phối Giá Trị Giao Dịch (Transaction Price Distribution)

![Price Distribution](../../reports/figures/price_distribution.png)

* **Thống kê mô tả:**
  * Trung bình (Mean): ~0.0278 (Đã chuẩn hóa/ẩn danh)
  * Cao nhất (Max): 0.59

**Observation $\rightarrow$ Insight:**
* **Observation:** Hầu hết các giao dịch có giá trị nhỏ (nằm trong khoảng < 0.05). Biểu đồ phân phối lệch trái rất mạnh, chỉ một số ít giao dịch có giá trị cực cao (lên tới 0.59).
* **Insight:** Khách hàng chủ yếu mua sắm các mặt hàng thời trang giá rẻ hoặc trung bình. Do đó, các chương trình khuyến mãi mua chéo (Cross-sell) nên tập trung gợi ý các sản phẩm phụ kiện hoặc quần áo giá trị thấp để dễ dàng kích thích quyết định mua hàng (Impulse buying).

---

## 2. Phân Tích Song Biến & Chuỗi Thời Gian (Bivariate & Temporal Analysis)

### 2.1 Xu Hướng Doanh Thu Theo Thời Gian (Revenue Trend)

![Revenue Trend](../../reports/figures/revenue_trend.png)

* **Thống kê mô tả:**
  * Tháng đạt đỉnh (Peak Month): Tháng 6 năm 2019
  * Doanh thu tháng đỉnh: ~48,648

**Observation $\rightarrow$ Insight:**
* **Observation:** Doanh thu có sự biến động rõ rệt theo chu kỳ tháng/mùa. Các đợt tăng vọt thường xuất hiện vào giữa năm (khoảng tháng 6, tháng 7) tương ứng với mùa vụ Hè (Summer). 
* **Insight:** Bộ phận Merchandising & Inventory Planning (Trụ cột 3) cần đảm bảo lượng hàng hóa dồi dào vào các tháng 5 và 6 để đón đầu làn sóng mua sắm mùa hè. Các chương trình xả hàng có thể được thực hiện vào cuối mùa để dọn kho.

### 2.2 So Sánh Doanh Thu Theo Kênh Bán Hàng (Sales Channel Comparison)

![Sales Channel Comparison](../../reports/figures/sales_channel_comparison.png)

* **Thống kê mô tả:**
  * Doanh thu Kênh 1: 215,682
  * Doanh thu Kênh 2: 668,963

**Observation $\rightarrow$ Insight:**
* **Observation:** Kênh bán hàng 2 (thường giả định là Online/E-commerce) mang lại tổng doanh thu gấp hơn 3 lần so với Kênh bán hàng 1 (Offline/Store).
* **Insight:** Chiến lược số hóa (Digitalization) của H&M đang hoạt động rất hiệu quả. Việc tập trung phát triển các mô hình cá nhân hóa trên nền tảng trực tuyến sẽ mang lại tác động ROI (Return On Investment) cực kỳ lớn do tệp khách hàng mua sắm online chiếm tỷ trọng áp đảo.

---

## 3. Phân Tích Đa Biến & Tương Quan (Multivariate & Correlation)

### 3.1 Ma Trận Tương Quan Các Biến Khách Hàng (Correlation Heatmap)

![Correlation Heatmap](../../reports/figures/correlation_heatmap.png)

**Observation $\rightarrow$ Insight:**
* **Observation:** Có sự tương quan mạnh giữa `frequency` (tần suất mua sắm) và `monetary` (tổng chi tiêu). Điều này là hiển nhiên. Tuy nhiên, `recency` (số ngày từ lần cuối mua hàng) có xu hướng tương quan âm (negative correlation) với `frequency`, nghĩa là khách hàng mua càng nhiều lần thì khoảng cách từ lần mua cuối cùng của họ đến nay càng ngắn.
* **Insight:** Những khách hàng có tần suất mua cao (Champions) là nhóm dễ bị rời bỏ nhất nếu họ đột ngột ngừng mua sắm (Recency tăng cao). Mô hình dự đoán Churn cần đánh trọng số cao cho sự thay đổi đột ngột của biến `recency` ở nhóm khách hàng có `frequency` cao.

---

## 4. Deep-Dive Business Insights (Phân Tích Sâu)

### 4.1 Doanh Thu Theo Nhóm Tuổi (Revenue by Age Group)

![Revenue by Age Group](../../reports/figures/revenue_by_age.png)

**Observation $\rightarrow$ Insight:**
* **Observation:** Nhóm khách hàng từ 21-30 tuổi đóng góp doanh thu lớn nhất, theo sau là nhóm 31-40 và 41-50. Nhóm dưới 20 và trên 50 đóng góp một phần nhỏ.
* **Insight:** Phù hợp với phân phối khách hàng ban đầu, H&M là thương hiệu nhắm mạnh tới người trẻ đi làm (21-30). Các hệ thống gợi ý và chiến lược sản phẩm (Pillar 2) nên tối ưu hóa mạnh mẽ cho phân khúc tuổi này để tối đa hóa doanh thu. Tuy nhiên, vẫn cần những line hàng dành riêng cho tuổi trung niên.

### 4.2 Top 10 Nhóm Sản Phẩm Mang Lại Doanh Thu Cao Nhất (Top Categories by Revenue)

![Top 10 Categories by Revenue](../../reports/figures/top_categories_revenue.png)

**Observation $\rightarrow$ Insight:**
* **Observation:** Các mặt hàng thời trang "Garment Upper body" (Áo) và "Garment Lower body" (Quần) áp đảo hoàn toàn các danh mục khác về doanh thu. Các mặt hàng phụ kiện như Giày, Túi xách, Underwear mang lại doanh thu khiêm tốn hơn.
* **Insight:** Đóng vai trò là danh mục "hút tiền" chính, các loại quần và áo cơ bản cần được đảm bảo tồn kho ở mức cao (Pillar 3). Phụ kiện có thể dùng làm mồi nhử Cross-sell ở bước thanh toán để tăng giá trị giỏ hàng (AOV).

### 4.3 Xu Hướng Doanh Thu Kênh Bán Hàng Trực Tuyến và Ngoại Tuyến (Channel Trend over Time)

![Channel Trend over Time](../../reports/figures/channel_trend_over_time.png)

**Observation $\rightarrow$ Insight:**
* **Observation:** Biểu đồ thể hiện biến động mạnh trong giai đoạn đầu năm 2020. Đặc biệt trong quý 1 và 2 năm 2020 (vùng highlight đỏ - chịu ảnh hưởng mạnh của đại dịch COVID-19), doanh thu Offline (Kênh 1) giảm mạnh hoặc đi ngang do các đợt giãn cách xã hội (lockdowns). Kênh Online (Kênh 2) vẫn duy trì sức mua ổn định hoặc tăng tốc mạnh mẽ bù đắp cho kênh Offline.
* **Insight:** Đại dịch COVID-19 là một sự kiện thiên nga đen đã làm thay đổi mạnh mẽ thói quen mua sắm. Kênh Online (Kênh 2) đã trở thành trụ cột gánh vác doanh thu của toàn công ty, thể hiện sức đề kháng tuyệt vời trước biến động vĩ mô. Các thuật toán cá nhân hóa (Personalization - Pillar 2) cần được thiết kế ưu tiên cho trải nghiệm Web/App nhằm khai thác triệt để "bình thường mới" (New Normal) này.

---
**Kết luận:** EDA đã cung cấp cái nhìn sâu sắc vào hoạt động kinh doanh đa kênh của H&M. Tính mùa vụ và khả năng chống chịu của kênh Online trong đại dịch COVID-19 cho thấy Personalization và Inventory Planning dựa trên nền tảng số hóa (Data-driven) là vô cùng cần thiết.
