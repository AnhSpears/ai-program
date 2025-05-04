import logging
from logging.handlers import TimedRotatingFileHandler
import json

def setup_logging(app):
    handler = TimedRotatingFileHandler('app.log', when='midnight', backupCount=7)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
