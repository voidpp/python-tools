import os
from io import StringIO
from .utils import override

class MockHandlers(object):

    def __init__(self, file_system):
        self.__file_system = file_system

    @override('builtins.open')
    def open(self, filename, mode = 'r'):
        data = self.__file_system.get_data(filename)
        if data is None:
            raise FileNotFoundError("No such file or directory: '{}'".format(filename))
        return StringIO(data)

    @override('os.path.exists')
    def exists(self, filename):
        return self.__file_system.get_data(filename) is not None

    @override('os.getcwd')
    def getcwd(self):
        return self.__file_system.cwd

    @override('os.path.expanduser')
    def expanduser(self, path):
        return os.path.normpath(path.replace("~", "/home/{}/".format(self.__file_system.user)))
