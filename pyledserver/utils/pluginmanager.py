import plugins
import logging
import importlib
import inspect
import threading

logger = logging.getLogger('pyledserver.PluginManager')
logger.setLevel(logging.DEBUG)

class PluginInfo(object):
    def __init__(self, obj):
        if ' ' in obj.p_identifier:
            raise ValueError

        self.obj = obj

        self.identifier = obj.p_identifier
        self.name = obj.p_name
        self.author = obj.p_author
        self.expected_args = obj.p_expected_args

class PluginManager(object):
    def __init__(self):
        self.plugins = []
        self._get_plugins()

    def _get_plugins(self):
        """ Loads all plugins in plugins/ directory """
        logger.debug('Gathering plugins')

        for plugin in plugins.__all__:
            try:
                module = importlib.import_module('plugins.' + plugin)

                for plugin_class in dir(module):
                    obj = getattr(module, plugin_class)

                    if inspect.isclass(obj) and issubclass(obj, threading.Thread): # if plugin is subclass of Thread
                        try:
                            self.plugins.append(PluginInfo(obj))
                            logger.info('Plugin found: \"{}\" with identifier: \"{}\"'.format(obj.p_name, obj.p_identifier))
                        except (AttributeError, ValueError) as err:
                            if isinstance(err, AttributeError):
                                logger.exception('Plugin: \"{}\" missing one or more required properties, ignoring...'.format(plugin_class))
                            elif isinstance(err, ValueError):
                                logger.exception('Plugin: \"{}\" contains a space in the identifier, ignoring...'.format(plugin_class))

            except ModuleNotFoundError:
                            logger.warning('Could not load plugin: {}'.format(plugin))

    def get_plugin_thread(self, identifier, args, led_strip):
        if ' ' in identifier:
            logger.error('Space found in message, ignoring...')
            raise ValueError
        
        for plugin in self.plugins:
            if plugin.identifier == identifier:
                logger.info('Running plugin \"{}\"'.format(plugin.name))

                return plugin.obj(led_strip, args)

        logger.error('Invalid plugin identifier in message')
        raise ValueError