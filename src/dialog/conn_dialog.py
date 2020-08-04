# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'conn_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
"""
添加、编辑连接对话框界面
"""

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

from src.constant.constant import EDIT_CONN_MENU, ADD_CONN_MENU, \
    SAVE_CONN_SUCCESS_PROMPT, CONN_NAME_EXISTS
from src.func.connection_function import test_connection
from src.little_widget.message_box import pop_ok, pop_fail
from src.sys.sys_info_storage.sqlite import Connection, update_conn, \
    add_conn, get_new_conn, check_name_available


class ConnDialog(QDialog):

    conn_signal = QtCore.pyqtSignal(object, Connection)

    def __init__(self, connection, dialog_title, gui, screen_rect):
        super().__init__()
        # 只是为了维护一个主窗口对象，方便其他操作
        self.gui_parent = gui
        self.dialog = self
        self.dialog_title = dialog_title
        self.connection = connection
        self._translate = QtCore.QCoreApplication.translate
        self.main_screen_rect = screen_rect
        self.setup_ui()

    def setup_ui(self):
        self.dialog.setObjectName("Dialog")
        # 当前窗口大小根据主窗口大小计算
        self.dialog.resize(self.main_screen_rect.width() * 0.4, self.main_screen_rect.height() * 0.5)
        # 字体
        self.setStyleSheet("#title{font-size:30px;font-family:楷体;font-weight:500;qproperty-alignment:AlignHCenter;}"
                           "QLabel,QLineEdit,QPushButton{font-size:18px;font-family:楷体;}"
                           "#frame{border-style:solid;border-radius:25px;background-color:Gainsboro;}")
        # 不透明度
        self.setWindowOpacity(0.95)
        # 隐藏窗口边框
        self.dialog.setWindowFlags(Qt.FramelessWindowHint)
        # 设置窗口背景透明
        self.dialog.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        self.verticalLayout_frame = QtWidgets.QVBoxLayout(self.dialog)
        self.verticalLayout_frame.setObjectName("verticalLayout_frame")
        self.frame = QtWidgets.QFrame(self.dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.top_blank = QtWidgets.QLabel(self.frame)
        self.top_blank.setText("")
        self.top_blank.setObjectName("top_blank")
        self.verticalLayout.addWidget(self.top_blank)
        self.title = QtWidgets.QLabel(self.frame)
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title)
        self.under_title_first_blank = QtWidgets.QLabel(self.frame)
        self.under_title_first_blank.setText("")
        self.under_title_first_blank.setObjectName("under_title_first_blank")
        self.verticalLayout.addWidget(self.under_title_first_blank)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.user_value = QtWidgets.QLineEdit(self.frame)
        self.user_value.setObjectName("user_value")
        self.gridLayout.addWidget(self.user_value, 6, 2, 1, 1)
        self.grid_layout_blank = QtWidgets.QLabel(self.frame)
        self.grid_layout_blank.setText("")
        self.grid_layout_blank.setObjectName("grid_layout_blank")
        self.gridLayout.addWidget(self.grid_layout_blank, 0, 1, 1, 1)
        self.name_check = QtWidgets.QLabel(self.frame)
        self.name_check.setObjectName("name_check")
        self.gridLayout.addWidget(self.name_check, 1, 2, 1, 1)
        self.host_value = QtWidgets.QLineEdit(self.frame)
        self.host_value.setObjectName("host_value")
        self.gridLayout.addWidget(self.host_value, 2, 2, 1, 1)
        self.host = QtWidgets.QLabel(self.frame)
        self.host.setObjectName("host")
        self.gridLayout.addWidget(self.host, 2, 0, 1, 1)
        self.user = QtWidgets.QLabel(self.frame)
        self.user.setObjectName("user")
        self.gridLayout.addWidget(self.user, 6, 0, 1, 1)
        self.passwd = QtWidgets.QLabel(self.frame)
        self.passwd.setObjectName("passwd")
        self.gridLayout.addWidget(self.passwd, 8, 0, 1, 1)
        self.port_value = QtWidgets.QLineEdit(self.frame)
        self.port_value.setObjectName("port_value")
        self.gridLayout.addWidget(self.port_value, 4, 2, 1, 1)
        self.conn_name = QtWidgets.QLabel(self.frame)
        self.conn_name.setObjectName("conn_name")
        self.gridLayout.addWidget(self.conn_name, 0, 0, 1, 1)
        self.passwd_value = QtWidgets.QLineEdit(self.frame)
        self.passwd_value.setObjectName("passwd_value")
        self.gridLayout.addWidget(self.passwd_value, 8, 2, 1, 1)
        self.conn_name_value = QtWidgets.QLineEdit(self.frame)
        self.conn_name_value.setObjectName("conn_name_value")
        self.gridLayout.addWidget(self.conn_name_value, 0, 2, 1, 1)
        self.port = QtWidgets.QLabel(self.frame)
        self.port.setObjectName("port")
        self.gridLayout.addWidget(self.port, 4, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.bottom_blank = QtWidgets.QLabel(self.frame)
        self.bottom_blank.setText("")
        self.bottom_blank.setObjectName("bottom_blank")
        self.verticalLayout.addWidget(self.bottom_blank)
        # 按钮
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.test_conn = QtWidgets.QPushButton(self.frame)
        self.test_conn.setObjectName("test_conn")
        self.gridLayout_2.addWidget(self.test_conn, 0, 0, 1, 1)
        self.button_blank = QtWidgets.QLabel(self.frame)
        self.button_blank.setObjectName("button_blank")
        self.gridLayout_2.addWidget(self.button_blank, 0, 1, 1, 1)
        self.ok = QtWidgets.QPushButton(self.frame)
        self.ok.setObjectName("ok")
        self.gridLayout_2.addWidget(self.ok, 0, 2, 1, 1)
        self.cancel = QtWidgets.QPushButton(self.frame)
        self.cancel.setObjectName("cancel")
        self.gridLayout_2.addWidget(self.cancel, 0, 3, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout_2)
        self.verticalLayout_frame.addWidget(self.frame)
        # 设置tab键的顺序
        self.dialog.setTabOrder(self.conn_name_value, self.host_value)
        self.dialog.setTabOrder(self.host_value, self.port_value)
        self.dialog.setTabOrder(self.port_value, self.user_value)
        self.dialog.setTabOrder(self.user_value, self.passwd_value)
        # 设置端口号只能输入数字
        self.port_value.setValidator(QtGui.QIntValidator())

        self.conn_name_value.textEdited.connect(self.check_input)
        self.host_value.textEdited.connect(self.check_input)
        self.port_value.textEdited.connect(self.check_input)
        self.user_value.textEdited.connect(self.check_input)
        self.passwd_value.textEdited.connect(self.check_input)

        # 测试连接按钮：点击触发测试mysql连接功能
        self.test_conn.clicked.connect(self.test_connection)
        # 确定按钮：点击触发添加连接记录到系统库中，并增加到展示界面
        self.ok.clicked.connect(self.handle_func)
        # 确定、测试连接按钮默认不可用，只有当输入框都有值才可用
        self.ok.setDisabled(True)
        self.test_conn.setDisabled(True)
        # 取消按钮：点击则关闭对话框
        self.cancel.clicked.connect(self.dialog.close)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.dialog)

    def retranslateUi(self):
        self.title.setText(self.dialog_title)
        self.conn_name.setText("连接名：")
        self.host.setText("主机：")
        self.port.setText("端口号：")
        self.user.setText("用户名：")
        self.passwd.setText("密码：")
        # 按钮
        self.test_conn.setText("测试连接")
        self.ok.setText("确定")
        self.cancel.setText("取消")
        # 回显
        if self.connection.id:
            self.conn_name_value.setText(self._translate("Dialog", self.connection.name))
            self.host_value.setText(self._translate("Dialog", self.connection.host))
            port = str(self.connection.port) if self.connection.port else None
            self.port_value.setText(self._translate("Dialog", port))
            self.user_value.setText(self._translate("Dialog", self.connection.user))
            self.passwd_value.setText(self._translate("Dialog", self.connection.pwd))
            self.ok.setDisabled(False)
            self.test_conn.setDisabled(False)
        else:
            self.host_value.setText(self._translate("Dialog", "localhost"))
            self.port_value.setText(self._translate("Dialog", "3306"))
            self.user_value.setText(self._translate("Dialog", "root"))

    def check_input(self):
        # 检查是否都有值
        conn = self.get_input()
        # 如果输入框都有值，那么就开放按钮，否则关闭
        if all(conn):
            self.ok.setDisabled(False)
            self.test_conn.setDisabled(False)
        else:
            self.ok.setDisabled(True)
            self.test_conn.setDisabled(True)

    def get_input_connection(self):
        return Connection(self.connection.id, *self.get_input())

    def get_input(self):
        conn_name = self.conn_name_value.text()
        host = self.host_value.text()
        port = int(self.port_value.text())
        user = self.user_value.text()
        pwd = self.passwd_value.text()
        return conn_name, host, port, user, pwd

    def test_connection(self):
        """测试连接"""
        new_conn = self.get_input_connection()
        test_connection(new_conn)

    def handle_func(self):
        """添加新的连接记录到系统库中，或编辑连接信息"""
        new_conn = self.get_input_connection()
        name_available = check_name_available(new_conn.name, self.connection.id)
        if name_available:
            if self.dialog_title == EDIT_CONN_MENU:
                update_conn(new_conn)
            elif self.dialog_title == ADD_CONN_MENU:
                add_conn(new_conn)
                new_conn = get_new_conn()
            pop_ok(self.dialog_title, SAVE_CONN_SUCCESS_PROMPT)
            self.dialog.close()
            self.conn_signal.emit(self.gui_parent, new_conn)
        else:
            pop_fail(self.dialog_title, CONN_NAME_EXISTS)
