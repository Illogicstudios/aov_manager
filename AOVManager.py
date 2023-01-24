import os
from functools import partial

import sys

from pymel.core import *
import maya.OpenMayaUI as omui

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from shiboken2 import wrapInstance

import utils

import maya.OpenMaya as OpenMaya


# CS mean create shaders part
# US mean update shaders part
class AOVManager(QtWidgets.QDialog):

    def __init__(self, prnt=wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)):
        super(AOVManager, self).__init__(prnt)
        # Model attributes

        # UI attributes
        self.__reinit_ui()

        # name the window
        self.setWindowTitle("AOV Manager")
        # make the window a "tool" in Maya's eyes so that it stays on top when you click off
        self.setWindowFlags(QtCore.Qt.Tool)
        # Makes the object get deleted from memory, not just hidden, when it is closed.
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Create the layout, linking it to actions and refresh the display
        self.__create_ui()
        self.__refresh_ui()
        self.__create_callback()

    # Create callbacks
    def __create_callback(self):
        pass
        # self.__selection_callback = \
        #     OpenMaya.MEventMessage.addEventCallback("SelectionChanged", self.on_selection_changed)

    # Remove callbacks
    def closeEvent(self, arg__1: QtGui.QCloseEvent) -> None:
        pass
        # OpenMaya.MMessage.removeCallback(self.__selection_callback)

    # initialize the ui
    def __reinit_ui(self):
        self.__ui_width = 500
        self.__ui_height = 300
        self.__ui_min_width = 300
        self.__ui_min_height = 200

    # Create the ui
    def __create_ui(self):
        # Reinit attributes of the UI
        self.__reinit_ui()
        self.setMinimumSize(self.__ui_min_width, self.__ui_min_height)
        self.resize(self.__ui_width, self.__ui_height)
        self.move(QtWidgets.QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())

        # Some aesthetic value
        size_btn = QtCore.QSize(180, 30)

        # asset_path = os.path.dirname(__file__) + "/assets/asset.png"

        # Main Layout
        main_lyt = QtWidgets.QVBoxLayout()
        main_lyt.setContentsMargins(10, 15, 10, 15)
        main_lyt.setSpacing(12)
        self.setLayout(main_lyt)

        ################################################################################################################

        # Layout ML.1
        lyt_1 = QtWidgets.QHBoxLayout()
        lyt_1.setAlignment(QtCore.Qt.AlignTop)
        main_lyt.addLayout(lyt_1, 1)

        # Separator ML.1 | ML.2
        sep = QtWidgets.QFrame()
        sep.setMinimumWidth(1)
        sep.setFixedWidth(2)
        sep.setFrameShape(QtWidgets.QFrame.VLine)
        sep.setFrameShadow(QtWidgets.QFrame.Sunken)
        sep.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        main_lyt.addWidget(sep)

        # Layout ML.2 : Update shaders
        lyt_2 = QtWidgets.QHBoxLayout()
        lyt_2.setAlignment(QtCore.Qt.AlignTop)
        main_lyt.addLayout(lyt_2, 1)

    # Refresh the ui according to the model attribute
    def __refresh_ui(self):
        self.refresh_btn()
        # [...]

    # Refresh the buttons
    def refresh_btn(self):
        pass
        # self.__ui_btn.setEnabled(True)
