# -*- coding: utf-8 -*-
"""
Trang 4: So sánh Cổ phiếu (Rủi ro & Lợi suất)
- Chọn từ 2 đến 5 mã cổ phiếu trong VN30
- So sánh đường Lợi suất tích lũy (%)
- Phân tích Đánh đổi Rủi ro - Lợi suất (Scatter plot: Lợi suất TB vs Độ biến động năm hóa)
- Biểu đồ Drawdown (Sụt giảm từ đỉnh)
- Ma trận hệ số tương quan (Correlation matrix heatmap)
- Tính toán hệ số Beta so với chỉ số VN30
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.data_loader import get_all_data

st.set_page_config(page_title="So sánh cổ phiếu | VN30", page_icon="⚖️", layout="wide")
st.title("⚖️ So sánh Cổ phiếu (Rủi ro - Lợi suất)")

# --- Load dữ liệu ---
data = get_all_data()
fact_loi = data["fact_loi"]
fact_gia = data["fact_gia"]
fact_cb = data["fact_cb"]
fact_ttm = data["fact_ttm"]
dim_cp = data["dim_cp"]
ngay_cap_nhat = data["ngay_cap_nhat"]

st.caption(f"📅 Cập nhật đến ngày: **{ngay_cap_nhat}**")

# --- Sidebar bộ lọc ---
st.sidebar.header("🔧 Bộ lọc")
danh_sach_ma = sorted(dim_cp["ma_cp"].unique().tolist())
mac_dinh = [m for m in ["FPT", "VCB", "HPG", "MWG"] if m in danh_sach_ma]

ma_duoc_chon = st.sidebar.multiselect(
    "Chọn 2 đến 5 mã cổ phiếu",
    options=danh_sach_ma,
    default=mac_dinh,
    max_selections=5
)

if len(ma_duoc_chon) < 2:
    st.warning("⚠️ Vui lòng chọn ít nhất **2 mã cổ phiếu** để tiến hành so sánh đối đầu.")
    st.stop()

NGAY_MIN = fact_loi["ngay"].min().date()
NGAY_MAX = fact_loi["ngay"].max().date()
ngay_bt = st.sidebar.date_input("Từ ngày", value=pd.Timestamp("2023-01-01").date(),
                                 min_value=NGAY_MIN, max_value=NGAY_MAX)
ngay_kt = st.sidebar.date_input("Đến ngày", value=NGAY_MAX,
                                 min_value=NGAY_MIN, max_value=NGAY_MAX)

if ngay_bt >= ngay_kt:
    st.error("Ngày bắt đầu phải trước ngày kết thúc.")
    st.stop()

# --- Chuẩn bị dữ liệu ---
mask_loi = (
    (fact_loi["ma_cp"].isin(ma_duoc_chon)) &
    (fact_loi["ngay"].dt.date >= ngay_bt) &
    (fact_loi["ngay"].dt.date <= ngay_kt)
)
df_loi_chon = fact_loi[mask_loi].sort_values(["ma_cp", "ngay"]).copy()

# Dữ liệu chỉ số VN30 để tính Beta
col_cs = "ma_chi_so" if "ma_chi_so" in fact_ttm.columns else "chi_so"
mask_vn30 = (
    (fact_ttm[col_cs] == "VN30") &
    (fact_ttm["ngay"].dt.date >= ngay_bt) &
    (fact_ttm["ngay"].dt.date <= ngay_kt)
)
df_vn30 = fact_ttm[mask_vn30].sort_values("ngay")[["ngay", "loi_suat"]].rename(columns={"loi_suat": "loi_suat_vn30"})

# Bảng Pivot lợi suất ngày của các mã
pivot_loi = df_loi_chon.pivot(index="ngay", columns="ma_cp", values="loi_suat").dropna()

# --- Tính toán thống kê rủi ro & lợi suất ---
thong_ke = []
palette = px.colors.qualitative.Plotly

for ma in ma_duoc_chon:
    sub_loi = df_loi_chon[df_loi_chon["ma_cp"] == ma].sort_values("ngay")
    if len(sub_loi) < 2:
        continue

    # Lợi suất tích lũy
    p_dau = sub_loi["gia_dong"].iloc[0]
    p_cuoi = sub_loi["gia_dong"].iloc[-1]
    ls_tk = (p_cuoi / p_dau - 1) * 100

    # Lợi suất TB ngày và Độ biến động năm hóa
    r_series = sub_loi["loi_suat"].dropna()
    bien_dong_nh = r_series.std() * np.sqrt(252) * 100

    # Max Drawdown trong kỳ
    sub_cb = fact_cb[
        (fact_cb["ma_cp"] == ma) &
        (fact_cb["ngay"].dt.date >= ngay_bt) &
        (fact_cb["ngay"].dt.date <= ngay_kt)
    ].sort_values("ngay")
    mdd = sub_cb["drawdown"].min() * 100 if len(sub_cb) > 0 and "drawdown" in sub_cb.columns else float("nan")

    # Tính Beta so với VN30
    merged_mkt = pd.merge(sub_loi[["ngay", "loi_suat"]], df_vn30, on="ngay").dropna()
    if len(merged_mkt) > 10 and merged_mkt["loi_suat_vn30"].var() > 0:
        cov = np.cov(merged_mkt["loi_suat"], merged_mkt["loi_suat_vn30"])[0][1]
        var_mkt = np.var(merged_mkt["loi_suat_vn30"], ddof=1)
        beta = cov / var_mkt if var_mkt > 0 else float("nan")
    else:
        beta = float("nan")

    thong_ke.append({
        "Mã CP": ma,
        "Lợi suất tích lũy (%)": ls_tk,
        "Biến động năm hóa (%)": bien_dong_nh,
        "Max Drawdown (%)": mdd,
        "Beta (vs VN30)": beta
    })

df_tk = pd.DataFrame(thong_ke)

# --- Hiển thị Bảng chỉ số tổng quan ---
st.subheader("📊 Bảng so sánh chỉ số Hiệu suất & Rủi ro")
col_format = {
    "Lợi suất tích lũy (%)": "{:+.2f}%",
    "Biến động năm hóa (%)": "{:.2f}%",
    "Max Drawdown (%)": "{:.2f}%",
    "Beta (vs VN30)": "{:.2f}"
}
st.dataframe(
    df_tk.style.format(col_format),
    use_container_width=True,
    hide_index=True
)

st.divider()

# --- Biểu đồ 1: Lợi suất tích lũy quy chuẩn (%) ---
st.subheader("📈 Lợi suất tích lũy so sánh (Chuẩn hóa từ ngày đầu kỳ)")

fig_cum = go.Figure()
for i, ma in enumerate(ma_duoc_chon):
    sub = df_loi_chon[df_loi_chon["ma_cp"] == ma].sort_values("ngay").copy()
    if len(sub) > 0:
        sub["cum_ret"] = (sub["gia_dong"] / sub["gia_dong"].iloc[0] - 1) * 100
        fig_cum.add_trace(go.Scatter(
            x=sub["ngay"],
            y=sub["cum_ret"],
            name=ma,
            line=dict(width=2.2),
            hovertemplate=f"<b>{ma}</b>: %{{y:.2f}}%<extra></extra>"
        ))

# Thêm đường VN30 làm tham chiếu
sub_v30 = fact_ttm[mask_vn30].sort_values("ngay").copy()
if len(sub_v30) > 0:
    sub_v30["cum_ret"] = (sub_v30["gia_dong"] / sub_v30["gia_dong"].iloc[0] - 1) * 100
    fig_cum.add_trace(go.Scatter(
        x=sub_v30["ngay"],
        y=sub_v30["cum_ret"],
        name="VN30 (Benchmark)",
        line=dict(color="black", width=2, dash="dash"),
        hovertemplate="<b>VN30</b>: %{y:.2f}%<extra></extra>"
    ))

fig_cum.update_layout(
    xaxis_title="Thời gian",
    yaxis_title="Lợi suất tích lũy (%)",
    height=400,
    hovermode="x unified",
    legend=dict(orientation="h", y=1.05)
)
fig_cum.add_hline(y=0, line_dash="dot", line_color="gray", opacity=0.5)
st.plotly_chart(fig_cum, use_container_width=True)

# --- Hàng 2: Scatter Rủi ro - Lợi suất & Drawdown ---
col_scatter, col_mdd = st.columns(2)

with col_scatter:
    st.subheader("🎯 Đánh đổi Lợi suất - Rủi ro")
    fig_scatter = px.scatter(
        df_tk,
        x="Biến động năm hóa (%)",
        y="Lợi suất tích lũy (%)",
        color="Mã CP",
        text="Mã CP",
        size=[18] * len(df_tk),
        labels={"Biến động năm hóa (%)": "Rủi ro: Độ biến động năm hóa (%)", "Lợi suất tích lũy (%)": "Lợi nhuận: Lợi suất tích lũy (%)"}
    )
    fig_scatter.update_traces(textposition="top center")
    fig_scatter.update_layout(height=380, showlegend=False)
    fig_scatter.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.4)
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_mdd:
    st.subheader("📉 Mức độ sụt giảm từ đỉnh (Drawdown)")
    fig_dd = go.Figure()
    for ma in ma_duoc_chon:
        sub_cb = fact_cb[
            (fact_cb["ma_cp"] == ma) &
            (fact_cb["ngay"].dt.date >= ngay_bt) &
            (fact_cb["ngay"].dt.date <= ngay_kt)
        ].sort_values("ngay")
        if len(sub_cb) > 0 and "drawdown" in sub_cb.columns:
            fig_dd.add_trace(go.Scatter(
                x=sub_cb["ngay"],
                y=sub_cb["drawdown"] * 100,
                name=ma,
                mode="lines",
                hovertemplate=f"<b>{ma}</b> DD: %{{y:.2f}}%<extra></extra>"
            ))
    fig_dd.update_layout(
        xaxis_title="Ngày",
        yaxis_title="Drawdown (%)",
        height=380,
        hovermode="x unified",
        legend=dict(orientation="h", y=1.1)
    )
    st.plotly_chart(fig_dd, use_container_width=True)

# --- Hàng 3: Ma trận tương quan ---
st.subheader("🔗 Ma trận Hệ số Tương quan Lợi suất")
if len(pivot_loi.columns) >= 2:
    corr_matrix = pivot_loi.corr().round(2)
    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        zmin=-1, zmax=1,
        title="Hệ số tương quan Pearson giữa lợi suất ngày"
    )
    fig_corr.update_layout(height=400)
    st.plotly_chart(fig_corr, use_container_width=True)
else:
    st.info("Không đủ dữ liệu chung ngày để tính ma trận tương quan.")
