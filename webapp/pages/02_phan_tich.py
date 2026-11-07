# -*- coding: utf-8 -*-
"""
Trang 2: Phân tích cổ phiếu chi tiết
- Biểu đồ nến (Candlestick) + MA20/50/200
- Khối lượng giao dịch
- RSI14
- MACD + Signal + Histogram
- Cảnh báo điều chỉnh giá bất thường
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.data_loader import get_all_data, CANH_BAO_GIA

st.set_page_config(page_title="Phân tích cổ phiếu | VN30", page_icon="📈", layout="wide")
st.title("📈 Phân tích Cổ phiếu")

data = get_all_data()
fact_gia = data["fact_gia"]
fact_cb = data["fact_cb"]
dim_cp = data["dim_cp"]
ngay_cap_nhat = data["ngay_cap_nhat"]

st.caption(f"📅 Cập nhật đến ngày: **{ngay_cap_nhat}**")

# --- Sidebar bộ lọc ---
st.sidebar.header("🔧 Bộ lọc")
danh_sach_ma = sorted(dim_cp["ma_cp"].tolist())
ma_chon = st.sidebar.selectbox("Chọn mã cổ phiếu", danh_sach_ma, index=danh_sach_ma.index("FPT") if "FPT" in danh_sach_ma else 0)

ten_ct = dim_cp[dim_cp["ma_cp"] == ma_chon]["ten_cong_ty"].values[0]
st.sidebar.markdown(f"**{ten_ct}**")

NGAY_MIN = fact_gia["ngay"].min().date()
NGAY_MAX = fact_gia["ngay"].max().date()
ngay_bt = st.sidebar.date_input("Từ ngày", value=pd.Timestamp("2023-01-01").date(),
                                 min_value=NGAY_MIN, max_value=NGAY_MAX)
ngay_kt = st.sidebar.date_input("Đến ngày", value=NGAY_MAX,
                                 min_value=NGAY_MIN, max_value=NGAY_MAX)

# --- Lọc dữ liệu ---
df_g = fact_gia[
    (fact_gia["ma_cp"] == ma_chon) &
    (fact_gia["ngay"].dt.date >= ngay_bt) &
    (fact_gia["ngay"].dt.date <= ngay_kt)
].sort_values("ngay").copy()

df_cb = fact_cb[
    (fact_cb["ma_cp"] == ma_chon) &
    (fact_cb["ngay"].dt.date >= ngay_bt) &
    (fact_cb["ngay"].dt.date <= ngay_kt)
].sort_values("ngay").copy()

if len(df_g) == 0:
    st.warning("Không có dữ liệu cho mã và khoảng thời gian này.")
    st.stop()

# --- Kiểm tra cảnh báo ---
for (ma, ngay_str), msg in CANH_BAO_GIA.items():
    if ma == ma_chon:
        ngay_dt = pd.Timestamp(ngay_str).date()
        if ngay_bt <= ngay_dt <= ngay_kt:
            st.warning(f"**{ma} — {ngay_str}**: {msg}")

# --- KPI nhanh ---
gia_hien_tai = df_g["gia_dong"].iloc[-1]
gia_dau_ky = df_g["gia_dong"].iloc[0]
ls_ky = (gia_hien_tai / gia_dau_ky - 1) * 100
kl_tb = df_g["khoi_luong"].mean()

c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Giá đóng cửa (nghìn đ)", f"{gia_hien_tai:.2f}")
c2.metric("📊 Lợi suất tích lũy kỳ", f"{ls_ky:+.2f}%")
c3.metric("📦 KL TB/ngày (cp)", f"{kl_tb:,.0f}")
rsi_gan = df_cb["rsi14"].dropna().iloc[-1] if len(df_cb) > 0 and "rsi14" in df_cb.columns else float("nan")
rsi_text = f"{rsi_gan:.1f}" if not pd.isna(rsi_gan) else "N/A"
rsi_note = "Quá mua" if not pd.isna(rsi_gan) and rsi_gan > 70 else ("Quá bán" if not pd.isna(rsi_gan) and rsi_gan < 30 else "Trung tính")
c4.metric("📉 RSI14 (gần nhất)", rsi_text, delta=rsi_note)

st.divider()

# --- Biểu đồ tổng hợp: Nến + MA + KL + RSI + MACD ---
fig = make_subplots(
    rows=4, cols=1,
    shared_xaxes=True,
    row_heights=[0.5, 0.15, 0.175, 0.175],
    vertical_spacing=0.03,
    subplot_titles=["Giá (nghìn đồng)", "Khối lượng (cổ phiếu)", "RSI14", "MACD"],
)

# Panel 1: Nến
fig.add_trace(go.Candlestick(
    x=df_g["ngay"],
    open=df_g["gia_mo"], high=df_g["gia_cao"],
    low=df_g["gia_thap"], close=df_g["gia_dong"],
    name="Giá", increasing_line_color="#4CAF50", decreasing_line_color="#F44336"
), row=1, col=1)

# MA20, MA50, MA200
for col_ma, mau, do_day in [("ma20", "#FF9800", 1.5), ("ma50", "#2196F3", 1.5), ("ma200", "#9C27B0", 1.5)]:
    if col_ma in df_cb.columns:
        fig.add_trace(go.Scatter(
            x=df_cb["ngay"], y=df_cb[col_ma],
            name=col_ma.upper(), line=dict(color=mau, width=do_day),
            hovertemplate=f"{col_ma.upper()}: %{{y:.2f}}<extra></extra>"
        ), row=1, col=1)

# Panel 2: Khối lượng
mau_kl = ["#4CAF50" if r > 0 else "#F44336"
           for r in (df_g["gia_dong"] - df_g["gia_mo"])]
fig.add_trace(go.Bar(
    x=df_g["ngay"], y=df_g["khoi_luong"],
    name="Khối lượng", marker_color=mau_kl, showlegend=False
), row=2, col=1)

# Panel 3: RSI
if "rsi14" in df_cb.columns:
    fig.add_trace(go.Scatter(
        x=df_cb["ngay"], y=df_cb["rsi14"],
        name="RSI14", line=dict(color="#FF9800", width=1.5)
    ), row=3, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5, row=3, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5, row=3, col=1)
    fig.add_hline(y=50, line_dash="dot", line_color="gray", opacity=0.3, row=3, col=1)

# Panel 4: MACD
if "macd" in df_cb.columns and "macd_tin_hieu" in df_cb.columns:
    fig.add_trace(go.Scatter(
        x=df_cb["ngay"], y=df_cb["macd"],
        name="MACD", line=dict(color="#2196F3", width=1.5)
    ), row=4, col=1)
    fig.add_trace(go.Scatter(
        x=df_cb["ngay"], y=df_cb["macd_tin_hieu"],
        name="Signal", line=dict(color="#FF5722", width=1.5, dash="dash")
    ), row=4, col=1)
    if "macd_phan_ky" in df_cb.columns:
        mau_hist = ["#4CAF50" if v >= 0 else "#F44336" for v in df_cb["macd_phan_ky"].fillna(0)]
        fig.add_trace(go.Bar(
            x=df_cb["ngay"], y=df_cb["macd_phan_ky"],
            name="Histogram", marker_color=mau_hist, showlegend=False, opacity=0.6
        ), row=4, col=1)

fig.update_layout(
    title=f"{ma_chon} — {ten_ct}",
    height=800,
    hovermode="x unified",
    xaxis_rangeslider_visible=False,
    legend=dict(orientation="h", y=1.02),
)
fig.update_yaxes(title_text="Giá (nghìn đ)", row=1, col=1)
fig.update_yaxes(title_text="Khối lượng", row=2, col=1)
fig.update_yaxes(title_text="RSI", row=3, col=1, range=[0, 100])
fig.update_yaxes(title_text="MACD", row=4, col=1)

st.plotly_chart(fig, use_container_width=True)

# --- Bảng dữ liệu gần nhất (20 phiên) ---
with st.expander("📋 Dữ liệu 20 phiên gần nhất"):
    hien_thi = df_g.tail(20)[["ngay", "gia_mo", "gia_cao", "gia_thap", "gia_dong", "khoi_luong"]].copy()
    hien_thi["ngay"] = hien_thi["ngay"].dt.strftime("%d/%m/%Y")
    hien_thi = hien_thi.rename(columns={
        "ngay": "Ngày", "gia_mo": "Mở cửa", "gia_cao": "Cao",
        "gia_thap": "Thấp", "gia_dong": "Đóng cửa", "khoi_luong": "Khối lượng"
    })
    st.dataframe(hien_thi.iloc[::-1].reset_index(drop=True), use_container_width=True)
