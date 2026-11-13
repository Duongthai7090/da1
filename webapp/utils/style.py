# -*- coding: utf-8 -*-
"""
Giao diện dùng chung: CSS, template Plotly, bảng màu.
Mỗi trang gọi setup("Tên trang", "Tiêu đề", "Mô tả") ngay đầu file.
Chỉ ảnh hưởng hiển thị, không đụng tới số liệu.
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio

# Bảng màu thống nhất
TANG, GIAM, DUNG = "#16A34A", "#DC2626", "#CA8A04"
VN30, VNINDEX = "#1D4ED8", "#64748B"
PALETTE = ["#1D4ED8", "#F59E0B", "#0D9488", "#7C3AED", "#DB2777", "#64748B"]

# Template Plotly mặc định: nền trong suốt, lưới mờ, chú thích phía trên
_tpl = go.layout.Template()
_tpl.layout = go.Layout(
    font=dict(family="Inter, Segoe UI, Arial, sans-serif", size=13, color="#0F172A"),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    colorway=PALETTE,
    title=dict(font=dict(size=15), x=0, xanchor="left"),
    xaxis=dict(gridcolor="#EEF1F5", linecolor="#E5E7EB", zeroline=False),
    yaxis=dict(gridcolor="#EEF1F5", linecolor="#E5E7EB", zeroline=False),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    margin=dict(l=10, r=10, t=60, b=40),
    hoverlabel=dict(bgcolor="white", font_size=12),
)
pio.templates["vn30"] = _tpl
pio.templates.default = "vn30"

_CSS = """
<style>
.block-container{padding-top:2rem;max-width:1280px}
h1{font-size:1.7rem!important;font-weight:700!important;letter-spacing:-.01em}
h2,h3{font-weight:650!important;letter-spacing:-.005em}
h3{font-size:1.15rem!important;margin-top:.6rem}
[data-testid="stSidebar"]{background:#fff;border-right:1px solid #E5E7EB}
[data-testid="stMetric"]{background:#fff;border:1px solid #E5E7EB;border-radius:14px;
  padding:14px 18px;box-shadow:0 1px 2px rgba(15,23,42,.04)}
[data-testid="stMetricLabel"] p{color:#64748B;font-size:.76rem;text-transform:uppercase;letter-spacing:.04em}
[data-testid="stMetricValue"]{font-size:1.9rem;font-weight:700}
[data-testid="stPlotlyChart"]{background:#fff;border:1px solid #E5E7EB;border-radius:14px;
  padding:0;overflow:hidden;background:#fff;box-shadow:0 1px 2px rgba(15,23,42,.04)}
[data-testid="stDataFrame"]{border:1px solid #E5E7EB;border-radius:12px;overflow:hidden}
button[data-baseweb="tab"]{font-weight:600}
hr{margin:1.2rem 0!important}
.sub{color:#64748B;font-size:.85rem;margin:-.4rem 0 1.1rem}
.note{background:#EFF4FF;border:1px solid #DBE6FF;border-radius:12px;padding:12px 16px;
  color:#1E3A8A;font-size:.9rem;margin:.4rem 0 1rem}
</style>
"""


def setup(page_title: str, title: str, ngay_cap_nhat: str = "", mo_ta: str = ""):
    """Cấu hình trang + CSS + tiêu đề. Phải là lệnh Streamlit đầu tiên."""
    st.set_page_config(page_title=f"{page_title} | VN30", page_icon="📈", layout="wide")
    st.markdown(_CSS, unsafe_allow_html=True)
    st.title(title)
    parts = [p for p in [mo_ta, f"Dữ liệu đến ngày {ngay_cap_nhat}" if ngay_cap_nhat else ""] if p]
    if parts:
        st.markdown(f'<div class="sub">{" · ".join(parts)}</div>', unsafe_allow_html=True)


def ghi_chu(noi_dung: str):
    """Hộp ghi chú/diễn giải ngắn dưới biểu đồ."""
    st.markdown(f'<div class="note">{noi_dung}</div>', unsafe_allow_html=True)
