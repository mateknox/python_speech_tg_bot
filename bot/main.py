import telebot
import speech_recognition as sr
import subprocess
from config import *

recognition = sr.Recognizer()
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    logging.info(f"Got a start msg: ${message}")
    bot.send_message(message.chat.id, 'Bot for speech to text translation. Send voice to start the process.',
                     parse_mode='Markdown')


@bot.message_handler(content_types=['voice'])
def voice_handler(message):
    logging.info(f"Got a voice message: ${message}")
    file_id = message.voice.file_id
    file = bot.get_file(file_id)

    download_file = bot.download_file(file.file_path)
    with open('audio.ogg', 'wb') as file:
        file.write(download_file)

    try:
        voice_text = voice_recognizer('ru_RU')
        bot.send_message(message.chat.id, voice_text)
    finally:
        os.remove('audio.wav')
        os.remove('audio.ogg')


def voice_recognizer(language):
    logging.info("Trying to parse voice.")
    subprocess.run(['ffmpeg', '-i', 'audio.ogg', 'audio.wav', '-y'])
    file = sr.AudioFile('audio.wav')
    with file as source:
        try:
            audio = recognition.record(source)
            text = recognition.recognize_google(audio, language=language)
        except Exception as e:
            logging.info(f"Exception: ${e}")
            text = 'Words not recognized.'
    return text


if __name__ == '__main__':
    bot.polling(True)
