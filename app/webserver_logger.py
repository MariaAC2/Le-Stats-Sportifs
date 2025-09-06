import logging
from logging.handlers import RotatingFileHandler

# Set up message formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
format_handler = logging.StreamHandler()
format_handler.setFormatter(formatter)

# Set up info handler which is a rotating file handler
info_handler = RotatingFileHandler('file.log', maxBytes=1024, backupCount=3)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)

# Get logger for the rotating file handlers
logger = logging.getLogger()
logger.setLevel(logging.INFO) # set level as INFO
logger.addHandler(format_handler) # add formatter
logger.addHandler(info_handler) # add file handler

# Get logger for errors
error_logger = logging.getLogger("webserver.log")
error_logger.setLevel(logging.ERROR) # set level as ERROR
error_logger.addHandler(format_handler) # add formatter