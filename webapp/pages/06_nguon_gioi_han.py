# -*- coding: utf-8 -*-
"""
Trang 6: Nguồn Dữ liệu & Giới hạn Dự án
- Bảng độ phủ dữ liệu từng mã cổ phiếu VN30 (Ngày bắt đầu, Ngày kết thúc, Số dòng/phiên)
- Thống kê kiến trúc tầng dữ liệu Gold
- Chi tiết các hạn chế dữ liệu, sự kiện lệch giá, và các giả định theo chuẩn đồ án BA
- Hướng dẫn quy trình cập nhật dữ liệu tự động
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.data_loader import get_all_data, CANH_BAO_GIA
from utils.style import setup, ghi_chu, TANG, GIAM, VN30, VNINDEX

setup('Nguồn & giới hạn', 'Nguồn dữ liệu & giới hạn')

# --- Load dữ liệu ---
data = get_all_data()
dim_cp = data["dim_cp"]
fact_gia = data["fact_gia"]
fact_ttm = data["fact_ttm"]
fact_tc = data["fact_tc"]
ngay_cap_nhat = data["ngay_cap_nhat"]

st.caption(f"Thời điểm dữ liệu cập nhật gần nhất: **{ngay_cap_nhat}**")

# --- Thống kê tổng thể ---
st.subheader("Kiến trúc Kho dữ liệu Chuẩn hóa (Gold Layer)")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Số mã cổ phiếu VN30", f"{len(dim_cp)}")
c2.metric("Tổng số phiên giao dịch", f"{len(fact_gia):,}")
c3.metric("Dữ liệu chỉ số thị trường", f"{len(fact_ttm):,} dòng")
c4.metric("Báo cáo tài chính", f"{len(fact_tc):,} bản ghi")

st.divider()

# --- Tab phân chia: Độ phủ dữ liệu & Hạn chế ---
tab_dophu, tab_hanche, tab_kientruc = st.tabs([
    "Độ phủ dữ liệu", "Hạn chế dữ liệu", "Kiến trúc & Cập nhật"
])

with tab_dophu:
    st.subheader("Độ phủ dữ liệu giao dịch 30 mã cổ phiếu VN30")
    
    # Tính toán độ phủ thực tế từ fact_gia
    do_phu = fact_gia.groupby("ma_cp").agg(
        ngay_dau=("ngay", "min"),
        ngay_cuoi=("ngay", "max"),
        so_phien=("ngay", "count")
    ).reset_index()

    do_phu["ngay_dau_str"] = do_phu["ngay_dau"].dt.strftime("%d/%m/%Y")
    do_phu["ngay_cuoi_str"] = do_phu["ngay_cuoi"].dt.strftime("%d/%m/%Y")

    bang_dp = dim_cp[["ma_cp", "ten_cong_ty", "nganh_cap1", "mau_bctc"]].merge(
        do_phu[["ma_cp", "ngay_dau_str", "ngay_cuoi_str", "so_phien"]],
        on="ma_cp",
        how="left"
    )

    bang_dp = bang_dp.rename(columns={
        "ma_cp": "Mã CP",
        "ten_cong_ty": "Tên doanh nghiệp",
        "nganh_cap1": "Nhóm ngành",
        "mau_bctc": "Mẫu BCTC",
        "ngay_dau_str": "Từ ngày",
        "ngay_cuoi_str": "Đến ngày",
        "so_phien": "Số phiên giao dịch"
    })

    st.dataframe(bang_dp, use_container_width=True, hide_index=True)

with tab_hanche:
    st.subheader("Các giới hạn và phát hiện bất thường về dữ liệu")

    st.markdown("""
### 1. Kiểm tra Điều chỉnh giá và Biến động mạnh
- **TCB (15/10/2026)**: Xuất hiện mức giảm đột biến **-33.4%** nhưng không tìm thấy sự kiện chia tách/cổ tức tương ứng từ nguồn sự kiện thô. Được gắn cờ cảnh báo trên giao diện phân tích kỹ thuật.
- **SHB (14/05/2021)**: Phiên tăng trần +10% trùng thời điểm chia cổ tức/cổ phiếu thưởng 10%, nghi vấn giá nguồn KBS đã hoặc chưa trừ hệ số điều chỉnh chuẩn xác.
- **BSR**: Cổ phiếu từ UPCoM chuyển sàn nên có một số phiên biến động biên độ rộng (+/- 15%).

### 2. Dữ liệu Báo cáo Tài chính
- **Nhóm Chứng khoán (SSI, TCX)**: Có mẫu BCTC đặc thù (`mau_bctc = 'CK'`), khác biệt hoàn toàn với Doanh nghiệp sản xuất thông thường (`DN`) và Ngân hàng (`NH`). Hệ thống tạm thời để **N/A** cho các chỉ số tài chính của 2 mã này nhằm bảo đảm tính nhất quán của mô hình so sánh.
- **Chỉ tiêu Định giá (P/E, P/B, Vốn hóa)**: Do thiếu chuỗi lịch sử số lượng cổ phiếu lưu hành sau các đợt chia tách/phát hành riêng lẻ theo ngày, theo phạm vi mục 9 của đồ án, chỉ tiêu này không được tính toán suy đoán nhằm tránh sai lệch số liệu. Phân tích cơ bản tập trung vào năng lực nội tại: **ROE, ROA, Biên lợi nhuận, Đòn bẩy và CIR**.

### 3. Dữ liệu Vĩ mô & Tin tức
- **Lãi suất liên ngân hàng (VNIBOR)**: Ngân hàng Nhà nước Việt Nam không cung cấp Web API truy vấn mở miễn phí, do đó hiển thị **N/A**.
- **Tỷ giá USD/VND**: Thu thập điểm tỷ giá bán ra hiện hành từ cổng XML mở của Vietcombank, chưa có chuỗi lịch sử chi tiết từng ngày.
- **Tin tức**: Nguồn cấp RSS từ VnExpress Kinh Doanh được lấy tự động; các nguồn CafeF và Vietstock có cơ chế chặn XML Parser tự động được ghi nhận theo tài liệu dự án.
""")

with tab_kientruc:
    st.subheader("Nguyên tắc kiến trúc & Quy trình cập nhật")

    st.markdown("""
- **Nguồn chân lý duy nhất (Single Source of Truth)**: Toàn bộ Dashboard và Báo cáo Power BI đọc trực tiếp từ thư mục `gold/` (định dạng CSV UTF-8 with BOM và Parquet). Cơ sở dữ liệu nguồn MySQL chỉ dùng ở chế độ `SELECT ONLY`.
- **Cơ chế Caching thông minh**: Streamlit sử dụng `@st.cache_data` liên kết với thời gian sửa đổi gần nhất (`mtime`) của các tệp Gold. Khi người dùng chạy lệnh cập nhật, dữ liệu mới sẽ tự động hiển thị mà không cần khởi động lại máy chủ.
- **Quy trình cập nhật hàng ngày (1 lệnh duy nhất)**:
  ```bash
  python src/cap_nhat.py
  ```
  Lệnh trên sẽ tự động:
  1. Xác định ngày cuối cùng của từng mã trong `fact_gia_ngay`
  2. Tải thêm các phiên mới qua thư viện `vnstock` (KBS)
  3. Tính toán lại MA20, MA50, MA200, RSI, MACD, Drawdown
  4. Cập nhật dữ liệu chỉ số thị trường VN-Index & VN30
  5. Chạy bộ kiểm thử tự động `tests/kiem_tra_gold.py` đảm bảo tính toàn vẹn 100%.
""")
