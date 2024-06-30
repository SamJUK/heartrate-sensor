from datetime import datetime

class Logger:
    LVL_DEBUG = 'DEBUG'
    LVL_INFO = 'INFO'
    LVL_WARNING = 'WARN'
    LVL_ERROR = 'ERR'
    LVL_CRITICAL = 'CRIT'

    def __init__(self, name='main'):
        self.name = name

    def timestamp(self):
        return datetime.now().strftime('%m/%d/%Y %H:%M:%S')

    def log(self, message, level=LVL_INFO, timestamp=True):
        print(f'{ f'[{self.timestamp()}]' if timestamp else ''} {f'{self.name}.{level}'.ljust(12, ' ')} - {message}')

    def debug(self, message):
        return self.log(message, level=self.LVL_DEBUG)
    
    def info(self, message):
        return self.log(message, level=self.LVL_INFO)
    
    def warn(self, message):
        return self.log(message, level=self.LVL_WARNING)
    
    def error(self, message):
        return self.log(message, level=self.LVL_ERROR)
    
    def critical(self, message):
        return self.log(message, level=self.LVL_CRITICAL)