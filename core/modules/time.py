
import datetime
from core.utils.log import logger

def get_time():
    now = datetime.datetime.now()
    logger.info(f"The current time is {now.strftime('%H:%M')}")
