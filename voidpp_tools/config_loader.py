import os
import abc
from .dict_utils import recursive_update

class ConfigLoaderException(Exception):
    pass

class ConfigFormatter(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def encode(self, data):
        """
            Args:
                data: any serializable python type

            Returns:
                The encoded string data
        """
        pass

    @abc.abstractmethod
    def decode(self, data):
        """
            Args:
                data (str): the raw data from the file

            Returns:
                Dict, list or any serializable python type
        """
        pass

class ConfigLoader(object):
    """
        Args:
            formatter (ConfigFormatter): config encode/decode interface instance
            base_path (str): a custom path which may be contains the config
            nested (bool): in case of true, load all the config files found in the sources and merges it
    """
    def __init__(self, formatter, base_path, nested = False):
        self.sources = [
            os.getcwd(),
            os.path.dirname(os.path.abspath(base_path)),
            os.path.expanduser('~'),
            '/etc',
        ]
        self.__loaded_config_file = None
        self.__formatter = formatter
        self.__nested = nested

    @property
    def filename(self):
        return self.__loaded_config_file

    def __search_config_files(self, filename):
        filenames = []
        tries = []
        for source in self.sources:
            file_path = os.path.join(source, filename)
            tries.append(file_path)
            if not os.path.exists(file_path):
                continue
            filenames.append(file_path)

        return filenames, tries

    def __load_config_files(self, filenames):
        data = dict()

        for filename in filenames:
            with open(filename) as f:
                recursive_update(data, self.__formatter.decode(f.read()))

        return data

    def load(self, filename, create = None, default_conf = {}):
        """Load the config file

        Args:
            filename (str): the filename of the config, without any path
            create (str): if the config file not found, and this parameter is not None,
                          a config file will be create with content of default_conf
            default_conf (dict): content of the default config data

        Returns:
            Return value of the ConfigFormatter.decode or the default_conf value

        Raises:
            ConfigLoaderException: if the config file not found

        """
        filenames, tries = self.__search_config_files(filename)

        if len(filenames):
            self.__loaded_config_file = filenames if self.__nested else filenames[0]
            return self.__load_config_files(filenames if self.__nested else filenames[:1])

        if create is not None:
            self.__loaded_config_file = os.path.join(create, filename)
            self.save(default_conf)
            return default_conf

        raise ConfigLoaderException("Config file not found in: %s" % tries)

    def save(self, data):
        """Save the config data

        Args:
            data: any serializable config data

        Raises:
            ConfigLoaderException: if the ConfigLoader.load not called, so there is no config file name,
                                   or the data is not serializable or the loader is nested
        """
        if self.__nested:
            raise ConfigLoaderException("Cannot save the config if the 'nested' paramter is True!")

        if self.__loaded_config_file is None:
            raise ConfigLoaderException("Load not called yet!")

        try:
            with open(self.__loaded_config_file, 'w') as f:
                f.write(self.__formatter.encode(data))
        except Exception as e:
            raise ConfigLoaderException("Config data is not serializable: %s" % e)
