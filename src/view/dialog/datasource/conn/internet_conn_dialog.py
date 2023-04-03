# -*- coding: utf-8 -*-
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QFormLayout, QLabel, QLineEdit

from src.constant.ds_dialog_constant import HOST_TEXT, PORT_TEXT, USERNAME_TEXT, PWD_TEXT, \
    PORT_INPUT_PLACEHOLDER_TEXT, HOST_MAX_LENGTH_PLACEHOLDER_TEXT, USER_MAX_LENGTH_PLACEHOLDER_TEXT, \
    PWD_MAX_LENGTH_PLACEHOLDER_TEXT
from src.view.dialog.datasource.conn.conn_dialog_abc import ConnDialogABC

_author_ = 'luwt'
_date_ = '2022/9/27 18:05'


class InternetConnDialog(ConnDialogABC):
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

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_ds_content_info_ui(self):
        # 主体表单布局
        self.ds_info_layout = QFormLayout()
        # 主机地址
        self.host_label = QLabel(self.frame)
        self.host_value = QLineEdit(self.frame)
        self.ds_info_layout.addRow(self.host_label, self.host_value)

        # 开放扩展点，可以增加其他特有信息
        self.setup_special_conn_info_ui()

        # 端口号
        self.port_label = QLabel(self.frame)
        self.port_value = QLineEdit(self.frame)
        self.ds_info_layout.addRow(self.port_label, self.port_value)
        # 用户名
        self.user_label = QLabel(self.frame)
        self.user_value = QLineEdit(self.frame)
        self.ds_info_layout.addRow(self.user_label, self.user_value)
        # 密码
        self.pwd_label = QLabel(self.frame)
        self.pwd_value = QLineEdit(self.frame)
        self.ds_info_layout.addRow(self.pwd_label, self.pwd_value)

    def setup_special_conn_info_ui(self): ...

    def setup_conn_info_label(self):
        self.host_label.setText(HOST_TEXT)
        self.port_label.setText(PORT_TEXT)
        self.user_label.setText(USERNAME_TEXT)
        self.pwd_label.setText(PWD_TEXT)
        self.setup_special_conn_info_label()

    def setup_special_conn_info_label(self): ...

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def collect_conn_info_input(self):
        host = self.host_value.text()
        port = int(self.port_value.text()) if self.port_value.text() else ''
        user = self.user_value.text()
        pwd = self.pwd_value.text()
        other_conn_info = self.collect_special_conn_info()
        conn_param = host, port, user, pwd
        if other_conn_info:
            conn_param = *conn_param, *other_conn_info
        return conn_param

    def collect_special_conn_info(self) -> tuple: ...

    def connect_conn_info_signal(self):
        self.host_value.textEdited.connect(self.check_input)
        self.port_value.textEdited.connect(self.check_input)
        self.user_value.textEdited.connect(self.check_input)
        self.pwd_value.textEdited.connect(self.check_input)
        self.connect_special_conn_info_signal()

    def connect_special_conn_info_signal(self): ...

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def setup_other_input_limit_rule(self):
        # 设置端口号只能输入数字
        self.port_value.setValidator(QIntValidator())
        # 设置最多可输入字符数
        self.host_value.setMaxLength(100)
        self.user_value.setMaxLength(30)
        self.pwd_value.setMaxLength(50)
        self.setup_special_conn_info_input_limit_rule()

    def setup_special_conn_info_input_limit_rule(self): ...

    def setup_other_placeholder_text(self):
        self.port_value.setPlaceholderText(PORT_INPUT_PLACEHOLDER_TEXT)
        self.host_value.setPlaceholderText(HOST_MAX_LENGTH_PLACEHOLDER_TEXT)
        self.user_value.setPlaceholderText(USER_MAX_LENGTH_PLACEHOLDER_TEXT)
        self.pwd_value.setPlaceholderText(PWD_MAX_LENGTH_PLACEHOLDER_TEXT)
        self.setup_special_conn_info_placeholder_text()

    def setup_special_conn_info_placeholder_text(self): ...

    def setup_echo_other_data(self):
        self.host_value.setText(self.dialog_data.conn_info_type.host)
        self.port_value.setText(str(self.dialog_data.conn_info_type.port))
        self.user_value.setText(self.dialog_data.conn_info_type.user)
        self.pwd_value.setText(self.dialog_data.conn_info_type.pwd)
        self.setup_echo_special_conn_info_data()

    def setup_echo_special_conn_info_data(self): ...

    # ------------------------------ 后置处理 end ------------------------------ #
