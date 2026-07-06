import streamlit as st

from services.viterbi_tokenizer import ViterbiChineseTokenizer

st.set_page_config(page_title="Bộ tách từ Viterbi", page_icon="🧠", layout="wide")

st.title("🧠 Bộ tách từ tiếng Trung bằng Viterbi")

st.markdown(
    "Dùng thuật toán Viterbi với từ điển dựa trên tần suất để tách câu Tiếng Trung."
)

# =========================
# MAIN INPUT
# =========================
col1, col2 = st.columns([2, 1])

with col1:
    text_input = st.text_area(
        "Nhập văn bản tiếng Trung",
        height=200,
        placeholder="Nhập đoạn tiếng Trung vào đây...",
    )
    col11, col12 = st.columns([2, 1])

    separator = col11.selectbox(
        "Dấu phân cách giữa các token",
        ["Khoảng trắng", "Dấu gạch dưới (_)", "Dấu gạch chéo (/)"],
        index=0,
    )

    with col12:
      st.markdown("<br>", unsafe_allow_html=True)
      run_btn = st.button(
          "🚀 Tách từ",
          use_container_width=True,
      )

    # =========================
    # OUTPUT AREA
    # =========================
    st.markdown("---")
    st.subheader("📤 Kết quả")

    if run_btn:
        if not text_input.strip():
            st.warning("Vui lòng nhập văn bản tiếng Trung.")
        else:

            tokenizer = ViterbiChineseTokenizer()
            tokens = tokenizer.tokenize(text_input)

            if separator == "Khoảng trắng":
                sep_char = " "
            elif separator == "Dấu gạch chéo (/)":
                sep_char = "/"
            elif separator == "Dấu gạch dưới (_)":
                sep_char = "_"
            else:
                sep_char = " "

            result_text = sep_char.join(tokens)
            result_text = "\n".join(line.lstrip() for line in result_text.splitlines())

            st.code(result_text, language="text")

with col2:
    st.markdown("### ✨ Tính năng")

    st.write("⚡ Tách từ nhanh, xử lý gần như tức thì.")
    st.write("🎯 Độ chính xác cao với từ điển hơn 30.000 từ thông dụng.")
    st.write("📄 Không giới hạn độ dài văn bản (phụ thuộc cấu hình máy).")
    st.write("🔒 Chạy hoàn toàn trên máy chủ của ứng dụng, không gửi dữ liệu sang dịch vụ bên thứ ba.")

    st.markdown("---")

    st.markdown("## ☕ Ủng hộ mình")

    col_qr, col_text = st.columns([1, 1.6], gap="large")

    with col_qr:
        st.image(
            "assets/buy_me_coffee_qr.png",
            width=180,  # 👈 tăng size QR
        )

    with col_text:
        st.markdown(
            """
            <div style="font-size:16px; line-height:1.8">

            Nếu bạn thấy công cụ này hữu ích, mình rất cảm ơn nếu bạn ủng hộ một ly cà phê ☕

            <br/><br/>

            <b>💳 Thông tin chuyển khoản ủng hộ</b><br/>
            Ngân hàng: <b>MB Bank</b><br/>
            Số tài khoản: <b>0349796850</b><br/>
            Chủ tài khoản: <b>NGUYỄN VĂN KHÁNH NHÂN</b><br/>

            <br/>

            👉 Hoặc quét mã QR bên cạnh để ủng hộ nhanh.

            </div>
            """,
            unsafe_allow_html=True,
        )
          

