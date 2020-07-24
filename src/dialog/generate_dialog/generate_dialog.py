# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'confirm_select_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
"""
点击生成按钮，弹窗页面。
第一个页面为选择表字段展示页面。
第二个页面为生成器输出配置页面
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

from src.constant.constant import WARNING_TITLE, PARAM_WARNING_MSG
from src.dialog.generate_dialog.confirm_selected_tree_ui import TreeWidgetUI
from src.dialog.generate_dialog.path_generator_ui import PathGeneratorUI
from src.func.project_generator_input import check_params
from src.dialog.generate_dialog.project_generator_ui import ProjectGeneratorUI
from src.dialog.generate_result_dialog import GenerateResultDialog
from src.little_widget.message_box import pop_warning
from src.sys.settings.font import set_font


class DisplaySelectedDialog(QDialog):

    def __init__(self, gui, selected_data):
        super().__init__()
        self.dialog = self
        # 维护主界面窗口对象
        self.gui = gui
        # 选中的数据，以此来渲染树
        self.selected_data = selected_data
        # 输出配置，也就是在第二步中选择的数据
        self.output_config_dict = dict()
        self._translate = _translate = QtCore.QCoreApplication.translate
        self.setup_ui()

    def setup_ui(self):
        self.dialog.setObjectName("Dialog")
        # 固定大小，不允许缩放
        self.dialog.setFixedSize(1000, 800)
        # 设置字体
        self.dialog.setFont(set_font())
        # 建立布局
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        # 展示已选中数据的树结构
        self.tree_widget_ui = TreeWidgetUI(self)
        self.tree_widget = self.tree_widget_ui.widget
        self.verticalLayout.addWidget(self.tree_widget)

        # 去掉窗口右上角的问号
        self.dialog.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        QtCore.QMetaObject.connectSlotsByName(self.dialog)

    def select_project_generator(self):
        """选择项目生成器"""
        # 隐藏树控件
        self.tree_widget.hide()
        # 打开下一页
        if hasattr(self, 'project_generator_widget'):
            self.project_generator_widget.show()
        else:
            self.project_generator_widget = ProjectGeneratorUI(self).widget
            self.verticalLayout.addWidget(self.project_generator_widget)

    def select_path_generator(self):
        """选择路径生成器"""
        # 隐藏树控件
        self.tree_widget.hide()
        # 打开下一页
        if hasattr(self, 'path_generator_widget'):
            self.path_generator_widget.show()
        else:
            self.path_generator_widget = PathGeneratorUI(self).widget
            self.verticalLayout.addWidget(self.path_generator_widget)

    def generate(self):
        dialog = GenerateResultDialog(self.gui, self.output_config_dict, self.selected_data)
        dialog.close_parent_signal.connect(self.dialog.close)
        dialog.exec()



