
import cv2
import cvzone
import math
import time
import datetime
import threading
import numpy as np

from ultralytics import YOLO
from telegram_utils import send_telegram
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from model.classname import *
from constants import *



def isInside(points, corner):
    if len(points) >= 3:
        polygon = Polygon(points)
        corner = Point(corner)
        # print(polygon.contains(corner))
        return polygon.contains(corner)
    else:
        return False

class YoloDetect():
    def __init__(self):
        self.model = YOLO("model/yolov8n.pt")  # load a pretrained model (recommended for training)
        self.last_alert_alarm = None
        self.alert_telegram_each = 20  # seconds time delay gửi thông báo
        self.last_alert = None
        self.alert_alarm = 3.5 # seconds
        self.detectFlag = ''
        self.on_Alarm = True
        # self.sensitive = _sensitive
    
    #Vẽ detech đối tượng
    def draw_prediction(self, frame, points, cls, conf, x1, y1, x2, y2, w, h, win, soundDefault):
        # Tính toạ độ Centroid
        top_left = (x1, y1)
        top_right = (x2, y1)
        bottom_left = (x1, y2)
        bottom_right = ( x2, y2)
        centroid = ((x1+x2)//2, (y1+y2)//2)
    
        cv2.circle(frame, top_left, 5, (255, 0, 255), -1)
        cv2.circle(frame, top_right, 5, (255, 0, 255), -1)
        cv2.circle(frame, bottom_left, 5, (255, 0, 255), -1)
        cv2.circle(frame, bottom_right, 5, (255, 0, 255), -1)
        cv2.circle(frame, centroid, 5, (255, 0, 255), -1)
        
        cvzone.cornerRect(frame, (x1, y1, w, h), l= 9, rt= 2, colorR=(255, 0, 255))
        cvzone.putTextRect(frame, f'{classNames[cls]} {conf}', (max(0 , x1), max(35, y1)), scale=1, thickness=1, offset=3)
        
        corners = [top_left, top_right, bottom_left, bottom_right, centroid]

        # Duyệt qua các góc trong mảng
        for corner in corners:
        # Kiểm tra xem tọa độ góc có nằm trong tập hợp các điểm points không
            if isInside(points, corner):
                # Gọi hàm alert và trả về kết quả của hàm
                self.detectFlag  = win
                frame = self.alert(frame, win)
                if self.on_Alarm:
                    self.sound_warning(win, soundDefault)
                

        
    def detect_Flag(self):
        return self.detectFlag 

    def ON_Alarm(self, detect):
        self.on_Alarm = not self.on_Alarm
        if detect:
            if self.on_Alarm:
                imgBG[380:380 + ico_h , 1150:1150 + ico_w] =  ico_on_rs
            else:
                imgBG[380:380 + ico_h, 1150:1150 + ico_w] =  ico_off_rs



    def sound_warning(self,win, soundDefault):
        # Delay âm thanh cảnh báo
        if (self.last_alert_alarm is None) or((datetime.datetime.utcnow() - self.last_alert_alarm).total_seconds() > self.alert_alarm):
            self.last_alert_alarm = datetime.datetime.utcnow()
            print(soundDefault)
            if soundDefault:
                if win == win_c1:
                    alarm1.play()
                elif win == win_c2:
                    alarm2.play()
                elif win == win_c3:
                    alarm3.play()
                elif win == win_c4:
                    alarm4.play()
            else:
                alarm = pygame.mixer.Sound('src/sound/api.mp3')
                alarm.play()

    def alert(self, img, win):
        
        #Hiện Text Cảnh Báo
        cv2.putText(img, 'ALARM!!!', (5, 315), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.rectangle(img, (5, 350), (260, 325) , (96, 96, 96), -1)
        cv2.putText(img, str(datetime.datetime.utcnow()), (5, 345), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.imwrite("detect_file/imgDetect.png", img)
        # Delay Gửi tin nhắn sau 15 giây
        if (self.last_alert is None) or (
                (datetime.datetime.utcnow() - self.last_alert).total_seconds() > self.alert_telegram_each):
            self.last_alert = datetime.datetime.utcnow()
            if win == win_c1:
                cv2.imwrite("detect_file/alert1.png", cv2.resize(cv2.imread(photo), dsize=None, fx=1, fy=1))
                imgDetech = cv2.resize(cv2.imread(photo1), (320, 230))
            elif win == win_c2:
                cv2.imwrite("detect_file/alert2.png", cv2.resize(cv2.imread(photo), dsize=None, fx=1, fy=1))
                imgDetech = cv2.resize(cv2.imread(photo2), (320, 230))
            elif win == win_c3:
                cv2.imwrite("detect_file/alert3.png", cv2.resize(cv2.imread(photo), dsize=None, fx=1, fy=1))
                imgDetech = cv2.resize(cv2.imread(photo3), (320, 230))
            elif win == win_c4:
                cv2.imwrite("detect_file/alert4.png", cv2.resize(cv2.imread(photo), dsize=None, fx=1, fy=1))
                imgDetech = cv2.resize(cv2.imread(photo4), (320, 230))
            thread = threading.Thread(target=send_telegram, args=(win,))
            thread.start()
            
        imgBG[437:437 + 230, 948:948 + 320] =  cv2.resize(cv2.imread(photo), (320, 230))   
        return img

    def detect(self, frame, points, win, sensitive, soundDefault):
         # Vẽ Box
        for result in self.model(frame, stream=True):
        #Lấy toạ độ boxes(Hộp giới hạn) của đối tượng
            boxes = result.boxes
            for box in boxes:
                
                # góc trên cùng bên trái (x1, y1) và góc dưới cùng bên phải (x2, y2)
                x1, y1, x2, y2 = box.xyxy[0] 
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # as về interger 
                w, h = x2-x1, y2-y1
                bbox =int(x1), int(y1), int(w), int(h)
                # Độ chính xác - vẽ hình chữ nhật độ chính xác
                conf = math.ceil((box.conf[0]*100))/100            
                # Lớp nhận dạng
                cls = int(box.cls[0]) # Chỉ số class
                print(sensitive)
                if classNames[cls] == 'person' and conf >= float(sensitive) :  
                    # self.person_handle(frame, points, cls, conf, x1, y1, x2, y2, w, h)
                    self.draw_prediction(frame, points, cls, conf, x1, y1, x2, y2, w, h, win, soundDefault)
        return frame