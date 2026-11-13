# -*- coding: utf-8 -*-
"""app.py - Trang chủ VN30 Dashboard. Chạy: streamlit run webapp/app.py"""
import sys
from pathlib import Path
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.data_loader import get_all_data
from utils.style import setup

d = get_all_data()
setup("Trang chủ", "Dashboard phân tích cổ phiếu VN30", d["ngay_cap_nhat"],
      "Dữ liệu tích hợp từ nhiều nguồn, cập nhật hằng ngày")

n_ma = d["dim_cp"]["ma_cp"].nunique() if len(d["dim_cp"]) else 0
c = st.columns(4)
c[0].metric("Số mã theo dõi", n_ma)
c[1].metric("Phiên giao dịch", f"{d['fact_gia']['ngay'].nunique():,}" if len(d["fact_gia"]) else "N/A")
c[2].metric("Dòng dữ liệu giá", f"{len(d['fact_gia']):,}")
c[3].metric("Cập nhật đến", d["ngay_cap_nhat"])

st.write("")
st.markdown("#### Các trang")
trang = [
    ("Tổng quan VN30 / ngành", "VN30 so với VN-Index, độ rộng thị trường, hiệu suất ngành, bản đồ nhiệt"),
    ("Phân tích cổ phiếu", "Nến, MA, RSI, MACD, lợi suất theo tháng, phân phối lợi suất"),
    ("Báo cáo tài chính", "ROE, ROA, biên lợi nhuận, đòn bẩy, so sánh trong ngành"),
    ("So sánh cổ phiếu", "Rủi ro - lợi suất, drawdown, tương quan, beta"),
    ("Tin tức & vĩ mô", "Tin tức gắn mã, GDP, CPI, tỷ giá"),
    ("Nguồn & giới hạn", "Độ phủ dữ liệu, hạn chế, quy trình cập nhật"),
]
cols = st.columns(3)
for i, (t, m) in enumerate(trang):
    with cols[i % 3]:
        st.markdown(f"**{t}**  \n<span style='color:#64748B;font-size:.88rem'>{m}</span>", unsafe_allow_html=True)
        st.write("")
st.caption("Nguồn: vnstock (KBS, VCI), World Bank, RSS tin tức. Đồ án Business Analysis, 2026.")
