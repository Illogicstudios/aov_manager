import importlib
from common import utils

utils.unload_packages(silent=True, package="aov_manager")
importlib.import_module("aov_manager")
from aov_manager.AOVManager import AOVManager
try:
    aov_manager.close()
except:
    pass
aov_manager = AOVManager()
aov_manager.show()
