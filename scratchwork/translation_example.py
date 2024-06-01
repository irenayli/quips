import logging
import time

from utils.translation import translate


logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s:%(name)s:%(filename)s - %(message)s',
    handlers=[logging.FileHandler(f'logs/log_{time.strftime("%Y%m%d")}.log'), logging.StreamHandler()]
)


translate('hello! I am a potato', 'cmn')