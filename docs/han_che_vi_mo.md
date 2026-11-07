## Hạn chế: Lãi suất liên ngân hàng (VNIBOR)
- **Nguồn**: Ngân hàng Nhà nước Việt Nam không cung cấp API công khai miễn phí.
- **Ảnh hưởng**: Cột lãi suất liên ngân hàng thiếu trong `fact_vi_mo`.
- **Xử lý**: Trang Tin tức & Vĩ mô trên webapp hiển thị "N/A" cho chỉ tiêu này.

## Hạn chế: Tỷ giá USD/VND
- **Nguồn**: Vietcombank API công khai — chỉ có tỷ giá hiện tại (không có lịch sử).
- **Ảnh hưởng**: `fact_vi_mo` chỉ có 1 dòng tỷ giá (ngày hiện tại).
- **Xử lý**: Trang vĩ mô hiển thị tỷ giá điểm hiện tại thay vì chuỗi thời gian.