# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'confirm_select_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets, QtGui
import sip
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QTreeWidgetItem

from constant import CONFIRM_TREE_HEADER_LABELS


class DisplaySelectedDialog(QDialog):

    QtCore.pyqtSignal(object)

    def __init__(self, selected_data):
        super().__init__()
        self.dialog = self
        # 选中的数据，以此来渲染树
        self.selected_data = selected_data
        self._translate = _translate = QtCore.QCoreApplication.translate
        self.setup_ui()

    def setup_ui(self):
        self.dialog.setObjectName("Dialog")
        self.dialog.resize(600, 700)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_confirm = QtWidgets.QVBoxLayout()
        self.verticalLayout_confirm.setObjectName("verticalLayout_confirm")

        self.treeWidget = QtWidgets.QTreeWidget(self.dialog)
        self.treeWidget.setObjectName("treeWidget")
        self.verticalLayout_confirm.addWidget(self.treeWidget)
        # 树结构的字体设置
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(13)
        self.treeWidget.setFont(font)
        # 按钮
        self.buttonBox = QtWidgets.QDialogButtonBox(self.dialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)

        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_confirm.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.verticalLayout_confirm)
        # 去掉窗口右上角的问号
        self.dialog.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)

        # 按钮响应事件
        self.buttonBox.accepted.connect(self.accept_ok)
        self.buttonBox.rejected.connect(self.reject_ok)
        self.make_tree()
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.dialog)

    def retranslateUi(self):
        self.dialog.setWindowTitle(self._translate("Dialog", "Dialog"))
        self.treeWidget.headerItem().setText(0, self._translate("Dialog", CONFIRM_TREE_HEADER_LABELS))
        self.button_ok = self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
        self.button_ok.setText('下一步')
        self.button_cancel = self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel)
        self.button_cancel.setText('取消')

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

    def accept_ok(self):
        # 删除树控件
        self.verticalLayout.removeItem(self.verticalLayout_confirm)
        sip.delete(self.verticalLayout_confirm)
        # 展示日历控件
        self.calendarWidget = QtWidgets.QCalendarWidget(self.dialog)
        self.calendarWidget.setObjectName("calendarWidget")
        self.verticalLayout.addWidget(self.calendarWidget)
        print("接收")

    def reject_ok(self):
        print('拒绝')
        self.dialog.close()

