# Đồ án BA: Dashboard Phân Tích Cổ Phiếu VN30 (2018 - 2026)

Hệ thống phân tích đầu tư và trực quan hóa dữ liệu toàn diện cho rổ cổ phiếu **VN30** và chỉ số thị trường Việt Nam (**VN-Index, VN30 Index**), phục vụ các nhà đầu tư cá nhân và hội đồng đánh giá đồ án Phân tích Nghiệp vụ (Business Analysis).

---

## 🌟 Điểm nổi bật của Dự án

1. **Kiến trúc Dữ liệu Gold Layer Độc lập & Tự động**:
   - Kho dữ liệu Star Schema chuẩn hóa với 7 bảng nghiệp vụ (`dim_co_phieu`, `dim_ngay`, `fact_gia_ngay`, `fact_loi_suat`, `fact_chi_bao_ky_thuat`, `fact_chi_so_tai_chinh`, `fact_chi_so_thi_truong`, `fact_vi_mo`, `fact_tin_tuc`).
   - Cung cấp cả 2 định dạng: **CSV UTF-8 with BOM** (tương thích 100% với Power BI Desktop) và **Parquet** (tối ưu hóa cho phân tích Python/Streamlit).
2. **Cập nhật dữ liệu Một lệnh duy nhất**:
   - Chạy lệnh `python src/cap_nhat.py` để tự động tải phiên mới qua `vnstock`, nối Gold, tính lại chỉ báo kỹ thuật (MA, RSI, MACD, Drawdown), cập nhật VN-Index và chạy bộ test tự động.
3. **Webapp Đa trang Streamlit 6 Chức năng**:
   - **01. Tổng quan VN30 & Ngành**: KPI thị trường, so sánh đường lợi suất tích lũy VN30 vs VN-Index, Top 5 tăng/giảm, Treemap heatmap lợi suất theo ngành.
   - **02. Phân tích Cổ phiếu**: Biểu đồ Nến tương tác, khối lượng, MA20/50/200, RSI14, MACD và cờ cảnh báo điều chỉnh giá.
   - **03. Báo cáo Tài chính**: Hiệu quả sinh lời (ROE, ROA), biên lợi nhuận, đòn bẩy tài chính, chỉ số ngân hàng chuyên biệt (CIR, LDR xấp xỉ), xử lý hiển thị N/A chuẩn xác cho CTCK.
   - **04. So sánh Đối đầu (2 - 5 mã)**: Lợi suất tích lũy, phân tích đánh đổi Lợi suất - Rủi ro (Scatter plot), sụt giảm từ đỉnh (Drawdown), ma trận tương quan Pearson, Beta so với VN30.
   - **05. Tin tức & Vĩ mô**: Dữ liệu tăng trưởng GDP, lạm phát CPI (World Bank), tỷ giá USD/VND Vietcombank, dòng tin tức tài chính RSS VnExpress.
   - **06. Nguồn & Giới hạn**: Bảng độ phủ dữ liệu từng mã, thống kê hệ thống, tóm tắt hạn chế và cảnh báo.
4. **Mô hình Báo cáo Power BI Chuyên nghiệp**:
   - Bộ mã chuyển đổi Power Query M (`powerbi/vn30_powerquery.m`), hệ thống DAX Measure tối ưu (`powerbi/vn30_measures.dax`) và hướng dẫn tạo Dashboard wireframe chi tiết (`powerbi/HUONG_DAN_DUNG_POWERBI.md`).

---

## 📁 Cấu trúc Thư mục

```text
da1/
├── gold/                        # Tầng dữ liệu chuẩn hóa duy nhất (CSV + Parquet)
│   ├── dim_co_phieu.*           # 30 mã VN30 và thông tin phân ngành
│   ├── dim_ngay.*               # Lịch ngày giao dịch chuẩn hóa
│   ├── fact_gia_ngay.*          # 56.000+ phiên OHLCV điều chỉnh
│   ├── fact_loi_suat.*          # Lợi suất hàng ngày
│   ├── fact_chi_bao_ky_thuat.*  # MA20/50/200, RSI14, MACD, Drawdown
│   ├── fact_chi_so_tai_chinh.*  # BCTC năm 2022-2025 (28 mã DN+NH)
│   ├── fact_chi_so_thi_truong.* # VNINDEX & VN30 OHLCV
│   ├── fact_vi_mo.*             # GDP, CPI, Tỷ giá USD
│   └── fact_tin_tuc.*           # Tin tức sự kiện RSS
├── webapp/                      # Ứng dụng Web tương tác Streamlit
│   ├── app.py                   # Điểm vào chính & Sidebar điều hướng
│   ├── pages/                   # 6 trang nghiệp vụ chi tiết
│   │   ├── 01_tong_quan.py
│   │   ├── 02_phan_tich.py
│   │   ├── 03_bctc.py
│   │   ├── 04_so_sanh.py
│   │   ├── 05_tin_tuc_vi_mo.py
│   │   └── 06_nguon_gioi_han.py
│   └── utils/
│       └── data_loader.py       # Caching mtime tự động tải dữ liệu mới
├── powerbi/                     # Tài nguyên tích hợp Microsoft Power BI
│   ├── vn30_powerquery.m        # Script Power Query nạp dữ liệu từ gold/
│   ├── vn30_measures.dax        # Danh mục Measure DAX chuẩn nghiệp vụ
│   └── HUONG_DAN_DUNG_POWERBI.md # Hướng dẫn dựng Dashboard Power BI
├── src/                         # Kịch bản cập nhật dữ liệu tự động
│   ├── cap_nhat.py              # Cập nhật giá & chỉ báo kỹ thuật hàng ngày
│   └── cap_nhat_bctc.py         # Cập nhật Báo cáo tài chính theo quý
├── tests/
│   └── kiem_tra_gold.py         # Bộ kiểm thử tự động toàn vẹn Gold (7 bài test)
├── docs/                        # Tài liệu phân tích nghiệp vụ & Báo cáo
│   ├── insight.md               # 6 phát hiện nghiệp vụ & khuyến nghị đầu tư
│   ├── han_che_du_lieu.md       # Báo cáo các giới hạn & cảnh báo dữ liệu
│   ├── huong_dan_cap_nhat.md    # Hướng dẫn thao tác cập nhật dữ liệu
│   ├── kiem_tra_dieu_chinh_gia.md # Kết quả kiểm định giá điều chỉnh
│   ├── trang_thai.md            # Tiến độ triển khai nhiệm vụ
│   └── nhat_ky.md               # Nhật ký phát triển chi tiết
└── requirements.txt             # Danh mục thư viện Python
```

---

## 🚀 Hướng dẫn Cài đặt & Chạy ứng dụng

### 1. Môi trường Python
Yêu cầu Python 3.10+:
```bash
# Tạo và kích hoạt môi trường ảo
python -m venv .venv
# Trên Windows:
.\.venv\Scripts\Activate.ps1
# Cài đặt các gói phụ thuộc
pip install -r requirements.txt
```

### 2. Khởi chạy Webapp Streamlit tại máy nội bộ (Local)
```bash
streamlit run webapp/app.py
```
Trình duyệt sẽ tự động mở tại địa chỉ `http://localhost:8501`.

### 3. Cập nhật dữ liệu phiên mới
Chỉ cần thực hiện lệnh sau sau mỗi phiên giao dịch:
```bash
python src/cap_nhat.py
```
Webapp sẽ tự động phát hiện tệp Gold mới qua cơ chế caching `mtime` và cập nhật dữ liệu mà không cần khởi động lại server.

---

## ☁️ Hướng dẫn Triển khai lên Streamlit Community Cloud

Dự án được thiết kế để triển khai sẵn sàng lên nền tảng đám mây hoàn toàn miễn phí:
1. **Đẩy mã nguồn lên GitHub**:
   - Toàn bộ thư mục `gold/` chứa dữ liệu CSV/Parquet được lưu trữ trực tiếp trong repository (không cần kết nối ra ngoài cơ sở dữ liệu MySQL).
2. **Đăng nhập vào Streamlit Community Cloud**:
   - Truy cập [share.streamlit.io](https://share.streamlit.io) và đăng nhập bằng tài khoản GitHub.
3. **Tạo App mới (New App)**:
   - **Repository**: Chọn repo GitHub của dự án (ví dụ `username/da1-vn30-dashboard`).
   - **Branch**: `main`
   - **Main file path**: `webapp/app.py`
4. **Bấm "Deploy"**:
   - Streamlit Cloud sẽ tự động đọc `requirements.txt`, cài đặt môi trường và khởi chạy ứng dụng trực tuyến với đường link chia sẻ công khai.

---

## 📊 Hướng dẫn Kết nối với Power BI Desktop

Xem chi tiết tại [powerbi/HUONG_DAN_DUNG_POWERBI.md](powerbi/HUONG_DAN_DUNG_POWERBI.md):
1. Mở Power BI Desktop, vào **Home > Transform Data > Advanced Editor**.
2. Dán mã nguồn từ [powerbi/vn30_powerquery.m](powerbi/vn30_powerquery.m).
3. Đổi tham số `DuongDanGold` trỏ về thư mục `gold/` trên máy tính của bạn.
4. Bấm **Close & Apply** và tạo bảng `_Measures` từ file [powerbi/vn30_measures.dax](powerbi/vn30_measures.dax).

---

## 📜 Kiểm thử Chất lượng Dữ liệu

Chạy bộ kiểm thử toàn vẹn tự động:
```bash
python tests/kiem_tra_gold.py
```
Bộ kiểm tra xác thực tính hợp lệ của tất cả các bảng: không trùng lặp khóa chính, toàn vẹn tham chiếu, tính liên tục của chuỗi giá, quan hệ logic `gia_cao >= gia_thap` và `high >= low` đối với toàn bộ 56.000+ dòng dữ liệu.
