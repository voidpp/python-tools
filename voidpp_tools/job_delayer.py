
from threading import Timer

class JobDelayer(object):
    """It will delaying the given job with the given timeout and if a delaying is already in progress reset the timeout

    Args:
        job (callable): callback
        timeout (float): timeout in seconds
    """

    def __init__(self, job: callable, timeout: float = 1):
        self._timeout = timeout
        self._job = job
        self._timer = None

    @property
    def timeout(self):
        return self._timeout

    def _fire(self):
        self._timer = None
        self._job()

    def start(self):
        """Starts the delayed execution"""

        if self._timer:
            self._timer.cancel()

        self._timer = Timer(self._timeout, self._fire)
        self._timer.start()
