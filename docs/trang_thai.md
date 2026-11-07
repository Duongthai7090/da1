# Trạng thái triển khai dự án VN30 Dashboard

Checklist nhiệm vụ theo Mục 5 của AGENTS.md:

- [x] **A1**. Gold từ dữ liệu hiện có + test.
- [x] **1**. VN-Index và VN30 Index (OHLCV ngày từ 2018-10-16) bằng `vnstock` -> `gold\fact_chi_so_thi_truong` (CSV+Parquet), có `loi_suat`, test khóa/high>=low.
- [x] **2**. `src\cap_nhat.py` + `src\cap_nhat_bctc.py` + `docs\huong_dan_cap_nhat.md`; chạy thử cập nhật 1 lần, báo số dòng mới.
- [x] **3**. Kiểm tra giá đã điều chỉnh (timebox): ngày `abs(loi_suat) > 0.10` đối chiếu `exright_date` trong `data\raw\su_kien` -> `docs\kiem_tra_dieu_chinh_gia.md`. Nghi lệch: chỉ cảnh báo trên dashboard, không viết lại thuật toán.
- [x] **3b**. Vĩ mô và tin tức, MỨC TỐI THIỂU (timebox, phiếu ĐATN có yêu cầu): `gold\fact_vi_mo` (lãi suất liên ngân hàng, tỷ giá, CPI/GDP nếu lấy được) và `gold\fact_tin_tuc` (tiêu đề, ngày, nguồn, link từ RSS CafeF/VnExpress/Vietstock, gắn mã liên quan bằng khớp từ khóa/mã; KHÔNG sentiment). Lấy theo `sleep` + checkpoint, tôn trọng điều khoản trang. Không lấy được: trang tương ứng hiện "N/A" và ghi vào hạn chế dữ liệu.
- [x] **4**. Webapp Streamlit (`webapp\app.py`, `webapp\pages\`, `requirements.txt`), 6 trang như mục 6 và mục 9. Chạy thử toàn bộ trang không lỗi.
- [x] **5**. Power BI theo phạm vi mới mục 9 (không tạo .pbip, chỉnh .m, .dax, HUONG_DAN_DUNG_POWERBI.md).
- [x] **6**. (Timebox, BỎ theo mục 9) số cổ phiếu lưu hành -> `gold\fact_dinh_gia`. Ghi nhận vào `docs/han_che_du_lieu.md`.
- [x] **7**. Hoàn thiện: `docs\han_che_du_lieu.md`, `docs\insight.md` (5-7 phát hiện có số liệu + gợi ý hành động), `README.md`, đóng gói để deploy Streamlit Cloud (dữ liệu Gold nằm trong repo).

---
*Ghi chú: Cập nhật tự động sau mỗi đầu việc hoàn thành.*
