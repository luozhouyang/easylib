import unittest
import logging

from easylib.log import TimedRotatingLoggerInitializer, RotatingLoggerInitializer


class LoggerInitializerTest(unittest.TestCase):

    def testTimedRotatingLoggerInitializer(self):
        logger = logging.getLogger('easylib')
        logger.info('Info from logger easylib.')

        initializer = TimedRotatingLoggerInitializer(name='easylib2', path='/tmp/easylib2.log')
        initializer.initialize()
        logger = logging.getLogger('easylib2')
        logger.info('Info from logger easylib2.')

    def testRotatingLoggerInitializer(self):
        initializer = RotatingLoggerInitializer(name='easylib-rotating-logger', path='/tmp/easylib.rotating.log')
        initializer.initialize()
        logger = logging.getLogger('easylib-rotating-logger')
        logger.info('Info from logger %s' % logger.name)


if __name__ == '__main__':
    unittest.main()
