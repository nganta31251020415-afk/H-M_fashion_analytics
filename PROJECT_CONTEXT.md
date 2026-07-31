# PROJECT CONTEXT

## H&M Personalized Fashion Analytics Portfolio Project

**Last Updated:** 2026-07-27

---

# 1. Project Overview

Đây là một Portfolio Project mô phỏng quy trình làm việc của một Data Analyst trong doanh nghiệp.

Dataset sử dụng:

> H&M Personalized Fashion Recommendations (Kaggle)

Mục tiêu của dự án không phải là đạt thứ hạng cao trên Kaggle Competition mà là xây dựng một portfolio chuyên nghiệp, thể hiện đầy đủ quy trình phân tích dữ liệu từ Business Understanding đến Machine Learning.

Dự án ưu tiên:

- Business Thinking
- Data Analytics Workflow
- Documentation
- Storytelling
- Dashboard Design
- Machine Learning phục vụ bài toán kinh doanh

Không ưu tiên:

- Kaggle Leaderboard
- Deep Learning
- Recommendation System đầy đủ
- Mô hình quá phức tạp

---

# 2. Project Objectives

Pipeline dự kiến:

1. Business Understanding
2. Data Understanding
3. Data Modeling
4. Data Cleaning
5. Data Validation
6. SQL Analytics
7. Exploratory Data Analysis (EDA)
8. Power BI Dashboard
9. Machine Learning
10. Business Storytelling
11. Documentation

Business luôn được ưu tiên trước kỹ thuật.

---

# 3. Dataset

Dataset:

H&M Personalized Fashion Recommendations

Bao gồm ba bảng:

## customers

- customer_id
- FN
- Active
- club_member_status
- fashion_news_frequency
- age
- postal_code

Rows:

1,371,980

---

## articles

- article_id
- product_code
- product_type_name
- product_group_name
- graphical_appearance_name
- colour_group_name
- index_name
- section_name
- garment_group_name
- detail_desc

Rows:

105,542

---

## transactions_train

- t_dat
- customer_id
- article_id
- price
- sales_channel_id

Rows:

31,788,324

---

# 4. Technology Stack

Programming

- Python
- SQL

Database

- DuckDB

Visualization

- Power BI

IDE

- VS Code
- Antigravity IDE

AI

- ChatGPT
- Gemini
- Claude
- Antigravity

Version Control

- Git
- GitHub

---

# 5. Development Principles

- Business first.
- Data before Machine Learning.
- Documentation throughout the project.
- Dashboard must answer business questions.
- Machine Learning must solve business problems.
- AI assists development but does not replace analytical thinking.

---

# 6. Coding Convention

File names:

English

Source code:

English

Variable names:

English

Comments:

English

Documentation (development stage):

Vietnamese

Final README:

English

---

# 7. Documentation Structure

docs/

01_business_understanding.md

02_data_dictionary.md

03_data_profiling_report.md

04_data_modeling.md

05_data_cleaning_validation.md

06_sql_analysis.md

07_eda.md

08_power_bi_dashboard.md

09_machine_learning.md

10_project_conclusion.md

Notebook lưu toàn bộ quá trình thực hiện.

Markdown tổng hợp kết quả cuối cùng.

---

# 8. Completed Phases

## Phase 0 — Project Setup

Completed.

Đã hoàn thành:

- Virtual Environment
- Package Installation
- Git
- GitHub
- Project Structure
- README
- Business Understanding

---

## Phase 1 — Data Understanding

Completed.

Đã thực hiện:

- Data Profiling
- Schema Inspection
- Data Types
- Row Count
- Missing Values
- Cardinality
- Date Range
- Sample Data
- Data Dictionary

### Grain Validation

Đã xác nhận:

transactions_train không có Primary Key tự nhiên.

Composite:

(customer_id,
article_id,
t_dat,
sales_channel_id)

không unique.

Theo tài liệu chính thức của H&M:

Duplicate rows phản ánh khách hàng mua nhiều hơn một đơn vị của cùng sản phẩm trong cùng ngày.

Không phải lỗi dữ liệu.

### Missing Values

customers

- FN (~65%)
- Active (~66%)
- club_member_status
- fashion_news_frequency
- age

articles

- detail_desc (~0.39%)

transactions_train

Không có NULL đáng kể.

### Cardinality

Không phải tất cả khách hàng đều có giao dịch.

Không phải tất cả sản phẩm đều được bán.

### Date Range

2018-09-20

↓

2020-09-22

---

## Phase 2 — Data Modeling

Completed.

Đã xác định:

- Grain của từng bảng
- Primary Key
- Foreign Key
- Fact Table
- Dimension Tables
- Star Schema
- ERD
- Thiết kế quan hệ giữa các bảng

Quyết định thiết kế:

Fact Table

- transactions_train

Dimension Tables

- customers
- articles

Date Dimension

Chưa tạo ở giai đoạn hiện tại.

Sẽ bổ sung nếu cần trong các bước phân tích nâng cao.

Zero-transaction customers

Được giữ lại trong Customer Dimension.

Lý do:

- phục vụ Customer Segmentation
- phân tích tỷ lệ chuyển đổi
- đánh giá hiệu quả marketing
- không làm mất thông tin nghiệp vụ

---

# 9. Business Notes

price

Đã chuẩn hóa.

Không phải tiền tệ thực tế.

Không diễn giải là USD hoặc bất kỳ đơn vị tiền tệ nào.

sales_channel_id

Có hai giá trị.

Ý nghĩa cần được xác nhận từ tài liệu chính thức trước khi phân tích doanh thu theo kênh.

articles

Có hai hệ thống phân cấp khác nhau.

Hierarchy 1

product_code

↓

product_type

↓

product_group

Hierarchy 2

index

↓

section

↓

garment_group

Không được nhầm lẫn hai hệ thống này.

---

# 10. GitHub

Repository chỉ chứa:

- Source Code
- SQL
- Notebook
- Documentation

Dataset gốc không đưa lên GitHub vì vượt quá giới hạn dung lượng.

Người dùng sẽ tự tải dataset từ Kaggle.

---

# 11. Working Style

Ưu tiên:

- Giải thích rõ từng bước
- Pipeline đơn giản
- Documentation đầy đủ
- Business Thinking

Nếu có nhiều cách triển khai:

Luôn phân tích:

- Ưu điểm
- Nhược điểm
- Khuyến nghị

Không tự động thay đổi kiến trúc dự án nếu chưa có sự đồng ý của người dùng.

---

# 12. Current Status

Current Status:

✅ Phase 0 — Completed

✅ Phase 1 — Completed

✅ Phase 2 — Completed

Next Phase:

Phase 3 — Data Cleaning & Data Validation

Mục tiêu:

- Làm sạch dữ liệu
- Chuẩn hóa kiểu dữ liệu
- Xử lý Missing Values
- Kiểm tra Referential Integrity
- Kiểm tra Data Quality
- Lưu dữ liệu sạch vào data/processed

Lưu ý:

Không chỉnh sửa dữ liệu trong thư mục data/raw.

Toàn bộ dữ liệu sau xử lý phải được lưu vào data/processed.