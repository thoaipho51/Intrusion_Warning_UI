import streamlit as st
import requests
import time
import cv2
from constants import *
st.set_page_config(page_title="Setup RTSP", page_icon=":wrench:", layout= "wide")

st.markdown(
    f"<h1 style='text-align: center;'>Cấu Hình Thông Số RTSP </h1>",
    unsafe_allow_html=True
)
col1, col2 = st.columns(2)




def get_audio(payload):
    url = 'https://api.fpt.ai/hmi/tts/v5'
    headers = {
        'api-key': 'CKhFlS2M8VGts6QSwEz5YiqzwdmgIJtW',
        'speed': '0.5',
        'voice': 'linhsan'
        }

    response = requests.request('POST', url, data=payload.encode('utf-8'), headers=headers)

    audio_url = response.json()['async']

    r = requests.get(audio_url, stream=True)

    with open('./src/sound/api.mp3', 'wb') as f:
        f.write(r.content)


    file_size_on_disk = os.path.getsize('./src/sound/api.mp3')
    if file_size_on_disk >= 1000:
        st.write("Thiết lập giọng nói thành công")
    else:
        st.write("Tải thất bại, vui lòng thử lại !")


with col1:
    choose_list = ["Giọng nói mặc định", "Thiết lập giọng nói thủ công"]
    result = st.selectbox('Lựa chọn của bạn', choose_list)
    index = choose_list.index(result)
    if index + 1 == 2:
        payload = st.text_area('Nhập giọng nói cảnh báo')
        if len(payload) < 10:
            st.warning('Giọng nói cảnh báo phải có ít nhất 10 ký tự')
        else:
            if st.button('Xác nhận'):
                get_audio(payload)
                SoundDefaults = False
    else:
        st.write("Thiết lập giọng nói mặc định")

with col2:
    
    cam1 =st.text_input('Input RTSP link 1')
    cam2 =st.text_input('Input RTSP link 2')
    cam3 =st.text_input('Input RTSP link 3')
    cam4 =st.text_input('Input RTSP link 4')
    
if st.button('Submit'):
    st.write(result)
    st.write(cam1)
    st.write(cam2)
    st.write(cam3)
    st.write(cam4)
    #  TEST ERROR CAMERA 1
    if cam1.isdigit():
        if cam1 == "0":
            cam1 = int(cam1)
        else:
            print(f"Link Camera 1 lỗi !! Hệ thống sẽ dùng RTSP mặc định")
            cam1 = default_camera

    # SRC Camera
    camera_1 = cam1
    cap2 = cv2.VideoCapture(cam2)
    if not cap2.isOpened():
        print(f"Link Camera 2 lỗi !! Hệ thống sẽ dùng RTSP mặc định")
        camera_2 = default_camera
    else:
        camera_2 = cam2
        
    cap3 = cv2.VideoCapture(cam3)
    if not cap3.isOpened():
        print(f"Link Camera 3 lỗi !! Hệ thống sẽ dùng RTSP mặc định")
        camera_3 = default_camera
    else:
        camera_3 = cam3

    cap4 = cv2.VideoCapture(cam4)
    if not cap4.isOpened():
        print(f"Link Camera 4 lỗi !! Hệ thống sẽ dùng RTSP mặc định")
        camera_4 = default_camera
    else:
        camera_4 = cam4
    from main import *
