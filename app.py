import streamlit as st

st.set_page_config(page_title="Bộ công cụ học tiếng Trung", page_icon="📚", layout="wide")
st.title("📚 Bộ công cụ học tiếng Trung")

st.caption(
    "Tập hợp các công cụ miễn phí giúp người học, giáo viên và nhà phát triển làm việc với tiếng Trung dễ dàng hơn."
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):

        st.subheader("✍️ Tạo worksheet luyện viết chữ Hán")

        st.write(
            "Tạo worksheet đẹp, có thể in được và điều chỉnh lưới tùy ý."
        )

        st.write(
            "✅ Xuất PDF\n"
            "✅ Tùy chỉnh lưới\n"
            "✅ Phù hợp cho lớp học và tự học"
        )

        if st.button(
            "Mở trình tạo worksheet",
            use_container_width=True,
            key="practice",
        ):
            st.switch_page("pages/01_Practice_Sheet.py")

with col2:
    with st.container(border=True):

        st.subheader("🧠 Bộ tách từ tiếng Trung")

        st.write(
            "Tách câu tiếng Trung thành các token bằng thuật toán Viterbi."
        )

        st.write(
            "⚡ Nhanh chóng\n"
            "🎯 Độ chính xác cao\n"
            "📚 Từ điển hơn 30k từ"
        )

        if st.button(
            "Mở bộ tách từ",
            use_container_width=True,
            key="tokenizer",
        ):
            st.switch_page("pages/02_viterbi_tokenizer.py")

st.divider()

st.subheader("🚀 Sắp ra mắt")

c1, c2, c3 = st.columns(3)

with c1:
    with st.container(border=True):
        st.markdown("### 📖 Từ điển")
        st.caption("Tra cứu Trung-Việt")

with c2:
    with st.container(border=True):
        st.markdown("### 🈶 Phân tích chữ Hán")
        st.caption("Bộ thủ và thành phần chữ")

with c3:
    with st.container(border=True):
        st.markdown("### 📝 Flashcards")
        st.caption("Tạo thẻ học Anki")