''' Logger setup'''
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from config import LOGGING_CONFIG

_LOGGER = None

def setup_logger():
    ''' Sets up logger'''
    global _LOGGER
    logger = logging.getLogger("nyc-airbnb-data-pipeline") # Pipeline name

    if  logger.hasHandlers():
        _LOGGER = logger
        return _LOGGER

    # Create folder for log files if not exists
    script_directory = Path(__file__).resolve().parent

    log_path = script_directory / LOGGING_CONFIG['log_file']
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Set logging level
    logging_level = getattr(logging, LOGGING_CONFIG['level'].upper(), logging.INFO)
    logger.setLevel(logging_level)

    # Rotating file handler
    file_handler = RotatingFileHandler(log_path,
                                    maxBytes=LOGGING_CONFIG['max_bytes'],
                                    backupCount=LOGGING_CONFIG['backup_count'],
                                    encoding="utf-8")
    formatter = logging.Formatter(LOGGING_CONFIG['format'])
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    _LOGGER = logger

def get_logger():
    ''' Returns existing logger '''
    if _LOGGER is None:
        setup_logger()
    return _LOGGER
