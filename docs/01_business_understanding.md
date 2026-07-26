# Business Understanding & Business Questions
## Dự án Phân tích Dữ liệu & Machine Learning – H&M Personalized Fashion Analytics

> **Phiên bản tài liệu:** v1.0  
> **Trạng thái:** Hoàn thành Phase 0 – Business Understanding

---

# 1. Mục tiêu dự án

Mục tiêu của dự án không chỉ là xây dựng các mô hình Machine Learning, mà là thực hiện một **dự án Data Analytics hoàn chỉnh theo quy trình thực tế trong doanh nghiệp**, từ việc hiểu bài toán kinh doanh cho đến xây dựng dashboard, phân tích dữ liệu, dự báo và đưa ra các khuyến nghị phục vụ việc ra quyết định.

Dự án sẽ bao gồm toàn bộ quy trình phân tích dữ liệu:

- Business Understanding (Hiểu bài toán kinh doanh)
- Data Understanding (Tìm hiểu dữ liệu)
- Data Cleaning & Validation (Làm sạch và kiểm định dữ liệu)
- Exploratory Data Analysis (EDA)
- SQL Analytics
- Dashboard trực quan bằng Power BI
- Machine Learning
- Storytelling & Business Recommendation
- Documentation & Portfolio

Trong quá trình thực hiện, các công cụ AI như ChatGPT, Claude, Codex và Antigravity IDE sẽ được sử dụng để hỗ trợ lập trình, tối ưu quy trình và tăng tốc độ phát triển. Tuy nhiên, mọi quyết định về business, phân tích dữ liệu, lựa chọn mô hình và diễn giải kết quả đều sẽ được người thực hiện kiểm tra, đánh giá và chịu trách nhiệm.

---

# 2. Bối cảnh kinh doanh

H&M là một trong những thương hiệu bán lẻ thời trang lớn nhất thế giới, hoạt động theo mô hình **Omnichannel** (kết hợp giữa cửa hàng vật lý và kênh bán hàng trực tuyến).

Là một doanh nghiệp hoạt động trong lĩnh vực **Fast Fashion**, H&M liên tục tung ra các bộ sưu tập mới với vòng đời sản phẩm ngắn, nhu cầu mua sắm thay đổi nhanh theo mùa và xu hướng thời trang. Điều này khiến việc phân tích hành vi khách hàng, quản lý tồn kho và dự báo nhu cầu trở thành những bài toán rất quan trọng.

Bộ dữ liệu của H&M mô phỏng khá sát môi trường kinh doanh thực tế khi bao gồm:

- Thông tin khách hàng
- Danh mục sản phẩm
- Lịch sử giao dịch

Đây là nền tảng phù hợp để thực hiện một dự án Retail Data Analytics hoàn chỉnh và xây dựng các mô hình Machine Learning phục vụ hoạt động kinh doanh.

---

# 3. Bài toán kinh doanh

Dự án hướng tới việc giải quyết các bài toán kinh doanh thường gặp trong ngành bán lẻ thời trang:

- Làm thế nào để tăng doanh thu trên mỗi khách hàng?
- Làm thế nào để tăng tỷ lệ khách hàng quay lại mua hàng và giảm tỷ lệ rời bỏ (Churn)?
- Làm thế nào để dự báo nhu cầu nhằm hỗ trợ quản lý tồn kho?
- Làm thế nào để tối ưu ngân sách marketing bằng cách tập trung vào nhóm khách hàng có giá trị cao?
- Làm thế nào để cá nhân hóa trải nghiệm mua sắm?
- Làm thế nào để đưa ra quyết định nhập hàng dựa trên dữ liệu lịch sử?

---

# 4. Stakeholder

Mặc dù đây là dự án cá nhân, toàn bộ quá trình phân tích sẽ được xây dựng như một dự án thực tế trong doanh nghiệp với nhiều nhóm người sử dụng kết quả khác nhau.

| Stakeholder | Nhu cầu |
|-------------|---------|
| **CMO / Marketing Team** | Hiểu rõ phân khúc khách hàng, tối ưu chiến dịch marketing, tăng tỷ lệ giữ chân khách hàng và nâng cao hiệu quả ngân sách marketing. |
| **Merchandising / Category Manager** | Xác định sản phẩm và danh mục bán chạy, theo dõi xu hướng tiêu dùng và hỗ trợ quyết định nhập hàng. |
| **Supply Chain / Demand Planning** | Dự báo nhu cầu theo thời gian nhằm hạn chế tình trạng thiếu hàng hoặc tồn kho quá nhiều. |
| **E-commerce / Product Team** | Hiểu hành vi mua sắm, cải thiện trải nghiệm người dùng và tăng tỷ lệ chuyển đổi trên website hoặc ứng dụng. |
| **Ban lãnh đạo (Executive/C-Level)** | Theo dõi tình hình kinh doanh thông qua dashboard tổng quan và các KPI quan trọng để hỗ trợ ra quyết định chiến lược. |

---

# 5. Các KPI quan trọng

Các KPI dưới đây sẽ được sử dụng xuyên suốt quá trình phân tích, trực quan hóa và đánh giá kết quả.

## Doanh thu

- Tổng doanh thu
- Doanh thu theo tháng
- Tốc độ tăng trưởng doanh thu
- Doanh thu theo danh mục sản phẩm
- Doanh thu theo phân khúc khách hàng

## Khách hàng

- Số lượng khách hàng đang hoạt động
- Tỷ lệ khách hàng quay lại mua hàng (Repeat Purchase Rate)
- Tỷ lệ giữ chân khách hàng (Retention Rate)
- Giá trị vòng đời khách hàng (Customer Lifetime Value - CLV)
- Tần suất mua hàng
- Giá trị trung bình mỗi đơn hàng (Average Order Value - AOV)
- Tỷ lệ khách hàng mới và khách hàng cũ

## Sản phẩm

- Sản phẩm bán chạy nhất
- Danh mục bán chạy nhất
- Tốc độ tăng trưởng của từng danh mục
- Hiệu suất bán hàng theo mùa

## Dự báo

- Dự báo doanh số theo danh mục
- Dự báo khả năng khách hàng quay lại mua hàng
- Dự báo xu hướng doanh thu

---

# 6. Tiêu chí đánh giá thành công của dự án

Dự án được xem là thành công khi đạt được các mục tiêu sau.

## Về Business

- Trả lời đầy đủ các câu hỏi kinh doanh đã đặt ra.
- Đưa ra các khuyến nghị có thể áp dụng trong thực tế.

## Về Analytics

- Xây dựng được pipeline phân tích dữ liệu hoàn chỉnh từ dữ liệu thô đến insight.
- Trực quan hóa dữ liệu rõ ràng, dễ hiểu.
- Storytelling logic và có tính thuyết phục.

## Về Machine Learning

- Xây dựng tối thiểu hai mô hình Machine Learning phục vụ bài toán kinh doanh.
- Đánh giá mô hình bằng các chỉ số phù hợp.
- Giải thích kết quả mô hình theo góc nhìn kinh doanh thay vì chỉ trình bày chỉ số kỹ thuật.

## Về Portfolio

- Repository GitHub được tổ chức khoa học.
- Tài liệu đầy đủ.
- Quy trình có thể tái lập.
- Dashboard Power BI trực quan.
- Có thể trình bày toàn bộ dự án như một case study thực tế.

---

# 7. Các câu hỏi kinh doanh

Toàn bộ quá trình phân tích sẽ xoay quanh việc trả lời các câu hỏi dưới đây. Các câu hỏi sẽ được giải quyết bằng SQL, EDA, Dashboard hoặc Machine Learning tùy từng giai đoạn.

## Phân tích sản phẩm

1. Những sản phẩm nào mang lại doanh thu cao nhất?
2. Danh mục sản phẩm nào tăng trưởng tốt nhất theo thời gian?
3. Màu sắc hoặc loại sản phẩm nào được ưa chuộng theo từng mùa?
4. Những sản phẩm nào có vòng đời bán ngắn nhất?
5. Những sản phẩm nào thường được mua cùng nhau?

## Phân tích khách hàng

6. Phân khúc khách hàng nào đóng góp nhiều doanh thu nhất?
7. Tỷ lệ khách hàng quay lại mua hàng của từng phân khúc là bao nhiêu?
8. Khách hàng mới và khách hàng cũ đóng góp doanh thu như thế nào?
9. Nhóm tuổi nào có mức chi tiêu cao nhất?
10. Có nhóm khách hàng nào đang có dấu hiệu rời bỏ hay không?

## Phân tích theo thời gian

11. Doanh thu thay đổi như thế nào theo tháng và theo mùa?
12. Ngày nào trong tuần có doanh thu cao nhất?
13. Xu hướng doanh thu trong dài hạn như thế nào?

## Phân tích theo kênh bán

14. Hành vi mua sắm giữa kênh online và cửa hàng có gì khác nhau?
15. Kênh bán nào tạo ra nhiều khách hàng có giá trị cao hơn?

## Góc nhìn quản trị

16. Giá trị vòng đời khách hàng trung bình của từng phân khúc là bao nhiêu?
17. 20% khách hàng có tạo ra khoảng 80% doanh thu theo nguyên lý Pareto hay không?
18. Danh mục sản phẩm nào nên được ưu tiên nhập hàng trong mùa tiếp theo?

---

# 8. Kế hoạch ứng dụng Machine Learning

Machine Learning chỉ được triển khai sau khi hoàn thành các bước làm sạch dữ liệu, kiểm định dữ liệu và phân tích khám phá.

Các mô hình dự kiến bao gồm:

## Customer Segmentation

- Phân tích RFM
- Phân cụm khách hàng bằng K-Means

**Giá trị mang lại**

- Xác định nhóm khách hàng có giá trị cao.
- Hỗ trợ Marketing triển khai các chiến dịch phù hợp với từng nhóm khách hàng.

---

## Purchase Prediction

Dự đoán khả năng khách hàng sẽ tiếp tục mua hàng trong tương lai.

**Giá trị mang lại**

- Hỗ trợ giữ chân khách hàng.
- Xây dựng các chương trình chăm sóc khách hàng phù hợp.

---

## Category Sales Forecasting

Dự báo doanh số của từng danh mục sản phẩm.

**Giá trị mang lại**

- Hỗ trợ lập kế hoạch nhập hàng.
- Giảm tồn kho và hạn chế thiếu hàng.

---

## Revenue Forecasting

Dự báo doanh thu trong tương lai.

**Giá trị mang lại**

- Hỗ trợ lập kế hoạch kinh doanh.
- Hỗ trợ ban lãnh đạo đưa ra mục tiêu doanh thu.

---

# 9. Phạm vi dự án

Dự án tập trung vào:

- Retail Data Analytics
- Data Cleaning & Validation
- SQL Analytics
- Exploratory Data Analysis (EDA)
- Dashboard bằng Power BI
- Customer Segmentation
- Purchase Prediction
- Category Sales Forecasting
- Revenue Forecasting
- Business Storytelling

Mục tiêu là xây dựng một dự án phân tích dữ liệu hoàn chỉnh theo quy trình doanh nghiệp thực tế.

---

# 10. Ngoài phạm vi dự án

Các nội dung dưới đây sẽ **không thực hiện** trong phạm vi dự án:

- Recommendation System hoàn chỉnh (Candidate Generation, ANN Search, Ranking...)
- Xử lý ảnh sản phẩm bằng Computer Vision
- Deep Learning trên dữ liệu hình ảnh
- Phân tích dữ liệu thời gian thực (Real-time Analytics)
- Triển khai Production, API hoặc MLOps

Lý do là các nội dung trên làm tăng đáng kể độ phức tạp của dự án nhưng không mang lại nhiều giá trị đối với mục tiêu chính là Data Analytics và Business Intelligence.

---

# 11. Nguyên tắc thực hiện dự án

Trong suốt quá trình thực hiện, dự án sẽ tuân theo các nguyên tắc sau:

- Luôn bắt đầu từ bài toán kinh doanh trước khi lựa chọn giải pháp kỹ thuật.
- Phân tích dữ liệu trước khi xây dựng Machine Learning.
- Mỗi dashboard đều phải trả lời ít nhất một câu hỏi kinh doanh.
- Mỗi mô hình Machine Learning đều phải phục vụ một mục tiêu kinh doanh cụ thể.
- Chú trọng khả năng tái lập, chất lượng code và tài liệu bên cạnh hiệu quả mô hình.
- AI chỉ đóng vai trò là công cụ hỗ trợ phát triển, không thay thế tư duy phân tích và ra quyết định.