import os
import logging
from pathlib import Path

# Use Pathlib for cleaner path management
BASE_DIR = Path(__file__).resolve().parent

# Fetch token from environment variable, or fallback to your token string
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "<INSERT_TOKEN_HERE>")

# Configure logging with a stream handler so you can see logs in the console too
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(BASE_DIR / "logs.txt", encoding="utf-8"),
        logging.StreamHandler()  # Prints to terminal/screen
    ]
)

logger = logging.getLogger("speech_bot")
