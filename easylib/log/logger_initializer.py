import logging

from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler


class TimedRotatingLoggerInitializer:

    def __init__(self,
                 path='/tmp/easylib.log',
                 name=None,
                 when='D',
                 interval=1,
                 backup_count=5,
                 format='%(asctime)s - %(levelname)s - %(name)s - %(filename)s - %(lineno)d - %(funcName)s -%(message)s',
                 level=logging.INFO):
        self.name = name
        self.path = path
        self.level = level
        self.when = when
        self.interval = interval
        self.backup_count = backup_count
        self.format = format

    def initialize(self):
        formatter = logging.Formatter(self.format)
        handler = TimedRotatingFileHandler(
            filename=self.path,
            when=self.when,
            interval=self.interval,
            backupCount=self.backup_count,
            encoding='utf8')
        handler.setFormatter(formatter)
        logger = logging.getLogger(self.name)
        logger.addHandler(handler)
        logger.setLevel(self.level)
        logger.info('Logger %s initialized.' % logger.name)


class RotatingLoggerInitializer:

    def __init__(self,
                 path='/tmp/easylib.log',
                 name=None,
                 max_bytes=5 * 1024 * 1024,
                 backup_count=5,
                 format='%(asctime)s - %(levelname)s - %(name)s - %(filename)s - %(lineno)d - %(funcName)s -%(message)s',
                 level=logging.INFO):
        self.name = name
        self.format = format
        self.backup_count = backup_count
        self.path = path
        self.max_bytes = max_bytes
        self.level = level

    def initialize(self):
        formatter = logging.Formatter(self.format)
        handler = RotatingFileHandler(
            filename=self.path,
            mode='a',
            maxBytes=self.max_bytes,
            backupCount=self.backup_count,
            encoding='utf8')
        handler.setFormatter(formatter)
        logger = logging.getLogger(self.name)
        logger.addHandler(handler)
        logger.setLevel(self.level)
        logger.info('Logger %s initialized.' % logger.name)
