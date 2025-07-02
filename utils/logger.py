import logging
import os
from datetime import datetime

def get_logger(name="logger"):
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        # 建立 log 資料夾
        log_dir = "log"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 檔名
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"{name}_{now}.log"
        log_path = os.path.join(log_dir, log_filename)
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # File Handler
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        # 設定日誌輸出格式
        formatter = logging.Formatter(
            '[%(asctime)s][%(name)s][%(levelname)s]_%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)


    return logger