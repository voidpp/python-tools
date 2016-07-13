
import os
import sys
import logging

class Colors(object):
    green = '\033[1;32m'
    red = '\033[1;31m'
    cyan = '\033[1;36m'
    yellow = '\033[1;33m'
    default = '\033[0m'

class ColorFactory(object):

    @staticmethod
    def is_output_supports_color():
        """
        Returns True if the running system's terminal supports color, and False
        otherwise.
        """
        plat = sys.platform
        supported_platform = plat != 'Pocket PC' and (plat != 'win32' or 'ANSICON' in os.environ)

        is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
        if not supported_platform or not is_a_tty:
            return False
        return True

    @staticmethod
    def get_colors():
        supp = ColorFactory.is_output_supports_color()
        attrs = {k: getattr(Colors,k) if supp else '' for k in dir(Colors) if k[0] != '_'}
        return type('Colors', (object,), attrs)

class ColoredLoggerFormatter(logging.Formatter):

    def __init__(self, debug):
        super(ColoredFormatter, self).__init__()
        self.debug = debug

    def format(self, record):
        colors = {
            logging.ERROR: Colors.red,
            logging.WARNING: Colors.yellow,
            logging.INFO: Colors.default,
            logging.DEBUG: Colors.cyan
        }

        if self.debug:
            msg = '%s - %s:%s: ' % (datetime.now(), record.name, record.lineno)
            msg += Colors.default + record.getMessage()
        else:
            msg = record.getMessage()

        msg = colors.get(record.levelno, Colors.default) + msg + Colors.default

        if record.exc_info:
            msg += '\n' + self.formatException(record.exc_info)

        return msg
