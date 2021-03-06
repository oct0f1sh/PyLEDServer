import os, glob
import logging

logger = logging.getLogger('pyledserver.Plugins')
logger.setLevel(logging.DEBUG)

logger.debug('Scanning plugins/ for Python')

modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
__all__ = [os.path.basename(f)[:-3] for f in modules if not f.endswith("__init__.py")]

del os, glob, modules