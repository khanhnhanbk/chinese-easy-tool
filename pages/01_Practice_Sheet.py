from typing import Any

import streamlit as st

from datas.usersetting import UserSettings, SeparatorEnum
from services.generate_practice_sheet import ChinesePracticeSheetGenerator

st.set_page_config(
    page_title="Hanzi Practice PDF Generator",
    page_icon="✍️",
    layout="wide",
)

st.title("✍️ Hanzi Practice PDF Generator")
st.markdown(
    "Tạo worksheet luyện viết chữ Hán có thể in, bố cục cân đối, gợi ý hữu ích và tải xuống đơn giản."
)

# ======================
# SESSION STATE INIT
# ======================
default_state: dict[str, Any] = {
    "text": "",
    "output_filename": "output.pdf",
    "grid_size": 45,
    "trace_columns": 5,
    "margin_left": 25,
    "margin_top": 35,
    "show_pinyin": True,
    "multi_char_line": False,
    "allow_duplicate": False,
    "separator_label": "TỰ ĐỘNG (ANY)",
    "pdf_ready": False,
    "pdf_bytes": None,
    "last_generated_filename": "output.pdf",
}

for k, v in default_state.items():
    st.session_state.setdefault(k, v)

separator_map = {
    "XUỐNG DÒNG (ENTER)": SeparatorEnum.ENTER,
    "DẤU PHẨY (COMMA)": SeparatorEnum.COMMA,
    "CHẤM PHẨY (SEMICOLON)": SeparatorEnum.SEMICOLON,
    "TỰ ĐỘNG (ANY)": SeparatorEnum.ANY,
}

# ======================
# UI LAYOUT
# ======================
left, right = st.columns([2.5, 1], gap="large")

with left:
    st.subheader("🧾 Nội dung worksheet")

    text = st.text_area(
        "Nhập chữ Hán hoặc cụm từ",
        value=st.session_state["text"],
        height=280,
    )

    with st.expander("⚙️ Cài đặt nâng cao", expanded=True):
        c1, c2 = st.columns(2)

        with c1:
            grid_size = st.slider("Kích thước ô", 30, 80, st.session_state["grid_size"])
            trace_columns = st.slider(
                "Số cột luyện nét", 1, 10, st.session_state["trace_columns"]
            )
            margin_left = st.slider("Lề trái", 10, 80, st.session_state["margin_left"])
            margin_top = st.slider("Lề trên", 10, 80, st.session_state["margin_top"])

        with c2:
            show_pinyin = st.checkbox(
                "Hiển thị Pinyin", st.session_state["show_pinyin"]
            )
            multi_char_line = st.checkbox(
                "Chế độ từ ghép", st.session_state["multi_char_line"]
            )
            allow_duplicate = st.checkbox(
                "Cho phép trùng ký tự", st.session_state["allow_duplicate"]
            )

            separator_label = st.selectbox(
                "Dấu phân tách",
                list(separator_map.keys()),
                index=list(separator_map.keys()).index(
                    st.session_state["separator_label"]
                ),
            )

with right:
    st.subheader("📦 Output")

    output_filename = st.text_input(
        "Tên file PDF",
        value=st.session_state["output_filename"],
    )

    st.markdown("---")

    st.markdown(
        "**Gợi ý nhanh:**\n"
        "- Ô lớn phù hợp người mới bắt đầu.\n"
        "- Chỉ bật Pinyin khi cần hỗ trợ phát âm.\n"
        "- Dùng chế độ từ ghép khi muốn luyện tập từ ghép."
    )

    # ======================
    # 2 BUTTONS SIDE BY SIDE
    # ======================
    btn_col1, btn_col2 = st.columns(2)

    with btn_col1:
        generate_clicked = st.button("🚀 Tạo PDF", use_container_width=True)

    with btn_col2:
        download_clicked = False
        if st.session_state["pdf_ready"]:
            download_clicked = st.download_button(
                label="⬇️ Tải PDF",
                data=st.session_state["pdf_bytes"],
                file_name=st.session_state["last_generated_filename"],
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.button("⬇️ Tải PDF", disabled=True, use_container_width=True)

# ======================
# GENERATE LOGIC
# ======================
if generate_clicked:
    if not text.strip():
        st.warning("Vui lòng nhập chữ Hán trước khi tạo worksheet.")
    else:
        st.session_state.update(
            {
                "text": text,
                "output_filename": output_filename,
                "grid_size": grid_size,
                "trace_columns": trace_columns,
                "margin_left": margin_left,
                "margin_top": margin_top,
                "show_pinyin": show_pinyin,
                "multi_char_line": multi_char_line,
                "allow_duplicate": allow_duplicate,
                "separator_label": separator_label,
            }
        )

        settings = UserSettings(
            grid_size=grid_size,
            trace_columns=trace_columns,
            margin_left=margin_left,
            margin_top=margin_top,
            show_pinyin=show_pinyin,
            multi_char_line=multi_char_line,
            allow_duplicate=allow_duplicate,
            separator=separator_map[separator_label],
            output_filename=output_filename or "output.pdf",
        )

        generator = ChinesePracticeSheetGenerator(
            characters=text, user_settings=settings
        )

        pdf = generator.generate()
        pdf_bytes = pdf.getvalue() if hasattr(pdf, "getvalue") else pdf

        st.session_state["pdf_bytes"] = pdf_bytes
        st.session_state["last_generated_filename"] = settings.output_filename

        st.session_state["pdf_ready"] = True
        st.success(f"Đã tạo worksheet: **{settings.output_filename}**")
        st.rerun()