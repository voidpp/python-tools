
class LoggerProxy(object):
    def __init__(self, level):
        self.level = level

    def write(self, msg):
        if msg != '\n':
            self.level(msg)

    def flush(self):
        pass
