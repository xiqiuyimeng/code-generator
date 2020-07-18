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
from PyQt5.QtWidgets import QDialog, QTreeWidgetItem

from constant import CONFIRM_TREE_HEADER_LABELS
from select_generator_ui import setup_tab_ui


class DisplaySelectedDialog(QDialog):

    def __init__(self, selected_data):
        super().__init__()
        self.dialog = self
        # 选中的数据，以此来渲染树
        self.selected_data = selected_data
        self._translate = _translate = QtCore.QCoreApplication.translate
        self.setup_ui()

    def setup_ui(self):
        self.dialog.setObjectName("Dialog")
        self.dialog.resize(791, 633)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(self.dialog)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.treeWidget = QtWidgets.QTreeWidget(self.widget)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
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
        self.first_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.first_buttonBox.setObjectName("first_buttonBox")

        self.verticalLayout_2.addWidget(self.first_splitter)
        self.verticalLayout.addWidget(self.widget)

        # 去掉窗口右上角的问号
        self.dialog.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)

        # 按钮响应事件
        self.first_buttonBox.accepted.connect(self.next_step)
        self.first_buttonBox.rejected.connect(self.dialog.close)
        self.make_tree()

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.dialog)

    def retranslateUi(self):
        self.dialog.setWindowTitle(self._translate("Dialog", "Dialog"))
        self.treeWidget.headerItem().setText(0, self._translate("Dialog", CONFIRM_TREE_HEADER_LABELS))
        self.first_buttonBox_2.button(QtWidgets.QDialogButtonBox.Ok).setText('关闭所有表')
        self.first_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText('下一步')
        self.first_buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText('取消')

    def make_tree(self):
        """根据选中数据构建树"""
        for conn_name, db_dict in self.selected_data.items():
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

    def next_step(self):
        # 隐藏树控件
        self.widget.hide()
        # 打开下一页
        if hasattr(self, 'widget_generator'):
            self.widget_generator.show()
        else:
            setup_tab_ui(self)

    def pre_step(self):
        # 隐藏选择生成器界面
        self.widget_generator.hide()
        # 展示树控件
        self.widget.show()

