# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem

from src.constant.constant import CONFIRM_TREE_HEADER_LABELS, COLLAPSE_BUTTON, PROJECT_GENERATOR_BUTTON, CANCEL_BUTTON, \
    EXPAND_BUTTON, PATH_GENERATOR_BUTTON
from src.sys.settings.font import set_font

_author_ = 'luwt'
_date_ = '2020/7/23 15:51'


class TreeWidgetUI:
    """确认选中数据界面，负责将数据按树形展示"""

    def __init__(self, dialog):
        # 主窗口，树部件将会展示在主窗口中
        self.parent = dialog
        self._translate = self.parent._translate
        self.setup_tree_ui()

    def setup_tree_ui(self):
        self.widget = QtWidgets.QWidget(self.parent)
        self.widget.setObjectName("little_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.treeWidget = QtWidgets.QTreeWidget(self.widget)
        self.parent.treeWidget = self.treeWidget
        self.treeWidget.setObjectName("treeWidget")
        # 字体
        self.treeWidget.setFont(set_font())
        self.verticalLayout_2.addWidget(self.treeWidget)
        self.first_splitter = QtWidgets.QSplitter(self.widget)
        self.first_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.first_splitter.setObjectName("first_splitter")
        # 按钮
        self.first_buttonBox_2 = QtWidgets.QDialogButtonBox(self.first_splitter)
        self.first_buttonBox_2.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.first_buttonBox_2.setObjectName("first_buttonBox_2")
        self.first_buttonBox_2.setLayoutDirection(Qt.RightToLeft)
        self.first_buttonBox = QtWidgets.QDialogButtonBox(self.first_splitter)
        self.first_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel
                                                | QtWidgets.QDialogButtonBox.Ok
                                                | QtWidgets.QDialogButtonBox.Yes)
        self.first_buttonBox.setObjectName("first_buttonBox")
        self.verticalLayout_2.addWidget(self.first_splitter)

        # 按钮响应事件
        self.first_buttonBox.clicked.connect(self.first_buttonBox_func)
        self.first_buttonBox_2.accepted.connect(lambda: self.expand_collapse())
        self.make_tree()

        self.retranslateUi()

    def make_tree(self):
        """根据选中数据构建树"""
        for conn_name, db_dict in self.parent.selected_data.items():
            conn_item = self.make_item(self.treeWidget, conn_name)
            for db_name, tb_dict in db_dict.items():
                db_item = self.make_item(conn_item, db_name)
                for tb_name, cols in tb_dict.items():
                    tb_item = self.make_item(db_item, tb_name)
                    for col in cols:
                        self.make_item(tb_item, col)
        self.treeWidget.expandAll()

    def make_item(self, parent, name):
        item = QTreeWidgetItem(parent)
        item.setText(0, self._translate("Dialog", name))
        return item

    def retranslateUi(self):
        self.parent.setWindowTitle(self._translate("Dialog", "Dialog"))
        self.treeWidget.headerItem().setText(0, self._translate("Dialog", CONFIRM_TREE_HEADER_LABELS))
        self.expand_collapse_button = self.first_buttonBox_2.button(QtWidgets.QDialogButtonBox.Ok)
        self.parent.expand_collapse_button = self.expand_collapse_button
        self.expand_collapse_button.setText(COLLAPSE_BUTTON)
        self.first_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText(PROJECT_GENERATOR_BUTTON)
        self.first_buttonBox.button(QtWidgets.QDialogButtonBox.Yes).setText(PATH_GENERATOR_BUTTON)
        self.first_buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText(CANCEL_BUTTON)

    def expand_collapse(self):
        """提供给确认数据页，树结构的展开和折叠"""
        # 如果当前是展开，就关闭所有项，并将按钮文字改为展开所有，
        #  如果是关闭状态，就展开所有项，将按钮文字改为关闭所有
        if self.expand_collapse_button.text() == EXPAND_BUTTON:
            self.expand_collapse_button.setText(COLLAPSE_BUTTON)
            self.treeWidget.expandAll()
        else:
            self.expand_collapse_button.setText(EXPAND_BUTTON)
            self.treeWidget.collapseAll()

    def first_buttonBox_func(self, btn):
        """第一个按钮组功能，分发选择项目生成器、路径生成器、父窗口退出功能"""
        if btn.text() == PROJECT_GENERATOR_BUTTON:
            self.parent.select_project_generator()
        elif btn.text() == PATH_GENERATOR_BUTTON:
            self.parent.select_path_generator()
        elif btn.text() == CANCEL_BUTTON:
            self.parent.close()

