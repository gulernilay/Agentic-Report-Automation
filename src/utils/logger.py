from loguru import logger
import sys
from .config import settings

def setup_logger():
    logger.remove()
    logger.add(sys.stdout, level=settings.LOG_LEVEL.upper(), colorize=True,
               format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>")
    return logger

logger = setup_logger()
