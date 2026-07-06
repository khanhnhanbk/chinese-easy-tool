import streamlit as st

st.set_page_config(page_title="Chinese Learning Toolkit", page_icon="📚", layout="wide")

st.title("📚 Chinese Learning Toolkit")

tool = st.sidebar.selectbox(
    "Choose tool", ["Home", "Hanzi Practice PDF", "Viterbi Tokenizer"]
)

if tool == "Home":
    st.write("""
    Welcome!

    Choose a tool from the sidebar.

    Current tools:
    - ✍️ Hanzi Practice PDF
    - 🧠 Viterbi Tokenizer
    """)

elif tool == "Viterbi Tokenizer":
    st.switch_page("pages/02_viterbi_tokenizer.py")

elif tool == "Hanzi Practice PDF":
    st.switch_page("pages/01_Practice_Sheet.py")
