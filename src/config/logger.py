
"""
LOGGING MODULE: AN INStANCE WHICH LOG THE ERRORS AND INFOS OF ALL MODULES
"""


import logging
from src.config.config import LOGGING_FILE_PATH

#!BASIC CONFIG

logging.basicConfig(
    level=logging.INFO,
    filename="logs/scraper.logs",
    filemode='w',
    format="%(asctime)s | %(levelname)s | %(filename)s | %(message)s"   
)


#*LOGGER INSTANCE

logger = logging.getLogger(__name__)
