import logging
import os.path
from enum import IntEnum

TELEMETRY = os.getcwd() + '\\telemetry\\'
ERROR_LOG_FILE = TELEMETRY + 'error.log'
DEBUG_LOG_FILE = TELEMETRY + 'debug.log'
INFO_LOG_FILE =  TELEMETRY + 'info.log'
ALL_FILE_PATHS = [ERROR_LOG_FILE, DEBUG_LOG_FILE, INFO_LOG_FILE]

for file_path in ALL_FILE_PATHS:
    if os.path.exists(file_path):
        os.remove(file_path)

# Init logging
logging.basicConfig(
    filename=ERROR_LOG_FILE,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.basicConfig(
    filename=DEBUG_LOG_FILE,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.basicConfig(
    filename=INFO_LOG_FILE,
    level=logging.BASIC_FORMAT,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class MSG_TYPE:
    ERROR = 0
    DEBUG = 1
    INFO = 2

def log_message(message: str, msg_type: MSG_TYPE, exception_data=None):
    if msg_type == MSG_TYPE.ERROR:
        if exception_data:
            logging.error(f'{message} with exception %s', exception_data, exc_info=True)
        else:
            logging.error(f'{message}')
    if msg_type == MSG_TYPE.DEBUG:
        logging.debug(f'{message}')
    if msg_type == MSG_TYPE.INFO:
        logging.info(f'{message}')
