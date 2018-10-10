import Plugins
import importlib
import threading
import inspect

divider = '\n------------------'

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
        print('Gathering plugins...')

        for plugin in Plugins.__all__:
            module = importlib.import_module('Plugins.' + plugin)
            
            for p_class in dir(module):
                obj = getattr(module, p_class)

                if inspect.isclass(obj) and issubclass(obj, threading.Thread):
                    try:
                        self.plugins.append(PluginInfo(obj))
                        print('Plugin found: \"{}\" with identifier: \"{}\"'.format(obj.p_name, obj.p_identifier))
                    except (AttributeError, ValueError) as err:
                        if isinstance(err, AttributeError):
                            print('Plugin: \"{}\" missing one or more required properties, ignoring...'.format(p_class))
                        elif isinstance(err, ValueError):
                            print('Plugin: \"{}\" contains a space in the identifier, ignoring...'.format(p_class))

        print(divider[1:])

    def get_plugin_thread(self, identifier, args, led_strip):
        if ' ' in identifier:
            print('PluginManager - SPACE FOUND IN MESSAGE, IGNORING...')
            raise ValueError

        for plugin in self.plugins:
            if plugin.identifier == identifier:
                print('PluginManager - Running plugin \"{}\"'.format(plugin.name) + divider)
                return plugin.obj(led_strip, args)

        print('PluginManager - INVALID PLUGIN IDENTIFIER IN MESSAGE')
        raise ValueError