import logging
import os
import sys

def setup_logging():
    user_home = os.path.expanduser("~")
    
    app_folder_name = "LolSiralamaTakip"
    log_folder_path = os.path.join(user_home, app_folder_name)

    if not os.path.exists(log_folder_path):
        try:
            os.makedirs(log_folder_path)
        except Exception as e:
            log_folder_path = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)

    log_path = os.path.join(log_folder_path, "app.log")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Log dosyası şuraya kaydediliyor: {log_path}")
    return logger

logger = setup_logging()
