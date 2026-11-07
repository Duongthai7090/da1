# -*- coding: utf-8 -*-
"""
Trang 1: Tổng quan thị trường VN30 và ngành
- KPI: lợi suất VN30, VN-Index, thanh khoản, số mã tăng/giảm
- Đường lợi suất tích lũy VN30 vs VN-Index
- Top 5 tăng/giảm phiên gần nhất
- Heatmap lợi suất theo ngành
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.data_loader import get_all_data

st.set_page_config(page_title="Tổng quan | VN30", page_icon="🏠", layout="wide")
st.title("🏠 Tổng quan VN30 & Ngành")

# --- Load dữ liệu ---
data = get_all_data()
fact_ttm = data["fact_ttm"]
fact_loi = data["fact_loi"]
fact_gia = data["fact_gia"]
dim_cp = data["dim_cp"]
ngay_cap_nhat = data["ngay_cap_nhat"]

st.caption(f"📅 Cập nhật đến ngày: **{ngay_cap_nhat}**")

# --- Bộ lọc sidebar ---
st.sidebar.header("🔧 Bộ lọc")
NGAY_MIN = fact_loi["ngay"].min().date()
NGAY_MAX = fact_loi["ngay"].max().date()

ngay_bat_dau = st.sidebar.date_input("Từ ngày", value=pd.Timestamp("2023-01-01").date(),
                                      min_value=NGAY_MIN, max_value=NGAY_MAX)
ngay_ket_thuc = st.sidebar.date_input("Đến ngày", value=NGAY_MAX,
                                       min_value=NGAY_MIN, max_value=NGAY_MAX)

# --- Lọc dữ liệu theo khoảng thời gian ---
mask_ttm = (fact_ttm["ngay"].dt.date >= ngay_bat_dau) & (fact_ttm["ngay"].dt.date <= ngay_ket_thuc)
df_ttm = fact_ttm[mask_ttm].copy()
mask_loi = (fact_loi["ngay"].dt.date >= ngay_bat_dau) & (fact_loi["ngay"].dt.date <= ngay_ket_thuc)
df_loi = fact_loi[mask_loi].copy()
mask_gia = (fact_gia["ngay"].dt.date >= ngay_bat_dau) & (fact_gia["ngay"].dt.date <= ngay_ket_thuc)
df_gia = fact_gia[mask_gia].copy()

# Gộp với dim_cp để có ngành
df_loi = df_loi.merge(dim_cp[["ma_cp", "nganh_cap1", "ten_cong_ty"]], on="ma_cp", how="left")
df_gia = df_gia.merge(dim_cp[["ma_cp", "nganh_cap1"]], on="ma_cp", how="left")

# --- KPI ---
def tinh_loi_suat_tich_luy(df_chi_so, ten_chi_so: str) -> float:
    """Tính lợi suất tích lũy (%) trong khoảng thời gian."""
    col_name = "ma_chi_so" if "ma_chi_so" in df_chi_so.columns else "chi_so"
    sub = df_chi_so[df_chi_so[col_name] == ten_chi_so].sort_values("ngay")
    if len(sub) < 2:
        return float("nan")
    r = (sub["gia_dong"].iloc[-1] / sub["gia_dong"].iloc[0] - 1) * 100
    return r


ls_vn30 = tinh_loi_suat_tich_luy(df_ttm, "VN30")
ls_vni = tinh_loi_suat_tich_luy(df_ttm, "VNINDEX")

# Thanh khoản trung bình (khối lượng trung bình ngày của 30 mã)
kl_tb = df_gia.groupby("ngay")["khoi_luong"].sum().mean() if len(df_gia) > 0 else 0

# Phiên gần nhất: số mã tăng/giảm
ngay_gan_nhat = df_loi["ngay"].max() if len(df_loi) > 0 else None
if ngay_gan_nhat is not None:
    df_phien_cuoi = df_loi[df_loi["ngay"] == ngay_gan_nhat]
    so_tang = (df_phien_cuoi["loi_suat"] > 0).sum()
    so_giam = (df_phien_cuoi["loi_suat"] < 0).sum()
    so_dung = (df_phien_cuoi["loi_suat"] == 0).sum()
else:
    so_tang = so_giam = so_dung = 0

col1, col2, col3, col4, col5 = st.columns(5)
def fmt_pct(v):
    if pd.isna(v): return "N/A"
    sign = "+" if v >= 0 else ""
    return f"{sign}{v:.2f}%"

with col1:
    delta = fmt_pct(ls_vn30)
    color = "normal" if pd.isna(ls_vn30) else ("normal" if ls_vn30 >= 0 else "inverse")
    st.metric("📊 VN30 Index (lợi suất TK)", fmt_pct(ls_vn30),
              delta=None, help="Lợi suất tích lũy VN30 trong khoảng thời gian chọn")
with col2:
    st.metric("📈 VN-Index (lợi suất TK)", fmt_pct(ls_vni))
with col3:
    st.metric("💹 Thanh khoản TB/ngày (CP)", f"{kl_tb/1e6:.1f}M cp")
with col4:
    st.metric("🟢 Số mã tăng (phiên gần nhất)", f"{so_tang}", delta=None)
with col5:
    st.metric("🔴 Số mã giảm (phiên gần nhất)", f"{so_giam}", delta=None)

st.divider()

# --- Biểu đồ 1: Lợi suất tích lũy VN30 vs VN-Index ---
st.subheader("📈 Lợi suất tích lũy VN30 vs VN-Index")

if len(df_ttm) > 0:
    fig_ls = go.Figure()
    col_idx = "ma_chi_so" if "ma_chi_so" in df_ttm.columns else "chi_so"
    for chi_so, mau, ten in [
        ("VN30", "#1976D2", "VN30 Index"),
        ("VNINDEX", "#E53935", "VN-Index"),
    ]:
        sub = df_ttm[df_ttm[col_idx] == chi_so].sort_values("ngay").copy()
        if len(sub) > 0:
            sub["loi_suat_tk"] = (sub["gia_dong"] / sub["gia_dong"].iloc[0] - 1) * 100
            fig_ls.add_trace(go.Scatter(
                x=sub["ngay"], y=sub["loi_suat_tk"],
                name=ten, line=dict(color=mau, width=2),
                hovertemplate="%{x|%d/%m/%Y}<br>%{y:.2f}%<extra></extra>"
            ))
    fig_ls.update_layout(
        title="Lợi suất tích lũy (%) — cơ sở = ngày đầu kỳ",
        xaxis_title="Ngày", yaxis_title="Lợi suất tích lũy (%)",
        legend=dict(x=0.01, y=0.99), hovermode="x unified",
        height=380
    )
    fig_ls.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    st.plotly_chart(fig_ls, use_container_width=True)
else:
    st.warning("Không có dữ liệu chỉ số thị trường trong khoảng thời gian này.")

# --- Biểu đồ 2 & 3: Top tăng/giảm + Heatmap ngành ---
col_top, col_heat = st.columns([1, 2])

with col_top:
    st.subheader("🏆 Top tăng/giảm (kỳ chọn)")
    if len(df_loi) > 0:
        # Lợi suất tích lũy từng mã trong kỳ
        ls_ky = df_loi.groupby(["ma_cp", "ten_cong_ty"]).apply(
            lambda g: (
                g.sort_values("ngay")["gia_dong"].iloc[-1] /
                g.sort_values("ngay")["gia_dong"].iloc[0] - 1
            ) * 100
        ).reset_index(name="loi_suat_ky")
        ls_ky = ls_ky.sort_values("loi_suat_ky", ascending=False)

        top5_tang = ls_ky.head(5)
        top5_giam = ls_ky.tail(5).sort_values("loi_suat_ky")

        fig_top = go.Figure()
        fig_top.add_trace(go.Bar(
            x=top5_tang["loi_suat_ky"],
            y=top5_tang["ma_cp"],
            orientation="h", name="Top tăng",
            marker_color="#4CAF50",
            hovertemplate="%{y}: %{x:.2f}%<extra></extra>"
        ))
        fig_top.add_trace(go.Bar(
            x=top5_giam["loi_suat_ky"],
            y=top5_giam["ma_cp"],
            orientation="h", name="Top giảm",
            marker_color="#F44336",
            hovertemplate="%{y}: %{x:.2f}%<extra></extra>"
        ))
        fig_top.update_layout(
            title="Top 5 tăng/giảm (lợi suất tích lũy %)",
            barmode="overlay", height=380,
            xaxis_title="Lợi suất tích lũy (%)", yaxis_title="",
            margin=dict(l=60)
        )
        fig_top.add_vline(x=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig_top, use_container_width=True)

with col_heat:
    st.subheader("🔥 Heatmap lợi suất theo ngành (phiên gần nhất)")
    if ngay_gan_nhat is not None and len(df_phien_cuoi) > 0:
        heat_df = df_phien_cuoi.copy()
        heat_df["loi_suat_pct"] = heat_df["loi_suat"] * 100
        heat_df["ten_hien_thi"] = heat_df["ma_cp"] + "<br>" + heat_df["loi_suat_pct"].apply(
            lambda x: f"+{x:.2f}%" if x > 0 else f"{x:.2f}%"
        )
        fig_heat = px.treemap(
            heat_df,
            path=["nganh_cap1", "ma_cp"],
            values=heat_df["khoi_luong"].clip(lower=1),
            color="loi_suat_pct",
            color_continuous_scale=["#F44336", "#FFF176", "#4CAF50"],
            color_continuous_midpoint=0,
            custom_data=["ten_cong_ty", "loi_suat_pct"],
            title=f"Heatmap theo ngành — {ngay_gan_nhat.strftime('%d/%m/%Y') if hasattr(ngay_gan_nhat, 'strftime') else ngay_gan_nhat}",
        )
        fig_heat.update_traces(
            texttemplate="%{label}<br>%{customdata[1]:.2f}%",
            hovertemplate="<b>%{label}</b><br>%{customdata[0]}<br>Lợi suất: %{customdata[1]:.2f}%<extra></extra>"
        )
        fig_heat.update_layout(height=380, coloraxis_colorbar=dict(title="Lợi suất (%)"))
        st.plotly_chart(fig_heat, use_container_width=True)
    else:
        st.info("Chưa có dữ liệu phiên gần nhất.")

# --- Bảng lợi suất ngày gần nhất ---
st.subheader(f"📋 Chi tiết phiên gần nhất ({ngay_gan_nhat.strftime('%d/%m/%Y') if ngay_gan_nhat and hasattr(ngay_gan_nhat, 'strftime') else 'N/A'})")
if ngay_gan_nhat is not None:
    bang = df_phien_cuoi[["ma_cp", "ten_cong_ty", "nganh_cap1", "gia_dong", "loi_suat", "khoi_luong"]].copy()
    bang["loi_suat_%"] = (bang["loi_suat"] * 100).round(2)
    bang["gia_dong"] = bang["gia_dong"].round(2)
    bang["khoi_luong"] = bang["khoi_luong"].apply(lambda x: f"{x:,.0f}")
    bang = bang.rename(columns={
        "ma_cp": "Mã", "ten_cong_ty": "Tên công ty",
        "nganh_cap1": "Ngành", "gia_dong": "Giá đóng (nghìn đ)",
        "loi_suat_%": "Lợi suất (%)", "khoi_luong": "Khối lượng"
    })
    bang = bang[["Mã", "Tên công ty", "Ngành", "Giá đóng (nghìn đ)", "Lợi suất (%)", "Khối lượng"]]
    bang = bang.sort_values("Lợi suất (%)", ascending=False).reset_index(drop=True)

    def to_style(val):
        if isinstance(val, (int, float)):
            if val > 0: return "color: #4CAF50; font-weight: bold"
            elif val < 0: return "color: #F44336; font-weight: bold"
            return "color: #FFC107"
        return ""

    st.dataframe(
        bang.style.applymap(to_style, subset=["Lợi suất (%)"]),
        use_container_width=True, height=350
    )
