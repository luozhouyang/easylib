from easylib.log import TimedRotatingLoggerInitializer

name = 'easylib'

initializer = TimedRotatingLoggerInitializer(name='easylib', path='/tmp/easylib.log')
initializer.initialize()
