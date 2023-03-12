import streamlit as st

st.set_page_config(page_title="Setup RTSP", page_icon=":wrench:", layout= "wide")


# st.title(':wrench:')
st.markdown(
    f"<h1 style='text-align: center;'>Cấu Hình Thông Số RTSP </h1>",
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)
# --- HEADER 

btn_check = False

with col1:
    choose_list = ["Giọng nói mặc định", "Thiết lập giọng nói thủ công"]
    result = st.selectbox('Lựa chọn của bạn', choose_list)
    index = choose_list.index(result)
    if index + 1 == 2:
        setup_voice = st.text_area('Nhập giọng nói cảnh báo', disabled=False)
        btn_check = st.button('Thiết lập',disabled=False)
    else:
        setup_voice = st.text_area('Nhập giọng nói cảnh báo', disabled=True)
        btn_check = st.button('Thiết lập', disabled=True)
    
st.write(btn_check)

with col2:

    src1 =st.text_input('Nhập src thứ 1')
    src2 =st.text_input('Nhập src thứ 2')
    src3 =st.text_input('Nhập src thứ 3')
    src4 =st.text_input('Nhập src thứ 4')

