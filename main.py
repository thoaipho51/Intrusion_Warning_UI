import cv2
import numpy as np

import streamlit as st
import requests
import time

from imutils.video import VideoStream
from yolodetect import YoloDetect   

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
    sensitive_list = ["Vừa phải", "Nhạy", "Rất nhạy"]
    sensitive = st.selectbox('Độ nhạy phát hiện', sensitive_list)
    index_sensitive = sensitive_list.index(sensitive)
    if index_sensitive == 0:
        #st.write("Độ Nhạy: Vừa phải")
        senSitive = 0.75
    elif index_sensitive == 1:
        #st.write("Độ Nhạy: Nhạy")
        senSitive = 0.5
    elif index_sensitive == 2:
        #st.write("Độ Nhạy: Rất nhạy")
        senSitive = 0.2
    
    
    choose_list = ["Giọng nói mặc định", "Thiết lập giọng nói thủ công"]
    result = st.selectbox('Lựa chọn của bạn', choose_list)
    index_choose = choose_list.index(result)
    if index_choose + 1 == 2:
        payload = st.text_area('Nhập giọng nói cảnh báo')
        if len(payload) < 10:
            st.warning('Giọng nói cảnh báo phải có ít nhất 10 ký tự')
        else:
            if st.button('Áp dụng cảnh báo'):
                get_audio(payload)
    else:
        st.write("Thiết lập giọng nói mặc định")
    

with col2:
    
    cam1 =st.text_input('Input RTSP link 1')
    cam2 =st.text_input('Input RTSP link 2')
    cam3 =st.text_input('Input RTSP link 3')
    cam4 =st.text_input('Input RTSP link 4')
    
if st.button('Khởi động hệ thống'):
    soundDefault = True
    if os.path.isfile('./src/sound/api.mp3'):
        file_size_on_disk = os.path.getsize('./src/sound/api.mp3')
        if file_size_on_disk is not False and file_size_on_disk >= 1000:
            soundDefault = False
        
    st.write(soundDefault)
    #  TEST ERROR CAMERA 1
    if cam1.isdigit():
        if cam1 == "0":
            cam1 = int(cam1)
        else:
            st.write(f"Link Camera 1 lỗi !! Hệ thống sẽ dùng RTSP mặc định")
            cam1 = default_camera

    # SRC Camera
    camera_1 = cam1
    cap2 = cv2.VideoCapture(cam2)
    if not cap2.isOpened():
        st.write(f"Link Camera 2 lỗi !! Hệ thống sẽ dùng RTSP mặc định")
        camera_2 = default_camera
    else:
        camera_2 = cam2
        
    cap3 = cv2.VideoCapture(cam3)
    if not cap3.isOpened():
        st.write(f"Link Camera 3 lỗi !! Hệ thống sẽ dùng RTSP mặc định")
        camera_3 = default_camera
    else:
        camera_3 = cam3

    cap4 = cv2.VideoCapture(cam4)
    if not cap4.isOpened():
        st.write(f"Link Camera 4 lỗi !! Hệ thống sẽ dùng RTSP mặc định")
        camera_4 = default_camera
    else:
        camera_4 = cam4

#----------------------------------------------------------------


    # Danh sách các nguồn camera
    camera_srcs = [camera_1, camera_2, camera_3, camera_4]

    # Mở cửa sổ và luồng video cho mỗi nguồn camera
    windows = []
    videos = []
    list_points = []
    list_vwrt = []

    for idx, src in enumerate(camera_srcs):
        window_name = "Camera " + str(idx+1)
        cv2.namedWindow(window_name)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
        windows.append(window_name)
        video = VideoStream(src=src).start()
        videos.append(video)
        list_points.append([])
        vwrt = cv2.VideoWriter(f'detect_file/video_alarm{idx + 1}.avi', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 20.0, (f_width,f_height))
        list_vwrt.append(vwrt)
        


    #========================== SETUP ================================
    # Chua cac diem nguoi dung chon de tao da giac

    win_c1, win_c2, win_c3, win_c4 = windows

    # new model Yolo - Khởi tạo model Yolo và khai báo lớp nhận diện
    model = YoloDetect()

    detect = False

    #Sự kiện click chuột trái để vẻ điểm 
    def handle_left_click(event, x, y, flags, param):
        points, window  = param
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append([x, y]) 
            click.play()
            if len(points) == 4:
                if window == win_c1:
                    print(f'Nhấn phím 1 để kết thúc vùng detect cho {window}')
                    key1.play()
                if window == win_c2:
                    print(f'Nhấn phím 2 để kết thúc vùng detect cho {window}')
                    key2.play()
                if window == win_c3:
                    print(f'Nhấn phím 3 để kết thúc vùng detect cho {window}')
                    key3.play()
                if window == win_c4:
                    print(f'Nhấn phím 4 để kết thúc vùng detect cho {window}')
                    key4.play()
            if len(points) == 5:
                detect_key.play()

    #Vẽ các đa giác trên khung hình camera
    def draw_polygon (frame, points):
        
        for point in points:
            frame = cv2.circle(frame, (point[0], point[1]), 4, (0, 0, 255), -1) #BGR

        frame = cv2.polylines(frame, [np.int32(points)], False, (234, 78, 57), thickness=2)
        return frame

    #========================== ================================

    # Vòng lặp chính
    while True:
        
        # Đọc từng khung hình từ từng luồng video
        frames = []
        
        for idx, (video,window) in enumerate(zip(videos, windows)): 
            if window == 'Camera ' + str(idx+1):
                #Đọc và resize lại kích thước video
                frame = video.read()
                if frame is None:
                    continue
                frame = cv2.resize(frame, (f_width, f_height))

                # Ve ploygon
                frame = draw_polygon(frame, list_points[idx])
                # print(list_points)
                if detect:
                    frame = model.detect(frame= frame, points= list_points[idx], win= window, sensitive = senSitive, soundDefault= soundDefault)
                
                # add frame vào list frames
                frames.append(frame)


            for frame, vwrt in zip(frames, list_vwrt):
                if window == 'Camera ' + str(idx+1):
                    cv2.setMouseCallback(window, handle_left_click, (list_points[idx], window))
                    if model.detect_Flag() == window:
                        vwrt.write(frame)
                    if idx == 0:
                        imgBG[8:8 + f_height, 5:5 + f_width] = frame
                    elif idx == 1:
                        # imgBG[73:73 + f_height, (30 + 440):(30 + 440) + f_width] = frame
                        imgBG[8:8 + f_height, 470:470 + f_width] = frame

                    elif idx == 2:
                        # imgBG[(73 + 325):(73 + 325) + f_height, 30:30 + f_width] = frame
                        imgBG[362 :362 + f_height, 5:5 + f_width] = frame

                    elif idx == 3:
                        # imgBG[(73 + 325):(73 + 325) + f_height, (30 + 440):(30 + 440) + f_width] = frame
                        imgBG[362 :362 + f_height, 470:470 + f_width] = frame


                if detect:
                    cv2.imshow('Intrusion Warning', imgBG)
                    cv2.setWindowProperty('Intrusion Warning', cv2.WND_PROP_TOPMOST, 1)
                    

                else:
                    cv2.imshow('Setting', howToUse) # setting app
                    cv2.setWindowProperty('Setting', cv2.WND_PROP_TOPMOST, 1)
                    cv2.imshow(window, frame)

        
        key = cv2.waitKey(1)
        if key == ord('q'):
            # Đường dẫn tới file cần xoá
            file_path = 'src/sound/api.mp3'

            # Kiểm tra xem file có tồn tại không
            if os.path.exists(file_path):
                # Nếu có, xoá file
                os.remove(file_path)
                print(f"File '{file_path}' đã được giải phóng.")
            else:
                # Nếu không, thông báo lỗi
                print(f"File '{file_path}' không tồn tại.")
            break
        elif key == ord('d'):
            detect = True 
            if cv2.getWindowProperty("Setting", cv2.WND_PROP_VISIBLE) != 0:
                cv2.destroyWindow('Setting')
                start_alarm.play()
        elif key == ord('f'):
            detect = False
            #check cửa sổ
            if cv2.getWindowProperty("Intrusion Warning", cv2.WND_PROP_VISIBLE) != 0:
                cv2.destroyWindow("Intrusion Warning")
                reset_zone.play()
            #reset vùng cảnh báo
            for idx, points in enumerate(list_points):
                list_points[idx]= []
                
        elif key == ord('o'):
            model.ON_Alarm(detect)
            ring_sound.play()

        else:
            for idx, points in enumerate(list_points):
                if key == ord(str(idx + 1)):
                    if len(points) >= 3:
                        end_detect.play()
                        points.append(points[0])
                    else:
                        pass

            

    # Dừng luồng video và đóng các cửa sổ

    for vwrt in list_vwrt:
        vwrt.release()
    for video in videos:
        video.stop()
    cv2.destroyAllWindows()
    
