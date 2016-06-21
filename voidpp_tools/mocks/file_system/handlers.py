import os
from io import StringIO
from .utils import override
from voidpp_tools.compat import builtins, FileNotFoundError, FileExistsError, UnsupportedOperation

class MockStringIO(StringIO):
    def __init__(self, filename, mock_fs, mode):
        super(MockStringIO, self).__init__()
        self.__filename = filename
        self.__mock_fs = mock_fs
        self.__mode = mode
        self.__loaded = False

    def __load(self):
        if self.__loaded:
            return
        self.__loaded = True
        data = self.__mock_fs.get_data(self.__filename)
        if self.__mode.startswith('a') and data is None:
            data = u''
        super(MockStringIO, self).write(data)
        if self.__mode.startswith('r'):
            self.seek(0)

    def read(self, n=None):
        if self.__mode in ['w', 'wb']:
            raise UnsupportedOperation('not readable')
        self.__load()
        return super(MockStringIO, self).read(n)

    def write(self, content):
        if self.__mode in ['r', 'rb']:
            raise UnsupportedOperation('not writable')
        if self.__mode.startswith('a'):
            self.__load()
        super(MockStringIO, self).write(content)

    def close(self):
        self.__mock_fs.set_data(self.__filename, self.getvalue())
        super(MockStringIO, self).close()


class MockHandlers(object):

    def __init__(self, file_system):
        self.__file_system = file_system

    def __path_exists(self, path, mode):
        if not mode.startswith('r'):
            path = os.path.dirname(path)
        if self.__file_system.get_data(path) is None:
            return False
        return True

    @override(builtins + '.open')
    def open(self, filename, mode = 'r'):
        if not self.__path_exists(filename, mode):
            raise FileNotFoundError("No such file or directory: '{}'".format(filename))

        return MockStringIO(filename, self.__file_system, mode)

    @override('os.path.exists')
    def exists(self, filename):
        return self.__file_system.get_data(filename) is not None

    @override('os.getcwd')
    def getcwd(self):
        return self.__file_system.cwd

    @override('os.path.expanduser')
    def expanduser(self, path):
        return os.path.normpath(path.replace("~", "/home/{}/".format(self.__file_system.user)))

    @override('os.mkdir')
    def mkdir(self, path):
        if self.__file_system.get_data(path) is None:
            try:
                self.__file_system.set_data(path, dict())
            except KeyError:
                raise FileNotFoundError("No such file or directory: '{}'".format(path))
        else:
            raise FileExistsError("File exists: '{}'".format(path))

    @override('os.path.isfile')
    def isfile(self, path):
        data = self.__file_system.get_data(path)
        return False if (isinstance(data, dict) or data is None) else True

    @override('os.path.isdir')
    def isdir(self, path):
        return isinstance(self.__file_system.get_data(path), dict)
