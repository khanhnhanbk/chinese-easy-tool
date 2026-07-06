# Chinese Easy Tool

Bộ công cụ học tiếng Trung bằng Streamlit, bao gồm tạo worksheet luyện viết chữ Hán và tách từ tiếng Trung.

## Tính năng chính

- Trang home bằng tiếng Việt với điều hướng rõ ràng
- Tạo worksheet luyện viết chữ Hán:
  - chỉnh kích thước ô
  - chỉnh số cột luyện nét
  - chỉnh lề trái và lề trên
  - bật/tắt hiển thị Pinyin
  - chế độ nhiều ký tự
  - xuất file PDF và tải về ngay
- Bộ tách từ tiếng Trung Viterbi:
  - tách câu thành token
  - tùy chọn dấu phân cách giữa các token
  - giữ nguyên số nguyên như `20`

## Cấu trúc dự án

- `app.py` - trang chính (home) của ứng dụng
- `pages/01_Practice_Sheet.py` - trang tạo worksheet luyện viết chữ Hán
- `pages/02_viterbi_tokenizer.py` - trang tách từ tiếng Trung
- `services/generate_practice_sheet.py` - logic tạo PDF
- `services/viterbi_tokenizer.py` - bộ tách từ Viterbi
- `datas/usersetting.py` - model cài đặt người dùng
- `fonts/` - font chữ dùng cho chữ Hán và Pinyin
- `assets/` - tài nguyên tĩnh như ảnh QR
- `requirements.txt` - thư viện Python cần cài

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
.venv\Scripts\python.exe -m streamlit run app.py
```

## Hướng dẫn sử dụng

1. Mở ứng dụng.
2. Chọn công cụ từ trang chủ.
3. Với `Tạo worksheet luyện viết chữ Hán`:
   - Nhập chữ Hán hoặc cụm từ.
   - Chỉnh cài đặt trong phần Cài đặt nâng cao.
   - Nhấn `🚀 Tạo PDF`.
   - Nhấn `⬇️ Tải PDF` khi nút download xuất hiện.
4. Với `Bộ tách từ tiếng Trung`:
   - Nhập đoạn văn bản tiếng Trung.
   - Chọn dấu phân cách giữa các token.
   - Nhấn `🚀 Tách từ`.
   - Kết quả sẽ hiển thị theo định dạng đã chọn.

## Buy me a coffee

Nếu bạn thấy công cụ này hữu ích, mình rất cảm ơn nếu bạn ủng hộ một ly cà phê.

- Ngân hàng: **MB Bank**
- Số tài khoản: **0349796850**
- Chủ tài khoản: **NGUYỄN VĂN KHÁNH NHÂN**

Hoặc quét mã QR bên dưới

![assets/buy_me_coffee_qr.png](assets/buy_me_coffee_qr.png)

## Ghi chú

- Worksheet PDF được tạo bằng ReportLab.
- Bộ tách từ dùng thuật toán Viterbi và từ điển tần suất.
- Ứng dụng hiển thị cảnh báo khi ô nhập trống.

## Giấy phép

Dự án cung cấp "như hiện trạng" và không có bảo hành.
