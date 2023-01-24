import sys
import utils

if __name__ == '__main__':
    # TODO put right directory
    install_dir = 'PATH/TO/aov_manager'
    if not sys.path.__contains__(install_dir):
        sys.path.append(install_dir)

    # TODO import and start right tool
    import AOVManager
    from AOVManager import *
    from utils import *

    unload_packages(silent=True, packages=["AOVManager"])
    ltp = AOVManager()
    ltp.show()
