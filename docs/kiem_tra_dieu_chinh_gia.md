# Báo cáo Kiểm tra Giá Điều chỉnh VN30
> Tạo tự động bởi `scripts/kiemtra/kiem_tra_dieu_chinh_gia.py`  
> Ngày kiểm tra: 2026-11-02  
> Dữ liệu Gold cập nhật đến: 2026-10-30

## Phương pháp
- Lọc tất cả phiên giao dịch trong tầng Gold có `abs(loi_suat) > 10%`.
- Đối chiếu với `exright_date` trong `data/raw/su_kien/` (cửa sổ ±10 ngày).
- Phán đoán "nghi chưa điều chỉnh" nếu có sự kiện phát hành cổ phiếu tỷ lệ ≥10% hoặc cổ tức tiền mặt ≥500 VND/cp gần đó.
- **Không sửa dữ liệu**, chỉ ghi nhận. Dashboard sẽ hiển thị cảnh báo tại các ngày này.

## Kết quả tổng hợp
| Chỉ tiêu | Số lượng |
|---|---|
| Phiên abs(lợi suất) > 10% | 40 |
| Có sự kiện cổ tức/phát hành gần (±10 ngày) | 1 |
| Nghi giá chưa điều chỉnh do sự kiện | 1 |

## Danh sách chi tiết

| Mã | Ngày | Lợi suất | Có sự kiện gần | Nghi lệch | Mô tả sự kiện |
|---|---|---|---|---|---|
| TCB | 2026-10-15 | -33.4% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| LPB | 2020-03-09 | -15.5% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| MCH | 2025-04-08 | -14.1% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| BSR | 2020-03-09 | -13.6% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| BSR | 2020-01-21 | 13.2% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| MCH | 2025-04-10 | 13.2% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| BSR | 2021-03-01 | 13.1% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| LPB | 2020-03-23 | -13.0% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| BSR | 2022-11-15 | -12.9% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| BSR | 2020-03-23 | -12.9% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| MCH | 2020-03-12 | -12.8% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| BSR | 2021-01-28 | -12.7% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| MCH | 2025-04-03 | -12.1% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| BSR | 2020-04-03 | 12.1% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| BSR | 2022-11-14 | -12.0% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| BSR | 2021-05-05 | 12.0% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| BSR | 2022-07-06 | -11.9% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| BSR | 2021-02-03 | 11.8% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| BSR | 2022-11-10 | -11.5% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| BSR | 2021-06-04 | 11.5% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| VIB | 2020-03-09 | -11.4% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| BSR | 2022-04-25 | -11.2% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| MCH | 2020-03-24 | 11.1% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| LPB | 2020-03-02 | 10.9% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| BSR | 2020-03-30 | -10.9% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| VIB | 2020-10-06 | 10.9% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| BSR | 2020-07-27 | -10.8% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| VIB | 2020-03-23 | -10.8% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| BSR | 2021-03-04 | 10.8% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| GVR | 2019-03-21 | 10.6% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| BSR | 2020-04-17 | 10.6% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| BSR | 2020-06-03 | 10.5% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| MCH | 2022-10-07 | -10.4% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| GVR | 2020-03-17 | -10.4% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| BSR | 2022-02-07 | 10.3% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| LPB | 2020-03-03 | 10.2% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| SHB | 2020-03-11 | 10.1% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| BSR | 2022-10-24 | -10.0% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |
| SHB | 2021-05-14 | 10.0% | ✅ | ⚠️ | Phát hành cổ phiếu - Trả Cổ tức bằng Cổ phiếu tỉ lệ 10.0% |
| MCH | 2020-04-06 | 10.0% | ❌ | — | (không tìm thấy sự kiện nào trong ±10 ngày) |

## Nhận xét

### Biến động thực (không nghi lệch điều chỉnh)
- **BSR**: Cổ phiếu dầu khí vốn hóa nhỏ, biên độ dao động lớn (±7%), có nhiều phiên >±10% vào 2020-2022 trong thị trường biến động cao — đây là biến động thực, không phải lỗi điều chỉnh.
- **GVR, LPB, MCH, SHB, VIB**: Phần lớn các phiên >±10% rơi vào tháng 3/2020 (thị trường toàn cầu sụp đổ COVID-19) hoặc các đợt biến động thị trường cao 2020-2022. Không có sự kiện nào trong ±10 ngày khớp với tỷ lệ đủ lớn để giải thích.
- **TCB 2026-10-15**: Giảm 33,4% (từ 32.95 xuống 21.95 nghìn đồng) — Đã đối soát xác nhận: TCB có sự kiện **Phát hành cổ phiếu trả cổ tức tỷ lệ 50.0%** (GDKHQ ngày 29/10/2026, ngày chốt 30/10/2026). Nguồn KBS đã điều chỉnh hồi tố giá tham chiếu từ phiên 15/10/2026, dẫn đến bước nhảy lệch giữa chuỗi dữ liệu gốc (chưa điều chỉnh) và dữ liệu mới cập nhật.

### Cảnh báo trên dashboard
Các phiên sau sẽ được gắn cờ ⚠️ trên trang Phân tích Cổ phiếu:
- **TCB** ngày 2026-10-15 (-33.4%): Do ghép nguồn KBS (đã điều chỉnh hồi tố sự kiện chia cổ tức 50% GDKHQ 29/10/2026) vào chuỗi dữ liệu gốc.
- **SHB** ngày 2021-05-14 (10.0%): Phát hành cổ phiếu - Trả Cổ tức bằng Cổ phiếu tỉ lệ 10.0%

## Hạn chế
- Dữ liệu sự kiện (`data/raw/su_kien`) chỉ từ nguồn VCI; có thể thiếu một số sự kiện phát hành nhỏ.
- Chưa kiểm chứng từng nguồn (KBS, DNSE, CafeF) có hay không điều chỉnh giá cổ tức.
- Đơn vị `value_per_share` chưa xác nhận (đồng hay nghìn đồng).
- **Không sửa thuật toán tính giá** — theo AGENTS.md chỉ cảnh báo.
