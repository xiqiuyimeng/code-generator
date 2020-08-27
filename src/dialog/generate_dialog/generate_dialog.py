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

from src.dialog.draggable_dialog import DraggableDialog
from src.dialog.generate_dialog.confirm_selected_tree_ui import TreeWidgetUI
from src.dialog.generate_dialog.path_generator_ui import PathGeneratorUI
from src.dialog.generate_dialog.project_generator_ui import ProjectGeneratorUI
from src.dialog.generate_result_dialog import GenerateResultDialog


class DisplaySelectedDialog(DraggableDialog):

    def __init__(self, gui, selected_data, screen_rect):
        super().__init__()
        # 维护主界面窗口对象
        self.gui = gui
        # 选中的数据，以此来渲染树
        self.selected_data = selected_data
        self._translate = _translate = QtCore.QCoreApplication.translate
        self.main_screen_rect = screen_rect
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("Dialog")
        # 当前窗口大小根据主窗口大小计算
        self.setFixedSize(self.main_screen_rect.width() * 0.8, self.main_screen_rect.height() * 0.8)
        # 获取当前窗口大小
        self.screen_rect = self.geometry()
        self.verticalLayout_frame = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_frame.setObjectName("verticalLayout_frame")
        self.generate_frame = QtWidgets.QFrame(self)
        self.generate_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.generate_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.generate_frame.setObjectName("generate_frame")
        # 建立布局
        self.verticalLayout = QtWidgets.QVBoxLayout(self.generate_frame)
        self.verticalLayout.setObjectName("verticalLayout")
        # 展示已选中数据的树结构
        self.tree_widget_ui = TreeWidgetUI(self)
        self.tree_widget = self.tree_widget_ui.widget
        self.verticalLayout.addWidget(self.tree_widget)
        self.verticalLayout_frame.addWidget(self.generate_frame)

        # 不透明度
        self.setWindowOpacity(0.95)
        # 隐藏窗口边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置窗口背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

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

    def generate(self, output_dict):
        dialog = GenerateResultDialog(self.gui, output_dict, self.selected_data, self.screen_rect)
        dialog.close_parent_signal.connect(self.close)
        dialog.exec()



