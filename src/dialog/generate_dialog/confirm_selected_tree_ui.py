# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTreeWidgetItem

from src.constant.constant import CONFIRM_TREE_HEADER_LABELS, COLLAPSE_BUTTON, \
    PROJECT_GENERATOR_BUTTON, CANCEL_BUTTON, EXPAND_BUTTON, PATH_GENERATOR_BUTTON
from src.scrollable_widget.scrollable_widget import MyTreeWidget

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
        self.widget = QtWidgets.QWidget(self.parent.generate_frame)
        self.widget.setObjectName("little_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tree_header_label = QtWidgets.QLabel(self.widget)
        self.tree_header_label.setObjectName("tree_header_label")
        self.verticalLayout_2.addWidget(self.tree_header_label)
        self.treeWidget = MyTreeWidget(self.widget)
        self.parent.treeWidget = self.treeWidget
        self.treeWidget.setObjectName("treeWidget")
        # 树控件背景透明
        self.treeWidget.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.verticalLayout_2.addWidget(self.treeWidget)

        # 按钮
        self.gridLayout_button = QtWidgets.QGridLayout()
        self.gridLayout_button.setObjectName("gridLayout_button")
        self.expand_collapse_button = QtWidgets.QPushButton(self.widget)
        self.expand_collapse_button.setObjectName("expand_collapse_button")
        self.gridLayout_button.addWidget(self.expand_collapse_button, 0, 0, 1, 1)
        self.button_blank = QtWidgets.QLabel(self.widget)
        self.button_blank.setObjectName("button_blank")
        self.gridLayout_button.addWidget(self.button_blank, 0, 1, 1, 1)
        self.path_generator_button = QtWidgets.QPushButton(self.widget)
        self.path_generator_button.setObjectName("path_generator_button")
        self.gridLayout_button.addWidget(self.path_generator_button, 0, 2, 1, 1)
        self.project_generator_button = QtWidgets.QPushButton(self.widget)
        self.project_generator_button.setObjectName("project_generator_button")
        self.gridLayout_button.addWidget(self.project_generator_button, 0, 3, 1, 1)
        self.cancel_button = QtWidgets.QPushButton(self.widget)
        self.cancel_button.setObjectName("cancel_button")
        self.gridLayout_button.addWidget(self.cancel_button, 0, 4, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_button)

        # 按钮响应事件
        self.expand_collapse_button.clicked.connect(self.expand_collapse)
        self.path_generator_button.clicked.connect(self.parent.select_path_generator)
        self.project_generator_button.clicked.connect(self.parent.select_project_generator)
        self.cancel_button.clicked.connect(self.parent.close)

        self.make_tree()

        self.retranslateUi()

    def make_tree(self):
        """根据选中数据构建树"""
        self.treeWidget.setIconSize(QSize(40, 30))
        conn_icon = QIcon(":icon/mysql_conn_icon.png")
        db_icon = QIcon(":icon/database_icon.png")
        tb_icon = QIcon(":icon/table_icon.png")
        col_icon = QIcon(":icon/column_icon.png")
        for conn_name, db_dict in self.parent.selected_data.items():
            conn_item = self.make_item(self.treeWidget, conn_name, conn_icon)
            for db_name, tb_dict in db_dict.items():
                db_item = self.make_item(conn_item, db_name, db_icon)
                for tb_name, cols in tb_dict.items():
                    tb_item = self.make_item(db_item, tb_name, tb_icon)
                    for col in cols:
                        self.make_item(tb_item, col[1], col_icon)
        self.treeWidget.expandAll()

    def make_item(self, parent, name, icon):
        item = QTreeWidgetItem(parent)
        item.setText(0, self._translate("Dialog", name))
        item.setIcon(0, QIcon(icon))
        return item

    def retranslateUi(self):
        self.parent.setWindowTitle(self._translate("Dialog", CONFIRM_TREE_HEADER_LABELS))
        self.treeWidget.headerItem().setHidden(True)
        self.tree_header_label.setText(CONFIRM_TREE_HEADER_LABELS)
        self.expand_collapse_button.setText(COLLAPSE_BUTTON)
        self.path_generator_button.setText(PATH_GENERATOR_BUTTON)
        self.project_generator_button.setText(PROJECT_GENERATOR_BUTTON)
        self.cancel_button.setText(CANCEL_BUTTON)

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

