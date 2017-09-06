
import json
import os
import logging
from voidpp_tools.job_delayer import JobDelayer

logger = logging.getLogger(__name__)

class FileCacheHub(object):
    """Shared cache manager

    Args:
        cache_file_path (str):
        write_delay_timeout (float): delaying the file write (see JobDelayer)

    Example:
        from voidpp_tools.cache import FileCacheHub, CacheNode

        class MyCache1(CacheNode):
            def __init__(self, hub: FileCacheHub):
                super().__init__('mynode1', {}, hub)

            def get_custom_data(self, name):
                return self._data.get(name, None)

            def set_custom_data(self, name, value):
                self._data[name] = value
                self.save()

        class MyCache2(CacheNode):
            def __init__(self, hub: FileCacheHub):
                super().__init__('mynode2', [], hub)

            def get_list(self):
                return self._data

            def add(self, value):
                self._data.append(value)
                self.save()

        cache_hub = FileCacheHub('/tmp/mycache.json')

        cache1 = MyCache1(cache_hub)
        cache2 = MyCache2(cache_hub)

        cache1.set_custom_data('teve', 42)
        cache2.add(84)

        # ...

        # content of /tmp/mycache.json will be: '{"mynode1": {"teve": 42}, "mynode2": [84]}'

    Example:
        from voidpp_tools.cache import SimpleCache

        class MyCache(SimpleCache):
            def __init__(self, cache_file_path):
                super().__init__(cache_file_path, [])

            def get_list(self):
                return self._data

            def add(self, value):
                self._data.append(value)
                self.save()

        cache = MyCache('/tmp/mycache.json')
        cache.add(42)

        # ...

        # content of /tmp/mycache.json will be: '[42]'
    """

    def __init__(self, cache_file_path: str, write_delay_timeout: float = 1):
        logger.debug("Initialize FileCacheHub cache_file_path: %s, write_delay_timeout: %s", cache_file_path, write_delay_timeout)
        self._cache_file_path = cache_file_path
        self._data = {}
        if os.path.isfile(cache_file_path):
            logger.debug("Load file content from '%s'", cache_file_path)
            with open(cache_file_path) as f:
                self._data = json.load(f)

        self._delayed_writer = JobDelayer(self.flush, write_delay_timeout)

    def flush(self):
        logger.debug("Write cache to %s", self._cache_file_path)
        with open(self._cache_file_path, 'w') as f:
            json.dump(self._data, f)

    def _set_data(self, path: str, value, force):
        if path:
            data = self._data
            parts = path.split('.')

            for part in parts[:-1]:
                if part not in data:
                    data[part] = {}
                data = data[part]

            last_part = parts[-1:][0]

            if last_part not in data or force:
                data[last_part] = value

            data = data[last_part]

            return data
        else:
            if not self._data or force:
                self._data = value
            return self._data

    def get_node_data(self, path = '', default = None):
        return self._set_data(path, default, False)

    def save_node_data(self, path: str, data):
        self._set_data(path, data, True)

        if self._delayed_writer.timeout:
            self._delayed_writer.start()
        else:
            self.flush()


class CacheNode(object):
    """Base class for shared
    """

    def __init__(self, path, default_data, hub: FileCacheHub):
        self._path = path
        self._hub = hub
        self._data = hub.get_node_data(path, default_data)

    def save(self):
        self._hub.save_node_data(self._path, self._data)


class SimpleCache(CacheNode):
    """Base class for a simple cache, with a hidden hub.

    If there is no multiple cache data, use this.

    Args:
        cache_file_path (str): writeable file path
        default_data: default data
        write_delay_timeout (float): see FileCacheHub
    """

    def __init__(self, cache_file_path, default_data, write_delay_timeout = 1):
        super().__init__('', default_data, FileCacheHub(cache_file_path, write_delay_timeout))
