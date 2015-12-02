from threading import Thread, Event
import logging

logger = logging.getLogger(__name__)

class RunnerThread(Thread):
    def __init__(self, callback):
        super(RunnerThread, self).__init__()
        self.__callback = callback

    def run(self):
        try:
            self.__callback()
        except:
            logger.exception("Error occured during timer callback run")

class Timer(Thread):
    """
    Simple repeating timer.
    """
    def __init__(self, interval, callback):
        super(Timer, self).__init__()

        self.interval_event = Event()
        self.main_event = Event()
        self.interval = interval
        self.callback = callback

        self.daemon = True # stop if the program exits

        # start the thread (not the timer...)
        super(Timer, self).start()

    def run(self):
        while self.main_event.wait():
            while not self.interval_event.wait(self.interval):
                runner = RunnerThread(self.callback)
                runner.setDaemon(True)
                runner.start()

    def start(self, interval = None):
        if interval is not None:
            self.interval = interval
        self.interval_event.clear()
        self.main_event.set()

    def is_running(self):
        return not self.interval_event.is_set()

    def stop(self):
        self.interval_event.set()
