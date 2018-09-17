import os
from io import StringIO, FileIO
from shutil import copyfile
from .utils import override
from voidpp_tools.compat import builtins, FileNotFoundError, FileExistsError, UnsupportedOperation

class stat_result(object):

    def __getattr__(self, name):
        return 0

class MockStringIO(StringIO):
    def __init__(self, filename, mock_fs, mode):
        super(MockStringIO, self).__init__()
        self._filename = filename
        self._mock_fs = mock_fs
        self._mode = mode
        self._loaded = False

    def _load(self):
        if self._loaded:
            return
        self._loaded = True
        data = self._mock_fs.get_data(self._filename)
        if self._mode.startswith('a') and data is None:
            data = u''
        super(MockStringIO, self).write(data)
        if self._mode.startswith('r'):
            self.seek(0)

    def read(self, n=None):
        if self._mode in ['w', 'wb']:
            raise UnsupportedOperation('not readable')
        self._load()
        return super(MockStringIO, self).read(n)

    def write(self, content):
        if self._mode in ['r', 'rb']:
            raise UnsupportedOperation('not writable')
        if self._mode.startswith('a'):
            self._load()
        super(MockStringIO, self).write(content)

    def close(self):
        self._mock_fs.set_data(self._filename, self.getvalue())
        super(MockStringIO, self).close()


class MockHandlers(object):

    def __init__(self, file_system):
        self._file_system = file_system

    def _path_exists(self, path, mode):
        if not mode.startswith('r'):
            path = os.path.dirname(path)
        if self._file_system.get_data(path) is None:
            return False
        return True

    def _isdir(self, path):
        return isinstance(self._file_system.get_data(path), dict)

    def _isfile(self, path):
        data = self._file_system.get_data(path)
        return False if (isinstance(data, dict) or data is None) else True

    @override(builtins + '.open')
    def open(self, filename, mode = 'r'):
        if not self._path_exists(filename, mode):
            raise FileNotFoundError("No such file or directory: '{}'".format(filename))

        return MockStringIO(filename, self._file_system, mode)

    @override('shutil.copyfile')
    def shutil_copyfile(self, src, dst, *, follow_symlinks=True):
        data = self._file_system.get_data(src)
        if not data:
            raise FileNotFoundError("No such file or directory: '{}'".format(src))
        self._file_system.set_data(dst, data)
        return dst

    @override('io.FileIO')
    def fileio(self, filename, mode = 'r'):
        if not self._path_exists(filename, mode):
            raise FileNotFoundError("No such file or directory: '{}'".format(filename))

        return MockStringIO(filename, self._file_system, mode)

    @override('os.listdir')
    def listdir(self, path):
        if not self._isdir(path):
            raise FileNotFoundError("[Errno 2] No such file or directory: '{}'".format(path))

        for name in self._file_system.get_data(path):
            yield name

    @override('os.path.exists')
    def exists(self, filename):
        return self._file_system.get_data(filename) is not None

    @override('os.getcwd')
    def getcwd(self):
        return self._file_system.cwd

    @override('os.path.expanduser')
    def expanduser(self, path):
        return os.path.normpath(path.replace("~", "/home/{}/".format(self._file_system.user)))

    @override('os.mkdir')
    def mkdir(self, path, mode=0o777):
        if self._file_system.get_data(path) is None:
            try:
                self._file_system.set_data(path, dict())
            except KeyError:
                raise FileNotFoundError("No such file or directory: '{}'".format(path))
        else:
            raise FileExistsError("File exists: '{}'".format(path))

    @override('os.path.isfile')
    def isfile(self, path):
        return self._isfile(path)

    @override('os.path.isdir')
    def isdir(self, path):
        return self._isdir(path)

    @override('os.chmod')
    def chmod(self, path, flags):
        # TODO: maybe implement?
        pass

    @override('os.stat')
    def stat(self, path):
        return stat_result()

    @override('os.remove')
    def remove(self, path):
        if not self._isfile(path):
            raise FileNotFoundError("No such file or directory: '{}'".format(path))
        self._file_system.remove_data(path)
