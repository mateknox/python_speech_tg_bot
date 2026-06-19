import os
import logging
import subprocess
import telebot
import speech_recognition as sr
from config import TOKEN

# Initialize logging and tools
logger = logging.getLogger("speech_bot")
recognition = sr.Recognizer()
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    logger.info(f"Received start/help command from chat_id: {message.chat.id}")
    welcome_text = (
        "🤖 *Speech-to-Text Bot*\n\n"
        "Send me any voice message, and I will transcribe it into text for you!"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown')


@bot.message_handler(content_types=['voice'])
def voice_handler(message):
    chat_id = message.chat.id
    logger.info(f"Received voice message from chat_id: {chat_id}")

    # Generate unique filenames based on chat_id to prevent multi-user collision
    ogg_filename = f"audio_{chat_id}.ogg"
    wav_filename = f"audio_{chat_id}.wav"

    try:
        # Download file from Telegram
        file_id = message.voice.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open(ogg_filename, 'wb') as f:
            f.write(downloaded_file)

        # Transcribe audio
        voice_text = voice_recognizer(ogg_filename, wav_filename, language='ru-RU')
        bot.send_message(chat_id, voice_text)

    except Exception as e:
        logger.error(f"Error handling voice message: {e}", exc_info=True)
        bot.send_message(chat_id, "⚠️ An error occurred while processing your audio.")

    finally:
        # Safely clean up files if they exist
        for filename in (ogg_filename, wav_filename):
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                except OSError as e:
                    logger.error(f"Could not delete temporary file {filename}: {e}")


def voice_recognizer(ogg_path, wav_path, language):
    logger.info(f"Converting {ogg_path} to WAV...")

    # Run ffmpeg. stderr=subprocess.DEVNULL keeps logs clean unless there is a system crash
    subprocess.run(['ffmpeg', '-i', ogg_path, wav_path, '-y'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not os.path.exists(wav_path):
        logger.error("FFmpeg conversion failed. WAV file not created.")
        return "Failed to process audio file formatting."

    logger.info("Processing speech recognition...")
    recognizer_file = sr.AudioFile(wav_path)

    with recognizer_file as source:
        try:
            audio = recognition.record(source)
            # Google Speech recognition uses hyphens (ru-RU), not underscores (ru_RU)
            text = recognition.recognize_google(audio, language=language)
        except sr.UnknownValueError:
            logger.warning("Google Speech Recognition could not understand audio.")
            text = 'Sorry, I couldn\'t recognize any words.'
        except sr.RequestError as e:
            logger.error(f"Could not request results from Google Speech Recognition service; {e}")
            text = 'Service temporarily unavailable.'
        except Exception as e:
            logger.error(f"Unexpected error during recognition: {e}")
            text = 'An unexpected error occurred during transcription.'

    return text


if __name__ == '__main__':
    logger.info("Bot started successfully...")
    # infinite_loop=True keeps the bot running even if it encounters network timeouts
    bot.infinity_polling()
