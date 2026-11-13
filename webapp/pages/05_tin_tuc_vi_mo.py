# -*- coding: utf-8 -*-
"""
Trang 5: Tin tức Thị trường & Chỉ báo Vĩ mô
- Chỉ số vĩ mô: Tăng trưởng GDP, Lạm phát CPI (World Bank), Tỷ giá USD/VND (Vietcombank)
- Lãi suất liên ngân hàng: Hiển thị "N/A" kèm ghi chú giới hạn dữ liệu nguồn
- Đối chiếu xu hướng GDP/CPI với chỉ số thị trường VN-Index
- Tin tức tài chính: Cập nhật từ RSS VnExpress, bộ lọc từ khóa, lọc theo mã VN30 liên quan và liên kết trực tiếp bài viết
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.data_loader import get_all_data
from utils.style import setup, ghi_chu, TANG, GIAM, VN30, VNINDEX

setup('Tin tức & vĩ mô', 'Tin tức & kinh tế vĩ mô')

# --- Load dữ liệu ---
data = get_all_data()
fact_vi_mo = data["fact_vi_mo"]
fact_tin = data["fact_tin"]
fact_ttm = data["fact_ttm"]
dim_cp = data["dim_cp"]
ngay_cap_nhat = data["ngay_cap_nhat"]

st.caption(f"Cập nhật dữ liệu giá đến ngày: **{ngay_cap_nhat}**")

tab_vimo, tab_tintuc = st.tabs(["Kinh tế vĩ mô", "Tin tức thị trường"])

# =========================================================================
# TAB 1: KINH TẾ VĨ MÔ
# =========================================================================
with tab_vimo:
    st.subheader("Các chỉ báo vĩ mô chính của Việt Nam")

    # Trích xuất số liệu
    df_gdp = fact_vi_mo[fact_vi_mo["loai_chi_tieu"] == "tang_truong_gdp"].sort_values("ngay")
    df_cpi = fact_vi_mo[fact_vi_mo["loai_chi_tieu"] == "lam_phat_cpi"].sort_values("ngay")
    df_usd = fact_vi_mo[fact_vi_mo["loai_chi_tieu"] == "ty_gia_usd_vnd"]

    gdp_gan = df_gdp["gia_tri"].iloc[-1] if len(df_gdp) > 0 else None
    nam_gdp = pd.to_datetime(df_gdp["ngay"].iloc[-1]).year if len(df_gdp) > 0 else ""

    cpi_gan = df_cpi["gia_tri"].iloc[-1] if len(df_cpi) > 0 else None
    nam_cpi = pd.to_datetime(df_cpi["ngay"].iloc[-1]).year if len(df_cpi) > 0 else ""

    usd_gan = df_usd["gia_tri"].iloc[-1] if len(df_usd) > 0 else None

    # KPI 4 cột
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(f"Tăng trưởng GDP ({nam_gdp})", f"{gdp_gan:.2f}%" if gdp_gan else "N/A", help="Nguồn: World Bank")
    with c2:
        st.metric(f"Lạm phát CPI ({nam_cpi})", f"{cpi_gan:.2f}%" if cpi_gan else "N/A", help="Nguồn: World Bank")
    with c3:
        st.metric("Tỷ giá USD/VND (Bán)", f"{usd_gan:,.0f} VND" if usd_gan else "N/A", help="Nguồn: Vietcombank tỷ giá hiện tại")
    with c4:
        st.metric("Lãi suất liên ngân hàng (VNIBOR)", "N/A", help="Ngân hàng Nhà nước không cung cấp API công khai miễn phí. Xem trang Nguồn & Giới hạn.")

    st.divider()

    # Biểu đồ chuỗi thời gian GDP & CPI
    st.subheader("Xu hướng Tăng trưởng GDP & Lạm phát CPI (2016 - 2025)")
    fig_macro = go.Figure()

    if len(df_gdp) > 0:
        fig_macro.add_trace(go.Bar(
            x=pd.to_datetime(df_gdp["ngay"]).dt.year.astype(str),
            y=df_gdp["gia_tri"],
            name="Tăng trưởng GDP (%)",
            marker_color="#1E88E5",
            text=df_gdp["gia_tri"].apply(lambda x: f"{x:.2f}%"),
            textposition="auto"
        ))

    if len(df_cpi) > 0:
        fig_macro.add_trace(go.Scatter(
            x=pd.to_datetime(df_cpi["ngay"]).dt.year.astype(str),
            y=df_cpi["gia_tri"],
            name="Lạm phát CPI (%)",
            line=dict(color="#E53935", width=3),
            marker=dict(size=8),
            mode="lines+markers"
        ))

    fig_macro.update_layout(
        height=380,
        yaxis_title="Tỷ lệ (%)",
        xaxis_title="Năm",
        legend=dict(orientation="h", y=1.1),
        barmode="group"
    )
    st.plotly_chart(fig_macro, use_container_width=True)

    # Đối chiếu VN-Index cuối năm với tăng trưởng GDP
    st.subheader("Tương quan diễn biến VN-Index & Bối cảnh Kinh tế")
    col_cs_vmo = "ma_chi_so" if "ma_chi_so" in fact_ttm.columns else "chi_so"
    df_vni = fact_ttm[fact_ttm[col_cs_vmo] == "VNINDEX"].sort_values("ngay").copy()
    if len(df_vni) > 0:
        fig_vni = px.line(
            df_vni,
            x="ngay",
            y="gia_dong",
            title="Diễn biến VN-Index qua các chu kỳ kinh tế (2018 - nay)",
            labels={"ngay": "Thời gian", "gia_dong": "Điểm VN-Index"}
        )
        fig_vni.update_traces(line_color="#E53935", line_width=1.8)
        fig_vni.update_layout(height=350)
        st.plotly_chart(fig_vni, use_container_width=True)

    st.info("ℹ️ **Ghi chú dữ liệu vĩ mô**: Số liệu GDP và CPI được truy vấn từ World Bank Open Data API. Lãi suất liên ngân hàng VNIBOR và chuỗi tỷ giá lịch sử hàng ngày không có API mở miễn phí nên được đánh dấu N/A.")

# =========================================================================
# TAB 2: TIN TỨC THỊ TRƯỜNG
# =========================================================================
with tab_tintuc:
    st.subheader("Dòng tin sự kiện tài chính & doanh nghiệp")

    col_f1, col_f2 = st.columns([1, 2])
    with col_f1:
        ma_filter = st.selectbox(
            "Lọc theo mã cổ phiếu liên quan",
            options=["Tất cả"] + sorted(dim_cp["ma_cp"].unique().tolist())
        )
    with col_f2:
        tu_khoa = st.text_input("🔍 Tìm kiếm theo từ khóa trong tiêu đề/nội dung", value="")

    df_tin_view = fact_tin.copy()

    # Xử lý chuỗi ngày
    if "ngay" in df_tin_view.columns and len(df_tin_view) > 0:
        df_tin_view["ngay_str"] = pd.to_datetime(df_tin_view["ngay"]).dt.strftime("%d/%m/%Y")
    else:
        df_tin_view["ngay_str"] = "N/A"

    # Lọc mã
    if ma_filter != "Tất cả":
        df_tin_view = df_tin_view[
            df_tin_view["ma_lien_quan"].astype(str).str.contains(ma_filter, na=False) |
            df_tin_view["tieu_de"].str.contains(ma_filter, case=False, na=False) |
            df_tin_view["mo_ta"].str.contains(ma_filter, case=False, na=False)
        ]

    # Lọc từ khóa
    if tu_khoa.strip():
        df_tin_view = df_tin_view[
            df_tin_view["tieu_de"].str.contains(tu_khoa, case=False, na=False) |
            df_tin_view["mo_ta"].str.contains(tu_khoa, case=False, na=False)
        ]

    st.write(f"Tìm thấy **{len(df_tin_view)}** bài viết phù hợp:")

    if len(df_tin_view) == 0:
        st.warning("Không tìm thấy tin tức nào phù hợp với bộ lọc hiện tại.")
    else:
        for idx, row in df_tin_view.head(20).iterrows():
            try:
                tieu_de = row.get("tieu_de", "Không có tiêu đề")
                url = row.get("url", "#")
                nguon = row.get("nguon", "Tin tức")
                mo_ta = row.get("mo_ta", "")
                ngay_str = row.get("ngay_str", "N/A")
                ma_lq = row.get("ma_lien_quan")

                with st.container():
                    st.markdown(f"#### [{tieu_de}]({url})")
                    ma_badge = f"🏷️ **Mã liên quan:** `{ma_lq}`" if pd.notna(ma_lq) and str(ma_lq).strip() not in ["", "nan"] else ""
                    st.caption(f"🗓️ Ngày: {ngay_str} | 📰 Nguồn: **{nguon}** {ma_badge}")
                    if pd.notna(mo_ta) and str(mo_ta).strip():
                        st.write(mo_ta)
                    st.divider()
            except Exception:
                continue
