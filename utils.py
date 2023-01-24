import sys


# Clear a layout recusrively
def clear_layout(layout):
    children = []
    for i in range(layout.count()):
        child = layout.itemAt(i).widget()
        if not child:
            clear_layout(layout.itemAt(i).layout())
        else:
            children.append(child)
    for child in children:
        child.deleteLater()


def unload_packages(silent=True, packages=None):
    if packages is None:
        packages = []

    # construct reload list
    reload_list = []
    for i in sys.modules.keys():
        for package in packages:
            if i.startswith(package):
                reload_list.append(i)

    # unload everything
    for i in reload_list:
        try:
            if sys.modules[i] is not None:
                del (sys.modules[i])
                if not silent:
                    print("Unloaded: %s" % i)
        except:
            pass
