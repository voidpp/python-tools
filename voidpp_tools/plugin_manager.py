
import importlib
import logging

logger = logging.getLogger(__name__)

class PluginDescriptor(object):

    def __init__(self, name, module_name, class_name, arguments):
        self.name = name
        self.module_name = module_name
        self.class_name = class_name
        self.arguments = arguments

    def __repr__(self):
        return "<PluginDescriptor: name={}, module={}, class={}, arguments={}>".format(
                self.name, self.module_name, self.class_name, self.arguments)

class PluginException(Exception):
    pass

class PluginManager(object):

    def __init__(self, descriptors: dict):
        self._descriptors = descriptors
        self._plugins = {}

    def _load_class(self, desc: PluginDescriptor):

        logger.debug("Try to import plugin from %s.%s", desc.module_name, desc.class_name)
        try:
            module = importlib.import_module(desc.module_name)
        except ImportError as e:
            msg = "Cannot import module '{}'".format(desc.module_name)
            logger.error(msg)
            raise PluginException(msg)

        try:
            plugin_class = getattr(module, desc.class_name)
        except AttributeError as e:
            msg = "Cannot import class '{}' from module".format(desc.class_name)
            logger.error(msg)
            raise PluginException(msg)

        return plugin_class

    def load(self, name):
        return self._load(self._descriptors[name])

    def _load(self, desc: PluginDescriptor):

        plugin_class = self._load_class(desc)

        logger.debug("Load plugin: %s", desc)

        instance = plugin_class(**desc.arguments)

        logger.debug("Plugin successfully created %s", instance)

        return instance

    def names(self):
        for name in self._descriptors:
            yield name

    def __getitem__(self, name):
        if name not in self._plugins:
            if name not in self._descriptors:
                raise KeyError("Missing key '{}'".format(name))
            self._plugins[name] = self.load(name)
        return self._plugins[name]

    def __contains__(self, name):
        return name in self._descriptors
