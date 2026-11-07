# -*- coding: utf-8 -*-
"""
Tải và cache dữ liệu Gold cho webapp.
Dùng mtime của file làm cache key để tự động nhận dữ liệu mới sau khi chạy cap_nhat.py.
Đường dẫn tương đối độc lập với môi trường chạy (Local Windows hoặc Streamlit Cloud Linux).
"""

import os
import streamlit as st
import pandas as pd
from pathlib import Path

# Xác định đường dẫn thư mục gold tương đối từ file hiện tại
_BASE_DIR = Path(__file__).resolve().parent.parent.parent
GOLD_DIR = _BASE_DIR / "gold"
if not GOLD_DIR.exists():
    # Thử fallback thư mục làm việc hiện tại
    GOLD_DIR = Path("gold").resolve()


def _mtime(filename: str) -> float:
    """Lấy thời gian sửa đổi của file (dùng làm cache key)."""
    try:
        path = GOLD_DIR / filename
        return path.stat().st_mtime if path.exists() else 0.0
    except Exception:
        return 0.0


# ---- Mỗi hàm cache theo mtime để tự refresh khi dữ liệu mới ----

@st.cache_data
def load_dim_co_phieu(_mtime_key=None) -> pd.DataFrame:
    try:
        path = GOLD_DIR / "dim_co_phieu.csv"
        return pd.read_csv(path) if path.exists() else pd.DataFrame()
    except Exception:
        return pd.DataFrame()


@st.cache_data
def load_dim_ngay(_mtime_key=None) -> pd.DataFrame:
    try:
        path = GOLD_DIR / "dim_ngay.csv"
        return pd.read_csv(path, parse_dates=["ngay"]) if path.exists() else pd.DataFrame()
    except Exception:
        return pd.DataFrame()


@st.cache_data
def load_fact_gia(_mtime_key=None) -> pd.DataFrame:
    try:
        path = GOLD_DIR / "fact_gia_ngay.csv"
        return pd.read_csv(path, parse_dates=["ngay"]) if path.exists() else pd.DataFrame()
    except Exception:
        return pd.DataFrame()


@st.cache_data
def load_fact_loi_suat(_mtime_key=None) -> pd.DataFrame:
    try:
        path = GOLD_DIR / "fact_loi_suat.csv"
        return pd.read_csv(path, parse_dates=["ngay"]) if path.exists() else pd.DataFrame()
    except Exception:
        return pd.DataFrame()


@st.cache_data
def load_fact_chi_bao(_mtime_key=None) -> pd.DataFrame:
    try:
        path = GOLD_DIR / "fact_chi_bao_ky_thuat.csv"
        return pd.read_csv(path, parse_dates=["ngay"]) if path.exists() else pd.DataFrame()
    except Exception:
        return pd.DataFrame()


@st.cache_data
def load_fact_tai_chinh(_mtime_key=None) -> pd.DataFrame:
    try:
        path = GOLD_DIR / "fact_chi_so_tai_chinh.csv"
        return pd.read_csv(path) if path.exists() else pd.DataFrame()
    except Exception:
        return pd.DataFrame()


@st.cache_data
def load_fact_thi_truong(_mtime_key=None) -> pd.DataFrame:
    try:
        path = GOLD_DIR / "fact_chi_so_thi_truong.csv"
        return pd.read_csv(path, parse_dates=["ngay"]) if path.exists() else pd.DataFrame()
    except Exception:
        return pd.DataFrame()


@st.cache_data
def load_fact_vi_mo(_mtime_key=None) -> pd.DataFrame:
    try:
        path = GOLD_DIR / "fact_vi_mo.csv"
        if not path.exists():
            return pd.DataFrame(columns=["ngay", "loai_chi_tieu", "gia_tri", "don_vi", "nguon"])
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame(columns=["ngay", "loai_chi_tieu", "gia_tri", "don_vi", "nguon"])


@st.cache_data
def load_fact_tin_tuc(_mtime_key=None) -> pd.DataFrame:
    try:
        path = GOLD_DIR / "fact_tin_tuc.csv"
        if not path.exists():
            return pd.DataFrame(columns=["ngay", "tieu_de", "mo_ta", "url", "nguon", "ma_lien_quan"])
        df = pd.read_csv(path)
        if "ngay" in df.columns:
            df["ngay"] = pd.to_datetime(df["ngay"], errors="coerce")
        return df
    except Exception:
        return pd.DataFrame(columns=["ngay", "tieu_de", "mo_ta", "url", "nguon", "ma_lien_quan"])


def get_all_data():
    """
    Tải tất cả bảng dữ liệu Gold.
    Dùng mtime làm cache key để tự động refresh.
    Trả về dict với các DataFrame đã sẵn sàng.
    """
    # Cache key = tuple mtime của các file chính
    keys = {
        "dim_co_phieu": _mtime("dim_co_phieu.csv"),
        "fact_gia": _mtime("fact_gia_ngay.csv"),
        "fact_thi_truong": _mtime("fact_chi_so_thi_truong.csv"),
    }

    dim_cp = load_dim_co_phieu(keys["dim_co_phieu"])
    dim_ngay = load_dim_ngay(keys["dim_co_phieu"])
    fact_gia = load_fact_gia(keys["fact_gia"])
    fact_loi = load_fact_loi_suat(keys["fact_gia"])
    fact_cb = load_fact_chi_bao(keys["fact_gia"])
    fact_tc = load_fact_tai_chinh(keys["dim_co_phieu"])
    fact_ttm = load_fact_thi_truong(keys["fact_thi_truong"])
    fact_vi_mo = load_fact_vi_mo(keys["dim_co_phieu"])
    fact_tin = load_fact_tin_tuc(keys["dim_co_phieu"])

    ngay_cap_nhat = fact_gia["ngay"].max().strftime("%d/%m/%Y") if len(fact_gia) > 0 else "N/A"

    return {
        "dim_cp": dim_cp,
        "dim_ngay": dim_ngay,
        "fact_gia": fact_gia,
        "fact_loi": fact_loi,
        "fact_cb": fact_cb,
        "fact_tc": fact_tc,
        "fact_ttm": fact_ttm,
        "fact_vi_mo": fact_vi_mo,
        "fact_tin": fact_tin,
        "ngay_cap_nhat": ngay_cap_nhat,
    }


# Danh sách mã cảnh báo giá điều chỉnh bất thường
CANH_BAO_GIA = {
    ("TCB", "2026-10-15"): "⚠️ Lợi suất -33.4%, không tìm được sự kiện tương ứng (có thể lỗi dữ liệu nguồn).",
    ("SHB", "2021-05-14"): "⚠️ Lợi suất +10%, trùng sự kiện phát hành thêm 10% — giá có thể chưa điều chỉnh.",
}
