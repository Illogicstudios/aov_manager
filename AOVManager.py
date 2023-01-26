import os
from functools import partial

import sys

from pymel.core import *
import maya.OpenMayaUI as omui

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from PySide2.QtWidgets import *
from PySide2.QtCore import *

from shiboken2 import wrapInstance

import utils

import maya.OpenMaya as OpenMaya


class AOVManager(QDialog):

    def __init__(self, prnt=wrapInstance(int(omui.MQtUtil.mainWindow()), QWidget)):
        super(AOVManager, self).__init__(prnt)

        # Model attributes
        self.__lights_selected = []
        self.__name_light_group_default = True
        self.__light_groups = {}
        self.__selection_lg = None
        self.__selection_lg_light = None

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
        self.__selection_callback = \
            OpenMaya.MEventMessage.addEventCallback("SelectionChanged", self.__on_selection_changed)
        self.__dag_callback = \
            OpenMaya.MEventMessage.addEventCallback("DagObjectCreated", self.__on_dag_changed)

    # Remove callbacks
    def closeEvent(self, arg__1: QtGui.QCloseEvent) -> None:
        OpenMaya.MMessage.removeCallback(self.__selection_callback)
        OpenMaya.MMessage.removeCallback(self.__dag_callback)

    # initialize the ui
    def __reinit_ui(self):
        self.__ui_width = 600
        self.__ui_height = 500
        self.__ui_min_width = 400
        self.__ui_min_height = 300

    # Create the ui
    def __create_ui(self):
        # Reinit attributes of the UI
        self.__reinit_ui()
        self.setMinimumSize(self.__ui_min_width, self.__ui_min_height)
        self.resize(self.__ui_width, self.__ui_height)
        self.move(QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())

        # Some aesthetic value
        size_btn = QtCore.QSize(180, 30)

        # asset_path = os.path.dirname(__file__) + "/assets/asset.png"

        # Main Layout
        main_lyt = QVBoxLayout()
        main_lyt.setSpacing(8)
        self.setLayout(main_lyt)
        tab_widget = QTabWidget()
        main_lyt.addWidget(tab_widget)

        ################################################### Tabs #######################################################

        # Layout Tab 1 : AOVs
        aovs_lyt = QGridLayout()
        aovs_lyt.setColumnStretch(0, 1)
        aovs_lyt.setColumnStretch(1, 1)
        aov_widget = QWidget()
        aov_widget.setLayout(aovs_lyt)
        tab_widget.addTab(aov_widget, "AOVs")

        # Layout Tab 2 : Lights
        lights_lyt = QGridLayout()
        lights_lyt.setColumnStretch(0, 2)
        lights_lyt.setColumnStretch(1, 3)
        light_widget = QWidget()
        light_widget.setLayout(lights_lyt)
        tab_widget.addTab(light_widget, "Light Groups")

        ############################################### Tab 1 : AOVs ###################################################

        # Widget ML.1.1 : Available AOVs
        available_aovs_title = QLabel("Available AOVs")
        available_aovs_title.setAlignment(Qt.AlignCenter)
        aovs_lyt.addWidget(available_aovs_title, 0, 0)
        # Widget ML.1.2 : Active AOVs
        active_aovs = QLabel("Active AOVs")
        active_aovs.setAlignment(Qt.AlignCenter)
        aovs_lyt.addWidget(active_aovs, 0, 1)

        # Widget ML.1.3 : List Available AOVs
        list_available_aovs_view = QListWidget()
        list_available_aovs_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        aovs_lyt.addWidget(list_available_aovs_view, 1, 0)
        # Widget ML.1.4 : List Active AOVs
        list_active_aovs_view = QListWidget()
        list_active_aovs_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        aovs_lyt.addWidget(list_active_aovs_view, 1, 1)

        # Widget ML.1.5 : Add AOV to active
        add_aov_to_active_btn = QPushButton(">>>")
        aovs_lyt.addWidget(add_aov_to_active_btn, 2, 0)
        # Widget ML.1.6: Remove AOV from Active
        remove_aov_to_active_btn = QPushButton("<<<")
        aovs_lyt.addWidget(remove_aov_to_active_btn, 2, 1)

        # Widget ML.1.6 : Fix name prefix checkbox
        fix_name_prefix_checkbox = QCheckBox("Fix name prefix \n<RenderLayout>/<Scene>/<Scene>")
        fix_name_prefix_checkbox.setChecked(True)
        aovs_lyt.addWidget(fix_name_prefix_checkbox, 3, 0)
        # Widget ML.1.7: DWAAB Compression checkbox
        dwaab_compression_checkbox = QCheckBox("DWAAB Compression")
        dwaab_compression_checkbox.setChecked(True)
        aovs_lyt.addWidget(dwaab_compression_checkbox, 3, 1)

        ############################################ Tab 2 : Light Groups ##############################################

        # Widget ML.2.1 : Lights title
        lights_title = QLabel("Lights")
        lights_title.setAlignment(Qt.AlignCenter)
        lights_lyt.addWidget(lights_title, 0, 0)
        # Widget ML.2.2 : Light groups title
        lg_title = QLabel("Light Groups AOV")
        lg_title.setAlignment(Qt.AlignCenter)
        lights_lyt.addWidget(lg_title, 0, 1)

        # Widget ML.2.3 : List Lights
        self.__ui_light_list_view = QListWidget()
        self.__ui_light_list_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.__ui_light_list_view.itemSelectionChanged.connect(self.__on_light_selection_changed)
        lights_lyt.addWidget(self.__ui_light_list_view, 1, 0)
        # Layout ML.2.4 : Light groups
        lg_lyt = QVBoxLayout()
        lights_lyt.addLayout(lg_lyt, 1, 1)
        # Layout ML.2.4.1 : Light group name
        lg_name_lyt = QHBoxLayout()
        lg_lyt.addLayout(lg_name_lyt, 1)
        # Widget ML.2.4.1.1 : Light group name prefix
        lg_prefix = QLabel("RGBA_")
        lg_name_lyt.addWidget(lg_prefix)
        # Widget ML.2.4.1.2 : Light group name edit
        self.__ui_lg_name_edit = QLineEdit("")
        self.__ui_lg_name_edit.textEdited.connect(self.__on_light_group_name_changed)
        lg_name_lyt.addWidget(self.__ui_lg_name_edit)
        # Widget ML.2.4.2 : Button create light group
        self.__ui_lg_create_btn = QPushButton("Create light group with selected lights")
        self.__ui_lg_create_btn.clicked.connect(self.__create_light_group)
        lg_lyt.addWidget(self.__ui_lg_create_btn)
        # Widget ML.2.4.3 : Tree List light group
        self.__ui_lg_tree_widget = QTreeWidget()
        self.__ui_lg_tree_widget.setHeaderHidden(True)
        self.__ui_lg_tree_widget.itemSelectionChanged.connect(self.__selection_lg_changed)
        lg_lyt.addWidget(self.__ui_lg_tree_widget)

        # Widget ML.2.5 : Add light to light group button
        self.__ui_add_selected_light_to_lg_btn = QPushButton("Add to light group selected")
        self.__ui_add_selected_light_to_lg_btn.setEnabled(False)
        self.__ui_add_selected_light_to_lg_btn.clicked.connect(self.__add_lights_to_light_group)
        lights_lyt.addWidget(self.__ui_add_selected_light_to_lg_btn, 2, 0)
        # Widget ML.2.6: Create a light group by light button
        create_lg_by_light_btn = QPushButton("Create a light group by light")
        create_lg_by_light_btn.clicked.connect(self.__create_light_group_by_light)
        lights_lyt.addWidget(create_lg_by_light_btn, 3, 0)

        # Widget ML.2.7 : Remove light or a light group button
        self.__ui_remove_selection_lg = QPushButton("Remove Selection")
        self.__ui_remove_selection_lg.setEnabled(False)
        self.__ui_remove_selection_lg.clicked.connect(self.__remove_selection_lg)
        lights_lyt.addWidget(self.__ui_remove_selection_lg, 2, 1)
        # Widget ML.2.8 : Remove all light groups button
        self.__ui_remove_all_lg_btn = QPushButton("Remove all")
        self.__ui_remove_all_lg_btn.setEnabled(False)
        self.__ui_remove_all_lg_btn.clicked.connect(self.__remove_all_light_groups)
        lights_lyt.addWidget(self.__ui_remove_all_lg_btn, 3, 1)

    @staticmethod
    def __get_all_lights():
        return ls(type=["light"] + listNodeTypes("light"), dag=True)

    def __on_selection_changed(self, *args, **kwargs):
        self.__refresh_ui()

    def __on_dag_changed(self, *args, **kwargs):
        self.__refresh_ui()

    # Refresh the ui according to the model attribute
    def __refresh_ui(self):
        self.__retrieve_light_groups()
        self.__refresh_lights_list()
        self.__refresh_light_group_name()
        self.__refresh_light_group_list()
        self.__refresh_btn()

    def __on_light_selection_changed(self):
        self.__lights_selected = []
        for item in self.__ui_light_list_view.selectedItems():
            self.__lights_selected.append(item.data(Qt.UserRole))
        self.__refresh_light_group_name()
        self.__refresh_btn()

    def __on_light_group_name_changed(self):
        self.__name_light_group_default = False

    def __create_light_group(self, lights=None, name=None):
        if lights is None:
            lights = self.__lights_selected

        if name is None:
            name = self.__ui_lg_name_edit.text()

        lights_filtered = []

        for l in lights:
            if "default" in l.aiAov.get():
                lights_filtered.append(l)

        self.__add_lights_to_light_group(lights_filtered, "RGBA_" + name)

        self.__retrieve_light_groups()
        self.__name_light_group_default = True
        self.__refresh_light_group_name()
        self.__refresh_light_group_list()
        self.__refresh_lights_list()
        self.__refresh_btn()

    def __create_light_group_by_light(self):
        lights = self.__get_all_lights()
        for light in lights:
            light = light.getTransform()
            self.__create_light_group([light], light.name())

    def __remove_all_light_groups(self):
        lights = self.__get_all_lights()
        for l in lights:
            l.aiAov.set("default")
        self.__retrieve_light_groups()
        self.__refresh_light_group_list()
        self.__refresh_lights_list()
        self.__refresh_btn()

    def __add_lights_to_light_group(self, lights = None, light_group = None):
        if lights is None:
            lights = self.__lights_selected

        if light_group is None:
            light_group = self.__selection_lg

        for light in lights:
            light.aiAov.set(light_group)

        self.__retrieve_light_groups()
        self.__selection_lg = None
        self.__selection_lg_light = None
        self.__refresh_light_group_list()
        self.__refresh_lights_list()
        self.__refresh_btn()

    def __refresh_lights_list(self):
        self.__ui_light_list_view.clear()
        lights = self.__get_all_lights()
        for l in lights:
            if "default" in l.aiAov.get():
                transform = l.getTransform()
                item = QtWidgets.QListWidgetItem()
                item.setText(transform.name())
                item.setData(Qt.UserRole, transform)
                self.__ui_light_list_view.addItem(item)

    def __retrieve_light_groups(self):
        lights = AOVManager.__get_all_lights()
        self.__light_groups = {}
        for l in lights:
            aov_light_group = l.aiAov.get()
            if "default" not in aov_light_group:
                if aov_light_group not in self.__light_groups:
                    self.__light_groups[aov_light_group] = []
                self.__light_groups[aov_light_group].append(l)
    def __refresh_light_group_list(self):
        tmp_selection_lg = self.__selection_lg
        tmp_selection_lg_light = self.__selection_lg_light

        self.__ui_lg_tree_widget.clear()

        for lg, lights in self.__light_groups.items():
            item = QtWidgets.QTreeWidgetItem([lg])
            item.setData(0,Qt.UserRole,lg)
            self.__ui_lg_tree_widget.addTopLevelItem(item)
            for light in lights:
                child = QtWidgets.QTreeWidgetItem([light.name()])
                child.setData(0,Qt.UserRole,light)
                item.addChild(child)
            item.setExpanded(True)
        self.__selection_lg = tmp_selection_lg
        self.__selection_lg_light = tmp_selection_lg_light

    def __refresh_light_group_name(self):
        if self.__name_light_group_default:
            if len(self.__lights_selected) > 0:
                name = self.__lights_selected[0].name()
                while "RGBA_"+name in self.__light_groups.keys():
                    if not name[-1].isdigit():
                        name += '1'
                    elif name[-1] == '9':
                        new_name = ""
                        len_name = len(name)
                        for i in range(len_name):
                            if i != len_name-1:
                                new_name+=name[i]
                        new_name += '1'
                        name = new_name
                    else:
                        new_name = ""
                        len_name = len(name)
                        for i in range(len_name):
                            if i != len_name-1:
                                new_name+=name[i]
                        new_name += str(int(name[-1])+1)
                        name = new_name
                self.__ui_lg_name_edit.setText(name)
            else:
                self.__ui_lg_name_edit.setText("")

    def __remove_selection_lg(self):
        if self.__selection_lg_light is not None:
            self.__selection_lg_light.aiAov.set("default")
        elif self.__selection_lg is not None:
            for light in self.__light_groups[self.__selection_lg]:
                light.aiAov.set("default")
        self.__retrieve_light_groups()
        self.__selection_lg = None
        self.__selection_lg_light = None
        self.__refresh_light_group_list()
        self.__refresh_lights_list()
        self.__refresh_btn()

    def __selection_lg_changed(self):
        item = self.__ui_lg_tree_widget.currentItem()
        if item is not None:
            selection = item.data(0,Qt.UserRole)
            if type(selection) == str:
                self.__selection_lg_light = None
                self.__selection_lg = selection
            else:
                self.__selection_lg_light = selection
                self.__selection_lg = item.parent().data(0,Qt.UserRole)
        else:
            self.__selection_lg_light = None
            self.__selection_lg = None
        self.__refresh_btn()

    # Refresh the buttons
    def __refresh_btn(self):
        self.__ui_lg_create_btn.setEnabled(len(self.__ui_lg_name_edit.text()) > 0)
        self.__ui_add_selected_light_to_lg_btn.setEnabled(len(self.__lights_selected) > 0 and self.__selection_lg is not None)
        self.__ui_remove_selection_lg.setEnabled(self.__selection_lg_light is not None or self.__selection_lg is not None)
        self.__ui_remove_all_lg_btn.setEnabled(len(self.__light_groups) > 0)

