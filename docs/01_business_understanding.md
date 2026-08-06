# Business Understanding & Business Questions
## Dự án Phân tích Dữ liệu & Machine Learning – H&M Personalized Fashion Analytics

> **Phiên bản tài liệu:** v2.0  
> **Trạng thái:** Hoàn thành Cập nhật Phase 0 – Business Understanding (Mentor Feedback Aligned)

---

# 1. Mục tiêu dự án

Mục tiêu của dự án không chỉ là xây dựng các mô hình Machine Learning độc lập, mà là thực hiện một **dự án Data Analytics hoàn chỉnh theo quy trình thực tế trong doanh nghiệp bán lẻ thời trang**, từ việc thấu hiểu 3 bài toán kinh doanh trọng tâm cho đến xây dựng dashboard, phân tích dữ liệu, dự báo và đưa ra các khuyến nghị thực chiến (actionable insights).

Dự án tuân thủ toàn bộ quy trình phân tích dữ liệu chuyên nghiệp:

- **Business Understanding** (Hiểu bài toán kinh doanh theo 3 trụ cột chính)
- **Data Understanding & Data Profiling** (Tìm hiểu & đánh giá chất lượng dữ liệu)
- **Data Cleaning & Validation** (Làm sạch và kiểm định dữ liệu nghiêm ngặt)
- **Exploratory Data Analysis (EDA)** (Phân tích khám phá chuyên sâu)
- **SQL Analytics** (Truy vấn phân tích dữ liệu bằng SQL)
- **Dashboard trực quan bằng Power BI** (Thiết kế đa tab chuẩn FOXIA)
- **Machine Learning & Personalization Baseline** (Phân cụm, dự báo Churn, Basket Analysis & Demand Forecasting)
- **Storytelling & Business Recommendation** (Truyền tải insight & đề xuất hành động theo ma trận Impact/Effort)
- **Documentation & Portfolio** (Tài liệu hóa tiêu chuẩn cao)

---

# 2. Bối cảnh kinh doanh

H&M là một trong những thương hiệu bán lẻ thời trang lớn nhất thế giới, hoạt động theo mô hình **Omnichannel** (kết hợp giữa cửa hàng vật lý và kênh bán hàng trực tuyến).

Là một doanh nghiệp hoạt động trong lĩnh vực **Fast Fashion**, H&M liên tục tung ra các bộ sưu tập mới với vòng đời sản phẩm ngắn, nhu cầu mua sắm thay đổi nhanh theo mùa và xu hướng thời trang. Điều này tạo ra 3 thách thức cốt lõi:
1. Tỷ lệ giữ chân khách hàng (Retention) và nguy cơ rời bỏ (Churn) do sự cạnh tranh khốc liệt.
2. Nhu cầu cá nhân hóa trải nghiệm (Personalization) giữa hàng chục nghìn danh mục sản phẩm đa dạng.
3. Áp lực tối ưu hóa lượng hàng tồn kho (Inventory) và đưa ra quyết định nhập hàng (Merchandising) chính xác dựa trên lịch sử bán hàng.

Bộ dữ liệu của H&M chứa thông tin thực tế về:
- **Customers**: Thông tin phân vùng, độ tuổi và thói quen nhận tin.
- **Articles**: Danh mục, phân loại màu sắc, nhóm hàng thời trang.
- **Transactions**: Lịch sử giao dịch chi tiết theo thời gian và kênh bán hàng.

---

# 3. Ba Bài Toán Kinh Doanh Trọng Tâm (Core Business Pillars)

Theo định hướng tối ưu bài toán kinh doanh, dự án tập trung giải quyết **3 vấn đề trọng tâm chính**:

```
                                  ┌─────────────────────────────────────────┐
                                  │      H&M FASHION ANALYTICS CORE         │
                                  └────────────────────┬────────────────────┘
                                                       │
         ┌─────────────────────────────────────────────┼─────────────────────────────────────────────┐
         ▼                                             ▼                                             ▼
┌─────────────────────────┐               ┌─────────────────────────┐               ┌─────────────────────────┐
│       TRỤ CỘT 1         │               │       TRỤ CỘT 2         │               │       TRỤ CỘT 3         │
│  Tăng Retention & Giảm  │               │   Cá Nhân Hóa Trải      │               │   Quyết Định Nhập Hàng  │
│      Rời Bỏ (Churn)     │               │    Nghiệm Mua Sắm       │               │    Dựa Trên Dữ Liệu     │
└─────────────────────────┘               └─────────────────────────┘               └─────────────────────────┘
```

### **Trụ cột 1: Làm thế nào để tăng tỷ lệ khách hàng quay lại mua hàng và giảm tỷ lệ rời bỏ (Churn)?**
- **Mục tiêu**: Phân tích hành vi khách hàng, xác định chu kỳ quay lại (Purchase Cycle), phân đoạn khách hàng theo giá trị (RFM / CLV) và phát hiện sớm các dấu hiệu rủi ro rời bỏ để có chiến lược giữ chân phù hợp.

### **Trụ cột 2: Làm thế nào để cá nhân hóa trải nghiệm mua sắm?**
- **Mục tiêu**: Hiểu rõ sở thích cá nhân và hành vi mua kèm (Co-purchasing), ứng dụng Market Basket Analysis và mô hình gợi ý sản phẩm (Recommendation Engine) nhằm đề xuất đúng sản phẩm cho đúng phân khúc khách hàng vào đúng thời điểm.

### **Trụ cột 3: Làm thế nào để đưa ra quyết định nhập hàng dựa trên dữ liệu lịch sử?**
- **Mục tiêu**: Phân tích xu hướng tiêu dùng theo mùa, chu kỳ sống của dòng sản phẩm (Product Lifecycle) và xây dựng mô hình dự báo nhu cầu (Demand Forecasting) để tối ưu hóa danh mục và số lượng nhập hàng cho mùa tiếp theo.

---

# 4. Stakeholder & Nhu cầu phân tích

| Stakeholder | Trụ cột liên quan | Nhu cầu kinh doanh cốt lõi |
|-------------|-------------------|----------------------------|
| **CMO / Marketing Team** | Trụ cột 1 & 2 | Hiểu rõ phân khúc khách hàng (RFM), giảm tỷ lệ Churn, triển khai các chiến dịch Remarketing & Personalization tối ưu ngân sách. |
| **Merchandising / Category Manager** | Trụ cột 3 | Xác định danh mục/mặt hàng bán chạy, đánh giá tốc độ quay vòng sản phẩm và đưa ra quyết định nhập hàng (Buying & Re-ordering). |
| **Supply Chain / Demand Planning** | Trụ cột 3 | Dự báo nhu cầu theo danh mục/thời gian nhằm giảm tồn kho quá mức (Overstock) hoặc thiếu hàng (Stock-out). |
| **E-commerce / Product Team** | Trụ cột 2 | Cá nhân hóa hiển thị sản phẩm mua kèm (Cross-sell / Up-sell), tăng tỷ lệ chuyển đổi (Conversion Rate) và giá trị đơn hàng (AOV). |
| **Ban lãnh đạo (Executive/C-Level)** | Cả 3 Trụ cột | Theo dõi sức khỏe doanh nghiệp tổng quan qua Dashboard Power BI với các chỉ số Retention Rate, AOV, Sales Growth và Churn Rate. |

---

# 5. Các KPI quan trọng theo 3 Trụ Cột

Các chỉ số KPI dưới đây được thiết kế phục vụ trực tiếp 3 trụ cột kinh doanh:

## Trụ cột 1: Retention & Churn KPIs
- **Repeat Purchase Rate (RPR)**: Tỷ lệ khách hàng mua từ 2 lần trở lên.
- **Customer Churn Rate**: Tỷ lệ khách hàng không phát sinh giao dịch sau khoảng thời gian ngưỡng (ví dụ: 90 ngày / 180 ngày).
- **Customer Lifetime Value (CLV)**: Giá trị vòng đời trung bình theo từng phân khúc.
- **Recency, Frequency, Monetary (RFM Metrics)**: Điểm số phân hạng khách hàng.
- **Cohort Retention Rate**: Tỷ lệ giữ chân khách hàng theo các nhóm gia nhập theo tháng.

## Trụ cột 2: Personalization & Cross-Sell KPIs
- **Average Order Value (AOV)**: Giá trị trung bình mỗi đơn hàng.
- **Items Per Order (Basket Size)**: Số lượng sản phẩm trung bình trên một đơn hàng.
- **Support, Confidence, Lift**: Chỉ số đánh giá độ mạnh của luật kết hợp sản phẩm (Market Basket Rules).
- **Segment Product Preference Index**: Mức độ ưu thích danh mục theo độ tuổi/phân khúc.

## Trụ cột 3: Merchandising & Demand KPIs
- **Total Revenue & Revenue Growth Rate**: Doanh thu tổng và tốc độ tăng trưởng MoM/YoY.
- **Category / Product Velocity**: Tốc độ bán chạy lẻ của từng mã hàng.
- **Forecasted Demand vs Actual Sales**: Nhu cầu dự báo so với thực tế.
- **Seasonality Index**: Chỉ số biến động nhu cầu theo mùa trong năm.

---

# 6. Tiêu chí đánh giá thành công của dự án

Dự án đạt tiêu chuẩn thành công khi hoàn thành các mục tiêu sau:

1. **Về Business**: Giải quyết trọn vẹn 3 câu hỏi kinh doanh trọng tâm của mentor và đưa ra đề xuất hành động cụ thể theo ma trận Impact vs Effort.
2. **Về Analytics & SQL**: Xây dựng pipeline truy vấn SQL và EDA sạch vẽ ra bức tranh toàn cảnh về Retention, Basket Pattern và Category Performance.
3. **Về Power BI Dashboard**: Thiết kế Dashboard đa tab chuẩn phong cách FOXIA (Overview, Customer Analytics, Product/Inventory Analytics, Diagnostic Deep-dive).
4. **Về Machine Learning**: Xây dựng thành công 4 mô hình/thuật toán tương ứng với 3 trụ cột (RFM Segmentation, Churn Classifier, Market Basket Recommendation Engine, Demand Forecasting).
5. **Về Portfolio & Quality**: Mã nguồn sạch, tài liệu chuyên nghiệp, có khả năng tái lập và giải thích rõ góc nhìn business.

---

# 7. Các câu hỏi kinh doanh chi tiết (Re-organized by 3 Pillars)

Toàn bộ 18 câu hỏi phân tích được sắp xếp lại theo 3 trụ cột chính:

### Nhóm 1: Tăng Retention & Giảm Churn (Phân tích Khách hàng)
1. Tỷ lệ khách hàng quay lại mua hàng (Repeat Purchase Rate) hiện tại là bao nhiêu và biến động như thế nào theo thời gian?
2. Phân khúc khách hàng nào (theo phân tích RFM) đóng góp nhiều doanh thu nhất?
3. Nhóm khách hàng nào đang có nguy cơ rời bỏ (Churn Risk) cao nhất dựa trên chỉ số Recency và Frequency?
4. Khách hàng mới (New Customers) và khách hàng cũ (Returning Customers) đóng góp doanh thu như thế nào?
5. Giá trị vòng đời khách hàng (CLV) trung bình của từng nhóm tuổi và phân khúc là bao nhiêu?
6. Nguyên lý Pareto (20% khách hàng đóng góp 80% doanh thu) có đúng với tập dữ liệu H&M không?

### Nhóm 2: Cá nhân hóa trải nghiệm mua sắm (Personalization & Basket Analytics)
7. Những cặp hoặc bộ sản phẩm/danh mục nào thường được khách hàng mua cùng nhau trong một giao dịch (Market Basket Analysis)?
8. Độ tuổi và phân khúc khách hàng khác nhau có sở thích về nhóm hàng, màu sắc hay phong cách thời trang khác nhau như thế nào?
9. Dựa trên lịch sử mua sắm gần nhất, sản phẩm tiếp theo (Next Best Item) nào nên được khuyến nghị cho từng phân khúc?
10. Hành vi mua sắm và giá trị giỏ hàng (Basket Size / AOV) giữa kênh online và cửa hàng vật lý có sự khác biệt gì?
11. Tỷ lệ mua lặp lại trên cùng một dòng sản phẩm (Category Loyalty) là bao nhiêu?

### Nhóm 3: Quyết định nhập hàng dựa trên dữ liệu lịch sử (Merchandising & Demand)
12. Những danh mục (Category) và sản phẩm (Article) nào mang lại doanh thu và sản lượng cao nhất trong lịch sử?
13. Xu hướng doanh thu và sản lượng bán thay đổi như thế nào theo tháng, theo mùa (Spring/Summer vs Autumn/Winter)?
14. Chu kỳ bán (Product Lifecycle) của các sản phẩm mốt thời trang kéo dài trong bao lâu trước khi suy giảm doanh số?
15. Những mặt hàng/danh mục nào có tốc độ tăng trưởng nhanh nhất và nên được ưu tiên nhập hàng cho mùa tiếp theo?
16. Nhu cầu tiêu thụ (Demand) của từng danh mục chính trong 1 - 3 tháng tới dự báo sẽ là bao nhiêu?
17. Ngày nào trong tuần và thời điểm nào trong tháng phát sinh nhu cầu mua sắm đỉnh điểm?
18. Cơ cấu sản phẩm (Product Mix) hiện tại đã tối ưu giữa dòng hàng mặc hàng ngày (Basics) và dòng hàng thời trang xu hướng (Trend Items) chưa?

---

# 8. Kế hoạch ứng dụng Machine Learning & Analytics Baseline

Machine Learning được xây dựng để phục vụ trực tiếp 3 trụ cột kinh doanh:

| STT | Mô hình / Thuật toán | Trụ cột phục vụ | Thuật toán dự kiến | Giá trị kinh doanh mang lại |
|:---:|----------------------|-----------------|--------------------|-----------------------------|
| **1** | **Customer Segmentation (RFM + K-Means)** | Trụ cột 1 & 2 | RFM Scoring, K-Means Clustering | Phân nhóm khách hàng thành các Segment (VIP, Loyal, At-Risk, Hibernating) để tối ưu chiến dịch giữ chân. |
| **2** | **Customer Churn & Repeat Purchase Model** | Trụ cột 1 | Logistic Regression, Random Forest, XGBoost / LightGBM | Dự đoán xác suất một khách hàng sẽ rời bỏ hoặc quay lại mua hàng trong 90 ngày tới. |
| **3** | **Market Basket & Recommendation Baseline** | Trụ cột 2 | Apriori / FP-Growth, Item-based Collaborative Filtering | Xây dựng các luật kết hợp mua hàng (Association Rules) và engine gợi ý sản phẩm tiếp theo cho từng phân khúc. |
| **4** | **Category Sales & Demand Forecasting** | Trụ cột 3 | Prophet / ARIMA, LightGBM Time-Series Regression | Dự báo doanh số và sản lượng theo danh mục cho 1 - 3 tháng tới phục vụ kế hoạch nhập hàng. |

---

# 9. Phạm vi dự án (Project Scope)

Dự án tập trung vào:
- **Exploratory Data Analysis (EDA)** & **SQL Analytics** sâu rộng.
- **Power BI Dashboard** thiết kế đa tab chuẩn FOXIA (Overview, Customer Analytics, Product/Inventory Analytics, Diagnostic Deep-dive).
- **Customer Segmentation** (RFM & K-Means).
- **Customer Churn Prediction** (Supervised Binary Classification).
- **Personalization Baseline** (Market Basket Analysis & Segment-Based Recommender).
- **Demand Forecasting** (Time-series forecasting cho Category Sales).
- **Business Recommendations** (Chiến lược giữ chân, gợi ý nhập hàng và cá nhân hóa).

---

# 10. Khống chế phạm vi (Out of Scope)

Các nội dung dưới đây nằm **ngoài phạm vi triển khai** để giữ dự án tập trung vào Data Analytics & Business Value:
- Xây dựng hệ thống Recommendation công nghiệp phức tạp thời gian thực (Real-time Candidate Generation, Vector Search, Deep Learning Recommender).
- Xử lý hình ảnh sản phẩm bằng Computer Vision (CNN/ResNet).
- Hạ tầng MLOps phức tạp, Kubeflow hay Docker Kubernetes Orchestration.
- Phân tích dữ liệu luồng Real-time Streaming (Kafka/Spark Streaming).

---

# 11. Nguyên tắc thực hiện dự án

- **Business-First**: Mọi phân tích, biểu đồ và mô hình ML đều phải bắt đầu từ và phục vụ cho 1 trong 3 trụ cột kinh doanh.
- **Empirical Rigor**: Luôn kiểm định chất lượng dữ liệu trước khi rút ra kết luận.
- **FOXIA Standard Dashboard**: Thiết kế Dashboard theo tư duy 5 tầng, rõ ràng, trực quan, hỗ trợ ra quyết định.
- **Actionable Insights**: Mỗi phát hiện đều phải đi kèm khuyến nghị cụ thể (What → Why → What to do).