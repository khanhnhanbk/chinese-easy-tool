# Chinese Easy Tool

Ứng dụng Streamlit tạo worksheet luyện viết chữ Hán có thể in được dưới dạng PDF.

## Tính năng

- Nhập chữ Hán hoặc cụm từ
- Tùy chỉnh bố cục worksheet:
  - kích thước ô
  - số cột luyện nét
  - lề trái và lề trên
  - hiển thị Pinyin
  - chế độ nhiều ký tự
- Sinh file PDF và tải về ngay
- Chọn tên file đầu ra dễ dàng

## Cấu trúc dự án

- `app.py` - trang chính của ứng dụng
- `pages/01_Practice_Sheet.py` - trang tạo worksheet
- `services/generate_practice_sheet.py` - logic tạo PDF
- `datas/usersetting.py` - model cài đặt người dùng
- `fonts/` - font chữ dùng cho chữ Hán và Pinyin
- `assets/` - tài nguyên tĩnh như ảnh QR
- `requirements.txt` - các thư viện Python cần cài

## Yêu cầu

- Python 3.11+
- `streamlit`
- `reportlab`
- `pypinyin`

## Cài đặt

```bash
cd "c:\Users\nhann\Documents\Python\chinese-easy-tool"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Chạy ứng dụng

```bash
.venv\Scripts\python.exe -m streamlit run pages/01_Practice_Sheet.py
```

## Cách dùng

1. Nhập chữ Hán hoặc cụm từ ở ô bên trái.
2. Chỉnh cài đặt worksheet trong phần Cài đặt nâng cao.
3. Nhập tên file PDF đầu ra.
4. Nhấn `🚀 Tạo PDF` để sinh worksheet.
5. Nhấn `⬇️ Tải PDF` khi nút download xuất hiện.

## Buy me a coffee

Nếu bạn thấy công cụ này hữu ích, mình rất cảm ơn nếu bạn ủng hộ một ly cà phê.

- Ngân hàng: **MB Bank**
- Số tài khoản: **0349796850**
- Chủ tài khoản: **NGUYỄN VĂN KHÁNH NHÂN**

Hoặc quét mã QR bên dưới

![assets/buy_me_coffee_qr.png](assets/buy_me_coffee_qr.png)

## Ghi chú

- Ứng dụng dùng ReportLab để xuất PDF.
- File PDF có thể tải về trực tiếp từ trang.
- Nếu ô nhập trống, quá trình tạo sẽ hiển thị cảnh báo.

## Giấy phép

Dự án cung cấp "như hiện trạng" và không có bảo hành.
