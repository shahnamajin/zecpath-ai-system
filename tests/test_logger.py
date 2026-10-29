import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import logger

logger.info("Application Started")
logger.warning("Warning Example")
logger.error("Error Example")