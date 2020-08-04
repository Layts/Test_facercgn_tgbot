import telebot
import requests
import cv2
import numpy as np
import io
import pydub


TELEGRAM_API_TOKEN = ''
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)
AUDIO_PATH = r'C:\Boot\audio'
PHOTO_PATH = r'C:\Boot\photo'
pydub.AudioSegment.converter = r"C:\Boot\ffmpeg\bin\ffmpeg.exe"


@bot.message_handler(content_types=['voice'])
def save_audio(message):
    file_info = bot.get_file(message.voice.file_id)
    print(message)
    
    file = requests.get(f'https://api.telegram.org/file/bot{TELEGRAM_API_TOKEN}/{file_info.file_path}')
    s = io.BytesIO(file.content)
    pydub.AudioSegment.from_raw(s, sample_width=1, frame_rate=16000, channels=1).export(f"{AUDIO_PATH}\\audio_message_0.wav", format='wav')


@bot.message_handler(content_types=['photo'])
def save_photo(message):
    # Load cascade with weights
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # Get file_id from message
    photo_info = message.json['photo'][0]
    file_info = bot.get_file(photo_info['file_id'])
    # Get image as bytes
    file = requests.get(f'https://api.telegram.org/file/bot{TELEGRAM_API_TOKEN}/{file_info.file_path}')
    # Making image from bytes
    nparr = np.fromstring(file.content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if type(faces) == tuple:
        print('На фото нет лиц')
    else:
        # Save photo with faces
        iswritten = cv2.imwrite(f"{PHOTO_PATH}\{photo_info['file_unique_id']}.jpg", img)
        if iswritten:
            print('Фото сохранено')


bot.polling()

