# -*- coding: utf-8 -*-
"""
Trang 3: Phân tích Báo cáo Tài chính & Chỉ số Cơ bản
- ROE, ROA, Đòn bẩy tài chính (Nợ/VCSH, Vay/VCSH)
- Doanh nghiệp phi tài chính: Biên LN gộp, Biên LN ròng, Doanh thu, LNST
- Ngân hàng: Tỷ lệ CIR, LDR xấp xỉ, NIM (NII/TSBQ)
- So sánh chỉ số cơ bản trong cùng nhóm ngành
- Xử lý N/A đối với công ty chứng khoán (SSI, TCX) hoặc thiếu dữ liệu
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.data_loader import get_all_data

st.set_page_config(page_title="Báo cáo Tài chính | VN30", page_icon="📋", layout="wide")
st.title("📋 Phân tích Báo cáo Tài chính & Cơ bản")

# --- Load dữ liệu ---
data = get_all_data()
fact_tc = data["fact_tc"]
dim_cp = data["dim_cp"]
ngay_cap_nhat = data["ngay_cap_nhat"]

st.caption(f"📅 Cập nhật dữ liệu giá đến ngày: **{ngay_cap_nhat}** | Dữ liệu BCTC: **2022 - 2025**")

# Kết hợp với dim_co_phieu để có ngành và tên công ty
df_all = fact_tc.merge(
    dim_cp[["ma_cp", "ten_cong_ty", "nganh_cap1", "mau_bctc"]],
    on="ma_cp",
    how="right"
)

# --- Sidebar bộ lọc ---
st.sidebar.header("🔧 Bộ lọc")
danh_sach_ma = sorted(dim_cp["ma_cp"].unique().tolist())
ma_chon = st.sidebar.selectbox(
    "Chọn mã cổ phiếu",
    danh_sach_ma,
    index=danh_sach_ma.index("HPG") if "HPG" in danh_sach_ma else 0
)

thong_tin_cp = dim_cp[dim_cp["ma_cp"] == ma_chon].iloc[0]
ten_ct = thong_tin_cp["ten_cong_ty"]
nganh_ct = thong_tin_cp["nganh_cap1"]
mau_bctc = thong_tin_cp["mau_bctc"]

st.sidebar.markdown(f"**Công ty:** {ten_ct}")
st.sidebar.markdown(f"**Ngành:** {nganh_ct}")
st.sidebar.markdown(f"**Mẫu BCTC:** `{mau_bctc}`")

# Kiểm tra trường hợp đặc biệt: Công ty Chứng khoán (CK) như SSI, TCX
if mau_bctc == "CK":
    st.warning(f"⚠️ **{ma_chon}** là công ty Chứng khoán (`mau_bctc = 'CK'`). Hiện tại mô hình dữ liệu tài chính chưa hỗ trợ chuẩn hóa chỉ số riêng cho nhóm CTCK. Các chỉ số cơ bản hiển thị **N/A**.")

df_cp = df_all[df_all["ma_cp"] == ma_chon].sort_values("nam").copy()

# --- Tab hiển thị: Chi tiết mã & So sánh ngành ---
tab_chitiet, tab_nganh = st.tabs(["📊 Chi tiết doanh nghiệp", "🏢 So sánh trong ngành"])

with tab_chitiet:
    if len(df_cp.dropna(subset=["tong_tai_san"])) == 0:
        st.info(f"Không có dữ liệu BCTC cho mã **{ma_chon}**.")
    else:
        nam_gan_nhat = df_cp["nam"].dropna().max()
        row_gan_nhat = df_cp[df_cp["nam"] == nam_gan_nhat].iloc[0]

        # --- KPI Cards ---
        st.subheader(f"📌 Chỉ số trọng yếu năm {int(nam_gan_nhat) if pd.notna(nam_gan_nhat) else 'N/A'}")
        c1, c2, c3, c4 = st.columns(4)

        roe_val = row_gan_nhat.get("roe")
        roa_val = row_gan_nhat.get("roa")
        de_val = row_gan_nhat.get("no_tren_von_chu")
        lnst_val = row_gan_nhat.get("lnst")

        with c1:
            st.metric("📈 ROE", f"{roe_val * 100:.2f}%" if pd.notna(roe_val) else "N/A")
        with c2:
            st.metric("📊 ROA", f"{roa_val * 100:.2f}%" if pd.notna(roa_val) else "N/A")
        with c3:
            st.metric("⚖️ Nợ / Vốn chủ sở hữu", f"{de_val:.2f}x" if pd.notna(de_val) else "N/A")
        with c4:
            st.metric("💰 LNST (tỷ đồng)", f"{lnst_val / 1e9:,.0f}" if pd.notna(lnst_val) else "N/A")

        st.divider()

        # --- Biểu đồ xu hướng tài chính ---
        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.subheader("📈 Hiệu quả sinh lời (ROE & ROA)")
            fig_roe = go.Figure()
            df_plot_roe = df_cp.dropna(subset=["nam"])
            fig_roe.add_trace(go.Bar(
                x=df_plot_roe["nam"].astype(str),
                y=df_plot_roe["roe"] * 100,
                name="ROE (%)",
                marker_color="#2E7D32",
                text=df_plot_roe["roe"].apply(lambda x: f"{x*100:.1f}%" if pd.notna(x) else ""),
                textposition="auto"
            ))
            fig_roe.add_trace(go.Bar(
                x=df_plot_roe["nam"].astype(str),
                y=df_plot_roe["roa"] * 100,
                name="ROA (%)",
                marker_color="#81C784",
                text=df_plot_roe["roa"].apply(lambda x: f"{x*100:.1f}%" if pd.notna(x) else ""),
                textposition="auto"
            ))
            fig_roe.update_layout(
                barmode="group",
                height=350,
                yaxis_title="Tỷ lệ (%)",
                xaxis_title="Năm",
                legend=dict(orientation="h", y=1.1)
            )
            st.plotly_chart(fig_roe, use_container_width=True)

        with col_chart2:
            if mau_bctc == "NH":
                st.subheader("🏦 Hiệu quả hoạt động Ngân hàng (CIR & LDR)")
                fig_nh = go.Figure()
                fig_nh.add_trace(go.Scatter(
                    x=df_plot_roe["nam"].astype(str),
                    y=df_plot_roe["cir"] * 100,
                    name="Tỷ lệ CIR (%)",
                    line=dict(color="#FF9800", width=3),
                    marker=dict(size=8),
                    mode="lines+markers"
                ))
                fig_nh.add_trace(go.Scatter(
                    x=df_plot_roe["nam"].astype(str),
                    y=df_plot_roe["ldr_xap_xi"] * 100,
                    name="LDR xấp xỉ (%)",
                    line=dict(color="#1976D2", width=3, dash="dot"),
                    marker=dict(size=8),
                    mode="lines+markers"
                ))
                fig_nh.update_layout(
                    height=350,
                    yaxis_title="Tỷ lệ (%)",
                    xaxis_title="Năm",
                    legend=dict(orientation="h", y=1.1)
                )
                st.plotly_chart(fig_nh, use_container_width=True)
            else:
                st.subheader("🏭 Biên lợi nhuận Doanh nghiệp")
                fig_bien = go.Figure()
                fig_bien.add_trace(go.Scatter(
                    x=df_plot_roe["nam"].astype(str),
                    y=df_plot_roe["bien_loi_nhuan_gop"] * 100,
                    name="Biên LN gộp (%)",
                    line=dict(color="#1E88E5", width=3),
                    mode="lines+markers"
                ))
                fig_bien.add_trace(go.Scatter(
                    x=df_plot_roe["nam"].astype(str),
                    y=df_plot_roe["bien_loi_nhuan_rong"] * 100,
                    name="Biên LN ròng (%)",
                    line=dict(color="#43A047", width=3),
                    mode="lines+markers"
                ))
                fig_bien.update_layout(
                    height=350,
                    yaxis_title="Tỷ lệ (%)",
                    xaxis_title="Năm",
                    legend=dict(orientation="h", y=1.1)
                )
                st.plotly_chart(fig_bien, use_container_width=True)

        # --- Bảng số liệu chi tiết ---
        st.subheader("📑 Bảng cân đối & Kết quả kinh doanh tóm tắt")
        cols_hien_thi = ["nam", "tong_tai_san", "von_chu", "no_phai_tra", "lnst"]
        if mau_bctc == "DN":
            cols_hien_thi += ["doanh_thu_thuan", "bien_loi_nhuan_gop", "bien_loi_nhuan_rong"]
        elif mau_bctc == "NH":
            cols_hien_thi += ["cho_vay_kh", "tien_gui_kh", "cir", "ldr_xap_xi"]

        df_table = df_cp[cols_hien_thi].copy().sort_values("nam", ascending=False)
        for col_ty in ["tong_tai_san", "von_chu", "no_phai_tra", "lnst", "doanh_thu_thuan", "cho_vay_kh", "tien_gui_kh"]:
            if col_ty in df_table.columns:
                df_table[col_ty] = df_table[col_ty].apply(lambda x: f"{x/1e9:,.0f} tỷ" if pd.notna(x) else "N/A")

        for col_pct in ["bien_loi_nhuan_gop", "bien_loi_nhuan_rong", "cir", "ldr_xap_xi"]:
            if col_pct in df_table.columns:
                df_table[col_pct] = df_table[col_pct].apply(lambda x: f"{x*100:.2f}%" if pd.notna(x) else "N/A")

        df_table = df_table.rename(columns={
            "nam": "Năm", "tong_tai_san": "Tổng tài sản", "von_chu": "Vốn chủ sở hữu",
            "no_phai_tra": "Nợ phải trả", "lnst": "LNST",
            "doanh_thu_thuan": "Doanh thu thuần", "bien_loi_nhuan_gop": "Biên LN gộp",
            "bien_loi_nhuan_rong": "Biên LN ròng", "cho_vay_kh": "Cho vay KH",
            "tien_gui_kh": "Tiền gửi KH", "cir": "CIR", "ldr_xap_xi": "LDR xấp xỉ"
        })
        st.dataframe(df_table, use_container_width=True, hide_index=True)

with tab_nganh:
    st.subheader(f"🏢 So sánh các mã cùng ngành: {nganh_ct}")
    df_nganh = df_all[df_all["nganh_cap1"] == nganh_ct].copy()
    nam_so_sanh = st.selectbox(
        "Chọn năm so sánh",
        sorted(df_nganh["nam"].dropna().unique().astype(int).tolist(), reverse=True),
        index=0
    )

    df_nganh_nam = df_nganh[df_nganh["nam"] == nam_so_sanh].copy()
    if len(df_nganh_nam) == 0:
        st.info("Không có dữ liệu cho năm này.")
    else:
        c_ng1, c_ng2 = st.columns(2)
        with c_ng1:
            fig_ss_roe = px.bar(
                df_nganh_nam.sort_values("roe", ascending=False),
                x="ma_cp", y=df_nganh_nam["roe"] * 100,
                color="ma_cp",
                title=f"So sánh ROE (%) năm {nam_so_sanh}",
                labels={"y": "ROE (%)", "ma_cp": "Mã CP"},
                text_auto=".1f"
            )
            fig_ss_roe.update_layout(showlegend=False, height=350)
            st.plotly_chart(fig_ss_roe, use_container_width=True)

        with c_ng2:
            fig_ss_de = px.bar(
                df_nganh_nam.sort_values("no_tren_von_chu", ascending=False),
                x="ma_cp", y="no_tren_von_chu",
                color="ma_cp",
                title=f"Đòn bẩy (Nợ / VCSH) năm {nam_so_sanh}",
                labels={"no_tren_von_chu": "Nợ / VCSH (lần)", "ma_cp": "Mã CP"},
                text_auto=".2f"
            )
            fig_ss_de.update_layout(showlegend=False, height=350)
            st.plotly_chart(fig_ss_de, use_container_width=True)

        # Bảng so sánh toàn ngành
        st.markdown(f"**Bảng tổng hợp chỉ số tài chính nhóm ngành {nganh_ct} ({nam_so_sanh})**")
        cols_view = ["ma_cp", "ten_cong_ty", "roe", "roa", "no_tren_von_chu", "lnst"]
        df_nganh_view = df_nganh_nam[cols_view].copy()
        df_nganh_view["roe"] = df_nganh_view["roe"].apply(lambda x: f"{x*100:.2f}%" if pd.notna(x) else "N/A")
        df_nganh_view["roa"] = df_nganh_view["roa"].apply(lambda x: f"{x*100:.2f}%" if pd.notna(x) else "N/A")
        df_nganh_view["no_tren_von_chu"] = df_nganh_view["no_tren_von_chu"].apply(lambda x: f"{x:.2f}x" if pd.notna(x) else "N/A")
        df_nganh_view["lnst"] = df_nganh_view["lnst"].apply(lambda x: f"{x/1e9:,.0f} tỷ" if pd.notna(x) else "N/A")

        df_nganh_view = df_nganh_view.rename(columns={
            "ma_cp": "Mã CP", "ten_cong_ty": "Tên công ty",
            "roe": "ROE", "roa": "ROA",
            "no_tren_von_chu": "Nợ / VCSH", "lnst": "LNST"
        })
        st.dataframe(df_nganh_view, use_container_width=True, hide_index=True)
