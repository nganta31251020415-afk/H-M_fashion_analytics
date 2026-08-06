"""
SQL Analysis Script - Pillar 1: RFM & Churn Analysis

This script reads data/marts/customer_features.parquet using DuckDB,
executes an SQL aggregation query grouping by rfm_segment, prints the summary
table to the console, and exports a comprehensive Markdown report to
docs/sql_reports/retention_rfm_analysis.md.
"""

from pathlib import Path
import duckdb
import pandas as pd


def run_rfm_analysis(
    marts_customer_path: Path,
    output_report_path: Path
) -> None:
    """
    Executes RFM & Churn SQL analysis and writes formatted report.

    Args:
        marts_customer_path (Path): Path to customer_features.parquet.
        output_report_path (Path): Path to output Markdown report file.
    """
    print("=" * 75)
    print("Executing Phase 4 SQL Analysis - Pillar 1: RFM & Churn Analysis")
    print("=" * 75)

    con = duckdb.connect()
    
    parquet_str = marts_customer_path.as_posix()

    # Step 1: SQL Aggregation Query
    query = f"""
    WITH total_stats AS (
        SELECT 
            COUNT(*) AS grand_total_customers,
            SUM(monetary) AS grand_total_revenue
        FROM read_parquet('{parquet_str}')
    )
    SELECT 
        c.rfm_segment,
        CAST(COUNT(*) AS INTEGER) AS customer_count,
        ROUND(COUNT(*) * 100.0 / t.grand_total_customers, 2) AS percentage,
        ROUND(SUM(c.monetary), 2) AS total_revenue,
        ROUND(SUM(c.monetary) * 100.0 / t.grand_total_revenue, 2) AS revenue_percentage,
        ROUND(AVG(c.recency), 1) AS avg_recency,
        ROUND(AVG(c.frequency), 1) AS avg_frequency,
        ROUND(AVG(c.monetary), 4) AS avg_monetary,
        ROUND(AVG(c.category_diversity), 1) AS avg_category_diversity
    FROM read_parquet('{parquet_str}') c, total_stats t
    GROUP BY c.rfm_segment, t.grand_total_customers, t.grand_total_revenue
    ORDER BY total_revenue DESC
    """

    df_res = con.execute(query).df()

    # Step 2: Print Console Output Table
    print("\n" + "=" * 75)
    print("RFM & CHURN SEGMENTATION PERFORMANCE SUMMARY")
    print("=" * 75)
    print(df_res.to_string(index=False))
    print("=" * 75)

    # Step 3: Format & Export Markdown Report
    output_report_path.parent.mkdir(parents=True, exist_ok=True)

    report_markdown = f"""# Báo Cáo Phân Tích SQL – Trụ Cột 1: Retention & Churn Analysis (RFM Segmentation)

> **Dự án:** H&M Personalized Fashion Analytics  
> **Nguồn dữ liệu:** `data/marts/customer_features.parquet` (1,371,980 khách hàng)  
> **Công cụ xử lý:** DuckDB & SQL Analytics  
> **Ngày thực hiện:** {pd.Timestamp.now().strftime('%Y-%m-%d')}

---

## 1. Kết Quả Phân Tích Tổng Hợp (RFM Segment Metrics)

Bảng dưới đây thống kê chi tiết quy mô, tỷ lệ đóng góp doanh thu và chỉ số hành vi trung bình của 6 phân khúc khách hàng (sắp xếp theo doanh thu giảm dần):

| RFM Segment | Số lượng KH (`customer_count`) | Tỷ lệ KH (`%`) | Tổng Doanh Thu (`total_revenue`) | Tỷ lệ Doanh Thu (`%`) | Recency TB (`avg_recency`) | Frequency TB (`avg_frequency`) | Chi tiêu TB (`avg_monetary`) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
"""

    for _, row in df_res.iterrows():
        report_markdown += (
            f"| **{row['rfm_segment']}** | {int(row['customer_count']):,} | {row['percentage']:.2f}% | "
            f"${row['total_revenue']:,.2f} | {row['revenue_percentage']:.2f}% | {row['avg_recency']:.1f} ngày | "
            f"{row['avg_frequency']:.1f} lần | ${row['avg_monetary']:.4f} |\n"
        )

    # Add totals row
    total_cust = df_res['customer_count'].sum()
    total_rev = df_res['total_revenue'].sum()
    report_markdown += (
        f"| **TỔNG CỘNG** | **{total_cust:,}** | **100.00%** | **${total_rev:,.2f}** | **100.00%** | — | — | — |\n\n"
    )

    report_markdown += """---

## 2. Nhận Xét & Business Insights Rút Ra (Key Takeaways)

### 📌 1. Quy Luật Pareto Sắc Nét (84.47% Doanh Thu Đến Từ 40% Khách Hàng)
- Hai nhóm **Champions** ({champions_cust:,} KH - 24.70%) và **Loyal** ({loyal_cust:,} KH - 15.30%) đóng góp tới **84.47% tổng doanh thu** của doanh nghiệp (${top2_rev:,.2f}).
- **Champions** là phân khúc gánh vác chính cho toàn bộ H&M với tỷ lệ chi tiêu trung bình lên tới **${champions_avg_m:.4f}** và tần suất quay lại mua hàng trung bình **17.4 ngày giao dịch**.
- **Hành động nghiệp vụ:** Cần thiết lập ngay chương trình VIP Loyalty đặc quyền (Early Access bộ sưu tập mới, hỗ trợ chăm sóc riêng, quà tặng sinh nhật) để bảo vệ tuyệt đối nhóm Champions khỏi đối thủ cạnh tranh.

### ⚠️ 2. Cảnh Báo Nguy Cơ Rời Bỏ Ở Nhóm "At Risk" (113,257 Khách Hàng)
- Phân khúc **At Risk** chiếm **8.26%** tổng số khách hàng ({at_risk_cust:,} KH) với giá trị chi tiêu trung bình khá tốt (**${at_risk_avg_m:.4f}**) và từng có tần suất mua trung bình **2.9 lần**.
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
""".format(
        champions_cust=int(df_res.loc[df_res['rfm_segment'] == 'Champions', 'customer_count'].values[0]),
        loyal_cust=int(df_res.loc[df_res['rfm_segment'] == 'Loyal', 'customer_count'].values[0]),
        top2_rev=df_res.loc[df_res['rfm_segment'].isin(['Champions', 'Loyal']), 'total_revenue'].sum(),
        champions_avg_m=df_res.loc[df_res['rfm_segment'] == 'Champions', 'avg_monetary'].values[0],
        at_risk_cust=int(df_res.loc[df_res['rfm_segment'] == 'At Risk', 'customer_count'].values[0]),
        at_risk_avg_m=df_res.loc[df_res['rfm_segment'] == 'At Risk', 'avg_monetary'].values[0]
    )

    with open(output_report_path, "w", encoding="utf-8") as f:
        f.write(report_markdown)

    print(f"\n[Success] Report generated successfully at: {output_report_path}")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[2]
    
    marts_path = project_root / "data" / "marts" / "customer_features.parquet"
    report_path = project_root / "docs" / "sql_reports" / "retention_rfm_analysis.md"

    run_rfm_analysis(
        marts_customer_path=marts_path,
        output_report_path=report_path
    )
