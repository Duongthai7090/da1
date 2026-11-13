# -*- coding: utf-8 -*-
"""
Trang 1: Tổng quan thị trường VN30 và ngành
- KPI: lợi suất, biến động, drawdown, thanh khoản, độ rộng thị trường
- Lợi suất tích lũy VN30 vs VN-Index, drawdown
- Độ rộng thị trường (số mã tăng/giảm, % mã trên MA50/MA200)
- Hiệu suất theo ngành, top tăng/giảm, heatmap, bảng chi tiết
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.data_loader import get_all_data
from utils.style import setup, ghi_chu, TANG, GIAM, VN30, VNINDEX

data = get_all_data()
fact_ttm, fact_loi, fact_gia = data["fact_ttm"], data["fact_loi"], data["fact_gia"]
fact_cb, dim_cp = data["fact_cb"], data["dim_cp"]
setup("Tổng quan", "Tổng quan VN30 & ngành", data["ngay_cap_nhat"], "Nguồn: vnstock (KBS)")

# --- Bộ lọc ---
st.sidebar.markdown("**Bộ lọc**")
NGAY_MIN, NGAY_MAX = fact_loi["ngay"].min().date(), fact_loi["ngay"].max().date()
ngay_bat_dau = st.sidebar.date_input("Từ ngày", value=pd.Timestamp("2023-01-01").date(),
                                     min_value=NGAY_MIN, max_value=NGAY_MAX)
ngay_ket_thuc = st.sidebar.date_input("Đến ngày", value=NGAY_MAX,
                                      min_value=NGAY_MIN, max_value=NGAY_MAX)


def loc(df):
    d = df["ngay"].dt.date
    return df[(d >= ngay_bat_dau) & (d <= ngay_ket_thuc)].copy()


df_ttm, df_loi, df_gia, df_cb = loc(fact_ttm), loc(fact_loi), loc(fact_gia), loc(fact_cb)
df_loi = df_loi.merge(dim_cp[["ma_cp", "nganh_cap1", "ten_cong_ty"]], on="ma_cp", how="left")
if len(df_loi) == 0:
    st.warning("Không có dữ liệu trong khoảng thời gian này.")
    st.stop()


def chuoi_chi_so(ma):
    s = df_ttm[df_ttm["ma_chi_so"] == ma].sort_values("ngay").reset_index(drop=True)
    return s


vn30, vni = chuoi_chi_so("VN30"), chuoi_chi_so("VNINDEX")


def ls_tich_luy(s):
    return (s["gia_dong"].iloc[-1] / s["gia_dong"].iloc[0] - 1) * 100 if len(s) > 1 else np.nan


def bien_dong(s):  # độ lệch chuẩn lợi suất ngày, năm hóa
    return s["gia_dong"].pct_change().std() * np.sqrt(252) * 100 if len(s) > 2 else np.nan


def drawdown(s):
    return (s["gia_dong"] / s["gia_dong"].cummax() - 1) * 100


def pct(v):
    return "N/A" if pd.isna(v) else f"{v:+.1f}%"


# Phiên gần nhất
ngay_cuoi = df_loi["ngay"].max()
phien = df_loi[df_loi["ngay"] == ngay_cuoi]
so_tang, so_giam = int((phien["loi_suat"] > 0).sum()), int((phien["loi_suat"] < 0).sum())
kl_tb = df_gia.groupby("ngay")["khoi_luong"].sum().mean() / 1e6 if len(df_gia) else 0

# --- KPI ---
c = st.columns(4)
c[0].metric("VN30 · lợi suất kỳ", pct(ls_tich_luy(vn30)))
c[1].metric("VN-Index · lợi suất kỳ", pct(ls_tich_luy(vni)))
c[2].metric("Chênh lệch VN30 − VN-Index", pct(ls_tich_luy(vn30) - ls_tich_luy(vni)), help="Điểm phần trăm, trong kỳ chọn")
c[3].metric("Thanh khoản TB / ngày", f"{kl_tb:.0f}M cp")
c = st.columns(4)
c[0].metric("Biến động VN30 (năm hóa)", "N/A" if pd.isna(bien_dong(vn30)) else f"{bien_dong(vn30):.1f}%")
c[1].metric("Sụt giảm tối đa VN30", "N/A" if len(vn30) < 2 else f"{drawdown(vn30).min():.1f}%")
c[2].metric("Phiên gần nhất: mã tăng", so_tang)
c[3].metric("Phiên gần nhất: mã giảm", so_giam)

st.write("")

# --- Hàng 1: lợi suất tích lũy + drawdown ---
col_a, col_b = st.columns([3, 2])
with col_a:
    fig = go.Figure()
    for s, mau, ten in [(vn30, VN30, "VN30"), (vni, VNINDEX, "VN-Index")]:
        if len(s):
            fig.add_trace(go.Scatter(x=s["ngay"], y=(s["gia_dong"] / s["gia_dong"].iloc[0] - 1) * 100,
                                     name=ten, line=dict(color=mau, width=2.4 if ten == "VN30" else 1.8),
                                     hovertemplate="%{x|%d/%m/%Y}: %{y:.1f}%<extra>" + ten + "</extra>"))
    fig.add_hline(y=0, line_dash="dot", line_color="#94A3B8")
    fig.update_layout(title="Lợi suất tích lũy (%), gốc = đầu kỳ", height=360, hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
with col_b:
    fig = go.Figure()
    for s, mau, ten in [(vn30, VN30, "VN30"), (vni, VNINDEX, "VN-Index")]:
        if len(s):
            fig.add_trace(go.Scatter(x=s["ngay"], y=drawdown(s), name=ten, line=dict(color=mau, width=1.6),
                                     fill="tozeroy" if ten == "VN30" else None,
                                     fillcolor="rgba(29,78,216,.10)"))
    fig.update_layout(title="Sụt giảm từ đỉnh (%)", height=360, hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

# --- Hàng 2: độ rộng thị trường ---
col_a, col_b = st.columns(2)
with col_a:
    br = df_loi.assign(tang=df_loi["loi_suat"] > 0, giam=df_loi["loi_suat"] < 0).groupby("ngay")[["tang", "giam"]].sum()
    br["rong"] = (br["tang"] - br["giam"]).rolling(10, min_periods=1).mean()
    fig = go.Figure(go.Scatter(x=br.index, y=br["rong"], line=dict(color=VN30, width=2),
                               fill="tozeroy", fillcolor="rgba(29,78,216,.10)",
                               hovertemplate="%{x|%d/%m/%Y}: %{y:.1f}<extra></extra>"))
    fig.add_hline(y=0, line_dash="dot", line_color="#94A3B8")
    fig.update_layout(title="Độ rộng thị trường: (mã tăng − mã giảm), TB 10 phiên", height=320)
    st.plotly_chart(fig, use_container_width=True)
with col_b:
    if len(df_cb) and {"ma50", "ma200"} <= set(df_cb.columns):
        x = df_cb.dropna(subset=["ma50"]).copy()
        x["t50"] = x["gia_dong"] > x["ma50"]
        x["t200"] = x["gia_dong"] > x["ma200"]
        ty = x.groupby("ngay")[["t50", "t200"]].mean() * 100
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ty.index, y=ty["t50"], name="Trên MA50", line=dict(color=VN30, width=2)))
        fig.add_trace(go.Scatter(x=ty.index, y=ty["t200"], name="Trên MA200", line=dict(color="#F59E0B", width=2)))
        fig.add_hline(y=50, line_dash="dot", line_color="#94A3B8")
        fig.update_layout(title="Tỷ lệ mã nằm trên MA50 / MA200 (%)", height=320, yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)

# --- Lợi suất kỳ theo mã ---
df_loi = df_loi.sort_values(["ma_cp", "ngay"])
ls_ma = df_loi.groupby("ma_cp").agg(
    ten=("ten_cong_ty", "first"), nganh=("nganh_cap1", "first"),
    dau=("gia_dong", "first"), cuoi=("gia_dong", "last")).reset_index()
ls_ma["ls"] = (ls_ma["cuoi"] / ls_ma["dau"] - 1) * 100

# --- Hàng 3: ngành + top tăng/giảm ---
col_a, col_b = st.columns(2)
with col_a:
    ng = ls_ma.groupby("nganh")["ls"].mean().sort_values().reset_index()
    fig = go.Figure(go.Bar(x=ng["ls"], y=ng["nganh"], orientation="h",
                           marker_color=[TANG if v >= 0 else GIAM for v in ng["ls"]],
                           hovertemplate="%{y}: %{x:.1f}%<extra></extra>"))
    fig.update_layout(title="Lợi suất kỳ trung bình theo ngành (%)", height=380)
    st.plotly_chart(fig, use_container_width=True)
with col_b:
    tt = pd.concat([ls_ma.nlargest(5, "ls"), ls_ma.nsmallest(5, "ls")]).sort_values("ls")
    fig = go.Figure(go.Bar(x=tt["ls"], y=tt["ma_cp"], orientation="h",
                           marker_color=[TANG if v >= 0 else GIAM for v in tt["ls"]],
                           hovertemplate="%{y}: %{x:.1f}%<extra></extra>"))
    fig.update_layout(title="Top 5 tăng / giảm theo lợi suất kỳ (%)", height=380)
    st.plotly_chart(fig, use_container_width=True)
ghi_chu("Lợi suất tính trên giá đóng cửa đã điều chỉnh. Riêng <b>TCB</b> có điểm gãy giá ngày 15/10/2026 "
        "(cổ phiếu thưởng 50%) nên lợi suất kỳ chứa mốc này của TCB chưa phản ánh đúng.")

# --- Treemap phiên gần nhất ---
heat = phien.copy()
heat["ls_pct"] = heat["loi_suat"] * 100
fig = px.treemap(heat, path=["nganh_cap1", "ma_cp"], values=heat["khoi_luong"].clip(lower=1),
                 color="ls_pct", color_continuous_scale=[GIAM, "#FEF3C7", TANG],
                 color_continuous_midpoint=0, custom_data=["ten_cong_ty", "ls_pct"],
                 title=f"Bản đồ nhiệt phiên {ngay_cuoi:%d/%m/%Y} (kích thước = khối lượng)")
fig.update_traces(texttemplate="%{label}<br>%{customdata[1]:.2f}%",
                  hovertemplate="<b>%{label}</b><br>%{customdata[0]}<br>%{customdata[1]:.2f}%<extra></extra>")
fig.update_traces(root_color="#F7F8FA")
fig.update_layout(height=420, coloraxis_colorbar=dict(title="%"))
st.plotly_chart(fig, use_container_width=True)

# --- Bảng chi tiết ---
st.subheader("Chi tiết 30 mã")
bang = ls_ma[["ma_cp", "ten", "nganh", "cuoi", "ls"]].copy()
p = phien.set_index("ma_cp")
bang["ngay_pct"] = bang["ma_cp"].map(p["loi_suat"]) * 100
bang["kl"] = bang["ma_cp"].map(p["khoi_luong"])
if len(df_cb):
    lc = df_cb.sort_values("ngay").groupby("ma_cp").last()
    bang["rsi"] = bang["ma_cp"].map(lc["rsi14"])
    bang["so_ma200"] = (bang["ma_cp"].map(lc["gia_dong"] / lc["ma200"] - 1) * 100)
    bang["dd"] = bang["ma_cp"].map(lc["drawdown"]) * 100 if lc["drawdown"].abs().max() <= 1.5 else bang["ma_cp"].map(lc["drawdown"])
bang = bang.sort_values("ls", ascending=False).reset_index(drop=True)
bang = bang.rename(columns={"ma_cp": "Mã", "ten": "Công ty", "nganh": "Ngành", "cuoi": "Giá (nghìn đ)",
                            "ls": "Lợi suất kỳ (%)", "ngay_pct": "Phiên cuối (%)", "kl": "Khối lượng",
                            "rsi": "RSI14", "so_ma200": "So với MA200 (%)", "dd": "Cách đỉnh (%)"})
st.dataframe(
    bang, use_container_width=True, hide_index=True, height=420,
    column_config={
        "Giá (nghìn đ)": st.column_config.NumberColumn(format="%.2f"),
        "Lợi suất kỳ (%)": st.column_config.NumberColumn(format="%+.1f"),
        "Phiên cuối (%)": st.column_config.NumberColumn(format="%+.2f"),
        "Khối lượng": st.column_config.NumberColumn(format="%d"),
        "RSI14": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%.0f"),
        "So với MA200 (%)": st.column_config.NumberColumn(format="%+.1f"),
        "Cách đỉnh (%)": st.column_config.NumberColumn(format="%.1f"),
    })
