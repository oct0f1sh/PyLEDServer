import Plugins
import importlib
import threading
import inspect

for plugin in Plugins.__all__:
    print(plugin)
    module = importlib.import_module('Plugins.' + plugin)
    for p_class in dir(module):
        obj = getattr(module, p_class)

        if inspect.isclass(obj) and issubclass(obj, threading.Thread):
            print('\t{}: {}'.format(p_class, obj.message))