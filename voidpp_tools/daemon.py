
import sys, os, time, atexit
from signal import SIGTERM

from .logger_proxy import LoggerProxy

class Daemon(object):
    """
    A generic daemon class.

    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, pidfile, logger):
        self.logger = logger
        self.pidfile = pidfile


    def init(self):
        """
        Called before the daemonize, so useful some init before the fork, eg print the user config parse errors, etc...
        return False to stop the daemonize!
        """
        return (True, 'Ok')

    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as e:
            self.logger.error("Fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError as e:
            self.logger.error("Fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        with open(self.pidfile,'w+') as f:
            f.write("%s\n" % pid)

        sys.stdout = LoggerProxy(self.logger.info)
        sys.stderr = LoggerProxy(self.logger.error)

    def delpid(self):
        if os.path.exists(self.pidfile):
            os.remove(self.pidfile)

    def get_pid(self):
        pid = None

        try:
            with open(self.pidfile, 'r') as f:
                try:
                    pid = int(f.read().strip())
                except TypeError as e:
                    pid = None
        except IOError:
            pid = None

        return pid

    def is_running(self):

        pid = self.get_pid()

        if pid is None:
            return False

        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True

    def status(self):
        return 'Daemon is ' + ('running' if self.is_running() else 'not running')

    def start(self):
        """
        Start the daemon
        """

        if self.is_running():
            msg = "Daemon already running (pidfile:%s)" % self.pidfile
            self.logger.error(msg)
            return msg

        initres = self.init()

        if not initres[0]:
            return initres[1]

        # Start the daemon
        self.daemonize()
        return self.run()

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        pid = self.get_pid()

        if not pid:
            message = "Pidfile %s does not exist. Daemon not running?" % self.pidfile
            self.logger.error(message)
            return message # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                self.logger.error(err)
                sys.exit(1)

        return 'Daemon is stopped'

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """
