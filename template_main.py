import sys

if __name__ == '__main__':
    # TODO put right directory
    install_dir = 'PATH/TO/aov_manager'
    if not sys.path.__contains__(install_dir):
        sys.path.append(install_dir)

    modules = ["AOVManager", "AOVBehavior", "AOV"]

    from utils import *

    unload_packages(silent=True, packages=modules)

    for module in modules:
        importlib.import_module(module)

    from AOVManager import *

    try:
        aov_manager.close()
    except:
        pass
    aov_manager = AOVManager()
    aov_manager.show()

