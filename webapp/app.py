# -*- coding: utf-8 -*-
"""app.py - Điểm vào + điều hướng. Chạy: streamlit run webapp/app.py"""
import streamlit as st

# Điều hướng tường minh để menu hiển thị tên tiếng Việt có dấu
pg = st.navigation([
    st.Page("views/trang_chu.py", title="Trang chủ", default=True),
    st.Page("pages/01_tong_quan.py", title="Tổng quan VN30 & ngành", url_path="tong_quan"),
    st.Page("pages/02_phan_tich.py", title="Phân tích cổ phiếu", url_path="phan_tich"),
    st.Page("pages/03_bctc.py", title="Báo cáo tài chính", url_path="bctc"),
    st.Page("pages/04_so_sanh.py", title="So sánh cổ phiếu", url_path="so_sanh"),
    st.Page("pages/05_tin_tuc_vi_mo.py", title="Tin tức & vĩ mô", url_path="tin_tuc_vi_mo"),
    st.Page("pages/06_nguon_gioi_han.py", title="Nguồn & giới hạn", url_path="nguon_gioi_han"),
])
pg.run()
