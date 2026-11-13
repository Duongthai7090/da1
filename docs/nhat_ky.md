# Nhật ký triển khai dự án Dashboard VN30

## 2026-11-08: Hoàn thành Phạm vi mới theo Mục 10 của AGENTS.md
- **Nạp dữ liệu vào MySQL schema `vn30_gold` (`src/nap_mysql.py`)**:
  - Viết `src/nap_mysql.py` đọc toàn bộ `gold/*.parquet`, khởi tạo tự động 11 bảng dữ liệu với khóa chính, khóa duy nhất, chỉ mục tối ưu, bảng mã `utf8mb4`.
  - Cơ chế nạp chạy lặp lại an toàn (DELETE/TRUNCATE + bulk insert trong transaction).
  - Kết quả nạp 11 bảng: `dim_co_phieu` (30 dòng), `dim_ngay` (2.933 dòng), `fact_gia_ngay` (56.163 dòng), `fact_loi_suat` (56.163 dòng), `fact_chi_bao_ky_thuat` (56.163 dòng), `fact_chi_so_tai_chinh` (112 dòng), `fact_chi_so_thi_truong` (4.014 dòng), `fact_su_kien` (392 dòng), `fact_tin_tuc` (160 dòng), `fact_vi_mo` (21 dòng), `meta_tai_lieu` (4 dòng). Tổng cộng **176.155 dòng**, khớp chính xác 100% với tầng Gold.
  - Tích hợp tự động gọi `nap_mysql.py` vào cuối quy trình cập nhật hàng ngày `src/cap_nhat.py`.
- **Cào sự kiện cổ tức/phát hành 30 mã VN30 & Đối soát lỗi TCB (`scripts/etl/cao_lai_su_kien.py`)**:
  - Cào thành công 30/30 mã VN30 từ VCI với cơ chế checkpoint và bắt `BaseException` tự động nghỉ giải phóng quota Guest limit.
  - Tạo bảng `stg_su_kien` và chuẩn hóa thành `fact_su_kien` (392 sự kiện).
  - **Xác nhận thành công**: TCB có sự kiện **Phát hành cổ phiếu trả cổ tức tỷ lệ 50.0%** (GDKHQ ngày **29/10/2026**, ngày chốt danh sách **30/10/2026**). Nguồn KBS điều chỉnh hồi tố giá tham chiếu (giảm 1/1.5) từ phiên 15/10/2026, làm rõ bản chất mức giảm danh nghĩa -33.4% khi ghép nối nguồn. Xuất đầy đủ ra `gold/fact_su_kien.csv` và `.parquet`.
- **Pipeline Tin tức RSS theo mô hình `stg -> master -> map` (`scripts/etl/pipeline_tin_tuc.py`)**:
  - Thu thập 160 bài báo tài chính từ 4 nguồn RSS công khai (VnExpress, Tuổi Trẻ, Thanh Niên, VietnamNet) vào `stg_tin_tuc`.
  - Chuẩn hóa sang `fact_tin_tuc`: Ánh xạ tự động mã cổ phiếu (`ma_cp`), ngành cấp 1 (`nganh_cap1` qua `dim_co_phieu`), và phân loại tin (`loai_tin`: Sự kiện CK, Ngành, Chung) bằng hệ thống từ khóa; giữ `NULL` cho các trường chưa xác định. Xuất ra Gold và nạp vào MySQL `vn30_gold`.
- **Dựng khung dữ liệu phi cấu trúc & `meta_tai_lieu` (`scripts/etl/dung_khung_phi_cau_truc.py`)**:
  - Thiết lập cây thư mục phân cấp `data/tai_lieu/<ma_cp>/<loai>/<nam>/`.
  - Tải và lưu trữ 4 tệp PDF tài liệu BCTC mẫu cho các doanh nghiệp đầu ngành (FPT, VCB, HPG, TCB).
  - Tạo bảng `meta_tai_lieu` trong MySQL `vn30_gold` và xuất file `gold/meta_tai_lieu.parquet` với trường `meta_dac_thu = NULL`.
- **Nâng cấp Webapp Streamlit (`webapp/pages/05_tin_tuc_vi_mo.py` & `webapp/utils/data_loader.py`)**:
  - Bổ sung tab **"📅 Sự kiện GDKHQ & Quyền"** với bộ lọc mã cổ phiếu, hình thức chi trả, tìm kiếm loại sự kiện và highlight trực quan sự kiện cổ tức 50% của TCB.
  - Bổ sung bộ lọc phân loại tin tức và hiển thị nhãn Ngành / Loại tin trên từng bài viết.
  - Cập nhật tài liệu `docs/han_che_du_lieu.md` và `docs/kiem_tra_dieu_chinh_gia.md`: Làm rõ không có giá theo giờ/intraday, không có đồ thị cổ đông, không dùng mô hình AI dự báo; tin ngành phân loại theo từ khóa và tệp PDF chỉ là tài liệu mẫu.
- **Kiểm thử tự động**:
  - `tests/kiem_tra_gold.py`: 9/9 bài kiểm tra ĐẠT (PASS) 100%.
  - `tests/test_app.py`: 7/7 trang Streamlit PASSED không có exception nào.


## 2026-11-01: Hoàn thành Bước A1 (Xây dựng tầng dữ liệu Gold)
- **Tạo bộ dữ liệu Gold**: Đã trích xuất và lưu trữ 6 bảng Star Schema trong thư mục `gold/` ở cả 2 định dạng CSV và Parquet (`dim_co_phieu`, `dim_ngay`, `fact_gia_ngay`, `fact_loi_suat`, `fact_chi_bao_ky_thuat`, `fact_chi_so_tai_chinh`).
- **Phạm vi chuẩn hóa**: Thu gọn đúng 30 mã VN30 hiện hành (`thuoc_vn30_hien_hanh = 1`) trong cửa sổ chung từ 2018-10-16 đến 2026-10-14 (55.803 dòng giá/lợi suất/chỉ báo; 112 dòng BCTC 2022-2025).
- **Tính toán chỉ báo kỹ thuật**: Bổ sung đầy đủ MA20, MA50, MA200, RSI14 (Wilder), MACD (12,26,9), biến động 20 phiên x $\sqrt{252}$, và drawdown từ đỉnh lịch sử trên toàn bộ chuỗi trước khi cắt cửa sổ.
- **Kiểm thử chất lượng**: Viết và chạy thành công bộ kiểm tra tự động `tests/kiem_tra_gold.py` (khóa chính không trùng, không null, toàn vẹn tham chiếu, `gia_cao >= gia_thap` 100% hợp lệ).

## 2026-11-07: Chuẩn bị đóng gói & Kiểm thử mô phỏng Cloud (Streamlit Community Cloud)
- **Đã làm**:
  - Ghi đè `.gitignore` theo cơ chế Whitelist chỉ cho phép đẩy `webapp/`, `gold/`, `docs/`, `requirements.txt`, `README.md`, `.gitignore`; chặn triệt để `__pycache__`, `.env`, `.venv`, MySQL config.
  - Tối ưu `requirements.txt` gốc chỉ chứa các thư viện tối thiểu cần thiết cho webapp (`streamlit`, `pandas`, `numpy`, `plotly`, `pyarrow` có phiên bản cố định; loại bỏ hoàn toàn `vnstock`, `mysql`, `SQLAlchemy`).
  - Chuẩn hóa module `webapp/utils/data_loader.py` và trang `05_tin_tuc_vi_mo.py`: 100% đường dẫn tương đối từ `Path(__file__)`, không còn bất kỳ đường dẫn cứng `C:\`, có khối `try/except` bảo vệ khi nạp dữ liệu và đọc RSS.
  - **Mô phỏng Cloud**: Đã tạo thư mục tạm cô lập, thiết lập môi trường ảo sạch (`clean_venv`), cài đặt gói từ `requirements.txt` và chạy kiểm thử `AppTest` trên toàn bộ 6 trang + `app.py`. Kết quả: **7/7 trang PASSED với 0 lỗi**.
  - **Kiểm định dung lượng & An toàn**: Tổng dung lượng repository là **17.55 MB** (41 tệp); file lớn nhất là `fact_chi_bao_ky_thuat.csv` (**5.16 MB** < giới hạn 50MB của GitHub); 100% không chứa bất kỳ file nhạy cảm nào (.env, mật khẩu, token).

## 2026-11-06: Hoàn thành Nhiệm vụ 5 (Tích hợp Power BI theo phạm vi mới)
- **Đã làm**:
  - Đối chiếu tên cột giữa script Power Query `powerbi/vn30_powerquery.m` và các tệp dữ liệu thô trong `powerbi/csv/`: Kết quả khớp hoàn toàn 100%.
  - Bổ sung 3 khối truy vấn Power Query M mới vào `vn30_powerquery.m`: `FactChiSo` (đọc `gold/fact_chi_so_thi_truong.csv`), `FactViMo` (đọc `gold/fact_vi_mo.csv`), `FactTin` (đọc `gold/fact_tin_tuc.csv`).
  - Bổ sung các DAX Measure so sánh chỉ số thị trường vào `powerbi/vn30_measures.dax`: `[Lợi suất quy 100 (Chỉ số)]`, `[VN30 quy 100]`, `[VNINDEX quy 100]`.
  - Cập nhật mục 3 (Đặc tả 6 trang Power BI), mục 5 (Danh sách kiểm thử kỳ vọng bổ sung FactChiSo, FactViMo, FactTin), và mục 6 (Nội dung giới hạn dữ liệu) trong file `powerbi/HUONG_DAN_DUNG_POWERBI.md`. Giữ nguyên toàn bộ phần còn lại.
- **Kết quả**: Gói tài nguyên Power BI đã sẵn sàng để người dùng nạp dữ liệu và làm mới tự động trên Power BI Desktop.

## 2026-11-06: Hoàn thành Nhiệm vụ 7 (Hoàn thiện Tài liệu, Insight & Đóng gói Deploy)
- **Đã làm**:
  - Soạn thảo `docs/han_che_du_lieu.md`: Tổng hợp đầy đủ giới hạn dữ liệu về phạm vi 30 mã, bất thường TCB (-33.4%) và SHB (+10%), đặc thù BCTC CTCK (SSI, TCX), căn cứ kỹ thuật bỏ bảng định giá P/E, P/B (nhiệm vụ 6) và hạn chế dữ liệu vĩ mô/tin tức.
  - Soạn thảo `docs/insight.md`: Đúc kết 6 phát hiện nghiệp vụ then chốt kèm số liệu định lượng (VN30 vượt trội VN-Index +16.7% Alpha; phân hóa lợi suất LPB +1038% vs SAB -45%; cạm bẫy ROE cao ở VNM/SAB; tương quan cao trong ngành ngân hàng >0.7; đánh đổi rủi ro-lợi suất VCB/FPT vs BSR/HPG; và chu kỳ phục hồi sau khủng hoảng COVID/2022) cùng bảng khuyến nghị danh mục mẫu.
  - Xây dựng `README.md` chuẩn dự án BA và hướng dẫn triển khai lên Streamlit Community Cloud (không phụ thuộc MySQL bên ngoài).
  - Tối ưu hóa file `requirements.txt` chuẩn môi trường sản xuất.
- **Kết quả**: Tài liệu hóa toàn diện, sẵn sàng bàn giao và deploy cloud.

## 2026-11-06: Hoàn thành Nhiệm vụ 4 (Webapp Streamlit 6 trang)
- **Đã làm**: Xây dựng hoàn chỉnh 4 trang còn lại của Webapp: `03_bctc.py` (ROE/ROA, biên LN, đòn bẩy, CIR/LDR cho ngân hàng, N/A cho CTCK), `04_so_sanh.py` (Lợi suất tích lũy đối đầu, scatter risk-return, drawdown, ma trận tương quan Pearson, Beta vs VN30), `05_tin_tuc_vi_mo.py` (GDP, CPI, USD/VND Vietcombank, N/A cho VNIBOR, RSS VnExpress), `06_nguon_gioi_han.py` (Độ phủ dữ liệu 30 mã, tóm tắt hạn chế và cảnh báo).
- **Kiểm thử**: Viết kịch bản kiểm thử tự động sử dụng `streamlit.testing.v1.AppTest` cho tất cả 6 trang + `app.py`. Đã phát hiện và sửa lỗi ánh xạ tên cột chỉ số `ma_chi_so`. Kết quả: 7/7 script kiểm thử đạt trạng thái PASSED với 0 exception.
- **Vấn đề còn lại**: Đã xử lý đầy đủ các giá trị thiếu hoặc đặc thù ngành (CK) bằng hiển thị "N/A" thân thiện và giải thích chi tiết.

## 2026-11-06: Hoàn thiện Nhiệm vụ 3b và Tiếp nhận Thay đổi phạm vi (Mục 9)
- **Đã làm**: Kiểm tra dữ liệu vĩ mô và tin tức đã tạo (`gold/fact_vi_mo.csv` 21 dòng từ World Bank + Vietcombank, `gold/fact_tin_tuc.csv` 50 bài RSS VnExpress có trích xuất mã VN30 liên quan). Tick hoàn thành 3b.
- **Tiếp nhận phạm vi mới**: Ghi mục 9 vào AGENTS.md/GEMINI.md; thứ tự ưu tiên: 1 (Webapp 4 trang còn lại) -> 4 (Việc 7: docs, README, requirements, Streamlit Cloud) -> 2 (Việc 5: Power BI chỉnh .m, .dax, hướng dẫn). Việc 6 (P/E, P/B) chính thức bỏ và đưa vào hạn chế dữ liệu.
- **Vấn đề còn lại**: Lãi suất liên ngân hàng không có API miễn phí -> đã ghi hạn chế và hiển thị N/A trên dashboard; CafeF/Vietstock chặn RSS -> đã ghi nhận.

## 2026-11-02: Hoàn thành Nhiệm vụ 3 (Kiểm tra giá điều chỉnh)
- **Đã làm**: Viết `scripts/kiemtra/kiem_tra_dieu_chinh_gia.py`, lọc 40 phiên có abs(lợi suất) > 10%, đối chiếu sự kiện trong `data/raw/su_kien/`.
- **Kết quả**: Tạo `docs/kiem_tra_dieu_chinh_gia.md`. Phát hiện 1 trường hợp nghi (SHB 2021-05-14 +10% khớp phát hành thêm 10%); TCB 2026-10-15 -33.4% không có sự kiện tương ứng → cảnh báo trên dashboard. Phần lớn còn lại là biến động thực (COVID tháng 3/2020, BSR biến động cao).
- **Vấn đề**: Thuật toán điều chỉnh giá không sửa; chỉ ghi cảnh báo. Cờ cảnh báo sẽ hiện ⚠️ trên webapp trang Phân tích.

## 2026-11-02: Hoàn thành Nhiệm vụ 2 (Script cập nhật tự động)
- **Đã làm**: Viết `src/cap_nhat.py` (cập nhật hàng ngày: giá 30 mã + chỉ số thị trường + tính lại chỉ báo kỹ thuật + kiểm thử tự động), `src/cap_nhat_bctc.py` (cập nhật BCTC theo quý), `docs/huong_dan_cap_nhat.md`.
- **Kết quả chạy thử**: Nạp 388 dòng giá cổ phiếu mới (30 mã, từ 2026-10-15 đến 2026-10-30) và 26 dòng chỉ số thị trường (VNI+VN30), bổ sung 12 ngày vào dim_ngay. Toàn bộ test 7/7 xanh (PASSED) sau cập nhật. Dữ liệu cập nhật đến ngày 2026-10-30.
- **Vấn đề**: vnstock Guest limit 20 lượt/phút; đã xây cơ chế `BaseException` catch + auto-chờ 30 giây. Với 30 mã cần ~265 giây; tỷ lệ cào thành công 100%.
- **Đã làm**: Viết script `scripts/etl/tao_fact_chi_so_thi_truong.py` tải trọn bộ lịch sử OHLCV của VN-Index và VN30 Index từ vnstock (2018-10-16 đến 2026-10-14, 1.995 phiên mỗi chỉ số), tính lợi suất ngày, chuẩn hóa OHLC.
- **Kết quả**: Tạo thành công `gold/fact_chi_so_thi_truong.csv` (395 KB) và `.parquet` (217 KB) với 3.990 dòng. Đã cập nhật bộ test `tests/kiem_tra_gold.py` kiểm tra toàn vẹn khóa, không null, `gia_cao >= gia_thap`, kết quả test 7/7 bài kiểm tra đều xanh (PASS).
- **Vấn đề còn lại / Ghi nhận**: Có 13 dòng dữ liệu thô (3 của VNI, 10 của VN30) có giá đóng cửa ATC lệch nhẹ so với high/low trong phiên; đã áp dụng hàm chuẩn hóa và gắn cờ `co_sua_ohlc` đồng bộ với chuẩn của dự án.

