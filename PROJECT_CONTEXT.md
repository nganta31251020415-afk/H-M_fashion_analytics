# PROJECT_CONTEXT

> Mục đích của file này là ghi lại trạng thái hiện tại của dự án để có thể tiếp tục làm việc ở bất kỳ cuộc trò chuyện nào mà không cần giải thích lại từ đầu.

---

# Thông tin dự án

**Tên dự án**

H&M Personalized Fashion Analytics

**Dataset**

H&M Personalized Fashion Recommendations (Kaggle)

---

# Tiến độ hiện tại

## Phase 0 — Project Setup & Business Understanding

**Trạng thái:** ✅ Hoàn thành

Đã hoàn thành:

- Thiết lập môi trường Python.
- Khởi tạo Git.
- Tạo cấu trúc project.
- Đưa dataset vào `data/raw/`.
- Xóa thư mục `images/` (không sử dụng trong phạm vi dự án).
- Hoàn thành tài liệu `docs/01_business_understanding.md`.
- Commit toàn bộ Phase 0.

---

# Quyết định đã thống nhất

- Dùng DuckDB thay cho SQLite.
- Dashboard bằng Power BI.
- Documentation viết bằng tiếng Việt trong quá trình phát triển.
- README cuối cùng sẽ viết bằng tiếng Anh.
- Machine Learning chỉ triển khai sau khi hoàn thành Data Analytics.
- Không thực hiện Recommendation System hoàn chỉnh.
- Không xử lý ảnh sản phẩm.
- AI được sử dụng để hỗ trợ lập trình nhưng mọi phân tích và kết luận sẽ được tự đánh giá.

---

# Cấu trúc hiện tại

```text
hm-fashion-analytics/

├── data/
├── docs/
├── notebooks/
├── sql/
├── src/
├── dashboard/
├── models/
├── reports/
├── tests/
├── README.md
└── .gitignore
```

---

# Bước tiếp theo

## Phase 1 — Data Understanding

Mục tiêu:

Hiểu dữ liệu trước khi tiến hành Data Profiling và Data Cleaning.

Công việc dự kiến:

- Đọc 3 bảng dữ liệu bằng DuckDB.
- Kiểm tra schema.
- Xác định data grain.
- Kiểm tra kiểu dữ liệu.
- Xem dữ liệu mẫu.
- Xây dựng Data Dictionary.
- Ghi nhận các vấn đề ban đầu của dữ liệu.

---

# Ghi chú

Mỗi khi hoàn thành một Phase, cập nhật file này:

- Phase nào đã hoàn thành.
- Các quyết định quan trọng.
- Các thay đổi về phạm vi dự án.
- Bước tiếp theo cần thực hiện.

File này đóng vai trò là "bộ nhớ" của dự án khi chuyển sang cuộc trò chuyện mới hoặc quay lại sau một thời gian.