import logging
from logging.handlers import RotatingFileHandler
import os

log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_handler = RotatingFileHandler(os.path.join(log_dir, 'wobb_ai.log'), maxBytes=5 * 1024 * 1024, backupCount=3)
log_handler.setLevel(logging.DEBUG)
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)

error_handler = RotatingFileHandler(os.path.join(log_dir, 'error.log'), maxBytes=5 * 1024 * 1024, backupCount=3)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(log_formatter)

logger.addHandler(error_handler)
logger.info('Application started')
logger.debug('Debugging the graph generation process')
logger.warning('Data inconsistency detected')
logger.error('Failed to connect to the database')
