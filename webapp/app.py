# -*- coding: utf-8 -*-
"""
app.py - Điểm vào chính của webapp VN30 Dashboard.
Chạy: streamlit run webapp/app.py
"""

import streamlit as st

st.set_page_config(
    page_title="VN30 Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS tùy chỉnh nhỏ
st.markdown("""
<style>
    .main .block-container { padding-top: 1rem; }
    .metric-card { background: #f0f2f6; border-radius: 8px; padding: 12px; }
    .stMetric label { font-size: 0.82rem !important; }
</style>
""", unsafe_allow_html=True)

# Trang chủ
st.title("📊 Dashboard Phân Tích Cổ Phiếu VN30")
st.markdown("""
**Chào mừng đến với Dashboard phân tích cổ phiếu VN30!**

Sử dụng thanh điều hướng bên trái để chuyển sang các trang:

| Trang | Nội dung |
|-------|----------|
| 🏠 **Tổng quan VN30/Ngành** | KPI thị trường, lợi suất tích lũy, top tăng/giảm, heatmap ngành |
| 📈 **Phân tích cổ phiếu** | Biểu đồ nến, MA, RSI, MACD cho từng mã |
| 📋 **BCTC** | ROE, ROA, biên lợi nhuận, đòn bẩy tài chính |
| ⚖️ **So sánh cổ phiếu** | Rủi ro-lợi suất, tương quan, drawdown, beta |
| 📰 **Tin tức & Vĩ mô** | Tin tức gắn mã, CPI, GDP, tỷ giá |
| ℹ️ **Nguồn & Giới hạn** | Độ phủ dữ liệu, hạn chế, thời điểm cập nhật |

---
*Dữ liệu: VN30, 2018-10-16 đến nay. Nguồn: vnstock (KBS), World Bank, VnExpress.*  
*Đồ án Business Analysis - 2026*
""")
