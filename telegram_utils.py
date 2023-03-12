import telegram
from constants import *


def send_telegram(win):
    
    try:
        bot = telegram.Bot(token=my_token)
        if win == win_c1:
            bot.sendPhoto(chat_id=chat_id, photo=open(photo1, "rb"), caption="Hình Ảnh Xâm Nhập Từ: " + win_c1)
            bot.sendVideo(chat_id=chat_id, video=open(video1, "rb"), caption="Video Xâm Nhập !!!")
        elif win == win_c2:
            bot.sendPhoto(chat_id=chat_id, photo=open(photo2, "rb"), caption="Hình Ảnh Xâm Nhập Từ: " + win_c2)
            bot.sendVideo(chat_id=chat_id, video=open(video2, "rb"), caption="Video Xâm Nhập !!!")
        elif win == win_c3:
            bot.sendPhoto(chat_id=chat_id, photo=open(photo3, "rb"), caption="Hình Ảnh Xâm Nhập Từ: " + win_c3)
            bot.sendVideo(chat_id=chat_id, video=open(video3, "rb"), caption="Video Xâm Nhập !!!")
        elif win == win_c4:
            bot.sendPhoto(chat_id=chat_id, photo=open(photo4, "rb"), caption="Hình Ảnh Xâm Nhập Từ: " + win_c4)
            bot.sendVideo(chat_id=chat_id, video=open(video4, "rb"), caption="Video Xâm Nhập !!!")
        else:
            pass
    except Exception as ex:
        print("Tin nhắn chưa được gửi do lỗi: ", ex)

    print("Đã gửi thông báo về telegram")

