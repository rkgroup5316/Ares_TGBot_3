import logging
from logging.handlers import RotatingFileHandler


# Configure logger
logger = logging.getLogger('telegram_bot')
logger.setLevel(logging.INFO)

# Formatter for log messages
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)


file_handler = RotatingFileHandler("logs.txt", mode="w+", maxBytes=10000000, backupCount=2)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


# Add console handler to the logger
logger.addHandler(console_handler)


