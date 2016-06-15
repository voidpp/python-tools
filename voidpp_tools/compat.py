import sys
import importlib

def __compat(data):
    try:
        return data[sys.version_info.major]()
    except KeyError as e:
        raise Exception("Unhandled version: {}".format(sys.version_info.major))


mock = __compat({
    2: lambda: importlib.import_module('mock'),
    3: lambda: importlib.import_module('unittest.mock'),
})

builtins = __compat({
    2: lambda: '__builtin__',
    3: lambda: 'builtins',
})

FileNotFoundError = __compat({
    2: lambda: OSError,
    3: lambda: FileNotFoundError,
})

