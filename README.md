# Telegram Speech-to-Text Bot

A lightweight Telegram bot that accepts voice messages, converts them using `FFmpeg`, and transcribes them into text using the Google Speech Recognition API.

## Requirements

1. **Python 3.8+**
2. **FFmpeg**: Must be installed on your system and added to your system's PATH.
   - *Ubuntu/Debian:* `sudo apt install ffmpeg`
   - *macOS:* `brew install ffmpeg`
   - *Windows:* Download binaries from FFmpeg website and add to environment variables.

## Installation

1. Clone the repository and navigate into it.
2. Install dependencies:
   ```bash
   pip install pyTelegramBotAPI SpeechRecognition
