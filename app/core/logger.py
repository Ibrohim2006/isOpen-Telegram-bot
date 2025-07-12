import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime
import pytz

tz = pytz.timezone("Asia/Tashkent")

def setup_logger(name: str = "bot"):
    """Configure and return a logger instance"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # File handler with rotation (10 files of 1MB each)
    file_handler = RotatingFileHandler(
        log_dir / "bot.log",
        maxBytes=1024*1024,  # 1MB
        backupCount=10,
        encoding='utf-8'
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def tz_aware_now():
    """Return timezone-aware current datetime"""
    return datetime.now(tz)

class TelegramLogsHandler(logging.Handler):
    """Custom handler to send critical logs to Telegram admin"""
    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id
        self.setLevel(logging.ERROR)

    def emit(self, record):
        log_entry = self.format(record)
        try:
            asyncio.create_task(
                self.bot.send_message(
                    chat_id=self.chat_id,
                    text=f"🚨 ERROR LOG:\n<code>{log_entry}</code>",
                    parse_mode="HTML"
                )
            )
        except Exception as e:
            print(f"Failed to send log to Telegram: {e}")

# Initialize the main logger
logger = setup_logger()