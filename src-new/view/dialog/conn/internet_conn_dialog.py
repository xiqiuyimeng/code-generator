# -*- coding: utf-8 -*-
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QFormLayout, QLabel, QLineEdit

from constant.constant import HOST_TEXT, PORT_TEXT, USERNAME_TEXT, PWD_TEXT
from view.dialog.conn.abstract_conn_dialog import AbstractConnDialog

_author_ = 'luwt'
_date_ = '2022/9/27 18:05'


class InternetConnDialog(AbstractConnDialog):
    """
    网络连接数据库类型对话框，通过网络通信连接的数据库，
    必然包括：主机地址、端口、用户名、密码，
    可能有些数据库需要其他信息，在端口号与用户名之间开放扩展点
    """

    def __init__(self, *args):
        self.host_label: QLabel = ...
        self.host_value: QLineEdit = ...
        self.port_label: QLabel = ...
        self.port_value: QLineEdit = ...
        self.user_label: QLabel = ...
        self.user_value: QLineEdit = ...
        self.pwd_label: QLabel = ...
        self.pwd_value: QLineEdit = ...
        super().__init__(*args)

    def setup_conn_info_ui(self):
        # 主体表单布局
        self.conn_info_layout = QFormLayout()
        # 主机地址
        self.host_label = QLabel(self.frame)
        self.host_value = QLineEdit(self.frame)
        self.conn_info_layout.addRow(self.host_label, self.host_value)

        # 开放扩展点，可以增加其他特有信息
        self.setup_special_conn_info_ui()

        # 端口号
        self.port_label = QLabel(self.frame)
        self.port_value = QLineEdit(self.frame)
        self.conn_info_layout.addRow(self.port_label, self.port_value)
        # 用户名
        self.user_label = QLabel(self.frame)
        self.user_value = QLineEdit(self.frame)
        self.conn_info_layout.addRow(self.user_label, self.user_value)
        # 密码
        self.pwd_label = QLabel(self.frame)
        self.pwd_value = QLineEdit(self.frame)
        self.conn_info_layout.addRow(self.pwd_label, self.pwd_value)

    def setup_special_conn_info_ui(self): ...

    def setup_conn_info_label(self):
        self.host_label.setText(HOST_TEXT)
        self.port_label.setText(PORT_TEXT)
        self.user_label.setText(USERNAME_TEXT)
        self.pwd_label.setText(PWD_TEXT)

    def setup_conn_info_value_show(self):
        self.host_value.setText(self.connection.conn_info_type.host)
        self.port_value.setText(str(self.connection.conn_info_type.port))
        self.user_value.setText(self.connection.conn_info_type.user)
        self.pwd_value.setText(self.connection.conn_info_type.pwd)

    def collect_conn_info_input(self):
        host = self.host_value.text()
        port = int(self.port_value.text())
        user = self.user_value.text()
        pwd = self.pwd_value.text()
        other_conn_info = self.collect_other_conn_info()
        conn_param = host, port, user, pwd
        if other_conn_info:
            conn_param = *conn_param, *other_conn_info
        return conn_param

    def collect_other_conn_info(self) -> tuple: ...

    def setup_input_conn_info_limit_rule(self):
        # 设置端口号只能输入数字
        self.port_value.setValidator(QIntValidator())
        # 设置最多可输入字符数
        self.host_value.setMaxLength(100)
        self.user_value.setMaxLength(30)
        self.pwd_value.setMaxLength(50)

    def connect_conn_info_signal(self):
        self.host_value.textEdited.connect(self.check_input)
        self.port_value.textEdited.connect(self.check_input)
        self.user_value.textEdited.connect(self.check_input)
        self.pwd_value.textEdited.connect(self.check_input)
