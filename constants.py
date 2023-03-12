import cv2
import os
import pygame, sys



pygame.init()
wellcome = pygame.mixer.Sound('src/sound/wellcome_start.wav')
wellcome.play()



# telegram API
my_token = "5675089226:AAEeKFKcL3j_Mi7nrK-kSNFo2twCRvnSB8c"
chat_id = "962508308"

senSitive = 0.5



win_c1 = "Camera 1"
win_c2 = "Camera 2"
win_c3 = "Camera 3"
win_c4 = "Camera 4"

# Âm báo ấn phím
key1 = pygame.mixer.Sound('src/sound/key1.wav')
key2 = pygame.mixer.Sound('src/sound/key2.wav')
key3 = pygame.mixer.Sound('src/sound/key3.wav')
key4 = pygame.mixer.Sound('src/sound/key4.wav')

#Âm báo camera xâm nhập 
alarm1 = pygame.mixer.Sound('src/sound/cam1.wav')
alarm2 = pygame.mixer.Sound('src/sound/cam2.wav')
alarm3 = pygame.mixer.Sound('src/sound/cam3.wav')
alarm4 = pygame.mixer.Sound('src/sound/cam4.wav')


click = pygame.mixer.Sound('src/sound/click.wav')
detect_key = pygame.mixer.Sound('src/sound/detect.mp3')
start_alarm = pygame.mixer.Sound('src/sound/start_zone_alarm.wav')
end_detect = pygame.mixer.Sound('src/sound/end_detect.wav')
reset_zone = pygame.mixer.Sound('src/sound/reset_zone_alarm.wav')
ring_sound = pygame.mixer.Sound('src/sound/ring_sound.wav')
default_camera = "src/err.mp4"



#Cấu Hình 
f_width = 460 
f_height = 350 

#Cảnh Báo
ico_w = 50
ico_h = 40
on_Alarm = True
                #settup image
ico_on = cv2.imread('src/on.png')
ico_on_rs = cv2.resize(ico_on, (ico_w, ico_h))
ico_off = cv2.imread('src/off.png')
ico_off_rs = cv2.resize(ico_off, (ico_w, ico_h))


detect_class = 'person' #Lớp cần detect
imgBG = cv2.imread('src/Background.png')
splashScr = cv2.imread('src/splash_screen.png')
howToUse = cv2.imread('src/Use.png')

photo1="detect_file/alert1.png"
photo2="detect_file/alert2.png"
photo3="detect_file/alert3.png"
photo4="detect_file/alert4.png"
photo = "detect_file/imgDetect.png"

video1="detect_file/video_alarm1.avi"
video2="detect_file/video_alarm2.avi"
video3="detect_file/video_alarm3.avi"
video4="detect_file/video_alarm4.avi"







