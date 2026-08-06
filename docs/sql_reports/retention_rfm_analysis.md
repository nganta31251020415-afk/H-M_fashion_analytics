# Báo Cáo Phân Tích SQL – Trụ Cột 1: Retention & Churn Analysis (RFM Segmentation)

> **Dự án:** H&M Personalized Fashion Analytics  
> **Nguồn dữ liệu:** `data/marts/customer_features.parquet` (1,371,980 khách hàng)  
> **Công cụ xử lý:** DuckDB & SQL Analytics  
> **Ngày thực hiện:** 2026-08-05

---

## 1. Kết Quả Phân Tích Tổng Hợp (RFM Segment Metrics)

Bảng dưới đây thống kê chi tiết quy mô, tỷ lệ đóng góp doanh thu và chỉ số hành vi trung bình của 6 phân khúc khách hàng (sắp xếp theo doanh thu giảm dần):

| RFM Segment | Số lượng KH (`customer_count`) | Tỷ lệ KH (`%`) | Tổng Doanh Thu (`total_revenue`) | Tỷ lệ Doanh Thu (`%`) | Recency TB (`avg_recency`) | Frequency TB (`avg_frequency`) | Chi tiêu TB (`avg_monetary`) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Champions** | 338,811 | 24.70% | $589,070.60 | 66.59% | 35.5 ngày | 17.4 lần | $1.7386 |
| **Loyal** | 209,981 | 15.30% | $158,161.50 | 17.88% | 186.1 ngày | 8.3 lần | $0.7532 |
| **Others** | 322,433 | 23.50% | $64,194.26 | 7.26% | 106.7 ngày | 2.0 lần | $0.1991 |
| **Lost** | 373,606 | 27.23% | $40,293.69 | 4.55% | 515.4 ngày | 1.1 lần | $0.1079 |
| **At Risk** | 113,257 | 8.26% | $31,639.68 | 3.58% | 427.6 ngày | 2.9 lần | $0.2794 |
| **New Customers** | 13,892 | 1.01% | $1,286.24 | 0.15% | 70.0 ngày | 1.0 lần | $0.0926 |
| **TỔNG CỘNG** | **1,371,980** | **100.00%** | **$884,645.97** | **100.00%** | — | — | — |

---

## 2. Nhận Xét & Business Insights Rút Ra (Key Takeaways)

### 📌 1. Quy Luật Pareto Sắc Nét (84.47% Doanh Thu Đến Từ 40% Khách Hàng)
- Hai nhóm **Champions** (338,811 KH - 24.70%) và **Loyal** (209,981 KH - 15.30%) đóng góp tới **84.47% tổng doanh thu** của doanh nghiệp ($747,232.10).
- **Champions** là phân khúc gánh vác chính cho toàn bộ H&M với tỷ lệ chi tiêu trung bình lên tới **$1.7386** và tần suất quay lại mua hàng trung bình **17.4 ngày giao dịch**.
- **Hành động nghiệp vụ:** Cần thiết lập ngay chương trình VIP Loyalty đặc quyền (Early Access bộ sưu tập mới, hỗ trợ chăm sóc riêng, quà tặng sinh nhật) để bảo vệ tuyệt đối nhóm Champions khỏi đối thủ cạnh tranh.

### ⚠️ 2. Cảnh Báo Nguy Cơ Rời Bỏ Ở Nhóm "At Risk" (113,257 Khách Hàng)
- Phân khúc **At Risk** chiếm **8.26%** tổng số khách hàng (113,257 KH) với giá trị chi tiêu trung bình khá tốt (**$0.2794**) và từng có tần suất mua trung bình **2.9 lần**.
- Tuy nhiên, thời gian không quay lại mua hàng của nhóm này đã kéo dài trung bình **427.6 ngày (~14 tháng)**. Đây là nhóm khách hàng trung thành cũ đang dần rơi vào trạng thái ngủ đông và rời bỏ thương hiệu.
- **Hành động nghiệp vụ (Chiến dịch Win-Back):** 
  - Triển khai chiến dịch Remarketing tự động qua Email/App Notification với voucher giảm giá hấp dẫn (ví dụ: *"We miss you - Giảm 20% cho đơn hàng tiếp theo"*).
  - Kết hợp Recommender Engine để gợi ý các sản phẩm thuộc danh mục yêu thích trước đây của họ.

### 🚪 3. Tỷ Lệ Rời Bỏ Tích Lũy Cao Ở Nhóm "Lost" (373,606 Khách Hàng - 27.23%)
- Phân khúc **Lost** chiếm tỷ trọng khách hàng lớn nhất trong toàn bộ cơ sở dữ liệu (**27.23%**), với thời gian im lặng trung bình lên tới **515.4 ngày (> 1.4 năm)** và tần suất mua trung bình chỉ **1.1 lần**.
- **Hành động nghiệp vụ:** Tối ưu hóa chi phí Marketing bằng cách cắt giảm ngân sách quảng cáo trả phí (Paid Ads) nhắm tới nhóm này. Chuyển sang các kênh remarketing chi phí thấp (Automation Email) và tập trung ngân sách cho nhóm At Risk & Champions.

### 🆕 4. Cơ Hội Chuyển Đổi Nhóm "New Customers" (13,892 Khách Hàng)
- Khách hàng mới có Recency trung bình **70.0 ngày** nhưng tần suất mua mới chỉ dừng ở **1.0 lần**.
- **Hành động nghiệp vụ (Onboarding Series):** Gửi chuỗi tin nhắn chào mừng và gợi ý các sản phẩm mua kèm (Cross-sell/Up-sell) trong vòng 30-45 ngày đầu tiên để kích hoạt đơn hàng thứ 2, đưa họ chuyển dịch lên nhóm Loyal/Champions.

---

## 3. Khuyến Nghị Chiến Lược Cho Bài Toán Giảm Churn (Actionable Recommendations)

| Thứ tự ưu tiên | Phân khúc mục tiêu | Hành động đề xuất | Mục tiêu KPI |
|:---:|:---|:---|:---|
| **Ưu tiên 1** | **Champions** | Giữ chân bằng đặc quyền VIP, ưu đãi cá nhân hóa và CSKH riêng. | Duy trì Retention Rate > 90% |
| **Ưu tiên 2** | **At Risk** | Khôi phục bằng chiến dịch Win-back (Voucher 15-20% + Recommender). | Keo kéo 15-20% khách quay lại |
| **Ưu tiên 3** | **New Customers** | Nudge mua đơn thứ 2 trong 30-45 ngày bằng voucher đơn tiếp theo. | Tăng tỷ lệ mua lặp (RPR) > 35% |
| **Ưu tiên 4** | **Lost** | Tự động hóa Email Win-back chi phí thấp, tránh phung phí ad spend. | Tối ưu chi phí CAC |
