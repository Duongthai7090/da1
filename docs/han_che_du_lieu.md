# Báo cáo Giới hạn & Hạn chế Dữ liệu (Data Limitations)
**Dự án**: Đồ án Business Analysis — Dashboard Phân tích Cổ phiếu VN30  
**Tác giả / Nhóm thực hiện**: Nhóm Đồ án BA  
**Thời điểm hoàn thành**: Tháng 11/2026  

---

## 1. Giới hạn về Phạm vi và Độ phủ Dữ liệu (Coverage)
- **Danh mục cổ phiếu**: Hệ thống chỉ theo dõi danh mục **30 mã cổ phiếu** thành phần thuộc chỉ số VN30 hiện hành tại kỳ rà soát gần nhất. Không mở rộng ra toàn bộ hơn 1.600 cổ phiếu trên 3 sàn HOSE, HNX, UPCoM.
- **Khung thời gian giao dịch**: Dữ liệu giá giao dịch hàng ngày (OHLCV) được chuẩn hóa trong khung thời gian từ **16/10/2018** đến **30/10/2026** (khoảng 8 năm). Các mã mới niêm yết muộn hơn hoặc chuyển sàn (như BSR từ UPCoM) chỉ có dữ liệu từ ngày chính thức giao dịch được hệ thống ghi nhận.
- **Tần suất dữ liệu**: Dữ liệu giá là dữ liệu cuối ngày (Daily EOD), **hoàn toàn không có dữ liệu theo giờ (Intraday/Hourly) hay Tick-by-tick**.
- **Cơ cấu cổ đông & Mạng lưới quan hệ**: Hệ thống **không cung cấp đồ thị cổ đông (Shareholder ownership graph)** hay mạng lưới sở hữu chéo do nguồn dữ liệu miễn phí không có cấu trúc quan hệ thực thể đầy đủ.
- **Mô hình Trí tuệ nhân tạo (AI / Machine Learning / LLM)**: Hệ thống là bộ giải pháp Business Analysis & BI chuẩn mực; **không tích hợp mô hình dự báo giá AI, sentiment analysis hay LLM chatbot**.

---

## 2. Kiểm tra Điều chỉnh Giá và Bất thường Giao dịch
Theo kết quả đối chiếu giữa các phiên biến động lớn ($|Lợi\ suất| > 10\%$) và dữ liệu sự kiện doanh nghiệp (`docs/kiem_tra_dieu_chinh_gia.md` & `gold/fact_su_kien.csv`):
1. **Mã TCB (Phiên 15/10/2026)**:
   - Xuất hiện mức giảm đột ngột **-33.4%** (từ 32.95 xuống 21.95 nghìn đồng).
   - *Đối soát dữ liệu quyền*: Đã cào và xác nhận chính thức sự kiện: **TCB phát hành cổ phiếu trả cổ tức tỷ lệ 50.0%**, Ngày GDKHQ là **29/10/2026**, Ngày chốt danh sách là **30/10/2026** (nguồn VCI). Nguồn dữ liệu KBS đã điều chỉnh hồi tố giá tham chiếu (giảm 1/1.5 tương ứng -33.3%) từ các phiên cập nhật nửa cuối tháng 10/2026, dẫn đến bước nhảy nối nguồn giữa dữ liệu lịch sử gốc và dữ liệu mới cập nhật.
   - *Biện pháp xử lý*: Tuân thủ quy tắc không tự ý sửa đổi dữ liệu gốc, hệ thống giữ nguyên chuỗi giá thực tế và hiển thị thông điệp cảnh báo rõ ràng trên Dashboard.
2. **Mã SHB (Phiên 14/05/2021)**:
   - Lợi suất tăng trần **+10%** trùng ngày chốt danh sách chia cổ tức bằng cổ phiếu tỷ lệ 10%. Có nghi vấn nguồn dữ liệu chưa trừ triệt để giá tham chiếu điều chỉnh. Được ghi nhận cảnh báo trên hệ thống.
3. **Mã BSR**:
   - Có một số phiên có biên độ dao động trên 10% do xuất phát điểm giao dịch trên sàn UPCoM (biên độ $\pm 15\%$) trước khi chuyển sang HOSE. Đây là biến động thị trường tự nhiên.

---

## 3. Hạn chế về Dữ liệu Báo cáo Tài chính (BCTC)
1. **Nhóm Công ty Chứng khoán (SSI, TCX)**:
   - Ngành dịch vụ tài chính/chứng khoán sử dụng hệ thống tài khoản và mẫu biểu BCTC đặc thù (`mau_bctc = 'CK'`), khác biệt căn bản so với BCTC Doanh nghiệp sản xuất thông thường (`DN`) và Ngân hàng thương mại (`NH`).
   - Cụ thể: Các chỉ tiêu như Doanh thu thuần, Biên lợi nhuận gộp, Nợ vay hay Tỷ lệ CIR/LDR không áp dụng tương đồng.
   - *Biện pháp xử lý*: Để bảo đảm tính nghiêm ngặt của đồ án phân tích nghiệp vụ, hệ thống hiển thị **N/A** kèm thông báo diễn giải cụ thể khi người dùng chọn SSI hoặc TCX, tránh so sánh khập khiễng.
2. **Kỳ báo cáo BCTC**:
   - Dữ liệu tài chính hiện có bao gồm báo cáo tài chính năm kiểm toán từ **2022 đến 2025** (4 năm tài chính). Chưa có chuỗi BCTC hàng quý (Quarterly) đồng bộ cho toàn bộ 30 mã.

---

## 4. Quyết định Bỏ Chỉ số Định giá (P/E, P/B, Vốn hóa thị trường)
- **Lý do kỹ thuật & nghiệp vụ**: Việc tính toán tỷ số định giá theo chuỗi thời gian ngày ($P/E$, $P/B$, Vốn hóa) đòi hỏi số lượng cổ phiếu lưu hành (Outstanding Shares) chính xác tại từng ngày giao dịch trong lịch sử (sau khi điều chỉnh phát hành riêng lẻ, chuyển đổi trái phiếu, ESOP, mua bán cổ phiếu quỹ). Nguồn dữ liệu miễn phí hiện tại chỉ cung cấp số cổ phiếu lưu hành tại một thời điểm gần nhất (Snapshot) hoặc thiếu bảng sự kiện vốn chi tiết.
- Nếu lấy số cổ phiếu hiện tại nhân ngược lại quá khứ sẽ tạo ra sai số lớn (Look-ahead bias) và làm biến dạng định giá.
- **Biện pháp xử lý**: Theo quy định thay đổi phạm vi tại **Mục 9 của AGENTS.md**, dự án **chính thức lược bỏ bảng `fact_dinh_gia`**. Trên giao diện Dashboard, phân tích cơ bản tập trung tối đa vào hiệu quả hoạt động nội tại của doanh nghiệp: **ROE, ROA, Biên lợi nhuận, Đòn bẩy tài chính, và các chỉ số ngân hàng (CIR, LDR)**.

---

## 5. Hạn chế về Dữ liệu Vĩ mô & Tin tức
1. **Lãi suất liên ngân hàng (VNIBOR)**:
   - Ngân hàng Nhà nước Việt Nam (SBV) chỉ công bố số liệu dưới dạng bảng biểu trên cổng thông tin, không cung cấp REST API mở miễn phí.
   - Do đó, Dashboard hiển thị **N/A** đối với lãi suất liên ngân hàng.
2. **Tỷ giá hối đoái USD/VND**:
   - Cổng XML của Vietcombank cung cấp tỷ giá bán ra hiện hành (Spot rate tại thời điểm truy vấn), không cung cấp chuỗi thời gian lịch sử chi tiết 8 năm. Vì vậy hệ thống chỉ hiển thị điểm tỷ giá hiện tại.
3. **Kinh tế vĩ mô (GDP & CPI)**:
   - Số liệu được lấy từ World Bank Open Data API theo chu kỳ **năm** (Annual), phản ánh xu hướng trung - dài hạn, không có dữ liệu CPI/GDP theo từng tháng.
5. **Nguồn cấp Tin tức (RSS) & Phân loại Ngành**:
   - Dữ liệu tin tức được thu thập tự động từ các nguồn RSS công khai (VnExpress, Tuổi Trẻ, Thanh Niên, VietnamNet).
   - **Phân loại ngành và mã liên quan được thực hiện thuần túy theo cơ chế khớp từ khóa (Rule-based Keyword Mapping)**, không sử dụng mô hình học máy (NLP/NER) phức tạp. Các bài viết vĩ mô không chứa từ khóa đặc thù ngành sẽ được xếp vào nhóm "Chung" hoặc để giá trị `NULL`.

---

## 6. Dữ liệu Phi cấu trúc (Tài liệu BCTC PDF)
- Hệ thống xây dựng khung kiến trúc phân cấp `data/tai_lieu/<ma_cp>/<loai>/<nam>/` và bảng quản lý `meta_tai_lieu`.
- **Tập tin PDF hiện tại chỉ là dữ liệu mẫu (Sample/Mock)** nhằm minh họa năng lực quản lý tài liệu phi cấu trúc đối với các mã đầu ngành (FPT, VCB, HPG, TCB). Hệ thống **không cào hàng loạt toàn bộ tệp PDF BCTC lịch sử** theo đúng phạm vi kỹ thuật của đồ án.

---

## 7. Kết luận & Tác động Nghiệp vụ
Các hạn chế nêu trên hoàn toàn nằm trong tầm kiểm soát và được xử lý theo đúng nguyên tắc:
- **Không tự ý suy đoán số liệu khi không đủ cơ sở dữ liệu nguồn.**
- **Mọi vị trí thiếu dữ liệu đều được hiển thị "N/A" một cách minh bạch, có chú thích rõ ràng.**
- **Không làm gián đoạn hay phát sinh lỗi hệ thống trên Dashboard và Mô hình Power BI.**
