# Hướng dẫn Cập nhật Dữ liệu VN30

Quy trình cập nhật dữ liệu tự động cho tầng Gold, Webapp và Power BI (tối đa 6 bước):

1. **Kích hoạt môi trường ảo Python:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Cập nhật dữ liệu giá, chỉ báo kỹ thuật và chỉ số thị trường hàng ngày:**
   ```powershell
   python src/cap_nhat.py
   ```
   *Lệnh này tự động cào phiên mới của 30 mã VN30 + VN-Index/VN30, tính lại chỉ báo kỹ thuật, nối vào `gold/`, chống trùng lặp và chạy kiểm thử tự động.*

3. **Cập nhật dữ liệu báo cáo tài chính (chạy định kỳ theo quý/năm):**
   ```powershell
   python src/cap_nhat_bctc.py
   ```

4. **Kiểm tra chất lượng toàn bộ dữ liệu Gold (độc lập):**
   ```powershell
   python tests/kiem_tra_gold.py
   ```

5. **Xem dữ liệu trên Webapp Streamlit:**
   ```powershell
   streamlit run webapp/app.py
   ```
   *Webapp tự động nhận diện dữ liệu mới thông qua cơ chế khóa cache theo thời gian sửa file (`mtime`).*

6. **Đồng bộ dữ liệu sang Power BI Desktop:**
   - Mở file dự án Power BI (`powerbi/VN30.pbip`).
   - Nhấn nút **Refresh** trên thanh công cụ Home để tải dữ liệu CSV mới từ thư mục `gold/`.
