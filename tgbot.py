import telebot
import requests
import soundfile as sf


TELEGRAM_API_TOKEN = ''
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)


@bot.message_handler(content_types=['voice'])
def save_audio(message):
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TELEGRAM_API_TOKEN, file_info.file_path))
    f = open("C:\Boot\output.ogg", 'wb')
    f.write(file.content)
    f.close()
    data, samplerate = sf.read('C:\Boot\output.ogg')
    sf.write('C:\Boot\new_file.wav', data, samplerate=16000)


@bot.message_handler(content_types=['photo'])
def save_photo(messqge)


bot.polling()
