# 🛍️ Dự án Phân tích Dữ liệu H&M: Giải pháp Data & Machine Learning Toàn diện

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-Fast%20SQL-yellow?style=for-the-badge&logo=duckdb&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Statsmodels](https://img.shields.io/badge/Statsmodels-Time%20Series-green?style=for-the-badge)

---

## 📖 Tổng quan Dự án (Project Overview)

Chào mừng đến với kho lưu trữ **Phân tích Dữ liệu H&M**! Đây là **Dự án Danh mục Phân tích Dữ liệu Toàn diện định hướng Kinh doanh (Business-Driven End-to-End Data Analytics Portfolio Project)** được thiết kế để mô phỏng môi trường Bán lẻ & Thương mại Điện tử thực tế.

Sử dụng tập dữ liệu khổng lồ về các giao dịch, sản phẩm và siêu dữ liệu của khách hàng H&M, dự án này thể hiện một vòng đời dữ liệu hoàn chỉnh: bắt đầu từ quá trình **Xử lý dữ liệu SQL (Data Wrangling)**, chuyển sang **Phân tích Khám phá Dữ liệu (EDA)** và kết thúc bằng **các mô hình Học máy (Machine Learning)** có tính ứng dụng cao. Mục tiêu tối thượng là thu hẹp khoảng cách giữa dữ liệu thô và chiến lược kinh doanh của Ban lãnh đạo.

---

## 🎯 Các Trụ cột Kinh doanh Cốt lõi (Core Business Pillars)

Những nỗ lực phân tích và mô hình hóa của dự án hoàn toàn bám sát vào việc giải quyết 3 thách thức lớn của ngành bán lẻ:

1. **Giữ chân Khách hàng & Rời bỏ (Trụ cột 1):** Phân khúc tệp khách hàng để xác định nhóm VIP và nhóm có nguy cơ rời bỏ, hỗ trợ triển khai các chiến dịch marketing mục tiêu.
2. **Cá nhân hóa & Gợi ý sản phẩm (Trụ cột 2):** Xây dựng hệ thống gợi ý chuyên biệt cho khách hàng giá trị cao nhằm tăng Giá trị đơn hàng trung bình (AOV) và Tỷ lệ chuyển đổi.
3. **Dự báo Nhu cầu Tồn kho (Trụ cột 3):** Dự báo khối lượng bán hàng trong tương lai cho các danh mục bán chạy nhất để ngăn ngừa tình trạng hết hàng và giảm thiểu lượng tồn kho quá mức.

---

## 📂 Cấu trúc Kho lưu trữ (Repository Structure)

Kho lưu trữ được tổ chức tuân theo các tiêu chuẩn tốt nhất của Data Engineering và Data Science:

```text
hm-fashion-analytics/
├── data/               # Dữ liệu thô, dữ liệu trung gian và dữ liệu đã xử lý (Parquet/CSV)
├── docs/               # Tài liệu Markdown, từ điển dữ liệu và Báo cáo Kinh doanh cuối cùng
├── models/             # Các mô hình ML và Scaler đã lưu (pkl)
├── notebooks/          # Jupyter Notebooks cho EDA và các luồng ML (01 đến 04)
├── reports/            # Hình ảnh, biểu đồ và báo cáo tóm tắt
├── src/                # Mã nguồn Python (làm sạch dữ liệu, truy vấn SQL, vẽ biểu đồ)
├── tests/              # Unit test để kiểm tra tính toàn vẹn của dữ liệu
├── venv/               # Môi trường ảo Python (Virtual Environment)
├── PROJECT_CONTEXT.md  # Yêu cầu dự án chi tiết ban đầu
└── README.md           # Bạn đang xem tệp này!
```

---

## 🚀 Thông tin chuyên sâu & Mô hình Học Máy (Key Insights & ML Models)

### 💡 Thông tin Kinh doanh (Business Insights - EDA)
- **Nhân khẩu học:** Thế hệ Gen Z và Millennials (độ tuổi 21-30) là nhóm mang lại nguồn doanh thu chủ đạo nhất.
- **Sản phẩm chủ lực (Cash Cows):** Danh mục **"Garment Upper body"** (Quần áo phần trên) thống trị doanh số ở mọi phân khúc.
- **Hiệu suất Kênh bán:** Kênh **Online** vượt trội hoàn toàn so với doanh số Offline, xu hướng này càng được minh chứng rõ rệt và củng cố bền vững trong đại dịch COVID-19.

### 🧠 Các giải pháp Học Máy (Machine Learning Implementations)
1. **Phân khúc khách hàng (K-Means Clustering):** 
   - Áp dụng phân tích RFM (Recency, Frequency, Monetary).
   - Xác định 5 cụm chiến lược: *Champions (VIP), Loyal (Trung thành), Promising (Tiềm năng), At Risk (Nguy cơ rời bỏ), Lost (Đã mất)*.
2. **Hệ thống Gợi ý 2 lớp (2-Stage Recommender Engine):**
   - **Giai đoạn 1 (Popularity Baseline):** Giải quyết vấn đề "cold-start" (người dùng mới) bằng cách gợi ý các sản phẩm đang thịnh hành.
   - **Giai đoạn 2 (Item-based Collaborative Filtering):** Sử dụng TruncatedSVD và Cosine Similarity để tìm quy luật mua kèm (co-purchasing), tập trung vào các nhóm khách hàng giá trị cao.
3. **Dự báo Chuỗi thời gian (Holt-Winters):**
   - Xây dựng mô hình Làm trơn Hàm mũ (Exponential Smoothing) tích hợp xu hướng (trend) và tính mùa vụ (seasonality).
   - Dự báo nhu cầu hàng tuần cho danh mục bán chạy nhất "Garment Upper body".

---

## 🛠️ Công nghệ sử dụng (Tech Stack)

- **Xử lý Dữ liệu & SQL:** DuckDB, Pandas, Numpy, PyArrow (Parquet)
- **Machine Learning & Thống kê:** Scikit-Learn, Statsmodels, SciPy
- **Trực quan hóa Dữ liệu:** Matplotlib, Seaborn
- **Môi trường lập trình:** Python 3.8+, Jupyter Notebook, VS Code

---

## 📥 Tải Dữ liệu (Data Acquisition)

Do tập dữ liệu gốc rất lớn, các file dữ liệu thô không được lưu trữ trực tiếp trên GitHub này. Để chạy được dự án, bạn cần tải dữ liệu trực tiếp từ Kaggle:

1. Truy cập cuộc thi trên Kaggle: [H&M Personalized Fashion Recommendations](https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/data)
2. Đăng nhập/Đăng ký tài khoản Kaggle và chọn **Download All**.
3. Giải nén file vừa tải về.
4. Di chuyển 3 file dữ liệu chính (`articles.csv`, `customers.csv`, `transactions_train.csv`) vào thư mục `data/` của dự án này theo cấu trúc sau:

hm-fashion-analytics/
├── data/
│   ├── articles.csv
│   ├── customers.csv
│   └── transactions_train.csv
...

---

## 💡 Hướng dẫn chạy dự án (How to Run)

Thực hiện theo các bước sau để sao chép môi trường và chạy các Notebook trên máy tính của bạn:

**1. Clone kho lưu trữ (Clone the repository)**
```bash
git clone https://github.com/your-username/hm-fashion-analytics.git
cd hm-fashion-analytics
```

**2. Thiết lập Môi trường ảo (Set up Virtual Environment)**
```bash
python -m venv venv

# Trên Windows:
.\venv\Scripts\activate
# Trên Mac/Linux:
source venv/bin/activate
```

**3. Cài đặt Thư viện phụ thuộc (Install Dependencies)**
```bash
pip install pandas numpy scikit-learn statsmodels matplotlib seaborn duckdb pyarrow jupyter
```

**4. Khởi chạy Jupyter Notebooks**
Điều hướng tới thư mục `notebooks/` để khám phá quy trình phân tích theo từng bước:
```bash
jupyter notebook
```
* **Lưu ý:** Vui lòng chạy các Notebook theo thứ tự tuần tự (01 -> 02 -> 03 -> 04) để đảm bảo luồng dữ liệu chính xác.

---
*Xây dựng với niềm đam mê quản trị ra quyết định dựa trên dữ liệu.* 🚀
