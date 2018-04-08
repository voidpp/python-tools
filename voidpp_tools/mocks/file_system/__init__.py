import os
from contextlib import contextmanager
from functools import wraps

from voidpp_tools.compat import mock
from voidpp_tools.compat import FileNotFoundError

from .handlers import MockHandlers

def mockfs(data = {}, cwd = '/', user = 'douglas'):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            with FileSystem(data, cwd, user).mock():
                return func(*args, **kwargs)
        return wrapped
    return wrapper

class FileSystem(object):

    def __init__(self, data, cwd = '/', user = 'douglas'):
        self._data = data
        self.cwd = cwd
        self.user = user

    @contextmanager
    def mock(self):
        patchers = self.__create_patchers()

        for patcher in patchers:
            patcher.start()

        try:
            yield
        finally:
            for patcher in patchers:
                patcher.stop()

    def get_data(self, path):
        data = self._data
        for part in path.split(os.path.sep):
            if not len(part):
                continue
            try:
                data = data[part]
            except KeyError:
                return None
        return data

    def remove_data(self, path): # XXX: tests!
        data = self._data
        for part in path.split(os.path.sep):
            if not len(part):
                continue
            try:
                if not isinstance(data[part], dict):
                    del data[part]
                    return True
                data = data[part]
            except KeyError:
                return False
        return False

    def set_data(self, path, content, create_folders = False):
        data = self._data
        paths = path.strip(os.path.sep).split(os.path.sep)
        visited = []
        for part in paths[:-1]:
            visited.append(part)
            if part not in data:
                if create_folders:
                    data[part] = {}
                else:
                    raise FileNotFoundError("Cannot set data for '{}', because '/{}' does not exists!".format(path, os.path.join(*visited)))
            data = data[part]
        data[paths[-1]] = content

    def __collect_mocks(self, obj):
        functions = {}
        for name in dir(obj):
            func = getattr(obj, name)
            if hasattr(func, 'target_name'):
                functions[func.target_name] = func
        return functions

    def __create_patchers(self):
        functions = self.__collect_mocks(MockHandlers(self))

        patchers = []
        for name, function in functions.items():
            patcher = mock.patch(name, function)
            patchers.append(patcher)

        return patchers
