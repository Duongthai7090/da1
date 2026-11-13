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

Checklist nhiệm vụ theo Mục 10 của AGENTS.md (Áp dụng từ 2026-11-08):

- [x] **10.0**. Sửa lỗi / đối soát sự kiện quyền TCB (giải trình bước nhảy giá và xác nhận sự kiện cổ tức 50%).
- [x] **10.1**. `src/nap_mysql.py`: đọc `gold/*.parquet`, tạo bảng trong `vn30_gold` (giữ tên `dim_/fact_`, thêm khóa chính + chỉ mục, `utf8mb4`), chạy lặp lại được (truncate+load trong transaction), in số dòng từng bảng và so với Gold. Gọi script này ở cuối `src/cap_nhat.py`.
- [x] **10.2**. Cào lại sự kiện cổ tức/phát hành 30 mã (VCI qua vnstock) -> `stg_su_kien` -> `fact_su_kien` (`ma_cp`, `loai`, `ngay_gdkhq`, `ngay_chot`, `ngay_chi_tra`, `ty_le`, `hinh_thuc`, `nguon`). Xác nhận có TCB cổ tức 50% bằng cổ phiếu, ex-date 29/10/2026. Xuất thêm ra `gold/` để webapp đọc không cần MySQL.
- [x] **10.3**. Tin tức theo kiểu stg -> master -> map: `stg_tin_tuc` (tiêu đề, link, ngày, nguồn, nội dung thô) -> `fact_tin_tuc` gắn `ma_cp` (khớp mã/tên công ty) và `nganh_cap1` (qua `dim_co_phieu`), cột `loai_tin` (sự kiện CK / ngành / chung) bằng từ khóa. Cột chưa map được để NULL. Nguồn: RSS công khai (VnExpress, Tuổi Trẻ, Thanh Niên, VietnamNet), tôn trọng robots.txt, có sleep.
- [x] **10.4**. Phi cấu trúc, chỉ dựng khung: thư mục `data/tai_lieu/<ma_cp>/<loai>/<nam>/`, bảng `meta_tai_lieu` (`ma_cp`, `loai`, `ky`, `nguon_url`, `ngay`, `duong_dan`, `meta_dac_thu` NULL). Tải thử tối đa 3-5 PDF công khai (FPT, VCB, HPG, TCB) làm mẫu, không cào hàng loạt.
- [x] **10.5**. Thêm bảng sự kiện GDKHQ vào trang Tin tức của webapp. Cập nhật `docs/han_che_du_lieu.md`: không có giá theo giờ, đồ thị cổ đông, AI; tin ngành chỉ theo từ khóa; PDF chỉ là mẫu.
- [x] **10.6**. Chạy tests + AppTest (7/7 trang PASS), ghi nhật ký, hoàn tất cập nhật.



---
*Ghi chú: Cập nhật tự động sau mỗi đầu việc hoàn thành.*
